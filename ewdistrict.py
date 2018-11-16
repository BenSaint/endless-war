"""
	district data model for database persistence
"""
import ewcfg
import ewutils


class EwDistrict:
	id_server = ""
	name = ""
	controlling_faction = ""
	capture_progress = 0

	def __init__(self, id_server = None, district = None):
		if id_server is not None and district is not None:
			self.id_server = id_server
			self.name = district

			data = ewutils.execute_sql_query("SELECT {controlling_faction}, {capture_progress} FROM districts WHERE id_server = {id_server} AND {district_col} = {district}".format(
				controlling_faction = ewcfg.col_controlling_faction,
				capture_progress = ewcfg.col_capture_progress,
				id_server = id_server,
				district_col = ewcfg.col_district,
				district = "'%s'" % district
			))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.controlling_faction = data[0][0]
				self.capture_progress = data[0][1]
				# ewutils.logMsg("EwDistrict object '" + self.name + "' created.  Controlling faction: " + self.controlling_faction + "; Capture progress: %d" % self.capture_progress)
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO districts ({id_server}, {district}) VALUES ({id}, {dist})".format(
					id_server = ewcfg.col_id_server,
					district = ewcfg.col_district,
					id = id_server,
					dist = "'%s'" % district
				))

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO districts({controlling_faction}, {capture_progress}) VALUES({cf}, {cp})".format(
			controlling_faction = ewcfg.col_controlling_faction,
			capture_progress = ewcfg.col_capture_progress,
			cf = self.controlling_faction,
			cp = self.capture_progress
		))

	def increase_caputure_progress(self):
		# if player in district
		self.capture_progress += ewcfg.capture_progress_per_tick

def capture_tick(self):
	pass
