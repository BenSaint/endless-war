import random
import asyncio

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
from ew import EwUser, EwMarket
from ewslimeoid import EwSlimeoid

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
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	response = ewcfg.howls[random.randrange(len(ewcfg.howls))]
	if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
		response += "\n{} howls along with you! {}".format(str(slimeoid.name), ewcfg.howls[random.randrange(len(ewcfg.howls))])
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

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
			response = "{} currently has {:,} slime{}.".format(member.display_name, user_data.slimes, (" and {} slime poudrin{}".format(poudrins_count, ("" if poudrins_count == 1 else "s")) if poudrins_count > 0 else ""))

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
		slimeoid = EwSlimeoid(member = cmd.message.author)

		poi = ewcfg.id_to_poi.get(user_data.poi)
		if poi != None:
			response = "You find yourself {} {}. ".format(poi.str_in, poi.str_name)

		# return my data
		if user_data.life_state == ewcfg.life_state_corpse:
			response += "You are a level {} deadboi.".format(user_data.slimelevel)
		else:
			response += "You are a level {} slimeboi.".format(user_data.slimelevel)
		
		coinbounty = int(user_data.bounty / ewcfg.slimecoin_exchangerate)

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
			response += " You are {}% hungry.".format(
				round(user_data.hunger * 100.0 / ewutils.hunger_max_bylevel(user_data.slimelevel), 1)
			)

		if user_data.ghostbust:
			response += " The coleslaw in your stomach enables you to bust ghosts."

		if user_data.busted and user_data.life_state == ewcfg.life_state_corpse:
			response += " You are busted and therefore cannot leave the sewers without reviving."

		if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
			response += " You are accompanied by {}, a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))

	else:
		member = cmd.mentions[0]
		user_data = EwUser(member = member)
		market_data = EwMarket(id_server = cmd.message.server.id)
		slimeoid = EwSlimeoid(member = member)

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
			
			coinbounty = int(user_data.bounty / ewcfg.slimecoin_exchangerate)

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

			if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
				response += "They are accompanied by {}, a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))

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
	Salute the NLACakaNM flag.
"""
async def salute(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'https://ew.krakissi.net/img/nlacakanm_flag.gif'))

"""
	Burn the NLACakaNM flag.
"""
async def unsalute(cmd):
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'https://ew.krakissi.net/img/nlacakanm_flag_burning.gif'))
	
	
"""
	Rowdys THRASH
"""
async def thrash(cmd):
	user_data = EwUser(member = cmd.message.author)

	if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_rowdys:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, '\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:slime1:431564830541873182><:slime3:431659469844381717><:slime1:431564830541873182><:rf:504174176656162816>\n<:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>\n<:rowdyfucker:431275088076079105><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rowdyfucker:431275088076079105>\n<:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>'))
	
"""
	Killers DAB
"""
async def dab(cmd):
	user_data = EwUser(member = cmd.message.author)

	if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_killers:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, '\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152>\n<:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152>\n<:copkiller:431275071945048075> <:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:copkiller:431275071945048075>\n<:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152>\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:slime3:431659469844381717><:slime1:431564830541873182><:slime1:431564830541873182><:slime3:431659469844381717><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152>'))

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
	
""" Accept a russian roulette challenge """
async def accept(cmd):
	user = EwUser(member = cmd.message.author)
	if(user.rr_challenger != ""):
		challenger = EwUser(id_user = user.rr_challenger, id_server = user.id_server)
		if(user.rr_challenger != user.id_user and challenger.rr_challenger != user.id_user):
			challenger.rr_challenger = user.id_user
			challenger.persist()
			response = "You accept the challenge! Both of you head out back behind the casino and load a bullet into the gun."
			await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	return

""" Refuse a russian roulette challenge """
async def refuse(cmd):
	user = EwUser(member = cmd.message.author)
	if(user.rr_challenger != ""):
		challenger = EwUser(id_user = user.rr_challenger, id_server = user.id_server)
		if(user.rr_challenger != user.id_user and challenger.rr_challenger != user.id_user):
			response = "You refuse the challenge, but not before leaving a large puddle of urine beneath you."
			await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	return

"""Slimeoids"""

# play with your slimeoid
async def playfetch(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	
	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to play fetch with."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."	

	else:
		head = ewcfg.head_map.get(slimeoid.head)
		response = head.str_fetch.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

async def observeslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	
	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to observe."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."	

	else:
		options = [
			'body',
			'weapon',
			'special',
			'brain',
		]

		roll = random.randrange(len(options))
		result = options[roll]

		if result == 'body':
			part = ewcfg.body_map.get(slimeoid.body)

		if result == 'weapon':
			part = ewcfg.offense_map.get(slimeoid.weapon)

		if result == 'special':
			part = ewcfg.special_map.get(slimeoid.special)

		if result == 'brain':
			part = ewcfg.brain_map.get(slimeoid.ai)
		
		response = part.str_observe.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

async def petslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	
	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to pet."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."	

	else:
		armor = ewcfg.defense_map.get(slimeoid.armor)
		response = armor.str_pet.format(
			slimeoid_name = slimeoid.name
		)
		response += " "
		brain = ewcfg.brain_map.get(slimeoid.ai)
		response += brain.str_pet.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

async def walkslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	
	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to take for a walk."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	else:
		brain = ewcfg.brain_map.get(slimeoid.ai)
		response = brain.str_walk.format(
			slimeoid_name = slimeoid.name
		)
		poi = ewcfg.id_to_poi.get(user_data.poi)
		response += " With that done, you go for a leisurely stroll around {}, while ".format(poi.str_name)
		legs = ewcfg.mobility_map.get(slimeoid.legs)
		response += legs.str_walk.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

# read the instructions
async def instructions(cmd):
	resp = await start(cmd = cmd)
	resp2 = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "There's no instructions to read here."

	else:
		response = "Welcome to SlimeCorp's Brawlden Laboratory Facilities."
		response += "\n\nThis facility specializes in the emerging technology of Slimeoids, or slime-based artificial lifeforms. Research into the properties of Slimeoids is ongoing, but already great advancements in the field have been made and we are proud to be the first to make them commercially available."
		response += "\n\nThis laboratory is equipped with everything required for the creation of a Slimeoid from scratch. To create a Slimeoid, you will need to supply one (1) Slime Poudrin, which will serve as the locus around which your Slimeoid will be based. You will also need to supply some Slime. You may supply as much or as little slime as you like, but greater Slime contribution will lead to superior Slimeoid genesis. To begin the Slimeoid creation process, use **!incubateslimeoid** followed by the amount of slime you wish to use."
		response += "\n\nAfter beginning incubation, you will need to use the console to adjust your Slimeoid's features while it is still forming. Use **!growbody**, **!growhead**, **!growlegs**, **!growweapon**, **!growarmor**, **!growspecial**, or **!growbrain** followed by a letter (A - G) to choose the appearance, abilities, and temperament of your Slimeoid. You will also need to give youe Slimeoid a name. Use **!nameslimeoid** followed by your desired name. These traits may be changed at any time before the incubation is completed."
		response += "\n\nIn addition to physical features, you will need to allocate your Slimeoid's attributes. Your Slimeoid will have a different amount of potential depending on how much slime you invested in its creation. You must distribute this potential across the three Slimeoid attributes, Moxie, Grit, and Chutzpah. Use **!raisemoxie**, **!lowermoxie**, **!raisegrit**, **!lowergrit**, **!raisechutzpah**, and **!lowerchutzpah** to adjust your Slimeoid's attributes to your liking."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		response = "\n\nWhen all of your Slimeoid's traits are confirmed, use **!spawnslimeoid** to end the incubation and eject your Slimeoid from the gestation vat. Be aware that once spawned, the Slimeoid's traits are finalized and cannot be changed, so be sure you are happy with your Slimeoid's construction before spawning. Additionally, be aware that you may only have one Slimeoid at a time, meaning should you ever want a new Slimeoid, you will need to euthanise your old one with **!dissolveslimeoid**. SlimeCorp assumes no responsibility for accidents, injuries, infections, physical disabilities, or ideological radicalizations that may occur due to prolonged contact with slime-based lifeforms."
		response += "\n\nYou can read a full description of your or someone else's Slimeoid with the **!slimeoid** command. Note that your Slimeoid, having been made out of slime extracted from your body, will recognize you as its master and follow you until such time as you choose to dispose of it. It will react to your actions, including when you kill an opponent, when you are killed, when you return from the dead, and when you !howl. In addition, you can also perform activities with your Slimeoid. Try **!observeslimeoid**, **!petslimeoid**, **!walkslimeoid**, and **!playfetch** and see what happens."
		response += "\n\nSlimeoid research is ongoing, and the effects of a Slimeoid's physical makeup, brain structure, and attribute allocation on its abilities are a rapidly advancing field. Field studies into the effects of these variables on one-on-one Slimeoid battles are set to begin in the near future. In the meantime, report any unusual findings or behaviors to the Cop Killer and Rowdy Fucker, who have much fewer important things to spend their time on than SlimeCorp employees."
		response += "\n\nThank you for choosing SlimeCorp.{}".format(ewcfg.emote_slimecorp)


	# Send the response to the player.
	await cmd.client.edit_message(resp2, ewutils.formatMessage(cmd.message.author, response))

# Create a slimeoid
async def incubateslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	poudrins = ewitem.inventory(
		id_user = cmd.message.author.id,
		id_server = cmd.message.server.id,
		item_type_filter = ewcfg.it_slimepoudrin
	)
	poudrins_count = len(poudrins)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."	

	elif poudrins_count < 1:
		response = "You need a slime poudrin."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)
		if value != None:
			user_data = EwUser(member = cmd.message.author)
			slimeoid = EwSlimeoid(member = cmd.message.author)
			market_data = EwMarket(id_server = cmd.message.author.server.id)
			if value == -1:
				value = user_data.slimes

			if slimeoid.life_state == ewcfg.slimeoid_state_active:
				response = "You have already created a Slimeoid. Dissolve your current slimeoid before incubating a new one."
				
			elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
				response = "You are already in the process of incubating a Slimeoid."

			elif value > user_data.slimes:
				response = "You do not have that much slime to sacrifice."
			
			else:
				# delete a slime poudrin from the player's inventory
				ewitem.item_delete(id_item = poudrins[0].get('id_item'))

				level = len(str(value))
				user_data.change_slimes(n = -value)
				slimeoid.life_state = ewcfg.slimeoid_state_forming
				slimeoid.level = level
				slimeoid.id_user = user_data.id_user
				slimeoid.id_server = user_data.id_server

				user_data.persist()
				slimeoid.persist()

				response = "You place a poudrin into a small opening on the console. As you do, a needle shoots up and pricks your finger, intravenously extracting {} slime from your body. The poudrin is then dropped into the gestation tank. Looking through the observation window, you see what was once your slime begin to seep into the tank and accrete around the poudrin. The incubation of a new Slimeoid has begun! {}".format(str(value), ewcfg.emote_slime2)

		else:
			response = "You must contribute some of your own slime to create a Slimeoid. Specify how much slime you will sacrifice."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

# Create a slimeoid
async def dissolveslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
		response = "Ghosts cannot interact with the SlimeCorp Lab apparati."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You have no slimeoid to dissolve."	

	else:			
		if slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "You hit a large red button with a white X on it. Immediately a buzzer goes off and the half-formed body of what would have been your new Slimeoid is flushed out of the gestation tank and down a drainage tube, along with your poudrin and slime. What a waste."
		else:
			brain = ewcfg.brain_map.get(slimeoid.ai)
			response = brain.str_dissolve.format(
				slimeoid_name = slimeoid.name
			)
			response += "{}".format(ewcfg.emote_slimeskull)

		slimeoid.life_state = ewcfg.slimeoid_state_none
		slimeoid.body = ""
		slimeoid.head = ""
		slimeoid.legs = ""
		slimeoid.armor = ""
		slimeoid.weapon = ""
		slimeoid.special = ""
		slimeoid.ai = ""
		slimeoid.type = ""
		slimeoid.name = ""
		slimeoid.atk = 0
		slimeoid.defense = 0
		slimeoid.intel = 0
		slimeoid.level = 0

		user_data.persist()
		slimeoid.persist()

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's body

async def growbody(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			body = ewcfg.body_map.get(value)
			if body != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(body.str_create)
					slimeoid.body = body.id_body
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the body console labelled A through G."
			else:
				response = "Choose an option from the buttons on the body console labelled A through G."
		else:
			response = "You must specify a body type. Choose an option from the buttons on the body console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


# shape your slimeoid's head
async def growhead(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			head = ewcfg.head_map.get(value)
			if head != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(head.str_create)
					slimeoid.head = head.id_head
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the head console labelled A through G."
			else:
				response = "Choose an option from the buttons on the head console labelled A through G."
		else:
			response = "You must specify a head type. Choose an option from the buttons on the head console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's legs
async def growlegs(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			mobility = ewcfg.mobility_map.get(value)
			if mobility != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(mobility.str_create)
					slimeoid.legs = mobility.id_mobility
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the mobility console labelled A through G."
			else:
				response = "Choose an option from the buttons on the mobility console labelled A through G."
		else:
			response = "You must specify means of locomotion. Choose an option from the buttons on the mobility console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
	
# shape your slimeoid's weapon
async def growweapon(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			offense = ewcfg.offense_map.get(value)
			if offense != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(offense.str_create)
					slimeoid.weapon = offense.id_offense
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the weapon console labelled A through G."
			else:
				response = "Choose an option from the buttons on the weapon console labelled A through G."
		else:
			response = "You must specify a means of attack. Choose an option from the buttons on the weapon console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
	
# shape your slimeoid's armor
async def growarmor(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			defense = ewcfg.defense_map.get(value)
			if defense != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(defense.str_create)
					slimeoid.armor = defense.id_defense
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the armor console labelled A through G."
			else:
				response = "Choose an option from the buttons on the armor console labelled A through G."
		else:
			response = "You must specify a method of protection. Choose an option from the buttons on the armor console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
	
# shape your slimeoid's special ability
async def growspecial(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			special = ewcfg.special_map.get(value)
			if special != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(special.str_create)
					slimeoid.special = special.id_special
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the special attack console labelled A through G."
			else:
				response = "Choose an option from the buttons on the special attack console labelled A through G."
		else:
			response = "You must specify a special attack type. Choose an option from the buttons on the special attack console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's brain.
async def growbrain(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			brain = ewcfg.brain_map.get(value)
			if brain != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(brain.str_create)
					slimeoid.ai = brain.id_brain
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the brain console labelled A through G."
			else:
				response = "Choose an option from the buttons on the brain console labelled A through G."
		else:
			response = "You must specify a brain structure. Choose an option from the buttons on the brain console labelled A through G."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		
# Name your slimeoid.
async def nameslimeoid(cmd):
	resp = await start(cmd = cmd)
	name = ""
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid already has a name."	

	
	else:

		if cmd.tokens_count < 2:
			response = "You must specify a name."
		else:
			name = cmd.message.content[(len(ewcfg.cmd_nameslimeoid)):].strip()

			if len(name) > 32:
				response = "That name is too long. ({:,}/32)".format(len(name))
		
			else:
				slimeoid.name = str(name)

				user_data.persist()
				slimeoid.persist()

				response = "You enter the name {} into the console.".format(str(name))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
	
#allocate a point to ATK
async def raisemoxie(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.atk += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more moxie."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowermoxie(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if (slimeoid.atk <= 0):
			response = "You cannot reduce your slimeoid's moxie any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.atk -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some moxie."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to DEF
async def raisegrit(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.defense += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more grit."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowergrit(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if (slimeoid.defense <= 0):
			response = "You cannot reduce your slimeoid's grit any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.defense -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some grit."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to DEF
async def raisechutzpah(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.intel += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more chutzpah."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowerchutzpah(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."	

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."	

	
	else:

		if (slimeoid.intel <= 0):
			response = "You cannot reduce your slimeoid's chutzpah any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
		
		else:
			slimeoid.intel -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some chutzpah."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))




# complete a slimeoid
async def spawnslimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	response = ""
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."
	
	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."		

	
	else:
			
		if slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "You have already created a Slimeoid. Dissolve your current slimeoid before incubating a new one."
			
		elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You have not yet begun incubating a slimeoid."
		
		else:
			needsbody = False
			needshead = False
			needslegs = False
			needsarmor = False
			needsweapon = False
			needsspecial = False
			needsbrain = False
			needsname = False
			needsstats = False
			incomplete = False

			if (slimeoid.body == ""):
				needsbody = True
				incomplete = True
			if (slimeoid.head == ""):
				needshead = True
				incomplete = True
			if (slimeoid.legs == ""):
				needslegs = True
				incomplete = True
			if (slimeoid.armor == ""):
				needsarmor = True
				incomplete = True
			if (slimeoid.weapon == ""):
				needsweapon = True
				incomplete = True
			if (slimeoid.special == ""):
				needsspecial = True
				incomplete = True
			if (slimeoid.ai == ""):
				needsbrain = True
				incomplete = True
			if (slimeoid.name == ""):
				needsname = True
				incomplete = True
			if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) < (slimeoid.level)):
				needsstats = True
				incomplete = True

			if incomplete == True:
				response = "Your slimeoid is not yet ready to be spawned from the gestation vat."
				if needsbody == True:
					response += "\nIts body has not yet been given a distinct form."
				if needshead == True:
					response += "\nIt does not yet have a head."
				if needslegs == True:
					response += "\nIt has no means of locomotion."
				if needsarmor == True:
					response += "\nIt lacks any form of protection."
				if needsweapon == True:
					response += "\nIt lacks a means of attack."
				if needsspecial == True:
					response += "\nIt lacks a special ability."
				if needsbrain == True:
					response += "\nIt does not yet have a brain."
				if needsstats == True:
					response += "\nIt still has potential that must be distributed between Moxie, Grit and Chutzpah."
				if needsname == True:
					response += "\nIt needs a name."
			else:
				slimeoid.life_state = ewcfg.slimeoid_state_active
				response = "You press the big red button labelled 'SPAWN'. The console lights up and there is a rush of mechanical noise as the fluid drains rapidly out of the gestation tube. The newly born Slimeoid within writhes in confusion before being sucked down an ejection chute and spat out messily onto the laboratory floor at your feet. Happy birthday, {} the Slimeoid!! {}".format(slimeoid.name, ewcfg.emote_slimeheart)

				response += "\n\n{} is a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))
				
				body = ewcfg.body_map.get(slimeoid.body)
				if body != None:
					response += " {}".format(body.str_body)

				head = ewcfg.head_map.get(slimeoid.head)
				if head != None:
					response += " {}".format(head.str_head)

				mobility = ewcfg.mobility_map.get(slimeoid.legs)
				if mobility != None:
					response += " {}".format(mobility.str_mobility)

				offense = ewcfg.offense_map.get(slimeoid.weapon)
				if offense != None:
					response += " {}".format(offense.str_offense)

				defense = ewcfg.defense_map.get(slimeoid.armor)
				if defense != None:
					response += " {}".format(defense.str_armor)

				special = ewcfg.special_map.get(slimeoid.special)
				if special != None:
					response += " {}".format(special.str_special)

				brain = ewcfg.brain_map.get(slimeoid.ai)
				if brain != None:
					response += " {}".format(brain.str_brain)

				stat = slimeoid.atk
				if stat == 0:
					statlevel = "almost no"
				if stat == 1:
					statlevel = "just a little bit of"
				if stat == 2:
					statlevel = "a decent amount of"
				if stat == 3:
					statlevel = "quite a bit of"
				if stat == 4:
					statlevel = "a whole lot of"
				if stat == 5:
					statlevel = "loads of"
				if stat == 6:
					statlevel = "massive amounts of"
				if stat == 7:
					statlevel = "seemingly inexhaustible stores of"
				if stat >= 8:
					statlevel = "truly godlike levels of"
				statname = "moxie"
				response += " It has {} {}.".format(statlevel, statname)

				stat = slimeoid.defense
				if stat == 0:
					statlevel = "almost no"
				if stat == 1:
					statlevel = "just a little bit of"
				if stat == 2:
					statlevel = "a decent amount of"
				if stat == 3:
					statlevel = "quite a bit of"
				if stat == 4:
					statlevel = "a whole lot of"
				if stat == 5:
					statlevel = "loads of"
				if stat == 6:
					statlevel = "massive amounts of"
				if stat == 7:
					statlevel = "seemingly inexhaustible stores of"
				if stat >= 8:
					statlevel = "truly godlike levels of"
				statname = "grit"
				response += " It has {} {}.".format(statlevel, statname)

				stat = slimeoid.intel
				if stat == 0:
					statlevel = "almost no"
				if stat == 1:
					statlevel = "just a little bit of"
				if stat == 2:
					statlevel = "a decent amount of"
				if stat == 3:
					statlevel = "quite a bit of"
				if stat == 4:
					statlevel = "a whole lot of"
				if stat == 5:
					statlevel = "loads of"
				if stat == 6:
					statlevel = "massive amounts of"
				if stat == 7:
					statlevel = "seemingly inexhaustible stores of"
				if stat >= 8:
					statlevel = "truly godlike levels of"
				statname = "chutzpah"
				response += " It has {} {}.".format(statlevel, statname)

			#	response += "\n\n {}".format()
				brain = ewcfg.brain_map.get(slimeoid.ai)
				response += "\n\n" + brain.str_spawn.format(
				slimeoid_name = slimeoid.name
				)

			user_data.persist()
			slimeoid.persist()

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

			
		
# Show a player's slimeoid data.
async def slimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	member = None
	selfcheck = True


	if cmd.mentions_count == 0:
		selfcheck = True
		slimeoid = EwSlimeoid(member = cmd.message.author)
	else:
		selfcheck = False
		member = cmd.mentions[0]
		user_data = EwUser(member = member)
		slimeoid = EwSlimeoid(member = member)

	if slimeoid.life_state == ewcfg.slimeoid_state_forming:
		if selfcheck == True:
			response = "Your Slimeoid is still forming in the gestation vat. It is about {} feet from end to end.".format(str(slimeoid.level))
		else:
			response = "{}'s Slimeoid is still forming in the gestation vat. It is about {} feet from end to end.".format(member.display_name, str(slimeoid.level))
	if slimeoid.life_state == ewcfg.slimeoid_state_active:
		if selfcheck == True:
			response = "You are accompanied by {}, a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))
		else:
			response = "{} is accompanied by {}, a {}-foot-tall Slimeoid.".format(member.display_name, slimeoid.name, str(slimeoid.level))
	
	body = ewcfg.body_map.get(slimeoid.body)
	if body != None:
		response += " {}".format(body.str_body)

	head = ewcfg.head_map.get(slimeoid.head)
	if head != None:
		response += " {}".format(head.str_head)

	mobility = ewcfg.mobility_map.get(slimeoid.legs)
	if mobility != None:
		response += " {}".format(mobility.str_mobility)

	offense = ewcfg.offense_map.get(slimeoid.weapon)
	if offense != None:
		response += " {}".format(offense.str_offense)

	defense = ewcfg.defense_map.get(slimeoid.armor)
	if defense != None:
		response += " {}".format(defense.str_armor)

	special = ewcfg.special_map.get(slimeoid.special)
	if special != None:
		response += " {}".format(special.str_special)

	brain = ewcfg.brain_map.get(slimeoid.ai)
	if brain != None:
		response += " {}".format(brain.str_brain)

	stat = slimeoid.atk
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	statname = "moxie"
	response += " It has {} {}.".format(statlevel, statname)

	stat = slimeoid.defense
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	statname = "grit"
	response += " It has {} {}.".format(statlevel, statname)

	stat = slimeoid.intel
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	statname = "chutzpah"
	response += " It has {} {}.".format(statlevel, statname)

	if slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You have not yet created a slimeoid."

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."


	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
