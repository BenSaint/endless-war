""" A weapon object which adds flavor text to kill/shoot. """
class EwWeapon:
	# A unique name for the weapon. This is used in the database and typed by
	# users, so it should be one word, all lowercase letters.
	id_weapon = ""

	# An array of names that might be used to identify this weapon by the player.
	alias = []

	# Displayed when !equip-ping this weapon
	str_equip = ""

	# Displayed when this weapon is used for a !kill
	str_kill = ""

	# Displayed when viewing the !trauma of another player.
	str_trauma = ""

	# Displayed when viewing the !trauma of yourself.
	str_trauma_self = ""

	# Displayed when a non-lethal hit occurs.
	str_damage = ""

	def __init__(self, id_weapon="", alias=[], str_equip="", str_kill="", str_trauma="", str_trauma_self="", str_damage=""):
		self.id_weapon = id_weapon
		self.alias = alias
		self.str_equip = str_equip
		self.str_kill = str_kill
		self.str_trauma = str_trauma
		self.str_trauma_self = str_trauma_self
		self.str_damage = str_damage

