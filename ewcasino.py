import asyncio
import random
import time

import ewcmd
import ewutils
import ewcfg
import ewrolemgr
import ewitem
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

# Map containing user IDs and the last time in UTC seconds since the player
# played russian roulette.
last_russianrouletted_times = {}

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
			await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, "You insert {:,} SlimeCoin. Balls begin to drop!".format(ewcfg.slimes_perpachinko)))
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

				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))


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
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

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
			await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, "You insert {:,} SlimeCoin and pull the handle...".format(ewcfg.slimes_perslot)))
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
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, "{} {} {}".format(
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

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
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(
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
	await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

async def baccarat(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	bet = ""
	all_bets = ["player", "dealer", "tie"]
	img_base = "https://ew.krakissi.net/img/cas/sb/"
	response = ""
	rank = ""
	suit = ""
	str_ranksuit = " the **{} of {}**. "

	global last_rouletted_times
	last_used = last_rouletted_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	if last_used + 2 > time_now:
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the Casino to gamble your SlimeCoin."
		await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
		await asyncio.sleep(1)
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
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

			elif len(bet) == 0:
				response = "You must specify what hand you are betting on. Options are {}.".format(ewutils.formatNiceList(names = all_bets), img_base)
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

			elif bet not in all_bets:
				response = "The dealer didn't understand your wager. Options are {}.".format(ewutils.formatNiceList(names = all_bets), img_base)
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

			else:
				resp_d = await ewcmd.start(cmd = cmd)
				resp_f = await ewcmd.start(cmd = cmd)
				response = "You bet {} SlimeCoin on {}. The dealer shuffles the deck, then begins to deal.".format(str(value),str(bet))
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

				response += "\nThe dealer deals you your first card..."

				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(3)

				winnings = 0
				end = False
				phit = False
				d = 0
				p = 0

				drawp1 = str(random.randint(1,52))
				if drawp1 in ["1", "14", "27", "40"]:
					p += 1
				if drawp1 in ["2", "15", "28", "41"]:
					p += 2
				if drawp1 in ["3", "16", "29", "42"]:
					p += 3
				if drawp1 in ["4", "17", "30", "43"]:
					p += 4
				if drawp1 in ["5", "18", "31", "44"]:
					p += 5
				if drawp1 in ["6", "19", "32", "45"]:
					p += 6
				if drawp1 in ["7", "20", "33", "46"]:
					p += 7
				if drawp1 in ["8", "21", "34", "47"]:
					p += 8
				if drawp1 in ["9", "22", "35", "48"]:
					p += 9
				if drawp1 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
					p += 0
				lastcard = drawp1
				if lastcard in ["1", "14", "27", "40"]:
					rank = "Ace"
				if lastcard in ["2", "15", "28", "41"]:
					rank = "Two"
				if lastcard in ["3", "16", "29", "42"]:
					rank = "Three"
				if lastcard in ["4", "17", "30", "43"]:
					rank = "Four"
				if lastcard in ["5", "18", "31", "44"]:
					rank = "Five"
				if lastcard in ["6", "19", "32", "45"]:
					rank = "Six"
				if lastcard in ["7", "20", "33", "46"]:
					rank = "Seven"
				if lastcard in ["8", "21", "34", "47"]:
					rank = "Eight"
				if lastcard in ["9", "22", "35", "48"]:
					rank = "Nine"
				if lastcard in ["10", "23", "36", "49"]:
					rank = "Ten"
				if lastcard in ["11", "24", "37", "50"]:
					rank = "Jack"
				if lastcard in ["12", "25", "38", "51"]:
					rank = "Queen"
				if lastcard in ["13", "26", "39", "52"]:
					rank = "King"
				if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
					suit = "Hearts"
				if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
					suit = "Slugs"
				if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
					suit = "Hats"
				if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
					suit = "Shields"

				if p > 9:
					p -= 10
				if d > 9:
					d -= 10

				response += str_ranksuit.format(rank, suit)
				response += img_base + lastcard + ".png"

				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)
				response += "\nThe dealer deals you your second card..."
				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(3)

				while True:
					drawp2 = str(random.randint(1,52))
					if drawp2 != drawp1:
						break
				if drawp2 in ["1", "14", "27", "40"]:
					p += 1
				if drawp2 in ["2", "15", "28", "41"]:
					p += 2
				if drawp2 in ["3", "16", "29", "42"]:
					p += 3
				if drawp2 in ["4", "17", "30", "43"]:
					p += 4
				if drawp2 in ["5", "18", "31", "44"]:
					p += 5
				if drawp2 in ["6", "19", "32", "45"]:
					p += 6
				if drawp2 in ["7", "20", "33", "46"]:
					p += 7
				if drawp2 in ["8", "21", "34", "47"]:
					p += 8
				if drawp2 in ["9", "22", "35", "48"]:
					p += 9
				if drawp2 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
					p += 0
				lastcard = drawp2
				if lastcard in ["1", "14", "27", "40"]:
					rank = "Ace"
				if lastcard in ["2", "15", "28", "41"]:
					rank = "Two"
				if lastcard in ["3", "16", "29", "42"]:
					rank = "Three"
				if lastcard in ["4", "17", "30", "43"]:
					rank = "Four"
				if lastcard in ["5", "18", "31", "44"]:
					rank = "Five"
				if lastcard in ["6", "19", "32", "45"]:
					rank = "Six"
				if lastcard in ["7", "20", "33", "46"]:
					rank = "Seven"
				if lastcard in ["8", "21", "34", "47"]:
					rank = "Eight"
				if lastcard in ["9", "22", "35", "48"]:
					rank = "Nine"
				if lastcard in ["10", "23", "36", "49"]:
					rank = "Ten"
				if lastcard in ["11", "24", "37", "50"]:
					rank = "Jack"
				if lastcard in ["12", "25", "38", "51"]:
					rank = "Queen"
				if lastcard in ["13", "26", "39", "52"]:
					rank = "King"
				if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
					suit = "Hearts"
				if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
					suit = "Slugs"
				if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
					suit = "Hats"
				if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
					suit = "Shields"

				if p > 9:
					p -= 10
				if d > 9:
					d -= 10

				response += str_ranksuit.format(rank, suit)
				response += img_base + lastcard + ".png"

				await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)

				responsesave = response

				response = "\nThe dealer deals the house its first card..."

				await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(3)

				while True:
					drawd1 = str(random.randint(1,52))
					if drawd1 != drawp1 and drawd1 != drawp2:
						break
				if drawd1 in ["1", "14", "27", "40"]:
					d += 1
				if drawd1 in ["2", "15", "28", "41"]:
					d += 2
				if drawd1 in ["3", "16", "29", "42"]:
					d += 3
				if drawd1 in ["4", "17", "30", "43"]:
					d += 4
				if drawd1 in ["5", "18", "31", "44"]:
					d += 5
				if drawd1 in ["6", "19", "32", "45"]:
					d += 6
				if drawd1 in ["7", "20", "33", "46"]:
					d += 7
				if drawd1 in ["8", "21", "34", "47"]:
					d += 8
				if drawd1 in ["9", "22", "35", "48"]:
					d += 9
				if drawd1 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
					d += 0
				lastcard = drawd1
				if lastcard in ["1", "14", "27", "40"]:
					rank = "Ace"
				if lastcard in ["2", "15", "28", "41"]:
					rank = "Two"
				if lastcard in ["3", "16", "29", "42"]:
					rank = "Three"
				if lastcard in ["4", "17", "30", "43"]:
					rank = "Four"
				if lastcard in ["5", "18", "31", "44"]:
					rank = "Five"
				if lastcard in ["6", "19", "32", "45"]:
					rank = "Six"
				if lastcard in ["7", "20", "33", "46"]:
					rank = "Seven"
				if lastcard in ["8", "21", "34", "47"]:
					rank = "Eight"
				if lastcard in ["9", "22", "35", "48"]:
					rank = "Nine"
				if lastcard in ["10", "23", "36", "49"]:
					rank = "Ten"
				if lastcard in ["11", "24", "37", "50"]:
					rank = "Jack"
				if lastcard in ["12", "25", "38", "51"]:
					rank = "Queen"
				if lastcard in ["13", "26", "39", "52"]:
					rank = "King"
				if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
					suit = "Hearts"
				if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
					suit = "Slugs"
				if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
					suit = "Hats"
				if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
					suit = "Shields"

				if p > 9:
					p -= 10
				if d > 9:
					d -= 10

				response += str_ranksuit.format(rank, suit)
				response += img_base + lastcard + ".png"

				await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)
				response += "\nThe dealer deals the house its second card..."
				await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(3)

				while True:
					drawd2 = str(random.randint(1,52))
					if drawd2 != drawp1 and drawd2 != drawp2 and drawd2 != drawd1:
						break
				if drawd2 in ["1", "14", "27", "40"]:
					d += 1
				if drawd2 in ["2", "15", "28", "41"]:
					d += 2
				if drawd2 in ["3", "16", "29", "42"]:
					d += 3
				if drawd2 in ["4", "17", "30", "43"]:
					d += 4
				if drawd2 in ["5", "18", "31", "44"]:
					d += 5
				if drawd2 in ["6", "19", "32", "45"]:
					d += 6
				if drawd2 in ["7", "20", "33", "46"]:
					d += 7
				if drawd2 in ["8", "21", "34", "47"]:
					d += 8
				if drawd2 in ["9", "22", "35", "48"]:
					d += 9
				if drawd2 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
					d += 0
				lastcard = drawd2
				if lastcard in ["1", "14", "27", "40"]:
					rank = "Ace"
				if lastcard in ["2", "15", "28", "41"]:
					rank = "Two"
				if lastcard in ["3", "16", "29", "42"]:
					rank = "Three"
				if lastcard in ["4", "17", "30", "43"]:
					rank = "Four"
				if lastcard in ["5", "18", "31", "44"]:
					rank = "Five"
				if lastcard in ["6", "19", "32", "45"]:
					rank = "Six"
				if lastcard in ["7", "20", "33", "46"]:
					rank = "Seven"
				if lastcard in ["8", "21", "34", "47"]:
					rank = "Eight"
				if lastcard in ["9", "22", "35", "48"]:
					rank = "Nine"
				if lastcard in ["10", "23", "36", "49"]:
					rank = "Ten"
				if lastcard in ["11", "24", "37", "50"]:
					rank = "Jack"
				if lastcard in ["12", "25", "38", "51"]:
					rank = "Queen"
				if lastcard in ["13", "26", "39", "52"]:
					rank = "King"
				if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
					suit = "Hearts"
				if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
					suit = "Slugs"
				if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
					suit = "Hats"
				if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
					suit = "Shields"

				if p > 9:
					p -= 10
				if d > 9:
					d -= 10

				response += str_ranksuit.format(rank, suit)
				response += img_base + lastcard + ".png"

				await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
				await asyncio.sleep(1)
				responsesave_d = response

				if d in [8, 9] or p in [8, 9]:
					end = True

				drawp3 = ""
				if (p <= 5) and (end != True):

					response = responsesave
					response += "\nThe dealer deals you another card..."

					await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
					await asyncio.sleep(3)

					phit = True
					while True:
						drawp3 = str(random.randint(1,52))
						if drawp3 != drawp1 and drawp3 != drawp2 and drawp3 != drawd1 and drawp3 != drawd2:
							break
					if drawp3 in ["1", "14", "27", "40"]:
						p += 1
					if drawp3 in ["2", "15", "28", "41"]:
						p += 2
					if drawp3 in ["3", "16", "29", "42"]:
						p += 3
					if drawp3 in ["4", "17", "30", "43"]:
						p += 4
					if drawp3 in ["5", "18", "31", "44"]:
						p += 5
					if drawp3 in ["6", "19", "32", "45"]:
						p += 6
					if drawp3 in ["7", "20", "33", "46"]:
						p += 7
					if drawp3 in ["8", "21", "34", "47"]:
						p += 8
					if drawp3 in ["9", "22", "35", "48"]:
						p += 9
					if drawp3 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
						p += 0
					lastcard = drawp3
					if lastcard in ["1", "14", "27", "40"]:
						rank = "Ace"
					if lastcard in ["2", "15", "28", "41"]:
						rank = "Two"
					if lastcard in ["3", "16", "29", "42"]:
						rank = "Three"
					if lastcard in ["4", "17", "30", "43"]:
						rank = "Four"
					if lastcard in ["5", "18", "31", "44"]:
						rank = "Five"
					if lastcard in ["6", "19", "32", "45"]:
						rank = "Six"
					if lastcard in ["7", "20", "33", "46"]:
						rank = "Seven"
					if lastcard in ["8", "21", "34", "47"]:
						rank = "Eight"
					if lastcard in ["9", "22", "35", "48"]:
						rank = "Nine"
					if lastcard in ["10", "23", "36", "49"]:
						rank = "Ten"
					if lastcard in ["11", "24", "37", "50"]:
						rank = "Jack"
					if lastcard in ["12", "25", "38", "51"]:
						rank = "Queen"
					if lastcard in ["13", "26", "39", "52"]:
						rank = "King"
					if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
						suit = "Hearts"
					if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
						suit = "Slugs"
					if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
						suit = "Hats"
					if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
						suit = "Shields"

					if p > 9:
						p -= 10
					if d > 9:
						d -= 10

					response += str_ranksuit.format(rank, suit)
					response += img_base + lastcard + ".png"

					await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))
					await asyncio.sleep(1)

				if ((phit != True and d <= 5) or (phit == True and ((d <= 2) or (d == 3 and drawp3 not in ["8", "21", "34", "47"]) or (d == 4 and drawp3 in ["2", "15", "28", "41", "3", "16", "29", "42", "4", "17", "30", "43", "5", "18", "31", "44", "6", "19", "32", "45", "7", "20", "33", "46"]) or (d == 5 and drawp3 in ["4", "17", "30", "43", "5", "18", "31", "44", "6", "19", "32", "45", "7", "20", "33", "46"]) or (d == 6 and drawp3 in ["6", "19", "32", "45", "7", "20", "33", "46"])))) and (d != 7) and (end != True):
					
					response = responsesave_d
					response += "\nThe dealer deals the house another card..."
					await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
					await asyncio.sleep(3)
					
					while True:
						drawd3 = str(random.randint(1,52))
						if drawd3 != drawp1 and drawd3 != drawp2 and drawd3 != drawd1 and drawd3 != drawd2 and drawd3 != drawp3:
							break
					if drawd3 in ["1", "14", "27", "40"]:
						d += 1
					if drawd3 in ["2", "15", "28", "41"]:
						d += 2
					if drawd3 in ["3", "16", "29", "42"]:
						d += 3
					if drawd3 in ["4", "17", "30", "43"]:
						d += 4
					if drawd3 in ["5", "18", "31", "44"]:
						d += 5
					if drawd3 in ["6", "19", "32", "45"]:
						d += 6
					if drawd3 in ["7", "20", "33", "46"]:
						d += 7
					if drawd3 in ["8", "21", "34", "47"]:
						d += 8
					if drawd3 in ["9", "22", "35", "48"]:
						d += 9
					if drawd3 in ["10","11","12","13","23","24","25","26","36","37","38","39","49","50","51","52"]:
						d += 0
					lastcard = drawd3
					if lastcard in ["1", "14", "27", "40"]:
						rank = "Ace"
					if lastcard in ["2", "15", "28", "41"]:
						rank = "Two"
					if lastcard in ["3", "16", "29", "42"]:
						rank = "Three"
					if lastcard in ["4", "17", "30", "43"]:
						rank = "Four"
					if lastcard in ["5", "18", "31", "44"]:
						rank = "Five"
					if lastcard in ["6", "19", "32", "45"]:
						rank = "Six"
					if lastcard in ["7", "20", "33", "46"]:
						rank = "Seven"
					if lastcard in ["8", "21", "34", "47"]:
						rank = "Eight"
					if lastcard in ["9", "22", "35", "48"]:
						rank = "Nine"
					if lastcard in ["10", "23", "36", "49"]:
						rank = "Ten"
					if lastcard in ["11", "24", "37", "50"]:
						rank = "Jack"
					if lastcard in ["12", "25", "38", "51"]:
						rank = "Queen"
					if lastcard in ["13", "26", "39", "52"]:
						rank = "King"
					if lastcard in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]:
						suit = "Hearts"
					if lastcard in ["14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]:
						suit = "Slugs"
					if lastcard in ["27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]:
						suit = "Hats"
					if lastcard in ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]:
						suit = "Shields"

					if p > 9:
						p -= 10
					if d > 9:
						d -= 10

					response += str_ranksuit.format(rank, suit)
					response += img_base + lastcard + ".png"

					await ewutils.edit_message(cmd.client, resp_d, ewutils.formatMessage(cmd.message.author, response))
					await asyncio.sleep(2)

				if p > 9:
					p -= 10
				if d > 9:
					d -= 10

				if p > d:
					response = "\n\nPlayer hand beats the dealer hand {} to {}.".format(str(p), str(d))
					result = "player"
					odds = 2
				elif d > p:
					response = "\n\nDealer hand beats the player hand {} to {}.".format(str(d), str(p))
					result = "dealer"
					odds = 2
				else: # p == d (peed lol)
					response = "\n\nPlayer hand and dealer hand tied at {}.".format(str(p))
					result = "tie"
					odds = 8

				if bet == result:
					winnings = (odds * value)
					response += "\n\n**You won {:,} SlimeCoin!**".format(winnings)
				else:
					response += "\n\n*You lost your bet.*"

				# add winnings/subtract losses
				user_data = EwUser(member = cmd.message.author)
				user_data.change_slimecredit(n = winnings - value, coinsource = ewcfg.coinsource_casino)
				user_data.persist()
				await ewutils.edit_message(cmd.client, resp_f, ewutils.formatMessage(cmd.message.author, response))

		else:
			response = "Specify how much SlimeCoin you will wager."
			await ewutils.edit_message(cmd.client, resp, ewutils.formatMessage(cmd.message.author, response))

def check(str):
	if str.content == ewcfg.cmd_accept or str.content == ewcfg.cmd_refuse:
		return True

async def russian_roulette(cmd):
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_casino:
		#Only at the casino
		response = "You can only play russian roulette at the casino."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if cmd.mentions_count != 1:
		#Must mention only one player
		response = "Mention the player you want to challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	author = cmd.message.author
	member = cmd.mentions[0]

	global last_russianrouletted_times
	last_used_author = last_russianrouletted_times.get(author.id)
	last_used_member = last_russianrouletted_times.get(member.id)

	if last_used_author == None:
		last_used_author = 0
	if last_used_member == None:
		last_used_member = 0

	if last_used_author + ewcfg.cd_rr > time_now or last_used_member + ewcfg.cd_rr > time_now:
		response = "**ENOUGH**"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if author.id == member.id:
		response = "You might be looking for !suicide."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	challenger = EwUser(member = author)
	challengee = EwUser(member = member)

	#Players have been challenged
	if challenger.rr_challenger != "":
		response = "You are already in the middle of a challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challengee.rr_challenger != "":
		response = "{} is already in the middle of a challenge.".format(member.display_name).replace("@", "\{at\}")
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger.poi != challengee.poi:
		#Challangee must be in the casino
		response = "Both players must be in the casino."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Players have to be enlisted
	if challenger.life_state != ewcfg.life_state_enlisted or challengee.life_state != ewcfg.life_state_enlisted:
		if challenger.life_state == ewcfg.life_state_corpse:
			response = "You try to grab the gun, but it falls through your hands. Ghosts can't hold weapons.".format(author.display_name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

		elif challengee.life_state == ewcfg.life_state_corpse:
			response = "{} tries to grab the gun, but it falls through their hands. Ghosts can't hold weapons.".format(member.display_name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

		else:
			response = "Juveniles are too cowardly to gamble their lives."
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Assign a challenger so players can't be challenged
	challenger.rr_challenger = challenger.id_user
	challengee.rr_challenger = challenger.id_user

	challenger.persist()
	challengee.persist()

	response = "You have been challenged by {} to a game of russian roulette. Do you !accept or !refuse?".format(author.display_name).replace("@", "\{at\}")
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

	#Start game
	if accepted == 1:

		for spin in range(1, 7):
			challenger = EwUser(member = author)
			challengee = EwUser(member = member)
			
			#In case any of the players suicide mid-game
			if challenger.life_state == ewcfg.life_state_corpse:
				response = "{} couldn't handle the pressure and killed themselves.".format(author.display_name).replace("@", "\{at\}")
				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(member, response))
				break
				
			if challengee.life_state == ewcfg.life_state_corpse:
				response = "{} couldn't handle the pressure and killed themselves.".format(member.display_name).replace("@", "\{at\}")
				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
				break
				
			#Challenger goes second
			if spin % 2 == 0:
				player = author
			else:
				player = member

			response = "You put the gun to your head and pull the trigger..."
			res = await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(player, response))
			await asyncio.sleep(1)

			#Player dies
			if random.randint(1, (7 - spin)) == 1:
				await ewutils.edit_message(cmd.client, res, ewutils.formatMessage(player, (response + " **BANG**")))
				response = "You return to the Casino with {}'s slime.".format(player.display_name).replace("@", "\{at\}")
				was_suicide = False
				#Challenger dies
				if spin % 2 == 0:
					winner = member

					challenger = EwUser(member = author)
					challengee = EwUser(member = member)
					
					if challengee.life_state != ewcfg.life_state_corpse:
						challengee.change_slimes(n = challenger.slimes, source = ewcfg.source_killing)
						ewitem.item_loot(member = author, id_user_target = member.id)
						
						challenger.id_killer = challenger.id_user
						challenger.die(cause = ewcfg.cause_suicide)
					#In case the other player killed themselves
					else:
						was_suicide = True
						winner = author
						response = "You shoot {}'s corpse, adding insult to injury.".format(member.display_name).replace("@", "\{at\}")

				#Challangee dies
				else:
					winner = author

					challenger = EwUser(member = author)
					challengee = EwUser(member = member)

					if challenger.life_state != ewcfg.life_state_corpse:					
						challenger.change_slimes(n = challengee.slimes, source = ewcfg.source_killing)
						ewitem.item_loot(member = member, id_user_target = author.id)

						challengee.id_killer = challengee.id_user
						challengee.die(cause = ewcfg.cause_suicide)
					#In case the other player killed themselves
					else:
						was_suicide = True
						winner = member
						response = "You shoot {}'s corpse, adding insult to injury.".format(author.display_name).replace("@", "\{at\}")
					
				challenger.rr_challenger = ""
				challengee.rr_challenger = ""

				challenger.persist()
				challengee.persist()

				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(winner, response))

				await ewrolemgr.updateRoles(client = cmd.client, member = author)
				await ewrolemgr.updateRoles(client = cmd.client, member = member)

				if was_suicide == False:
					deathreport = "You arrive among the dead by your own volition. {}".format(ewcfg.emote_slimeskull)
					deathreport = "{} ".format(ewcfg.emote_slimeskull) + ewutils.formatMessage(player, deathreport)

					sewerchannel = ewutils.get_channel(cmd.message.server, ewcfg.channel_sewers)
					await ewutils.send_message(cmd.client, sewerchannel, deathreport)

				break

			#Or survives
			else:
				await ewutils.edit_message(cmd.client, res, ewutils.formatMessage(player, (response + " but it's empty")))
				await asyncio.sleep(1)
				#track spins?

	#Or cancel the challenge
	else:
		response = "{} was too cowardly to accept your challenge.".format(member.display_name).replace("@", "\{at\}")
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
		last_russianrouletted_times[author.id] = time_now - 540
		last_russianrouletted_times[member.id] = time_now - 540


	challenger = EwUser(member = author)
	challengee = EwUser(member = member)

	challenger.rr_challenger = ""
	challengee.rr_challenger = ""

	challenger.persist()
	challengee.persist()

	return
