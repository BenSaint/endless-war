import MySQLdb
import datetime
import time

import ewcfg

db_pool = {}
db_pool_id = 0

""" Write the string to stdout with a timestamp. """
def logMsg(string):
	print("[{}] {}".format(datetime.datetime.now(), string))

	return string

""" read a file named fname and return its contents as a string """
def getValueFromFileContents(fname):
	token = ""

	try:
		f_token = open(fname, "r")
		f_token_lines = f_token.readlines()

		for line in f_token_lines:
			line = line.rstrip()
			if len(line) > 0:
				token = line
	except IOError:
		token = ""
		print("Could not read {} file.".format(fname))
	finally:
		f_token.close()

	return token

""" get the Discord API token from the config file on disk """
def getToken():
	return getValueFromFileContents("token")

""" get the Twitch client ID from the config file on disk """
def getTwitchClientId():
	return getValueFromFileContents("twitch_client_id")

""" print a list of strings with nice comma-and grammar """
def formatNiceList(names=[], conjunction="and"):
	l = len(names)

	if l == 0:
		return ''

	if l == 1:
		return names[0]
	
	return ', '.join(names[0:-1]) + '{comma} {conj} '.format(comma=(',' if l > 2 else ''), conj=conjunction) + names[-1]

""" turn a list of Users into a list of their respective names """
def userListToNameString(list_user):
	names = []

	for user in list_user:
		names.append(user.display_name)

	return formatNiceList(names)

""" turn a list of Roles into a map of name=>Role """
def getRoleMap(roles):
	roles_map = {}

	for role in roles:
		roles_map[role.name.replace(" ", "").lower()] = role

	return roles_map

""" connect to the database """
def databaseConnect():
	conn_info = None

	conn_id_todelete = []

	global db_pool
	global db_pool_id

	# Iterate through open connections and find the currently active one.
	for pool_id in db_pool:
		conn_info_iter = db_pool.get(pool_id)

		if conn_info_iter['closed'] == True:
			if conn_info_iter['count'] <= 0:
				conn_id_todelete.append(pool_id)
		else:
			conn_info = conn_info_iter

	# Close and remove dead connections.
	if len(conn_id_todelete) > 0:
		for pool_id in conn_id_todelete:
			conn_info_iter = db_pool[pool_id]
			conn_info_iter['conn'].close()

			del db_pool[pool_id]

	# Create a new connection.
	if conn_info == None:
		db_pool_id += 1
		conn_info = {
			'conn': MySQLdb.connect(host="localhost", user="rfck-bot", passwd="rfck", db="rfck"),
			'created': int(time.time()),
			'count': 1,
			'closed': False
		}
		db_pool[db_pool_id] = conn_info
	else:
		conn_info['count'] += 1

	return conn_info

""" close (maybe) the active database connection """
def databaseClose(conn_info):
	conn_info['count'] -= 1

	# Expire old database connections.
	if (conn_info['created'] + 60) < int(time.time()):
		conn_info['closed'] = True

""" get the slime count for the specified member (player). sets to 0 if they aren't in the database """
def getSlimesForPlayer(conn, cursor, member):
	user_slimes = 0

	cursor.execute("SELECT slimes FROM users WHERE id_user = %s AND id_server = %s", (member.id, member.server.id))
	result = cursor.fetchone();

	if result == None:
		cursor.execute("REPLACE INTO users(id_user, id_server) VALUES(%s, %s)", (member.id, member.server.id))
	else:
		user_slimes = result[0]

	return user_slimes

""" dump help document """
def getHelpText():
	text = ""

	try:
		f_help = open("help", "r")
		lines = f_help.readlines()

		for line in lines:
			text = text + line

	except IOError:
		text = ""
		print("Could not read help file.")
	finally:
		f_help.close()

	return text

""" format responses with the username: """
def formatMessage(user_target, message):
	return "*{}*: {}".format(user_target.display_name, message)

""" Returns the latest value, so that short PvP timer actions don't shorten remaining PvP time. """
def calculatePvpTimer(current_time_expirpvp, desired_time_expirpvp):
	if desired_time_expirpvp > current_time_expirpvp:
		return desired_time_expirpvp

	return current_time_expirpvp

""" Returns an array of the most recent counts of all invested slime coin, from newest at 0 to oldest. """
def getRecentTotalSlimeCoins(id_server=None, count=2, conn=None, cursor=None):
	if id_server != None:
		our_cursor = False
		our_conn = False

		values = []

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			count = int(count)
			cursor.execute("SELECT {} FROM stats WHERE {} = %s ORDER BY {} DESC LIMIT %s".format(
				ewcfg.col_total_slimecredit,
				ewcfg.col_id_server,
				ewcfg.col_timestamp
			), (
				id_server,
				(count if (count > 0) else 2)
			))

			for row in cursor.fetchall():
				values.append(row[0])

			# Make sure we return at least one value.
			if len(values) == 0:
				values.append(0)

			# If we don't have enough data, pad out to count with the last value in the array.
			value_last = values[-1]
			while len(values) < count:
				values.append(value_last)
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

		return values

""" Reduce stamina (relieve fatigue) for every player in the server. """
def pushupServerStamina(id_server = None, conn = None, cursor = None):
	if id_server != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Save data
			cursor.execute("UPDATE users SET {stamina} = {stamina} + {tick} WHERE id_server = %s AND stamina < {limit}".format(
				stamina = ewcfg.col_stamina,
				tick = ewcfg.stamina_pertick,
				limit = ewcfg.stamina_max
			), (
				id_server,
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

""" Reduce inebriation for every player in the server. """
def pushdownServerInebriation(id_server = None, conn = None, cursor = None):
	if id_server != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Save data
			cursor.execute("UPDATE users SET {inebriation} = {inebriation} - {tick} WHERE id_server = %s AND {inebriation} > {limit}".format(
				inebriation = ewcfg.col_inebriation,
				tick = ewcfg.inebriation_pertick,
				limit = 0
			), (
				id_server,
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

""" Save a timestamped snapshot of the current market for historical purposes. """
def persistMarketHistory(market_data=None, conn=None, cursor=None):
	if market_data != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Save data
			cursor.execute("INSERT INTO stats({}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, (SELECT sum({}) FROM users WHERE {} = %s), (SELECT sum({}) FROM users WHERE {} = %s), (SELECT count(*) FROM users WHERE {} = %s), (SELECT count(*) FROM users WHERE {} = %s AND {} > %s))".format(
				# Insert columns
				ewcfg.col_id_server,
				ewcfg.col_slimes_casino,
				ewcfg.col_rate_market,
				ewcfg.col_rate_exchange,
				ewcfg.col_total_slime,
				ewcfg.col_total_slimecredit,
				ewcfg.col_total_players,
				ewcfg.col_total_players_pvp,

				# Inner queries
				ewcfg.col_slimes,
				ewcfg.col_id_server,
				ewcfg.col_slimecredit,
				ewcfg.col_id_server,
				ewcfg.col_id_server,
				ewcfg.col_id_server,
				ewcfg.col_time_expirpvp
			), (
				market_data.id_server,
				market_data.slimes_casino,
				market_data.rate_market,
				market_data.rate_exchange,
				market_data.id_server,
				market_data.id_server,
				market_data.id_server,
				market_data.id_server,
				int(time.time())
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)


""" Parse a list of tokens and return an integer value. If allow_all, return -1 if the word 'all' is present. """
def getIntToken(tokens=[], allow_all=False):
	value = None

	for token in tokens[1:]:
		try:
			value = int(token.replace(",", ""))
			if value < 0:
				value = None
			break
		except:
			if allow_all and ("{}".format(token)).lower() == 'all':
				value = -1
			else:
				value = None

	return value

""" Get the map of weapon skills for the specified player. """
def weaponskills_get(id_server=None, id_user=None, member=None, conn=None, cursor=None):
	weaponskills = {}

	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			cursor.execute("SELECT {weapon}, {weaponskill}, {weaponname} FROM weaponskills WHERE {id_server} = %s AND {id_user} = %s".format(
				weapon=ewcfg.col_weapon,
				weaponskill=ewcfg.col_weaponskill,
				weaponname=ewcfg.col_name,
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user
			), (
				id_server,
				id_user
			))

			data = cursor.fetchall()
			if data != None:
				for row in data:
					weaponskills[row[0]] = {
						'skill': row[1],
						'name': row[2]
					}
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

	return weaponskills

""" Set an individual weapon skill value for a player. """
def weaponskills_set(id_server=None, id_user=None, member=None, weapon=None, weaponskill=0, weaponname="", conn=None, cursor=None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None and weapon != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			cursor.execute("REPLACE INTO weaponskills({id_server}, {id_user}, {weapon}, {weaponskill}, {weaponname}) VALUES(%s, %s, %s, %s, %s)".format(
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user,
				weapon=ewcfg.col_weapon,
				weaponskill=ewcfg.col_weaponskill,
				weaponname=ewcfg.col_name
			), (
				id_server,
				id_user,
				weapon,
				weaponskill,
				weaponname
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

""" Clear all weapon skills for a player (probably called on !revive). """
def weaponskills_clear(id_server=None, id_user=None, member=None, conn=None, cursor=None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Clear any records that might exist.
			cursor.execute("UPDATE weaponskills SET {weaponskill} = %s WHERE {weaponskill} > %s AND {id_server} = %s AND {id_user} = %s".format(
				weaponskill=ewcfg.col_weaponskill,
				id_server=ewcfg.col_id_server,
				id_user=ewcfg.col_id_user
			), (
				ewcfg.weaponskill_max_onrevive,
				ewcfg.weaponskill_max_onrevive,
				id_server,
				id_user
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				databaseClose(conn_info)

""" add the PvP flag role to a member """
async def add_pvp_role(cmd = None):
	member = cmd.message.author
	roles_map_user = getRoleMap(member.roles)

	if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
		await cmd.client.add_roles(member, cmd.roles_map[ewcfg.role_copkillers_pvp])
	elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
		await cmd.client.add_roles(member, cmd.roles_map[ewcfg.role_rowdyfuckers_pvp])
	elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
		await cmd.client.add_roles(member, cmd.roles_map[ewcfg.role_juvenile_pvp])
	elif ewcfg.role_corpse in roles_map_user and ewcfg.role_corpse_pvp not in roles_map_user:
		await cmd.client.add_roles(member, cmd.roles_map[ewcfg.role_corpse_pvp])
