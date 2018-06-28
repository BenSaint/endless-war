import ewutils
import ewcfg
from ewplayer import EwPlayer

"""
	EwItemDef is a class used to model base items. These are NOT the items
	owned by players, but rather the description of what those items are.
"""
class EwItemDef:
	# This is the unique reference name for this item.
	item_type = ""

	# If this is true, the item can not be traded or stolen.
	soulbound = False

	# If this value is positive, the item may actually be a pile of the same type of item, up to the specified size.
	stack_max = -1

	# If this value is greater than one, creating this item will actually give the user that many of them.
	stack_size = 1

	# Nice display name for this item.
	str_name = ""

	# The long description of this item's appearance.
	str_desc = ""

	# A map of default additional properties.
	item_props = None

	def __init__(
		self,
		item_type = "",
		str_name = "",
		str_desc = "",
		soulbound = False,
		stack_max = -1,
		stack_size = 1,
		item_props = None
	):
		self.item_type = item_type
		self.str_name = str_name
		self.str_desc = str_desc
		self.soulbound = soulbound
		self.stack_max = stack_max
		self.stack_size = stack_size
		self.item_props = item_props

"""
	EwItem is the instance of an item (described by EwItemDef, linked by
	item_type) which is possessed by a player and stored in the database.
"""
class EwItem:
	id_item = -1
	id_server = ""
	id_user = ""
	item_type = ""
	time_expir = -1

	stack_max = -1
	stack_size = 0
	soulbound = False

	item_props = {}

	def __init__(
		self,
		id_item = None,
		conn = None,
		cursor = None
	):
		if(id_item != None):
			self.id_item = id_item

			our_cursor = False
			our_conn = False

			try:
				# Get database handles if they weren't passed.
				if(cursor == None):
					if(conn == None):
						conn = ewutils.databaseConnect()
						our_conn = True

					cursor = conn.cursor()
					our_cursor = True

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {} FROM items WHERE id_item = %s".format(
					ewcfg.col_id_server,
					ewcfg.col_id_user,
					ewcfg.col_item_type,
					ewcfg.col_time_expir,
					ewcfg.col_stack_max,
					ewcfg.col_stack_size,
					ewcfg.col_soulbound
				), (
					self.id_item,
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.id_server = result[0]
					self.id_user = result[1]
					self.item_type = result[2]
					self.time_expir = result[3]
					self.stack_max = result[4]
					self.stack_size = result[5]
					self.soulbound = (result[6] != 0)

					# Retrieve additional properties
					cursor.execute("SELECT {}, {} FROM items_prop WHERE id_item = %s".format(
						ewcfg.col_name,
						ewcfg.col_value
					), (
						self.id_item,
					))

					for row in cursor:
						self.item_props[row[0]] = row[1]

				else:
					# Item not found.
					self.id_item = -1

			finally:
				# Clean up the database handles.
				if(our_cursor):
					cursor.close()
				if(our_conn):
					conn.close()

	""" Save user data object to the database. """
	def persist(self, conn=None, cursor=None):
		our_cursor = False
		our_conn = False

		try:
			# Get database handles if they weren't passed.
			if(cursor == None):
				if(conn == None):
					conn = ewutils.databaseConnect()
					our_conn = True

				cursor = conn.cursor()
				our_cursor = True

			# Save the object.
			cursor.execute("REPLACE INTO items({}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_item,
				ewcfg.col_id_server,
				ewcfg.col_id_user,
				ewcfg.col_item_type,
				ewcfg.col_time_expir,
				ewcfg.col_stack_max,
				ewcfg.col_stack_size,
				ewcfg.col_soulbound
			), (
				self.id_item,
				self.id_server,
				self.id_user,
				self.item_type,
				self.time_expir,
				self.stack_max,
				self.stack_size,
				(1 if self.soulbound else 0)
			))

			# Remove all existing property rows.
			cursor.execute("DELETE FROM items_prop WHERE {} = %s".format(
				ewcfg.col_id_item
			), (
				self.id_item,
			))

			# Write out all current property rows.
			for name in self.item_props:
				cursor.execute("INSERT INTO items_prop({}, {}, {}) VALUES(%s, %s, %s)".format(
					ewcfg.col_id_item,
					ewcfg.col_name,
					ewcfg.col_value
				), (
					self.id_item,
					name,
					self.item_props[name]
				))

			if our_cursor:
				conn.commit()
		finally:
			# Clean up the database handles.
			if(our_cursor):
				cursor.close()
			if(our_conn):
				conn.close()

"""
	Return the visible description of an item.
"""
def item_look(item):
	item_def = ewcfg.item_def_map.get(item.item_type)

	if item_def == None:
		return "You aren't sure what it is."

	response = item_def.str_desc

	# Replace up to two levels of variable substitutions.
	if response.find('{') >= 0:
		response = response.format_map(item.item_props)

		if response.find('{') >= 0:
			response = response.format_map(item.item_props)

	return response


"""
	Create a new item and give it to a player.

	Returns the unique database ID of the newly created item.
"""
def item_create(
	item_type = None,
	id_user = None,
	id_server = None,
	item_props = None,
	conn = None,
	cursor = None
):
	our_cursor = False
	our_conn = False

	item_def = ewcfg.item_def_map.get(item_type)

	if item_def == None:
		ewutils.logMsg('Tried to create invalid item_type: {}'.format(item_type))
		return

	try:
		# Get database handles if they weren't passed.
		if(cursor == None):
			if(conn == None):
				conn = ewutils.databaseConnect()
				our_conn = True

			cursor = conn.cursor()
			our_cursor = True

		# Create the item in the database.
		cursor.execute("INSERT INTO items({}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s)".format(
			ewcfg.col_item_type,
			ewcfg.col_id_user,
			ewcfg.col_id_server,
			ewcfg.col_soulbound,
			ewcfg.col_stack_max,
			ewcfg.col_stack_size
		), (
			item_type,
			id_user,
			id_server,
			(1 if item_def.soulbound else 0),
			item_def.stack_max,
			item_def.stack_size
		))

		item_id = cursor.lastrowid
		conn.commit()

		if item_id > 0:
			# If additional properties are specified in the item definition or in this create call, create and persist them.
			if item_props != None or item_def.item_props != None:
				item_inst = EwItem(id_item = item_id)

				if item_def.item_props != None:
					item_inst.item_props.update(item_def.item_props)

				if item_props != None:
					item_inst.item_props.update(item_props)

				item_inst.persist(conn = conn, cursor = cursor)

			conn.commit()
	finally:
		# Clean up the database handles.
		if(our_cursor):
			cursor.close()
		if(our_conn):
			conn.close()


	return item_id

"""
	Returns true if the command string is !inv or equivalent.
"""
def cmd_is_inventory(cmd):
	return (cmd == ewcfg.cmd_inventory or cmd == ewcfg.cmd_inventory_alt1 or cmd == ewcfg.cmd_inventory_alt2 or cmd == ewcfg.cmd_inventory_alt3)


"""
	Dump out a player's inventory.
"""
async def inventory(cmd):
	resp = await cmd.client.send_message(cmd.message.author, '...')
	response = "You are holding:\n"

	try:
		conn = ewutils.databaseConnect()
		cursor = conn.cursor()

		player = EwPlayer(
			id_user = cmd.message.author.id,
			id_server = (cmd.message.server.id if (cmd.message.server != None) else None),
			conn = conn,
			cursor = cursor
		)

		if player.id_server != None:
			cursor.execute("SELECT {}, {}, {}, {}, {} FROM items WHERE {} = %s AND {} = %s".format(
				ewcfg.col_id_item,
				ewcfg.col_item_type,
				ewcfg.col_soulbound,
				ewcfg.col_stack_max,
				ewcfg.col_stack_size,

				ewcfg.col_id_user,
				ewcfg.col_id_server
			), (
				player.id_user,
				player.id_server
			))

			items = []
			for row in cursor:
				id_item = row[0]
				item_type = row[1]
				soulbound = (row[2] == 1)
				stack_max = row[3]
				stack_size = row[4]

				item_def = ewcfg.item_def_map.get(item_type)

				if(item_def != None):
					items.append({
						'id_item': id_item,
						'item_type': item_type,
						'soulbound': soulbound,
						'stack_max': stack_max,
						'stack_size': stack_size,

						'item_def': item_def
					})

			for item in items:
				item_def = item.get('item_def')
				id_item = item.get('id_item')
				name = item_def.str_name

				quantity = 0
				if item.get('stack_max') > 0:
					quantity = item.get('stack_size')

				# Name requires variable substitution. Look up the item properties.
				if name.find('{') >= 0:
					item_inst = EwItem(
						id_item = id_item,
						conn = conn,
						cursor = cursor
					)

					if item_inst != None and item_inst.id_item >= 0:
						name = name.format_map(item_inst.item_props)

						if name.find('{') >= 0:
							name = name.format_map(item_inst.item_props)

				response += "\n{id_item}: {soulbound_style}{name}{soulbound_style}{quantity}".format(
					id_item = id_item,
					name = name,
					soulbound_style = ("**" if item.get('soulbound') else ""),
					quantity = (" x{:,}".format(quantity) if (quantity > 0) else "")
				)
	finally:
		cursor.close()
		conn.close()

	await cmd.client.edit_message(resp, response)
