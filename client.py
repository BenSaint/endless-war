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
import ewcmd
from ew import EwUser, EwMarket
from ewwep import EwEffectContainer

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
		time_twitch_downed = 0
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

						if stream_was_live == True and stream_live == False:
							time_twitch_downed = time_now

						if stream_was_live == False and stream_live == True and (time_now - time_twitch_downed) > 600:
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
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						market_data = EwMarket(id_server=server.id, conn=conn, cursor=cursor)
						credit_totals = ewutils.getRecentTotalSlimeCoins(id_server=server.id, conn=conn, cursor=cursor)
					finally:
						cursor.close()
						conn.close()

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
						rate_market += (active_bonus / 4)

						# Invest/Withdraw effects
						credit_rate = 0
						if credit_totals[0] != credit_totals[1]:
							# Positive if net investment, negative if net withdrawal.
							credit_change = (credit_totals[0] - credit_totals[1])
							credit_rate = ((credit_change * 1.0) / credit_totals[1])

							if credit_rate > 1.0:
								credit_rate = 1.0
							elif credit_rate < -0.5:
								credit_rate = -0.5

							credit_rate = int((credit_rate * ewcfg.max_iw_swing) if credit_rate > 0 else (credit_rate * 2 * ewcfg.max_iw_swing))

						rate_market += credit_rate

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
						
						# Advance the time and potentially change weather.
						market_data.clock += 1
						if market_data.clock >= 24 or market_data.clock < 0:
							market_data.clock = 0
						weatherchange = random.randrange(30)
						if weatherchange >= 29:
							pattern_count = len(ewcfg.weather_list)
							if pattern_count > 1:
								weather_old = market_data.weather

								# Randomly select a new weather pattern. Try again if we get the same one we currently have.
								while market_data.weather == weather_old:
									pick = random.randrange(len(ewcfg.weather_list))
									market_data.weather = ewcfg.weather_list[pick].name

							# Log message for statistics tracking.
							ewutils.logMsg("The weather changed. It's now {}.".format(market_data.weather))

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
						
						if market_data.clock == 6:
							response += ' The Slime Stock Exchange is now open for business.'
						elif market_data.clock == 18:
							response += ' The Slime Stock Exchange has closed for the night.'

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
async def on_message_delete(message):
	if message != None and message.server != None and message.author.id != client.user.id and message.content.startswith(ewcfg.cmd_prefix):
		ewutils.logMsg("deleted message from {}: {}".format(message.author.display_name, message.content))
		await client.send_message(message.channel, ewutils.formatMessage(message.author, '**I SAW THAT.**'));

@client.event
async def on_message(message):
	time_now = int(time.time())

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

	content_tolower = message.content.lower()

	if message.content.startswith(ewcfg.cmd_prefix) or message.server == None or len(message.author.roles) < 2:
		"""
			Wake up if we need to respond to messages. Could be:
				message starts with !
				direct message (server == None)
				user is new/has no roles (len(roles) < 2)
		"""

		# tokenize the message. the command should be the first word.
		tokens = message.content.split(' ')
		tokens_count = len(tokens)
		cmd = tokens[0].lower()

		""" reply to DMs with help document """
		if message.server == None:
			time_last = last_helped_times.get(message.author.id, 0)

			# Only send the help doc once every thirty seconds. There's no need to spam it.
			if (time_now - time_last) > 30:
				last_helped_times[message.author.id] = time_now
				await client.send_message(message.channel, 'Check out the guide for help: https://ew.krakissi.net/guide/')

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
		if cmd == ewcfg.cmd_kill or cmd == ewcfg.cmd_shoot:
			response = ""

			user_data = EwUser(member=message.author)

			if message.channel.name != ewcfg.channel_combatzone:
				response = "You must go to the #{} to commit gang violence.".format(ewcfg.channel_combatzone)
			elif mentions_count > 1:
				response = "One shot at a time!"
			elif mentions_count <= 0:
				response = "Your bloodlust is appreciated, but ENDLESS WAR didn\'t understand that name."
			elif user_data.stamina >= ewcfg.stamina_max:
				response = "You are too exhausted for gang violence right now. Go get some grub!"
			elif mentions_count == 1:
				# The roles assigned to the author of this message.
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				# Get shooting player's info
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					if user_data.slimelevel <= 0:
						user_data.slimelevel = 1

					# Flag the shooter for PvP no matter what happens next.
					user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))
					user_data.persist(conn=conn, cursor=cursor)

					# Get target's info.
					member = mentions[0]
					shootee_data = EwUser(member=member, conn=conn, cursor=cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()

				miss = False
				crit = False
				strikes = 0

				# Shot player's assigned Discord roles.
				roles_map_target = ewutils.getRoleMap(member.roles)

				# Slime level data. Levels are in powers of 10.
				slimes_bylevel = int((10 ** user_data.slimelevel) / 10)
				slimes_spent = int(slimes_bylevel / 10)
				slimes_damage = int((slimes_bylevel / 5.0) * (100 + (user_data.weaponskill * 5)) / 100.0)
				slimes_dropped = shootee_data.totaldamage

				fumble_chance = (random.randrange(10) - 4)
				if fumble_chance > user_data.weaponskill:
					miss = True

				user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkillers in roles_map_user
				user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

				# Add the PvP flag role.
				if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
				elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
				elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
					await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])

				if ewcfg.role_copkiller in roles_map_target or ewcfg.role_rowdyfucker in roles_map_target:
					# Disallow killing generals.
					response = "He is hiding in his ivory tower and playing video games like a retard."

				elif (slimes_spent > user_data.slimes):
					# Not enough slime to shoot.
					response = "You don't have enough slime to attack. ({:,}/{:,})".format(user_data.slimes, slimes_spent)

				elif (time_now - user_data.time_lastkill) < ewcfg.cd_kill:
					# disallow kill if the player has killed recently
					response = "Take a moment to appreciate your last slaughter."

				elif shootee_data.id_killer == user_data.id_user:
					# Don't allow the shootee to be shot by the same player twice.
					response = "You have already proven your superiority over {}.".format(member.display_name)

				elif time_now > shootee_data.time_expirpvp:
					# Target is not flagged for PvP.
					response = "{} is not mired in the ENDLESS WAR right now.".format(member.display_name)

				elif user_iskillers == False and user_isrowdys == False:
					# Only killers, rowdys, the cop killer, and rowdy fucker can shoot people.
					if ewcfg.role_juvenile in roles_map_user:
						response = "Juveniles lack the moral fiber necessary for violence."
					else:
						response = "You lack the moral fiber necessary for violence."

				elif ewcfg.role_corpse in roles_map_target:
					# Target is already dead.
					response = "{} is already dead.".format(member.display_name)

				elif (time_now - shootee_data.time_lastrevive) < ewcfg.invuln_onrevive:
					# User is currently invulnerable.
					response = "{} has died too recently and is immune.".format(member.display_name)

				else:
					# Slimes from this shot might be awarded to the boss.
					role_boss = (ewcfg.role_copkiller if user_iskillers else ewcfg.role_rowdyfucker)
					boss_slimes = 0

					role_corpse = roles_map[ewcfg.role_corpse]

					was_juvenile = False
					was_killed = False
					was_shot = False

					if (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)) or (ewcfg.role_juvenile in roles_map_target):
						# User can be shot.
						if ewcfg.role_juvenile in roles_map_target:
							was_juvenile = True

						was_shot = True

					if was_shot:
						#stamina drain
						user_data.stamina += ewcfg.stamina_pershot
						
						# Weaponized flavor text.
						weapon = ewcfg.weapon_map.get(user_data.weapon)
						randombodypart = ewcfg.hitzone_list[random.randrange(len(ewcfg.hitzone_list))]

						# Weapon-specific adjustments
						if weapon != None and weapon.fn_effect != None:
							# Build effect container
							ctn = EwEffectContainer(
								miss=miss,
								crit=crit,
								slimes_damage=slimes_damage,
								slimes_spent=slimes_spent,
								user_data=user_data,
								shootee_data=shootee_data
							)

							# Make adjustments
							weapon.fn_effect(ctn)

							# Apply effects for non-reference values
							miss = ctn.miss
							crit = ctn.crit
							slimes_damage = ctn.slimes_damage
							slimes_spent = ctn.slimes_spent
							strikes = ctn.strikes
							# user_data and shootee_data should be passed by reference, so there's no need to assign them back from the effect container.

							if miss:
								slimes_damage = 0

						# Remove !revive invulnerability.
						user_data.time_lastrevive = 0
						user_data.slimes -= slimes_spent

						# Remove repeat killing protection if.
						if user_data.id_killer == shootee_data.id_user:
							user_data.id_killer = ""

						# Don't allow attacking to cause you to go negative.
						if user_data.slimes < 0:
							user_data.slimes = 0

						if slimes_damage >= shootee_data.slimes:
							was_killed = True

						if was_killed:
							# Move around slime as a result of the shot.
							if shootee_data.slimes > 0:
								if was_juvenile:
									user_data.slimes += slimes_dropped
								else:
									market_data = EwMarket(id_server=message.server.id)
									coinbounty = int(shootee_data.bounty / (market_data.rate_exchange / 1000000.0))
									user_data.slimecredit += coinbounty
									user_data.slimes += int(slimes_dropped / 2)
									boss_slimes += int(slimes_dropped / 2)

							# Player was killed.
							shootee_data.slimes = 0
							shootee_data.id_killer = user_data.id_user
							shootee_data.bounty = 0

							if weapon != None:
								response = weapon.str_damage.format(
									name_player=message.author.display_name,
									name_target=member.display_name,
									hitzone=randombodypart,
									strikes=strikes
								)
								if crit:
									response += " {}".format(weapon.str_crit.format(
										name_player=message.author.display_name,
										name_target=member.display_name
									))

								response += "\n\n{}".format(weapon.str_kill.format(
									name_player=message.author.display_name,
									name_target=member.display_name,
									emote_skull=ewcfg.emote_slimeskull
								))
								shootee_data.trauma = weapon.id_weapon
							else:
								response = "{name_target} is hit!!\n\n{name_target} has died.".format(name_target=member.display_name)
								shootee_data.trauma = ""

							#adjust kills bounty
							user_data.kills += 1
							user_data.bounty += int((shootee_data.bounty / 2) + (shootee_data.totaldamage / 4))

							# Give a bonus to the player's weapon skill for killing a stronger player.
							if shootee_data.slimelevel > user_data.slimelevel:
								user_data.weaponskill += 1

						else:
							# A non-lethal blow!
							shootee_data.slimes -= slimes_damage
							shootee_data.totaldamage += slimes_damage

							if weapon != None:
								if miss:
									response = "{}".format(weapon.str_miss.format(
										name_player=message.author.display_name,
										name_target=member.display_name
									))
								else:
									response = weapon.str_damage.format(
										name_player=message.author.display_name,
										name_target=member.display_name,
										hitzone=randombodypart,
										strikes=strikes
									)
									if crit:
										response += " {}".format(weapon.str_crit.format(
											name_player=message.author.display_name,
											name_target=member.display_name
										))
							else:
								if miss:
									response = "{} is unharmed.".format(member.display_name)
								else:
									response = "{} is hit!!".format(member.display_name)
					else:
						response = 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter {}.'.format(member.display_name)

					# Level up the player if appropriate.
					new_level = len(str(int(user_data.slimes)))
					if new_level > user_data.slimelevel:
						response += "\n\n{} has been empowered by slime and is now a level {} slimeboi!".format(message.author.display_name, new_level)
						user_data.slimelevel = new_level

					# Give slimes to the boss if possible.
					boss_member = None
					if boss_slimes > 0:
						for member_search in message.author.server.members:
							if role_boss in ewutils.getRoleMap(member_search.roles):
								boss_member = member_search
								break

					# Persist every users' data.
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data.persist(conn=conn, cursor=cursor)
						shootee_data.persist(conn=conn, cursor=cursor)

						if boss_member != None:
							boss_data = EwUser(member=boss_member, conn=conn, cursor=cursor)
							boss_data.slimes += boss_slimes
							boss_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					# Assign the corpse role to the newly dead player.
					if was_killed:
						await client.replace_roles(member, role_corpse)

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Choose your weapon
		elif cmd == ewcfg.cmd_equip:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to change your equipment.".format(ewcfg.channel_dojo)
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				weapon = ewcfg.weapon_map.get(value)
				if weapon != None:
					response = weapon.str_equip
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						user_skills = ewutils.weaponskills_get(member=message.author, conn=conn, cursor=cursor)

						user_data.weapon = weapon.id_weapon
						user_data.weaponskill = user_skills.get(weapon.id_weapon)
						if user_data.weaponskill == None:
							user_data.weaponskill = 0

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose your weapon: {}".format(ewutils.formatNiceList(names=ewcfg.weapon_names, conjunction="or"))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Kill yourself to return slime to your general.
		elif cmd == ewcfg.cmd_suicide:
			response = ""

			# Only allowed in the combat zone.
			if message.channel.name != ewcfg.channel_combatzone:
				response = "You must go to the #{} to commit suicide.".format(ewcfg.channel_combatzone)
			elif message.author.id == '295313459934003200':
				response = "You can't do that, Doop."
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

					if user_data.stamina >= ewcfg.stamina_max:
						response = "You are too exhausted to train right now. Go get some grub!"
					elif sparred_data.stamina >= ewcfg.stamina_max:
						response = "{} is too exhausted to train right now. They need a snack!".format(member.display_name)
					elif user_iskillers == False and user_isrowdys == False:
						# Only killers, rowdys, the cop killer, and the rowdy fucker can spar
						response = "Juveniles lack the backbone necessary for combat."
					else:
						was_juvenile = False
						was_sparred = False
						was_dead = False
						was_player_tired = False
						was_target_tired = False
						was_enemy = False
						duel = False

						roles_map_target = ewutils.getRoleMap(member.roles)

						#Determine if the !spar is a duel:
						weapon = None
						if user_data.weapon != None and user_data.weapon != "" and user_data.weapon == sparred_data.weapon:
							weapon = ewcfg.weapon_map.get(user_data.weapon)
							duel = True

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
						elif (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)):
							# Target is a member of the opposing faction.
							was_enemy = True


						#if the duel is successful
						if was_sparred:
							weaker_player = sparred_data if sparred_data.slimes < user_data.slimes else user_data
							stronger_player = sparred_data if user_data is weaker_player else user_data

							# Flag the player for PvP
							user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))

							# Weaker player gains slime based on the slime of the stronger player.
							slimegain = ewcfg.slimes_perspar if (stronger_player.slimes / 2) > ewcfg.slimes_perspar else (stronger_player.slimes / 2)
							weaker_player.slimes += slimegain
							
							#stamina drain for both players
							user_data.stamina += ewcfg.stamina_perspar
							sparred_data.stamina += ewcfg.stamina_perspar

							# Bonus 50% slime to both players in a duel.
							if duel:
								weaker_player.slimes += int(slimegain / 2)
								stronger_player.slimes += int(slimegain / 2)
								if weaker_player.weaponskill < 5:
									weaker_player.weaponskill += 1
								if stronger_player.weaponskill < 5:
									stronger_player.weaponskill += 1

							weaker_player.time_lastspar = time_now

							try:
								conn = ewutils.databaseConnect()
								cursor = conn.cursor()

								user_data.persist(conn=conn, cursor=cursor)
								sparred_data.persist(conn=conn, cursor=cursor)

								conn.commit()
							finally:
								cursor.close()
								conn.close()

							# Add the PvP flag role.
							if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
							elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
							elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
								await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])

							# player was sparred with
							if duel and weapon != None:
								response = weapon.str_duel.format(name_player=message.author.display_name, name_target=member.display_name)
							else:
								response = '{} parries the attack. :knife: {}'.format(member.display_name, ewcfg.emote_slime5)

							#Notify if max skill is reached	
							if weapon != None:
								if user_data.weaponskill == 5:
									response += ' {} is a master of the {}.'.format(message.author.display_name, weapon.id_weapon)
								if sparred_data.weaponskill == 5:
									response += ' {} is a master of the {}.'.format(member.display_name, weapon.id_weapon)

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
							elif was_enemy:
								# target and player are different factions
								response = "You cannot spar with your enemies."
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
					player_is_pvp = False

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						player_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)

						# Endless War collects his fee.
						fee = (player_data.slimecredit / 10)
						player_data.slimecredit -= fee
						market_data.slimes_revivefee += fee
						
						# Preserve negaslime
						if player_data.slimes < 0:
							market_data.negaslime += player_data.slimes

						# Give player some initial slimes.
						player_data.slimes = ewcfg.slimes_onrevive

						# Clear fatigue, totaldamage, bounty, killcount.
						player_data.stamina = 0
						player_data.totaldamage = 0
						player_data.bounty = 0
						player_data.kills = 0

						# Clear PvP flag.
						player_data.time_expirpvp = time_now - 1;

						# Clear weapon and weaponskill.
						player_data.weapon = ""
						player_data.weaponskill = 0
						ewutils.weaponskills_clear(member=message.author, conn=conn, cursor=cursor)

						# Set time of last revive. This used to provied spawn protection, but currently isn't used.
						player_data.time_lastrevive = time_now

						if(player_data.time_expirpvp > time_now):
							player_is_pvp = True

						# Set initial slime level. It's probably 2.
						player_data.slimelevel = len(str(player_data.slimes))

						player_data.persist(conn=conn, cursor=cursor)
						market_data.persist(conn=conn, cursor=cursor)

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

					if user_data.stamina >= ewcfg.stamina_max:
						mismined = last_mismined_times.get(message.author.id)

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

						if mismined['count'] >= 5:
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

						# Adjust slime level.
						was_levelup = False
						new_level = len(str(int(user_data.slimes)))
						if new_level > user_data.slimelevel:
							was_levelup = True
							user_data.slimelevel = new_level

						# Fatigue the miner.
						user_data.stamina += ewcfg.stamina_permine
						if random.randrange(10) > 6:
							user_data.stamina += ewcfg.stamina_permine

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

						# Tell the player their slime level increased.
						if was_levelup:
							await client.send_message(message.channel, ewutils.formatMessage(message.author, "You have been empowered by slime and are now a level {} slimeboi!".format(new_level)))
				else:
					mismined = last_mismined_times.get(message.author.id)

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
			user_data = None

			if mentions_count == 0:
				user_data = EwUser(member=message.author)

				# return my score
				response = "You currently have {:,} slime.".format(user_data.slimes)

			else:
				member = mentions[0]
				user_data = EwUser(member=member)

				# return somebody's score
				response = "{} currently has {:,} slime.".format(member.display_name, user_data.slimes)

			# Update the user's slime level.
			if user_data != None:
				new_level = len(str(int(user_data.slimes)))
				if new_level > user_data.slimelevel:
					user_data.slimelevel = new_level

				user_data.persist()

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Show a player's combat data.
		elif cmd == ewcfg.cmd_data:
			response = ""
			user_data = None

			if mentions_count == 0:
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
					market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)

					# Update the user's slime level.
					new_level = len(str((int(user_data.slimes))))
					if new_level > user_data.slimelevel:
						user_data.slimelevel = new_level
						user_data.persist(conn=conn, cursor=cursor)
						conn.commit()
				finally:
					cursor.close()
					conn.close()

				# return my data
				response = "You are a level {} slimeboi.".format(user_data.slimelevel)
				
				coinbounty = int(user_data.bounty / (market_data.rate_exchange / 1000000.0))

				weapon = ewcfg.weapon_map.get(user_data.weapon)
				if weapon != None:
					if user_data.weaponskill >= 5:
						response += " {}".format(weapon.str_weaponmaster_self.format(rank=(user_data.weaponskill - 4)))
					else:
						response += " {}".format(weapon.str_weapon_self)
					
				trauma = ewcfg.weapon_map.get(user_data.trauma)
				if trauma != None:
					response += " {}".format(trauma.str_trauma_self)

				if user_data.kills > 0:
					response += " You have {:,} confirmed kills.".format(user_data.kills)
				
				if coinbounty != 0:
					response += " SlimeCorp offers a bounty of {:,} SlimeCoin for your death.".format(coinbounty)

				if user_data.stamina > 0:
					response += " You are {}% fatigued.".format(user_data.stamina * 100.0 / ewcfg.stamina_max)
			else:
				member = mentions[0]
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=member, conn=conn, cursor=cursor)
					market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)

					new_level = len(str(int(user_data.slimes)))
					if new_level > user_data.slimelevel:
						user_data.slimelevel = new_level
						user_data.persist(conn=conn, cursor=cursor)
						conn.commit()
				finally:
					cursor.close()
					conn.close()

				# return somebody's score
				response = "{} is a level {} slimeboi.".format(member.display_name, user_data.slimelevel)
				
				coinbounty = int(user_data.bounty / (market_data.rate_exchange / 1000000.0))

				weapon = ewcfg.weapon_map.get(user_data.weapon)
				if weapon != None:
					if user_data.weaponskill >= 5:
						response += " {}".format(weapon.str_weaponmaster.format(rank=(user_data.weaponskill - 4)))
					else:
						response += " {}".format(weapon.str_weapon)
					
				trauma = ewcfg.weapon_map.get(user_data.trauma)
				if trauma != None:
					response += " {}".format(trauma.str_trauma)

				if user_data.kills > 0:
					response += " They have {:,} confirmed kills.".format(user_data.kills)

				if coinbounty != 0:
					response += " SlimeCorp offers a bounty of {:,} SlimeCoin for their death.".format(coinbounty)

			# Update the user's slime level.
			if user_data != None:
				new_level = len(str(int(user_data.slimes)))
				if new_level > user_data.slimelevel:
					user_data.slimelevel = new_level

				user_data.persist()

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		#check what time it is, and the weather
		elif cmd == ewcfg.cmd_time or cmd == ewcfg.cmd_clock or cmd == ewcfg.cmd_weather:
			response = ""
			market_data = EwMarket(id_server=message.author.server.id)
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
				if time_current >= 4 and time_current <= 5:
					flair = weather_data.str_sunrise
				if time_current >= 6 and time_current <= 16:
					flair = weather_data.str_day
				if time_current >= 17 and time_current <= 18:
					flair = weather_data.str_sunset
				if time_current >= 19 or time_current <= 4:
					flair = weather_data.str_night
					
			response += "It is currently {}{} in NLACakaNM.{}".format(displaytime, ampm, (' ' + flair))
			
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
				elif ewcfg.role_corpse in roles_map_target:
					# Dead players can't be haunted.
					response = "{} is already dead.".format(member.display_name)
				elif ewcfg.role_rowdyfuckers in roles_map_target or ewcfg.role_copkillers in roles_map_target or ewcfg.role_juvenile in roles_map_target:
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

				if ewcmd.is_casino_open(market_data.clock) == False:
					response = ewcfg.str_casino_closed
				elif value > user_data.slimecredit:
					response = "You don't have enough SlimeCoin."
				else:
					#subtract slimecoin from player
					user_data.slimecredit -= value
					user_data.persist()

					# Add some suspense...
					await client.edit_message(resp, ewutils.formatMessage(message.author, "You insert {:,} SlimeCoin and pull the handle...".format(ewcfg.slimes_perslot)))
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
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						# add winnings
						user_data.slimecredit += winnings

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

				last_slotsed_times[message.author.id] = 0

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Play slime pachinko!
		elif cmd == ewcfg.cmd_slimepachinko:
			last_used = last_pachinkoed_times.get(message.author.id)

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

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)
					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
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
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						# Significant time has passed since the user issued this command. We can't trust that their data hasn't changed.
						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

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
				last_pachinkoed_times[message.author.id] = 0

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# See what's for sale in the Food Court.
		elif cmd == ewcfg.cmd_menu:
			if message.channel.name != ewcfg.channel_foodcourt:
				# Only allowed in the food court.
				response = ewcfg.str_food_channelreq.format(action="see the menu")
			else:
				response = "NLACakaNM Food Court Menu:\n\n"

				for vendor in ewcfg.food_vendor_inv:
					response += "**{}**: *{}*\n".format(vendor, ewutils.formatNiceList(names=ewcfg.food_vendor_inv[vendor]))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# Order refreshing food and drinks!
		elif cmd == ewcfg.cmd_order:
			if message.channel.name != ewcfg.channel_foodcourt:
				# Only allowed in the food court.
				response = ewcfg.str_food_channelreq.format(action="order")
			else:
				value = None
				if tokens_count > 1:
					for token in tokens[1:]:
						if token.startswith('<@') == False:
							value = token
							break

				food = ewcfg.food_map.get(value)

				member = None
				if mentions_count == 1:
					member = mentions[0]
					if member.id == message.author.id:
						member = None

				if food == None:
					response = "Check the {} for a list of items you can {}.".format(ewcfg.cmd_menu, ewcfg.cmd_order)
				else:
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
						market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)

						target_data = None
						if member != None:
							target_data = EwUser(member=member, conn=conn, cursor=cursor)
					finally:
						cursor.close()
						conn.close()

					value = int(food.price / (market_data.rate_exchange / 1000000.0))
					if value <= 0:
						value = 1

					# Kingpins eat free.
					roles_map_user = ewutils.getRoleMap(message.author.roles)
					if ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
						value = 0

					if value > user_data.slimecredit:
						# Not enough money.
						response = "A {food} is {cost:,} SlimeCoin (and you only have {credits:,}).".format(
							food=food.str_name,
							cost=value,
							credits=user_data.slimecredit
						)
					else:
						user_data.slimecredit -= value

						if target_data != None:
							target_data.stamina -= food.recover_stamina
							if target_data.stamina < 0:
								target_data.stamina = 0
						else:
							user_data.stamina -= food.recover_stamina
							if user_data.stamina < 0:
								user_data.stamina = 0

						market_data.slimes_casino += food.price

						response = "You slam {cost:,} SlimeCoin down at the {vendor} for a {food}{sharetext}{flavor}".format(
							cost=value,
							vendor=food.vendor,
							food=food.str_name,
							sharetext=(". " if member == None else " and give it to {}.\n\n{}".format(member.display_name, ewutils.formatMessage(member, ""))),
							flavor=food.str_eat
						)

						try:
							conn = ewutils.databaseConnect()
							cursor = conn.cursor()

							user_data.persist(conn=conn, cursor=cursor)
							market_data.persist(conn=conn, cursor=cursor)

							if target_data != None:
								target_data.persist(conn=conn, cursor=cursor)

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


		# Transfer slime between players. Shares a cooldown with investments.
		elif cmd == ewcfg.cmd_transfer or cmd == ewcfg.cmd_transfer_alt1:
			if message.channel.name != ewcfg.channel_stockexchange:
				# Only allowed in the stock exchange.
				response = ewcfg.str_exchange_channelreq.format(currency="SlimeCoin", action="transfer")
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			if mentions_count != 1:
				# Must have exactly one target to send to.
				response = "Mention the player you want to send SlimeCoin to."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			member = mentions[0]
			roles_map_target = ewutils.getRoleMap(member.roles)

			if ewcfg.role_rowdyfucker in roles_map_target or ewcfg.role_copkiller in roles_map_target:
				# Disallow transfers to RF and CK kingpins.
				response = "You can't transfer SlimeCoin to a known criminal warlord."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return


			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				target_data = EwUser(member=member, conn=conn, cursor=cursor)
				user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
				market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
			finally:
				cursor.close()
				conn.close()

			if market_data.clock >= 18 or market_data.clock < 6:
				response = ewcfg.str_exchange_closed
			else:
				# Parse the slime value to send.
				value = None
				if tokens_count > 1:
					value = ewutils.getIntToken(tokens=tokens, allow_all=True)

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
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Invest in the slime market!
		elif cmd == ewcfg.cmd_invest:
			if message.channel.name != ewcfg.channel_stockexchange:
				# Only allowed in the stock exchange.
				response = ewcfg.str_exchange_channelreq.format(currency="slime", action="invest")
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			roles_map_user = ewutils.getRoleMap(message.author.roles)
			if ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow investments by RF and CK kingpins.
				response = "You're too powerful to be playing the market."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
				market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
			finally:
				cursor.close()
				conn.close()

			if market_data.clock >= 18 or market_data.clock < 6:
				response = ewcfg.str_exchange_closed
			else:
				value = None
				if tokens_count > 1:
					value = ewutils.getIntToken(tokens=tokens, allow_all=True)

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
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Withdraw your investments!
		elif cmd == ewcfg.cmd_withdraw:
			if message.channel.name != ewcfg.channel_stockexchange:
				# Only allowed in the stock exchange.
				response = ewcfg.str_exchange_channelreq.format(currency="SlimeCoin", action="withdraw")
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data = EwUser(member=message.author, conn=conn, cursor=cursor)
				market_data = EwMarket(id_server=message.author.server.id, conn=conn, cursor=cursor)
			finally:
				cursor.close()
				conn.close()

			if market_data.clock >= 18 or market_data.clock < 6:
				response = ewcfg.str_exchange_closed
			else:
				value = None
				if tokens_count > 1:
					value = ewutils.getIntToken(tokens=tokens, allow_all=True)

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
							response += "\n\n{} has been empowered by slime and is now a level {} slimeboi!".format(message.author.display_name, new_level)
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
						roles_map_user = ewutils.getRoleMap(message.author.roles)
						if ewcfg.role_copkillers in roles_map_user and ewcfg.role_copkillers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_copkillers_pvp])
						elif ewcfg.role_rowdyfuckers in roles_map_user and ewcfg.role_rowdyfuckers_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_rowdyfuckers_pvp])
						elif ewcfg.role_juvenile in roles_map_user and ewcfg.role_juvenile_pvp not in roles_map_user:
							await client.add_roles(message.author, roles_map[ewcfg.role_juvenile_pvp])


				else:
					response = ewcfg.str_exchange_specify.format(currency="SlimeCoin", action="withdraw")

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))


		# Show the current slime market exchange rate (slime per credit).
		elif cmd == ewcfg.cmd_exchangerate or cmd == ewcfg.cmd_exchangerate_alt1:
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

		# Show the total of negative slime in the world.
		elif cmd == ewcfg.cmd_negaslime:
			negaslime = 0

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				# Count all negative slime currently possessed by dead players.
				cursor.execute("SELECT sum({}) FROM users WHERE id_server = %s AND {} < 0".format(
					ewcfg.col_slimes,
					ewcfg.col_slimes
				), (message.server.id, ))

				result = cursor.fetchone();

				if result != None:
					negaslime = result[0]

					if negaslime == None:
						negaslime = 0
						
				# Add persisted negative slime.
				market_data = EwMarket(id_server=message.server.id, conn=conn, cursor=cursor)
				negaslime += market_data.negaslime

			finally:
				cursor.close()
				conn.close()

			await client.edit_message(resp, ewutils.formatMessage(message.author, "The dead have amassed {:,} negative slime.".format(negaslime)))
			
		# Read the Lab Instructions
		elif cmd == ewcfg.cmd_labmanual
			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to research how to create a Slimeoid.".format(ewcfg.channel_slimeoidlab)
			else:
				response = "In SlimeCorp Labs, you can create a Slimeoid minion.\n!incubate to begin the birthing process. Then choose its form and abilities with !growhead, !growmobility, !growoffense, !growdefense, and !growspecial.\nUse !growpower to allocate 6 points between your Slimeoid's ATK, DEF, and INT stats. Use !nameslimeoid to give it a name. Finally, !spawn to complete your Slimeoid's incubation and birth it into the world.\n Should you decide your Slimeoid is unfit, !dissolve to re-incorporate the unfortunate Slimeoid back into SlimeCorp's slime vats."
				# Send the response to the player.
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		# Create a slimeoid
		elif cmd == ewcfg.cmd_incubate:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to create a Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				body = ewcfg.body_map.get(value)
				
				if user_data.slimeoid_weapon != ''
					response = "You have already created a Slimeoid."
				
				elif body = None:
					response = offense.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_body = body.id_body

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose what your Slimeoid's form will be: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.body_names, conjunction="or"))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
		
		# shape your slimeoid's head
		elif cmd == ewcfg.cmd_growhead:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to modify your Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				head = ewcfg.head_map.get(value)
				
				if user_data.slimeoid_head != ''
					response = "You have already chosen the shape of {}\'s head.".format(user_data.slimeoid_name)
				
				elif user_data.slimeoid_body == ''
					response = "You must !incubate to create a Slimeoid first."
				
				elif head = None:
					response = head.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_head = head.id_head

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose a head shape for {}: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.head_names, conjunction="or"))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# shape your slimeoid's legs
		elif cmd == ewcfg.cmd_growmobility:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to modify your Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				mobility = ewcfg.mobility_map.get(value)
				
				if user_data.slimeoid_mobility != ''
					response = "You have already given {} a means of mobility.".format(user_data.slimeoid_name)
				
				elif user_data.slimeoid_body == ''
					response = "You must !incubate to create a Slimeoid first."
				
				elif mobility = None:
					response = mobility.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_mobility = mobility.id_mobility

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose a means of mobility for {}: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.mobility_names, conjunction="or"))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		# shape your slimeoid's weapon
		elif cmd == ewcfg.cmd_growweapon:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to modify your Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				offense = ewcfg.offense_map.get(value)
				
				if user_data.slimeoid_weapon != ''
					response = "You have already given {} a means of offense.".format(user_data.slimeoid_name)
				
				elif user_data.slimeoid_body == ''
					response = "You must !spawnslimeoid to create a Slimeoid first."
				
				elif offense = None:
					response = offense.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_weapon = offense.id_offense

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose a means of offense for {}: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.offense_names, conjunction="or"))

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		# shape your slimeoid's armor
		elif cmd == ewcfg.cmd_growarmor:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to modify your Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				defense = ewcfg.defense_map.get(value)
				
				if user_data.slimeoid_armor != ''
					response = "You have already given {} a means of defense.".format(user_data.slimeoid_name)
					
				elif user_data.slimeoid_body == ''
					response = "You must !spawnslimeoid to create a Slimeoid first."
				
				elif offense = None:
					response = defense.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_armor = defense.id_defense

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose a means of defense for {}: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.defense_names, conjunction="or"))
				
			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		# shape your slimeoid's special ability
		elif cmd == ewcfg.cmd_growspecial:
			response = ""

			if message.channel.name != ewcfg.channel_dojo:
				response = "You must go to the #{} to modify your Slimeoid.".format(ewcfg.channel_slimeoidlab)
			
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			else:
				value = None
				if tokens_count > 1:
					value = tokens[1]

				user_data = EwUser(member=message.author)
				special = ewcfg.offense_map.get(value)
				
				if user_data.slimeoid_special != ''
					response = "You have already given {} a special ability.".format(user_data.slimeoid_name)
					
				elif user_data.slimeoid_body == ''
					response = "You must !spawnslimeoid to create a Slimeoid first."
				
				elif special = None:
					response = special.str_create
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

						user_data.slimeoid_special = offense.id_offense

						user_data.persist(conn=conn, cursor=cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					response = "Choose a special ability for {}: {}".format(user_data.slimeoid_name, ewutils.formatNiceList(names=ewcfg.special_names, conjunction="or"))
				user_data.persist()
			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				
		# Name your slimeoid.
		elif cmd = ewcfg.cmd_nameslimeoid
		
			if message.channel.name != ewcfg.channel_slimeoidlab:
				# Only allowed in the stock exchange.
				response = "Go to Slimecorp's slimeoid Labs to create and customize your Slimeoid."

			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				
			user_data = EwUser(member=message.author)	
			elif user_data.slimeoid_name != ''
				response = "You have already given {} a name.".format(user_data.slimeoid_name)				
			
			elif user_data.slimeoid_body == ''
					response = "You must !spawnslimeoid to create a Slimeoid first."
			
			else:
				name = ""
				if tokens_count > 1:
					name = tokens[1].lower()
					user_data = EwUser(member=message.author)
					user_data.slimeoid_name = name
					response = "You hereby dub your slimeoid '{}'.".format(name)
				
				user_data.persist()
					
			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
		
		# LVL up your SLimeoid
		elif cmd = ewcfg.cmd_growpower
		
			if message.channel.name != ewcfg.channel_slimeoidlab:
				# Only allowed in the stock exchange.
				response = "Go to Slimecorp's slimeoid Labs to create and customize your Slimeoid."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return

			roles_map_user = ewutils.getRoleMap(message.author.roles)
			elif ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				# Disallow slimeoids by RF and CK kingpins.
				response = "SlimeCorp has banned you from using their facilities."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return
			
			else:
				if tokens_count > 1:
					stat = tokens[1].lower()
					user_data = EwUser(member=message.author)
					if user_data.slimeoid_level >= 5
						response = "Your Slimeoid is at full power."
					else:
						if stat = "atk":
							user_data.slimeoid_atk += 1
							response = "{}\'s offensive ability has increased.".format(user_data.slimeoid_name)
							user_data.slimeoid_level += 1
						elif stat = "def":
							user_data.slimeoid_def += 1
							response = "{}\'s offensive ability has increased.".format(user_data.slimeoid_name)
							user_data.slimeoid_level += 1
						elif stat = "int":
							user_data.slimeoid_int += 1
							response = "{}\'s offensive ability has increased.".format(user_data.slimeoid_name)
							user_data.slimeoid_level += 1
						else:
							Specify which of your Slimeoid's attributes you will enhance: ATK, DEF, or INT
				
				user_data.persist()
					
			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
			
		# Complete your Slimeoid
		elif cmd == ewcfg.cmd_spawn:
			response = ""
			user_data = EwUser(member=message.author)
			if user_data.slimeoid_level = 5 and user_data.slimeoid_body != '' and user_data.slimeoid_head != '' and user_data.slimeoid_weapon != '' and user_data.slimeoid_armor != '' and user_data.slimeoid_special != '' and user_data.slimeoid_name != '':
				user_data.slimeoid_ready = True
				response = "Congratulations! You are now the proud owner of {} the Slimeoid!".format(user_data.slimeoid_name)
				user_data.persist()
			else:
				response = "Your Slimeoid is not ready to be spawned yet."
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				
		# dissolve your Slimeoid
		elif cmd == ewcfg.cmd_dissolve:
			response = ""
			if message.channel.name != ewcfg.channel_slimeoidlab:
				# Only allowed in the stock exchange.
				response = "Go to Slimecorp's slimeoid Labs to dissolve your Slimeoid."
				await client.edit_message(resp, ewutils.formatMessage(message.author, response))
				return
			else:
				user_data = EwUser(member=message.author)
				user_data.slimeoid_level = 0
				user_data.slimeoid_body != ''
				user_data.slimeoid_head != ''
				user_data.slimeoid_weapon != ''
				user_data.slimeoid_armor != ''
				user_data.slimeoid_special != ''
				user_data.slimeoid_name != '':
				user_data.slimeoid_ready = False
				response = "You dissolve your Slimeoid into the SlimeCorp slime vats. Use !incubate to begin creating a replacement."
			
		# Show a player's slimeoid data.
		elif cmd == ewcfg.cmd_slimeoid:
			response = ""
			user_data = None

			if mentions_count == 0:
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=message.author, conn=conn, cursor=cursor)

				finally:
					cursor.close()
					conn.close()

				# return my data
				if user_data.slimeoid_ready = True:
					response = "{} is a 2-foot-tall Slimeoid.".format(user_data.slimeoid_name)
					response += " {}".format(slimeoid.str_body)
					response += " {}".format(slimeoid.str_head)
					response += " {}".format(slimeoid.str_mobility)
					response += " {}".format(slimeoid.str_weapon)
					response += " {}".format(slimeoid.str_armor)
					response += " {}".format(slimeoid.str_special)
				
				else:
					response = "You  have not spawned a Slimeoid."
					
			else:
				member = mentions[0]
				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member=member, conn=conn, cursor=cursor)
				finally:
					cursor.close()
					conn.close()

				# return somebody's score
				if user_data.slimeoid_ready = True:
					response = "{} is a 2-foot-tall Slimeoid.".format(user_data.slimeoid_name)
					response += " {}".format(slimeoid.str_body)
					response += " {}".format(slimeoid.str_head)
					response += " {}".format(slimeoid.str_mobility)
					response += " {}".format(slimeoid.str_weapon)
					response += " {}".format(slimeoid.str_armor)
					response += " {}".format(slimeoid.str_special)
				
				else:
					response = "They have not spawned a Slimeoid."

			# Send the response to the player.
			await client.edit_message(resp, ewutils.formatMessage(message.author, response))

		# !harvest is not a command
		elif cmd == ewcfg.cmd_harvest:
			await client.edit_message(resp, ewutils.formatMessage(message.author, '**HARVEST IS NOT A COMMAND YOU FUCKING IDIOT**'))

		# AWOOOOO
		elif cmd == ewcfg.cmd_howl or cmd == ewcfg.cmd_howl_alt1:
			await client.edit_message(resp, ewcmd.cmd_howl(message))

		# advertise patch notes
		elif cmd == ewcfg.cmd_patchnotes:
			await client.edit_message(resp, ewutils.formatMessage(message.author, 'Look for the latest patchnotes on the news page: https://ew.krakissi.net/news/'))

		# advertise help services
		elif cmd == ewcfg.cmd_help or cmd == ewcfg.cmd_help_alt1 or cmd == ewcfg.cmd_help_alt2:
			await client.edit_message(resp, ewutils.formatMessage(message.author, 'Check out the guide for help: https://ew.krakissi.net/guide/'))

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

	elif content_tolower.find(ewcfg.cmd_howl) >= 0 or content_tolower.find(ewcfg.cmd_howl_alt1) >= 0:
		""" Howl if !howl is in the message at all. """
		await client.send_message(message.channel, ewcmd.cmd_howl(message))

# find our REST API token
token = ewutils.getToken()

if token == None or len(token) == 0:
	ewutils.logMsg('Please place your API token in a file called "token", in the same directory as this script.')
	sys.exit(0)

# connect to discord and run indefinitely
client.run(token)
