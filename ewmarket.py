import time

import ewcmd
import ewitem
import ewrolemgr
import ewutils
import ewcfg
import ewstats
from ew import EwUser, EwMarket

""" donate slime to slimecorp in exchange for slimecoin """
async def donate(cmd):
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_slimecorphq:
		# Only allowed in SlimeCorp HQ.
		response = "You must go to SlimeCorp HQ to donate slime."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return

	user_data = EwUser(member = cmd.message.author)

	value = None
	if cmd.tokens_count > 1:
		value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)

	if value != None:
		if value < 0:
			value = user_data.slimes
		if value <= 0:
			value = None

	if value != None and value < ewcfg.slimecoin_exchangerate:
		response = "You must volunteer to donate at least %d slime to receive compensation." % ewcfg.slimecoin_exchangerate

	elif value != None:
		# Amount of slime invested.
		cost_total = int(value)
		coin_total = int(value / ewcfg.slimecoin_exchangerate)

		if user_data.slimes < cost_total:
			response = "Acid-green flashes of light and bloodcurdling screams emanate from small window of SlimeCorp HQ. Unfortunately, you did not survive the procedure. Your body is dumped down a disposal chute to the sewers."
			user_data.die(cause = ewcfg.cause_donation)
			user_data.persist()
			# Assign the corpse role to the player. He dead.
			await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
			sewerchannel = ewutils.get_channel(cmd.message.server, ewcfg.channel_sewers)
			await ewutils.send_message(cmd.client, sewerchannel, "{} ".format(ewcfg.emote_slimeskull) + ewutils.formatMessage(cmd.message.author, "You have died in a medical mishap. {}".format(ewcfg.emote_slimeskull)))
		else:
			# Do the transfer if the player can afford it.
			user_data.change_slimes(n = -cost_total, source = ewcfg.source_spending)
			user_data.change_slimecredit(n = coin_total, coinsource = ewcfg.coinsource_donation)
			user_data.time_lastinvest = time_now

			# Persist changes
			user_data.persist()

			response = "You stumble out of a Slimecorp HQ vault room in a stupor. You don't remember what happened in there, but your body hurts and you've got {slimecoin:,} shiny new SlimeCoin in your pocket.".format(slimecoin = coin_total)

	else:
		response = ewcfg.str_exchange_specify.format(currency = "slime", action = "donate")

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" transfer slimecoin between players """
async def xfer(cmd):
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_stockexchange:
		# Only allowed in the stock exchange.
		response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "transfer")
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return

	if cmd.mentions_count != 1:
		# Must have exactly one target to send to.
		response = "Mention the player you want to send SlimeCoin to."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return

	member = cmd.mentions[0]
	target_data = EwUser(member = member)

	if target_data.life_state == ewcfg.life_state_kingpin:
		# Disallow transfers to RF and CK kingpins.
		response = "You can't transfer SlimeCoin to a known criminal warlord."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		return

	user_data = EwUser(member = cmd.message.author)
	market_data = EwMarket(id_server = cmd.message.author.server.id)

	if cmd.message.author.id == member.id:
		user_data.id_killer = cmd.message.author.id
		user_data.die(cause = ewcfg.cause_suicide)
		user_data.persist()

		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "Gaming the slimeconomy is punishable by death. SlimeCorp soldiers execute you immediately."))
		await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)
		return

	# Parse the slime value to send.
	value = None
	if cmd.tokens_count > 1:
		value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)

	if value != None:
		if value < 0:
			value = user_data.slimes
		if value <= 0:
			value = None

	if value != None:
		# Cost including the 5% transfer fee.
		cost_total = int(value * 1.05)

		if user_data.slimecredit < cost_total:
			response = "You don't have enough SlimeCoin. ({:,}/{:,})".format(user_data.slimecredit, cost_total)
		else:
			# Do the transfer if the player can afford it.
			target_data.change_slimecredit(n = value, coinsource = ewcfg.coinsource_transfer)
			user_data.change_slimecredit(n = -cost_total, coinsource = ewcfg.coinsource_transfer)
			user_data.time_lastinvest = time_now

			# Persist changes
			response = "You transfer {slime:,} SlimeCoin to {target_name}. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(slime = value, target_name = member.display_name, fee = (cost_total - value))

			target_data.persist()
			user_data.persist()
	else:
		response = ewcfg.str_exchange_specify.format(currency = "SlimeCoin", action = "transfer")

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" show player's slimecoin balance """
async def slimecoin(cmd):
	response = ""
	user_data = None

	if cmd.mentions_count == 0:
		coins = EwUser(member = cmd.message.author).slimecredit
		response = "You have {:,} SlimeCoin.".format(coins)
	else:
		member = cmd.mentions[0]
		coins = EwUser(member = member).slimecredit
		response = "{} has {:,} SlimeCoin.".format(member.display_name, coins)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
