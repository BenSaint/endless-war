import random
import asyncio
import time

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
from ew import EwUser, EwMarket
from ewitem import EwItem
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
		return await ewutils.send_message(client, channel, message)

	return None

""" pure flavor command, howls """
async def cmd_howl(cmd):
	user_data = EwUser(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	response = ewcfg.howls[random.randrange(len(ewcfg.howls))]

	if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
		response += "\n{} howls along with you! {}".format(str(slimeoid.name), ewcfg.howls[random.randrange(len(ewcfg.howls))])

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" returns true if it's night time and the casino is open, else false. """
def is_casino_open(t):
	if t < 18 and t >= 6:
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
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
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

		cosmetics = ewitem.inventory(
			id_user = cmd.message.author.id,
			id_server = cmd.message.server.id,
			item_type_filter = ewcfg.it_cosmetic
		)
		adorned_cosmetics = []
		for cosmetic in cosmetics:
			cos = EwItem(id_item = cosmetic.get('id_item'))
			if cos.item_props['adorned'] == 'true':
				adorned_cosmetics.append(cosmetic.get('name'))

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

		if len(adorned_cosmetics) > 0:
			response += " You have a {} adorned.".format(ewutils.formatNiceList(adorned_cosmetics, 'and'))

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

		cosmetics = ewitem.inventory(
			id_user = user_data.id_user,
			id_server = user_data.id_server,
			item_type_filter = ewcfg.it_cosmetic
		)
		adorned_cosmetics = []
		for cosmetic in cosmetics:
			cos = EwItem(id_item = cosmetic.get('id_item'))
			if cos.item_props['adorned'] == 'true':
				adorned_cosmetics.append(cosmetic.get('name'))

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

			if len(adorned_cosmetics) > 0:
				response += " They have a {} adorned.".format(ewutils.formatNiceList(adorned_cosmetics, 'and'))
        
			if (slimeoid.life_state == ewcfg.slimeoid_state_active) and (user_data.life_state != ewcfg.life_state_corpse):
				response += "They are accompanied by {}, a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


"""
	Harvest is not and has never been a command.
"""
async def harvest(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, '**HARVEST IS NOT A COMMAND YOU FUCKING IDIOT**'))

"""
	Salute the NLACakaNM flag.
"""
async def salute(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'https://ew.krakissi.net/img/nlacakanm_flag.gif'))

"""
	Burn the NLACakaNM flag.
"""
async def unsalute(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'https://ew.krakissi.net/img/nlacakanm_flag_burning.gif'))
	
	
"""
	Rowdys THRASH
"""
async def thrash(cmd):
	user_data = EwUser(member = cmd.message.author)

	if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_rowdys:
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, '\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:slime1:431564830541873182><:slime3:431659469844381717><:slime1:431564830541873182><:rf:504174176656162816>\n<:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>\n<:rowdyfucker:431275088076079105><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:slime1:431564830541873182><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rowdyfucker:431275088076079105>\n<:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:slime3:431659469844381717><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:slime1:431564830541873182><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816><:rf:504174176656162816>'))
	
"""
	Killers DAB
"""
async def dab(cmd):
	user_data = EwUser(member = cmd.message.author)

	if (user_data.life_state == ewcfg.life_state_enlisted or user_data.life_state == ewcfg.life_state_kingpin) and user_data.faction == ewcfg.faction_killers:
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, '\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:slime3:431659469844381717><:slime1:431564830541873182><:slime3:431659469844381717><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152>\n<:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152>\n<:copkiller:431275071945048075> <:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:copkiller:431275071945048075>\n<:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:slime3:431659469844381717><:ck:504173691488305152><:ck:504173691488305152><:ck:504173691488305152>\n<:blank:492087853702971403><:blank:492087853702971403><:blank:492087853702971403><:ck:504173691488305152><:slime3:431659469844381717><:slime1:431564830541873182><:slime1:431564830541873182><:slime3:431659469844381717><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152><:ck:504173691488305152><:slime1:431564830541873182><:ck:504173691488305152>'))

"""
	advertise patch notes
"""
async def patchnotes(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Look for the latest patchnotes on the news page: https://ew.krakissi.net/news/'))

"""
	advertise help services
"""
async def help(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Check out the guide for help: https://ew.krakissi.net/guide/'))

"""
	Link to the world map.
"""
async def map(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Online world map: https://ew.krakissi.net/map/'))

"""
	Link to the RFCK wiki.
"""
async def wiki(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Wiki: https://rfck.miraheze.org/wiki/Main_Page'))

"""
	Link to the fan art booru.
"""
async def booru(cmd):
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Rowdy Fuckers Cop Killers Booru: http://rfck.booru.org/'))
	
""" Accept a russian roulette challenge """
async def accept(cmd):
	user = EwUser(member = cmd.message.author)
	if(user.rr_challenger != ""):
		challenger = EwUser(id_user = user.rr_challenger, id_server = user.id_server)
		if(user.rr_challenger != user.id_user and challenger.rr_challenger != user.id_user):
			challenger.rr_challenger = user.id_user
			challenger.persist()
			if cmd.message.channel.name == ewcfg.channel_arena:
				response = "You accept the challenge! Both of your Slimeoids ready themselves for combat!"
			else:
				response = "You accept the challenge! Both of you head out back behind the casino and load a bullet into the gun."
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


""" Refuse a russian roulette challenge """
async def refuse(cmd):
	user = EwUser(member = cmd.message.author)

	if(user.rr_challenger != ""):
		challenger = EwUser(id_user = user.rr_challenger, id_server = user.id_server)

		user.rr_challenger = ""
		user.persist()

		if(user.rr_challenger != user.id_user and challenger.rr_challenger != user.id_user):
			response = "You refuse the challenge, but not before leaving a large puddle of urine beneath you."
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		else:
			challenger.rr_challenger = ""
			challenger.persist()


"""
	Slimeoids
"""

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
		await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
		response = "\n\nWhen all of your Slimeoid's traits are confirmed, use **!spawnslimeoid** to end the incubation and eject your Slimeoid from the gestation vat. Be aware that once spawned, the Slimeoid's traits are finalized and cannot be changed, so be sure you are happy with your Slimeoid's construction before spawning. Additionally, be aware that you may only have one Slimeoid at a time, meaning should you ever want a new Slimeoid, you will need to euthanise your old one with **!dissolveslimeoid**. SlimeCorp assumes no responsibility for accidents, injuries, infections, physical disabilities, or ideological radicalizations that may occur due to prolonged contact with slime-based lifeforms."
		response += "\n\nYou can read a full description of your or someone else's Slimeoid with the **!slimeoid** command. Note that your Slimeoid, having been made out of slime extracted from your body, will recognize you as its master and follow you until such time as you choose to dispose of it. It will react to your actions, including when you kill an opponent, when you are killed, when you return from the dead, and when you !howl. In addition, you can also perform activities with your Slimeoid. Try **!observeslimeoid**, **!petslimeoid**, **!walkslimeoid**, and **!playfetch** and see what happens."
		response += "\n\nSlimeoid research is ongoing, and the effects of a Slimeoid's physical makeup, brain structure, and attribute allocation on its abilities are a rapidly advancing field. Field studies into the effects of these variables on one-on-one Slimeoid battles are set to begin in the near future. In the meantime, report any unusual findings or behaviors to the Cop Killer and Rowdy Fucker, who have much fewer important things to spend their time on than SlimeCorp employees."
		response += "\n\nThank you for choosing SlimeCorp.{}".format(ewcfg.emote_slimecorp)


	# Send the response to the player.
	await ewutils.edit_message(cmd.client, resp2, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))


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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
	
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
	
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
	
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
		
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
	
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))




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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

			
		
# Show a player's slimeoid data.
async def slimeoid(cmd):
	resp = await start(cmd = cmd)
	user_data = EwUser(member = cmd.message.author)
	member = None
	selfcheck = True
	response = ""

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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

def check(str):
	if str.content == ewcfg.cmd_accept or str.content == ewcfg.cmd_refuse:
		return True

async def slimeoidbattle(cmd):

	if cmd.message.channel.name != ewcfg.channel_arena:
		#Only at the casino
		response = "You can only have Slimeoid Battles at the Battle Arena."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if cmd.mentions_count != 1:
		#Must mention only one player
		response = "Mention the player you want to challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	author = cmd.message.author
	member = cmd.mentions[0]

	if author.id == member.id:
		response = "You can't challenge yourself, dumbass."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	challenger = EwUser(member = author)
	challenger_slimeoid = EwSlimeoid(member = author)
	challengee = EwUser(member = member)
	challengee_slimeoid = EwSlimeoid(member = member)

	challenger.rr_challenger = ""
	challengee.rr_challenger = ""

	#Players have been challenged
	if challenger.rr_challenger != "":
		response = "You are already in the middle of a challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challengee.rr_challenger != "":
		response = "{} is already in the middle of a challenge.".format(member.display_name).replace("@", "\{at\}")
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger.poi != challengee.poi:
		#Challangee must be in the casino
		response = "Both players must be in the Battle Arena."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger_slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "You do not have a Slimeoid ready to battle with!"
	
	if challengee_slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "{} does not have a Slimeoid ready to battle with!".format(member.display_name)

	#Players have to be enlisted
	if challenger.life_state == ewcfg.life_state_corpse or challengee.life_state == ewcfg.life_state_corpse:
		if challenger.life_state == ewcfg.life_state_corpse:
			response = "Your Slimeoid won't battle for you while you're dead.".format(author.display_name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

		elif challengee.life_state == ewcfg.life_state_corpse:
			response = "{}'s Slimeoid wont battle for them while they're dead.".format(member.display_name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Assign a challenger so players can't be challenged
	challenger.rr_challenger = challenger.id_user
	challengee.rr_challenger = challenger.id_user

	challenger.persist()
	challengee.persist()

	response = "You have been challenged by {} to a Slimeoid Battle. Do you !accept or !refuse?".format(author.display_name).replace("@", "\{at\}")
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(member, response))

	#Wait for an answer
	accepted = 0
	try:
		msg = await cmd.client.wait_for_message(timeout = 30, author = member, check = check)

		if msg != None:
			if msg.content == "!accept":
				accepted = 1
	except:
		accepted = 0

	# Clear challenger field.
	challenger = EwUser(member = author)
	challengee = EwUser(member = member)

	challenger.rr_challenger = ""
	challengee.rr_challenger = ""

	challenger.persist()
	challengee.persist()

	#Start game
	if accepted == 1:
		s1name = str(challengee_slimeoid.name)
		s1weapon = ewcfg.offense_map.get(challengee_slimeoid.weapon)
		s1armor = ewcfg.defense_map.get(challengee_slimeoid.armor)
		s1special = ewcfg.special_map.get(challengee_slimeoid.special)
		s1legs = ewcfg.mobility_map.get(challengee_slimeoid.legs)
		s1brain = ewcfg.brain_map.get(challengee_slimeoid.ai)
		s1moxie = challengee_slimeoid.atk + 1
		s1grit = challengee_slimeoid.defense + 1
		s1chutzpah = challengee_slimeoid.intel + 1

		s2name = str(challenger_slimeoid.name)
		s2weapon = ewcfg.offense_map.get(challenger_slimeoid.weapon)
		s2armor = ewcfg.defense_map.get(challenger_slimeoid.armor)
		s2special = ewcfg.special_map.get(challenger_slimeoid.special)
		s2legs = ewcfg.mobility_map.get(challenger_slimeoid.legs)
		s2brain = ewcfg.brain_map.get(challenger_slimeoid.ai)
		s2moxie = challenger_slimeoid.atk + 1
		s2grit = challenger_slimeoid.defense + 1
		s2chutzpah = challenger_slimeoid.intel + 1

		challenger_resistance = ""
		challengee_resistance = ""
		challenger_weakness = ""
		challengee_weakness = ""

		#challengee resistance/weakness
		if challengee_slimeoid.armor == 'scales':
			if challenger_slimeoid.weapon == 'electricity':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s scales conduct the electricity away from its vitals!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'TK':
				s2chutzpah += 2
				challengee_weakness = " {}'s scales refract and amplify the disrupting brainwaves inside its skull!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'boneplates':
			if challenger_slimeoid.weapon == 'blades':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s bone plates block the worst of the damage!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'spines':
				s2chutzpah += 2
				challengee_weakness = " {}'s bone plates only drive the quills deeper into its body as it moves!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'formless':
			if challenger_slimeoid.weapon == 'bludgeon':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s squishy body easily absorbs the blows!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'webs':
				s2chutzpah += 2
				challengee_weakness = " {}'s squishy body easily adheres to and becomes entangled by the webs!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'regeneration':
			if challenger_slimeoid.weapon == 'spikes':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {} quickly begins regenerating the small puncture wounds inflicted by the spikes!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'spit':
				s2chutzpah += 2
				challengee_weakness = " {}'s regeneration is impeded by the corrosive chemicals!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'stench':
			if challenger_slimeoid.weapon == 'teeth':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s noxious fumes make its opponent hesitant to put its mouth anywhere near it!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'throw':
				s2chutzpah += 2
				challengee_weakness = " {}'s foul odor gives away its position, making it easy to target with thrown projectiles!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'oil':
			if challenger_slimeoid.weapon == 'grip':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s slippery coating makes it extremely difficult to grab on to!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'fire':
				s2chutzpah += 2
				challengee_weakness = " {}'s oily coating is flammable, igniting as it contacts the flame!".format(challengee_slimeoid.name)
		if challengee_slimeoid.armor == 'quantumfield':
			if challenger_slimeoid.weapon == 'slam':
				s2moxie -= 2
				if s2moxie <= 1:
					s2moxie = 1
				challengee_resistance = " {}'s quantum superposition makes it difficult to hit head-on!".format(challengee_slimeoid.name)
			if challenger_slimeoid.special == 'laser':
				s2chutzpah += 2
				challengee_weakness = " {}'s quantum particles are excited by the high-frequency radiation, destabilizing its structure!".format(challengee_slimeoid.name)

		#challenger resistance/weakness
		if challenger_slimeoid.armor == 'scales':
			if challengee_slimeoid.weapon == 'electricity':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s scales conduct the electricity away from its vitals!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'TK':
				s1chutzpah += 2
				challenger_weakness = " {}'s scales refract and amplify the disrupting brainwaves inside its skull!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'boneplates':
			if challengee_slimeoid.weapon == 'blades':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s bone plates block the worst of the damage!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'spines':
				s1chutzpah += 2
				challenger_weakness = " {}'s bone plates only drive the quills deeper into its body as it moves!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'formless':
			if challengee_slimeoid.weapon == 'bludgeon':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s squishy body easily absorbs the blows!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'webs':
				s1chutzpah += 2
				challenger_weakness = " {}'s squishy body easily adheres to and becomes entangled by the webs!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'regeneration':
			if challengee_slimeoid.weapon == 'spikes':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {} quickly begins regenerating the small puncture wounds inflicted by the spikes!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'spit':
				s1chutzpah += 2
				challenger_weakness = " {}'s regeneration is impeded by the corrosive chemicals!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'stench':
			if challengee_slimeoid.weapon == 'teeth':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s noxious fumes make its opponent hesitant to put its mouth anywhere near it!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'throw':
				s1chutzpah += 2
				challenger_weakness = " {}'s foul odor gives away its position, making it easy to target with thrown projectiles!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'oil':
			if challengee_slimeoid.weapon == 'grip':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s slippery coating makes it extremely difficult to grab on to!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'fire':
				s1chutzpah += 2
				challenger_weakness = " {}'s oily coating is flammable, igniting as it contacts the flame!".format(challenger_slimeoid.name)
		if challenger_slimeoid.armor == 'quantumfield':
			if challengee_slimeoid.weapon == 'slam':
				s1moxie -= 2
				if s1moxie <= 1:
					s1moxie = 1
				challenger_resistance = " {}'s quantum superposition makes it difficult to hit head-on!".format(challenger_slimeoid.name)
			if challengee_slimeoid.special == 'laser':
				s1chutzpah += 2
				challenger_weakness = " {}'s quantum particles are excited by the high-frequency radiation, destabilizing its structure!".format(challenger_slimeoid.name)
			

		s1_active = False
		in_range = False

		if challengee_slimeoid.defense > challenger_slimeoid.defense:
			s1_active = True
		elif challengee_slimeoid.defense == challenger_slimeoid.defense:
			coinflip = random.randrange(1,3)
			if coinflip == 1:
				s1_active = True

		player = author

		response = "**{} sends {} out into the Battle Arena!**".format(author.display_name, s2name)
		await ewutils.send_message(cmd.client, cmd.message.channel, response)
		await asyncio.sleep(1)
		response = "**{} sends {} out into the Battle Arena!**".format(member.display_name, s1name)
		await ewutils.send_message(cmd.client, cmd.message.channel, response)
		await asyncio.sleep(1)
		response = "\nThe crowd erupts into cheers! The battle between {} and {} has begun! :crossed_swords:".format(s1name, s2name)
#		response += "\n{} {} {} {} {} {}".format(str(s1moxie),str(s1grit),str(s1chutzpah),str(challengee_slimeoid.weapon),str(challengee_slimeoid.armor),str(challengee_slimeoid.special))
#		response += "\n{} {} {} {} {} {}".format(str(s2moxie),str(s2grit),str(s2chutzpah),str(challenger_slimeoid.weapon),str(challenger_slimeoid.armor),str(challenger_slimeoid.special))
#		response += "\n{}, {}".format(str(challengee_resistance),str(challengee_weakness))
#		response += "\n{}, {}".format(str(challenger_resistance),str(challenger_weakness))
		await ewutils.send_message(cmd.client, cmd.message.channel, response)
		await asyncio.sleep(3)
			
		s1hpmax = 50 + (challengee_slimeoid.level * 20)
		s2hpmax = 50 + (challenger_slimeoid.level * 20)
		s1hp = s1hpmax
		s2hp = s2hpmax

		turncounter = 100
		while s1hp > 0 and s2hp > 0 and turncounter > 0:
			# Limit the number of turns in battle.
			turncounter -= 1

			response = ""
			battlecry = random.randrange(1,4)
			thrownobject = ewcfg.thrownobjects_list[random.randrange(len(ewcfg.thrownobjects_list))]
			if s1_active:
				player = member
				if in_range == False:

					#determine strat based on ai
					if challengee_slimeoid.ai in ['a', 'g']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'attack'
						else:
							strat = 'move'
					elif challengee_slimeoid.ai in ['b', 'd', 'f']:
						ranged_strat = random.randrange(1,3)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challengee_slimeoid.ai in ['c', 'e']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'

					#potentially add brain-based flavor text
					if strat == 'attack' and battlecry == 1:
						if (s1hpmax/s1hp) > 3:
							response = s1brain.str_battlecry_weak.format(
								slimeoid_name=s1name
							)
						else:
							response = s1brain.str_battlecry.format(
								slimeoid_name=s1name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					elif strat == 'move' and battlecry == 1:
						if (s1hpmax/s1hp) > 3:
							response = s1brain.str_movecry_weak.format(
								slimeoid_name=s1name
							)
						else:
							response = s1brain.str_movecry.format(
								slimeoid_name=s1name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					#perform action
					if strat == 'move':
						if (s1hpmax/s1hp) > 3:
							in_range = True
							response = s1legs.str_advance_weak.format(
								active=s1name,
								inactive=s2name,
							)
						else:
							in_range = True
							response = s1legs.str_advance.format(
								active=s1name,
								inactive=s2name,
							)
#						response += " *s1close*"

					else:
						hp = s2hp
						damage = (s1chutzpah * 10)
						s2hp -= damage
						response = "**"
						if s2hp <= 0:
							response += s1special.str_special_attack_coup.format(
								active=s1name,
								inactive=s2name,
								object=thrownobject
							)
							challenger_weakness = ""
						elif (s1hpmax/s1hp) > 3:
							response += s1special.str_special_attack_weak.format(
								active=s1name,
								inactive=s2name,
								object=thrownobject
							)
						else:
							response += s1special.str_special_attack.format(
								active=s1name,
								inactive=s2name,
								object=thrownobject
							)	
						response += "**"
						response += " :boom:"
#						response += " strat:{}".format(str(ranged_strat))

						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

						if challenger_weakness != "" or s2hp > 0:
							response = ""
							if challenger_weakness != "":
								response = challenger_weakness

							if s2hp > 0:
								if hp/damage > 10:
									response += " {} barely notices the damage.".format(challenger_slimeoid.name)
								elif hp/damage > 6:
									response += " {} is hurt, but shrugs it off.".format(challenger_slimeoid.name)
								elif hp/damage > 4:
									response += " {} felt that one!".format(challenger_slimeoid.name)
								elif hp/damage >= 3:
									response += " {} really felt that one!".format(challenger_slimeoid.name)
								elif hp/damage < 3:
									response += " {} reels from the force of the attack!!".format(challenger_slimeoid.name)							
#						response += " *s1shoot{}*".format(str(damage))
#						response += " *({}/{} s2hp)*".format(s2hp, s2hpmax)

				else:
					#determine strat based on ai
					if challengee_slimeoid.ai in ['a', 'b', 'c']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challengee_slimeoid.ai in ['d']:
						ranged_strat = random.randrange(1,3)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challengee_slimeoid.ai in ['e', 'f', 'g']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'attack'
						else:
							strat = 'move'

					#potentially add brain-based flavor text
					if strat == 'attack' and battlecry == 1:
						if (s1hpmax/s1hp) > 3:
							response = s1brain.str_battlecry_weak.format(
								slimeoid_name=s1name
							)
						else:
							response = s1brain.str_battlecry.format(
								slimeoid_name=s1name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					elif strat == 'move' and battlecry == 1:
						if (s1hpmax/s1hp) > 3:
							response = s1brain.str_movecry_weak.format(
								slimeoid_name=s1name
							)
						else:
							response = s1brain.str_movecry.format(
								slimeoid_name=s1name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					#perform action
					if strat == 'attack':
						hp = s2hp
						damage = int((s1moxie / s2grit) * 15)
						s2hp -= damage
						response = "**"
						if s2hp <= 0:
							response += s1weapon.str_attack_coup.format(
								active=s1name,
								inactive=s2name,
							)
							challenger_resistance = ""
						elif (s1hpmax/s1hp) > 3:
							response += s1weapon.str_attack_weak.format(
								active=s1name,
								inactive=s2name,
							)
						else:
							response += s1weapon.str_attack.format(
								active=s1name,
								inactive=s2name,
							)	
						response += "**"
						response += " :boom:"
#						response += " strat:{}".format(str(ranged_strat))

						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

						if challenger_resistance != "" or s2hp > 0:
							response = ""
							if challenger_resistance != "":
								response += challenger_resistance
							if s2hp > 0:
								if hp/damage > 10:
									response += " {} barely notices the damage.".format(challenger_slimeoid.name)
								elif hp/damage > 6:
									response += " {} is hurt, but shrugs it off.".format(challenger_slimeoid.name)
								elif hp/damage > 4:
									response += " {} felt that one!".format(challenger_slimeoid.name)
								elif hp/damage >= 3:
									response += " {} really felt that one!".format(challenger_slimeoid.name)
								elif hp/damage < 3:
									response += " {} reels from the force of the attack!!".format(challenger_slimeoid.name)				
#						response += " *s1hit{}*".format(str(damage))
#						response += " *({}/{}s2hp)*".format(s2hp, s2hpmax)

					else:
						if (s1hpmax/s1hp) > 3:
							in_range = False
							response = s1legs.str_retreat_weak.format(
								active=s1name,
								inactive=s2name,
							)
						else:
							in_range = False
							response = s1legs.str_retreat.format(
								active=s1name,
								inactive=s2name,
							)
#						response += " *s1flee*"

				s1_active = False

			else:
				player = author
				if in_range == False:

					#determine strat based on ai
					if challenger_slimeoid.ai in ['a', 'g']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'attack'
						else:
							strat = 'move'
					elif challenger_slimeoid.ai in ['b', 'd', 'f']:
						ranged_strat = random.randrange(1,3)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challenger_slimeoid.ai in ['c', 'e']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'

					#potentially add brain-based flavor text
					if strat == 'attack' and battlecry == 1:
						if (s2hpmax/s2hp) > 3:
							response = s2brain.str_battlecry_weak.format(
								slimeoid_name=s2name
							)
						else:
							response = s2brain.str_battlecry.format(
								slimeoid_name=s2name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					elif strat == 'move' and battlecry == 1:
						if (s2hpmax/s2hp) > 3:
							response = s2brain.str_movecry_weak.format(
								slimeoid_name=s2name
							)
						else:
							response = s2brain.str_movecry.format(
								slimeoid_name=s2name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					#perform action
					if strat == 'move':
						if (s2hpmax/s2hp) > 3:
							in_range = True
							response = s2legs.str_advance_weak.format(
								active=s2name,
								inactive=s1name,
							)
						else:
							in_range = True
							response = s2legs.str_advance.format(
								active=s2name,
								inactive=s1name,
							)
#						response += " *s2close*"

					else:
						hp = s1hp
						damage = (s2chutzpah * 10)
						s1hp -= damage
						response = "**"
						if s1hp <= 0:
							response += s2special.str_special_attack_coup.format(
								active=s2name,
								inactive=s1name,
								object=thrownobject
							)
							challengee_weakness = ""
						elif (s2hpmax/s2hp) > 3:
							response += s2special.str_special_attack_weak.format(
								active=s2name,
								inactive=s1name,
								object=thrownobject
							)
						else:
							response += s2special.str_special_attack.format(
								active=s2name,
								inactive=s1name,
								object=thrownobject
							)
						response += "**"
						response += " :boom:"
#						response += " strat:{}".format(str(ranged_strat))

						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

						if challengee_weakness != "" or s1hp > 0:
							response = ""
							if challengee_weakness != "":
								response += challengee_weakness
							if s1hp > 0:
								if hp/damage > 10:
									response += " {} barely notices the damage.".format(challengee_slimeoid.name)
								elif hp/damage > 6:
									response += " {} is hurt, but shrugs it off.".format(challengee_slimeoid.name)
								elif hp/damage > 4:
									response += " {} felt that one!".format(challengee_slimeoid.name)
								elif hp/damage >= 3:
									response += " {} really felt that one!".format(challengee_slimeoid.name)
								elif hp/damage < 3:
									response += " {} reels from the force of the attack!!".format(challengee_slimeoid.name)	
#						response += " *s2shoot{}*".format(str(damage))
#						response += " *({}/{} s1hp)*".format(s1hp, s1hpmax)
				else:

					#determine strat based on ai
					if challenger_slimeoid.ai in ['a', 'b', 'c']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challenger_slimeoid.ai in ['d']:
						ranged_strat = random.randrange(1,3)
						if ranged_strat < 2:
							strat = 'move'
						else:
							strat = 'attack'
					elif challenger_slimeoid.ai in ['e', 'f', 'g']:
						ranged_strat = random.randrange(1,5)
						if ranged_strat < 2:
							strat = 'attack'
						else:
							strat = 'move'

					#potentially add brain-based flavor text
					if strat == 'attack' and battlecry == 1:
						if (s2hpmax/s2hp) > 3:
							response = s2brain.str_battlecry_weak.format(
								slimeoid_name=s2name
							)
						else:
							response = s2brain.str_battlecry.format(
								slimeoid_name=s2name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					elif strat == 'move' and battlecry == 1:
						if (s2hpmax/s2hp) > 3:
							response = s2brain.str_movecry_weak.format(
								slimeoid_name=s2name
							)
						else:
							response = s2brain.str_movecry.format(
								slimeoid_name=s2name
							)
						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

					#perform action
					if strat == 'attack':
						hp = s1hp
						damage = int((s2moxie / s1grit) * 15)
						s1hp -= damage
						response = "**"
						if s1hp <= 0:
							response += s2weapon.str_attack_coup.format(
								active=s2name,
								inactive=s1name,
							)
							challengee_resistance = ""
						elif (s2hpmax/s2hp) > 3:
							response += s2weapon.str_attack_weak.format(
								active=s2name,
								inactive=s1name,
							)
						else:
							response += s2weapon.str_attack.format(
								active=s2name,
								inactive=s1name,
							)
						response += "**"
						response += " :boom:"
#						response += " strat:{}".format(str(ranged_strat))

						await ewutils.send_message(cmd.client, cmd.message.channel, response)
						await asyncio.sleep(1)

						if challengee_resistance != "" or s2hp > 0:
							response = ""
							if challengee_resistance != "":
								response = challengee_resistance

							if s1hp > 0:
								if hp/damage > 10:
									response += " {} barely notices the damage.".format(challengee_slimeoid.name)
								elif hp/damage > 6:
									response += " {} is hurt, but shrugs it off.".format(challengee_slimeoid.name)
								elif hp/damage > 4:
									response += " {} felt that one!".format(challengee_slimeoid.name)
								elif hp/damage >= 3:
									response += " {} really felt that one!".format(challengee_slimeoid.name)
								elif hp/damage < 3:
									response += " {} reels from the force of the attack!!".format(challengee_slimeoid.name)	

#						response += " *s2hit{}*".format(str(damage))
#						response += " *({}/{} s1hp)*".format(s1hp, s1hpmax)

					else:
						if (s2hpmax/s2hp) > 3:
							in_range = False
							response = s2legs.str_retreat_weak.format(
								active=s2name,
								inactive=s1name,
							)
						else:
							in_range = False
							response = s2legs.str_retreat.format(
								active=s2name,
								inactive=s1name,
							)
#						response += " *s2flee*"

				s1_active = True
				
			# Send the response to the player.
			if s1hp > 0 and s2hp > 0:
				await ewutils.send_message(cmd.client, cmd.message.channel, response)
				await asyncio.sleep(2)

		if s1hp <= 0:
			response = "\n" + s1legs.str_defeat.format(
				slimeoid_name=s1name
			)
			response += " {}".format(ewcfg.emote_slimeskull)
			response += "\n" + s2brain.str_victory.format(
				slimeoid_name=s2name
			)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			await asyncio.sleep(2)
			response = "\n**{} has won the Slimeoid battle!! The crowd erupts into cheers for {} and {}!!** :tada:".format(challenger_slimeoid.name, challenger_slimeoid.name, author.display_name)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			await asyncio.sleep(2)
		else:
			response = "\n" + s2legs.str_defeat.format(
				slimeoid_name=s2name
			)
			response += " {}".format(ewcfg.emote_slimeskull)
			response += "\n" + s1brain.str_victory.format(
				slimeoid_name=s1name
			)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			await asyncio.sleep(2)
			response = "\n**{} has won the Slimeoid battle!! The crowd erupts into cheers for {} and {}!!** :tada:".format(challengee_slimeoid.name, challengee_slimeoid.name, member.display_name)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			await asyncio.sleep(2)

	else:
		response = "{} was too cowardly to accept your challenge.".format(member.display_name).replace("@", "\{at\}")

		# Send the response to the player.
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
