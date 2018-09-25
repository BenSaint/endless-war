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
import re
import os


import ewutils
import ewcfg
import ewcmd
import ewcasino
import ewfood
import ewwep
import ewjuviecmd
import ewmarket
import ewspooky
import ewkingpin
import ewplayer
import ewserver
import ewitem
import ewmap
import ewrolemgr
import ewraidboss

from ewitem import EwItem
from ew import EwUser, EwMarket

ewutils.logMsg('Starting up...')

client = discord.Client()

# A map containing user IDs and the last time in UTC seconds since we sent them
# the help doc via DM. This is to prevent spamming.
last_helped_times = {}

# Map of server ID to a map of active users on that server.
active_users_map = {}

# Map of all command words in the game to their implementing function.
cmd_map = {
	# Attack another player
	ewcfg.cmd_kill: ewwep.attack,
	ewcfg.cmd_shoot: ewwep.attack,
	ewcfg.cmd_attack: ewwep.attack,

	# Choose your weapon
	ewcfg.cmd_equip: ewwep.equip,

	# Kill yourself
	ewcfg.cmd_suicide: ewwep.suicide,

	# Spar with an ally
	ewcfg.cmd_spar: ewwep.spar,

	# Name your current weapon.
	ewcfg.cmd_annoint: ewwep.annoint,


	# move from juvenile to one of the armies (rowdys or killers)
	ewcfg.cmd_enlist: ewjuviecmd.enlist,

	# gives slime to the miner (message.author)
	ewcfg.cmd_mine: ewjuviecmd.mine,

	# Show the current slime score of a player.
	ewcfg.cmd_score: ewcmd.score,
	ewcfg.cmd_score_alt1: ewcmd.score,

	# Show a player's combat data.
	ewcfg.cmd_data: ewcmd.data,

	#check what time it is, and the weather
	ewcfg.cmd_time: ewcmd.weather,
	ewcfg.cmd_clock: ewcmd.weather,
	ewcfg.cmd_weather: ewcmd.weather,


	# Show the total of negative slime in the world.
	#ewcfg.cmd_negaslime: ewspooky.negaslime,

	# revive yourself as a juvenile after having been killed.
	ewcfg.cmd_revive: ewspooky.revive,

	# Ghosts can haunt enlisted players to reduce their slime score.
	ewcfg.cmd_haunt: ewspooky.haunt,


	# Play slime pachinko!
	ewcfg.cmd_slimepachinko: ewcasino.pachinko,

	# Toss the dice at slime craps!
	ewcfg.cmd_slimecraps: ewcasino.craps,

	# Pull the lever on a slot machine!
	ewcfg.cmd_slimeslots: ewcasino.slots,

	# Play slime roulette!
	ewcfg.cmd_slimeroulette: ewcasino.roulette,


	# See what's for sale in the Food Court.
	ewcfg.cmd_menu: ewfood.menu,

	# Order refreshing food and drinks!
	ewcfg.cmd_order: ewfood.order,


	# Transfer slime between players. Shares a cooldown with investments.
	ewcfg.cmd_transfer: ewmarket.xfer,
	ewcfg.cmd_transfer_alt1: ewmarket.xfer,

	# Show the player's slime credit.
	ewcfg.cmd_slimecredit: ewmarket.slimecoin,
	ewcfg.cmd_slimecredit_alt1: ewmarket.slimecoin,

	# Donate your slime to SlimeCorp in exchange for SlimeCoin.
	ewcfg.cmd_donate: ewmarket.donate,


	# show player inventory
	ewcfg.cmd_inventory: ewitem.inventory_print,
	ewcfg.cmd_inventory_alt1: ewitem.inventory_print,
	ewcfg.cmd_inventory_alt2: ewitem.inventory_print,
	ewcfg.cmd_inventory_alt3: ewitem.inventory_print,

	# get an item's description
	ewcfg.cmd_inspect: ewitem.item_look,

	# use an item
	ewcfg.cmd_use: ewitem.item_use,


	# Remove a megaslime (1 mil slime) from a general.
	ewcfg.cmd_deadmega: ewkingpin.deadmega,

	# Release a player from their faction.
	ewcfg.cmd_pardon: ewkingpin.pardon,


	# Navigate the world map.
	ewcfg.cmd_move: ewmap.move,
	ewcfg.cmd_move_alt1: ewmap.move,
	ewcfg.cmd_move_alt2: ewmap.move,

	# Look around the POI you find yourself in.
	ewcfg.cmd_look: ewmap.look,

	# link to the world map
	ewcfg.cmd_map: ewcmd.map,

	# kill all players in your district; could be re-used for a future raid boss
	#ewcfg.cmd_writhe: ewraidboss.writhe,

	# Misc
	ewcfg.cmd_howl: ewcmd.cmd_howl,
	ewcfg.cmd_howl_alt1: ewcmd.cmd_howl,
	ewcfg.cmd_harvest: ewcmd.harvest,
	ewcfg.cmd_news: ewcmd.patchnotes,
	ewcfg.cmd_patchnotes: ewcmd.patchnotes,
	ewcfg.cmd_wiki: ewcmd.wiki,
	ewcfg.cmd_booru: ewcmd.booru,
	#ewcfg.cmd_help: ewcmd.help,
	#ewcfg.cmd_help_alt1: ewcmd.help,
	#ewcfg.cmd_help_alt2: ewcmd.help
}

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

	ewutils.logMsg("Loaded NLACakaNM world map. ({}x{})".format(ewmap.map_width, ewmap.map_height))
	ewmap.map_draw()

	# Flatten role names to all lowercase, no spaces.
	for poi in ewcfg.poi_list:
		if poi.role != None:
			poi.role = ewutils.mapRoleName(poi.role)

	await client.change_presence(game = discord.Game(name = ("dev. by @krak " + ewcfg.version)))

	# Look for a Twitch client_id on disk.
	# FIXME debug - temporarily disable Twitch integration
	if False: 
		twitch_client_id = ewutils.getTwitchClientId()

	# If no twitch client ID is available, twitch integration will be disabled.
	# FIXME debug - temporarily disable Twitch integration.
	if True:
		twich_client_id = None
		ewutils.logMsg('Twitch integration disabled.')
	elif twitch_client_id == None or len(twitch_client_id) == 0:
		ewutils.logMsg('No twitch_client_id file found. Twitch integration disabled.')
	else:
		ewutils.logMsg("Enabled Twitch integration.")

	# Channels in the connected discord servers to announce to.
	channels_announcement = []

	# Channels in the connected discord servers to send stock market updates to. Map of server ID to channel.
	channels_stockmarket = {}

	for server in client.servers:
		# Update server data in the database
		ewserver.server_update(server = server)

		# Grep around for channels
		ewutils.logMsg("connected to server: {}".format(server.name))
		for channel in server.channels:
			if(channel.type == discord.ChannelType.text):
				if(channel.name == ewcfg.channel_twitch_announcement):
					channels_announcement.append(channel)
					ewutils.logMsg("• found channel for announcements: {}".format(channel.name))

				elif(channel.name == ewcfg.channel_stockexchange):
					channels_stockmarket[server.id] = channel
					ewutils.logMsg("• found channel for stock exchange: {}".format(channel.name))

	try:
		ewutils.logMsg('Creating message queue directory.')
		os.mkdir(ewcfg.dir_msgqueue)
	except FileExistsError:
		ewutils.logMsg('Message queue directory already exists.')

	ewutils.logMsg('Ready.')


	"""
		Set up for infinite loop to perform periodic tasks.
	"""
	time_now = int(time.time())

	time_last_twitch = time_now
	time_twitch_downed = 0

	# Every three hours we log a message saying the periodic task hook is still active. On startup, we want this to happen within about 60 seconds, and then on the normal 3 hour interval.
	time_last_logged = time_now - ewcfg.update_hookstillactive + 60

	stream_live = None

	ewutils.logMsg('Beginning periodic hook loop.')
	while True:
		time_now = int(time.time())

		# Periodic message to log that this stuff is still running.
		if (time_now - time_last_logged) >= ewcfg.update_hookstillactive:
			time_last_logged = time_now

			ewutils.logMsg("Periodic hook still active.")

		# Check to see if a stream is live via the Twitch API.
		# FIXME disabled
		if False:
		#if twitch_client_id != None and (time_now - time_last_twitch) >= ewcfg.update_twitch:
			time_last_twitch = time_now

			try:
				# Twitch API call to see if there are any active streams.
				json_string = ""
				p = subprocess.Popen(
					"curl -H 'Client-ID: {}' -X GET 'https://api.twitch.tv/helix/streams?user_login = rowdyfrickerscopkillers' 2>/dev/null".format(twitch_client_id), 
					shell = True,
					stdout = subprocess.PIPE
				)

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
				ewutils.logMsg('Twitch handler hit an exception (continuing): {}'.format(json_string))
				traceback.print_exc(file = sys.stdout)

		# Adjust the exchange rate of slime for the market.
		try:
			for server in client.servers:
				# Load market data from the database.
				market_data = EwMarket(id_server = server.id)

				if market_data.time_lasttick + ewcfg.update_market <= time_now:
					market_data.time_lasttick = time_now

					# Advance the time and potentially change weather.
					market_data.clock += 1

					if market_data.clock >= 24 or market_data.clock < 0:
						market_data.clock = 0

					if random.randrange(30) == 0:
						pattern_count = len(ewcfg.weather_list)

						if pattern_count > 1:
							weather_old = market_data.weather

							# Randomly select a new weather pattern. Try again if we get the same one we currently have.
							while market_data.weather == weather_old:
								pick = random.randrange(len(ewcfg.weather_list))
								market_data.weather = ewcfg.weather_list[pick].name

						# Log message for statistics tracking.
						ewutils.logMsg("The weather changed. It's now {}.".format(market_data.weather))

					# Persist new data.
					market_data.persist()

					# Decay slime totals
					ewutils.decaySlimes(id_server = server.id)

					# Increase hunger for all players below the max.
					ewutils.pushupServerHunger(id_server = server.id)

					# Decrease inebriation for all players above min (0).
					ewutils.pushdownServerInebriation(id_server = server.id)

		except:
			ewutils.logMsg('An error occurred in the scheduled slime market update task:')
			traceback.print_exc(file = sys.stdout)

		# Parse files dumped into the msgqueue directory and send messages as needed.
		try:
			for msg_file in os.listdir(ewcfg.dir_msgqueue):
				fname = "{}/{}".format(ewcfg.dir_msgqueue, msg_file)

				msg = ewutils.readMessage(fname)
				os.remove(fname)

				msg_channel_names = []
				msg_channel_names_reverb = []

				if msg.channel != None:
					msg_channel_names.append(msg.channel)

				if msg.poi != None:
					poi = ewcfg.id_to_poi.get(msg.poi)
					if poi != None:
						if poi.channel != None and len(poi.channel) > 0:
							msg_channel_names.append(poi.channel)

						if msg.reverb == True:
							pois_adjacent = ewmap.path_to(poi_start = msg.poi)

							for poi_adjacent in pois_adjacent:
								if poi_adjacent.channel != None and len(poi_adjacent.channel) > 0:
									msg_channel_names_reverb.append(poi_adjacent.channel)

				if len(msg_channel_names) == 0:
					ewutils.logMsg('in file {} message for channel {} (reverb {})\n{}'.format(msg_file, msg.channel, msg.reverb, msg.message))
				else:
					# Send messages to every connected server.
					for server in client.servers:
						for channel in server.channels:
							if channel.name in msg_channel_names:
								await client.send_message(channel, "**{}**".format(msg.message))
							elif channel.name in msg_channel_names_reverb:
								await client.send_message(channel, "**Something is happening nearby...\n\n{}**".format(msg.message))
		except:
			ewutils.logMsg('An error occurred while trying to process the message queue:')
			traceback.print_exc(file = sys.stdout)

		# Wait a while before running periodic tasks.
		await asyncio.sleep(15)

@client.event
async def on_member_join(member):
	ewutils.logMsg("New member \"{}\" joined. Configuring default roles now.".format(member.display_name))
	await ewrolemgr.updateRoles(client = client, member = member)

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

	if message.server != None:
		# Note that the user posted a message.
		active_map = active_users_map.get(message.server.id)
		if active_map == None:
			active_map = {}
			active_users_map[message.server.id] = active_map
		active_map[message.author.id] = True

		# Update player information.
		ewplayer.player_update(
			member = message.author,
			server = message.server
		)

	content_tolower = message.content.lower()
	re_awoo = re.compile('.*![a]+[w]+o[o]+.*')

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

		# remove mentions to us
		mentions = list(filter(lambda user : user.id != client.user.id, message.mentions))
		mentions_count = len(mentions)

		# Create command object
		cmd_obj = ewcmd.EwCmd(
			tokens = tokens,
			message = message,
			client = client,
			mentions = mentions
		)

		"""
			Handle direct messages.
		"""
		if message.server == None:
			# Direct message the player their inventory.
			if ewitem.cmd_is_inventory(cmd):
				return await ewitem.inventory_print(cmd_obj)
			elif cmd == ewcfg.cmd_inspect:
				return await ewitem.item_look(cmd_obj)

			# FIXME add this back when the help doc is updated.
			"""
			else:
				time_last = last_helped_times.get(message.author.id, 0)

				# Only send the help doc once every thirty seconds. There's no need to spam it.
				if (time_now - time_last) > 30:
					last_helped_times[message.author.id] = time_now
					await client.send_message(message.channel, 'Check out the guide for help: https://ew.krakissi.net/guide/')
			"""

			# Nothing else to do in a DM.
			return

		# assign the appropriate roles to a user with less than @everyone, faction, location
		if len(message.author.roles) < 3:
			return await ewrolemgr.updateRoles(client = client, member = message.author)

		# Scold/ignore offline players.
		if message.author.status == discord.Status.offline:

			response = "You cannot participate in the ENDLESS WAR while offline."

			await client.send_message(message.channel, ewutils.formatMessage(message.author, response))

			return

		# Check the main command map for the requested command.
		global cmd_map
		cmd_fn = cmd_map.get(cmd)

		if cmd_fn != None:
			# Execute found command
			return await cmd_fn(cmd_obj)

		# FIXME debug
		# Test item creation
		elif debug == True and cmd == '!create':
			item_id = ewitem.item_create(
				item_type = 'medal',
				id_user = message.author.id,
				id_server = message.server.id,
				item_props = {
					'medal_name': 'Test Award',
					'medal_desc': '**{medal_name}**: *Awarded to Krak by Krak for testing shit.*'
				}
			)

			ewutils.logMsg('Created item: {}'.format(item_id))
			item = EwItem(id_item = item_id)
			item.item_props['test'] = 'meow'
			item.persist()

			item = EwItem(id_item = item_id)

			await client.send_message(message.channel, ewutils.formatMessage(message.author, ewitem.item_look(item)))

		# FIXME debug
		# Test item deletion
		elif debug == True and cmd == '!delete':
			items = ewitem.inventory(
				id_user = message.author.id,
				id_server = message.server.id
			)

			for item in items:
				ewitem.item_delete(
					id_item = item.get('id_item')
				)

			await client.send_message(message.channel, ewutils.formatMessage(message.author, 'ok'))

		# AWOOOOO
		elif re_awoo.match(cmd):
			return await ewcmd.cmd_howl(cmd_obj)

		# Debug command to override the role of a user
		elif debug == True and cmd == (ewcfg.cmd_prefix + 'setrole'):

			response = ""

			if mentions_count == 0:
				response = 'Set who\'s role?'
			else:
				roles_map = ewutils.getRoleMap(message.server.roles)
				role_target = tokens[1]
				role = roles_map.get(role_target)

				if role != None:
					for user in mentions:
						await client.replace_roles(user, role)

					response = 'Done.'
				else:
					response = 'Unrecognized role.'

			await client.send_message(cmd.message.channel, ewutils.formatMessage(message.author, response))

		# didn't match any of the command words.
		else:
			resp = await ewcmd.start(cmd = cmd_obj)

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

	elif content_tolower.find(ewcfg.cmd_howl) >= 0 or content_tolower.find(ewcfg.cmd_howl_alt1) >= 0 or re_awoo.match(content_tolower):
		""" Howl if !howl is in the message at all. """
		return await ewcmd.cmd_howl(ewcmd.EwCmd(
			message = message,
			client = client
		))

# find our REST API token
token = ewutils.getToken()

if token == None or len(token) == 0:
	ewutils.logMsg('Please place your API token in a file called "token", in the same directory as this script.')
	sys.exit(0)

# connect to discord and run indefinitely
client.run(token)
