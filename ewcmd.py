import random

import ewcfg
import ewutils

""" pure flavor command, howls """
def cmd_howl(message):
	return ewutils.formatMessage(message.author, ewcfg.howls[random.randrange(len(ewcfg.howls))])
