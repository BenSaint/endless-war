import MySQLdb
import datetime
import time
import re
import random

import discord

import ewcfg
from ew import EwUser

db_pool = {}
db_pool_id = 0

class Message:
	# Send the message to this exact channel by name.
	channel = None

	# Send the message to the channel associated with this point of interest.
	id_poi = None

	# Should this message echo to adjacent points of interest?
	reverb = None
	message = ""

	def __init__(
		self,
		channel = None,
		reverb = False,
		message = "",
		id_poi = None
	):
		self.channel = channel
		self.reverb = reverb
		self.message = message
		self.id_poi = id_poi

def readMessage(fname):
	msg = Message()

	try:
		f = open(fname, "r")
		f_lines = f.readlines()

		count = 0
		for line in f_lines:
			line = line.rstrip()
			count += 1
			if len(line) == 0:
				break

			args = line.split('=')
			if len(args) == 2:
				field = args[0].strip().lower()
				value = args[1].strip()

				if field == "channel":
					msg.channel = value.lower()
				elif field == "poi":
					msg.poi = value.lower()
				elif field == "reverb":
					msg.reverb = True if (value.lower() == "true") else False
			else:
				count -= 1
				break

		for line in f_lines[count:]:
			msg.message += (line.rstrip() + "\n")
	except:
		logMsg('failed to parse message.')
		traceback.print_exc(file = sys.stdout)
	finally:
		f.close()

	return msg

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
def formatNiceList(names = [], conjunction = "and"):
	l = len(names)

	if l == 0:
		return ''

	if l == 1:
		return names[0]
	
	return ', '.join(names[0:-1]) + '{comma} {conj} '.format(comma = (',' if l > 2 else ''), conj = conjunction) + names[-1]

""" turn a list of Users into a list of their respective names """
def userListToNameString(list_user):
	names = []

	for user in list_user:
		names.append(user.display_name)

	return formatNiceList(names)

""" turn a list of Roles into a map of name = >Role """
def getRoleMap(roles):
	roles_map = {}

	for role in roles:
		roles_map[mapRoleName(role.name)] = role

	return roles_map

""" canonical lowercase no space name for a role """
def mapRoleName(roleName):
	return roleName.replace(" ", "").lower()

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
			'conn': MySQLdb.connect(host = "localhost", user = "rfck-bot", passwd = "rfck", db = "rfck", charset = "utf8"),
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

""" format responses with the username: """
def formatMessage(user_target, message):
	return "*{}*: {}".format(user_target.display_name, message).replace("@", "\{at\}")

""" decay slime totals for all users """
def decaySlimes(id_server = None):
	if id_server != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			cursor.execute("SELECT id_user, slimes FROM users WHERE id_server = %s AND {slimes} > 1".format(
				slimes = ewcfg.col_slimes
			), (
				id_server,
			))

			users = cursor.fetchall()

			for user in users:
				slimes = user[1]
				slimes_to_decay = slimes - (slimes * (.5 ** (ewcfg.update_market / ewcfg.slime_half_life)))

				#round up or down, randomly weighted
				remainder = slimes_to_decay - int(slimes_to_decay)
				if random.random() < remainder: 
					slimes_to_decay += 1 
				slimes_to_decay = int(slimes_to_decay)

				if slimes_to_decay >= 1:
					cursor.execute("UPDATE users SET {slimes} = {slimes} - {decay} WHERE {id_server} = %s AND {id_user} = %s".format(
						slimes = ewcfg.col_slimes,
						decay = slimes_to_decay,
						id_server = ewcfg.col_id_server,
						id_user = ewcfg.col_id_user
					), (
						id_server,
						user[0]
					))
					#logMsg("decayed {} slimes from user ID: {}".format(slimes_to_decay, user[0]))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			databaseClose(conn_info)		

""" Increase hunger for every player in the server. """
def pushupServerHunger(id_server = None):
	if id_server != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save data
			cursor.execute("UPDATE users SET {hunger} = {hunger} + {tick} WHERE life_state > 0 AND id_server = %s AND hunger < {limit}".format(
				hunger = ewcfg.col_hunger,
				tick = ewcfg.hunger_pertick,
				limit = ewcfg.hunger_max
			), (
				id_server,
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			databaseClose(conn_info)

""" Reduce inebriation for every player in the server. """
def pushdownServerInebriation(id_server = None):
	if id_server != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save data
			cursor.execute("UPDATE users SET {inebriation} = {inebriation} - {tick} WHERE id_server = %s AND {inebriation} > {limit}".format(
				inebriation = ewcfg.col_inebriation,
				tick = ewcfg.inebriation_pertick,
				limit = 0
			), (
				id_server,
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			databaseClose(conn_info)

""" Parse a list of tokens and return an integer value. If allow_all, return -1 if the word 'all' is present. """
def getIntToken(tokens = [], allow_all = False):
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
def weaponskills_get(id_server = None, id_user = None, member = None):
	weaponskills = {}

	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			cursor.execute("SELECT {weapon}, {weaponskill}, {weaponname} FROM weaponskills WHERE {id_server} = %s AND {id_user} = %s".format(
				weapon = ewcfg.col_weapon,
				weaponskill = ewcfg.col_weaponskill,
				weaponname = ewcfg.col_name,
				id_server = ewcfg.col_id_server,
				id_user = ewcfg.col_id_user
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
			cursor.close()
			databaseClose(conn_info)

	return weaponskills

""" Set an individual weapon skill value for a player. """
def weaponskills_set(id_server = None, id_user = None, member = None, weapon = None, weaponskill = 0, weaponname = ""):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None and weapon != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			cursor.execute("REPLACE INTO weaponskills({id_server}, {id_user}, {weapon}, {weaponskill}, {weaponname}) VALUES(%s, %s, %s, %s, %s)".format(
				id_server = ewcfg.col_id_server,
				id_user = ewcfg.col_id_user,
				weapon = ewcfg.col_weapon,
				weaponskill = ewcfg.col_weaponskill,
				weaponname = ewcfg.col_name
			), (
				id_server,
				id_user,
				weapon,
				weaponskill,
				weaponname
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			databaseClose(conn_info)

""" Clear all weapon skills for a player (probably called on death). """
def weaponskills_clear(id_server = None, id_user = None, member = None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		try:
			conn_info = databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Clear any records that might exist.
			cursor.execute("UPDATE weaponskills SET {weaponskill} = %s WHERE {weaponskill} > %s AND {id_server} = %s AND {id_user} = %s".format(
				weaponskill = ewcfg.col_weaponskill,
				id_server = ewcfg.col_id_server,
				id_user = ewcfg.col_id_user
			), (
				ewcfg.weaponskill_max_onrevive,
				ewcfg.weaponskill_max_onrevive,
				id_server,
				id_user
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			databaseClose(conn_info)


re_flattener = re.compile("[ '\"!@#$%^&*().,/?{}\[\];:]")

"""
	Turn an array of tokens into a single word (no spaces or punctuation) with all lowercase letters.
"""
def flattenTokenListToString(tokens):
	global re_flattener
	target_name = ""

	if type(tokens) == list:
		for token in tokens:
			if token.startswith('<@') == False:
				target_name += re_flattener.sub("", token.lower())
	elif tokens.startswith('<@') == False:
		target_name = re_flattener.sub("", tokens.lower())

	return target_name


"""
	Execute a given sql_query. (the purpose of this function is to minimize repeated code and keep functions readable)
"""
def execute_sql_query(sql_query = None):
	data = None

	try:
		conn_info = databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()
		cursor.execute(sql_query, None)
		if sql_query.lower().startswith("select"):
			data = cursor.fetchall()
		conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		databaseClose(conn_info)

	return data


"""
	Send a message to multiple chat channels at once.
"""
async def post_in_multiple_channels(message = None, channels = None, client = None):
	for channel in channels:
		if channel.type == discord.ChannelType.text:
			await client.send_message(channel, message)
	return

"""
	Find a chat channel by name in a server.
"""
def get_channel(server = None, channel_name = ""):
	channel = None
	for chan in server.channels:
		if chan.name == channel_name:
			channel = chan

	return channel
