import MySQLdb
import datetime

import ewcfg

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
