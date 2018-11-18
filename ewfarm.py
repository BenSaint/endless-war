import time
from random import randint

import ewcfg

import ewitem
import ewutils
from ew import EwUser

class EwFarm:
	id_server = ""
	id_user = ""
	name = ""
	time_lastsow = ""

	def __init__(
			self,
			id_server = None,
			id_user = None,
			farm = None
		):
		if id_server is not None and id_user is not None and farm is not None:
			self.id_server = id_server
			self.id_user = id_user
			self.name = farm

			data = ewutils.execute_sql_query(
				"SELECT {time_lastsow} FROM farms WHERE id_server = {id_server} AND id_user = {id_user} AND {col_farm} = {farm}".format(
					time_lastsow = ewcfg.col_time_lastsow,
					id_server = id_server,
					id_user = id_user,
					col_farm = ewcfg.col_farm,
					farm = farm
				))

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.time_lastsow = data[0][0]
			else:  # create new entry
				ewutils.execute_sql_query(
					"REPLACE INTO farms (id_server, id_user, {col_farm}) VALUES ({id_server}, {id_user}, '{farm}')".format(
						id_server = id_server,
						id_user = id_user,
						col_farm = ewcfg.col_farm,
						farm = farm
					))

	def persist(self):
		ewutils.execute_sql_query(
			"REPLACE INTO districts(id_server, id_user, {col_farm}, {col_time_lastsow}) VALUES({id_server}, {id_user}, '{farm}', {time_lastsow})".format(
				col_farm = ewcfg.col_farm,
				col_time_lastsow = ewcfg.col_time_lastsow,
				id_server = self.id_server,
				id_user = self.id_user,
				farm = self.name,
				time_lastsow = self.time_lastsow
			))



"""
	Reap planted crops.
"""
async def reap(cmd):

	user_data = EwUser(member = cmd.message.author)

	# Checking availability of reap action
	if user_data.life_state == ewcfg.life_state_juvenile:
		response = "Only Juveniles of pure heart and with nothing better to do can farm."
	elif cmd.message.channel.name != ewcfg.channel_jr_farm or cmd.message.channel.name != ewcfg.channel_og_farm or cmd.message.channel.name != ewcfg.channel_ab_farm:
		response = "Do you remember planting anything here in this barren wasteland? No, you don’t. Idiot."
	else:
		if user_data.poi == ewcfg.poi_jr_farms:
			farm_number = 0
		elif user_data.poi == ewcfg.poi_og_farms:
			farm_number = 1
		else:  # if it's the farm in arsonbrook
			farm_number = 2

		if user_data.time_lastsow == 0:
			response = "You missed a step, you haven’t planted anything here yet."
		else:
			cur_time_min = time.time() / 60
			time_grown = cur_time_min - user_data.time_lastsow[farm_number]

			if time_grown < ewcfg.crops_time_to_grow:
				response = "Patience is a virtue and you are morally bankrupt. Just wait, asshole."
			else: # Reaping
				if time_grown > ewcfg.crops_time_to_grow * 2:
					response = "You eagerly cultivate your crop, but what’s this? It’s dead and wilted! It seems as though you’ve let it lay fallow for far too long. Pay better attention to your farm next time. You gain no slime."
				else:
					slime_gain = ewcfg.reap_gain

				#S(t) = 35000000 +  (t - 1440) * 992 + Log2(t/1440) * 11782046 caped at 100000000
#                if (time_grown < 20160):
#                    slimeGain = 33571520 + time_grown * 992 + math.log(time_grown, 2.0)
#                    else:
#                    slimeGain = 100000000
				#S(t) = 35000000 +  (t - 1440) * 992 + Log2(t/1440) * 11782046 that transitions into flat growth
#                if (time_grown < 20160):
#                    slimeGain = (33571520 + time_grown * 992 + math.log(time_grown, 2.0))/300#Divided by 300 to account for later balance changes
#                else:
#                    slimeGain = time_grown * 992 + 80001280

					plant_type = ewcfg.seed_list[randint(0,len(ewcfg.seed_list)-1)]
					response = "You reap what you’ve sown. Your investment has yielded" + str(slime_gain) + "slime and a bushel of" + plant_type
				user_data.time_lastsow = 0  # 0 means no seeds are currently planted
				user_data.persist()
	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	return


"""
	Sow seeds that may eventually be !reaped.
"""
async def sow(cmd):
	user_data = EwUser(member = cmd.message.author)

	# Checking availability of sow action
	if user_data.life_state == ewcfg.life_state_juvenile:
		response = "Only Juveniles of pure heart and with nothing better to do can farm."

	elif cmd.message.channel.name != ewcfg.channel_jr_farm or cmd.message.channel.name != ewcfg.channel_og_farm or cmd.message.channel.name != ewcfg.channel_ab_farm:
		response = "The cracked, filthy concrete streets around you would be a pretty terrible place for a farm. Try again on more arable land."

	else:
		if cmd.message.channel.name == ewcfg.channel_jr_farm:
			farm_number = 0
		elif cmd.message.channel.name == ewcfg.channel_og_farm:
			farm_number = 1
		else:  # if it's the farm in arsonbrook
			farm_number = 2

		if user_data.time_lastsow > 0:
			response = "You’ve already sown something here. Try planting in another farming location. If you’ve planted in all three farming locations, you’re shit out of luck. Just wait, asshole."
		else:
			poudrins = ewitem.inventory(
				id_user = cmd.message.author.id,
				id_server = cmd.message.server.id,
				item_type_filter = ewcfg.it_slimepoudrin
			)

			if len(poudrins) < 1:
				response = "You don't have anything to plant! Try collecting a poudrin."
			else:
				# Sowing
				response = "You sow a poudrin into the fertile soil beneath you. It will grow  in about a day."

				user_data.time_lastsow[farm_number] = int(time.time() / 60)  # Grow time is stored in minutes.
				ewitem.item_delete(id_item = poudrins[0].get('id_item'))  # Remove Poudrins

				user_data.persist()

	await cmd.client.send_message(cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	return
