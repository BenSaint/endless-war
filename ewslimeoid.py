import random
import asyncio

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
from ew import EwUser, EwMarket

""" Slimeoid data model for database persistence """
class EwSlimeoid:
	id_slimeoid = 0
	id_user = ""
	id_server = ""

	life_state = 0
	body = ""
	head = ""
	legs = ""
	armor = ""
	weapon = ""
	special = ""
	ai = ""
	sltype = "Lab"
	name = ""
	atk = 0
	defense = 0
	intel = 0
	level = 0
	time_defeated = 0

	#slimeoid = EwSlimeoid(member = cmd.message.author, )
	#slimeoid = EwSlimeoid(id_slimeoid = 12)

	""" Load the slimeoid data for this user from the database. """
	def __init__(self, member = None, id_slimeoid = None, life_state = None):
		query_suffix = ""

		if id_slimeoid != None:
			query_suffix = " WHERE id_slimeoid = '{}'".format(id_slimeoid)
		elif member != None:
			query_suffix = " WHERE id_user = '{}' AND id_server = '{}'".format(member.id, member.server.id)
			if life_state != None:
				query_suffix += " AND life_state = '{}'".format(life_state)

		if query_suffix != "":
			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM slimeoids{}".format(
					ewcfg.col_id_slimeoid,
					ewcfg.col_id_user,
					ewcfg.col_id_server,
					ewcfg.col_life_state,
					ewcfg.col_body,
					ewcfg.col_head,
					ewcfg.col_legs,
					ewcfg.col_armor,
					ewcfg.col_weapon,
					ewcfg.col_special,
					ewcfg.col_ai,
					ewcfg.col_type,
					ewcfg.col_name,
					ewcfg.col_atk,
					ewcfg.col_defense,
					ewcfg.col_intel,
					ewcfg.col_level,
					ewcfg.col_time_defeated,
					query_suffix
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.id_slimeoid = result[0]
					self.id_user = result[1]
					self.id_server = result[2]
					self.life_state = result[3]
					self.body = result[4]
					self.head = result[5]
					self.legs = result[6]
					self.armor = result[7]
					self.weapon = result[8]
					self.special = result[9]
					self.ai= result[10]
					self.sltype = result[11]
					self.name = result[12]
					self.atk = result[13]
					self.defense = result[14]
					self.intel = result[15]
					self.level = result[16]
					self.time_defeated = result[17]

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save slimeoid data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save the object.
			cursor.execute("REPLACE INTO slimeoids({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_slimeoid,
				ewcfg.col_id_user,
				ewcfg.col_id_server,
				ewcfg.col_life_state,
				ewcfg.col_body,
				ewcfg.col_head,
				ewcfg.col_legs,
				ewcfg.col_armor,
				ewcfg.col_weapon,
				ewcfg.col_special,
				ewcfg.col_ai,
				ewcfg.col_type,
				ewcfg.col_name,
				ewcfg.col_atk,
				ewcfg.col_defense,
				ewcfg.col_intel,
				ewcfg.col_level,
				ewcfg.col_time_defeated
			), (
				self.id_slimeoid,
				self.id_user,
				self.id_server,
				self.life_state,
				self.body,
				self.head,
				self.legs,
				self.armor,
				self.weapon,
				self.special,
				self.ai,
				self.sltype,
				self.name,
				self.atk,
				self.defense,
				self.intel,
				self.level,
				self.time_defeated
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

""" slimeoid model object """
class EwBody:
	id_body = ""
	alias = []
	str_create = ""
	str_body = ""
	def __init__(
		self,
		id_body = "",
		alias = [],
		str_create = "",
		str_body = "",
		str_observe = ""
	):
		self.id_body = id_body
		self.alias = alias
		self.str_create = str_create
		self.str_body = str_body
		self.str_observe = str_observe

class EwHead:
	id_head = ""
	alias = []
	str_create = ""
	str_head = ""
	def __init__(
		self,
		id_head = "",
		alias = [],
		str_create = "",
		str_head = "",
		str_feed = "",
		str_fetch = ""
	):
		self.id_head = id_head
		self.alias = alias
		self.str_create = str_create
		self.str_head = str_head
		self.str_feed = str_feed
		self.str_fetch = str_fetch
	
class EwMobility:
	id_mobility = ""
	alias = []
	str_advance = ""
	str_retreat = ""
	str_create = ""
	str_mobility = ""
	def __init__(
		self,
		id_mobility = "",
		alias = [],
		str_advance = "",
		str_advance_weak = "",
		str_retreat = "",
		str_retreat_weak = "",
		str_create = "",
		str_mobility = "",
		str_defeat = "",
		str_walk = ""
	):
		self.id_mobility = id_mobility
		self.alias = alias
		self.str_advance = str_advance
		self.str_advance_weak = str_advance_weak
		self.str_retreat = str_retreat
		self.str_retreat_weak = str_retreat_weak
		self.str_create = str_create
		self.str_mobility = str_mobility
		self.str_defeat = str_defeat
		self.str_walk = str_walk

class EwOffense:
	id_offense = ""
	alias = []
	str_attack = ""
	str_create = ""
	str_offense = ""
	def __init__(
		self,
		id_offense = "",
		alias = [],
		str_attack = "",
		str_attack_weak = "",
		str_attack_coup = "",
		str_create = "",
		str_offense = "",
		str_observe = ""
	):
		self.id_offense = id_offense
		self.alias = alias
		self.str_attack = str_attack
		self.str_attack_weak = str_attack_weak
		self.str_attack_coup = str_attack_coup
		self.str_create = str_create
		self.str_offense = str_offense
		self.str_observe = str_observe

class EwDefense:
	id_defense = ""
	alias = []
	str_create = ""
	str_defense = ""
	def __init__(
		self,
		id_defense = "",
		alias = [],
		str_create = "",
		str_defense = "",
		str_armor = "",
		str_pet = ""
	):
		self.id_defense = id_defense
		self.alias = alias
		self.str_create = str_create
		self.str_defense = str_defense
		self.str_armor = str_armor
		self.str_pet = str_pet

class EwSpecial:
	id_special = ""
	alias = []
	str_special_attack = ""
	str_create = ""
	str_special = ""
	def __init__(
		self,
		id_special = "",
		alias = [],
		str_special_attack = "",
		str_special_attack_weak = "",
		str_special_attack_coup = "",
		str_create = "",
		str_special = "",
		str_observe = ""
	):
		self.id_special = id_special
		self.alias = alias
		self.str_special_attack = str_special_attack
		self.str_special_attack_weak = str_special_attack_weak
		self.str_special_attack_coup = str_special_attack_coup
		self.str_create = str_create
		self.str_special = str_special
		self.str_observe = str_observe

class EwBrain:
	id_brain = ""
	alias = []
	str_create = ""
	str_brain = ""
	def __init__(
		self,
		id_brain = "",
		alias = [],
		str_create = "",
		str_brain = "",
		str_dissolve = "",
		str_spawn = "",
		str_revive = "",
		str_death = "",
		str_victory = "",
		str_battlecry = "",
		str_battlecry_weak = "",
		str_movecry = "",
		str_movecry_weak = "",
		str_kill = "",
		str_walk = "",
		str_pet = "",
		str_observe = ""
	):
		self.id_brain = id_brain
		self.alias = alias
		self.str_create = str_create
		self.str_brain = str_brain
		self.str_dissolve = str_dissolve
		self.str_spawn = str_spawn
		self.str_revive = str_revive
		self.str_death = str_death
		self.str_victory = str_victory
		self.str_battlecry = str_battlecry
		self.str_battlecry_weak = str_battlecry_weak
		self.str_movecry = str_movecry
		self.str_movecry_weak = str_movecry_weak
		self.str_kill = str_kill
		self.str_pet = str_pet
		self.str_walk = str_walk
		self.str_observe = str_observe
