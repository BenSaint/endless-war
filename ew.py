import ewutils
import ewcfg

# Common database columns
col_id_server = 'id_server'

# Database columns for users
col_id_user = 'id_user'
col_slimes = 'slimes'
col_slimelevel = 'slimelevel'
col_slimecredit = 'slimecredit'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_expirpvp = 'time_expirpvp'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'

# Database columns for markets
col_rate_market = 'rate_market'
col_rate_exchange = 'rate_exchange'
col_slimes_casino = 'slimes_casino'

""" Market data model for database persistence """
class EwMarket:
	id_server = ""

	slimes_casino = 0

	rate_market = 1000
	rate_exchange = 1000

	""" Load the market data for this server from the database. """
	def __init__(self, id_server=None, conn=None, cursor=None):
		if(id_server != None):
			self.id_server = id_server

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
				cursor.execute("SELECT {}, {}, {} FROM markets WHERE id_server = %s".format(
					col_slimes_casino,
					col_rate_market,
					col_rate_exchange
				), (self.id_server, ))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.slimes_casino = result[0]
					self.rate_market = result[1]
					self.rate_exchange = result[2]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO markets(id_server) VALUES(%s)", (id_server, ))

					conn.commit()
			finally:
				# Clean up the database handles.
				if(our_cursor):
					cursor.close()
				if(our_conn):
					conn.close()

	""" Save market data object to the database. """
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
			cursor.execute("REPLACE INTO markets({}, {}, {}, {}) VALUES(%s, %s, %s, %s)".format(
				col_id_server,
				col_slimes_casino,
				col_rate_market,
				col_rate_exchange
			), (
				self.id_server,
				self.slimes_casino,
				self.rate_market,
				self.rate_exchange
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()

""" User model for database persistence """
class EwUser:
	id_user = ""
	id_server = ""
	id_killer = ""

	slimes = 0
	slimecredit = 0
	slimelevel = 0

	time_lastkill = 0
	time_lastrevive = 0
	time_lastspar = 0
	time_expirpvp = 0
	time_lasthaunt = 0
	time_lastinvest = 0

	""" Create a new EwUser and optionally retrieve it from the database. """
	def __init__(self, member=None, conn=None, cursor=None, id_user=None, id_server=None):
		if(id_user == None) and (id_server == None):
			if(member != None):
				id_server = member.server.id
				id_user = member.id

		# Retrieve the object from the database if the user is provided.
		if(id_user != None) and (id_server != None):
			self.id_server = id_server
			self.id_user = id_user

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
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM users WHERE id_user = %s AND id_server = %s".format(
					col_slimes,
					col_slimelevel,
					col_slimecredit,
					col_time_lastkill,
					col_time_lastrevive,
					col_id_killer,
					col_time_lastspar,
					col_time_expirpvp,
					col_time_lasthaunt,
					col_time_lastinvest
				), (
					id_user,
					id_server
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.slimes = result[0]
					self.slimelevel = result [1]
					self.slimecredit = result[2]
					self.time_lastkill = result[3]
					self.time_lastrevive = result[4]
					self.id_killer = result[5]
					self.time_lastspar = result[6]
					self.time_expirpvp = result[7]
					self.time_lasthaunt = result[8]
					self.time_lastinvest = result[9]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO users(id_user, id_server) VALUES(%s, %s)", (id_user, id_server))
					
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
			cursor.execute("REPLACE INTO users({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				col_id_user,
				col_id_server,
				col_slimes,
				col_slimelevel,
				col_slimecredit,
				col_time_lastkill,
				col_time_lastrevive,
				col_id_killer,
				col_time_lastspar,
				col_time_expirpvp,
				col_time_lasthaunt,
				col_time_lastinvest
			), (
				self.id_user,
				self.id_server,
				self.slimes,
				self.slimelevel,
				self.slimecredit,
				self.time_lastkill,
				self.time_lastrevive,
				self.id_killer,
				self.time_lastspar,
				self.time_expirpvp,
				self.time_lasthaunt,
				self.time_lastinvest
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()
