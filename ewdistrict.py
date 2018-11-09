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
				district = district
			))

			if data is not None:
				self.controlling_faction = data[0][0]
				self.capture_progress = data[0][1]
				ewutils.logMsg("EwDistrict" + self.name + " created.  Controlling faction: " + self.controlling_faction + "; Capture progress: " + self.capture_progress)
			else:  # create new entry
				ewutils.execute_sql_query("REPLACE INTO districts (id_server, district) VALUES ({}, {})".format(
					id_server,
					district
				))



def capture_tick():
	i = 0