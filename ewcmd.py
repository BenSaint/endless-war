import random
import asyncio

import ewcfg
import ewutils
import ewitem
import ewrolemgr
from ew import EwUser, EwMarket

""" class to send general data about an interaction to a command """
class EwCmd:
	cmd = ""
	tokens = []
	tokens_count = 0
	message = None
	client = None
	mentions = []
	mentions_count = 0

	def __init__(
		self,
		tokens = [],
		message = None,
		client = None,
		mentions = []
	):
		self.tokens = tokens
		self.message = message
		self.client = client
		self.mentions = mentions

		mentions_count = len(mentions)
		if mentions_count > 0:
			self.mentions_count = mentions_count

		if len(tokens) >= 1:
			self.tokens_count = len(tokens)
			self.cmd = tokens[0]

""" Send an initial message you intend to edit later while processing the command. Returns handle to the message. """
async def start(cmd = None, message = '...', channel = None, client = None):
	if cmd != None:
		channel = cmd.message.channel
		client = cmd.client

	if client != None and channel != None:
		return await client.send_message(channel, message)

	return None

""" pure flavor command, howls """
async def cmd_howl(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, ewcfg.howls[random.randrange(len(ewcfg.howls))]))

""" returns true if it's night time and the casino is open, else false. """
def is_casino_open(time):
	if time < 18 and time >= 6:
		return False

	return True

""" show player's slime score """
async def score(cmd):
	response = ""
	user_data = None
	member = None

	poudrins = ewitem.inventory(
		id_user = cmd.message.author.id,
		id_server = cmd.message.server.id,
		item_type_filter = ewcfg.it_slimepoudrin
	)
	poudrins_count = len(poudrins)

	if cmd.mentions_count == 0:
		user_data = EwUser(member = cmd.message.author)

		# return my score
		response = "You currently have {:,} slime{}.".format(user_data.slimes, (" and {} slime poudrin{}".format(poudrins_count, ("" if poudrins_count == 1 else "s")) if poudrins_count > 0 else ""))

	else:
		member = cmd.mentions[0]
		user_data = EwUser(member = member)

		# return somebody's score
		response = "{} currently has {:,} slime{}.".format(member.display_name, user_data.slimes, (" and {} slime poudrin{}.".format(poudrins_count, ("" if poudrins_count == 1 else "s")) if poudrins_count > 0 else ""))

	# Update the user's slime level.
	if user_data != None:
		new_level = 0

		if user_data.life_state != ewcfg.life_state_corpse:
			new_level = len(str(int(user_data.slimes)))

		if new_level > user_data.slimelevel:
			user_data.slimelevel = new_level

		user_data.persist()

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
	if member != None:
		await ewrolemgr.updateRoles(client = cmd.client, member = member)

""" show player information and description """
async def data(cmd):
	resp = await start(cmd = cmd)
	response = ""
	user_data = None
	member = None

	if cmd.mentions_count == 0:
		user_data = EwUser(member = cmd.message.author)
		market_data = EwMarket(id_server = cmd.message.server.id)

		new_level = 0

		# Ghosts don't have a slime level.
		if user_data.life_state != ewcfg.life_state_corpse:
			new_level = len(str(int(user_data.slimes)))

		# Update the user's slime level.
		if new_level > user_data.slimelevel:
			user_data.slimelevel = new_level
			user_data.persist()

		poi = ewcfg.id_to_poi.get(user_data.poi)
		if poi != None:
			response = "You find yourself in {}. ".format(poi.str_name)

		# return my data
		if user_data.life_state == ewcfg.life_state_corpse:
			response += "You are a level {} deadboi.".format(user_data.slimelevel)
		else:
			response += "You are a level {} slimeboi.".format(user_data.slimelevel)
		
		coinbounty = int(user_data.bounty / (market_data.rate_exchange / 1000000.0))

		weapon = ewcfg.weapon_map.get(user_data.weapon)
		if weapon != None:
			response += " {} {}{}.".format(ewcfg.str_weapon_wielding_self, ("" if len(user_data.weaponname) == 0 else "{}, ".format(user_data.weaponname)), weapon.str_weapon)
			if user_data.weaponskill >= 5:
				response += " {}".format(weapon.str_weaponmaster_self.format(rank = (user_data.weaponskill - 4)))
			
		trauma = ewcfg.weapon_map.get(user_data.trauma)
		if trauma != None:
			response += " {}".format(trauma.str_trauma_self)

		if user_data.kills > 0:
			response += " You have {:,} confirmed kills.".format(user_data.kills)
		
		if coinbounty != 0:
			response += " SlimeCorp offers a bounty of {:,} SlimeCoin for your death.".format(coinbounty)

		if user_data.hunger > 0:
			response += " You are {}% hungry.".format(user_data.hunger * 100.0 / ewcfg.hunger_max)
	else:
		member = cmd.mentions[0]
		user_data = EwUser(member = member)
		market_data = EwMarket(id_server = cmd.message.server.id)

		new_level = 0
		if user_data.life_state != ewcfg.life_state_corpse:
			new_level = len(str(int(user_data.slimes)))

		if new_level > user_data.slimelevel:
			user_data.slimelevel = new_level
			user_data.persist()

		# return somebody's score
		if user_data.life_state == ewcfg.life_state_corpse:
			response = "{} is a level {} deadboi.".format(member.display_name, user_data.slimelevel)
		else:
			response = "{} is a level {} slimeboi.".format(member.display_name, user_data.slimelevel)
		
		coinbounty = int(user_data.bounty / (market_data.rate_exchange / 1000000.0))

		weapon = ewcfg.weapon_map.get(user_data.weapon)
		if weapon != None:
			response += " {} {}{}.".format(ewcfg.str_weapon_wielding, ("" if len(user_data.weaponname) == 0 else "{}, ".format(user_data.weaponname)), weapon.str_weapon)
			if user_data.weaponskill >= 5:
				response += " {}".format(weapon.str_weaponmaster.format(rank = (user_data.weaponskill - 4)))
			
		trauma = ewcfg.weapon_map.get(user_data.trauma)
		if trauma != None:
			response += " {}".format(trauma.str_trauma)

		if user_data.kills > 0:
			response += " They have {:,} confirmed kills.".format(user_data.kills)

		if coinbounty != 0:
			response += " SlimeCorp offers a bounty of {:,} SlimeCoin for their death.".format(coinbounty)

	# Update the user's slime level if they're alive.
	if user_data != None:
		new_level = 0

		if user_data.life_state != ewcfg.life_state_corpse:
			new_level = len(str(int(user_data.slimes)))

		if new_level > user_data.slimelevel:
			user_data.slimelevel = new_level

		user_data.persist()

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

	await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
	if member != None:
		await ewrolemgr.updateRoles(client = cmd.client, member = member)

""" time and weather information """
async def weather(cmd):
	resp = await start(cmd = cmd)
	response = ""
	market_data = EwMarket(id_server = cmd.message.author.server.id)
	time_current = market_data.clock
	displaytime = str(time_current)
	ampm = ''

	if time_current <= 12:
		ampm = 'AM'
	if time_current > 12:
		displaytime = str(time_current - 12)
		ampm = 'PM'

	if time_current == 0:
		displaytime = 'midnight'
		ampm = ''
	if time_current == 12:
		displaytime = 'high noon'
		ampm = ''

	flair = ''
	weather_data = ewcfg.weather_map.get(market_data.weather)
	if weather_data != None:
		if time_current >= 6 and time_current <= 7:
			flair = weather_data.str_sunrise
		if time_current >= 8 and time_current <= 17:
			flair = weather_data.str_day
		if time_current >= 18 and time_current <= 19:
			flair = weather_data.str_sunset
		if time_current >= 20 or time_current <= 5:
			flair = weather_data.str_night
			
	response += "It is currently {}{} in NLACakaNM.{}".format(displaytime, ampm, (' ' + flair))
	
	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


"""
	Harvest is not and has never been a command.
"""
async def harvest(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, '**HARVEST IS NOT A COMMAND YOU FUCKING IDIOT**'))

"""
	advertise patch notes
"""
async def patchnotes(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Look for the latest patchnotes on the news page: https://ew.krakissi.net/news/'))

"""
	advertise help services
"""
async def help(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Check out the guide for help: https://ew.krakissi.net/guide/'))

