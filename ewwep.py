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
	
	# Displayed when viewing the !weapon of another player.
	str_weapon = ""

	# Displayed when viewing the !weapon of yourself.
	str_weapon_self = ""

	# Same as weapon and weapon_self, but used when the player's weapon skill is max.
	str_weaponmaster = ""
	str_weaponmaster_self = ""

	# Displayed when a non-lethal hit occurs.
	str_damage = ""

	# Displayed when two players wielding the same weapon !spar with each other.
	str_duel = ""

	# Function that applies the special effect for this weapon.
	fn_effect = None

	# Displayed when a weapon effect causes a critical hit.
	str_crit = ""

	# Displayed when a weapon effect causes a miss.
	str_miss = ""

	def __init__(
		self,
		id_weapon="",
		alias=[],
		str_equip="",
		str_kill="",
		str_trauma="",
		str_trauma_self="",
		str_weapon="",
		str_weapon_self="",
		str_damage="",
		str_duel="",
		str_weaponmaster="",
		str_weaponmaster_self="",
		fn_effect=None,
		str_crit="",
		str_miss=""
	):
		self.id_weapon = id_weapon
		self.alias = alias
		self.str_equip = str_equip
		self.str_kill = str_kill
		self.str_trauma = str_trauma
		self.str_trauma_self = str_trauma_self
		self.str_weapon = str_weapon
		self.str_weapon_self = str_weapon_self
		self.str_damage = str_damage
		self.str_duel = str_duel
		self.str_weaponmaster = str_weaponmaster
		self.str_weaponmaster_self = str_weaponmaster_self
		self.fn_effect = fn_effect
		self.str_crit = str_crit
		self.str_miss = str_miss


""" A data-moving class which holds references to objects we want to modify with weapon effects. """
class EwEffectContainer:
	miss = False
	crit = False
	strikes = 0
	slimes_damage = 0
	slimes_spent = 0
	user_data = None
	shootee_data = None

	# Debug method to dump out the members of this object.
	def dump(self):
		print("effect:\nmiss: {miss}\ncrit: {crit}\nstrikes: {strikes}\nslimes_damage: {slimes_damage}\nslimes_spent: {slimes_spent}".format(
			miss=self.miss,
			crit=self.crit,
			strikes=self.strikes,
			slimes_damage=self.slimes_damage,
			slimes_spent=self.slimes_spent
		))

	def __init__(
		self,
		miss=False,
		crit=False,
		strikes=0,
		slimes_damage=0,
		slimes_spent=0,
		user_data=None,
		shootee_data=None
	):
		self.miss = miss
		self.crit = crit
		self.strikes = strikes
		self.slimes_damage = slimes_damage
		self.slimes_spent = slimes_spent
		self.user_data = user_data
		self.shootee_data = shootee_data
