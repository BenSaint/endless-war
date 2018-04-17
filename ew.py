import ewutils
import ewcfg

# Database columns
col_id_user = 'id_user'
col_id_server = 'id_server'
col_slimes = 'slimes'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_expirpvp = 'time_expirpvp'
col_time_lasthaunt = 'time_lasthaunt'

""" User model for database persistence """
class EwUser:
	id_user = ""
	id_server = ""
	id_killer = ""

	slimes = 0

	time_lastkill = 0
	time_lastrevive = 0
	time_lastspar = 0
	time_expirpvp = 0
	time_lasthaunt = 0

	""" Create a new EwUser and optionally retrieve it from the database. """
	def __init__(self, member=None, conn=None, cursor=None):
		# Retrieve the object from the database if the user is provided.
		if(member != None):
			self.id_server = member.server.id
			self.id_user = member.id

			our_cursor = False
			our_conn = False

			try:
				# Get database handles if they weren't passed.
				if(cursor == None):
					if(conn == None):
						conn = ewutils.databaseConnect()
						our_conn = True

					cursor = conn.cursor();
					our_cursor = True

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {} FROM users WHERE id_user = %s AND id_server = %s".format(
					col_slimes,
					col_time_lastkill,
					col_time_lastrevive,
					col_id_killer,
					col_time_lastspar,
					col_time_expirpvp,
					col_time_lasthaunt
				), (
					member.id,
					member.server.id
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.slimes = result[0]
					self.time_lastkill = result[1]
					self.time_lastrevive = result[2]
					self.id_killer = result[3]
					self.time_lastspar = result[4]
					self.time_expirpvp = result[5]
					self.time_lasthaunt = result[6]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO users(id_user, id_server) VALUES(%s, %s)", (member.id, member.server.id))
					
					conn.commit()

			finally:
				# Clean up the database handles.
				if(our_cursor):
					cursor.close()
				if(our_conn):
					conn.close()

	""" Save this user object to the database. """
	def persist(self, conn=None, cursor=None):
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = ewutils.databaseConnect()
					our_conn = True

				cursor = conn.cursor();
				our_cursor = True

			# Save the object.
			cursor.execute("REPLACE INTO users({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				col_id_user,
				col_id_server,
				col_slimes,
				col_time_lastkill,
				col_time_lastrevive,
				col_id_killer,
				col_time_lastspar,
				col_time_expirpvp,
				col_time_lasthaunt
			), (
				self.id_user,
				self.id_server,
				self.slimes,
				self.time_lastkill,
				self.time_lastrevive,
				self.id_killer,
				self.time_lastspar,
				self.time_expirpvp,
				self.time_lasthaunt
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()
