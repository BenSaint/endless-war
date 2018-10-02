import datetime

import ewcfg
import ewutils

async def post_leaderboards(client = None, server = None):
	leaderboard_channel = ewutils.get_channel(server = server, channel_name = ewcfg.channel_leaderboard)

	time = str(datetime.datetime.now()).rpartition(':')[0]

	await client.send_message(leaderboard_channel, "▓{} **STATE OF THE CITY** {} {}▓".format(ewcfg.emote_theeye, time, ewcfg.emote_theeye)) 

	topslimes = make_userdata_board(server = server, category = ewcfg.col_slimes, title = ewcfg.leaderboard_slimes)
	await client.send_message(leaderboard_channel, topslimes)
	topcoins = make_userdata_board(server = server, category = ewcfg.col_slimecredit, title = ewcfg.leaderboard_slimecredit)
	await client.send_message(leaderboard_channel, topcoins)
	topghosts = make_userdata_board(server = server, category = ewcfg.col_slimes, title = ewcfg.leaderboard_ghosts, lowscores = True, rows = 3)
	await client.send_message(leaderboard_channel, topghosts)
	topbounty = make_userdata_board(server = server, category = ewcfg.col_bounty, title = ewcfg.leaderboard_bounty)
	await client.send_message(leaderboard_channel, topbounty)
	kingpins = make_kingpin_board(server = server, title = ewcfg.leaderboard_kingpins)
	await client.send_message(leaderboard_channel, kingpins)

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

"""
	convert leaderboard data into a message ready string 
"""
def format_board(entries = None, title = ""):
	result = ""
	result += board_header(title)
	rank = 1
	for entry in entries:
		result += board_entry(entry, rank)
		rank += 1

	return result

def board_header(title):
	emote = None

	bar = " ▓▓▓▓▓▓▓ "

	if title == ewcfg.leaderboard_slimes:
		emote = ewcfg.emote_slime2
	elif title == ewcfg.leaderboard_slimecredit:
		emote = ewcfg.emote_slimecoin
	elif title == ewcfg.leaderboard_ghosts:
		emote = ewcfg.emote_negaslime
	elif title == ewcfg.leaderboard_bounty:
		emote = ewcfg.emote_slimegun
	elif title == ewcfg.leaderboard_kingpins:
		emote = ewcfg.emote_theeye

	return emote + bar + title + bar + emote + "\n"

def board_entry(entry, rank):
	faction = ewutils.get_faction(life_state = entry[1], faction = entry[2])
	faction_symbol = ewutils.get_faction_symbol(faction)

	result = "{} `{:_>15} | {}`\n".format(
		faction_symbol,
		"{:,}".format(entry[3]),
		entry[0]
	)

	return result
