import time
##import math
from random import randint

import ewutils
import ewcfg
import ewstats
import ewitem

# from ew import *
import ewcmd
import ewitem
import ewutils
from ewutils import formatMessage
from ew import EwUser

async def reap(cmd):
    #Checking availability of reap action
    resp = await ewcmd.start(cmd= cmd)
    response = ""
    user_data = EwUser(member = cmd.message.author)
    if(user_data.life_state == ewcfg.life_state_juvenile):
        response = "Only Juveniles of pure heart and with nothing better to do can farm."
    elif(cmd.message.channel.name != ewcfg.channel_jr_farm or cmd.message.channel.name != ewcfg.channel_og_farm or cmd.message.channel.name != ewcfg.channel_ab_farm):
        response = "Do you remember planting anything here in this barren wasteland? No, you don’t. Idiot."
    else:
        farmNumber = 0
        if(cmd.message.channel.name == ewcfg.channel_jr_farm):
            farmNumber = 0
        elif(cmd.message.channel.name != ewcfg.channel_og_farm):
            farmNumber = 1
        else:
            farmNumber = 2#AB
        if(not user_data.farmActive[farmNumber]):
            response = "You missed a step, you haven’t planted anything here yet."
        else:
            currentTime = time.time()/60
            timeGrown = currentTime - user_data.sowTime[farmNumber]
            if(timeGrown < 1440):
                response = "Patience is a virtue and you are morally bankrupt. Just wait, asshole."
            else: #Reaping
                #Flat rate Slime gain
#                slimeGain = 35000000
                #Flat Rate Based Times Level at time of sow.
                if(timeGrown < 2880):
                    response ="You eagerly cultivate your crop, but what’s this? It’s dead and wilted! It seems as though you’ve let it lay fallow for far too long. Pay better attention to your farm next time. You gain no slime."
                    user_data.farmActive[farmNumber] = False
                    user_data.persist()
                else:
                    slimeGain = 35000000
                #S(t) = 35000000 +  (t - 1440) * 992 + Log2(t/1440) * 11782046 caped at 100000000
#                if (timeGrown < 20160):
#                    slimeGain = 33571520 + timeGrown * 992 + math.log(timeGrown, 2.0)
#                    else:
#                    slimeGain = 100000000
                #S(t) = 35000000 +  (t - 1440) * 992 + Log2(t/1440) * 11782046 that transitions into flat growth
#                if (timeGrown < 20160):
#                    slimeGain = (33571520 + timeGrown * 992 + math.log(timeGrown, 2.0))/300#Divided by 300 to account for later balance changes
#                else:
#                    slimeGain = timeGrown * 992 + 80001280
                    response = "You reap what you’ve sown. Your investment has yielded" + str(slimeGain) + "slime and a bushel of" + user_data.plantType[farmNumber]
                user_data.farmActive[farmNumber] = False
    await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
    return

async def sow(cmd):
    # Checking availability of sow action
    resp = await ewcmd.start(cmd = cmd)
    response = "error"
    user_data = EwUser(member = cmd.message.author)
    if(user_data.life_state == ewcfg.life_state_juvenile):
        response = "Only Juveniles of pure heart and with nothing better to do can farm."
    elif(cmd.message.channel.name != ewcfg.channel_jr_farm or cmd.message.channel.name != ewcfg.channel_og_farm or cmd.message.channel.name != ewcfg.channel_ab_farm):
        response = "The cracked, filthy concrete streets around you would be a pretty terrible place for a farm. Try again on more arable land."
    else:
        farmNumber = 0
        if(cmd.message.channel.name == ewcfg.channel_jr_farm):
            farmNumber = 0
        elif(cmd.message.channel.name != ewcfg.channel_og_farm):
            farmNumber = 1
        else:
            farmNumber = 2#AB
        if(user_data.farmActive[farmNumber]):
            response = "You’ve already sown something here. Try planting in another farming location. If you’ve planted in all three farming locations, you’re shit out of luck. Just wait, asshole."
        else:
            poudrins = ewitem.inventory(
                id_user=cmd.message.author.id,
                id_server=cmd.message.server.id,
                item_type_filter=ewcfg.it_slimepoudrin
            )
            if (len(poudrins) < 1):
                response = "You don't have anything to plant! Try collecting a poudrin."
            else:
                #Sowing
                user_data.time_lastsow[farmNumber] = int(time.time()/60)#Grow time is stored in minutes.
                user_data.plantType[farmNumber] = ewcfg.seed_list[randint(0,len(ewcfg.seed_list)-1)]#select random plant
                ewitem.item_delete(id_item=poudrins[0].get('id_item'))#Remove Poudrins
                user_data.farmActive[farmNumber] = True
                user_data.persist()
                response = "You sow a poudrin into the fertile soil beneath you. It will grow  in about a day."
    await cmd.client.edit_message(resp, ewutils.formatMessage(cmd.message.author, response))
    return
