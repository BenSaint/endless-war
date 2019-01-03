"""
	Commands and utilities related to Juveniles.
"""
import time
import random
import math

import ewcfg
import ewutils
import ewcmd
import ewitem
import ewmap
import ewrolemgr
import ewstats
from ew import EwUser, EwMarket

# Map of user ID to a map of recent miss-mining time to count. If the count
# exceeds 3 in 5 seconds, you die.
last_mismined_times = {}

""" player enlists in a faction/gang """
async def enlist(cmd):
	time_now = int(time.time())
	response = ""
	user_data = EwUser(member = cmd.message.author)

	if user_data.life_state == ewcfg.life_state_grandfoe:
		return

	if user_data.life_state == ewcfg.life_state_juvenile:
		faction = ""
		if cmd.tokens_count > 1:
			faction = cmd.tokens[1].lower()

		user_slimes = user_data.slimes

		if user_slimes < ewcfg.slimes_toenlist:
			response = "You need to mine more slime to rise above your lowly station. ({}/{})".format(user_slimes, ewcfg.slimes_toenlist)
		else:
			if faction == "":
				faction = user_data.faction

			if faction == ewcfg.faction_rowdys or faction == ewcfg.faction_killers:
				if len(user_data.faction) > 0 and user_data.faction != faction:
					# Disallow joining a new faction. Player must be pardoned first.
					response = "Disgusting traitor. You can only join the {}.".format(user_data.faction)
				else:
					response = "Enlisting in the {}.".format(faction)

					user_data.life_state = ewcfg.life_state_enlisted
					user_data.faction = faction
					user_data.persist()

				await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
			else:
				response = "Which faction? Say '{} {}' or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys)

	elif user_data.life_state == ewcfg.life_state_corpse:
		response = 'You are dead, bitch.'

	else:
		response = "You can't do that right now, bitch."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" mine for slime (or endless rocks) """
async def mine(cmd):
	market_data = EwMarket(id_server = cmd.message.author.server.id)
	user_data = EwUser(member = cmd.message.author)

	# Kingpins can't mine.
	if user_data.life_state == ewcfg.life_state_kingpin or user_data.life_state == ewcfg.life_state_grandfoe:
		return

	# ghosts cant mine (anymore)
	if user_data.life_state == ewcfg.life_state_corpse:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive)))

	# Enlisted players only mine at certain times.
	if user_data.life_state == ewcfg.life_state_enlisted:
		if user_data.faction == ewcfg.faction_rowdys and (market_data.clock < 8 or market_data.clock > 17):
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "Rowdies only mine in the daytime. Wait for full daylight at 8am.".format(ewcfg.cmd_revive)))

		if user_data.faction == ewcfg.faction_killers and (market_data.clock < 20 and market_data.clock > 5):
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "Killers only mine under cover of darkness. Wait for nightfall at 8pm.".format(ewcfg.cmd_revive)))

	# Mine only in the mines.
	if cmd.message.channel.name in [ewcfg.channel_mines, ewcfg.channel_cv_mines, ewcfg.channel_tt_mines]:
		if user_data.hunger >= ewutils.hunger_max_bylevel(user_data.slimelevel):
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."))
		else:
			# Determine if a poudrin is found.
			poudrin = False
			poudrinamount = 0

			# juvies get poudrins 4 times as often as enlisted players
			poudrin_rarity = ewcfg.poudrin_rarity / (2 if user_data.life_state == ewcfg.life_state_juvenile else 1)
			poudrin_mined = random.randint(1, poudrin_rarity)

			if poudrin_mined == 1:
				poudrin = True
				poudrinamount = 1 if random.randint(1, 3) != 1 else 2  # 33% chance of extra drop

			user_initial_level = user_data.slimelevel

			# Add mined slime to the user.
			slime_bylevel = ewutils.slime_bylevel(user_data.slimelevel)

			mining_yield = math.floor((slime_bylevel / 10) + 1)
			alternate_yield = math.floor(200 + slime_bylevel ** (1 / math.e))

			mining_yield = min(mining_yield, alternate_yield)

			user_data.change_slimes(n = mining_yield, source = ewcfg.source_mining)

			was_levelup = True if user_initial_level < user_data.slimelevel else False

			# Create and give slime poudrins
			for pdx in range(poudrinamount):
				item_id = ewitem.item_create(
					item_type = ewcfg.it_slimepoudrin,
					id_user = cmd.message.author.id,
					id_server = cmd.message.server.id,
				)
				ewutils.logMsg('Created poudrin (item {}) for user (id {})'.format(
					item_id,
					cmd.message.author.id
				))

			# Fatigue the miner.
			hunger_cost_mod = ewutils.hunger_cost_mod(user_data.slimelevel)
			extra = hunger_cost_mod - int(hunger_cost_mod)  # extra is the fractional part of hunger_cost_mod

			user_data.hunger += ewcfg.hunger_permine * int(hunger_cost_mod)
			if extra > 0:  # if hunger_cost_mod is not an integer
				# there's an x% chance that an extra stamina is deducted, where x is the fractional part of hunger_cost_mod in percent (times 100)
				if random.randint(1, 100) <= extra * 100:
					user_data.hunger += ewcfg.hunger_permine

			user_data.persist()

			# Tell the player their slime level increased and/or a poudrin was found.
			if was_levelup or poudrin:
				response = ""

				if poudrin:
					if poudrinamount == 1:
						response += "You unearthed a slime poudrin! "
					elif poudrinamount == 2:
						response += "You unearthed two slime poudrins! "

					ewstats.change_stat(user = user_data, metric = ewcfg.stat_lifetime_poudrins, n = poudrinamount)

					ewutils.logMsg('{} has found {} poudrin(s)!'.format(cmd.message.author.display_name, poudrinamount))

				if was_levelup:
					response += "You have been empowered by slime and are now a level {} slimeboi!".format(user_data.slimelevel)

				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	else:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You can't mine here. Go to the mines."))

"""
	Mining in the wrong channel or while exhausted. This is deprecated anyway but let's sorta keep it around in case we need it.
"""
async def mismine(cmd, user_data, cause):
	time_now = int(time.time())
	global last_mismined_times

	mismined = last_mismined_times.get(cmd.message.author.id)

	if mismined is None:
		mismined = {
			'time': time_now,
			'count': 0
		}

	if time_now - mismined['time'] < 5:
		mismined['count'] += 1
	else:
		# Reset counter.
		mismined['time'] = time_now
		mismined['count'] = 1

	last_mismined_times[cmd.message.author.id] = mismined

	if mismined['count'] >= 11:  # up to 6 messages can be buffered by discord and people have been dying unfairly because of that
		# Lose some slime
		last_mismined_times[cmd.message.author.id] = None
		# user_data.die(cause = ewcfg.cause_mining)

		user_data.change_slimes(n = -(user_data.slimes / 5))
		user_data.persist()

		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You have lost an arm and a leg in a mining accident. Tis but a scratch."))
		# await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
		# sewerchannel = ewutils.get_channel(cmd.message.server, ewcfg.channel_sewers)
		# await ewutils.send_message(cmd.client, sewerchannel, "{} ".format(ewcfg.emote_slimeskull) + ewutils.formatMessage(cmd.message.author, "You have died in a mining accident. {}".format(ewcfg.emote_slimeskull)))
	else:
		if cause == "exhaustion":
			response = "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."
		else:
			response = "You can't mine in this channel. Go elsewhere."

		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
