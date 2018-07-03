import ewutils
import ewcfg

"""
	EwServer is a representation of a server, if the name of the server or
	other meta data is needed in a scope where it's not normally available.
"""
class EwServer:
	id_server = ""

	name = ""
	icon = ""

	def __init__(
		self,
		id_server = None,
		conn = None,
		cursor = None
	):
		if(id_server != None):
			self.id_server = id_server

			our_cursor = False
			our_conn = False

			try:
				# Get database handles if they weren't passed.
				if(cursor == None):
					if(conn == None):
						conn_info = ewutils.databaseConnect()
						conn = conn_info.get('conn')
						our_conn = True

					cursor = conn.cursor()
					our_cursor = True

				# Retrieve object
				cursor.execute("SELECT {}, {} FROM servers WHERE id_server = %s".format(
					ewcfg.col_name,
					ewcfg.col_icon
				), (self.id_server, ))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.name = result[0]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO servers({}) VALUES(%s)".format(
						ewcfg.col_id_server
					), (
						self.id_server,
					))

					conn.commit()
			finally:
				# Clean up the database handles.
				if(our_cursor):
					cursor.close()
				if(our_conn):
					ewutils.databaseClose(conn_info)

	""" Save server data object to the database. """
	def persist(self, conn=None, cursor=None):
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn_info = ewutils.databaseConnect()
					conn = conn_info.get('conn')
					our_conn = True

				cursor = conn.cursor()
				our_cursor = True

			# Save the object.
			cursor.execute("REPLACE INTO servers({}, {}, {}) VALUES(%s, %s, %s)".format(
				ewcfg.col_id_server,
				ewcfg.col_name,
				ewcfg.col_icon
			), (
				self.id_server,
				self.name,
				self.icon
			))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				ewutils.databaseClose(conn_info)


""" update the player record with the current data. """
def server_update(server = None):
	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		dbserver = EwServer(
			id_server = server.id,
			conn = conn,
			cursor = cursor
		)

		# Update values with Member data.
		dbserver.name = server.name
		dbserver.icon = server.icon_url

		dbserver.persist(
			conn = conn,
			cursor = cursor
		)

		conn.commit()
	finally:
		cursor.close()
		ewutils.databaseClose(conn_info)
