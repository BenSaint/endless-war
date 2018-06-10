"""
	Commands and utilities related to dead players.
"""
import time

import ewcmd
import ewcfg
import ewutils
from ew import EwUser, EwMarket

""" revive yourself from the dead. """
async def revive(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	response = ""

	if cmd.message.channel.name != ewcfg.channel_endlesswar and cmd.message.channel.name != ewcfg.channel_sewers:
		response = "Come to me. I hunger. #{}.".format(ewcfg.channel_sewers)
	else:
		roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

		if ewcfg.role_corpse in roles_map_user:
			player_is_pvp = False

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				player_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)
				market_data = EwMarket(id_server = cmd.message.server.id, conn = conn, cursor = cursor)

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
				ewutils.weaponskills_clear(member = cmd.message.author, conn = conn, cursor = cursor)

				# Set time of last revive. This used to provied spawn protection, but currently isn't used.
				player_data.time_lastrevive = time_now

				if(player_data.time_expirpvp > time_now):
					player_is_pvp = True

				# Set initial slime level. It's probably 2.
				player_data.slimelevel = len(str(player_data.slimes))

				player_data.persist(conn = conn, cursor = cursor)
				market_data.persist(conn = conn, cursor = cursor)

				# Give some slimes to every living player (currently online)
				for member in cmd.message.server.members:
					if member.id != cmd.message.author.id and member.id != cmd.client.user.id:
						if ewcfg.role_corpse not in ewutils.getRoleMap(member.roles):
							member_data = EwUser(member = member, conn = conn, cursor = cursor)
							member_data.slimes += ewcfg.slimes_onrevive_everyone
							member_data.persist(conn = conn, cursor = cursor)

				# Commit all transactions at once.
				conn.commit()
			finally:
				cursor.close()
				conn.close()

			if player_is_pvp:
				await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_juvenile], cmd.roles_map[ewcfg.role_juvenile_pvp])
			else:
				await cmd.client.replace_roles(cmd.message.author, cmd.roles_map[ewcfg.role_juvenile])

			response = '{slime4} A geyser of fresh slime erupts, showering Rowdy, Killer, and Juvenile alike. {slime4} {name} has been reborn in slime. {slime4}'.format(slime4 = ewcfg.emote_slime4, name = cmd.message.author.display_name)
		else:
			response = 'You\'re not dead just yet.'

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" leave your corpse and haunt NLACakaNM as a ghost """
async def disembody(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	
	response = ""
	
	# A map of role names to Roles assigned to the current user.
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

	# Get the user data from the database.
	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)

	finally:
		cursor.close()
		conn.close()

	if ewcfg.role_corpse not in roles_map_user:
		# Only dead players can haunt.
		response = "You're trapped in your disgusting, living body. Try {}.".format(ewcfg.cmd_suicide)
		
	elif user_data.slime >= 0:
		# You need Antislime to haunt.
		response = "You've lost all your antislime. Nothing to do now but !revive."
	
	else:
		user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp))
		
		# Add the PvP flag role.
		await ewutils.add_pvp_role(cmd = cmd)

		# Persist changes to the database.
		try:
			conn = ewutils.databaseConnect()
			cursor = conn.cursor()

			user_data.persist(conn = conn, cursor = cursor)

			conn.commit()
		finally:
			cursor.close()
			conn.close()

	if response != ""
		# Send the response to the player.
		await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" haunt living players to steal slime and convert it to antislime """
async def haunt(cmd):
	resp = await ewcmd.start(cmd = cmd)
	time_now = int(time.time())
	response = ""
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
	
	
	elif cmd.mentions_count > 1:
		response = "You can only spook one person at a time. Who do you think you are, the Lord of Ghosts?"
	elif cmd.mentions_count == 1:
		# A map of role names to Roles assigned to the current user.
		roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

		# Get the user and target data from the database.
		try:
			conn = ewutils.databaseConnect()
			cursor = conn.cursor()

			user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)

			member = cmd.mentions[0]
			haunted_data = EwUser(member = member, conn = conn, cursor = cursor)
		finally:
			cursor.close()
			conn.close()

		# A map of role names to Roles assigned to the targeted user.
		roles_map_target = ewutils.getRoleMap(member.roles)

		if ewcfg.role_corpse not in roles_map_user:
			# Only dead players can haunt.
			response = "You can't haunt while alive. Try {}.".format(ewcfg.cmd_suicide)
		elif ewcfg.role_corpse_pvp not in roles_map_user:
			# Only disembodies ghosts can haunt.
			response = "You'll need to leave your dead body behind first. Try {}.".format(ewcfg.cmd_disembody)
		elif cmd.message.channel.name != ewcfg.channel_sewers:
			# Allowed only in the combat zone.
			response = "You must go to the #{} to haunt the living.".format(ewcfg.channel_combatzone)
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
			hauntmax = int(10 ** (user_data.slimelevel - 2))
			haunted_slimes = int(haunted_data.slimes / ewcfg.slimes_hauntratio)
			
			if haunted_slimes > hauntmax:
				haunted_slimes = hauntmax

			haunted_data.slimes -= haunted_slimes
			haunted_data.totaldamage += haunted_slimes
			user_data.slimes -= haunted_slimes
			user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp))
			user_data.time_lasthaunt = time_now

			# Persist changes to the database.
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data.persist(conn = conn, cursor = cursor)
				haunted_data.persist(conn = conn, cursor = cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()
				
			# Add the PvP flag role.
			await ewutils.add_pvp_role(cmd = cmd)

			response = "{} has been haunted by the ghost of {}! Slime has been lost!".format(member.display_name, message.author.display_name)
		else:
			# Some condition we didn't think of.
			response = "You cannot haunt {}.".format(member.display_name)
	else:
		# No mentions, or mentions we didn't understand.
		response = "Your spookiness is appreciated, but ENDLESS WAR didn\'t understand that name."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

async def negaslime(cmd):
	resp = await ewcmd.start(cmd = cmd)
	negaslime = 0

	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		# Count all negative slime currently possessed by dead players.
		cursor.execute("SELECT sum({}) FROM users WHERE id_server = %s AND {} < 0".format(
			ewcfg.col_slimes,
			ewcfg.col_slimes
		), (cmd.message.server.id, ))

		result = cursor.fetchone();

		if result != None:
			negaslime = result[0]

			if negaslime == None:
				negaslime = 0
				
		# Add persisted negative slime.
		market_data = EwMarket(id_server = cmd.message.server.id, conn = conn, cursor = cursor)
		negaslime += market_data.negaslime

	finally:
		cursor.close()
		conn.close()

	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "The dead have amassed {:,} negative slime.".format(negaslime)))
