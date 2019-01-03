"""
	Commands for kingpins only.
"""
import ewitem
import ewutils
import ewcfg
import ewrolemgr
from ew import EwUser

"""
	Release the specified player from their commitment to their faction.
	Returns enlisted players to juvenile.
"""
async def pardon(cmd):
	response = ""
	user_data = EwUser(member = cmd.message.author)

	if user_data.life_state != ewcfg.life_state_kingpin:
		response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
	else:
		member = None
		if cmd.mentions_count == 1:
			member = cmd.mentions[0]
			if member.id == cmd.message.author.id:
				member = None

		if member == None:
			response = "Who?"
		else:
			member_data = EwUser(member = member)

			if member_data.faction == "":
				response = "{} isn't enlisted.".format(member.display_name)
			else:
				faction_old = member_data.faction
				member_data.faction = ""

				if member_data.life_state == ewcfg.life_state_enlisted:
					member_data.life_state = ewcfg.life_state_juvenile

				member_data.persist()
				response = "{} has been released from his association with the {}.".format(member.display_name, faction_old)
				await ewrolemgr.updateRoles(client = cmd.client, member = member)

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

""" Destroy a megaslime of your own for lore reasons. """
async def deadmega(cmd):
	response = ""
	user_data = EwUser(member = cmd.message.author)

	if user_data.life_state != ewcfg.life_state_kingpin:
		response = "Only the Rowdy Fucker {} and the Cop Killer {} can do that.".format(ewcfg.emote_rowdyfucker, ewcfg.emote_copkiller)
	else:
		value = 1000000
		user_slimes = 0

		if value > user_data.slimes:
			response = "You don't have that much slime to lose ({:,}/{:,}).".format(user_data.slimes, value)
		else:
			user_data.change_slimes(n = -value)
			user_data.persist()
			response = "Alas, poor megaslime. You have {:,} slime remaining.".format(user_data.slimes)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

"""
	Command that creates a princeps cosmetic item
"""
async def create(cmd):
	if EwUser(member = cmd.message.author).life_state != ewcfg.life_state_kingpin:
		response = 'Lowly Non-Kingpins cannot hope to create items with their bare hands.'
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if len(cmd.tokens) != 4:
		response = 'Usage: !create "<item_name>" "<item_desc>" <recipient>'
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	item_name = cmd.tokens[1]
	item_desc = cmd.tokens[2]

	if cmd.mentions[0]:
		recipient = cmd.mentions[0]
	else:
		response = 'You need to specify a recipient. Usage: !create "<item_name>" "<item_desc>" <recipient>'
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	item_props = {
		"cosmetic_name": item_name,
		"cosmetic_desc": item_desc,
		"adorned": "false",
		"rarity": "princeps"
	}

	new_item_id = ewitem.item_create(
		id_server = cmd.message.server.id,
		id_user = recipient.id,
		item_type = ewcfg.it_cosmetic,
		item_props = item_props
	)

	ewitem.soulbind(new_item_id)

	response = 'Item "{}" successfully created.'.format(item_name)
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
