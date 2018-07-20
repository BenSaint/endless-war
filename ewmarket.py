import time

import ewcmd
import ewutils
import ewcfg
from ew import EwUser, EwMarket

""" transfer slimecoin between players """
async def xfer(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_stockexchange:
		# Only allowed in the stock exchange.
		response = ewcfg.str_exchange_channelreq.format(currency = "SlimeCoin", action = "transfer")
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	if cmd.mentions_count != 1:
		# Must have exactly one target to send to.
		response = "Mention the player you want to send SlimeCoin to."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	member = cmd.mentions[0]
	target_data = EwUser(member = member)

	if target_data.life_state == ewcfg.life_state_kingpin:
		# Disallow transfers to RF and CK kingpins.
		response = "You can't transfer SlimeCoin to a known criminal warlord."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	user_data = EwUser(member = cmd.message.author)
	market_data = EwMarket(id_server = cmd.message.author.server.id)

	if market_data.clock > 19 or market_data.clock < 6:
		response = ewcfg.str_exchange_closed
	else:
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
			elif user_data.time_lastinvest + ewcfg.cd_invest > time_now:
				# Limit frequency of investments.
				response = ewcfg.str_exchange_busy.format(action = "transfer")
			else:
				# Do the transfer if the player can afford it.
				target_data.slimecredit += value
				user_data.slimecredit -= cost_total
				user_data.time_lastinvest = time_now

				# Persist changes
				response = "You transfer {slime:,} SlimeCoin to {target_name}. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(slime = value, target_name = member.display_name, fee = (cost_total - value))

				user_data.persist()
				target_data.persist()
		else:
			response = ewcfg.str_exchange_specify.format(currency = "SlimeCoin", action = "transfer")

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


""" show player's slimecoin balance """
async def slimecoin(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""

	market_data = EwMarket(id_server = cmd.message.server.id)
	user_slimecredit = EwUser(member = cmd.message.author).slimecredit

	net_worth = int(user_slimecredit * (market_data.rate_exchange / 1000000.0))
	response = "You have {:,} SlimeCoin, currently valued at {:,} slime.".format(user_slimecredit, net_worth)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
