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
		names.append(user.name)

	return formatNiceList(names)
