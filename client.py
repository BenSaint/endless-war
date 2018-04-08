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

	""" Wake up when we see a message start with pound. """
	if message.content.startswith('#'):
		# let the user know we're working on it
		resp = await client.send_message(message.channel, '...')

		# tokenize the message. the command should be the first word.
		tokens = message.content.split(' ')
		tokens_count = len(tokens)
		cmd = tokens[0].lower()

		# remove mentions to us
		mentions = list(filter(lambda user : user.id != client.user.id, message.mentions))

		# common data we'll need
		roles_map = ewutils.getRoleMap(message.server.roles)
		mentions_count = len(mentions)

		# process command words
		if cmd == ewcfg.cmd_kill:
			if mentions_count > 0:
				# The roles assigned to the author of this user.
				roles_map_user = ewutils.getRoleMap(message.author.roles)

				try:
					conn = ewutils.databaseConnect();
					cursor = conn.cursor();

					cursor.execute("SELECT slimes FROM users WHERE id_user = %s AND id_server = %s", [message.author.id, message.author.server.id])
					result = cursor.fetchone();

					user_slimes = 0
					if result == None:
						cursor.execute("REPLACE INTO users(id_user, id_server) VALUES(%s, %s)", [message.author.id, message.author.server.id])
						conn.commit();
					else:
						user_slimes = result[0]

					# FIXME debug
					print('user {} ({}/{}) has {} slimes.'.format(message.author.display_name, message.author.id, message.author.server.id, user_slimes))

					# TODO check that the user has enough slime for all the KILLS

					user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
					user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

					if user_iskillers == False and user_isrowdys == False:
						await client.edit_message(resp, "Nice try, loser.")
					else:
						role_corpse = roles_map[ewcfg.role_corpse]
						users_killed = []

						for member in mentions:
							roles_map_target = ewutils.getRoleMap(member.roles)
							if (user_iskillers and ewcfg.role_rowdyfuckers in roles_map_target) or (user_isrowdys and ewcfg.role_copkillers in roles_map_target):
								await client.replace_roles(member, role_corpse)
								users_killed.append(member)
							else:
								# FIXME debug
								print("couldn't kill {}".format(member.display_name))

						if len(users_killed) > 0:
							names = ewutils.userListToNameString(users_killed)
							await client.edit_message(resp, 'Killed {}!'.format(names))
						else:
							await client.edit_message(resp, "Didn't kill anybody.")
				finally:
					cursor.close()
					conn.close()
			else:
				await client.edit_message(resp, 'Okay tough guy, who are you killing?')

		# revive yourself as a juvenile after having been killed.
		elif cmd == ewcfg.cmd_revive:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_corpse in roles_map_user:
				await client.replace_roles(message.author, roles_map[ewcfg.role_juvenile])
				await client.edit_message(resp, 'Revived {}!'.format(message.author.display_name))
			else:
				await client.edit_message(resp, 'You\'re not dead.')

		# move from juvenile to one of the armies (rowdys or killers)
		elif cmd == ewcfg.cmd_enlist:
			roles_map_user = ewutils.getRoleMap(message.author.roles)

			if ewcfg.role_juvenile in roles_map_user:
				faction = ""

				# TODO check that the user has enough slime to enlist

				if tokens_count > 1:
					faction = tokens[1].lower()

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

		# gives +5 slime to the miner (message.author)
		elif cmd == ewcfg.cmd_mine:

			# TODO mine cmd

			# FIXME debug
			await client.edit_message(resp, "You can't do that right now.")

		# Debug command to override the role of a user
		elif cmd == '#setrole':
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
