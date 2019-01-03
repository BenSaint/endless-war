import time

import ewutils
import ewcfg
import ewstats
import ewitem

""" Market data model for database persistence """
class EwMarket:
	id_server = ""

	clock = 0
	weather = 'sunny'
	day = 0

	slimes_casino = 0
	slimes_revivefee = 0

	rate_market = 1000
	rate_exchange = 1000000
	boombust = 0
	time_lasttick = 0
	negaslime = 0
	decayed_slimes = 0

	""" Load the market data for this server from the database. """
	def __init__(self, id_server = None):
		if(id_server != None):
			self.id_server = id_server

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM markets WHERE id_server = %s".format(
					ewcfg.col_slimes_casino,
					ewcfg.col_rate_market,
					ewcfg.col_rate_exchange,
					ewcfg.col_boombust,
					ewcfg.col_time_lasttick,
					ewcfg.col_slimes_revivefee,
					ewcfg.col_negaslime,
					ewcfg.col_clock,
					ewcfg.col_weather,
					ewcfg.col_day,
					ewcfg.col_decayed_slimes
				), (self.id_server, ))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.slimes_casino = result[0]
					self.rate_market = result[1]
					self.rate_exchange = result[2]
					self.boombust = result[3]
					self.time_lasttick = result[4]
					self.slimes_revivefee = result[5]
					self.negaslime = result[6]
					self.clock = result[7]
					self.weather = result[8]
					self.day = result[9]
					self.decayed_slimes = result[10]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO markets(id_server) VALUES(%s)", (id_server, ))

					conn.commit()
			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save market data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save the object.
			cursor.execute("REPLACE INTO markets({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_server,
				ewcfg.col_slimes_casino,
				ewcfg.col_rate_market,
				ewcfg.col_rate_exchange,
				ewcfg.col_boombust,
				ewcfg.col_time_lasttick,
				ewcfg.col_slimes_revivefee,
				ewcfg.col_negaslime,
				ewcfg.col_clock,
				ewcfg.col_weather,
				ewcfg.col_day,
				ewcfg.col_decayed_slimes
			), (
				self.id_server,
				self.slimes_casino,
				self.rate_market,
				self.rate_exchange,
				self.boombust,
				self.time_lasttick,
				self.slimes_revivefee,
				self.negaslime,
				self.clock,
				self.weather,
				self.day,
				self.decayed_slimes
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

""" User model for database persistence """
class EwUser:
	id_user = ""
	id_server = ""
	id_killer = ""

	slimes = 0
	slimecredit = 0
	slimelevel = 1
	hunger = 0
	totaldamage = 0
	bounty = 0
	weapon = ""
	weaponskill = 0
	weaponname = ""
	trauma = ""
	ghostbust = False
	inebriation = 0
	faction = ""
	poi = ""
	life_state = 0
	busted = False
	rr_challenger = ""

	time_lastkill = 0
	time_lastrevive = 0
	time_lastspar = 0
	time_lasthaunt = 0
	time_lastinvest = 0
	#For possible time limit
	time_last_rr = 0

	""" fix data in this object if it's out of acceptable ranges """
	def limit_fix(self):
		if self.hunger > ewutils.hunger_max_bylevel(self.slimelevel):
			self.hunger = ewutils.hunger_max_bylevel(self.slimelevel)

		if self.inebriation < 0:
			self.inebriation = 0

		if self.poi == '':
			self.poi = ewcfg.poi_id_downtown
			
	""" gain or lose slime, recording statistics and potentially leveling up. """
	def change_slimes(self, n = 0, source = None):
		change = int(n)
		self.slimes += change

		if n >= 0:
			ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimes, n = change)
			ewstats.track_maximum(user = self, metric = ewcfg.stat_max_slimes, value = self.slimes)

			if source == ewcfg.source_mining:
				ewstats.change_stat(user = self, metric = ewcfg.stat_slimesmined, n = change)
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimesmined, n = change)

			if source == ewcfg.source_killing:
				ewstats.change_stat(user = self, metric = ewcfg.stat_slimesfromkills, n = change)
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimesfromkills, n = change)

			# todo add source from farming
		else:
			change *= -1 # convert to positive number
			if source != ewcfg.source_spending and source != ewcfg.source_ghostification:
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimeloss, n = change)

			if source == ewcfg.source_damage:
				self.totaldamage += change
				ewstats.track_maximum(user = self, metric = ewcfg.stat_max_hitsurvived, value = change)

			if source == ewcfg.source_self_damage:
				self.totaldamage += change
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_selfdamage, n = change)

			if source == ewcfg.source_decay:
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimesdecayed, n = change)

			if source == ewcfg.source_haunter:
				ewstats.track_maximum(user = self, metric = ewcfg.stat_max_hauntinflicted, value = change)
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimeshaunted, n = change)

		# potentially level up
		new_level = ewutils.level_byslime(self.slimes)
		if new_level > self.slimelevel:
			self.slimelevel = new_level
			if self.life_state == ewcfg.life_state_corpse:
				ewstats.track_maximum(user = self, metric = ewcfg.stat_max_ghost_level, value = self.slimelevel)
			else:
				ewstats.track_maximum(user = self, metric = ewcfg.stat_max_level, value = self.slimelevel)
		
	def die(self, cause = None):
		if cause == ewcfg.cause_busted:
			self.busted = True
		else:
			self.busted = False  # reset busted state on normal death; potentially move this to ewspooky.revive
			self.life_state = ewcfg.life_state_corpse
			ewstats.increment_stat(user = self, metric = ewcfg.stat_lifetime_deaths)
			ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimeloss, n = self.slimes)
			if cause != ewcfg.cause_killing and cause != ewcfg.cause_suicide:
				ewstats.increment_stat(user = self, metric = ewcfg.stat_lifetime_pve_deaths)
		self.slimes = 0
		self.poi = ewcfg.poi_id_thesewers
		self.bounty = 0
		self.totaldamage = 0
		self.slimelevel = 1
		self.hunger = 0
		self.inebriation = 0
		self.ghostbust = False
		# Clear weapon and weaponskill.
		self.weapon = ""
		self.weaponskill = 0
		ewutils.weaponskills_clear(id_server = self.id_server, id_user = self.id_user)
		ewstats.clear_on_death(id_server = self.id_server, id_user = self.id_user)
		ewitem.item_destroyall(id_server = self.id_server, id_user = self.id_user)

		ewutils.logMsg('server {}: {} was killed by {} - cause was {}'.format(self.id_server, self.id_user, self.id_killer, cause))

	def add_bounty(self, n = 0):
		self.bounty += int(n)
		ewstats.track_maximum(user = self, metric = ewcfg.stat_max_bounty, value = self.bounty)

	def change_slimecredit(self, n = 0, coinsource = None):
		change = int(n)
		self.slimecredit += change

		if change >= 0:
			ewstats.track_maximum(user = self, metric = ewcfg.stat_max_slimecredit, value = self.slimecredit)
			ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_slimecredit, n = change)
			if coinsource == ewcfg.coinsource_bounty:
				ewstats.change_stat(user = self, metric = ewcfg.stat_bounty_collected, n = change)
			if coinsource == ewcfg.coinsource_casino:
				ewstats.track_maximum(user = self, metric = ewcfg.stat_biggest_casino_win, value = change)
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_casino_winnings, n = change)
		else:
			change *= -1
			if coinsource == ewcfg.coinsource_revival:
				ewstats.change_stat(user = self, metric = ewcfg.stat_slimecredit_spent_on_revives, n = change)
			if coinsource == ewcfg.coinsource_casino:
				ewstats.track_maximum(user = self, metric = ewcfg.stat_biggest_casino_loss, value = change)
				ewstats.change_stat(user = self, metric = ewcfg.stat_lifetime_casino_losses, n = change)

	def add_weaponskill(self, n = 0):
		# Save the current weapon's skill
		if self.weapon != None and self.weapon != "":
			if self.weaponskill == None:
				self.weaponskill = 0
				self.weaponname = ""

			self.weaponskill += int(n)
			ewstats.track_maximum(user = self, metric = ewcfg.stat_max_wepskill, value = self.weaponskill)

			ewutils.weaponskills_set(
				id_server = self.id_server,
				id_user = self.id_user,
				weapon = self.weapon,
				weaponskill = self.weaponskill,
				weaponname = self.weaponname
			)

	def eat(self, food_item = None):
		item_props = food_item.item_props

		if float(food_item.time_expir if food_item.time_expir is not None else 0) < time.time():
			response = "You realize that the food you were trying to eat is already spoiled. In disgust, you throw it away."
		else:
			self.hunger -= int(item_props['recover_hunger'])
			if self.hunger < 0:
				self.hunger = 0
			self.inebriation += int(item_props['inebriation'])
			if self.inebriation > 20:
				self.inebriation = 20

			if food_item.id_item == "coleslaw":
				self.ghostbust = True

			response = item_props['str_eat'] + ("\n\nYou're stuffed!" if self.hunger <= 0 else "")

		ewitem.item_delete(food_item.id_item)

		return response

	""" Create a new EwUser and optionally retrieve it from the database. """
	def __init__(self, member = None, id_user = None, id_server = None):
		if(id_user == None) and (id_server == None):
			if(member != None):
				id_server = member.server.id
				id_user = member.id

		# Retrieve the object from the database if the user is provided.
		if(id_user != None) and (id_server != None):
			self.id_server = id_server
			self.id_user = id_user

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM users WHERE id_user = %s AND id_server = %s".format(
					ewcfg.col_slimes,
					ewcfg.col_slimelevel,
					ewcfg.col_hunger,
					ewcfg.col_totaldamage,
					ewcfg.col_bounty,
					ewcfg.col_weapon,
					ewcfg.col_trauma,
					ewcfg.col_slimecredit,
					ewcfg.col_time_lastkill,
					ewcfg.col_time_lastrevive,
					ewcfg.col_id_killer,
					ewcfg.col_time_lastspar,
					ewcfg.col_time_lasthaunt,
					ewcfg.col_time_lastinvest,
					ewcfg.col_weaponname,
					ewcfg.col_ghostbust,
					ewcfg.col_inebriation,
					ewcfg.col_faction,
					ewcfg.col_poi,
					ewcfg.col_life_state,
					ewcfg.col_busted,
					ewcfg.col_rrchallenger
				), (
					id_user,
					id_server
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.slimes = result[0]
					self.slimelevel = result[1]
					self.hunger = result[2]
					self.totaldamage = result[3]
					self.bounty = result[4]
					self.weapon = result[5]
					self.trauma = result[6]
					self.slimecredit = result[7]
					self.time_lastkill = result[8]
					self.time_lastrevive = result[9]
					self.id_killer = result[10]
					self.time_lastspar = result[11]
					self.time_lasthaunt = result[12]
					self.time_lastinvest = result[13]
					self.weaponname = result[14]
					self.ghostbust = (result[15] == 1)
					self.inebriation = result[16]
					self.faction = result[17]
					self.poi = result[18]
					self.life_state = result[19]
					self.busted = (result[20] == 1)
					self.rr_challenger = result[21]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO users(id_user, id_server, poi, life_state) VALUES(%s, %s, %s, %s)", (
						id_user,
						id_server,
						ewcfg.poi_id_downtown,
						ewcfg.life_state_juvenile
					))
					
					conn.commit()

				# Get the skill for the user's current weapon.
				if self.weapon != None and self.weapon != "":
					skills = ewutils.weaponskills_get(
						id_server = id_server,
						id_user = id_user
					)
					skill_data = skills.get(self.weapon)
					if skill_data != None:
						self.weaponskill = skill_data['skill']
						self.weaponname = skill_data['name']
					else:
						self.weaponskill = 0
						self.weaponname = ""

					if self.weaponskill == None:
						self.weaponskill = 0
						self.weaponname = ""
				else:
					self.weaponskill = 0
					self.weaponname = ""

				self.limit_fix();
			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save this user object to the database. """
	def persist(self):
	
		try:
			# Get database handles if they weren't passed.
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			self.limit_fix();

			# Save the object.
			# Todo Preserve Farming Data 	farmActive, plantType, time_lastsow
			cursor.execute("REPLACE INTO users({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_user,
				ewcfg.col_id_server,
				ewcfg.col_slimes,
				ewcfg.col_slimelevel,
				ewcfg.col_hunger,
				ewcfg.col_totaldamage,
				ewcfg.col_bounty,
				ewcfg.col_weapon,
				ewcfg.col_weaponskill,
				ewcfg.col_trauma,
				ewcfg.col_slimecredit,
				ewcfg.col_time_lastkill,
				ewcfg.col_time_lastrevive,
				ewcfg.col_id_killer,
				ewcfg.col_time_lastspar,
				ewcfg.col_time_lasthaunt,
				ewcfg.col_time_lastinvest,
				ewcfg.col_weaponname,
				ewcfg.col_ghostbust,
				ewcfg.col_inebriation,
				ewcfg.col_faction,
				ewcfg.col_poi,
				ewcfg.col_life_state,
				ewcfg.col_busted,
				ewcfg.col_rrchallenger
			), (
				self.id_user,
				self.id_server,
				self.slimes,
				self.slimelevel,
				self.hunger,
				self.totaldamage,
				self.bounty,
				self.weapon,
				self.weaponskill,
				self.trauma,
				self.slimecredit,
				self.time_lastkill,
				self.time_lastrevive,
				self.id_killer,
				self.time_lastspar,
				self.time_lasthaunt,
				self.time_lastinvest,
				self.weaponname,
				(1 if self.ghostbust else 0),
				self.inebriation,
				self.faction,
				self.poi,
				self.life_state,
				(1 if self.busted else 0),
				self.rr_challenger
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)
