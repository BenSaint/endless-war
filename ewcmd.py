import random

import ewcfg
import ewutils

""" pure flavor command, howls """
def cmd_howl(message):
	return ewutils.formatMessage(message.author, ewcfg.howls[random.randrange(len(ewcfg.howls))])

""" returns true if it's night time and the casino is open, else false. """
def is_casino_open(time):
	if time < 18 and time >= 6:
		return False

	return True
