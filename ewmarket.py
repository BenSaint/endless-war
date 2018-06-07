import time

import ewcmd
import ewutils
import ewcfg
from ew import EwUser, EwMarket

""" player invests slime in the market """
async def invest(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_stockexchange:
		# Only allowed in the stock exchange.
		response = ewcfg.str_exchange_channelreq.format(currency="slime", action="invest")
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
	if ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
		# Disallow investments by RF and CK kingpins.
		response = "You're too powerful to be playing the market."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
		market_data = EwMarket(id_server=cmd.message.author.server.id, conn=conn, cursor=cursor)
	finally:
		cursor.close()
		conn.close()

	if market_data.clock >= 18 or market_data.clock < 6:
		response = ewcfg.str_exchange_closed
	else:
		value = None
		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)

		if value != None:
			if value < 0:
				value = user_data.slimes
			if value <= 0:
				value = None

		if value != None:
			# Apply a brokerage fee of ~5% (rate * 1.05)
			rate_exchange = (market_data.rate_exchange / 1000000.0)
			feerate = 1.05

			# The user can only buy a whole number of credits, so adjust their cost based on the actual number of credits purchased.
			gross_credits = int(value / rate_exchange)
			
			fee = int((gross_credits * feerate) - gross_credits)
			
			net_credits = gross_credits - fee

			if value > user_data.slimes:
				response = "You don't have that much slime to invest."
			elif user_data.time_lastinvest + ewcfg.cd_invest > time_now:
				# Limit frequency of investments.
				response = ewcfg.str_exchange_busy.format(action="invest")
			else:
				user_data.slimes -= value
				user_data.slimecredit += net_credits
				user_data.time_lastinvest = time_now
				market_data.slimes_casino += value
				
				response = "You invest {slime:,} slime and receive {credit:,} SlimeCoin. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(slime=value, credit=net_credits, fee=fee)

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
			response = ewcfg.str_exchange_specify.format(currency="slime", action="invest")

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" player withdraws slime from the market """
async def withdraw(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_stockexchange:
		# Only allowed in the stock exchange.
		response = ewcfg.str_exchange_channelreq.format(currency="SlimeCoin", action="withdraw")
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
		market_data = EwMarket(id_server=cmd.message.author.server.id, conn=conn, cursor=cursor)
	finally:
		cursor.close()
		conn.close()

	if market_data.clock >= 18 or market_data.clock < 6:
		response = ewcfg.str_exchange_closed
	else:
		value = None
		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)

		if value != None:
			if value < 0:
				value = user_data.slimecredit
			if value <= 0:
				value = None

		if value != None:

			rate_exchange = (market_data.rate_exchange / 1000000.0)
								
			credits = value
			slimes = int(value * rate_exchange)

			if value > user_data.slimecredit:
				response = "You don't have that many SlimeCoin to exchange."
			elif user_data.time_lastinvest + ewcfg.cd_invest > time_now:
				# Limit frequency of withdrawals
				response = ewcfg.str_exchange_busy.format(action="withdraw")
			else:
				user_data.slimes += slimes
				user_data.slimecredit -= credits
				user_data.time_lastinvest = time_now
				market_data.slimes_casino -= slimes

				# Flag the user for PvP
				user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (int(time.time()) + ewcfg.time_pvp_invest_withdraw))

				response = "You exchange {credits:,} SlimeCoin for {slimes:,} slime.".format(credits=credits, slimes=slimes)

				# Level up the player if appropriate.
				new_level = len(str(int(user_data.slimes)))
				if new_level > user_data.slimelevel:
					response += "\n\n{} has been empowered by slime and is now a level {} slimeboi!".format(cmd.message.author.display_name, new_level)
					user_data.slimelevel = new_level

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data.persist(conn=conn, cursor=cursor)
					market_data.persist(conn=conn, cursor=cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()

				# Add the visible PvP flag role.
				await ewutils.add_pvp_role(cmd = cmd)

		else:
			response = ewcfg.str_exchange_specify.format(currency="SlimeCoin", action="withdraw")

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" transfer slimecoin between players """
async def xfer(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())

	if cmd.message.channel.name != ewcfg.channel_stockexchange:
		# Only allowed in the stock exchange.
		response = ewcfg.str_exchange_channelreq.format(currency="SlimeCoin", action="transfer")
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	if cmd.mentions_count != 1:
		# Must have exactly one target to send to.
		response = "Mention the player you want to send SlimeCoin to."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return

	member = cmd.mentions[0]
	roles_map_target = ewutils.getRoleMap(member.roles)

	if ewcfg.role_rowdyfucker in roles_map_target or ewcfg.role_copkiller in roles_map_target:
		# Disallow transfers to RF and CK kingpins.
		response = "You can't transfer SlimeCoin to a known criminal warlord."
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
		return


	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		target_data = EwUser(member=member, conn=conn, cursor=cursor)
		user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)
		market_data = EwMarket(id_server=cmd.message.author.server.id, conn=conn, cursor=cursor)
	finally:
		cursor.close()
		conn.close()

	if market_data.clock >= 18 or market_data.clock < 6:
		response = ewcfg.str_exchange_closed
	else:
		# Parse the slime value to send.
		value = None
		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)

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
				response = ewcfg.str_exchange_busy.format(action="transfer")
			else:
				# Do the transfer if the player can afford it.
				target_data.slimecredit += value
				user_data.slimecredit -= cost_total
				user_data.time_lastinvest = time_now

				# Persist changes
				response = "You transfer {slime:,} SlimeCoin to {target_name}. Your slimebroker takes his nominal fee of {fee:,} SlimeCoin.".format(slime=value, target_name=member.display_name, fee=(cost_total - value))

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data.persist(conn=conn, cursor=cursor)
					target_data.persist(conn=conn, cursor=cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()
		else:
			response = ewcfg.str_exchange_specify.format(currency="SlimeCoin", action="transfer")

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" show the current market exchange rate """
async def rate(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""

	market_data = EwMarket(id_server=cmd.message.server.id)

	response = "The current market value of SlimeCoin is {cred:,.3f} slime per 1,000 coin.".format(cred=(market_data.rate_exchange / 1000.0))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" show player's slimecoin balance """
async def slimecoin(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""

	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		market_data = EwMarket(id_server=cmd.message.server.id, conn=conn, cursor=cursor)
		user_slimecredit = EwUser(member=cmd.message.author, conn=conn, cursor=cursor).slimecredit
	finally:
		cursor.close()
		conn.close()

	net_worth = int(user_slimecredit * (market_data.rate_exchange / 1000000.0))
	response = "You have {:,} SlimeCoin, currently valued at {:,} slime.".format(user_slimecredit, net_worth)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
