"""
	Commands and utilities related to dead players.
"""
import time

import ewcmd
import ewcfg
import ewutils
import ewmap
import ewrolemgr
from ew import EwUser, EwMarket

""" revive yourself from the dead. """
async def revive(cmd):
	time_now = int(time.time())
	response = ""

	if cmd.message.channel.name != ewcfg.channel_endlesswar and cmd.message.channel.name != ewcfg.channel_sewers:
		response = "Come to me. I hunger. #{}.".format(ewcfg.channel_sewers)
	else:
		player_data = EwUser(member = cmd.message.author)

		if player_data.life_state == ewcfg.life_state_corpse:
			market_data = EwMarket(id_server = cmd.message.server.id)

			# Endless War collects his fee.
			fee = (player_data.slimecredit / 10)
			player_data.slimecredit -= fee
			market_data.slimes_revivefee += fee
			
			# Preserve negaslime
			if player_data.slimes < 0:
				market_data.negaslime += player_data.slimes
				player_data.change_slimes(n = -player_data.slimes) # set to 0

			# Give player some initial slimes.
			player_data.slimelevel = 0
			player_data.change_slimes(n = ewcfg.slimes_onrevive)

			# Set time of last revive. This used to provied spawn protection, but currently isn't used.
			player_data.time_lastrevive = time_now

			# Set life state. This is what determines whether the player is actually alive.
			player_data.life_state = ewcfg.life_state_juvenile

			# Get the player out of the sewers. Will be endless-war eventually.
			player_data.poi = ewcfg.poi_id_downtown

			player_data.persist()
			market_data.persist()

			# Give some slimes to every living player (currently online)
			for member in cmd.message.server.members:
				if member.id != cmd.message.author.id and member.id != cmd.client.user.id:
					member_data = EwUser(member = member)

					if member_data.life_state != ewcfg.life_state_corpse and member_data.life_state != ewcfg.life_state_grandfoe:
						member_data.change_slimes(n = ewcfg.slimes_onrevive_everyone)
						member_data.persist()

			await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

			response = '{slime4} A geyser of fresh slime erupts, showering Rowdy, Killer, and Juvenile alike. {slime4} {name} has been reborn in slime. {slime4}'.format(slime4 = ewcfg.emote_slime4, name = cmd.message.author.display_name)
		else:
			response = 'You\'re not dead just yet.'

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


""" haunt living players to steal slime """
async def haunt(cmd):
	time_now = int(time.time())
	response = ""

	if cmd.mentions_count > 1:
		response = "You can only spook one person at a time. Who do you think you are, the Lord of Ghosts?"
	elif cmd.mentions_count == 1:
		# Get the user and target data from the database.
		user_data = EwUser(member = cmd.message.author)

		member = cmd.mentions[0]
		haunted_data = EwUser(member = member)

		if user_data.life_state != ewcfg.life_state_corpse:
			# Only dead players can haunt.
			response = "You can't haunt now. Try {}.".format(ewcfg.cmd_suicide)
		elif user_data.busted:
			response = "You can't haunt while you're busted."
		elif haunted_data.life_state == ewcfg.life_state_kingpin:
			# Disallow haunting of generals.
			response = "He is too far from the sewers in his ivory tower, and thus cannot be haunted."
		elif (time_now - user_data.time_lasthaunt) < ewcfg.cd_haunt:
			# Disallow haunting if the user has haunted too recently.
			response = "You're being a little TOO spooky lately, don't you think?"
		elif ewmap.poi_is_pvp(haunted_data.poi) == False:
			# Require the target to be flagged for PvP
			response = "{} is not mired in the ENDLESS WAR right now.".format(member.display_name)
		elif haunted_data.life_state == ewcfg.life_state_corpse:
			# Dead players can't be haunted.
			response = "{} is already dead.".format(member.display_name)
		elif haunted_data.life_state == ewcfg.life_state_grandfoe:
			# Grand foes can't be haunted.
			response = "{} is invulnerable to ghosts.".format(member.display_name)
		elif haunted_data.life_state == ewcfg.life_state_enlisted or haunted_data.life_state == ewcfg.life_state_juvenile:
			# Target can be haunted by the player.
			haunted_slimes = int(haunted_data.slimes / ewcfg.slimes_hauntratio)
			if user_data.poi == haunted_data.poi:  # when haunting someone face to face, there is no cap and you get double the amount
				haunted_slimes *= 2
			elif haunted_slimes > ewcfg.slimes_hauntmax:
				haunted_slimes = ewcfg.slimes_hauntmax

			if -user_data.slimes < haunted_slimes:  # cap on for how much you can haunt
				haunted_slimes = -user_data.slimes

			haunted_data.change_slimes(n = -haunted_slimes)
			user_data.change_slimes(n = -haunted_slimes)
			user_data.time_lasthaunt = time_now

			# Persist changes to the database.
			user_data.persist()
			haunted_data.persist()

			response = "{} has been haunted by the ghost of {}! Slime has been lost!".format(member.display_name, cmd.message.author.display_name)
		else:
			# Some condition we didn't think of.
			response = "You cannot haunt {}.".format(member.display_name)
	else:
		# No mentions, or mentions we didn't understand.
		response = "Your spookiness is appreciated, but ENDLESS WAR didn\'t understand that name."

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def negaslime(cmd):
	negaslime = 0

	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
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
	finally:
		cursor.close()
		ewutils.databaseClose(conn_info)

	# Add persisted negative slime.
	market_data = EwMarket(id_server = cmd.message.server.id)
	negaslime += market_data.negaslime

	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "The dead have amassed {:,} negative slime.".format(negaslime)))
