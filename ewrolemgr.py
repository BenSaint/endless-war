import asyncio

import ewcfg
import ewutils

from ew import EwUser


"""
	Fix the Discord roles assigned to this member.
"""
async def updateRoles(
	client = None,
	member = None
):
	user_data = EwUser(member = member)

	roles_map = ewutils.getRoleMap(member.server.roles)
	roles_map_user = ewutils.getRoleMap(member.roles)

	if user_data.life_state != ewcfg.life_state_kingpin and ewcfg.role_kingpin in roles_map_user:
		# Fix the life_state of kingpins, if somehow it wasn't set.
		user_data.life_state = ewcfg.life_state_kingpin
		user_data.persist()
	elif user_data.life_state != ewcfg.life_state_grandfoe and ewcfg.role_grandfoe in roles_map_user:
		# Fix the life_state of a grand foe.
		user_data.life_state = ewcfg.life_state_grandfoe
		user_data.persist()

	faction_roles_remove = [
		ewcfg.role_juvenile,
		ewcfg.role_juvenile_pvp,
		ewcfg.role_rowdyfuckers,
		ewcfg.role_rowdyfuckers_pvp,
		ewcfg.role_copkillers,
		ewcfg.role_copkillers_pvp,
		ewcfg.role_corpse,
		ewcfg.role_corpse_pvp,
		ewcfg.role_kingpin,
		ewcfg.role_grandfoe
	]

	# Manage faction roles.
	faction_role = ewutils.get_faction(user_data = user_data)

	faction_roles_remove.remove(faction_role)

	# Manage location roles.
	poi_role = None

	poi = ewcfg.id_to_poi.get(user_data.poi)
	if poi != None:
		poi_role = poi.role

	poi_roles_remove = []
	for poi in ewcfg.poi_list:
		if poi.role != None and poi.role != poi_role:
			poi_roles_remove.append(poi.role)

	role_names = []
	for roleName in roles_map_user:
		if roleName not in faction_roles_remove and roleName not in poi_roles_remove:
			role_names.append(roleName)

	if faction_role not in role_names:
		role_names.append(faction_role)
	if poi_role != None and poi_role not in role_names:
		role_names.append(poi_role)

	replacement_roles = []
	for name in role_names:
		role = roles_map.get(name)

		if role != None:
			replacement_roles.append(role)
		else:
			ewutils.logMsg("error: role missing \"{}\"".format(name))

	try:
		await client.replace_roles(member, *replacement_roles)
	except:
		ewutils.logMsg('error: failed to replace roles for {}'.format(member.display_name))
