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

import ewutils
import ewcfg

print('Starting up...')

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as {} ({}).'.format(client.user.name, client.user.id))
	print('Ready.')

@client.event
async def on_message(message):
	""" Ignore DMs """
	if message.server == None:
		return

	""" Wake up when we see a message start with a bang. """
	if message.content.startswith(ewcfg.cmd_prefix):
		# tokenize the message. the command should be the first word.
		tokens = message.content.split(' ')
		tokens_count = len(tokens)
		cmd = tokens[0].lower()

		# remove mentions to us
		mentions = list(filter(lambda user : user.id != client.user.id, message.mentions))

		# common data we'll need
		roles_map = ewutils.getRoleMap(message.server.roles)
		mentions_count = len(mentions)

		# let the user know we're working on it
		if cmd != ewcfg.cmd_mine or message.channel.name != ewcfg.channel_mines:
			resp = await client.send_message(message.channel, '...')

		# process command words
		if cmd == ewcfg.cmd_kill:
			if mentions_count > 0:
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
					await client.edit_message(resp, "You don't have enough slimes! ({}/{})".format(user_slimes, mentions_count * ewcfg.slimes_tokill))
				else:
					user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
					user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

					# Only killers, rowdys, the cop killer, and the rowdy fucker can kill people
					if user_iskillers == False and user_isrowdys == False:
						await client.edit_message(resp, "Nice try, loser.")
					else:
						role_corpse = roles_map[ewcfg.role_corpse]
						juveniles_killed = []
						users_unkilled = []
						users_killed = []

						# Attempt to kill each mentioned player.
						for member in mentions:
							roles_map_target = ewutils.getRoleMap(member.roles)
							if (user_iskillers and ewcfg.role_rowdyfuckers in roles_map_target) or (user_isrowdys and ewcfg.role_copkillers in roles_map_target) or (ewcfg.role_juvenile in roles_map_target):
								if ewcfg.role_juvenile in roles_map_target:
									juveniles_killed.append(member)

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

								# Set the new slime value for the player.
								ewutils.setSlimesForPlayer(conn, cursor, message.author, user_slimes)

								# Remove all slimes from the other players.
								for member in users_killed:
									ewutils.setSlimesForPlayer(conn, cursor, member, 0)

								conn.commit()
							finally:
								cursor.close()
								conn.close()

							# Present a nice list of killed player names.
							names = ewutils.userListToNameString(users_killed)
							if len(users_unkilled) > 0:
								await client.edit_message(resp, 'Killed {}! (But you can\'t kill {}.)'.format(names, ewutils.userListToNameString(users_unkilled)))
							else:
								await client.edit_message(resp, 'Killed {}!'.format(names))

							# Try to show the new slime count on the killing player.
							try:
								await client.change_nickname(message.author, ewutils.getNickWithSlimes(message.author, user_slimes))
							except:
								pass
						else:
							if len(users_unkilled) > 0:
								await client.edit_message(resp, 'You can\'t kill {}.'.format(ewutils.userListToNameString(users_unkilled)))
							else:
								await client.edit_message(resp, "Didn't kill anybody.")
			else:
				await client.edit_message(resp, 'Okay tough guy, who are you killing?')

		# revive yourself as a juvenile after having been killed.
		elif cmd == ewcfg.cmd_revive:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_corpse in roles_map_user:
				# List of maps of member and slime count.
				member_slime_pile = []

				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();

					# Give player some initial slimes.
					ewutils.setSlimesForPlayer(conn, cursor, message.author, ewcfg.slimes_onrevive)
					member_slime_pile.append({ 'member': message.author, 'slimes': ewcfg.slimes_onrevive })

					for member in message.server.members:
						if member.id != message.author.id:
							member_slimes = ewutils.getSlimesForPlayer(conn, cursor, member) + ewcfg.slimes_onrevive_everyone
							ewutils.setSlimesForPlayer(conn, cursor, member, member_slimes)
							member_slime_pile.append({ 'member': member, 'slimes': member_slimes })

					conn.commit()
				finally:
					cursor.close()
					conn.close()

				await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile])
				await client.edit_message(resp, 'Revived {}!'.format(message.author.display_name))

				# Update score on user's nickname.
				for obj in member_slime_pile:
					try:
						await client.change_nickname(obj['member'], ewutils.getNickWithSlimes(obj['member'], obj['slimes']))
					except:
						pass
			else:
				await client.edit_message(resp, 'You\'re not dead.')

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
					await client.edit_message(resp, "You don't have enough slime ({}/{}).".format(user_slimes, ewcfg.slimes_toenlist))
				else:
					if faction == ewcfg.faction_rowdys:
						await client.replace_roles(message.author, roles_map[ewcfg.role_rowdyfuckers])
						await client.edit_message(resp, "Joined {}!".format(ewcfg.faction_rowdys))
					elif faction == ewcfg.faction_killers:
						await client.replace_roles(message.author, roles_map[ewcfg.role_copkillers])
						await client.edit_message(resp, "Joined {}!".format(ewcfg.faction_killers))
					else:
						await client.edit_message(resp, "Which faction? Say '{} {}' or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys))

			elif ewcfg.role_corpse in roles_map_user:
				await client.edit_message(resp, 'You are dead.')
			else:
				await client.edit_message(resp, "You can't do that right now.")

		# faction leader consumes the mentioned players of their own faction to absorb their slime count
		# kills the mentioned players
		elif cmd == ewcfg.cmd_devour:

			# TODO devour cmd

			# FIXME debug
			await client.edit_message(resp, "You can't do that right now.")

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

					# Update score on user's nickname.
					try:
						await client.change_nickname(message.author, ewutils.getNickWithSlimes(message.author, user_slimes))
					except:
						pass
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
				await client.edit_message(resp, "Your slime score is {}.".format(user_slimes))
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
				await client.edit_message(resp, "{}'s slime score is {}.".format(member.display_name, user_slimes))

		# rowdy fucker and cop killer (leaders) can give slimes to anybody
		elif cmd == ewcfg.cmd_giveslime or cmd == ewcfg.cmd_giveslime_alt1:
			roles_map_user = ewutils.getRoleMap(message.author.roles)
			if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
				await client.edit_message(resp, "Only the Rowdy Fucker or Cop Killer can do that.")
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
								await client.edit_message(resp, "You don't have enough slimes ({}/{}).".format(user_slimes, (value * mentions_count)))
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

								await client.edit_message(resp, "Slime scores altered!")
								
								# update nicknames for all members
								for obj in member_slimes:
									try:
										await client.change_nickname(obj['member'], ewutils.getNickWithSlimes(obj['member'], obj['slimes']))
									except:
										pass
								try:
									await client.change_nickname(message.author, ewutils.getNickWithSlimes(message.author, user_slimes))
								except:
									pass
						else:
							await client.edit_message(resp, "Give how many slimes?")

		# Debug command to override the role of a user
		elif cmd == '!setrole':
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
			msg_mistake = "oh, sorry"
			if randint == 2:
				msg_mistake = "whoops"
			elif randint == 3:
				msg_mistake = "nevermind"

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
