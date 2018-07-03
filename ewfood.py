import ewcfg
import ewutils
import ewcmd
from ew import EwUser, EwMarket

""" Food model object """
class EwFood:
	# The main name of this food.
	id_food = ""

	# A list of alternative names.
	alias = []

	# Stamina recovered by eating this food.
	recover_stamina = 0

	# Cost in slime to eat this food.
	price = 0

	# A nice string name describing this food.
	str_name = ""

	# Name of the vendor selling this food in the food court.
	vendor = ""

	# Flavor text displayed when you eat this food.
	str_eat = ""

	# Alcoholic effect
	inebriation = 0

	def __init__(
		self,
		id_food = "",
		alias = [],
		recover_stamina = 0,
		price = 0,
		str_name = "",
		vendor = "",
		str_eat = "",
		inebriation = 0
	):
		self.id_food = id_food
		self.alias = alias
		self.recover_stamina = recover_stamina
		self.price = price
		self.str_name = str_name
		self.vendor = vendor
		self.str_eat = str_eat
		self.inebriation = inebriation


""" show all available food items """
async def menu(cmd):
	if cmd.message.channel.name != ewcfg.channel_foodcourt:
		# Only allowed in the food court.
		response = ewcfg.str_food_channelreq.format(action = "see the menu")
	else:
		response = "NLACakaNM Food Court Menu:\n\n"

		for vendor in ewcfg.food_vendor_inv:
			response += "**{}**: *{}*\n".format(vendor, ewutils.formatNiceList(names = ewcfg.food_vendor_inv[vendor]))

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" players order food, for themselves or somebody else """
async def order(cmd):
	resp = await ewcmd.start(cmd = cmd)

	if cmd.message.channel.name != ewcfg.channel_foodcourt:
		# Only allowed in the food court.
		response = ewcfg.str_food_channelreq.format(action = "order")
	else:
		value = None
		if cmd.tokens_count > 1:
			for token in cmd.tokens[1:]:
				if token.startswith('<@') == False:
					value = token
					break

		food = ewcfg.food_map.get(value)

		member = None
		if cmd.mentions_count == 1:
			member = cmd.mentions[0]
			if member.id == cmd.message.author.id:
				member = None

		if food == None:
			response = "Check the {} for a list of items you can {}.".format(ewcfg.cmd_menu, ewcfg.cmd_order)
		else:
			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()

				user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)
				market_data = EwMarket(id_server = cmd.message.server.id, conn = conn, cursor = cursor)

				target_data = None
				if member != None:
					target_data = EwUser(member = member, conn = conn, cursor = cursor)
			finally:
				cursor.close()
				ewutils.databaseClose(conn_info)

			value = int(food.price / (market_data.rate_exchange / 1000000.0))
			if value <= 0:
				value = 1

			# Kingpins eat free.
			roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)
			if ewcfg.role_rowdyfucker in roles_map_user or ewcfg.role_copkiller in roles_map_user:
				value = 0

			if value > user_data.slimecredit:
				# Not enough money.
				response = "A {food} is {cost:,} SlimeCoin (and you only have {credits:,}).".format(
					food = food.str_name,
					cost = value,
					credits = user_data.slimecredit
				)
			else:
				user_data.slimecredit -= value

				if target_data != None:
					target_data.stamina -= food.recover_stamina
					if target_data.stamina < 0:
						target_data.stamina = 0
					target_data.inebriation += food.inebriation
					if target_data.inebriation > 20:
						target_data.inebriation = 20
					
				else:
					user_data.stamina -= food.recover_stamina
					if user_data.stamina < 0:
						user_data.stamina = 0
					user_data.inebriation += food.inebriation
					if user_data.inebriation > 20:
						user_data.inebriation = 20

				market_data.slimes_casino += food.price

				response = "You slam {cost:,} SlimeCoin down at the {vendor} for a {food}{sharetext}{flavor}".format(
					cost = value,
					vendor = food.vendor,
					food = food.str_name,
					sharetext = (". " if member == None else " and give it to {}.\n\n{}".format(member.display_name, ewutils.formatMessage(member, ""))),
					flavor = food.str_eat
				)
				if member == None and user_data.stamina <= 0:
					response += "\n\nYou're stuffed!"

				try:
					conn_info = ewutils.databaseConnect()
					conn = conn_info.get('conn')
					cursor = conn.cursor()

					user_data.persist(conn = conn, cursor = cursor)
					market_data.persist(conn = conn, cursor = cursor)

					if target_data != None:
						target_data.persist(conn = conn, cursor = cursor)

					conn.commit()
				finally:
					cursor.close()
					ewutils.databaseClose(conn_info)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
