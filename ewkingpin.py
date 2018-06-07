"""
	Commands for kingpins only.
"""
import ewcmd
import ewutils
import ewcfg
from ew import EwUser

""" consume a player to gain all of their slime """
async def devour(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
	is_copkiller = ewcfg.role_copkiller in roles_map_user
	is_rowdyfucker = ewcfg.role_rowdyfucker in roles_map_user

	if is_copkiller == False and is_rowdyfucker == False:
		response = "Know your place."
	else:
		if cmd.mentions_count == 0:
			response = "Devour who?"
		else:
			members_devoured = []
			members_na = []

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)

				# determine slime count for every member mentioned
				for member in cmd.mentions:
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

			role_corpse = cmd.roles_map[ewcfg.role_corpse]
			for member in members_devoured:
				# update slime counts
				try:
					# set roles to corpse for mentioned players
					await cmd.client.replace_roles(member, role_corpse)
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
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))


""" Give any player any amount of slime from your own stash. """
async def giveslime(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""

	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
	if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
		response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
	else:
		if cmd.mentions_count == 0:
			response = "Give slimes to who?"
		else:
			if cmd.tokens_count > 1:
				value = None
				for token in cmd.tokens[1:]:
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

						user_data = EwUser(member=cmd.message.author, conn=conn, cursor=cursor)

						# determine slime count for every member mentioned
						for member in cmd.mentions:
							member_slimes.append(EwUser(member=member, conn=conn, cursor=cursor))
					finally:
						cursor.close()
						conn.close()

					if (value * cmd.mentions_count) > user_data.slimes:
						response = "You don't have that much slime to give ({:,}/{:,}).".format(user_data.slimes, (value * cmd.mentions_count))
					else:
						user_data.slimes -= (value * cmd.mentions_count)

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
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" Destroy a megaslime of your own for lore reasons. """
async def deadmega(cmd):
	resp = await ewcmd.start(cmd = cmd)
	response = ""
	roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

	if (ewcfg.role_copkiller not in roles_map_user) and (ewcfg.role_rowdyfucker not in roles_map_user):
		response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
	else:
		value = 1000000
		user_slimes = 0
		user_data = EwUser(member=cmd.message.author)

		if value > user_data.slimes:
			response = "You don't have that much slime to lose ({:,}/{:,}).".format(user_data.slimes, value)
		else:
			user_data.slimes -= value
			user_data.persist()
			response = "Alas, poor megaslime. You have {:,} slime remaining.".format(user_data.slimes)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
