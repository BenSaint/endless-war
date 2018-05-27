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

	def __init__(
		self,
		id_food="",
		alias=[],
		recover_stamina=0,
		price=0,
		str_name="",
		vendor="",
		str_eat=""
	):
		self.id_food = id_food
		self.alias = alias
		self.recover_stamina = recover_stamina
		self.price = price
		self.str_name = str_name
		self.vendor = vendor
		self.str_eat = str_eat
