import asyncio
import random
import time

import ewcmd
import ewutils
import ewcfg
from ew import EwUser, EwMarket

# Map containing user IDs and the last time in UTC seconds since the pachinko
# machine was used.
last_pachinkoed_times = {}

# Map containing user IDs and the last time in UTC seconds since the player
# threw their dice.
last_crapsed_times = {}

# Map containing user IDs and the last time in UTC seconds since the slot
# machine was used.
last_slotsed_times = {}


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
		response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
	else:
		last_pachinkoed_times[cmd.message.author.id] = time_now
		value = ewcfg.slimes_perpachinko

		try:
			conn = ewutils.databaseConnect()
			cursor = conn.cursor()

			market_data = EwMarket(id_server=cmd.message.server.id, conn=conn, cursor=cursor)
			user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
		finally:
			cursor.close()
			conn.close()

		if ewcmd.is_casino_open(market_data.clock) == False:
			response = ewcfg.str_casino_closed
		elif value > user_data.slimecredit:
			response = "You don't have enough SlimeCoin to play."
		else:
			#subtract slimecoin from player
			user_data.slimecredit -= value
			user_data.persist()

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

			winnings = winballs * 250
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
				user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)

				# add winnings
				user_data.slimecredit += winnings

				user_data.persist(conn=conn, cursor=cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()

			if winnings > 0:
				response += "\n\n**You won {:,} SlimeCoin!**".format(winnings)
			else:
				response += "\n\nYou lost your SlimeCoin."

		# Allow the player to pachinko again now that we're done.
		last_pachinkoed_times[cmd.message.author.id] = 0

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


async def craps(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	global last_crapsed_times
	last_used = last_crapsed_times.get(cmd.message.author.id)

	if last_used == None:
		last_used = 0

	if last_used + 2 > time_now:
		response = "**ENOUGH**"
	elif cmd.message.channel.name != ewcfg.channel_casino:
		# Only allowed in the slime casino.
		response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
	else:
		last_crapsed_times[cmd.message.author.id] = time_now
		value = None

		if cmd.tokens_count > 1:
			for token in cmd.tokens[1:]:
				try:
					value = int(token)
					if value < 0:
						value = None
					break
				except:
					value = None

		if value != None:
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
				market_data = EwMarket(id_server=cmd.message.author.server.id, conn=conn, cursor=cursor)
			finally:
				cursor.close()
				conn.close()


			if ewcmd.is_casino_open(market_data.clock) == False:
				response = ewcfg.str_casino_closed
			elif value > user_data.slimecredit:
				response = "You don't have that much SlimeCoin to bet with."
			else:
				user_data.slimecredit -= value

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
				crapstokens = cmd.message.content.split(' ')

				if (roll1 + roll2) == 7:
					winnings = 5 * value
					response += "\n\n**You rolled a 7! It's your lucky day. You won {:,} SlimeCoin.**".format(winnings)
					user_data.slimecredit += winnings
				else:
					response += "\n\nYou didn't roll 7. You lost your SlimeCoins."

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data.persist(conn=conn, cursor=cursor)
					market_data.persist(conn=conn, cursor=cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()
		else:
			response = "Specify how much SlimeCoin you will wager."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

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
		response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
	else:
		value = ewcfg.slimes_perslot
		last_slotsed_times[cmd.message.author.id] = time_now

		try:
			conn = ewutils.databaseConnect()
			cursor = conn.cursor()

			user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
			market_data = EwMarket(id_server=cmd.message.author.server.id, conn=conn, cursor=cursor)

		finally:
			cursor.close()
			conn.close()

		if ewcmd.is_casino_open(market_data.clock) == False:
			response = ewcfg.str_casino_closed
		elif value > user_data.slimecredit:
			response = "You don't have enough SlimeCoin."
		else:
			#subtract slimecoin from player
			user_data.slimecredit -= value
			user_data.persist()

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

			# Add winnings (if there were any) and save the user data.
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
				user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)

				# add winnings
				user_data.slimecredit += winnings

				user_data.persist(conn=conn, cursor=cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()

		last_slotsed_times[cmd.message.author.id] = 0

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
