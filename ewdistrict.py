"""
	district data model for database persistence
"""
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
		ewutils.execute_sql_query("REPLACE INTO districts({controlling_faction}, {capturing_faction}, {capture_progress}) VALUES({ctrl_f},{capt_f), {cp})".format(
			controlling_faction = ewcfg.col_controlling_faction,
			capturing_faction = ewcfg.col_capturing_faction,
			capture_progress = ewcfg.col_capture_progress,
			ctrl_f = self.controlling_faction,
			capt_f = self.capturing_faction,
			cp = self.capture_progress
		))


"""
	Updates/Increments the capture_progress values of all districts every time it's called
"""
def capture_tick(id_server):
	cursor = None
	conn_info = None

	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		# queries

		cursor.execute("SELECT {district}, {controlling_faction}, {capturing_faction} {capture_progress} FROM districts WHERE id_server = {id_server}".format(
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

		if len(all_districts) > 0:
			for x in range(len(all_districts)):
				district = all_districts[x]

				district_name = district[0]
				controlling_faction = district[1]
				capturing_faction = district[2]
				progress = district[3]

				faction_capture = None

				# checks if any players are in the district and if there are only players of the same faction, i.e. progress can happen
				for player in all_players:
					poi = player[0]
					faction = player[1]
					life_state = player[2]

					if poi == district_name and life_state == ewcfg.life_state_enlisted:  # if the player is in the district and a gang member
						if faction != controlling_faction:  # if the district isn't already controlled by the player's faction
							if faction_capture is not None and faction_capture != faction:  # if someone of the opposite faction is in the district
								faction_capture = 'both'  # standstill, gang violence has to happen
							else:  # if the district can be captured
								faction_capture = faction

				if faction_capture not in ['both', None]:
					dist = EwDistrict(id_server = id_server, district = district_name)

					if faction_capture == dist.capturing_faction:
						dist.capture_progress += 10
					else:
						dist.capture_progress -= 10

					if dist.capture_progress > 60:
						dist.controlling_faction = dist.capturing_faction
					# if progress < 0, swap which faction is in the process of capturing it and make the value positive again
					elif dist.capture_progress < 0:
						dist.capturing_faction = faction_capture
						dist.capture_progress -= dist.capture_progress

					dist.persist()



		conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

