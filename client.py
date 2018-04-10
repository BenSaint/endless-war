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

import ewutils
import ewcfg

print('Starting up...')

client = discord.Client()

# A map containing user IDs and the last time in UTC seconds since we sent them
# the help doc via DM. This is to prevent spamming.
last_helped_times = {}

debug = False
while sys.argv:
	if sys.argv[0].lower() == '--debug':
		debug = True

	sys.argv = sys.argv[1:]

# When debug is enabled, additional commands are turned on.
if debug == True:
	print('Debug mode enabled.')

@client.event
async def on_ready():
	print('Logged in as {} ({}).'.format(client.user.name, client.user.id))
	print('Ready.')

	await client.change_presence(game=discord.Game(name="dev. by @krak"))


@client.event
async def on_message(message):
	""" do not interact with our own messages """
	if message.author.id == client.user.id or message.author.bot == True:
		return

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
		if cmd != ewcfg.cmd_mine or message.channel.name != ewcfg.channel_mines:
			resp = await client.send_message(message.channel, '...')

		# process command words
		if cmd == ewcfg.cmd_kill:
			if message.channel.name != ewcfg.channel_combatzone:
				await client.edit_message(resp, "You must go to the #{} to commit gang violence.".format(ewcfg.channel_combatzone))
			elif mentions_count > 0:
				# The roles assigned to the author of this user.
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();
					user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author)
				finally:
					cursor.close()
					conn.close()

				if user_slimes < (mentions_count * ewcfg.slimes_tokill):
					await client.edit_message(resp, "You are currently too weak-willed and feminine. Harvest more Juveniles for their slime. ({}/{})".format(user_slimes, mentions_count * ewcfg.slimes_tokill))
				else:
					user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
					user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

					# Only killers, rowdys, the cop killer, and the rowdy fucker can kill people
					if user_iskillers == False and user_isrowdys == False:
						await client.edit_message(resp, "Juveniles lack the moral fiber necessary for murder.")
					else:
						# slimes from this kill might be awarded to the boss
						role_boss = ewcfg.role_copkiller if user_iskillers == True else ewcfg.role_rowdyfucker
						boss_slimes = 0

						role_corpse = roles_map[ewcfg.role_corpse]
						juveniles_killed = []
						adults_killed = []
						users_unkilled = []
						users_killed = []

						# Attempt to kill each mentioned player.
						for member in mentions:
							roles_map_target = ewutils.getRoleMap(member.roles)
							if (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)) or (ewcfg.role_juvenile in roles_map_target):
								if ewcfg.role_juvenile in roles_map_target:
									juveniles_killed.append(member)
								else:
									adults_killed.append(member)

								users_killed.append(member)
								await client.replace_roles(member, role_corpse)
							else:
								users_unkilled.append(member)

						users_killed_count = len(users_killed)
						if users_killed_count > 0:
							try:
								conn = ewutils.databaseConnect();
								cursor = conn.cursor();

								user_slimes = user_slimes - (users_killed_count * ewcfg.slimes_tokill)

								# Add juvenile targets' slimes to this player.
								for member in juveniles_killed:
									juvenile_slimes = ewutils.getSlimesForPlayer(conn, cursor, member)
									if juvenile_slimes > 0:
										user_slimes = user_slimes + juvenile_slimes

								# Add adult tarets' slimes to the boss.
								for member in adults_killed:
									adult_slimes = ewutils.getSlimesForPlayer(conn, cursor, member)
									if adult_slimes > 0:
										boss_slimes = boss_slimes + adult_slimes

								# Set the new slime value for the player.
								ewutils.setSlimesForPlayer(conn, cursor, message.author, user_slimes)

								# Remove all slimes from the other players.
								for member in users_killed:
									ewutils.setSlimesForPlayer(conn, cursor, member, 0)

								conn.commit()
							finally:
								cursor.close()
								conn.close()

							# give slimes to the boss if possible.
							boss_member = None
							if boss_slimes > 0:
								for member in message.author.server.members:
									if role_boss in ewutils.getRoleMap(member.roles):
										boss_member = member
										break
								
								if boss_member != None:
									try:
										conn = ewutils.databaseConnect();
										cursor = conn.cursor();

										boss_slimes = ewutils.getSlimesForPlayer(conn, cursor, boss_member) + boss_slimes
										ewutils.setSlimesForPlayer(conn, cursor, boss_member, boss_slimes)

										conn.commit()
									finally:
										cursor.close()
										conn.close()

							# Present a nice list of killed player names.
							names = ewutils.userListToNameString(users_killed)
							if len(users_unkilled) > 0:
								await client.edit_message(resp, '{} have been SLAUGHTERED. :slime5: :gun: ({} was not.)'.format(names, ewutils.userListToNameString(users_unkilled)))
							else:
								await client.edit_message(resp, '{} has been SLAUGHTERED. :slime5: :gun:'.format(names))

						else:
							if len(users_unkilled) > 0:
								await client.edit_message(resp, 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter {}.'.format(ewutils.userListToNameString(users_unkilled)))
							else:
								await client.edit_message(resp, "ENDLESS WAR will not allow this betrayal.")
			else:
				await client.edit_message(resp, 'Your bloodlust is appreciated, but ENDLESS WAR didn\'t understand that name.')

		# revive yourself as a juvenile after having been killed.
		elif cmd == ewcfg.cmd_revive:
			if message.channel.name != ewcfg.channel_endlesswar:
				await client.edit_message(resp, "Come to me. I hunger. #{}.".format(ewcfg.channel_endlesswar))
			else:
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				if ewcfg.role_corpse in roles_map_user:
					# List of maps of member and slime count.
					member_slime_pile = []

					try:
						conn = ewutils.databaseConnect();
						cursor = conn.cursor();

						# Give player some initial slimes.
						slimes_initial = ewcfg.slimes_onrevive
						ewutils.setSlimesForPlayer(conn, cursor, message.author, slimes_initial)
						member_slime_pile.append({ 'member': message.author, 'slimes': slimes_initial })

						# Give some slimes to every living player (currently online)
						for member in message.server.members:
							if member.id != message.author.id and member.id != client.user.id:
								if ewcfg.role_corpse not in ewutils.getRoleMap(member.roles):
									member_slimes = ewutils.getSlimesForPlayer(conn, cursor, member) + ewcfg.slimes_onrevive_everyone
									ewutils.setSlimesForPlayer(conn, cursor, member, member_slimes)
									member_slime_pile.append({ 'member': member, 'slimes': member_slimes })

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile])
					await client.edit_message(resp, ':slime4: A geyser of fresh slime erupts, showering Rowdy, Killer, and Juvenile alike. :slime4: {} has been reborn in slime. :slime4:'.format(message.author.display_name))
				else:
					await client.edit_message(resp, 'You\'re not dead just yet.')

		# move from juvenile to one of the armies (rowdys or killers)
		elif cmd == ewcfg.cmd_enlist:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_juvenile in roles_map_user:
				faction = ""
				if tokens_count > 1:
					faction = tokens[1].lower()

				user_slimes = 0
				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();
					user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author)
				finally:
					cursor.close()
					conn.close()

				if user_slimes < ewcfg.slimes_toenlist:
					await client.edit_message(resp, "You need to mine more slime to rise above your lowly station. ({}/{})".format(user_slimes, ewcfg.slimes_toenlist))
				else:
					if faction == ewcfg.faction_rowdys:
						await client.replace_roles(message.author, roles_map[ewcfg.role_rowdyfuckers])
						await client.edit_message(resp, "Enlisted in the {}.".format(ewcfg.faction_rowdys))
					elif faction == ewcfg.faction_killers:
						await client.replace_roles(message.author, roles_map[ewcfg.role_copkillers])
						await client.edit_message(resp, "Enlisted in the {}.".format(ewcfg.faction_killers))
					else:
						await client.edit_message(resp, "Which faction? Say '{} {}' or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys))

			elif ewcfg.role_corpse in roles_map_user:
				await client.edit_message(resp, 'You are dead, bitch.')
			else:
				await client.edit_message(resp, "You can't do that right now, bitch.")

		# faction leader consumes the mentioned players of their own faction to absorb their slime count
		# kills the mentioned players
		elif cmd == ewcfg.cmd_devour:
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			is_copkiller = ewcfg.role_copkiller in roles_map_user
			is_rowdyfucker = ewcfg.role_rowdyfucker in roles_map_user

			if is_copkiller == False and is_rowdyfucker == False:
				await client.edit_message(resp, "Know your place.")
			else:
				if mentions_count == 0:
					await client.edit_message(resp, "Devour who?")
				else:
					members_devoured = []
					members_na = []

					try:
						conn = ewutils.databaseConnect();
						cursor = conn.cursor();
						user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author)

						# determine slime count for every member mentioned
						for member in mentions:
							roles_map_member = ewutils.getRoleMap(member.roles)

							if is_copkiller == True and ewcfg.role_copkillers in roles_map_member or is_rowdyfucker == True and ewcfg.role_rowdyfuckers in roles_map_member:
								# get slimes from the player
								slime_count = ewutils.getSlimesForPlayer(conn, cursor, member)
								user_slimes = user_slimes + slime_count

								# set player slimes to 0
								ewutils.setSlimesForPlayer(conn, cursor, member, 0)
								members_devoured.append(member)
							else:
								members_na.append(member)

						# add slime to rf/ck
						ewutils.setSlimesForPlayer(conn, cursor, message.author, user_slimes)

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
							await client.edit_message(resp, '{} has been devoured. ({} was not devoured.)'.format(names, ewutils.userListToNameString(members_na)))
						else:
							await client.edit_message(resp, '{} has been devoured.'.format(names))
					elif len(members_na) > 0:
						await client.edit_message(resp, '{} was not devoured.'.format(ewutils.userListToNameString(members_na)))
					else:
						await client.edit_message(resp, 'No one was devoured.')

		# gives slime to the miner (message.author)
		elif cmd == ewcfg.cmd_mine:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_corpse in roles_map_user:
				await client.send_message(message.channel, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive))
			else:
				if(message.channel.name == ewcfg.channel_mines):
					user_slimes = 0

					try:
						conn = ewutils.databaseConnect();
						cursor = conn.cursor();

						# Increment slimes for this user.
						user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author) + ewcfg.slimes_permine
						ewutils.setSlimesForPlayer(conn, cursor, message.author, user_slimes)

						conn.commit()
					finally:
						cursor.close()
						conn.close()
				else:
					await client.edit_message(resp, "You can't mine here. Try #{}.".format(ewcfg.channel_mines))

		# Show the current slime score of a player.
		elif cmd == ewcfg.cmd_score or cmd == ewcfg.cmd_score_alt1:
			if mentions_count == 0:
				user_slimes = 0
				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();
					user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author)
				finally:
					cursor.close()
					conn.close()

				# return my score
				await client.edit_message(resp, "Your slime score is {} :slime1:".format(user_slimes))
			else:
				member = mentions[0]
				user_slimes = 0
				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();
					user_slimes = ewutils.getSlimesForPlayer(conn, cursor, member)
				finally:
					cursor.close()
					conn.close()

				# return somebody's score
				await client.edit_message(resp, "{}'s slime score is {} :slime1:".format(member.display_name, user_slimes))

		# rowdy fucker and cop killer (leaders) can give slimes to anybody
		elif cmd == ewcfg.cmd_giveslime or cmd == ewcfg.cmd_giveslime_alt1:
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
				await client.edit_message(resp, "Only the Rowdy Fucker :rowdyfucker: and the Cop Killer :copkiller: can do that.")
			else:
				if mentions_count == 0:
					await client.edit_message(resp, "Give slimes to who?")
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
								conn = ewutils.databaseConnect();
								cursor = conn.cursor();
								user_slimes = ewutils.getSlimesForPlayer(conn, cursor, message.author)

								# determine slime count for every member mentioned
								for member in mentions:
									member_slimes.append({ 'member': member, 'slimes': (ewutils.getSlimesForPlayer(conn, cursor, member) + value) })
							finally:
								cursor.close()
								conn.close()

							if (value * mentions_count) > user_slimes:
								await client.edit_message(resp, "You don't have that much slime to give ({}/{}).".format(user_slimes, (value * mentions_count)))
							else:
								user_slimes = user_slimes - (value * mentions_count)

								try:
									conn = ewutils.databaseConnect();
									cursor = conn.cursor();

									ewutils.setSlimesForPlayer(conn, cursor, message.author, user_slimes)

									# give value slimes to mentioned players
									for obj in member_slimes:
										ewutils.setSlimesForPlayer(conn, cursor, obj['member'], obj['slimes'])

									conn.commit()
								finally:
									cursor.close()
									conn.close()

								await client.edit_message(resp, "Slime scores altered! :slime1:")
								
						else:
							await client.edit_message(resp, "Give how much slime?")


		# advertise help services
		elif cmd == ewcfg.cmd_help or cmd == ewcfg.cmd_help_alt1 or cmd == ewcfg.cmd_help_alt2:
			await client.edit_message(resp, 'Send me a DM for help.')

		# Debug command to override the role of a user
		elif debug == True and cmd == (ewcfg.cmd_prefix + 'setrole'):
			if mentions_count == 0:
				await client.edit_message(resp, 'Set who\'s role?')
			else:
				role_target = tokens[1]
				role = roles_map.get(role_target)

				if role != None:
					for user in mentions:
						await client.replace_roles(user, role)

					await client.edit_message(resp, 'Done.')
				else:
					await client.edit_message(resp, 'Unrecognized role.')

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
	print('Please place your API token in a file called "token", in the same directory as this script.')
	sys.exit(0)

# connect to discord and run indefinitely
client.run(token)
