"""
	Commands and utilities related to Juveniles.
"""
import time
import random

import ewcfg
import ewutils
import ewcmd
from ew import EwUser

# Map of user ID to a map of recent miss-mining time to count. If the count
# exceeds 3 in 5 seconds, you die.
last_mismined_times = {}

""" player enlists in a faction/gang """
async def enlist(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	response = ""
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

	if ewcfg.role_juvenile in roles_map_user:
		faction = ""
		if cmd.tokens_count > 1:
			faction = cmd.tokens[1].lower()

		user_data = EwUser(member = cmd.message.author)
		user_slimes = user_data.slimes
		user_is_pvp = (user_data.time_expirpvp > time_now)

		if user_slimes < ewcfg.slimes_toenlist:
			response = "You need to mine more slime to rise above your lowly station. ({}/{})".format(user_slimes, ewcfg.slimes_toenlist)
		else:
			if faction == ewcfg.faction_rowdys:
				if user_is_pvp:
					await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_rowdyfuckers], cmd.roles_map[ewcfg.role_rowdyfuckers_pvp])
				else:
					await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_rowdyfuckers])

				response = "Enlisted in the {}.".format(ewcfg.faction_rowdys)
			elif faction == ewcfg.faction_killers:
				if user_is_pvp:
					await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_copkillers], cmd.roles_map[ewcfg.role_copkillers_pvp])
				else:
					await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_copkillers])

				response = "Enlisted in the {}.".format(ewcfg.faction_killers)
			else:
				response = "Which faction? Say '{} {}' or '{} {}'.".format(ewcfg.cmd_enlist, ewcfg.faction_killers, ewcfg.cmd_enlist, ewcfg.faction_rowdys)

	elif ewcfg.role_corpse in roles_map_user:
		response = 'You are dead, bitch.'
	else:
		response = "You can't do that right now, bitch."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
	
""" Get to work, juvie. """
+async def toil(cmd):
+	resp = await ewcmd.start(cmd = cmd)
+	time_now = int(time.time())
+	
+	response = ""
+	
+	# A map of role names to Roles assigned to the current user.
+	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
+
+	# Get the user data from the database.
+	try:
+		conn = ewutils.databaseConnect()
+		cursor = conn.cursor()
+
+		user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)
+
+	finally:
+		cursor.close()
+		conn.close()
+
+	if ewcfg.role_corpse in roles_map_user:
+		# The dead can't toil.
+		response = "You lack a working body with which to perform backbreaking labor. Try {}.".format(ewcfg.cmd_revive)

	elif ewcfg.role_juvenile not in roles_map_user:
+		# The dead can't toil.
+		response = "Come on, you're better than that!."
+	
+	else:
+		user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp))
		# Add the PvP flag role.
		await ewutils.add_pvp_role(cmd = cmd)

	if response != ""
		# Send the response to the player.
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" mine for slime """
async def mine(cmd):
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
	time_now = int(time.time())

	if ewcfg.role_corpse in roles_map_user:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You can't mine while you're dead. Try {}.".format(ewcfg.cmd_revive)))
	elif ewcfg.role_juvenile_pvp not in roles_map_user:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You're still home in your pitiful cozy juvie house. Go and {} in the mines.".format(ewcfg.cmd_toil)))
	else:
		if(cmd.message.channel.name == ewcfg.channel_mines):
			user_data = EwUser(member = cmd.message.author)

			if user_data.stamina >= ewcfg.stamina_max:
				global last_mismined_times
				mismined = last_mismined_times.get(cmd.message.author.id)

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

				last_mismined_times[cmd.message.author.id] = mismined

				if mismined['count'] >= 5:
					# Death
					last_mismined_times[cmd.message.author.id] = None
					user_data.slimes = 0
					user_data.persist()

					await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You have died in a mining accident."))
					await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_corpse])
				else:
					await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You've exhausted yourself from mining. You'll need some refreshment before getting back to work."))
			else:
				# Determine if a poudrin is found.
				poudrin = False
				poudrinamount = 0
				poudrinchance = (random.randrange(3600) + 1)
				if poudrinchance == 3600:
					poudrin = True
					poudrinamount = (random.randrange(2) + 1)
					
				# Add mined slime to the user.
				user_data.slimes += (10 * (2 ** user_data.slimelevel))
				user_data.slimepoudrins += poudrinamount

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
				await ewutils.add_pvp_role(cmd = cmd)

				# Tell the player their slime level increased and/or a poudrin was found.
				if was_levelup or poudrin:
					response = ""

					if poudrin:
						if poudrinamount == 1:
							response += "You unearthed a slime poudrin! "
						elif poudrinamount == 2:
							response += "You unearthed two slime poudrins! "

						ewutils.logMsg('{} has found {} poudrin(s)!'.format(cmd.message.author.display_name, poudrinamount))

					if was_levelup:
						response += "You have been empowered by slime and are now a level {} slimeboi!".format(new_level)

					await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		else:
			# Mismined. Potentially kill the player for spamming the wrong channel.
			mismined = last_mismined_times.get(cmd.message.author.id)
			resp = await ewcmd.start(cmd = cmd)

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

			last_mismined_times[cmd.message.author.id] = mismined

			if mismined['count'] >= 3:
				# Death
				last_mismined_times[cmd.message.author.id] = None

				try:
					conn = ewutils.databaseConnect()
					cursor = conn.cursor()

					user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)
					user_data.slimes = 0
					user_data.persist(conn = conn, cursor = cursor)

					conn.commit()
				finally:
					cursor.close()
					conn.close()


				await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You have died in a mining accident."))
				await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_corpse])
			else:
				await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You can't mine here. Try #{}.".format(ewcfg.channel_mines)))
