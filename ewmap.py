import re 
import asyncio

from copy import deepcopy

import ewutils
import ewcmd

from ew import EwUser

# Map of user IDs to their course ID.
moves_active = {}
move_counter = 0

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

	# A description provided when !look-ing here.
	str_desc = ""

	# (X, Y) location on the map (left, top) zero-based origin.
	coord = None

	# Channel name associated with this POI
	channel = ""

	# Zone allows PvP combat and interactions.
	pvp = True

	def __init__(
		self,
		id_poi = "unknown", 
		alias = [],
		str_name = "Unknown",
		str_desc = "...",
		coord = (0, 0),
		channel = "",
		pvp = True
	):
		self.id_poi = id_poi
		self.alias = alias
		self.str_name = str_name
		self.str_desc = str_desc
		self.coord = coord
		self.channel = channel
		self.pvp = pvp

poi_list = [
	EwPoi( # 1
		id_poi = "downtown",
		alias = [
			"central",
			"dt",
			"stockmarket",
			"stockexchange",
			"slimemarket",
			"slimeexchange",
			"exchange"
		],
		str_name = "Downtown NLACakaNM",
		str_desc = "Skyscrapers tower over every street as far as the eye can see. Fluorescent signs flash advertisements in strange glyphs and the streets roar with the sound of engines and scraping metal from the subway deep underground.",
		coord = (23, 16),
		channel = "1-downtown-nlacakanm"
	),
	EwPoi( # 2
		id_poi = "smogsburg",
		alias = [
			"smog",
			"smogs",
			"bazaar",
			"market"
		],
		str_name = "Smogsburg",
		str_desc = "The pavement rumbles as subway trains grind along their tracks far beneath your feet. In every direction, smokestacks belch sickly clouds into the sky.",
		coord = (23, 11),
		channel = "2-smogsburg"
	),
	EwPoi( # 3
		id_poi = "copkilltown",
		alias = [
			"cop",
			"cops",
			"killers",
			"killer",
			"killtown",
			"copkt"
		],
		str_name = "Cop Killtown",
		str_desc = "Deep indigo edifices of metal and brick rise above the pavement. Apartment windows glint in the blue and purple light of neon signs, and a menacing cathedral looms darkly on the horizon.",
		coord = (17, 13),
		channel = "3-cop-killtown",
		pvp = False
	),
	EwPoi( # 4
		id_poi = "krakbay",
		alias = [
			"krak",
			"food-court",
			"foodcourt",
			"food"
		],
		str_name = "Krak Bay",
		str_desc = "Off the nearby riverbank, rusty barges churn their way along the Slime River. Posh riverside apartments taunt you with their cheap opulence.",
		coord = (16, 19),
		channel = "4-krak-bay"
	),
	EwPoi( # 5
		id_poi = "poudrinalley",
		alias = [
			"poudrin",
			"711",
			"outside711"
		],
		str_name = "Poudrin Alley",
		str_desc = "Bent and broken streetlights spark and flicker over the cracked, derelict pavement. The 7-11 stands dimly opposite a row of apartments, its CLOSED sign crooked and dusty.",
		coord = (19, 23),
		channel = "5-poudrin-alley"
	),
	EwPoi( # 6
		id_poi = "rowdyroughhouse",
		alias = [
			"rowdy",
			"rowdys",
			"rowdies",
			"roughhouse",
			"rowdyrh"
		],
		str_name = "Rowdy Roughhouse",
		str_desc = "", # TODO
		coord = (25, 21),
		channel = "6-rowdy-roughhouse",
		pvp = False
	),
	EwPoi( # 7
		id_poi = "greenlightdistrict",
		alias = [
			"greenlight",
			"casino"
		],
		str_name = "Green Light District",
		str_desc = "Fluorescent signs flicker bright glyphs over smooth freshly-paved streets, promising all conceivable earthly pleasures. The ground is tacky with some unknown but obviously sinful grime.",
		coord = (29, 14),
		channel = "7-green-light-district"
	),
	EwPoi( # 8
		id_poi = "oldnewyonkers",
		str_name = "Old New Yonkers",
		str_desc = "Rows of three-story brick and stone condominiums with white marble moulding wind along lanes of chipped cobblestone. Wrought-iron spikes jut from windows and balconies.",
		coord = (32, 9),
		channel = "8-old-new-yonkers"
	),
	EwPoi( # 9
		id_poi = "littlechernobyl",
		alias = [
			"chernobyl"
		],
		str_name = "Little Chernobyl",
		str_desc = "Pathetic little gardens front the uneven parking lots of corporate complexes housing dentists, fortune-tellers, real estate agencies, and other equally dull and pointless ventures.",
		coord = (25, 7),
		channel = "9-little-chernobyl"
	),
	EwPoi( # 10
		id_poi = "arsonbrook",
		alias = [
			"arson"
		],
		str_name = "Arsonbrook",
		str_desc = "North of the bridge, you see large swathes of what were once suburbs blackened and flat, occasionally still smoking. Legends say a Starbucks tried to open here once.",
		coord = (21, 3),
		channel = "10-arsonbrook"
	),
	EwPoi( # 11
		id_poi = "astatineheights",
		alias = [
			"astatine"
		],
		str_name = "Astatine Heights",
		str_desc = "Modern high-rise condos just from the steep hills to the north. To the south, classical stone and brick houses with columns command disgustingly decadent wide grassy yards.",
		coord = (17, 6),
		channel = "11-astatine-heights"
	),
	EwPoi( # 12
		id_poi = "gatlingsdale",
		alias = [
			"gatlings",
		],
		str_name = "Gatlingsdale",
		str_desc = "The brightest young minds of NLACakaNM fritter away their time here, amid hallowed halls of learning ringed endlessly by foreign book stores and cinemas showing midnight screenings of silent films.",
		coord = (13, 9),
		channel = "12-gatlingsdale"
	),
	EwPoi( # 13
		id_poi = "vandalpark",
		alias = [
			"vandal",
			"arena",
			"slimeoidarena"
		],
		str_name = "Vandal Park",
		str_desc = "The more-or-less clean air carries the roar of the crowd across the grassy fields surrounding the arena.",
		coord = (10, 12),
		channel = "13-vandal-park"
	),
	EwPoi( # 14
		id_poi = "glocksbury",
		alias = [
			"glocks"
		],
		str_name = "Glocksbury",
		str_desc = "You smell bacon. *Figurative* bacon. The streets are too orderly here... the cops must be about. Absolutely vile.",
		coord = (9, 16),
		channel = "14-glocksbury"
	),
	EwPoi( # 15
		id_poi = "northsleezeborough",
		alias = [
			"northsleezeboro",
			"nsleezeborough",
			"nsleezeboro"
		],
		str_name = "North Sleezeborough",
		str_desc = "Young jobless adults walk around in plaid and suspenders with curious facial hair, stopping into the occasional store front to buy a vinyl recording or an ironic knick-knack.",
		coord = (11, 19),
		channel = "15-north-sleezeborough"
	),
	EwPoi( # 16
		id_poi = "southsleezeborough",
		alias = [
			"southsleezeboro",
			"ssleezeborough",
			"ssleezeboro",
			"the-dojo",
			"dojo"
		],
		str_name = "South Sleezeborough",
		str_desc = "The streets are empty. The residents of this neighborhood have all lost their nerve and are hiding in their hovels in a futile attempts to stay safe from gang violence.",
		coord = (12, 22),
		channel = "16-south-sleezeborough"
	),
	EwPoi( # 17
		id_poi = "oozegardens",
		alias = [
			"ooze"
		],
		str_name = "Ooze Gardens",
		str_desc = "A bird chirps its last before falling dead from a withered tree. A trickle of slime runs down its bark. The resident's attempts to beautify the neighborhood with foliage have really backfired, aesthetically speaking.",
		coord = (14, 25),
		channel = "17-ooze-gardens"
	),
	EwPoi( # 18
		id_poi = "cratersville",
		alias = [
			"craters"
		],
		str_name = "Cratersville",
		str_desc = "The people here hurry to their destinations, avoiding eye contact. They must be wary after seeing gang members level the next town over not too long ago.",
		coord = (19, 28),
		channel = "18-cratersville"
	),
	EwPoi( # 19
		id_poi = "wreckington",
		alias = [
			"wrecking"
		],
		str_name = "Wreckington",
		str_desc = "You step over piles of rubble that once housed the now-displaced population of this neighborhood. A recent a dramatic victim of rampant gang warfare.",
		coord = (27, 24),
		channel = "19-wreckington"
	),
	EwPoi( # 20
		id_poi = "juviesrow",
		alias = [
			"juvies",
			"the-mines",
			"mines",
			"mine"
		],
		str_name = "Juvie's Row",
		str_desc = "Quaint little Juvie shanties pepper the landscape around the entrance to the slime mines. Pale rocks and sticks are arranged in sad fascimiles of white picket fences. You're filled with pity, as well as disgust.",
		coord = (32, 18),
		channel = "20-juvies-row"
	),
	EwPoi( # 21
		id_poi = "slimesend",
		alias = [
			"slimes"
		],
		str_name = "Slime's End",
		str_desc = "The narrow peninsula is bordered on both sides by the Slime Sea. The phosphorescence of the Sea illuminates the land and sky with an eerily even green glow.",
		coord = (40, 16),
		channel = "21-slimes-end"
	),
	EwPoi( # 22
		id_poi = "vagrantscorner",
		alias = [
			"vagrants"
		],
		str_name = "Vagrant's Corner",
		str_desc = "The glow of the Slime Sea illumunates the undersides of the docks and the heavy industrial machinery designed to pump slime into the cargo holds of outbound barges.",
		coord = (37, 11),
		channel = "22-vagrants-corner"
	),
	EwPoi( # 23
		id_poi = "assaultflatsbeachresort",
		alias = [
			"assaultflatsbeach",
			"assaultflats",
			"beach",
			"resort",
			"assault",
			"flats"
		],
		str_name = "Assault Flats Beach Resort",
		str_desc = "The white imported sand of the beach stretches toward the horizon, lapped by gentle waves of slime. Gleaming hotels jut out of the rock formations just off the beachfront.",
		coord = (40, 6),
		channel = "23-assault-flats-beach-resort"
	),
	EwPoi( # 24
		id_poi = "newnewyonkers",
		str_name = "New New Yonkers",
		str_desc = "Trendy restaurants and clubs sit empty in this sparsely-populated failed gentrification experiment.",
		coord = (36, 4),
		channel = "24-new-new-yonkers"
	),
	EwPoi( # 25
		id_poi = "brawlden",
		alias = [
			"slimecorplabs",
			"slimecorplab",
			"slimecorplaboratory",
			"slimecorp",
			"laboratory",
			"labs",
			"lab"
		],
		str_name = "Brawlden",
		str_desc = "Rough-looking bewifebeatered citizens are everywhere, doing unspecified maintenence on strange machines propped up on cinderblocks. A SlimeCorp Laboratory hums and whirrs in the distance, day and night.",
		coord = (28, 3),
		channel = "25-brawlden"
	),
	EwPoi( # 26
		id_poi = "toxington",
		str_name = "Toxington",
		str_desc = "You cover your mouth in a futile attempt to avoid breathing choking acidic vapor that continually rises off of the nearby lake.",
		coord = (9, 4),
		channel = "26-toxington"
	),
	EwPoi( # 27
		id_poi = "charcoalpark",
		alias = [
			"charcoal"
		],
		str_name = "Charcoal Park",
		str_desc = "The soil here is mostly black soot and the charred remains of a now long-gone series of low-income apartment complexes. A few shantytowns have been constructed as some of the only living trees in NLACakaNM have sprouted out of the ashes.",
		coord = (3, 3),
		channel = "27-charcoal-park"
	),
	EwPoi( # 28
		id_poi = "poloniumhill",
		alias = [
			"polonium"
		],
		str_name = "Polonium Hill",
		str_desc = "The gently rolling terrain is speckled with hideous minimansions that obviously cost a fortune and look like complete shit.",
		coord = (5, 9),
		channel = "28-polonium-hill"
	),
	EwPoi( # 29
		id_poi = "westglocksbury",
		alias = [
			"westglocks",
			"wglocks"
		],
		str_name = "West Glocksbury",
		str_desc = "Gunshots ring out periodically from somewhere in the distance, hidden by laundromats and barber shops. Even the most jaded NLACakaNMite may get a bit nervous 'round these parts.",
		coord = (4, 14),
		channel = "29-west-glocksbury"
	)
]

id_to_poi = {}
coord_to_poi = {}

for poi in poi_list:
	# Populate the map of coordinates to their point of interest, for looking up from the map.
	coord_to_poi[poi.coord] = poi

	# Populate the map of point of interest names/aliases to the POI.
	id_to_poi[poi.id_poi] = poi
	for alias in poi.alias:
		id_to_poi[alias] = poi

map_world = [
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -2, 30,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1,  0, -1, -1, 30, -1, -1, -1, -1,  0,  0, 30, -2, 30,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1,  0,  0,  0,  0, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, 30, -2, 30,  0, -1, -1,  0, -1, -1, 30, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0, -1,  0, 30, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0, -1, 30, -1, -1, -1, -1,  0, -1, -1, -2, 30,  0,  0,  0, -1, -1, -1, -1, -1, -1,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1,  0, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0,  0, 30, -2, -1, -1, -1,  0, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1,  0,  0, 30, -2, 30,  0,  0,  0,  0, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1,  0,  0,  0,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1,  0, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0,  0,  0,  0,  0, -1,  0,  0, 30, -2, 30,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1,  0, -1, -1,  0,  0, 30, -2, 30,  0,  0, -1, -1, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, 30, -1, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -2, 30,  0, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1,  0, 30, -2, 30,  0,  0,  0,  0, -1, -1,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1,  0, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1,  0,  0, 30, -2, 30,  0,  0,  0,  0,  0,  0, -1, -1,  0,  0,  0, 30, -2, 30,  0,  0,  0, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1,  0, -1, -1, -1,  0,  0,  0, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -2, 30,  0,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1,  0, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -2, 30,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -2, 30,  0,  0,  0, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 30,  0,  0,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ]
]
map_width = len(map_world[0])
map_height = len(map_world)

sem_wall = -1
sem_city = -2

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

	def __init__(self, path_from = None, steps = [], cost = 0, visited = {}):
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
def path_step(path, coord_next):
	visited_set_y = path.visited.get(coord_next[0])
	if visited_set_y == None:
		path.visited[coord_next[0]] = { coord_next[1]: True }
	elif visited_set_y.get(coord_next[1]) == True:
		# Already visited
		return False
	else:
		path.visited[coord_next[0]][coord_next[1]] = True

	cost_next = map_world[coord_next[1]][coord_next[0]]

	if cost_next == sem_city:
		cost_next = 0

	path.steps.append(coord_next)
	path.cost += cost_next

	return True

"""
	Returns a new path including all of path_base, with the next step coord_next.
"""
def path_branch(path_base, coord_next):
	path_next = EwPath(path_from = path_base)

	if path_step(path_next, coord_next) == False:
		return None
	
	return path_next

def path_to(coord_start = None, coord_end = None, poi_start = None, poi_end = None):
	score_golf = 65535
	paths_finished = []
	paths_walking = []

	if poi_start != None:
		poi = id_to_poi.get(poi_start)

		if poi != None:
			coord_start = poi.coord

	if poi_end != None:
		poi = id_to_poi.get(poi_end)

		if poi != None:
			coord_end = poi.coord

	path_base = EwPath(
		steps = [ coord_start ],
		cost = 0,
		visited = { coord_start[0]: { coord_start[1]: True } }
	)

	for neigh in neighbors(coord_start):
		path_next = path_branch(path_base, neigh)
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
			path_good = False
			path_base = EwPath(path_from = path)
			for neigh in neighbors(step_last):
				if neigh == step_penult:
					continue

				could_move = False

				branch = None
				if path_branches == 0:
					could_move = path_step(path, neigh)
				else:
					branch = path_branch(path_base, neigh)
					if branch != None:
						could_move = True
						paths_walking_new.append(branch)

				if could_move:
					path_branches += 1

					# Arrived at the actual destination?
					if neigh == coord_end:
						path_final = branch if branch != None else path
						if path_final.cost < score_golf:
							score_golf = path_final.cost
							paths_finished = []

						if path.cost <= score_golf:
							paths_finished.append(path_final)

						paths_dead.append(path_final)

			if path_branches == 0:
				paths_dead.append(path)

		for path in paths_dead:
			paths_walking.remove(path)
		if len(paths_walking_new) > 0:
			paths_walking += paths_walking_new

	path_true = None
	if len(paths_finished) > 0:
		path_true = paths_finished[0]
		path_true.iters = count_iter

	return path_true

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
			elif col == 0:
				col = "██"
			elif col == 30:
				col = "[]"

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

re_flattener = re.compile("['\"!@#$%^&*().,/?{}\[\];:]")

"""
	Player command to move themselves from one place to another.
"""
async def move(cmd):
	resp = await ewcmd.start(cmd = cmd)
	target_name = ""

	global re_flattener
	for token in cmd.tokens[1:]:
		if token.startswith('<@') == False:
			target_name += re_flattener.sub("", token.lower())

	user_data = EwUser(member = cmd.message.author)

	poi = id_to_poi.get(target_name)
	if poi == None:
		return await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "Never heard of it."))
	elif poi.id_poi == user_data.poi:
		return await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You're already there, bitch."))

	path = path_to(
		poi_start = user_data.poi,
		poi_end = target_name
	)

	if path == None:
		return await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You don't know how to get there."))

	global moves_active
	global move_counter

	# Check if we're already moving. If so, cancel move and change course. If not, register this course.
	move_current = moves_active.get(cmd.message.author.id)
	move_counter += 1

	if move_current == None:
		# No active course.
		# FIXME debug
		ewutils.logMsg("No current course id.")
	else:
		# Interrupt course.
		# FIXME debug
		ewutils.logMsg("Interrupted course id: {}".format(move_current))

	move_current = moves_active[cmd.message.author.id] = move_counter

	await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, "You begin walking to {}.".format(poi.str_name)))

	# Perform move.
	for step in path.steps[1:]:
		# Check to see if we have been interrupted and need to not move any farther.
		if moves_active[cmd.message.author.id] != move_current:
			# FIXME debug
			ewutils.logMsg('Move id {} interrupted.'.format(move_current))
			break

		val = map_world[step[1]][step[0]]

		ewutils.logMsg("step cost {}".format(val))

		if val == sem_city:
			poi_current = coord_to_poi.get(step)

			if poi_current != None:
				user_data = EwUser(member = cmd.message.author)
				user_data.poi = poi_current.id_poi
				user_data.persist()

				await cmd.client.send_message(
					cmd.message.channel,
					ewutils.formatMessage(
						cmd.message.author,
						"You enter {}.".format(poi_current.str_name)
					)
				)
		else:
			if val > 0:
				await asyncio.sleep(val)
