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

	# Hunger reduced by eating this food.
	recover_hunger = 0

	# Cost in SlimeCoin to eat this food.
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
		recover_hunger = 0,
		price = 0,
		str_name = "",
		vendor = "",
		str_eat = "",
		inebriation = 0
	):
		self.id_food = id_food
		self.alias = alias
		self.recover_hunger = recover_hunger
		self.price = price
		self.str_name = str_name
		self.vendor = vendor
		self.str_eat = str_eat
		self.inebriation = inebriation


""" show all available food items """
async def menu(cmd):
	user_data = EwUser(member = cmd.message.author)
	poi = ewcfg.id_to_poi.get(user_data.poi)

	if poi == None or len(poi.vendors) == 0:
		# Only allowed in the food court.
		response = ewcfg.str_food_channelreq.format(action = "see the menu")
	else:
		response = "{} Menu:\n\n".format(poi.str_name)

		for vendor in poi.vendors:
			response += "**{}**: *{}*\n".format(vendor, ewutils.formatNiceList(names = ewcfg.food_vendor_inv[vendor]))

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" players order food, for themselves or somebody else """
async def order(cmd):
	user_data = EwUser(member = cmd.message.author)
	poi = ewcfg.id_to_poi.get(user_data.poi)

	if (poi == None) or (len(poi.vendors) == 0):
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

		member_data = EwUser(member = member)

		if food == None or food.vendor not in poi.vendors:
			response = "Check the {} for a list of items you can {}.".format(ewcfg.cmd_menu, ewcfg.cmd_order)
		elif member is not None and member_data.poi != user_data.poi:
			response = "The delivery service has become unavailable due to unforeseen circumstances."
		else:
			market_data = EwMarket(id_server = cmd.message.server.id)

			target_data = None
			if member != None:
				target_data = EwUser(member = member)

			value = food.price

			# Kingpins eat free.
			if user_data.life_state == ewcfg.life_state_kingpin or user_data.life_state == ewcfg.life_state_grandfoe:
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
					target_data.hunger -= food.recover_hunger
					if target_data.hunger < 0:
						target_data.hunger = 0
					target_data.inebriation += food.inebriation
					if target_data.inebriation > 20:
						target_data.inebriation = 20
					
				else:
					user_data.hunger -= food.recover_hunger
					if user_data.hunger < 0:
						user_data.hunger = 0
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
				if member == None and user_data.hunger <= 0:
					response += "\n\nYou're stuffed!"

				if food.id_food == "coleslaw":
					user_data.ghostbust = True

				user_data.persist()
				market_data.persist()

				if target_data != None:
					target_data.persist()

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
