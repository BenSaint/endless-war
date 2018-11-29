"""
	district data model for database persistence
"""
import asyncio
import math

import ewcfg
import ewutils


class EwDistrict:
	id_server = ""
	name = ""
	controlling_faction = ""
	capturing_faction = ""
	capture_progress = 0

	def __init__(self, id_server = None, district = None):
		if id_server is not None and district is not None:
			self.id_server = id_server
			self.name = district

			data = ewutils.execute_sql_query("SELECT {controlling_faction}, {capturing_faction}, {capture_progress} FROM districts WHERE id_server = %s AND {district} = %s".format(
				controlling_faction = ewcfg.col_controlling_faction,
				capturing_faction = ewcfg.col_capturing_faction,
				capture_progress = ewcfg.col_capture_progress,
				district = ewcfg.col_district,
			), (
				id_server,
				district
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.controlling_faction = data[0][0]
				self.capturing_faction = data[0][1]
				self.capture_progress = data[0][2]
				# ewutils.logMsg("EwDistrict object '" + self.name + "' created.  Controlling faction: " + self.controlling_faction + "; Capture progress: %d" % self.capture_progress)
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO districts ({id_server}, {district}) VALUES (%s, %s)".format(
					id_server = ewcfg.col_id_server,
					district = ewcfg.col_district
				), (
					id_server,
					district
				))

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO districts(id_server, {district}, {controlling_faction}, {capturing_faction}, {capture_progress}) VALUES(%s, %s, %s, %s, %s)".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_progress = ewcfg.col_capture_progress
		), (
			self.id_server,
			self.name,
			self.controlling_faction,
			self.capturing_faction,
			self.capture_progress
		))

	def decay_capture_progress(self, property_class):
		max_capture_progress = {
			ewcfg.property_class_s: ewcfg.max_capture_progress_s,
			ewcfg.property_class_a: ewcfg.max_capture_progress_a,
			ewcfg.property_class_b: ewcfg.max_capture_progress_b,
			ewcfg.property_class_c: ewcfg.max_capture_progress_c
		}

		if property_class in max_capture_progress:
			if self.capture_progress > 0:
				# reduces the capture progress at a rate with which it arrives at 0 after 1 in-game day
				# it's ceil() instead of int() because, with different values, the decay may be 0 that way
				self.capture_progress -= math.ceil(max_capture_progress[property_class] / ewcfg.ticks_per_day)

			if self.capture_progress < 0:
				self.capture_progress = 0

			if self.capture_progress == 0:
				self.controlling_faction = ""
				self.capturing_faction = ""


"""
	Updates/Increments the capture_progress values of all districts every time it's called
"""
async def capture_tick(id_server):
	# the variables might apparently be accessed before assignment if i didn't declare them here
	cursor = None
	conn_info = None

	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		cursor.execute("SELECT {district}, {controlling_faction}, {capturing_faction}, {capture_progress} FROM districts WHERE id_server = %s".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_progress = ewcfg.col_capture_progress
		), (
			id_server,
		))

		all_districts = cursor.fetchall()

		cursor.execute("SELECT {poi}, {faction}, {life_state} FROM users WHERE id_server = %s".format(
			poi = ewcfg.col_poi,
			faction = ewcfg.col_faction,
			life_state = ewcfg.col_life_state
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

				# checks if any players are in the district and if there are only players of the same faction, i.e. progress can happen
				for player in all_players:
					# player[0] is their poi, player[2] their life_state. assigning them to variables might hurt the server's performance
					if player[0] == district_name and player[2] == ewcfg.life_state_enlisted:  # if the player is in the district and a gang member
						faction = player[1]

						if faction_capture is not None and faction_capture != faction:  # if someone of the opposite faction is in the district
							faction_capture = 'both'  # standstill, gang violence has to happen
							capture_speed = 0

						elif faction_capture in [None, faction]:  # if the district isn't already controlled by the player's faction and the capture isn't halted by an enemy
							faction_capture = faction
							capture_speed += 1

				if faction_capture not in ['both', None]:  # if only members of one faction is present
					dist = EwDistrict(id_server = id_server, district = district_name)
					property_class = ""
					max_capture_progress = 0

					# find the district's property class
					for poi in ewcfg.poi_list:
						if poi.id_poi == dist.name:
							property_class = poi.property_class.lower()

					# capture time is different based on the property class
					if property_class == ewcfg.property_class_s:
						max_capture_progress = ewcfg.max_capture_progress_s
					elif property_class == ewcfg.property_class_a:
						max_capture_progress = ewcfg.max_capture_progress_a
					elif property_class == ewcfg.property_class_b:
						max_capture_progress = ewcfg.max_capture_progress_b
					elif property_class == ewcfg.property_class_c:
						max_capture_progress = ewcfg.max_capture_progress_c

					if faction_capture == dist.capturing_faction:  # if the faction is already in the process of capturing, continue
						if dist.capture_progress < max_capture_progress:  # stop at maximum progress
							dist.capture_progress += ewcfg.capture_tick_length * capture_speed

					elif dist.capture_progress == 0 and dist.controlling_faction == "":  # if it's neutral, start the capture
						dist.capture_progress += ewcfg.capture_tick_length * capture_speed
						dist.capturing_faction = faction_capture

					else:  # lower the enemy faction's progress to revert it to neutral (or potentially get it onto your side without becoming neutral first)
						dist.capture_progress -= ewcfg.capture_tick_length * capture_speed * ewcfg.decapture_speed_multiplier

					# if capture_progress is at its maximum value (or above), assign the district to the capturing faction
					if dist.capture_progress >= max_capture_progress:
						dist.controlling_faction = dist.capturing_faction

					# if progress < 0, swap which faction is in the process of capturing it and make the value positive again
					elif dist.capture_progress < 0:
						dist.capturing_faction = faction_capture
						dist.capture_progress -= dist.capture_progress
					# if progress is exactly 0, the district returns to being neutral
					elif dist.capture_progress == 0:
						dist.capturing_faction = ""
						dist.controlling_faction = ""

					# # if the opposing faction successfully de-captures a district, it belongs to them now
					# elif dist.capture_progress <= 0:
					# 	dist.capturing_faction = faction_capture
					# 	dist.capture_progress = max_capture_progress
					# 	dist.controlling_faction = faction_capture

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
	Gives both kingpins the appropriate amount of slime for how many districts they own and lowers the capture_progress property of each district by a certain amount, turning them neutral after a while
"""
def give_kingpins_slime_and_decay_capture_progress(id_server):
	for kingpin_role in [ewcfg.role_rowdyfucker, ewcfg.role_copkiller]:
		kingpin = ewutils.find_kingpin(id_server = id_server, kingpin_role = kingpin_role)

		if kingpin is not None:
			slimegain = 0

			for id_district in ewcfg.capturable_districts:
				district = EwDistrict(id_server = id_server, district = id_district)
				property_class = ""

				# if the kingpin is controlling this district
				if district.controlling_faction == (ewcfg.faction_killers if kingpin.faction == ewcfg.faction_killers else ewcfg.faction_rowdys):
					# find the district's property class
					for poi in ewcfg.poi_list:
						if poi.id_poi == id_district:
							property_class = poi.property_class.lower()

					# give the kingpin slime based on the district's property class
					if property_class == ewcfg.property_class_s:
						slimegain += ewcfg.slime_yield_class_s
					elif property_class == ewcfg.property_class_a:
						slimegain += ewcfg.slime_yield_class_a
					elif property_class == ewcfg.property_class_b:
						slimegain += ewcfg.slime_yield_class_b
					elif property_class == ewcfg.property_class_c:
						slimegain += ewcfg.slime_yield_class_c

				district.decay_capture_progress(property_class)

			kingpin.change_slimes(n = slimegain)
			kingpin.persist()
			ewutils.logMsg(kingpin_role + " just received %d" % slimegain + " slime for their captured districts.")
