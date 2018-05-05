#!/usr/bin/python3
#
# endless-war
# mperron (2018)
#
# a chat bot for the RFCK discord server

import discord
import asyncio
import random
import sys
import time
import json
import subprocess
import traceback

import ewutils
import ewcfg
from ew import EwUser, EwMarket

ewutils.logMsg('Starting up...')

client = discord.Client()

# A map containing user IDs and the last time in UTC seconds since we sent them
# the help doc via DM. This is to prevent spamming.
last_helped_times = {}

# Map containing user IDs and the last time in UTC seconds since the slot
# machine was used.
last_slotsed_times = {}

# Map containing user IDs and the last time in UTC seconds since the player
# threw their dice.
last_crapsed_times = {}

# Map containing user IDs and the last time in UTC seconds since the pachinko
# machine was used.
last_pachinkoed_times = {}

# Map of user ID to a map of recent miss-mining time to count. If the count
# exceeds 3 in 5 seconds, you die.
last_mismined_times = {}

# Map of server ID to a map of active users on that server.
active_users_map = {}

debug = False
while sys.argv:
	if sys.argv[0].lower() == '--debug':
		debug = True

	sys.argv = sys.argv[1:]

# When debug is enabled, additional commands are turned on.
if debug == True:
	ewutils.logMsg('Debug mode enabled.')

@client.event
async def on_ready():
	ewutils.logMsg('Logged in as {} ({}).'.format(client.user.name, client.user.id))
	ewutils.logMsg('Ready.')

	await client.change_presence(game=discord.Game(name=("dev. by @krak " + ewcfg.version)))

	# Look for a Twitch client_id on disk.
	twitch_client_id = ewutils.getTwitchClientId()

	# If no twitch client ID is available, twitch integration will be disabled.
	if twitch_client_id == None or len(twitch_client_id) == 0:
		ewutils.logMsg('No twitch_client_id file found. Twitch integration disabled.')
	else:
		ewutils.logMsg("Enabled Twitch integration.")

		# Channels in the connected discord servers to announce to.
		channels_announcement = []

		# Channels in the connected discord servers to send stock market updates to. Map of server ID to channel.
		channels_stockmarket = {}

		for server in client.servers:
			ewutils.logMsg("connected to: {}".format(server.name))
			for channel in server.channels:
				if(channel.type == discord.ChannelType.text):
					if(channel.name == ewcfg.channel_twitch_announcement):
						channels_announcement.append(channel)
						ewutils.logMsg("• found for announcements: {}".format(channel.name))

					elif(channel.name == ewcfg.channel_stockexchange):
						channels_stockmarket[server.id] = channel
						ewutils.logMsg("• found for stock exchange: {}".format(channel.name))

		time_now = int(time.time())
		time_last_twitch = time_now
		time_last_pvp = time_now
		time_last_market = time_now

		# Every three hours we log a message saying the periodic task hook is still active. On startup, we want this to happen within about 60 seconds, and then on the normal 3 hour interval.
		time_last_logged = time_now - ewcfg.update_hookstillactive + 60

		stream_live = None
		while True:
			time_now = int(time.time())

			# Periodic message to log that this stuff is still running.
			if (time_now - time_last_logged) >= ewcfg.update_hookstillactive:
				time_last_logged = time_now

				ewutils.logMsg("Periodic hook still active.")

			# Check to see if a stream is live via the Twitch API.
			if (time_now - time_last_twitch) >= ewcfg.update_twitch:
				time_last_twitch = time_now

				try:
					# Twitch API call to see if there are any active streams.
					json_string = ""
					p = subprocess.Popen("curl -H 'Client-ID: {}' -X GET 'https://api.twitch.tv/helix/streams?user_login=rowdyfrickerscopkillers' 2>/dev/null".format(twitch_client_id), shell=True, stdout=subprocess.PIPE)
					for line in p.stdout.readlines():
						json_string += line.decode('utf-8')
					json_parsed = json.loads(json_string)

					# When a stream is up, data is an array of stream information objects.
					data = json_parsed.get('data')
					if data != None:
						data_count = len(data)
						stream_was_live = stream_live
						stream_live = True if data_count > 0 else False

						if stream_was_live == False and stream_live == True:
							ewutils.logMsg("The stream is now live.")

							# The stream has transitioned from offline to online. Make an announcement!
							for channel in channels_announcement:
								await client.send_message(
									channel,
									"ATTENTION CITIZENS. THE **ROWDY FUCKER** AND THE **COP KILLER** ARE **STREAMING**. BEWARE OF INCREASED KILLER AND ROWDY ACTIVITY.\n\n@everyone\n{}".format(
										"https://www.twitch.tv/rowdyfrickerscopkillers"
									)
								)
				except:
					ewutils.logMsg('Twitch handler hit an exception (continuing):')
					traceback.print_exc(file=sys.stdout)

			# Clear PvP roles from players who are no longer flagged.
			if (time_now - time_last_pvp) >= ewcfg.update_pvp:
				time_last_pvp = time_now

				try:
					for server in client.servers:
						roles_map = ewutils.getRoleMap(server.roles)

						role_juvenile_pvp = roles_map[ewcfg.role_juvenile_pvp]
						role_rowdyfuckers_pvp = roles_map[ewcfg.role_rowdyfuckers_pvp]
						role_copkillers_pvp = roles_map[ewcfg.role_copkillers_pvp]

						# Monitor all user roles and update if a user is no longer flagged for PvP.
						for member in server.members:
							pvp_role = None

							if role_juvenile_pvp in member.roles:
								pvp_role = role_juvenile_pvp
							elif role_copkillers_pvp in member.roles:
								pvp_role = role_copkillers_pvp
							elif role_rowdyfuckers_pvp in member.roles:
								pvp_role = role_rowdyfuckers_pvp

							if pvp_role != None:
								# Retrieve user data from the database.
								user_data = EwUser(member=member)

								# If the user's PvP expire time is historical, remove the PvP role.
								if user_data.time_expirpvp < int(time.time()):
									await client.remove_roles(member, pvp_role)

				except:
					ewutils.logMsg('An error occurred in the scheduled role update task:')
					traceback.print_exc(file=sys.stdout)

			# Adjust the exchange rate of slime for the market.
			try:
				for server in client.servers:
					# Load market data from the database.
					market_data = EwMarket(id_server=server.id)

					if market_data.time_lasttick + ewcfg.update_market < time_now:
						market_data.time_lasttick = time_now

						# Nudge the value back to stability.
						rate_market = market_data.rate_market
						if rate_market >= 1030:
							rate_market -= 10
						elif rate_market <= 970:
							rate_market += 10

						# Add participation bonus.
						active_bonus = 0
						active_map = active_users_map.get(server.id)
						if active_map != None:
							active_bonus = len(active_map)

							if active_bonus > 20:
								active_bonus = 20

						active_users_map[server.id] = {}
						rate_market += active_bonus - 2

						# Tick down the boombust cooldown.
						if market_data.boombust < 0:
							market_data.boombust += 1
						elif market_data.boombust > 0:
							market_data.boombust -= 1

						# Adjust the market rate.
						fluctuation = 0 #(random.randrange(5) - 2) * 100
						noise = (random.randrange(19) - 9) * 2
						subnoise = (random.randrange(13) - 6)

						# Some extra excitement!
						if noise == 0 and subnoise == 0:
							boombust = (random.randrange(3) - 1) * 200

							# If a boombust occurs shortly after a previous boombust, make sure it's the opposite effect. (Boom follows bust, bust follows boom.)
							if (market_data.boombust > 0 and boombust > 0) or (market_data.boombust < 0 and boombust < 0):
								boombust *= -1

							if boombust != 0:
								market_data.boombust = ewcfg.cd_boombust

								if boombust < 0:
									market_data.boombust *= -1
						else:
							boombust = 0

						rate_market += fluctuation + noise + subnoise + boombust
						if rate_market < 300:
							rate_market = (300 + noise + subnoise)

						percentage = ((rate_market / 10) - 100)
						percentage_abs = percentage * -1

						# If the value hits 0, we're stuck there forever.
						if market_data.rate_exchange <= 100:
							market_data.rate_exchange = 100

						# Apply the market change to the casino balance and exchange rate.
						market_data.slimes_casino = int(market_data.slimes_casino * (rate_market / 1000.0))
						market_data.rate_exchange = int(market_data.rate_exchange * (rate_market / 1000.0))

						try:
							conn = ewutils.databaseConnect()
							cursor = conn.cursor()

							# Persist new data.
							market_data.rate_market = rate_market
							market_data.persist(conn=conn, cursor=cursor)

							# Create a historical snapshot.
							ewutils.persistMarketHistory(market_data=market_data, conn=conn, cursor=cursor)

							conn.commit()
						finally:
							cursor.close()
							conn.close()

						# Give some indication of how the market is doing to the users.
						response = "..."

						# Market is up ...
						if rate_market > 1200:
							response = 'The slimeconomy is skyrocketing!!! Slime stock is up {p:.3g}%!!!'.format(p=percentage)
						elif rate_market > 1100:
							response = 'The slimeconomy is booming! Slime stock is up {p:.3g}%!'.format(p=percentage)
						elif rate_market > 1000:
							response = 'The slimeconomy is doing well. Slime stock is up {p:.3g}%.'.format(p=percentage)
						# Market is down ...
						elif rate_market < 800:
							response = 'The slimeconomy is plummetting!!! Slime stock is down {p:.3g}%!!!'.format(p=percentage_abs)
						elif rate_market < 900:
							response = 'The slimeconomy is stagnating! Slime stock is down {p:.3g}%!'.format(p=percentage_abs)
						elif rate_market < 1000:
							response = 'The slimeconomy is a bit sluggish. Slime stock is down {p:.3g}%.'.format(p=percentage_abs)
						# Perfectly balanced
						else:
							response = 'The slimeconomy is holding steady. No change in slime stock value.'

						# Send the announcement.
						channel = channels_stockmarket.get(server.id)
						if channel != None:
							await client.send_message(channel, ('**' + response + '**'))
						else:
							ewutils.logMsg('No stock market channel for server {}'.format(server.name))
			except:
				ewutils.logMsg('An error occurred in the scheduled slime market update task:')
				traceback.print_exc(file=sys.stdout)

			# Wait a while before running periodic tasks.
			await asyncio.sleep(15)

@client.event
async def on_member_join(member):
	roles_map = ewutils.getRoleMap(member.server.roles)
	role_juvenile = roles_map[ewcfg.role_juvenile]

	ewutils.logMsg("New member \"{}\" joined. Assigned Juveniles role.".format(member.display_name))

	await client.replace_roles(member, role_juvenile)

@client.event
async def on_message(message):
	""" do not interact with our own messages """
	if message.author.id == client.user.id or message.author.bot == True:
		return

	# Note that the user posted a message.
	if message.server != None:
		active_map = active_users_map.get(message.server.id)
		if active_map == None:
			active_map = {}
			active_users_map[message.server.id] = active_map
		active_map[message.author.id] = True

	"""
		Wake up if we need to respond to messages. Could be:
			message starts with !
			direct message (server == None)
			user is new/has no roles (len(roles) < 2)
	"""
	if message.content.startswith(ewcfg.cmd_prefix) or message.server == None or len(message.author.roles) < 2:
		# tokenize the message. the command should be the first word.
		tokens = message.content.split(' ')
		tokens_count = len(tokens)
		cmd = tokens[0].lower()

		""" reply to DMs with help document """
		if message.server == None:
			time_now = int(time.time())
			time_last = last_helped_times.get(message.author.id, 0)

			# Only send the help doc once every thirty seconds. There's no need to spam it.
			if (time_now - time_last) > 30:
				last_helped_times[message.author.id] = time_now
				await client.send_message(message.channel, ewutils.getHelpText())

			# Nothing else to do in a DM.
			return

		# remove mentions to us
		mentions = list(filter(lambda user : user.id != client.user.id, message.mentions))

		# common data we'll need
		roles_map = ewutils.getRoleMap(message.server.roles)
		mentions_count = len(mentions)

		# assign the juveniles role to a user with only 1 or 0 roles.
		if len(message.author.roles) < 2:
			role_juvenile = roles_map[ewcfg.role_juvenile]
			await client.replace_roles(message.author, role_juvenile)
			return

		# let the user know we're working on it
		resp = None
		if cmd != ewcfg.cmd_mine or message.channel.name != ewcfg.channel_mines:
			resp = await client.send_message(message.channel, '...')


		# Scold/ignore offline players.
		if message.author.status == discord.Status.offline:
			response = "You cannot participate in the ENDLESS WAR while offline."

			if resp != None:
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			else:
				await client.send_message(message.channel, ewutils.formatMessage(message.author, response))

			return

		# process command words
		if cmd == ewcfg.cmd_kill:
			response = ""

			if message.channel.name != ewcfg.channel_combatzone:
				response = "You must go to the #{} to commit gang violence.".format(ewcfg.channel_combatzone)

			# Only allow one kill at a time.
			elif mentions_count > 1:
				response = "One kill at a time!"

			elif mentions_count == 1:
				# The roles assigned to the author of this message.
				roles_map_user = ewutils.getRoleMap(message.author.roles)
				time_now = int(time.time())

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					# Get killing player's info.
					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

					# Flag the killer for PvP no matter what happens next.
					user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))
					user_data.persist(conn=conn, cursor=cursor)

					# Get target's info.
					member = mentions[0]
					killed_data = EwUser(member=member, conn=conn, cursor=cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()

				# Killed player's assigned Discord roles.
				roles_map_target = ewutils.getRoleMap(member.roles)

				# new (more fair?) slime calculation. more slimes makes you harder to kill.
				slimes_tokill = ewcfg.slimes_tokill + int(user_data.slimes/10) + int(killed_data.slimes/2)

				user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
				user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

				# Add the PvP flag role.
				if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
				elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
				elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])

				if ewcfg.role_copkiller in roles_map_target or ewcfg.role_rowdyfucker in roles_map_target:
					# disallow killing generals
					response = 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter a general.'

				elif (time_now - user_data.time_lastkill) < ewcfg.cd_kill:
					# disallow kill if the player has killed recently
					response = "Take a moment to appreciate your last slaughter."

				elif killed_data.id_killer == user_data.id_user:
					# disallow kill if the player is the id_killer of killed_data
					response = "You have already proven your superiority over {}.".format(member.display_name)

				elif time_now > killed_data.time_expirpvp:
					# target is not flagged for PvP
					response = "{} is not mired in the ENDLESS WAR right now.".format(member.display_name)

				elif user_data.slimes < slimes_tokill:
					# Not enough slime.
					response = "You are currently too weak-willed and feminine. Harvest more Juveniles for their slime."

				elif user_iskillers == False and user_isrowdys == False:
					# Only killers, rowdys, the cop killer, and the rowdy fucker can kill people
					if ewcfg.role_juvenile in roles_map_user:
						response = "Juveniles lack the moral fiber necessary for murder."
					else:
						response = "You lack the moral fiber necessary for murder."

				elif ewcfg.role_corpse in roles_map_target:
					# Target is already dead.
					response = '{} is already dead.'.format(member.display_name)

				elif (time_now - killed_data.time_lastrevive) < ewcfg.invuln_onrevive:
					# User is currently invulnerable
					response = '{} has died too recently and is immune.'.format(member.display_name)

				else:
					# slimes from this kill might be awarded to the boss
					role_boss = (ewcfg.role_copkiller if user_iskillers == True else ewcfg.role_rowdyfucker)
					boss_slimes = 0

					role_corpse = roles_map[ewcfg.role_corpse]

					was_juvenile = False
					was_killed = False

					if (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)) or (ewcfg.role_juvenile in roles_map_target):
						# User can be killed.
						if ewcfg.role_juvenile in roles_map_target:
							was_juvenile = True

						was_killed = True
						await client.replace_roles(member, role_corpse)

					if was_killed == True:
						try:
							conn = ewutils.databaseConnect()
							cursor = conn.cursor()

							user_data.slimes -= slimes_tokill

							if killed_data.slimes > 0:
								if was_juvenile == True:
									# Add juvenile targets' slimes to this player.
									user_data.slimes += killed_data.slimes
								else:
									# Add adult tarets' slimes to the boss.
									boss_slimes += killed_data.slimes

							# Remove !revive invulnerability.
							user_data.time_lastrevive = 0

							# Set the last kill time for kill cooldown.
							user_data.time_lastkill = time_now

							# Persist the player's data.
							user_data.persist(conn=conn, cursor=cursor)

							# Remove all slimes from the dead player.
							killed_data.slimes = 0
							killed_data.id_killer = message.author.id
							killed_data.persist(conn=conn, cursor=cursor)

							conn.commit()
						finally:
							cursor.close()
							conn.close()

						# give slimes to the boss if possible.
						boss_member = None
						if boss_slimes > 0:
							for member_search in message.author.server.members:
								if role_boss in ewutils.getRoleMap(member_search.roles):
									boss_member = member_search
									break

							if boss_member != None:
								try:
									conn = ewutils.databaseConnect()
									cursor = conn.cursor()

									boss_data = EwUser(member=boss_member, conn=conn, cursor=cursor)
									boss_data.slimes += boss_slimes
									boss_data.persist(conn=conn, cursor=cursor)

									conn.commit()
								finally:
									cursor.close()
									conn.close()

						# player was killed
						response = '{} has been SLAUGHTERED. {} :gun:'.format(member.display_name, ewcfg.emote_slime5)

					else:
						# teammate, or otherwise unkillable
						response = 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter {}.'.format(member.display_name)

			else:
				response = 'Your bloodlust is appreciated, but ENDLESS WAR didn\'t understand that name.'

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Kill yourself to return slime to your general.
		elif cmd == ewcfg.cmd_suicide:
			response = ""

			# Only allowed in the combat zone.
			if message.channel.name != ewcfg.channel_combatzone:
				response = "You must go to the #{} to commit suicide.".format(ewcfg.channel_combatzone)
			else:
				# Get the user data.
				user_data = EwUser(member=message.author)

				# The roles assigned to the author of this message.
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				# Slime transfer
				boss_slimes = user_data.slimes - (ewcfg.slimes_tokill + int(user_data.slimes * 3 / 5))

				user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
				user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user
				user_isgeneral = ewcfg.role_copkiller in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user
				user_isjuvenile = ewcfg.role_juvenile in roles_map_user
				user_isdead = ewcfg.role_corpse in roles_map_user

				if user_isdead:
					response = "Too late for that."
				elif user_isjuvenile:
					response = "Juveniles are too cowardly for suicide."
				elif user_isgeneral:
					response = "\*click* Alas, your gun has jammed."
				elif user_iskillers or user_isrowdys:
					role_corpse = roles_map[ewcfg.role_corpse]

					# Assign the corpse role to the player. He dead.
					await client.replace_roles(message.author, role_corpse)

					# Set the id_killer to the player himself, remove his slime.
					user_data.id_killer = message.author.id
					user_data.slimes = 0
					user_data.persist()

					# Give slimes to the boss if possible.
					boss_member = None
					if boss_slimes > 0:
						role_boss = (ewcfg.role_copkiller if user_iskillers == True else ewcfg.role_rowdyfucker)

						for member_search in message.author.server.members:
							boss_roles = ewutils.getRoleMap(member_search.roles)
							if role_boss in boss_roles and ewcfg.role_kingpin in boss_roles:
								boss_member = member_search
								break

						if boss_member != None:
							try:
								conn = ewutils.databaseConnect()
								cursor = conn.cursor()

								boss_data = EwUser(member=boss_member, conn=conn, cursor=cursor)
								boss_data.slimes += boss_slimes
								boss_data.persist(conn=conn, cursor=cursor)

								conn.commit()
							finally:
								cursor.close()
								conn.close()

					response = '{} has willingly returned to the slime. {}'.format(message.author.display_name, ewcfg.emote_slimeskull)
				else:
					# This should never happen. We handled all the role cases. Just in case.
					response = "\*click* Alas, your gun has jammed."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Spar with an ally
		elif cmd == ewcfg.cmd_spar:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to spar.".format(ewcfg.channel_dojo)

			# Only allow one kill at a time.
			elif mentions_count > 1:
				response = "One sparring partner at a time!"

			elif mentions_count == 1:
				member = mentions[0]

				if(member.id == message.author.id):
					response = "How do you expect to spar with yourself?"
				else:

					# The roles assigned to the author of this message.
					roles_map_user = ewutils.getRoleMap(message.author.roles)

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						# Get killing player's info.
						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						# Get target's info.
						sparred_data = EwUser(member=member, conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
					user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

					# Only killers, rowdys, the cop killer, and the rowdy fucker can spar
					if user_iskillers == False and user_isrowdys == False:
						response = "Juveniles lack the backbone necessary for combat."
					else:
						was_juvenile = False
						was_sparred = False
						was_dead = False
						was_player_tired = False
						was_target_tired = False

						time_now = int(time.time())

						roles_map_target = ewutils.getRoleMap(member.roles)

						if ewcfg.role_corpse in roles_map_target:
							# Target is already dead.
							was_dead = True
						elif (user_data.time_lastspar + ewcfg.cd_spar) > time_now:
							# player sparred too recently
							was_player_tired = True
						elif (sparred_data.time_lastspar + ewcfg.cd_spar) > time_now:
							# taret sparred too recently
							was_target_tired = True
						elif ewcfg.role_juvenile in roles_map_target:
							# Target is a juvenile.
							was_juvenile = True

						elif (user_iskillers and (ewcfg.role_copkillers in roles_map_target)) or (user_isrowdys and (ewcfg.role_rowdyfuckers in roles_map_target)):
							# User can be sparred.
							was_sparred = True


						#if the duel is successful
						if was_sparred:
							weaker_player = sparred_data if sparred_data.slimes < user_data.slimes else user_data
							stronger_player = sparred_data if user_data is weaker_player else user_data

							# Flag the player for PvP
							user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))

							# Weaker player gains slime based on the slime of the stronger player.
							weaker_player.slimes += ewcfg.slimes_perspar if (stronger_player.slimes / 2) > ewcfg.slimes_perspar else (stronger_player.slimes / 2)
							weaker_player.time_lastspar = time_now
							weaker_player.persist()

							# Persist the user if he was the stronger player.
							if user_data is not weaker_player:
								user_data.persist()

							# Add the PvP flag role.
							if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
							elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
							elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])

							# player was sparred with
							response = '{} parries the attack. :knife: {}'.format(member.display_name, ewcfg.emote_slime5)
						else:
							if was_dead:
								# target is already dead
								response = '{} is already dead.'.format(member.display_name)
							elif was_target_tired:
								# target has sparred too recently
								response = '{} is too tired to spar right now.'.format(member.display_name)
							elif was_player_tired:
								# player has sparred too recently
								response = 'You are too tired to spar right now.'
							else:
								#otherwise unkillable
								response = '{} cannot spar now.'.format(member.display_name)
			else:
				response = 'Your fighting spirit is appreciated, but ENDLESS WAR didn\'t understand that name.'

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# revive yourself as a juvenile after having been killed.
		elif cmd == ewcfg.cmd_revive:
			response = ""

			if message.channel.name != ewcfg.channel_endlesswar and message.channel.name != ewcfg.channel_sewers:
				response = "Come to me. I hunger. #{}.".format(ewcfg.channel_sewers)
			else:
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				if ewcfg.role_corpse in roles_map_user:
					time_now = int(time.time())
					player_is_pvp = False

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						player_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						# Give player some initial slimes.
						player_data.slimes = ewcfg.slimes_onrevive

						# Clear fatigue.
						player_data.stamina = 0

						# Clear PvP flag.
						player_data.time_expirpvp = time_now - 1;

						# Set time of last revive. This used to provied spawn protection, but currently isn't used.
						player_data.time_lastrevive = time_now

						if(player_data.time_expirpvp > time_now):
							player_is_pvp = True

						player_data.persist(conn=conn, cursor=cursor)

						# Give some slimes to every living player (currently online)
						for member in message.server.members:
							if member.id != message.author.id and member.id != client.user.id:
								if ewcfg.role_corpse not in ewutils.getRoleMap(member.roles):
									member_data = EwUser(member=member, conn=conn, cursor=cursor)
									member_data.slimes += ewcfg.slimes_onrevive_everyone
									member_data.persist(conn=conn, cursor=cursor)

						# Commit all transactions at once.
						conn.commit()
					finally:
						cursor.close()
						conn.close()

					if player_is_pvp:
						await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile], roles_map[ewcfg.role_juvenile_pvp])
					else:
						await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile])

					response = '{slime4} A geyser of fresh slime erupts, showering Rowdy, Killer, and Juvenile alike. {slime4} {name} has been reborn in slime. {slime4}'.format(slime4=ewcfg.emote_slime4, name=message.author.display_name)
				else:
					response = 'You\'re not dead just yet.'

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# move from juvenile to one of the armies (rowdys or killers)
		elif cmd == ewcfg.cmd_enlist:
			response = ""
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_juvenile in roles_map_user:
				faction = ""
				if tokens_count > 1:
					faction = tokens[1].lower()

				user_data = EwUser(member=message.author)
				user_slimes = user_data.slimes
				user_is_pvp = (user_data.time_expirpvp > int(time.time()))

				if user_slimes < ewcfg.slimes_toenlist:
					response = "You need to mine more slime to rise above your lowly station. ({}/{})".format(user_slimes, ewcfg.slimes_toenlist)
				else:
					if faction == ewcfg.faction_rowdys:
						if user_is_pvp:
							await client.replace_roles(message.author, roles_map[ewcfg.role_rowdyfuckers], roles_map[ewcfg.role_rowdyfuckers_pvp])
						else:
							await client.replace_roles(message.author, roles_map[ewcfg.role_rowdyfuckers])

						response = "Enlisted in the {}.".format(ewcfg.faction_rowdys)
					elif faction == ewcfg.faction_killers:
						if user_is_pvp:
							await client.replace_roles(message.author, roles_map[ewcfg.role_copkillers], roles_map[ewcfg.role_copkillers_pvp])
						else:
							await client.replace_roles(message.author, roles_map[ewcfg.role_copkillers])

						response = "Enlisted in the {}.".format(ewcfg.faction_killers)
					else:
						response = "Which faction? Say '{} {}' or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys)

			elif ewcfg.role_corpse in roles_map_user:
				response = 'You are dead, bitch.'
			else:
				response = "You can't do that right now, bitch."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# faction leader consumes the mentioned players of their own faction to absorb their slime count
		# kills the mentioned players
		elif cmd == ewcfg.cmd_devour:
			response = ""
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			is_copkiller = ewcfg.role_copkiller in roles_map_user
			is_rowdyfucker = ewcfg.role_rowdyfucker in roles_map_user

			if is_copkiller == False and is_rowdyfucker == False:
				response = "Know your place."
			else:
				if mentions_count == 0:
					response = "Devour who?"
				else:
					members_devoured = []
					members_na = []

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						# determine slime count for every member mentioned
						for member in mentions:
							roles_map_member = ewutils.getRoleMap(member.roles)

							if is_copkiller == True and ewcfg.role_copkillers in roles_map_member or is_rowdyfucker == True and ewcfg.role_rowdyfuckers in roles_map_member:

								# get slimes from the player
								member_data = EwUser(member=member, conn=conn, cursor=cursor)
								user_data.slimes += member_data.slimes

								# set player slimes to 0
								member_data.slimes = 0
								member_data.persist(conn=conn, cursor=cursor)

								members_devoured.append(member)
							else:
								members_na.append(member)

						# add slime to rf/ck
						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					role_corpse = roles_map[ewcfg.role_corpse]
					for member in members_devoured:
						# update slime counts
						try:
							# set roles to corpse for mentioned players
							await client.replace_roles(member, role_corpse)
						except:
							pass

					if len(members_devoured) > 0:
						names = ewutils.userListToNameString(members_devoured)
						if len(members_na) > 0:
							response = '{} has been devoured. ({} was not devoured.)'.format(names, ewutils.userListToNameString(members_na))
						else:
							response = '{} has been devoured.'.format(names)
					elif len(members_na) > 0:
						response = '{} was not devoured.'.format(ewutils.userListToNameString(members_na))
					else:
						response = 'No one was devoured.'

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# gives slime to the miner (message.author)
		elif cmd == ewcfg.cmd_mine:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_corpse in roles_map_user:
				await client.send_message(message.channel, ewutils.formatMessage(message.author, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive)))
			else:
				if(message.channel.name == ewcfg.channel_mines):
					user_data = EwUser(member=message.author)

					if user_data.stamina >= 250:
						mismined = last_mismined_times.get(message.author.id)
						time_now = int(time.time())

						if mismined == None:
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

						last_mismined_times[message.author.id] = mismined

						if mismined['count'] >= 3:
							# Death
							last_mismined_times[message.author.id] = None
							user_data.slimes = 0
							user_data.persist()

							await client.send_message(message.channel, ewutils.formatMessage(message.author, "You have died in a mining accident."))
							await client.replace_roles(message.author, roles_map[ewcfg.role_corpse])
						else:
							await client.send_message(message.channel, ewutils.formatMessage(message.author, "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."))
					else:
						# Add mined slime to the user.
						user_data.slimes += ewcfg.slimes_permine

						# Fatigue the miner.
						user_data.stamina += 1
						if random.randrange(10) > 6:
							user_data.stamina += 1

						# Flag the user for PvP
						user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (int(time.time()) + ewcfg.time_pvp_mine))
						user_data.persist()

						# Add the PvP flag role.
						if ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])
						elif ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
						elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
				else:
					mismined = last_mismined_times.get(message.author.id)
					time_now = int(time.time())

					if mismined == None:
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

					last_mismined_times[message.author.id] = mismined

					if mismined['count'] >= 3:
						# Death
						last_mismined_times[message.author.id] = None

						try:
							conn = ewutils.databaseConnect()
							cursor = conn.cursor()

							user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
							user_data.slimes = 0
							user_data.persist(conn=conn, cursor=cursor)

							conn.commit()
						finally:
							cursor.close()
							conn.close()


						await client.edit_message(resp, ewutils.formatMessage(message.author, "You have died in a mining accident."))
						await client.replace_roles(message.author, roles_map[ewcfg.role_corpse])
					else:
						await client.edit_message(resp, ewutils.formatMessage(message.author, "You can't mine here. Try #{}.".format(ewcfg.channel_mines)))


		# Show the current slime score of a player.
		elif cmd == ewcfg.cmd_score or cmd == ewcfg.cmd_score_alt1:
			response = ""

			if mentions_count == 0:
				user_slimes = EwUser(member=message.author).slimes

				# return my score
				response = "Your slime score is {:,} {}".format(user_slimes, ewcfg.emote_slime1)
			else:
				member = mentions[0]
				user_slimes = EwUser(member=member).slimes

				# return somebody's score
				response = "{}'s slime score is {:,} {}".format(member.display_name, user_slimes, ewcfg.emote_slime1)

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# rowdy fucker and cop killer (leaders) can give slimes to anybody
		elif cmd == ewcfg.cmd_giveslime or cmd == ewcfg.cmd_giveslime_alt1:
			response = ""

			roles_map_user = ewutils.getRoleMap(message.author.roles)
			if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
				response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
			else:
				if mentions_count == 0:
					response = "Give slimes to who?"
				else:
					if tokens_count > 1:
						value = None
						for token in tokens[1:]:
							try:
								value = int(token)
								break
							except:
								value = None

						if value != None:
							user_slimes = 0
							member_slimes = []
							try:
								conn = ewutils.databaseConnect()
								cursor = conn.cursor()

								user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

								# determine slime count for every member mentioned
								for member in mentions:
									member_slimes.append(EwUser(member=member, conn=conn, cursor=cursor))
							finally:
								cursor.close()
								conn.close()

							if (value * mentions_count) > user_data.slimes:
								response = "You don't have that much slime to give ({:,}/{:,}).".format(user_data.slimes, (value * mentions_count))
							else:
								user_data.slimes -= (value * mentions_count)

								try:
									conn = ewutils.databaseConnect()
									cursor = conn.cursor()

									user_data.persist(conn=conn, cursor=cursor)

									# give value slimes to mentioned players
									for obj in member_slimes:
										obj.slimes += value
										obj.persist(conn=conn, cursor=cursor)

									conn.commit()
								finally:
									cursor.close()
									conn.close()

								response = "Slime scores altered! {}".format(ewcfg.emote_slime1)

						else:
							response = "Give how much slime?"

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Ghosts can haunt enlisted players to reduce their slime score.
		elif cmd == ewcfg.cmd_haunt:
			response = ""

			if mentions_count > 1:
				response = "You can only spook one person at a time. Who do you think you are, the Lord of Ghosts?"
			elif mentions_count == 1:
				time_now = int(time.time())

				# A map of role names to Roles assigned to the current user.
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				# Get the user and target data from the database.
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

					member = mentions[0]
					haunted_data = EwUser(member=member, conn=conn, cursor=cursor)
				finally:
					cursor.close()
					conn.close()

				# A map of role names to Roles assigned to the targeted user.
				roles_map_target = ewutils.getRoleMap(member.roles)

				if ewcfg.role_corpse not in roles_map_user:
					# Only dead players can haunt.
					response = "You can't haunt now. Try {}.".format(ewcfg.cmd_suicide)
				elif message.channel.name != ewcfg.channel_sewers:
					# Allowed only from the-sewers.
					response = "You must haunt from #{}.".format(ewcfg.channel_sewers)
				elif ewcfg.role_copkiller in roles_map_target or ewcfg.role_rowdyfucker in roles_map_target:
					# Disallow haunting of generals.
					response = "He is too far from the sewers in his ivory tower, and thus cannot be haunted."
				elif (time_now - user_data.time_lasthaunt) < ewcfg.cd_haunt:
					# Disallow haunting if the user has haunted too recently.
					response = "You're being a little TOO spooky lately, don't you think?"
				elif time_now > haunted_data.time_expirpvp:
					# Require the target to be flagged for PvP
					response = "{} is not mired in the ENDLESS WAR right now.".format(member.display_name)
				elif ewcfg.role_juvenile in roles_map_target:
					# Juveniles can't be haunted.
					response = "The juveniles are innocent."
				elif ewcfg.role_corpse in roles_map_target:
					# Dead players can't be haunted.
					response = "{} is already dead.".format(member.display_name)
				elif ewcfg.role_rowdyfuckers in roles_map_target or ewcfg.role_copkillers in roles_map_target:
					# Target can be haunted by the player.
					haunted_slimes = int(haunted_data.slimes / ewcfg.slimes_hauntratio)
					if haunted_slimes > ewcfg.slimes_hauntmax:
						haunted_slimes = ewcfg.slimes_hauntmax

					haunted_data.slimes -= haunted_slimes
					user_data.slimes -= haunted_slimes
					user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_haunt))
					user_data.time_lasthaunt = time_now

					# Persist changes to the database.
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data.persist(conn=conn, cursor=cursor)
						haunted_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					response = "{} has been haunted by a discontent corpse! Slime has been lost!".format(member.display_name)
				else:
					# Some condition we didn't think of.
					response = "You cannot haunt {}.".format(member.display_name)
			else:
				# No mentions, or mentions we didn't understand.
				response = "Your spookiness is appreciated, but ENDLESS WAR didn\'t understand that name."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Toss the dice at slime craps!
		elif cmd == ewcfg.cmd_slimecraps:
			last_used = last_crapsed_times.get(message.author.id)
			time_now = int(time.time())

			if last_used == None:
				last_used = 0

			if last_used + 2 > time_now:
				response = "**ENOUGH**"
			elif message.channel.name != ewcfg.channel_casino:
				# Only allowed in the slime casino.
				response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
			else:
				last_crapsed_times[message.author.id] = time_now
				value = None

				if tokens_count > 1:
					for token in tokens[1:]:
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

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
					finally:
						cursor.close()
						conn.close()


					if value > user_data.slimecredit:
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
						crapstokens = message.content.split(' ')

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
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Pull the lever on a slot machine!
		elif cmd == ewcfg.cmd_slimeslots:
			last_used = last_slotsed_times.get(message.author.id)
			time_now = int(time.time())

			if last_used == None:
				last_used = 0

			if last_used + 30 > time_now:
				# Rate limit slot machine action.
				response = "**ENOUGH**"
			elif message.channel.name != ewcfg.channel_casino:
				# Only allowed in the slime casino.
				response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
			else:
				value = ewcfg.slimes_perslot
				last_slotsed_times[message.author.id] = time_now

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
					market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)

				finally:
					cursor.close()
					conn.close()

				if value > user_data.slimecredit:
					response = "You don't have enough SlimeCoin."
				else:
					# Add some suspense...
					await client.edit_message(resp, ewutils.formatMessage(message.author, "You insert {:,} SlimeCoin and pull the handle...".format(ewcfg.slimes_perslot)))
					await asyncio.sleep(3)

					# Spend slimes
					user_data.slimecredit -= value

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
						await client.edit_message(resp, ewutils.formatMessage(message.author, "{} {} {}".format(
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
					user_data.slimecredit += winnings
					user_data.persist()

				last_slotsed_times[message.author.id] = 0

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Play slime pachinko!
		elif cmd == ewcfg.cmd_slimepachinko:
			last_used = last_pachinkoed_times.get(message.author.id)
			time_now = int(time.time())

			if last_used == None:
				last_used = 0

			response = ""

			if last_used + 10 > time_now:
				response = "**ENOUGH**"
			elif message.channel.name != ewcfg.channel_casino:
				# Only allowed in the slime casino.
				response = "You must go to the #{} to gamble your SlimeCoin.".format(ewcfg.channel_casino)
			else:
				last_pachinkoed_times[message.author.id] = time_now
				value = ewcfg.slimes_perpachinko

				user_data = EwUser(member=message.author)

				if value > user_data.slimecredit:
					response = "You don't have enough SlimeCoin to play."
				else:
					await client.edit_message(resp, ewutils.formatMessage(message.author, "You insert {:,} SlimeCoin. Balls begin to drop!".format(ewcfg.slimes_perpachinko)))
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

						await client.edit_message(resp, ewutils.formatMessage(message.author, response))
						await asyncio.sleep(1)

					winnings = winballs * 250
					user_data.slimecredit += winnings
					user_data.persist()

					if winnings > 0:
						response += "\n\n**You won {:,} SlimeCoin!**".format(winnings)
					else:
						response += "\n\nYou lost your SlimeCoin."

				# Allow the player to pachinko again now that we're done.
				last_pachinkoed_times[message.author.id] = 0

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Order a refreshing slime and tonic!
		elif cmd == ewcfg.cmd_drink:
			response = ""

			if message.channel.name != ewcfg.channel_casino:
				# Only allowed in the slime casino.
				response = "You must go to the #{} to order a drink.".format(ewcfg.channel_casino)
			else:
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
					market_data = EwMarket(id_server = message.server.id, conn=conn, cursor=cursor)

				finally:
					cursor.close()
					conn.close()

				value = int(ewcfg.slimes_perdrink / (market_data.rate_exchange / 1000000.0))
				if value <= 0:
					value = 1

				if value > user_data.slimecredit:
					# User doesn't have enough SlimeCoin to get a drink.
					response = "A Slime and Tonic is {cost:,} SlimeCoin (and you only have {credits:,}).".format(cost=value, credits=user_data.slimecredit)
				else:
					# Spend slimes
					user_data.slimecredit -= value
					user_data.stamina = 0

					# Give the casino the slime value of the drink.
					market_data.slimes_casino += ewcfg.slimes_perdrink

					response = "You slam {cost:,} SlimeCoin down on the bar and chug your refreshing Slime and Tonic. Delicious!!".format(cost=value)

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data.persist(conn=conn, cursor=cursor)
						market_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Remove a megaslime (1 mil slime) from a general.
		elif cmd == ewcfg.cmd_deadmega:
			response = ""
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
				response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
			else:
				value = 1000000
				user_slimes = 0
				user_data = EwUser(member=message.author)

				if value > user_data.slimes:
					response = "You don't have that much slime to lose ({:,}/{:,}).".format(user_data.slimes, value)
				else:
					user_data.slimes -= value
					user_data.persist()
					response = "Alas, poor megaslime. You have {:,} slime remaining.".format(user_data.slimes)

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Invest in the slime market!
		elif cmd == ewcfg.cmd_invest:

			if message.channel.name != ewcfg.channel_stockexchange:
				# Only allowed in the stock exchange.
				response = "You must go to the #{} to invest your slime.".format(ewcfg.channel_stockexchange)
			else:
				value = None
				if tokens_count > 1:
					for token in tokens[1:]:
						try:
							value = int(token)
							if value < 0:
								value = None
							break
						except:
							value = None

				if value != None:
					time_now = int(time.time())

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
					finally:
						cursor.close()
						conn.close()

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
						response = "You can't invest right now. Your slimebroker is busy."
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
					response = "Specify how much slime you will invest."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Withdraw your investments!
		elif cmd == ewcfg.cmd_withdraw:

			if message.channel.name != ewcfg.channel_stockexchange:
				# Only allowed in the stock exchange.
				response = "You must go to the #{} to withdraw your slime.".format(ewcfg.channel_stockexchange)
			else:
				value = None
				if tokens_count > 1:
					for token in tokens[1:]:
						try:
							value = int(token)
							if value < 0:
								value = None
							break
						except:
							value = None

				if value != None:
					time_now = int(time.time())

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
					finally:
						cursor.close()
						conn.close()

					rate_exchange = (market_data.rate_exchange / 1000000.0)
										
					credits = value
					slimes = int(value * rate_exchange)

					if value > user_data.slimecredit:
						response = "You don't have that many SlimeCoin to exchange."
					elif user_data.time_lastinvest + ewcfg.cd_invest > time_now:
						# Limit frequency of withdrawals
						response = "You can't withdraw right now. Your slimebroker is busy."
					else:
						user_data.slimes += slimes
						user_data.slimecredit -= credits
						user_data.time_lastinvest = time_now
						market_data.slimes_casino -= slimes

						# Flag the user for PvP
						user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (int(time.time()) + ewcfg.time_pvp_invest_withdraw))

						response = "You exchange {credits:,} SlimeCoin for {slimes:,} slime.".format(credits=credits, slimes=slimes)

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
						roles_map_user = ewutils.getRoleMap(message.author.roles)
						if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
						elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
						elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])


				else:
					response = "Specify how much slime you will withdraw."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Show the current slime market exchange rate (slime per credit).
		elif cmd == ewcfg.cmd_exchangerate:
			response = ""

			market_data = EwMarket(id_server=message.server.id)

			response = "The current market value of SlimeCoin is {cred:,.3f} slime per 1,000 coin.".format(cred=(market_data.rate_exchange / 1000.0))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Show the player's slime credit.
		elif cmd == ewcfg.cmd_slimecredit or cmd == ewcfg.cmd_slimecredit_alt1:
			response = ""

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)
				user_slimecredit = EwUser(member=message.author, conn=conn, cursor=cursor).slimecredit
			finally:
				cursor.close()
				conn.close()

			net_worth = int(user_slimecredit * (market_data.rate_exchange / 1000000.0))
			response = "You have {:,} SlimeCoin, currently valued at {:,} slime.".format(user_slimecredit, net_worth)

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# !harvest is not a command
		elif cmd == ewcfg.cmd_harvest:
			await client.edit_message(resp, ewutils.formatMessage(message.author, '**HARVEST IS NOT A COMMAND YOU FUCKING IDIOT**'))

		# advertise help services
		elif cmd == ewcfg.cmd_help or cmd == ewcfg.cmd_help_alt1 or cmd == ewcfg.cmd_help_alt2:
			await client.edit_message(resp, ewutils.formatMessage(message.author, 'Send me a DM for help.'))

		# Debug command to override the role of a user
		elif debug == True and cmd == (ewcfg.cmd_prefix + 'setrole'):
			response = ""

			if mentions_count == 0:
				response = 'Set who\'s role?'
			else:
				role_target = tokens[1]
				role = roles_map.get(role_target)

				if role != None:
					for user in mentions:
						await client.replace_roles(user, role)

					response = 'Done.'
				else:
					response = 'Unrecognized role.'

			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# didn't match any of the command words.
		else:
			""" couldn't process the command. bail out!! """
			""" bot rule 0: be cute """
			randint = random.randint(1,3)
			msg_mistake = "ENDLESS WAR is growing frustrated."
			if randint == 2:
				msg_mistake = "ENDLESS WAR denies you his favor."
			elif randint == 3:
				msg_mistake = "ENDLESS WAR pays you no mind."

			await asyncio.sleep(1)
			await client.edit_message(resp, msg_mistake)
			await asyncio.sleep(2)
			await client.delete_message(resp)


# find our REST API token
token = ewutils.getToken()

if token == None or len(token) == 0:
	ewutils.logMsg('Please place your API token in a file called "token", in the same directory as this script.')
	sys.exit(0)

# connect to discord and run indefinitely
client.run(token)
