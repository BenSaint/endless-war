import random
import asyncio

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
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
		self.mentions_count = len(mentions)

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

	if cmd.mentions_count == 0:
		user_data = EwUser(member = cmd.message.author)
		poudrins = ewitem.inventory(
			id_user = cmd.message.author.id,
			id_server = cmd.message.server.id,
			item_type_filter = ewcfg.it_slimepoudrin
		)
		poudrins_count = len(poudrins)

		# return my score
		response = "You currently have {:,} slime{}.".format(user_data.slimes, (" and {} slime poudrin{}".format(poudrins_count, ("" if poudrins_count == 1 else "s")) if poudrins_count > 0 else ""))

	else:
		member = cmd.mentions[0]
		user_data = EwUser(member = member)
		poudrins = ewitem.inventory(
			id_user = user_data.id_user,
			id_server = cmd.message.server.id,
			item_type_filter = ewcfg.it_slimepoudrin
		)
		poudrins_count = len(poudrins)

		if user_data.life_state == ewcfg.life_state_grandfoe:
			# Can't see a raid boss's slime score.
			response = "{}'s power is beyond your understanding.".format(member.display_name)
		else:
			# return somebody's score
			response = "{} currently has {:,} slime{}.".format(member.display_name, user_data.slimes, (" and {} slime poudrin{}.".format(poudrins_count, ("" if poudrins_count == 1 else "s")) if poudrins_count > 0 else ""))

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
	if member != None:
		await ewrolemgr.updateRoles(client = cmd.client, member = member)

""" show player information and description """
async def data(cmd):
	response = ""
	user_data = None
	member = None

	if cmd.mentions_count == 0:
		user_data = EwUser(member = cmd.message.author)
		market_data = EwMarket(id_server = cmd.message.server.id)

		poi = ewcfg.id_to_poi.get(user_data.poi)
		if poi != None:
			response = "You find yourself {} {}. ".format(poi.str_in, poi.str_name)

		# return my data
		if user_data.life_state == ewcfg.life_state_corpse:
			response += "You are a level {} deadboi.".format(user_data.slimelevel)
		else:
			response += "You are a level {} slimeboi.".format(user_data.slimelevel)
		
		coinbounty = int(user_data.bounty / 1000)

		weapon = ewcfg.weapon_map.get(user_data.weapon)
		if weapon != None:
			response += " {} {}{}.".format(ewcfg.str_weapon_wielding_self, ("" if len(user_data.weaponname) == 0 else "{}, ".format(user_data.weaponname)), weapon.str_weapon)
			if user_data.weaponskill >= 5:
				response += " {}".format(weapon.str_weaponmaster_self.format(rank = (user_data.weaponskill - 4)))
			
		trauma = ewcfg.weapon_map.get(user_data.trauma)
		if trauma != None:
			response += " {}".format(trauma.str_trauma_self)

		user_kills = ewstats.get_stat(user = user_data, metric = ewcfg.stat_kills)
		if user_kills > 0:
			response += " You have {:,} confirmed kills.".format(user_kills)
		
		if coinbounty != 0:
			response += " SlimeCorp offers a bounty of {:,} SlimeCoin for your death.".format(coinbounty)

		if user_data.hunger > 0:
			response += " You are {}% hungry.".format(user_data.hunger * 100.0 / ewcfg.hunger_max)

		if user_data.ghostbust:
			response += " The coleslaw in your stomach enables you to bust ghosts."

		if user_data.busted and user_data.life_state == ewcfg.life_state_corpse:
			response += " You are busted and therefore cannot leave the sewers without reviving."

	else:
		member = cmd.mentions[0]
		user_data = EwUser(member = member)
		market_data = EwMarket(id_server = cmd.message.server.id)

		if user_data.life_state == ewcfg.life_state_grandfoe:
			poi = ewcfg.id_to_poi.get(user_data.poi)
			if poi != None:
				response = "{} is {} {}.".format(member.display_name, poi.str_in, poi.str_name)
			else:
				response = "You can't discern anything useful about {}.".format(member.display_name)
		else:

			# return somebody's score
			if user_data.life_state == ewcfg.life_state_corpse:
				response = "{} is a level {} deadboi.".format(member.display_name, user_data.slimelevel)
			else:
				response = "{} is a level {} slimeboi.".format(member.display_name, user_data.slimelevel)
			
			coinbounty = int(user_data.bounty / 1000)

			weapon = ewcfg.weapon_map.get(user_data.weapon)
			if weapon != None:
				response += " {} {}{}.".format(ewcfg.str_weapon_wielding, ("" if len(user_data.weaponname) == 0 else "{}, ".format(user_data.weaponname)), weapon.str_weapon)
				if user_data.weaponskill >= 5:
					response += " {}".format(weapon.str_weaponmaster.format(rank = (user_data.weaponskill - 4)))
				
			trauma = ewcfg.weapon_map.get(user_data.trauma)
			if trauma != None:
				response += " {}".format(trauma.str_trauma)

			user_kills = ewstats.get_stat(user = user_data, metric = ewcfg.stat_kills)
			if user_kills > 0:
				response += " They have {:,} confirmed kills.".format(user_kills)

			if coinbounty != 0:
				response += " SlimeCorp offers a bounty of {:,} SlimeCoin for their death.".format(coinbounty)

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
	if member != None:
		await ewrolemgr.updateRoles(client = cmd.client, member = member)

def weather_txt(id_server):
	response = ""
	market_data = EwMarket(id_server = id_server)
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
	return response

""" time and weather information """
async def weather(cmd):
	response = weather_txt(cmd.message.server.id)
	
	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


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

"""
	Link to the world map.
"""
async def map(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Online world map: https://ew.krakissi.net/map/'))

"""
	Link to the RFCK wiki.
"""
async def wiki(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Wiki: https://rfck.miraheze.org/wiki/Main_Page'))

"""
	Link to the fan art booru.
"""
async def booru(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Booru: http://rfck.booru.org/'))
