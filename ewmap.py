import asyncio

from copy import deepcopy

import ewutils
import ewcmd
import ewrolemgr
import ewcfg

from ew import EwUser

# Map of user IDs to their course ID.
moves_active = {}
move_counter = 0

"""
	Returns true if the specified point of interest is a PvP zone.
"""
def poi_is_pvp(poi_name = None):
	poi = ewcfg.id_to_poi.get(poi_name)

	if poi != None:
		return poi.pvp
	
	return False

"""
	Returns true if the specified name is used by any POI.
"""
def channel_name_is_poi(channel_name):
	if channel_name != None:
		for poi in ewcfg.poi_list:
			if poi.channel == channel_name:
				return True

	return False

"""
	Point of Interest (POI) data model
"""
class EwPoi:
	# The typable single-word ID of this location.
	id_poi = ""

	# Acceptable alternative typable single-word names for this place.
	alias = []

	# The nice name for this place.
	str_name = ""

	# You find yourself $str_in $str_name
	str_in = "in"

	# You $str_enter $str_name
	str_enter = "enter"

	# A description provided when !look-ing here.
	str_desc = ""

	# (X, Y) location on the map (left, top) zero-based origin.
	coord = None
	coord_alias = []

	# Channel name associated with this POI
	channel = ""

	# Discord role associated with this zone (control channel visibility).
	role = None

	# Zone allows PvP combat and interactions.
	pvp = True

	# Factions allowed in this zone.
	factions = []

	# Life states allowed in this zone.
	life_states = []

	# If true, the zone is inaccessible.
	closed = False

	# Message shown before entering the zone fails when it's closed.
	str_closed = None

	# Vendor names available at this POI.
	vendors = []

	def __init__(
		self,
		id_poi = "unknown", 
		alias = [],
		str_name = "Unknown",
		str_desc = "...",
		str_in = "in",
		str_enter = "enter",
		coord = None,
		coord_alias = [],
		channel = "",
		role = None,
		pvp = True,
		factions = [],
		life_states = [],
		closed = False,
		str_closed = None,
		vendors = [],
	):
		self.id_poi = id_poi
		self.alias = alias
		self.str_name = str_name
		self.str_desc = str_desc
		self.str_in = str_in
		self.str_enter = str_enter
		self.coord = coord
		self.coord_alias = coord_alias
		self.channel = channel
		self.role = role
		self.pvp = pvp
		self.factions = factions
		self.life_states = life_states
		self.closed = closed
		self.str_closed = str_closed
		self.vendors = vendors

map_world = [
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -2, 30,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0,  0, -1, -2, -1, -1, -1, 30, -1, -1, -1,  0, -1, -1, 30, -1, -1, -1, -1,  0,  0, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1,  5, -1,  0,  0,  0,  0, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, 30, -2, 30,  0, -1, -1,  0, -1, -1, 30, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0, -1, 30, -1, -1, -1, -1,  0, -1, -1, -2, 30,  0,  0,  0, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, 30,  0,  0,  0,  0,  0,  0, -1, 30, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1,  0, 30, -2,  5, -2, -1,  0, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -2, -1, -1, 30, -1, -1, -1,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1,  5, -1, -1,  0, -1, -1, -1,  0, -1, -1, -1, -2,  5, -2, 30,  0,  0,  0,  0,  0,  0,  0,  0, -1,  0,  0, 30, -2,  5, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1,  0,  0,  0,  0,  0, 30, -2, 30,  0,  0, -1, -1, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -2, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, 30, -1, -1, -1,  5, -1,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1,  0,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -2,  5, -2, -3, -3,  5, -2, -1, -2, -1,  0, -1, -1, -1, -1, -1,  0,  0, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1,  0, -1, -2, -1, -1, -1, -1, -1, -1, 30, -1, -3, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1,  0, -1,  5, -1, -1,  0,  0,  0,  0,  0, -1, -3,  5, -2, -1, -1, -1, 30, -2,  5, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1,  0, 30, -2, 30,  0,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, 30, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -2, 30,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0, -1, -1, 30, -1,  0,  0,  0,  0, 30, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2,  5, -1,  0, -1, -1,  0, 30, -2, 30,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1,  0, -1,  5, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0, -1, -2, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, 30, -2, 30,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ]
]
map_width = len(map_world[0])
map_height = len(map_world)

sem_wall = -1
sem_city = -2
sem_city_alias = -3

def pairToString(pair):
	return "({},{})".format("{}".format(pair[0]).rjust(2), "{}".format(pair[1]).ljust(2))

"""
	Find the cost to move through ortho-adjacent cells.
"""
def neighbors(coord):
	neigh = []

	if coord[1] > 0 and map_world[coord[1] - 1][coord[0]] != sem_wall:
		neigh.append((coord[0], coord[1] - 1))
	if coord[1] < (map_height - 1) and map_world[coord[1] + 1][coord[0]] != sem_wall:
		neigh.append((coord[0], coord[1] + 1))

	if coord[0] > 0 and map_world[coord[1]][coord[0] - 1] != sem_wall:
		neigh.append((coord[0] - 1, coord[1]))
	if coord[0] < (map_width - 1) and map_world[coord[1]][coord[0] + 1] != sem_wall:
		neigh.append((coord[0] + 1, coord[1]))

	return neigh


"""
	Directions and cost from coord to arrive at a destination.
"""
class EwPath:
	visited = None
	steps = None
	cost = 0
	iters = 0

	def __init__(
		self,
		path_from = None,
		steps = [],
		cost = 0,
		visited = {}
	):
		if path_from != None:
			self.steps = deepcopy(path_from.steps)
			self.cost = path_from.cost
			self.visited = deepcopy(path_from.visited)
		else:
			self.steps = steps
			self.cost = cost
			self.visited = visited
			

"""
	Add coord_next to the path.
"""
def path_step(path, coord_next, user_data):
	visited_set_y = path.visited.get(coord_next[0])
	if visited_set_y == None:
		path.visited[coord_next[0]] = { coord_next[1]: True }
	elif visited_set_y.get(coord_next[1]) == True:
		# Already visited
		return False
	else:
		path.visited[coord_next[0]][coord_next[1]] = True

	cost_next = map_world[coord_next[1]][coord_next[0]]

	if cost_next == sem_city or cost_next == sem_city_alias:
		next_poi = ewcfg.coord_to_poi.get(coord_next)
		if cost_next == sem_city and inaccessible(user_data = user_data, poi = next_poi):
			cost_next = 5000
		else:
			cost_next = 0

	path.steps.append(coord_next)
	path.cost += cost_next

	return True

"""
	Returns a new path including all of path_base, with the next step coord_next.
"""
def path_branch(path_base, coord_next, user_data):
	path_next = EwPath(path_from = path_base)

	if path_step(path_next, coord_next, user_data) == False:
		return None
	
	return path_next

def path_to(
	coord_start = None,
	coord_end = None,
	poi_start = None,
	poi_end = None,
	user_data = None
):
	score_golf = 65535
	paths_finished = []
	paths_walking = []

	pois_adjacent = []

	if poi_start != None:
		poi = ewcfg.id_to_poi.get(poi_start)

		if poi != None:
			coord_start = poi.coord

	if poi_end != None:
		poi = ewcfg.id_to_poi.get(poi_end)

		if poi != None:
			coord_end = poi.coord

	path_base = EwPath(
		steps = [ coord_start ],
		cost = 0,
		visited = { coord_start[0]: { coord_start[1]: True } }
	)

	for neigh in neighbors(coord_start):
		path_next = path_branch(path_base, neigh, user_data)
		if path_next != None:
			paths_walking.append(path_next)

	count_iter = 0
	while len(paths_walking) > 0:
		count_iter += 1

		paths_walking_new = []
		paths_dead = []

		for path in paths_walking:
			if path.cost >= score_golf:
				paths_dead.append(path)
				continue

			step_last = path.steps[-1]
			step_penult = path.steps[-2] if len(path.steps) >= 2 else None

			path_branches = 0
			path_base = EwPath(path_from = path)
			for neigh in neighbors(step_last):
				if neigh == step_penult:
					continue

				could_move = False

				branch = None
				if path_branches == 0:
					could_move = path_step(path, neigh, user_data)
				else:
					branch = path_branch(path_base, neigh, user_data)
					if branch != None:
						could_move = True
						paths_walking_new.append(branch)

				if could_move:
					path_branches += 1

					if coord_end != None:
						# Arrived at the actual destination?
						if neigh == coord_end:
							path_final = branch if branch != None else path
							if path_final.cost < score_golf:
								score_golf = path_final.cost
								paths_finished = []

							if path.cost <= score_golf:
								paths_finished.append(path_final)

							paths_dead.append(path_final)
					else:
						# Looking for adjacent points of interest.
						sem_current = map_world[neigh[1]][neigh[0]]
						poi_adjacent_coord = neigh

						if sem_current == sem_city_alias:
							poi_adjacent_coord = ewcfg.alias_to_coord.get(neigh)

							if poi_adjacent_coord != None:
								sem_current = sem_city

						if sem_current == sem_city and poi_adjacent_coord != coord_start:
							poi_adjacent = ewcfg.coord_to_poi.get(poi_adjacent_coord)

							if poi_adjacent != None:
								pois_adjacent.append(poi_adjacent)

							path_final = branch if branch != None else path
							paths_dead.append(path_final)

			if path_branches == 0:
				paths_dead.append(path)

		for path in paths_dead:
			try:
				paths_walking.remove(path)
			except:
				return None

		if len(paths_walking_new) > 0:
			paths_walking += paths_walking_new

	if coord_end != None:
		path_true = None
		if len(paths_finished) > 0:
			path_true = paths_finished[0]
			path_true.iters = count_iter

		return path_true
	else:
		return pois_adjacent


"""
	Debug method to draw the map, optionally with a path/route on it.
"""
def map_draw(path = None, coord = None):
	y = 0
	for row in map_world:
		outstr = ""
		x = 0

		for col in row:
			if col == sem_wall:
				col = "  "
			elif col == sem_city:
				col = "CT"
			elif col == sem_city_alias:
				col = "ct"
			elif col == 0:
				col = "██"
			elif col == 30:
				col = "[]"
			elif col == 5:
				col = "••"

			if path != None:
				visited_set_y = path.visited.get(x)
				if visited_set_y != None and visited_set_y.get(y) != None:
					col = "." + col[-1]

			if coord != None and coord == (x, y):
				col = "O" + col[-1]
					
			outstr += "{}".format(col)
			x += 1

		print(outstr)
		y += 1

def inaccessible(user_data = None, poi = None):
	if(
		len(poi.factions) > 0 and
		user_data.life_state != ewcfg.life_state_corpse and
		len(user_data.faction) > 0 and
		user_data.faction not in poi.factions
	) or (
		len(poi.life_states) > 0 and
		user_data.life_state not in poi.life_states
	):
		return True
	else:
		return False


"""
	Player command to move themselves from one place to another.
"""
async def move(cmd):
	if channel_name_is_poi(cmd.message.channel.name) == False:
		return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	target_name = ewutils.flattenTokenListToString(cmd.tokens[1:])
	if target_name == None or len(target_name) == 0:
		return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "Where to?"))

	user_data = EwUser(member = cmd.message.author)
	poi_current = ewcfg.id_to_poi.get(user_data.poi)
	poi = ewcfg.id_to_poi.get(target_name)

	if poi == None:
		return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "Never heard of it."))

	if poi.id_poi == user_data.poi:
		return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You're already there, bitch."))

	if inaccessible(user_data = user_data, poi = poi):
		return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You're not allowed to go there (bitch)."))

	if user_data.life_state == ewcfg.life_state_corpse and user_data.busted:
		if user_data.poi == ewcfg.poi_id_thesewers:
			return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You're busted, bitch. You can't leave the sewers until your !revive."))
		else:  # sometimes busted ghosts get stuck outside the sewers
			user_data.poi = ewcfg.poi_id_thesewers
			user_data.persist()
			await ewrolemgr.updateRoles(cmd.client, cmd.message.author)
			return

	if poi.coord == None or poi_current == None or poi_current.coord == None:
		path = EwPath(cost = 60)
	else:
		path = path_to(
			poi_start = user_data.poi,
			poi_end = target_name,
			user_data = user_data
		)

		if path == None:
			return await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You don't know how to get there."))

	global moves_active
	global move_counter

	# Check if we're already moving. If so, cancel move and change course. If not, register this course.
	move_current = moves_active.get(cmd.message.author.id)
	move_counter += 1

	# Take control of the move for this player.
	move_current = moves_active[cmd.message.author.id] = move_counter

	minutes = int(path.cost / 60)

	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You begin walking to {}.{}".format(
		poi.str_name,
		(" It's {} minute{} away.".format(
			minutes,
			("s" if minutes != 1 else "")
		) if minutes > 0 else "")
	)))

	life_state = user_data.life_state
	faction = user_data.faction

	if poi.coord == None or poi_current == None or poi_current.coord == None:
		if path.cost > 0:
			await asyncio.sleep(path.cost)

		user_data = EwUser(member = cmd.message.author)

		# If the player dies or enlists or whatever while moving, cancel the move.
		if user_data.life_state != life_state or faction != user_data.faction:
			return

		user_data.poi = poi.id_poi
		user_data.persist()

		await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

		channel = cmd.message.channel

		# Send the message in the channel for this POI if possible, else in the origin channel for the move.
		for ch in cmd.message.server.channels:
			if ch.name == poi.channel:
				channel = ch
				break

		await cmd.client.send_message(
			channel,
			ewutils.formatMessage(
				cmd.message.author,
				"You {} {}.".format(poi.str_enter, poi.str_name)
			)
		)
	else:
		# Perform move.
		for step in path.steps[1:]:
			# Check to see if we have been interrupted and need to not move any farther.
			if moves_active[cmd.message.author.id] != move_current:
				break

			val = map_world[step[1]][step[0]]
			poi_current = None

			# Standing on the actual city node.
			if val == sem_city:
				poi_current = ewcfg.coord_to_poi.get(step)

			# Standing on a node which is aliased (a part of the city).
			elif val == sem_city_alias:
				poi_current = ewcfg.coord_to_poi.get(ewcfg.alias_to_coord.get(step))

			if poi_current != None:
				user_data = EwUser(member = cmd.message.author)

				# If the player dies or enlists or whatever while moving, cancel the move.
				if user_data.life_state != life_state or faction != user_data.faction:
					return

				channel = cmd.message.channel

				# Prevent access to the zone if it's closed.
				if poi_current.closed == True:
					try:
						if poi_current.str_closed != None:
							message_closed = poi_current.str_closed
						else:
							message_closed = "The way into {} is blocked.".format(poi_current.str_name)

						# Send the message in the player's current if possible, else in the origin channel for the move.
						poi_current = ewcfg.id_to_poi.get(user_data.poi)
						for ch in cmd.message.server.channels:
							if ch.name == poi_current.channel:
								channel = ch
								break
					finally:
						return await cmd.client.send_message(
							channel,
							ewutils.formatMessage(
								cmd.message.author,
								message_closed
							)
						)

				# Send the message in the channel for this POI if possible, else in the origin channel for the move.
				for ch in cmd.message.server.channels:
					if ch.name == poi_current.channel:
						channel = ch
						break

				if user_data.poi != poi_current.id_poi:
					user_data.poi = poi_current.id_poi
					user_data.persist()

					await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

					await cmd.client.send_message(
						channel,
						ewutils.formatMessage(
							cmd.message.author,
							"You {} {}.".format(poi_current.str_enter, poi_current.str_name)
						)
					)
			else:
				if val > 0:
					#await asyncio.sleep(val/30) #fixme
					await asyncio.sleep(val)

"""
	Dump out the visual description of the area you're in.
"""
async def look(cmd):
	user_data = EwUser(member = cmd.message.author)
	poi = ewcfg.id_to_poi.get(user_data.poi)

	if poi != None:
		await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(
			cmd.message.author,
			"**{}**\n\n{}{}".format(
				poi.str_name,
				poi.str_desc,
				("\n\n{}".format(
					ewcmd.weather_txt(cmd.message.server.id)
				) if cmd.message.server != None else "")
			)
		))
