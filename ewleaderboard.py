import datetime

import ewcfg
import ewutils
from ew import EwMarket

async def post_leaderboards(client = None, server = None):
	leaderboard_channel = ewutils.get_channel(server = server, channel_name = ewcfg.channel_leaderboard)

	market = EwMarket(id_server = server.id)
	time = "day {}".format(market.day) 

	await client.send_message(leaderboard_channel, "▓▓{} **STATE OF THE CITY:** {} {}▓▓".format(ewcfg.emote_theeye, time, ewcfg.emote_theeye))

	kingpins = make_kingpin_board(server = server, title = ewcfg.leaderboard_kingpins)
	await client.send_message(leaderboard_channel, kingpins)
	districts = make_district_control_board(id_server = server.id, title = ewcfg.leaderboard_districts)
	await client.send_message(leaderboard_channel, districts)
	topslimes = make_userdata_board(server = server, category = ewcfg.col_slimes, title = ewcfg.leaderboard_slimes)
	await client.send_message(leaderboard_channel, topslimes)
	topcoins = make_userdata_board(server = server, category = ewcfg.col_slimecredit, title = ewcfg.leaderboard_slimecredit)
	await client.send_message(leaderboard_channel, topcoins)
	topghosts = make_userdata_board(server = server, category = ewcfg.col_slimes, title = ewcfg.leaderboard_ghosts, lowscores = True, rows = 3)
	await client.send_message(leaderboard_channel, topghosts)
	topbounty = make_userdata_board(server = server, category = ewcfg.col_bounty, title = ewcfg.leaderboard_bounty)
	await client.send_message(leaderboard_channel, topbounty)

def make_userdata_board(server = None, category = "", title = "", lowscores = False, rows = 5):
	entries = []
	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		cursor.execute("SELECT {name}, {state}, {faction}, {category} FROM users, players WHERE users.id_server = %s AND users.{id_user} = players.{id_user} ORDER BY {category} {order}".format(
			name = ewcfg.col_display_name,
			state = ewcfg.col_life_state,
			faction = ewcfg.col_faction,
			category = category,
			id_user = ewcfg.col_id_user,
			order = ('DESC' if lowscores == False else 'ASC')
		), (
			server.id, 
		))

		i = 0
		row = cursor.fetchone()
		while (row != None) and (i < rows):
			if row[1] == ewcfg.life_state_kingpin or row[1] == ewcfg.life_state_grandfoe:
				row = cursor.fetchone()
			else:
				entries.append(row)
				row = cursor.fetchone()
				i += 1

	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

	return format_board(entries = entries, title = title)

def make_kingpin_board(server = None, title = ""):
	entries = []
	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		cursor.execute("SELECT {name}, {state}, {faction}, {category} FROM users, players WHERE users.id_server = %s AND {state} = %s AND users.{id_user} = players.{id_user} ORDER BY {category} DESC".format(
			name = ewcfg.col_display_name,
			state = ewcfg.col_life_state,
			faction = ewcfg.col_faction,
			category = ewcfg.col_slimes,
			id_user = ewcfg.col_id_user
		), (
			server.id, 
			ewcfg.life_state_kingpin
		))

		rows = cursor.fetchall()
		for row in rows:
			entries.append(row)

	finally:
		# Clean up the database handles.
		cursor.close()
		ewutils.databaseClose(conn_info)

	return format_board(entries = entries, title = title)


def make_district_control_board(id_server, title):
	entries = []
	districts = ewutils.execute_sql_query(
		"SELECT {district}, {controlling_faction} FROM districts WHERE id_server = %s".format(
			district = ewcfg.col_district,
			controlling_faction = ewcfg.col_controlling_faction
		), (
			id_server,
		)
	)
	rowdy_districts = 0
	killer_districts = 0

	for district in districts:
		if district[1] == ewcfg.faction_rowdys:
			rowdy_districts += 1
		elif district[1] == ewcfg.faction_killers:
			killer_districts += 1

	rowdy_entry = [ewcfg.faction_rowdys.capitalize(), rowdy_districts]
	killer_entry = [ewcfg.faction_killers.capitalize(), killer_districts]

	return format_board(
		entries = [rowdy_entry, killer_entry] if rowdy_districts > killer_districts else [killer_entry, rowdy_entry],
		title = title,
		entry_type = ewcfg.entry_type_districts
	)

"""
	convert leaderboard data into a message ready string 
"""
def format_board(entries = None, title = "", entry_type = "player"):
	result = ""
	result += board_header(title)

	for entry in entries:
		result += board_entry(entry, entry_type)

	return result

def board_header(title):
	emote = None

	bar = " ▓▓▓▓▓"

	if title == ewcfg.leaderboard_slimes:
		emote = ewcfg.emote_slime2
		bar += "▓▓▓ "

	elif title == ewcfg.leaderboard_slimecredit:
		emote = ewcfg.emote_slimecoin
		bar += " "

	elif title == ewcfg.leaderboard_ghosts:
		emote = ewcfg.emote_negaslime
		bar += "▓ "

	elif title == ewcfg.leaderboard_bounty:
		emote = ewcfg.emote_slimegun
		bar += "▓ "

	elif title == ewcfg.leaderboard_kingpins:
		emote = ewcfg.emote_theeye
		bar += " "

	elif title == ewcfg.leaderboard_districts:
		emote = ewcfg.emote_nlacakanm
		bar += " "

	return emote + bar + title + bar + emote + "\n"

def board_entry(entry, entry_type):
	result = ""

	if entry_type == ewcfg.entry_type_player:
		faction = ewutils.get_faction(life_state = entry[1], faction = entry[2])
		faction_symbol = ewutils.get_faction_symbol(faction)

		result = "{} `{:_>15} | {}`\n".format(
			faction_symbol,
			"{:,}".format(entry[3]),
			entry[0]
		)

	elif entry_type == ewcfg.entry_type_districts:
		faction = entry[0]
		districts = entry[1]
		faction_symbol = ewutils.get_faction_symbol(faction)

		result = "{} `{:_>15} | {}`\n".format(
			faction_symbol,
			faction,
			districts
		)

	return result
