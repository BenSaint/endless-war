import asyncio
import math

import ewcfg
import ewstats
import ewutils

"""
	district data model for database persistence
"""
class EwDistrict:
	id_server = ""

	# The district's identifying string
	name = ""

	# The faction currently controlling this district
	controlling_faction = ""

	# The faction currently capturing this district
	capturing_faction = ""

	# The amount of progress made on the capture
	capture_points = 0

	# The property class of the district
	property_class = ""

	# The amount of CP it takes for the district to be captured
	max_capture_points = 0

	def __init__(self, id_server = None, district = None):
		if id_server is not None and district is not None:
			self.id_server = id_server
			self.name = district

			# find the district's property class
			for poi in ewcfg.poi_list:
				if poi.id_poi == self.name:
					self.property_class = poi.property_class.lower()

			self.max_capture_points = ewcfg.max_capture_points[self.property_class]

			data = ewutils.execute_sql_query("SELECT {controlling_faction}, {capturing_faction}, {capture_points} FROM districts WHERE id_server = %s AND {district} = %s".format(
				controlling_faction = ewcfg.col_controlling_faction,
				capturing_faction = ewcfg.col_capturing_faction,
				capture_points = ewcfg.col_capture_points,
				district = ewcfg.col_district,
			), (
				id_server,
				district
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.controlling_faction = data[0][0]
				self.capturing_faction = data[0][1]
				self.capture_points = data[0][2]
				# ewutils.logMsg("EwDistrict object '" + self.name + "' created.  Controlling faction: " + self.controlling_faction + "; Capture progress: %d" % self.capture_points)
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO districts ({id_server}, {district}) VALUES (%s, %s)".format(
					id_server = ewcfg.col_id_server,
					district = ewcfg.col_district
				), (
					id_server,
					district
				))

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO districts(id_server, {district}, {controlling_faction}, {capturing_faction}, {capture_points}) VALUES(%s, %s, %s, %s, %s)".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_points = ewcfg.col_capture_points
		), (
			self.id_server,
			self.name,
			self.controlling_faction,
			self.capturing_faction,
			self.capture_points
		))

	async def decay_capture_points(self):
		if self.capture_points > 0:
			# reduces the capture progress at a rate with which it arrives at 0 after 1 in-game day
			# it's ceil() instead of int() because, with different values, the decay may be 0 that way
			await self.change_capture_points(-math.ceil(self.max_capture_points / ewcfg.ticks_per_day), ewcfg.actor_decay)

		if self.capture_points < 0:
			self.capture_points = 0

		if self.capture_points == 0:
			if self.controlling_faction != "":  # if it was owned by a faction
				await ewutils.post_in_channels(
					id_server = self.id_server,
					message = "The {faction} have lost control over {district} because of sheer negligence.".format(
						faction = self.controlling_faction,
						district = ewcfg.id_to_poi[self.name].str_name
					),
					channels = [ewcfg.id_to_poi[self.name].channel] + ewcfg.hideout_channels
				)
			await self.change_ownership("", ewcfg.actor_decay)
			self.capturing_faction = ""

		self.persist()

	async def change_capture_points(self, progress, actor):  # actor can either be a faction or "decay"
		progress_percent_before = int(self.capture_points / self.max_capture_points * 100)

		self.capture_points += progress

		# ensures that the value doesn't exceed the bounds
		if self.capture_points < 0:
			self.capture_points = 0
		elif self.capture_points > self.max_capture_points:
			self.capture_points = self.max_capture_points

		progress_percent_after = int(self.capture_points / self.max_capture_points * 100)

		# display a message if it's reached a certain amount
		if (progress_percent_after // ewcfg.capture_milestone) != (progress_percent_before // ewcfg.capture_milestone):  # if a progress milestone was reached
			if progress > 0:  # if it was a positive change
				if ewcfg.capture_milestone <= progress_percent_after < ewcfg.capture_milestone * 2:  # if its the first milestone
					await ewutils.post_in_channels(
						id_server = self.id_server,
						message = "{faction} have started capturing {district}. Current progress: {progress}%".format(
							faction = self.capturing_faction.capitalize(),
							district = ewcfg.id_to_poi[self.name].str_name,
							progress = progress_percent_after
						),
						channels = [ewcfg.id_to_poi[self.name].channel]
					)
				else:
					# alert both factions of significant capture progress
					if progress_percent_after >= 30 > progress_percent_before:  # if the milestone of 30% was just reached
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction} are capturing {district}.".format(
								faction = self.capturing_faction.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								progress = progress_percent_after
							),
							channels = ewcfg.hideout_channels
						)

					if self.controlling_faction != actor:  # if it's not already owned by that faction
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction} continue to capture {district}. Current progress: {progress}%".format(
								faction = self.capturing_faction.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								progress = progress_percent_after
							),
							channels = [ewcfg.id_to_poi[self.name].channel]
						)
					else:
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction} are renewing their grasp on {district}. Current control level: {progress}%".format(
								faction = self.capturing_faction.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								progress = progress_percent_after
							),
							channels = [ewcfg.id_to_poi[self.name].channel]
						)
			else:  # if it was a negative change
				if self.controlling_faction != "":  # if the district is owned by a faction
					if progress_percent_after < 20 <= progress_percent_before:
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction}' control of {district} is slipping.".format(
								faction = self.controlling_faction.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								progress = progress_percent_after
							),
							channels = ewcfg.hideout_channels
						)

					elif progress_percent_after < 50 <= progress_percent_before and actor != ewcfg.actor_decay:
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction} are de-capturing {district}.".format(
								faction = actor.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								progress = progress_percent_after
							),
							channels = ewcfg.hideout_channels
						)

					await ewutils.post_in_channels(
						id_server = self.id_server,
						message = "{faction}' control of {district} has decreased. Remaining control level: {progress}%".format(
							faction = self.capturing_faction.capitalize(),
							district = ewcfg.id_to_poi[self.name].str_name,
							progress = progress_percent_after
						),
						channels = [ewcfg.id_to_poi[self.name].channel]
					)
				else:  # if it's an uncontrolled district
					await ewutils.post_in_channels(
						id_server = self.id_server,
						message = "{faction}' capture progress of {district} has decreased. Remaining progress: {progress}%".format(
							faction = self.capturing_faction.capitalize(),
							district = ewcfg.id_to_poi[self.name].str_name,
							progress = progress_percent_after
						),
						channels = [ewcfg.id_to_poi[self.name].channel]
					)

		# if capture_points is at its maximum value (or above), assign the district to the capturing faction
		if self.capture_points == self.max_capture_points and self.controlling_faction != actor:
			await self.change_ownership(self.capturing_faction, actor)

		# if the district has decayed or been de-captured and it wasn't neutral anyway, make it neutral
		elif self.capture_points == 0 and self.controlling_faction != "":
			await self.change_ownership("", actor)

	"""
		Change who controls the district. Can be used to update the channel topic by passing the already controlling faction as an arg.
	"""
	async def change_ownership(self, new_owner, actor, client = None):  # actor can either be a faction, "decay", or "init"
		factions = ["", ewcfg.faction_killers, ewcfg.faction_rowdys]

		if new_owner in factions:
			server = ewcfg.server_list[self.id_server]
			channel_str = ewcfg.id_to_poi[self.name].channel
			channel = ewutils.get_channel(server = server, channel_name = channel_str)

			if channel is not None and channel.topic:  # tests if the topic is neither None nor empty
				initialized = False

				# initialize channel topic control statuses
				for faction in factions:
					if ewcfg.control_topics[faction] in channel.topic:
						initialized = True

				if not initialized:
					new_topic = channel.topic + " " + ewcfg.control_topics[new_owner]

				# replace the the string of the previously controlling faction with that of the new one.
				else:
					new_topic = channel.topic.replace(ewcfg.control_topics[self.controlling_faction], ewcfg.control_topics[new_owner])

				if client is None:
					client = ewutils.get_client()

				if client is not None:
					await client.edit_channel(channel = channel, topic = new_topic)

			if self.controlling_faction != new_owner:  # if the controlling faction actually changed
				if new_owner != "":  # if it was captured by a faction instead of being de-captured or decayed
					await ewutils.post_in_channels(
						id_server = self.id_server,
						message = "{faction} just captured {district}.".format(
							faction = self.capturing_faction.capitalize(),
							district = ewcfg.id_to_poi[self.name].str_name
						),
						channels = [ewcfg.id_to_poi[self.name].channel] + ewcfg.hideout_channels
					)
				else:  # successful de-capture or full decay
					if actor != ewcfg.actor_decay:
						await ewutils.post_in_channels(
							id_server = self.id_server,
							message = "{faction} just wrested control over {district} from the {other_faction}.".format(
								faction = actor.capitalize(),
								district = ewcfg.id_to_poi[self.name].str_name,
								other_faction = self.controlling_faction  # the faction that just lost control
							),
							channels = [ewcfg.id_to_poi[self.name].channel] + ewcfg.hideout_channels
						)

				self.controlling_faction = new_owner
				self.persist()


"""
	Updates/Increments the capture_points values of all districts every time it's called
"""
async def capture_tick(id_server):
	# the variables might apparently be accessed before assignment if i didn't declare them here
	cursor = None
	conn_info = None

	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		cursor.execute("SELECT {district}, {controlling_faction}, {capturing_faction}, {capture_points} FROM districts WHERE id_server = %s".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_points = ewcfg.col_capture_points
		), (
			id_server,
		))

		all_districts = cursor.fetchall()

		cursor.execute("SELECT {poi}, {faction}, {life_state}, {id_user} FROM users WHERE id_server = %s".format(
			poi = ewcfg.col_poi,
			faction = ewcfg.col_faction,
			life_state = ewcfg.col_life_state,
			id_user = ewcfg.col_id_user
		), (
			id_server,
		))

		all_players = cursor.fetchall()

		if len(all_districts) > 0:  # if all_districts isn't empty
			for d in range(len(all_districts)):  # iterate through all districts
				district = all_districts[d]

				district_name = district[0]
				controlling_faction = district[1]

				# the faction that's actively capturing the district this tick
				# if no players are present, it's None, if only players of one faction (ignoring juvies and ghosts) are,
				# it's the faction's name, i.e. 'rowdys' or 'killers', and if both are present, it's 'both'
				faction_capture = None

				# how much progress will be made. is higher the more people of one faction are in a district, and is 0 if both teams are present
				capture_speed = 0

				dc_stat_increase_list = []

				# checks if any players are in the district and if there are only players of the same faction, i.e. progress can happen
				for player in all_players:
					# player[0] is their poi, player[2] their life_state. assigning them to variables might hurt the server's performance
					if player[0] == district_name and player[2] == ewcfg.life_state_enlisted:  # if the player is in the district and a gang member
						faction = player[1]

						if faction_capture is not None and faction_capture != faction:  # if someone of the opposite faction is in the district
							faction_capture = 'both'  # standstill, gang violence has to happen
							capture_speed = 0
							dc_stat_increase_list.clear()

						elif faction_capture in [None, faction]:  # if the district isn't already controlled by the player's faction and the capture isn't halted by an enemy
							faction_capture = faction
							capture_speed += 1
							dc_stat_increase_list.append(player[3])  # player[3] is their id

				if faction_capture not in ['both', None]:  # if only members of one faction is present
					dist = EwDistrict(id_server = id_server, district = district_name)

					if dist.capture_points < dist.max_capture_points:
						for stat_recipient in dc_stat_increase_list:
							ewstats.change_stat(
								id_server = id_server,
								id_user = stat_recipient,
								metric = ewcfg.stat_capture_points_contributed,
								n = ewcfg.capture_tick_length * capture_speed
							)

					if faction_capture == dist.capturing_faction:  # if the faction is already in the process of capturing, continue
						await dist.change_capture_points(ewcfg.capture_tick_length * capture_speed, faction_capture)

					elif dist.capture_points == 0 and dist.controlling_faction == "":  # if it's neutral, start the capture
						await dist.change_capture_points(ewcfg.capture_tick_length * capture_speed, faction_capture)
						dist.capturing_faction = faction_capture

					# lower the enemy faction's progress to revert it to neutral (or potentially get it onto your side without becoming neutral first)
					else:  # if the (de-)capturing faction is not in control
						await dist.change_capture_points(-(ewcfg.capture_tick_length * capture_speed * ewcfg.decapture_speed_multiplier), faction_capture)

					dist.persist()

		conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

	return

"""
	Coroutine that continually calls capture_tick; is called once per server, and not just once globally
"""
async def capture_tick_loop(id_server):
	interval = ewcfg.capture_tick_length
	# causes a capture tick to happen exactly every 10 seconds (the "elapsed" thing might be unnecessary, depending on how long capture_tick ends up taking on average)
	while True:
		await capture_tick(id_server = id_server)
		# ewutils.logMsg("Capture tick happened on server %s." % id_server + " Timestamp: %d" % int(time.time()))

		await asyncio.sleep(interval)

"""
	Gives both kingpins the appropriate amount of slime for how many districts they own and lowers the capture_points property of each district by a certain amount, turning them neutral after a while
"""
async def give_kingpins_slime_and_decay_capture_points(id_server):
	for kingpin_role in [ewcfg.role_rowdyfucker, ewcfg.role_copkiller]:
		kingpin = ewutils.find_kingpin(id_server = id_server, kingpin_role = kingpin_role)

		if kingpin is not None:
			slimegain = 0

			for id_district in ewcfg.capturable_districts:
				district = EwDistrict(id_server = id_server, district = id_district)

				# if the kingpin is controlling this district
				if district.controlling_faction == (ewcfg.faction_killers if kingpin.faction == ewcfg.faction_killers else ewcfg.faction_rowdys):

					# give the kingpin slime based on the district's property class
					slimegain += ewcfg.district_control_slime_yields[district.property_class]

				await district.decay_capture_points()

			kingpin.change_slimes(n = slimegain)
			kingpin.persist()
			ewutils.logMsg(kingpin_role + " just received %d" % slimegain + " slime for their captured districts.")
