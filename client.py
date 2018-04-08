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
						users_unkilled = []
						users_killed = []

						# Attempt to kill each mentioned player.
						for member in mentions:
							roles_map_target = ewutils.getRoleMap(member.roles)
							if (user_iskillers and ewcfg.role_rowdyfuckers in roles_map_target) or (user_isrowdys and ewcfg.role_copkillers in roles_map_target) or (ewcfg.role_juvenile in roles_map_target):
								await client.replace_roles(member, role_corpse)
								users_killed.append(member)
							else:
								users_unkilled.append(member)

						users_killed_count = len(users_killed)
						if users_killed_count > 0:
							try:
								conn = ewutils.databaseConnect();
								cursor = conn.cursor();

								# Subtract slimes for the kill count.
								ewutils.setSlimesForPlayer(conn, cursor, message.author, (user_slimes - (users_killed_count * ewcfg.slimes_tokill)))

								# Remove all slimes from the other players.
								# TODO
							finally:
								cursor.close()
								conn.close()

							# Present a nice list of killed player names.
							names = ewutils.userListToNameString(users_killed)
							if len(users_unkilled) > 0:
								await client.edit_message(resp, 'Killed {}! (But you can\'t kill {}.)'.format(names, ewutils.userListToNameString(users_unkilled)))
							else:
								await client.edit_message(resp, 'Killed {}!'.format(names))
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
				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();

					# Give player some initial slimes.
					ewutils.setSlimesForPlayer(conn, cursor, message.author, ewcfg.slimes_onrevive)

					conn.commit()
				finally:
					cursor.close()
					conn.close()

				# Update score on user's nickname.
				try:
					await client.change_nickname(message.author, ewutils.getNickWithSlimes(message.author, ewcfg.slimes_onrevive))
				except:
					pass

				await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile])
				await client.edit_message(resp, 'Revived {}!'.format(message.author.display_name))
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
