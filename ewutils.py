import MySQLdb
import re

# Regex to match the score count in a user's nickname.
re_slimescore = re.compile('^[0-9]{5,} +(.*)$');


""" get the API token from the config file on disk """
def getToken():
	token = ""

	try:
		f_token = open("token", "r")
		f_token_lines = f_token.readlines()

		for line in f_token_lines:
			line = line.rstrip()
			if len(line) > 0:
				token = line
	except IOError:
		token = ""
		print("Could not read token file.")
	finally:
		f_token.close()

	return token

""" print a list of strings with nice comma-and grammar """
def formatNiceList(names):
	l = len(names)

	if l == 0:
		return ''

	if l == 1:
		return names[0]
	
	return ', '.join(names[0:-1]) + '{} and '.format(',' if l > 2 else '') + names[-1]

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
	return MySQLdb.connect(host="localhost", user="rfck-bot", passwd="rfck", db="rfck")

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

""" set the slime count to a specific value """
def setSlimesForPlayer(conn, cursor, member, slimes):
	cursor.execute("REPLACE INTO users(id_user, id_server, slimes) VALUES(%s, %s, %s)", (member.id, member.server.id, slimes))


""" add or update the scorecard before a user's name """
def getNickWithSlimes(member, user_slimes):
	user_nick = member.nick

	# Update display name with slime count.
	if user_nick == None:
		user_nick = member.display_name
	else:
		# If the nickname already has a score, find the nick part and discard the score.
		match = re_slimescore.match(user_nick)
		if match != None:
			user_nick = match.group(1)

	return (('%05d ' % user_slimes) + user_nick)

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
