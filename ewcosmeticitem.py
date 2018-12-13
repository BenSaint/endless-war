

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
	pass