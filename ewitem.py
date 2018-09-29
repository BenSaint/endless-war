import ewutils
import ewcfg
from ew import EwUser
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
		id_item = None
	):
		if(id_item != None):
			self.id_item = id_item

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()

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
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save item data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

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

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)


"""
	Delete the specified item by ID. Also deletes all items_prop values.
"""
def item_delete(
	id_item = None
):
	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		# Create the item in the database.
		cursor.execute("DELETE FROM items WHERE {} = %s".format(
			ewcfg.col_id_item
		), (
			id_item,
		))

		conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

"""
	Create a new item and give it to a player.

	Returns the unique database ID of the newly created item.
"""
def item_create(
	item_type = None,
	id_user = None,
	id_server = None,
	item_props = None
):
	item_def = ewcfg.item_def_map.get(item_type)

	if item_def == None:
		ewutils.logMsg('Tried to create invalid item_type: {}'.format(item_type))
		return

	try:
		# Get database handles if they weren't passed.
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

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

				item_inst.persist()

			conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)


	return item_id


"""
	Destroy all of a player's non-soulbound items.
"""
def item_destroyall(id_server = None, id_user = None, member = None):
	if member != None:
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None:
		try:
			# Get database handles if they weren't passed.
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			cursor.execute("DELETE FROM items WHERE {id_server} = %s AND {id_user} = %s AND {soulbound} = 0".format(
				id_user = ewcfg.col_id_user,
				id_server = ewcfg.col_id_server,
				soulbound = ewcfg.col_soulbound,
			), (
				id_server,
				id_user
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)


"""
	Loot all non-soulbound items from a player upon killing them, reassinging to id_user_target.
"""
def item_loot(
	member = None,
	id_user_target = ""
):
	if member == None or len(id_user_target) == 0:
		return

	try:
		# Get database handles if they weren't passed.
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		# Create the item in the database.
		cursor.execute("UPDATE items SET {id_user} = %s WHERE {id_server} = %s AND {id_user} = %s AND {soulbound} = 0".format(
			id_user = ewcfg.col_id_user,
			id_server = ewcfg.col_id_server,
			soulbound = ewcfg.col_soulbound,
		), (
			id_user_target,
			member.server.id,
			member.id
		))

		conn.commit()
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)


"""
	Returns true if the command string is !inv or equivalent.
"""
def cmd_is_inventory(cmd):
	return (cmd == ewcfg.cmd_inventory or cmd == ewcfg.cmd_inventory_alt1 or cmd == ewcfg.cmd_inventory_alt2 or cmd == ewcfg.cmd_inventory_alt3)

"""
	Get a list of items for the specified player.

	Specify an item_type_filter to get only those items. Be careful: This is
	inserted into SQL without validation/sanitation.
"""
def inventory(
	id_user = "",
	id_server = None,
	item_type_filter = None
):
	items = []

	try:
		player = EwPlayer(
			id_user = id_user,
			id_server = id_server
		)

		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		sql = "SELECT {}, {}, {}, {}, {} FROM items WHERE {} = %s AND {} = %s"
		if item_type_filter != None:
			sql += " AND {} = '{}'".format(ewcfg.col_item_type, item_type_filter)

		if player.id_server != None:
			cursor.execute(sql.format(
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

				item['quantity'] = quantity

				# Name requires variable substitution. Look up the item properties.
				if name.find('{') >= 0:
					item_inst = EwItem(id_item = id_item)

					if item_inst != None and item_inst.id_item >= 0:
						name = name.format_map(item_inst.item_props)

						if name.find('{') >= 0:
							name = name.format_map(item_inst.item_props)

				item['name'] = name
	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

	return items

"""
	Dump out a player's inventory.
"""
async def inventory_print(cmd):
	response = "You are holding:\n"

	items = inventory(
		id_user = cmd.message.author.id,
		id_server = (cmd.message.server.id if (cmd.message.server != None) else None)
	)

	if len(items) == 0:
		response = "You don't have anything."
	else:
		for item in items:
			id_item = item.get('id_item')
			quantity = item.get('quantity')

			response += "\n{id_item}: {soulbound_style}{name}{soulbound_style}{quantity}".format(
				id_item = item.get('id_item'),
				name = item.get('name'),
				soulbound_style = ("**" if item.get('soulbound') else ""),
				quantity = (" x{:,}".format(quantity) if (quantity > 0) else "")
			)

	await cmd.client.send_message(cmd.message.channel, response)


"""
	Dump out the visual description of an item.
"""
async def item_look(cmd):
	item_id = ewutils.flattenTokenListToString(cmd.tokens[1:])

	try:
		item_id_int = int(item_id)
	except:
		item_id_int = None

	if item_id != None and len(item_id) > 0:
		response = "You don't have one."

		items = inventory(
			id_user = cmd.message.author.id,
			id_server = (cmd.message.server.id if (cmd.message.server != None) else None)
		)

		item_sought = None
		for item in items:
			if item.get('id_item') == item_id_int or ewutils.flattenTokenListToString(item.get('name')) == item_id:
				item_sought = item
				break

		if item_sought != None:
			item_def = item.get('item_def')
			id_item = item.get('id_item')
			name = item.get('name')
			response = item_def.str_desc

			# Replace up to two levels of variable substitutions.
			if response.find('{') >= 0:
				item_inst = EwItem(id_item = id_item)
				response = response.format_map(item_inst.item_props)

				if response.find('{') >= 0:
					response = response.format_map(item_inst.item_props)

			response = name + "\n\n" + response

		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	else:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, 'Inspect which item? (check **!inventory**)'))

# this is basically just the item_look command with some other stuff at the bottom
async def item_use(cmd):
	item_id = ewutils.flattenTokenListToString(cmd.tokens[1:])

	try:
		item_id_int = int(item_id)
	except:
		item_id_int = None

	if item_id != None and len(item_id) > 0:
		response = "You don't have one."

		items = inventory(
			id_user = cmd.message.author.id,
			id_server = (cmd.message.server.id if (cmd.message.server != None) else None)
		)

		item_sought = None
		for item in items:
			if item.get('id_item') == item_id_int or ewutils.flattenTokenListToString(item.get('name')) == item_id:
				item_sought = item
				break

		if item_sought != None:
			item_def = item.get('item_def')
			id_item = item.get('id_item')
			name = item.get('name')

			user_data = EwUser(member = cmd.message.author)

			if name.lower() == "endless rock":
				if user_data.poi != ewcfg.poi_id_endlesswar:
					response = "You have to be near ENDLESS WAR to use this item."
				else:
					# EW: Wake
					response = "You use the Endless Rock to awaken ENDLESS WAR."
					await ewutils.post_in_multiple_channels(
						# @everyone is purposely misspelled so testing isnt annoying everyone
						message = "@everyone ENDLESS WAR has awoken. https://ew.krakissi.net/img/revive.gif",
						channels = cmd.message.server.channels,  # all channels
						client = cmd.client
					)

					# take the endless rock away from the player who !used it
					give_item(id_user = '0', id_server = user_data.id_server, id_item = id_item)

		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	else:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author,
		                                                                         'Use which item? (check **!inventory**)'))


"""
	give an existing item to a player
"""
def give_item(
	member = None,
	id_item = None,
	id_user = None,
	id_server = None
):

	if(id_user == None) and (id_server == None) and (member != None):
		id_server = member.server.id
		id_user = member.id

	if id_server != None and id_user != None and id_item != None:
		sql_query = "UPDATE items SET {id_user} = {user_id} WHERE {id_server} = {server_id} AND {id_item} = {item_id}".format(
			id_user = ewcfg.col_id_user,
			user_id = id_user,
			id_server = ewcfg.col_id_server,
			server_id = id_server,
			id_item = ewcfg.col_id_item,
			item_id = id_item
		)

		ewutils.execute_sql_query(sql_query)

	return True
