import math
import time

import ewcfg
import ewitem
import ewutils
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

	# Names of the vendors selling this food in the food court.
	vendors = []

	# Flavor text displayed when you eat this food.
	str_eat = ""

	# Alcoholic effect
	inebriation = 0

	# Flavor text displayed when you inspect this food.
	str_desc = ""

	# Expiration time (can be left blank for standard expiration time)
	time_expir = 0

	def __init__(
		self,
		id_food = "",
		alias = [],
		recover_hunger = 0,
		price = 0,
		str_name = "",
		vendors = [],
		str_eat = "",
		inebriation = 0,
		str_desc = "",
		time_expir = 0
	):
		self.id_food = id_food
		self.alias = alias
		self.recover_hunger = recover_hunger
		self.price = price
		self.str_name = str_name
		self.vendors = vendors
		self.str_eat = str_eat
		self.inebriation = inebriation
		self.str_desc = str_desc
		self.time_expir = time_expir if time_expir > 0 else ewcfg.std_food_expir


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
		togo = False
		current_vendor = None
		if cmd.tokens_count > 1:
			for token in cmd.tokens[1:]:
				if token.startswith('<@') == False and token.lower() not in "togo":  # togo can be spelled together or separate
					value = token
					break
			for token in cmd.tokens[1:]:
				if token.lower() in "togo":  # lets people get away with just typing only to or only go (or only t etc.) but whatever
					togo = True
					break

		food = ewcfg.food_map.get(value.lower() if value != None else value)
		if food != None and ewcfg.vendor_vendingmachine in food.vendors:
			togo = True

		member = None
		if not togo:  # cant order togo for someone else, you can just give it to them in person
			if cmd.mentions_count == 1:
				member = cmd.mentions[0]
				if member.id == cmd.message.author.id:
					member = None

		member_data = EwUser(member = member)

		if food is not None:
			# gets a vendor that the item is available and the player currently located in
			current_vendor = (set(food.vendors).intersection(set(poi.vendors))).pop()

		if food == None or current_vendor is None or len(current_vendor) < 1:
			response = "Check the {} for a list of items you can {}.".format(ewcfg.cmd_menu, ewcfg.cmd_order)
		elif member is not None and member_data.poi != user_data.poi:
			response = "The delivery service has become unavailable due to unforeseen circumstances."
		else:
			market_data = EwMarket(id_server = cmd.message.server.id)

			target_data = None
			if member != None:
				target_data = EwUser(member = member)

			value = food.price if not togo else food.price * ewcfg.togo_price_increase

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
				user_data.change_slimecredit(n = -value, coinsource = ewcfg.coinsource_spending)

				if not togo:

					if target_data != None:
						target_data.hunger -= food.recover_hunger
						if target_data.hunger < 0:
							target_data.hunger = 0
						target_data.inebriation += food.inebriation
						if target_data.inebriation > ewcfg.inebriation_max:
							target_data.inebriation = ewcfg.inebriation_max
						if food.id_food == "coleslaw":
							target_data.ghostbust = True

					else:
						user_data.hunger -= food.recover_hunger
						if user_data.hunger < 0:
							user_data.hunger = 0
						user_data.inebriation += food.inebriation
						if user_data.inebriation > ewcfg.inebriation_max:
							user_data.inebriation = ewcfg.inebriation_max
						if food.id_food == "coleslaw":
							user_data.ghostbust = True

				else:  # if it's togo
					inv = ewitem.inventory(
						id_user = cmd.message.author.id,
						id_server = cmd.message.server.id
					)
					food_in_inv = 0
					for item in inv:
						if item.get('item_type') == ewcfg.it_food:
							food_in_inv += 1

					if food_in_inv >= math.ceil(user_data.slimelevel / ewcfg.max_food_in_inv_mod):
						# user_data never got persisted so the player won't lose money unnecessarily
						response = "You can't carry any more food than that."
						return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

					item_props = {
						# not all attributes are necessary to store in the database since the price and vendors list is only needed for buying it
						'food_name': food.str_name,
						'food_desc': food.str_desc,
						'recover_hunger': food.recover_hunger,
						'inebriation': food.inebriation,
						'str_eat': food.str_eat,
						'time_expir': time.time() + (food.time_expir if food.time_expir is not None else ewcfg.std_food_expir)
					}

					ewitem.item_create(
						item_type = ewcfg.it_food,
						id_user = cmd.message.author.id,
						id_server = cmd.message.server.id,
						item_props = item_props
					)

				response = "You slam {cost:,} SlimeCoin down at the {vendor} for a {food}{togo}{sharetext}{flavor}".format(
					cost = value,
					vendor = current_vendor,
					food = food.str_name,
					togo = " to go" if togo else "",
					sharetext = (". " if member == None else " and give it to {}.\n\n{}".format(member.display_name, ewutils.formatMessage(member, ""))),
					flavor = food.str_eat if not togo else ""
				)
				if member == None and user_data.hunger <= 0 and not togo:
					response += "\n\nYou're stuffed!"

				user_data.persist()
				market_data.persist()

				if target_data != None:
					target_data.persist()

	# Send the response to the player.
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
