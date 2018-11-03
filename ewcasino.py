import asyncio
import random
import time

import ewcmd
import ewutils
import ewcfg
import ewrolemgr
from ew import EwUser

# Map containing user IDs and the last time in UTC seconds since the pachinko
# machine was used.
last_pachinkoed_times = {}

# Map containing user IDs and the last time in UTC seconds since the player
# threw their dice.
last_crapsed_times = {}

# Map containing user IDs and the last time in UTC seconds since the slot
# machine was used.
last_slotsed_times = {}

# Map containing user IDs and the last time in UTC seconds since the player
# played roulette.
last_rouletted_times = {}

async def pachinko(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	global last_pachinkoed_times
	last_used = last_pachinkoed_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	response = ""

	if last_used + 10 > time_now:
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the Casino to gamble your SlimeCoin."
	else:
		last_pachinkoed_times[cmd.message.author.id] = time_now
		value = ewcfg.slimes_perpachinko

		user_data = EwUser(member = cmd.message.author)

		if value > user_data.slimecredit:
			response = "You don't have enough SlimeCoin to play."
		else:
			await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You insert {:,} SlimeCoin. Balls begin to drop!".format(ewcfg.slimes_perpachinko)))
			await asyncio.sleep(3)

			ball_count = 10
			response = ""
			winballs = 0

			# Drop ball_count balls
			while ball_count > 0:
				ball_count -= 1

				roll = random.randint(1, 5)
				response += "\n*plink*"

				# Add a varying number of plinks to make it feel more random.
				plinks = random.randint(1, 4)
				while plinks > 0:
					plinks -= 1
					response += " *plink*"
				response += " PLUNK"

				# 1/5 chance to win.
				if roll == 5:
					response += " ... **ding!**"
					winballs += 1

				await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

			winnings = int(winballs * ewcfg.slimes_perpachinko / 2)

			# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
			user_data = EwUser(member = cmd.message.author)

			# add winnings/subtract losses
			user_data.change_slimecredit(n = winnings - value, coinsource = ewcfg.coinsource_casino)
			user_data.persist()

			if winnings > 0:
				response += "\n\n**You won {:,} SlimeCoin!**".format(winnings)
			else:
				response += "\n\nYou lost your SlimeCoin."

		# Allow the player to pachinko again now that we're done.
		last_pachinkoed_times[cmd.message.author.id] = 0

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


async def craps(cmd):
	time_now = int(time.time())

	global last_crapsed_times
	last_used = last_crapsed_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	if last_used + 2 > time_now:
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the Casino to gamble your SlimeCoin."
	else:
		last_crapsed_times[cmd.message.author.id] = time_now
		value = None
		winnings = 0

		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)

		if value != None:
			user_data = EwUser(member = cmd.message.author)

			if value == -1:
				value = user_data.slimecredit

			elif value > user_data.slimecredit:
				response = "You don't have that much SlimeCoin to bet with."
			else:

				roll1 = random.randint(1,6)
				roll2 = random.randint(1,6)

				emotes_dice = [
					ewcfg.emote_dice1,
					ewcfg.emote_dice2,
					ewcfg.emote_dice3,
					ewcfg.emote_dice4,
					ewcfg.emote_dice5,
					ewcfg.emote_dice6
				]

				response = " {} {}".format(emotes_dice[roll1 - 1], emotes_dice[roll2 - 1])

				if (roll1 + roll2) == 7:
					winnings = 5 * value
					response += "\n\n**You rolled a 7! It's your lucky day. You won {:,} SlimeCoin.**".format(winnings)
				else:
					response += "\n\nYou didn't roll 7. You lost your SlimeCoins."

				# add winnings/subtract losses
				user_data.change_slimecredit(n = winnings - value, coinsource = ewcfg.coinsource_casino)
				user_data.persist()
		else:
			response = "Specify how much SlimeCoin you will wager."

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def slots(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	global last_slotsed_times
	last_used = last_slotsed_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	if last_used + 30 > time_now:
		# Rate limit slot machine action.
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the Casino to gamble your SlimeCoin."
	else:
		value = ewcfg.slimes_perslot
		last_slotsed_times[cmd.message.author.id] = time_now

		user_data = EwUser(member = cmd.message.author)

		if value > user_data.slimecredit:
			response = "You don't have enough SlimeCoin."
		else:
			# Add some suspense...
			await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You insert {:,} SlimeCoin and pull the handle...".format(ewcfg.slimes_perslot)))
			await asyncio.sleep(3)

			slots = [
				ewcfg.emote_tacobell,
				ewcfg.emote_pizzahut,
				ewcfg.emote_kfc,
				ewcfg.emote_moon,
				ewcfg.emote_111,
				ewcfg.emote_copkiller,
				ewcfg.emote_rowdyfucker,
				ewcfg.emote_theeye
			]
			slots_len = len(slots)

			# Roll those tumblers!
			spins = 3
			while spins > 0:
				await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "{} {} {}".format(
					slots[random.randrange(0, slots_len)],
					slots[random.randrange(0, slots_len)],
					slots[random.randrange(0, slots_len)]
				)))
				await asyncio.sleep(1)
				spins -= 1

			# Determine the final state.
			roll1 = slots[random.randrange(0, slots_len)]
			roll2 = slots[random.randrange(0, slots_len)]
			roll3 = slots[random.randrange(0, slots_len)]

			response = "{} {} {}".format(roll1, roll2, roll3)
			winnings = 0

			# Determine winnings.
			if roll1 == ewcfg.emote_tacobell and roll2 == ewcfg.emote_tacobell and roll3 == ewcfg.emote_tacobell:
				winnings = 5 * value
				response += "\n\n**¡Ándale! ¡Arriba! The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_pizzahut and roll2 == ewcfg.emote_pizzahut and roll3 == ewcfg.emote_pizzahut:
				winnings = 5 * value
				response += "\n\n**Oven-fired goodness! The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_kfc and roll2 == ewcfg.emote_kfc and roll3 == ewcfg.emote_kfc:
				winnings = 5 * value
				response += "\n\n**The Colonel's dead eyes unnerve you deeply. The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif (roll1 == ewcfg.emote_tacobell or roll1 == ewcfg.emote_kfc or roll1 == ewcfg.emote_pizzahut) and (roll2 == ewcfg.emote_tacobell or roll2 == ewcfg.emote_kfc or roll2 == ewcfg.emote_pizzahut) and (roll3 == ewcfg.emote_tacobell or roll3 == ewcfg.emote_kfc or roll3 == ewcfg.emote_pizzahut):
				winnings = value
				response += "\n\n**You dine on fast food. The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_moon and roll2 == ewcfg.emote_moon and roll3 == ewcfg.emote_moon:
				winnings = 5 * value
				response += "\n\n**Tonight seems like a good night for VIOLENCE. The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_111 and roll2 == ewcfg.emote_111 and roll3 == ewcfg.emote_111:
				winnings = 1111
				response += "\n\n**111111111111111111111111111111111111111111111111**\n\n**The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_copkiller and roll2 == ewcfg.emote_copkiller and roll3 == ewcfg.emote_copkiller:
				winnings = 40 * value
				response += "\n\n**How handsome!! The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_rowdyfucker and roll2 == ewcfg.emote_rowdyfucker and roll3 == ewcfg.emote_rowdyfucker:
				winnings = 40 * value
				response += "\n\n**So powerful!! The machine spits out {:,} SlimeCoin.**".format(winnings)

			elif roll1 == ewcfg.emote_theeye and roll2 == ewcfg.emote_theeye and roll3 == ewcfg.emote_theeye:
				winnings = 350 * value
				response += "\n\n**JACKPOT!! The machine spews forth {:,} SlimeCoin!**".format(winnings)

			else:
				response += "\n\n*Nothing happens...*"

			# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
			user_data = EwUser(member = cmd.message.author)

			# add winnings/subtract losses
			user_data.change_slimecredit(n = winnings - value, coinsource = ewcfg.coinsource_casino)
			user_data.persist()

		last_slotsed_times[cmd.message.author.id] = 0

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

async def roulette(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	bet = ""
	all_bets = ["0", "00", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
				"16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
				"32", "33", "34", "35", "36", "1strow", "2ndrow", "3rdrow", "1st12", "2nd12", "3rd12", "1to18",
				"19to36", "even", "odd", "pink", "purple", "green"]
	img_base = "https://ew.krakissi.net/img/cas/sr/"

	global last_rouletted_times
	last_used = last_rouletted_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	if last_used + 5 > time_now:
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
	else:
		last_rouletted_times[cmd.message.author.id] = time_now
		value = None

		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens = cmd.tokens[:2], allow_all = True)
			bet = ewutils.flattenTokenListToString(tokens = cmd.tokens[2:])

		if value != None:
			user_data = EwUser(member = cmd.message.author)

			if value == -1:
				value = user_data.slimecredit

			if value > user_data.slimecredit or value == 0:
				response = "You don't have enough SlimeCoin."
			elif len(bet) == 0:
				response = "You need to say what you're betting on. Options are: {}\n{}board.png".format(ewutils.formatNiceList(names = all_bets), img_base)
			elif bet not in all_bets:
				response = "The dealer didn't understand your wager. Options are: {}\n{}board.png".format(ewutils.formatNiceList(names = all_bets), img_base)
			else:
				await cmd.client.edit_message(resp, ewutils.formatMessage(
					cmd.message.author,
					img_base + "sr.gif"
				))

				await asyncio.sleep(5)

				roll = str(random.randint(1, 38))
				if roll == "37":
					roll = "0"
				if roll == "38":
					roll = "00"

				odd = ["1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "21", "23", "25", "27", "29", "31", "33", "35"]
				even = ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34", "36"]
				firstrow = ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"]
				secondrow = ["2", "5", "8", "11", "14", "17", "20", "23", "26", "29", "32", "35"]
				thirdrow = ["3", "6", "9", "12", "15", "18", "21", "24", "27", "30", "33", "36"]
				firsttwelve = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
				secondtwelve = ["13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
				thirdtwelve = ["25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]
				onetoeighteen = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
				nineteentothirtysix = ["19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]
				pink = ["2", "4", "6", "8", "10", "11", "13", "15", "17", "20", "22", "24", "26", "28", "29", "31", "33", "35"]
				purple = ["1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"]
				green = ["0", "00"]

				if roll == bet:
					winnings = (value * 36)
				elif bet == "1strow" and roll in firstrow:
					winnings = (value * 3)
				elif bet == "2ndrow" and roll in secondrow:
					winnings = (value * 3)
				elif bet == "3rdrow" and roll in thirdrow:
					winnings = (value * 3)
				elif bet == "1st12" and roll in firsttwelve:
					winnings = (value * 3)
				elif bet == "2nd12" and roll in secondtwelve:
					winnings = (value * 3)
				elif bet == "3rd12" and roll in thirdtwelve:
					winnings = (value * 3)
				elif bet == "1to18" and roll in onetoeighteen:
					winnings = (value * 2)
				elif bet == "19to36" and roll in nineteentothirtysix:
					winnings = (value * 2)
				elif bet == "odd" and roll in odd:
					winnings = (value * 2)
				elif bet == "even" and roll in even:
					winnings = (value * 2)
				elif bet == "pink" and roll in pink:
					winnings = (value * 2)
				elif bet == "purple" and roll in purple:
					winnings = (value * 2)
				elif bet == "green" and roll in green:
					winnings = (value * 18)
				else:
					winnings = 0

				response = "The ball landed on {}!\n".format(roll)
				if winnings > 0:
					response += " You won {} SlimeCoin!".format(winnings)
				else:
					response += " You lost your bet..."

				# Assemble image file name.
				response += "\n\n{}{}.gif".format(img_base, roll)

				# add winnings/subtract losses
				user_data.change_slimecredit(n = winnings - value, coinsource = ewcfg.coinsource_casino)
				user_data.persist()
		else:
			response = "Specify how much SlimeCoin you will wager."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

def check(str):
	if((str.content == ewcfg.cmd_accept) or (str.content == ewcfg.cmd_refuse)):
		return True

async def russian_roulette(cmd):
	if(cmd.message.channel.name != ewcfg.channel_casino):
		#Only at the casino
		response = "You can only play russian roulette at the casino"
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return

	if(cmd.mentions_count != 1):
		#Must mention only one player
		response = "Mention the player you want to challenge"
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return
	author = cmd.message.author
	challenger = EwUser(member = cmd.message.author)
	member = cmd.mentions[0]
	challengee = EwUser(member = cmd.mentions[0])
	if(challenger.id_user == challengee.id_user):
		response = "You might be looking for !suicide."
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
		return

	#Players have been challenged
	if(challenger.rr_challenger != ""):
		response = "You are already in the middle of a challenge."
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
		return

	if(challengee.rr_challenger != ""):
		response = "{} is already in the middle of a challenge.".format(member.display_name).replace("@", "\{at\}")
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
		return

	if(challenger.poi != challengee.poi):
		#Challangee must be in the casino
		response = "Both players must be in the casino."
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
		return

	#Players have to be enlisted
	if(challenger.life_state != ewcfg.life_state_enlisted or challengee.life_state != ewcfg.life_state_enlisted):
		if(challenger.life_state == ewcfg.life_state_corpse):
			response = "You try to grab the gun, but it falls through your hands. Ghosts can't hold weapons.".format(author.display_name).replace("@", "\{at\}")
			await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
			return
		elif (challengee.life_state == ewcfg.life_state_corpse):
			response = "{} tries to grab the gun, but it falls through their hands. Ghosts can't hold weapons.".format(member.display_name).replace("@", "\{at\}")
			await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
			return
		else:
			response = "Juveniles are too cowardly to gamble their lives."
			await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
			return

	response = "You have been challenged by {} to a game of russian roulette. Do you !accept or !refuse?".format(author.display_name).replace("@", "\{at\}")
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(member, response))
	#Assign a challenger so a player can't be challenged twice
	challenger.rr_challenger = challenger.id_user
	challengee.rr_challenger = challenger.id_user
	challenger.persist()
	challengee.persist()
	#Wait for an answer
	accepted = 0
	msg = await cmd.client.wait_for_message(timeout = 10, author = member, check=check)
	if(msg != None):
		if(msg.content == "!accept"):
			accepted = 1
	#Start game
	if(accepted == 1):
		challenger.time_last_rr = int(time.time())
		challengee.time_last_rr = int(time.time())
		for spin in range(1, 7):
			#Challenger goes second
			if((spin%2) == 0):
				player = author
			else:
				player = member
			response = "You put the gun to your head and pull the trigger..."
			res = await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(player, response))
			await asyncio.sleep(1)

			#Player dies
			if(random.randint(1, (7-spin)) == 1):
				await cmd.client.edit_message(res, ewutils.formatMessage(player, (response + " **BANG**")))
				#Challenger dies
				if((spin%2) == 0):
					response = "You return to the Casino with {}'s slime.".format(author.display_name).replace("@", "\{at\}")
					await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(member, response))
					challengee.change_slimes(n = challenger.slimes, source = ewcfg.source_killing)
					challenger.id_killer = challenger.id_user
					challenger.die(cause = ewcfg.cause_suicide)

				#Challangee dies
				else:
					response = "You return to the Casino with {}'s slime.".format(member.display_name).replace("@", "\{at\}")
					await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))
					challenger.change_slimes(n = challengee.slimes, source = ewcfg.source_killing)
					challengee.id_killer = challengee.id_user
					challengee.die(cause = ewcfg.cause_suicide)					
				break

			#Or survives
			else:
				await cmd.client.edit_message(res, ewutils.formatMessage(player, (response + " but it's empty")))
				await asyncio.sleep(1)
				#track spins ?
	#Or cancel the challenge
	else:
		response = "{} was too cowardly to accept your challenge.".format(member.display_name).replace("@", "\{at\}")
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(author, response))

	challenger.rr_challenger = ""
	challengee.rr_challenger = ""
	challenger.persist()
	challengee.persist()
	await ewrolemgr.updateRoles(client = cmd.client, member = author)
	await ewrolemgr.updateRoles(client = cmd.client, member = member)
	deathreport = "You arrive among the dead by your own volition. {}".format(ewcfg.emote_slimeskull)
	deathreport = "{} ".format(ewcfg.emote_slimeskull) + ewutils.formatMessage(player, deathreport)
	sewerchannel = ewutils.get_channel(cmd.message.server, ewcfg.channel_sewers)
	await cmd.client.send_message(sewerchannel, deathreport)
	return
