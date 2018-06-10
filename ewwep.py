import time
import random

import ewcmd
import ewcfg
import ewutils
from ew import EwUser, EwMarket

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
		id_weapon = "",
		alias = [],
		str_equip = "",
		str_kill = "",
		str_trauma = "",
		str_trauma_self = "",
		str_weapon = "",
		str_weapon_self = "",
		str_damage = "",
		str_duel = "",
		str_weaponmaster = "",
		str_weaponmaster_self = "",
		fn_effect = None,
		str_crit = "",
		str_miss = ""
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
			miss = self.miss,
			crit = self.crit,
			strikes = self.strikes,
			slimes_damage = self.slimes_damage,
			slimes_spent = self.slimes_spent
		))

	def __init__(
		self,
		miss = False,
		crit = False,
		strikes = 0,
		slimes_damage = 0,
		slimes_spent = 0,
		user_data = None,
		shootee_data = None
	):
		self.miss = miss
		self.crit = crit
		self.strikes = strikes
		self.slimes_damage = slimes_damage
		self.slimes_spent = slimes_spent
		self.user_data = user_data
		self.shootee_data = shootee_data

""" Player deals damage to a ghost. """
async def attack(cmd):
	resp = await ewcmd.start(cmd)
	time_now = int(time.time())
	response = ""

	user_data = EwUser(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_combatzone:
		response = "You must go to the #{} to commit gang violence.".format(ewcfg.channel_combatzone)
	elif cmd.mentions_count > 1:
		response = "One shot at a time!"
	elif cmd.mentions_count <= 0:
		response = "Your bloodlust is appreciated, but ENDLESS WAR didn\'t understand that name."
	elif user_data.stamina >= ewcfg.stamina_max:
		response = "You are too exhausted for gang violence right now. Go get some grub!"
	elif cmd.mentions_count == 1:
		# The roles assigned to the author of this message.
		roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

		# Get shooting player's info
		try:
			conn = ewutils.databaseConnect()
			cursor = conn.cursor()

			if user_data.slimelevel <= 0:
				user_data.slimelevel = 1

			# Flag the shooter for PvP no matter what happens next.
			user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))
			user_data.persist(conn = conn, cursor = cursor)

			# Get target's info.
			member = cmd.mentions[0]
			shootee_data = EwUser(member = member, conn = conn, cursor = cursor)

			conn.commit()
		finally:
			cursor.close()
			conn.close()

		miss = False
		crit = False
		strikes = 0

		# Shot player's assigned Discord roles.
		roles_map_target = ewutils.getRoleMap(member.roles)

		# Slime level data. Levels are in powers of 10.
		slimes_bylevel = int((10 ** user_data.slimelevel) / 10)
		slimes_spent = int(slimes_bylevel / 10)
		slimes_damage = int((slimes_bylevel / 5.0) * (100 + (user_data.weaponskill * 5)) / 100.0)
		slimes_dropped = shootee_data.totaldamage

		fumble_chance = (random.randrange(10) - 4)
		if fumble_chance > user_data.weaponskill:
			miss = True

		user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkillers in roles_map_user
		user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user

		# Add the PvP flag role.
		await ewutils.add_pvp_role(cmd = cmd)

		if ewcfg.role_copkiller in roles_map_target or ewcfg.role_rowdyfucker in roles_map_target:
			# Disallow killing generals.
			response = "He is hiding in his ivory tower and playing video games like a retard."

		elif (slimes_spent > user_data.slimes):
			# Not enough slime to shoot.
			response = "You don't have enough slime to attack. ({:,}/{:,})".format(user_data.slimes, slimes_spent)

		elif (time_now - user_data.time_lastkill) < ewcfg.cd_kill:
			# disallow kill if the player has killed recently
			response = "Take a moment to appreciate your last slaughter."

		elif shootee_data.id_killer == user_data.id_user:
			# Don't allow the shootee to be shot by the same player twice.
			response = "You have already proven your superiority over {}.".format(member.display_name)

		elif time_now > shootee_data.time_expirpvp:
			# Target is not flagged for PvP.
			response = "{} is not mired in the ENDLESS WAR right now.".format(member.display_name)

		elif user_iskillers == False and user_isrowdys == False:
			# Only killers, rowdys, the cop killer, and rowdy fucker can shoot people.
			if ewcfg.role_juvenile in roles_map_user:
				response = "Juveniles lack the moral fiber necessary for violence."
			else:
				response = "You lack the moral fiber necessary for violence."

		elif (time_now - shootee_data.time_lastrevive) < ewcfg.invuln_onrevive:
			# User is currently invulnerable.
			response = "{} has died too recently and is immune.".format(member.display_name)
		
		elif ewcfg.role_corpse in roles_map_target and ewcfg.role_corpse_pvp not in roles_map_target:
			# Target is already dead and not a ghost.
			response = "{} is already dead.".format(member.display_name)
		
		elif ewcfg.role_corpse_pvp in roles_map_target and user_data.ghostbust == False:
			# Target is a ghost, user can't attack ghosts:
			response = "{} is already dead.".format(member.display_name)
		
		elif ewcfg.role_corpse_pvp in roles_map_target and user_data.ghostbust == True:
			# Attack a ghostly target
			role_corpse = cmd.roles_map[ewcfg.role_corpse]

			was_busted = False
			was_shot = True

			if was_shot:
				#stamina drain
				user_data.stamina += ewcfg.stamina_pershot
				
				# Weaponized flavor text.
				weapon = ewcfg.weapon_map.get(user_data.weapon)
				randombodypart = ewcfg.hitzone_list[random.randrange(len(ewcfg.hitzone_list))]

				# Weapon-specific adjustments
				if weapon != None and weapon.fn_effect != None:
					# Build effect container
					ctn = EwEffectContainer(
						miss = miss,
						crit = crit,
						slimes_damage = slimes_damage,
						slimes_spent = slimes_spent,
						user_data = user_data,
						shootee_data = shootee_data
					)

					# Make adjustments
					weapon.fn_effect(ctn)

					# Apply effects for non-reference values
					miss = ctn.miss
					crit = ctn.crit
					slimes_damage = ctn.slimes_damage
					slimes_spent = ctn.slimes_spent
					strikes = ctn.strikes
					# user_data and shootee_data should be passed by reference, so there's no need to assign them back from the effect container.

					if miss:
						slimes_damage = 0

				# Remove !revive invulnerability.
				user_data.time_lastrevive = 0
				user_data.slimes -= slimes_spent

				# Remove repeat killing protection if.
				if user_data.id_killer == shootee_data.id_user:
					user_data.id_killer = ""

				# Don't allow attacking to cause you to go negative.
				if user_data.slimes < 0:
					user_data.slimes = 0

				if slimes_damage >= -shootee_data.slimes:
					was_busted = True

				if was_busted:
					# Move around slime as a result of the shot.
					market_data = EwMarket(id_server = cmd.message.server.id)
					coinbounty = int(shootee_data.bounty / (market_data.rate_exchange / 1000000.0))
					user_data.slimecredit += coinbounty

					# Player was busted.
					shootee_data.slimes = 0
					shootee_data.slimepoudrins = 0
					shootee_data.bounty = 0

					response = "{name_target}\'s ghost has been **BUSTED**!!".format(name_target = member.display_name)
					
					if coinbounty > 0:
						response += "\n\n SlimeCorp transfers {} SlimeCoin to {}\'s account.".format(str(coinbonty), message.author.display_name)

					#adjust busts
					user_data.busts += 1

				else:
					# A non-lethal blow!
					shootee_data.slimes += slimes_damage

					if weapon != None:
						if miss:
							response = "{}".format(weapon.str_miss.format(
								name_player = cmd.message.author.display_name,
								name_target = member.display_name + "\'s ghost"
							))
						else:
							response = weapon.str_damage.format(
								name_player = cmd.message.author.display_name,
								name_target = member.display_name + "\'s ghost",
								hitzone = randombodypart,
								strikes = strikes
							)
							if crit:
								response += " {}".format(weapon.str_crit.format(
									name_player = cmd.message.author.display_name,
									name_target = member.display_name + "\'s ghost"
								))
					else:
						if miss:
							response = "{}\'s ghost is unharmed.".format(member.display_name)
						else:
							response = "{}\'s ghost is hit!!".format(member.display_name)
			else:
				response = 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter {}.'.format(member.display_name)

			# Level up the player if appropriate.
			new_level = len(str(int(user_data.slimes)))
			if new_level > user_data.slimelevel:
				response += "\n\n{} has been empowered by slime and is now a level {} slimeboi!".format(cmd.message.author.display_name, new_level)
				user_data.slimelevel = new_level

			# Give slimes to the boss if possible.
			boss_member = None
			if boss_slimes > 0:
				for member_search in cmd.message.server.members:
					if role_boss in ewutils.getRoleMap(member_search.roles):
						boss_member = member_search
						break

			# Persist every users' data.
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data.persist(conn = conn, cursor = cursor)
				shootee_data.persist(conn = conn, cursor = cursor)

				if boss_member != None:
					boss_data = EwUser(member = boss_member, conn = conn, cursor = cursor)
					boss_data.slimes += boss_slimes
					boss_data.persist(conn = conn, cursor = cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()

			# Assign the corpse role to the newly dead player.
			if was_killed:
				await cmd.client.replace_roles(member, role_corpse)

		else:
			# Slimes from this shot might be awarded to the boss.
			role_boss = (ewcfg.role_copkiller if user_iskillers else ewcfg.role_rowdyfucker)
			boss_slimes = 0

			role_corpse = cmd.roles_map[ewcfg.role_corpse]

			was_juvenile = False
			was_killed = False
			was_shot = False

			if (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)) or (ewcfg.role_juvenile in roles_map_target):
				# User can be shot.
				if ewcfg.role_juvenile in roles_map_target:
					was_juvenile = True

				was_shot = True

			if was_shot:
				#stamina drain
				user_data.stamina += ewcfg.stamina_pershot
				
				# Weaponized flavor text.
				weapon = ewcfg.weapon_map.get(user_data.weapon)
				randombodypart = ewcfg.hitzone_list[random.randrange(len(ewcfg.hitzone_list))]

				# Weapon-specific adjustments
				if weapon != None and weapon.fn_effect != None:
					# Build effect container
					ctn = EwEffectContainer(
						miss = miss,
						crit = crit,
						slimes_damage = slimes_damage,
						slimes_spent = slimes_spent,
						user_data = user_data,
						shootee_data = shootee_data
					)

					# Make adjustments
					weapon.fn_effect(ctn)

					# Apply effects for non-reference values
					miss = ctn.miss
					crit = ctn.crit
					slimes_damage = ctn.slimes_damage
					slimes_spent = ctn.slimes_spent
					strikes = ctn.strikes
					# user_data and shootee_data should be passed by reference, so there's no need to assign them back from the effect container.

					if miss:
						slimes_damage = 0

				# Remove !revive invulnerability.
				user_data.time_lastrevive = 0
				user_data.slimes -= slimes_spent

				# Remove repeat killing protection if.
				if user_data.id_killer == shootee_data.id_user:
					user_data.id_killer = ""

				# Don't allow attacking to cause you to go negative.
				if user_data.slimes < 0:
					user_data.slimes = 0

				if slimes_damage >= shootee_data.slimes:
					was_killed = True

				if was_killed:
					# Move around slime as a result of the shot.
					if shootee_data.slimes > 0:
						if was_juvenile:
							user_data.slimes += (slimes_dropped + shootee_data.slimes)
							user_data.slimepoudrins += shootee_data.slimepoudrins
						else:
							market_data = EwMarket(id_server = cmd.message.server.id)
							coinbounty = int(shootee_data.bounty / (market_data.rate_exchange / 1000000.0))
							user_data.slimecredit += coinbounty
							user_data.slimes += int(slimes_dropped / 2)
							user_data.slimepoudrins += shootee_data.slimepoudrins
							boss_slimes += int(slimes_dropped / 2)

					# Player was killed.
					shootee_data.totaldamage += shootee_data.slimes
					shootee_data.slimes = -int(shootee_data.totaldamage / 10)
					shootee_data.slimepoudrins = 0
					shootee_data.id_killer = user_data.id_user
					shootee_data.bounty = 0

					if weapon != None:
						response = weapon.str_damage.format(
							name_player = cmd.message.author.display_name,
							name_target = member.display_name,
							hitzone = randombodypart,
							strikes = strikes
						)
						if crit:
							response += " {}".format(weapon.str_crit.format(
								name_player = cmd.message.author.display_name,
								name_target = member.display_name
							))

						response += "\n\n{}".format(weapon.str_kill.format(
							name_player = cmd.message.author.display_name,
							name_target = member.display_name,
							emote_skull = ewcfg.emote_slimeskull
						))
						shootee_data.trauma = weapon.id_weapon
					else:
						response = "{name_target} is hit!!\n\n{name_target} has died.".format(name_target = member.display_name)
						shootee_data.trauma = ""
					
					if coinbounty > 0:
						response += "\n\n SlimeCorp transfers {} SlimeCoin to {}\'s account.".format(str(coinbonty), message.author.display_name)

					#adjust kills bounty
					user_data.kills += 1
					user_data.bounty += int((shootee_data.bounty / 2) + (shootee_data.totaldamage / 4))

					# Give a bonus to the player's weapon skill for killing a stronger player.
					if shootee_data.slimelevel > user_data.slimelevel:
						user_data.weaponskill += 1

				else:
					# A non-lethal blow!
					shootee_data.slimes -= slimes_damage
					shootee_data.totaldamage += slimes_damage

					if weapon != None:
						if miss:
							response = "{}".format(weapon.str_miss.format(
								name_player = cmd.message.author.display_name,
								name_target = member.display_name
							))
						else:
							response = weapon.str_damage.format(
								name_player = cmd.message.author.display_name,
								name_target = member.display_name,
								hitzone = randombodypart,
								strikes = strikes
							)
							if crit:
								response += " {}".format(weapon.str_crit.format(
									name_player = cmd.message.author.display_name,
									name_target = member.display_name
								))
					else:
						if miss:
							response = "{} is unharmed.".format(member.display_name)
						else:
							response = "{} is hit!!".format(member.display_name)
			else:
				response = 'ENDLESS WAR finds this betrayal stinky. He will not allow you to slaughter {}.'.format(member.display_name)

			# Level up the player if appropriate.
			new_level = len(str(int(user_data.slimes)))
			if new_level > user_data.slimelevel:
				response += "\n\n{} has been empowered by slime and is now a level {} slimeboi!".format(cmd.message.author.display_name, new_level)
				user_data.slimelevel = new_level

			# Give slimes to the boss if possible.
			boss_member = None
			if boss_slimes > 0:
				for member_search in cmd.message.server.members:
					if role_boss in ewutils.getRoleMap(member_search.roles):
						boss_member = member_search
						break

			# Persist every users' data.
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data.persist(conn = conn, cursor = cursor)
				shootee_data.persist(conn = conn, cursor = cursor)

				if boss_member != None:
					boss_data = EwUser(member = boss_member, conn = conn, cursor = cursor)
					boss_data.slimes += boss_slimes
					boss_data.persist(conn = conn, cursor = cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()

			# Assign the corpse role to the newly dead player.
			if was_killed:
				await cmd.client.replace_roles(member, role_corpse)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" equip a weapon """
async def equip(cmd):
	resp = await ewcmd.start(cmd)
	response = ""

	if cmd.message.channel.name != ewcfg.channel_dojo:
		response = "You must go to the #{} to change your equipment.".format(ewcfg.channel_dojo)
	else:
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]

		weapon = ewcfg.weapon_map.get(value)
		if weapon != None:
			response = weapon.str_equip
			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)
				user_skills = ewutils.weaponskills_get(member = cmd.message.author, conn = conn, cursor = cursor)

				user_data.weapon = weapon.id_weapon
				weaponskillinfo = user_skills.get(weapon.id_weapon)
				if weaponskillinfo == None:
					user_data.weaponskill = 0
					user_data.weaponname = ""
				else:
					user_data.weaponskill = weaponskillinfo.get('skill')
					user_data.weaponname = weaponskillinfo.get('name')

				user_data.persist(conn = conn, cursor = cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()
		else:
			response = "Choose your weapon: {}".format(ewutils.formatNiceList(names = ewcfg.weapon_names, conjunction = "or"))

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" player kills themself """
async def suicide(cmd):
	resp = await ewcmd.start(cmd)
	response = ""

	# Only allowed in the combat zone.
	if cmd.message.channel.name != ewcfg.channel_combatzone:
		response = "You must go to the #{} to commit suicide.".format(ewcfg.channel_combatzone)
	else:
		# Get the user data.
		user_data = EwUser(member = cmd.message.author)

		# The roles assigned to the author of this message.
		roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

		# Slime transfer
		boss_slimes = user_data.slimes - (ewcfg.slimes_tokill + int(user_data.slimes * 3 / 5))

		user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
		user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user
		user_isgeneral = ewcfg.role_copkiller in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user
		user_isjuvenile = ewcfg.role_juvenile in roles_map_user
		user_isdead = ewcfg.role_corpse in roles_map_user

		if user_isdead:
			response = "Too late for that."
		elif user_isjuvenile:
			response = "Juveniles are too cowardly for suicide."
		elif user_isgeneral:
			response = "\*click* Alas, your gun has jammed."
		elif user_iskillers or user_isrowdys:
			role_corpse = cmd.roles_map[ewcfg.role_corpse]

			# Assign the corpse role to the player. He dead.
			await cmd.client.replace_roles(cmd.message.author, role_corpse)

			# Set the id_killer to the player himself, remove his slime and slime poudrins.
			user_data.id_killer = cmd.message.author.id
			user_data.slimes = 0
			user_data.slimepoudrins = 0
			user_data.persist()

			# Give slimes to the boss if possible.
			boss_member = None
			if boss_slimes > 0:
				role_boss = (ewcfg.role_copkiller if user_iskillers == True else ewcfg.role_rowdyfucker)

				for member_search in cmd.message.author.server.members:
					boss_roles = ewutils.getRoleMap(member_search.roles)
					if role_boss in boss_roles and ewcfg.role_kingpin in boss_roles:
						boss_member = member_search
						break

				if boss_member != None:
					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						boss_data = EwUser(member = boss_member, conn = conn, cursor = cursor)
						boss_data.slimes += boss_slimes
						boss_data.persist(conn = conn, cursor = cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

			response = '{} has willingly returned to the slime. {}'.format(cmd.message.author.display_name, ewcfg.emote_slimeskull)
		else:
			# This should never happen. We handled all the role cases. Just in case.
			response = "\*click* Alas, your gun has jammed."

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" Player spars with a friendly player to gain slime. """
async def spar(cmd):
	resp = await ewcmd.start(cmd)
	time_now = int(time.time())
	response = ""

	if cmd.message.channel.name != ewcfg.channel_dojo:
		response = "You must go to the #{} to spar.".format(ewcfg.channel_dojo)

	elif cmd.mentions_count > 1:
		response = "One sparring partner at a time!"
		
	elif cmd.mentions_count == 1:
		member = cmd.mentions[0]

		if(member.id == cmd.message.author.id):
			response = "How do you expect to spar with yourself?"
		else:
			# The roles assigned to the author of this message.
			roles_map_user = ewutils.getRoleMap(cmd.message.author.roles)

			try:
				conn = ewutils.databaseConnect()
				cursor = conn.cursor()

				# Get killing player's info.
				user_data = EwUser(member = cmd.message.author, conn = conn, cursor = cursor)

				# Get target's info.
				sparred_data = EwUser(member = member, conn = conn, cursor = cursor)

				conn.commit()
			finally:
				cursor.close()
				conn.close()

			user_iskillers = ewcfg.role_copkillers in roles_map_user or ewcfg.role_copkiller in roles_map_user
			user_isrowdys = ewcfg.role_rowdyfuckers in roles_map_user or ewcfg.role_rowdyfucker in roles_map_user
			user_idead = ewcfg.role_corpse in roles_map_user

			if user_data.stamina >= ewcfg.stamina_max:
				response = "You are too exhausted to train right now. Go get some grub!"
			elif sparred_data.stamina >= ewcfg.stamina_max:
				response = "{} is too exhausted to train right now. They need a snack!".format(member.display_name)
			elif user_isdead == True:
				response = "The dead think they're too cool for conventional combat. Pricks."
			elif user_iskillers == False and user_isrowdys == False:
				# Only killers, rowdys, the cop killer, and the rowdy fucker can spar
				response = "Juveniles lack the backbone necessary for combat."
			else:
				was_juvenile = False
				was_sparred = False
				was_dead = False
				was_player_tired = False
				was_target_tired = False
				was_enemy = False
				duel = False

				roles_map_target = ewutils.getRoleMap(member.roles)

				#Determine if the !spar is a duel:
				weapon = None
				if user_data.weapon != None and user_data.weapon != "" and user_data.weapon == sparred_data.weapon:
					weapon = ewcfg.weapon_map.get(user_data.weapon)
					duel = True

				if ewcfg.role_corpse in roles_map_target:
					# Target is already dead.
					was_dead = True
				elif (user_data.time_lastspar + ewcfg.cd_spar) > time_now:
					# player sparred too recently
					was_player_tired = True
				elif (sparred_data.time_lastspar + ewcfg.cd_spar) > time_now:
					# taret sparred too recently
					was_target_tired = True
				elif ewcfg.role_juvenile in roles_map_target:
					# Target is a juvenile.
					was_juvenile = True

				elif (user_iskillers and (ewcfg.role_copkillers in roles_map_target)) or (user_isrowdys and (ewcfg.role_rowdyfuckers in roles_map_target)):
					# User can be sparred.
					was_sparred = True
				elif (user_iskillers and (ewcfg.role_rowdyfuckers in roles_map_target)) or (user_isrowdys and (ewcfg.role_copkillers in roles_map_target)):
					# Target is a member of the opposing faction.
					was_enemy = True


				#if the duel is successful
				if was_sparred:
					weaker_player = sparred_data if sparred_data.slimes < user_data.slimes else user_data
					stronger_player = sparred_data if user_data is weaker_player else user_data

					# Flag the player for PvP
					user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, (time_now + ewcfg.time_pvp_kill))

					# Weaker player gains slime based on the slime of the stronger player.
					possiblegain = (ewcfg.slimes_perspar_base * (2 ** weaker_player.slimelevel))
					slimegain = possiblegain if (stronger_player.slimes / 10) > possiblegain else (stronger_player.slimes / 10)
					weaker_player.slimes += slimegain
					
					#stamina drain for both players
					user_data.stamina += ewcfg.stamina_perspar
					sparred_data.stamina += ewcfg.stamina_perspar

					# Bonus 50% slime to both players in a duel.
					if duel:
						weaker_player.slimes += int(slimegain / 2)
						stronger_player.slimes += int(slimegain / 2)

						if weaker_player.weaponskill < 5:
							weaker_player.weaponskill += 1
						elif (weaker_player.weaponskill + 1) < stronger_player.weaponskill:
							weaker_player.weaponskill += 1

						if stronger_player.weaponskill < 5:
							stronger_player.weaponskill += 1

					weaker_player.time_lastspar = time_now

					try:
						conn = ewutils.databaseConnect()
						cursor = conn.cursor()

						user_data.persist(conn = conn, cursor = cursor)
						sparred_data.persist(conn = conn, cursor = cursor)

						conn.commit()
					finally:
						cursor.close()
						conn.close()

					# Add the PvP flag role.
					await ewutils.add_pvp_role(cmd = cmd)

					# player was sparred with
					if duel and weapon != None:
						response = weapon.str_duel.format(name_player = cmd.message.author.display_name, name_target = member.display_name)
					else:
						response = '{} parries the attack. :knife: {}'.format(member.display_name, ewcfg.emote_slime5)

					#Notify if max skill is reached	
					if weapon != None:
						if user_data.weaponskill == 5:
							response += ' {} is a master of the {}.'.format(cmd.message.author.display_name, weapon.id_weapon)
						if sparred_data.weaponskill == 5:
							response += ' {} is a master of the {}.'.format(member.display_name, weapon.id_weapon)

				else:
					if was_dead:
						# target is already dead
						response = '{} is already dead.'.format(member.display_name)
					elif was_target_tired:
						# target has sparred too recently
						response = '{} is too tired to spar right now.'.format(member.display_name)
					elif was_player_tired:
						# player has sparred too recently
						response = 'You are too tired to spar right now.'
					elif was_enemy:
						# target and player are different factions
						response = "You cannot spar with your enemies."
					else:
						#otherwise unkillable
						response = '{} cannot spar now.'.format(member.display_name)
	else:
		response = 'Your fighting spirit is appreciated, but ENDLESS WAR didn\'t understand that name.'

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))

""" name a weapon using a slime poudrin """
async def annoint(cmd):
	resp = await ewcmd.start(cmd)
	response = ""

	if cmd.tokens_count < 2:
		response = "Specify a name for your weapon!"
	else:
		annoint_name = cmd.message.content[(len(ewcfg.cmd_annoint)):].strip()

		if len(annoint_name) > 32:
			response = "That name is too long. ({:,}/32)".format(len(annoint_name))
		else:
			user_data = EwUser(member = cmd.message.author)

			if user_data.slimepoudrins < 1:
				response = "You need a slime poudrin."
			elif user_data.slimes < 100:
				response = "You need more slime."
			elif user_data.weapon == "":
				response = "Equip a weapon first."
			else:
				# Perform the ceremony.
				user_data.slimes -= 100
				user_data.slimepoudrins -= 1
				user_data.weaponname = annoint_name

				if user_data.weaponskill < 10:
					user_data.weaponskill += 1

				user_data.persist()

				response = "You place your weapon atop the poudrin and annoint it with slime. It is now known as {}!\n\nThe name draws you closer to your weapon. The poudrin was destroyed in the process.".format(annoint_name)

	# Send the response to the player.
	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
