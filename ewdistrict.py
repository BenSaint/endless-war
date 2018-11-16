"""
	district data model for database persistence
"""
import asyncio
import time

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

			data = ewutils.execute_sql_query("SELECT {controlling_faction}, {capturing_faction}, {capture_progress} FROM districts WHERE id_server = {id_server} AND {district_col} = '{district}'".format(
				controlling_faction = ewcfg.col_controlling_faction,
				capturing_faction = ewcfg.col_capturing_faction,
				capture_progress = ewcfg.col_capture_progress,
				id_server = id_server,
				district_col = ewcfg.col_district,
				district = district
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.controlling_faction = data[0][0]
				self.capturing_faction = data[0][1]
				self.capture_progress = data[0][2]
				# ewutils.logMsg("EwDistrict object '" + self.name + "' created.  Controlling faction: " + self.controlling_faction + "; Capture progress: %d" % self.capture_progress)
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO districts ({id_server}, {district}) VALUES ({id}, '{dist}')".format(
					id_server = ewcfg.col_id_server,
					district = ewcfg.col_district,
					id = id_server,
					dist = district
				))

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO districts(id_server, {district}, {controlling_faction}, {capturing_faction}, {capture_progress}) VALUES({id_server}, '{dist}', '{ctrl_f}', '{capt_f}', {cp})".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_progress = ewcfg.col_capture_progress,
			id_server = self.id_server,
			dist = self.name,
			ctrl_f = self.controlling_faction,
			capt_f = self.capturing_faction,
			cp = self.capture_progress
		))


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

		cursor.execute("SELECT {district}, {controlling_faction}, {capturing_faction}, {capture_progress} FROM districts WHERE id_server = {id_server}".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_progress = ewcfg.col_capture_progress,
			id_server = id_server
		))

		all_districts = cursor.fetchall()

		cursor.execute("SELECT {poi}, {faction}, {life_state} FROM users WHERE id_server = {id_server} AND poi != 'thesewers'".format(  # saves some time, a lot of inactive players are in sewers
			poi = ewcfg.col_poi,
			faction = ewcfg.col_faction,
			life_state = ewcfg.col_life_state,
			id_server = id_server
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

				# checks if any players are in the district and if there are only players of the same faction, i.e. progress can happen
				for player in all_players:
					# player[0] is their poi, player[2] their life_state. assigning them to variables might hurt the server's performance
					if player[0] == district_name and player[2] == ewcfg.life_state_enlisted:  # if the player is in the district and a gang member
						faction = player[1]

						if faction_capture is not None and faction_capture != faction:  # if someone of the opposite faction is in the district
							faction_capture = 'both'  # standstill, gang violence has to happen

						elif faction_capture is None:  # if the district isn't already controlled by the player's faction and the capture isn't halted by an enemy
							faction_capture = faction

				if faction_capture not in ['both', None]:  # if only members of one faction is present
					dist = EwDistrict(id_server = id_server, district = district_name)

					if faction_capture == dist.capturing_faction:  # if the faction is already in the process of capturing, continue
						if dist.capture_progress < ewcfg.max_capture_progress:  # stop at maximum progress
							dist.capture_progress += ewcfg.capture_progress_per_tick

					elif dist.capture_progress == 0 and dist.controlling_faction == "":  # if it's neutral, start the capture
						dist.capture_progress += ewcfg.capture_progress_per_tick
						dist.capturing_faction = faction_capture

					else:  # lower the enemy faction's progress to revert it to neutral (or potentially get it onto your side without becoming neutral first)
						dist.capture_progress -= ewcfg.capture_progress_per_tick

					# if capture_progress is at its maximum value (or above), assign the district to the capturing faction
					if dist.capture_progress >= ewcfg.max_capture_progress:
						dist.controlling_faction = dist.capturing_faction
					# if progress < 0, swap which faction is in the process of capturing it and make the value positive again
					elif dist.capture_progress < 0:
						dist.capturing_faction = faction_capture
						dist.capture_progress -= dist.capture_progress
					# if progress is exactly 0, the district returns to being neutral
					elif dist.capture_progress == 0:
						dist.capturing_faction = ""
						dist.controlling_faction = ""

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
async def call_capture_tick(id_server, interval = 10):
	# causes a capture tick to happen exactly every 10 seconds (the "elapsed" thing might be unnecessary, depending on how long capture_tick ends up taking on average)
	while True:
		await capture_tick(id_server = id_server)
		ewutils.logMsg("Capture tick happened on server %s." % id_server + " Timestamp: %d" % int(time.time()))
		await asyncio.sleep(interval)
