import MySQLdb;

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
