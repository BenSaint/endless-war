import random

import ewcfg
import ewitem

"""
	Cosmetic item model object
"""
class EwCosmeticItem:
	# The name of the cosmetic item
	name = ""

	# The text displayed when you look at it
	description = ""

	# How rare the item is, can be "Plebeian", "Patrician", or "Princeps"
	rarity = ""

	def __init__(
		self,
		name = "",
		description = "",
		rarity = ""
	):
		self.name = name
		self.description = description
		self.rarity = rarity

"""
	Smelt command
"""
async def smelt(cmd):
	poudrins = ewitem.inventory(
		id_user = cmd.message.author.id,
		id_server = cmd.message.server.id,
		item_type_filter = ewcfg.it_slimepoudrin
	)

	if len(poudrins) < 3:
		response = "You don't have enough poudrins to smelt."
	else:
		for i in range(3):
			ewitem.item_delete(id_item = poudrins[i].get('id_item'))
		patrician_rarity = 100
		patrician_smelted = random.randint(1, patrician_rarity)
		patrician = False

		if patrician_smelted == 1:
			patrician = True

		if patrician:
			#item = patrician item
			pass
		else:
			pass #item = plebeian item
