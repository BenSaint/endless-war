import random

from ewwep import EwWeapon
from ewweather import EwWeather
from ewfood import EwFood
from ewitem import EwItemDef
from ewmap import EwPoi

# Global configuration options.
version = "v1.99"

# Update intervals
update_hookstillactive = 60 * 60 * 3
update_twitch = 60
update_pvp = 60
update_market = 900

# Market delta
max_iw_swing = 30

# Life states. How the player is living (or deading) in the database
life_state_corpse = 0
life_state_juvenile = 1
life_state_enlisted = 2
life_state_kingpin = 10

# ID tags for points of interest that are needed in code.
poi_id_thesewers = "thesewers"
poi_id_downtown = "downtown"
poi_id_slimeoidlab = "slimecorpslimeoidlaboratory"
poi_id_mine = "themines"
poi_id_thecasino = "thecasino"
poi_id_711 = "outsidethe711"
poi_id_speakeasy = "thekingswifessonspeakeasy"
poi_id_dojo = "thedojo"
poi_id_arena = "thebattlearena"
poi_id_nlacu = "newlosangelescityuniversity"
poi_id_foodcourt = "thefoodcourt"
poi_id_cinema = "nlacakanmcinemas"
poi_id_bazaar = "thebazaar"
poi_id_stockexchange = "theslimestockexchange"

# Role names. All lower case with no spaces.
role_juvenile = "juveniles"
role_juvenile_pvp = "juvenilepvp"
role_rowdyfucker = "rowdyfucker"
role_rowdyfuckers = "rowdys"
role_rowdyfuckers_pvp = "rowdypvp"
role_copkiller = "copkiller"
role_copkillers = "killers"
role_copkillers_pvp = "killerpvp"
role_corpse = "corpse"
role_corpse_pvp = "corpsepvp"
role_kingpin = "kingpin"

# Faction names
faction_killers = "killers"
faction_rowdys = "rowdys"

# Channel names
channel_mines = "the-mines"
channel_combatzone = "combat-zone"
channel_endlesswar = "endless-war"
channel_sewers = "the-sewers"
channel_dojo = "the-dojo"
channel_twitch_announcement = "rfck-chat"
channel_casino = "slime-casino"
channel_stockexchange = "slime-stock-exchange"
channel_foodcourt = "food-court"
channel_slimeoidlab = "slimecorp-labs"
channel_711 = "outside-the-7-11"
channel_speakeasy = "speakeasy"
channel_arena = "battle-arena"
channel_nlacu = "nlac-university"
channel_cinema = "nlacakanm-cinemas"
channel_bazaar = "bazaar"

# Commands
cmd_prefix = '!'
cmd_enlist = cmd_prefix + 'enlist'
cmd_revive = cmd_prefix + 'revive'
cmd_kill = cmd_prefix + 'kill'
cmd_shoot = cmd_prefix + 'shoot'
cmd_devour = cmd_prefix + 'devour'
cmd_mine = cmd_prefix + 'mine'
cmd_score = cmd_prefix + 'slimes'
cmd_score_alt1 = cmd_prefix + 'slime'
cmd_giveslime = cmd_prefix + 'giveslime'
cmd_giveslime_alt1 = cmd_prefix + 'giveslimes'
cmd_help = cmd_prefix + 'help'
cmd_help_alt1 = cmd_prefix + 'command'
cmd_help_alt2 = cmd_prefix + 'commands'
cmd_harvest = cmd_prefix + 'harvest'
cmd_spar = cmd_prefix + 'spar'
cmd_suicide = cmd_prefix + 'suicide'
cmd_haunt = cmd_prefix + 'haunt'
cmd_slimeslots = cmd_prefix + 'slimeslots'
cmd_slimecraps = cmd_prefix + 'slimecraps'
cmd_deadmega = cmd_prefix + 'deadmega'
cmd_invest = cmd_prefix + 'invest'
cmd_slimecredit = cmd_prefix + 'slimecoin'
cmd_slimecredit_alt1 = cmd_prefix + 'slimecredit'
cmd_withdraw = cmd_prefix + 'withdraw'
cmd_exchangerate = cmd_prefix + 'exchangerate'
cmd_exchangerate_alt1 = cmd_prefix + 'exchange'
cmd_slimepachinko = cmd_prefix + 'slimepachinko'
cmd_negaslime = cmd_prefix + 'negaslime'
cmd_equip = cmd_prefix + 'equip'
cmd_data = cmd_prefix + 'data'
cmd_clock = cmd_prefix + 'clock'
cmd_time = cmd_prefix + 'time'
cmd_weather = cmd_prefix + 'weather'
cmd_patchnotes = cmd_prefix + 'patchnotes'
cmd_howl = cmd_prefix + 'howl'
cmd_howl_alt1 = cmd_prefix + '56709'
cmd_transfer = cmd_prefix + 'transfer'
cmd_transfer_alt1 = cmd_prefix + 'xfer'
cmd_menu = cmd_prefix + 'menu'
cmd_order = cmd_prefix + 'order'
cmd_annoint = cmd_prefix + 'annoint'
cmd_disembody = cmd_prefix + 'disembody'
cmd_war = cmd_prefix + 'war'
cmd_toil = cmd_prefix + 'toil'
cmd_inventory = cmd_prefix + 'inventory'
cmd_inventory_alt1 = cmd_prefix + 'inv'
cmd_inventory_alt2 = cmd_prefix + 'stuff'
cmd_inventory_alt3 = cmd_prefix + 'bag'
cmd_move = cmd_prefix + 'move'
cmd_move_alt1 = cmd_prefix + 'goto'
cmd_move_alt2 = cmd_prefix + 'walk'
cmd_inspect = cmd_prefix + 'inspect'
cmd_look = cmd_prefix + 'look'
cmd_map = cmd_prefix + 'map'


# Slime costs/values
slimes_tokill = 20
slimes_permine = 20
slimes_perdrink = 500
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 420
slimes_perspar_base = 3000
slimes_hauntratio = 40
slimes_hauntmax = 5000
slimes_perslot = 100
slimes_perpachinko = 500

# hunger
hunger_max = 250
hunger_pershot = 1
hunger_perspar = 1
hunger_permine = 1
hunger_pertick = 3

#inebriation
inebriation_pertick = 2

# Lifetimes
invuln_onrevive = 0

# Cooldowns
cd_kill = 5
cd_spar = 600
cd_haunt = 600
cd_invest = 1200
cd_boombust = 22

# PvP timer pushouts
time_pvp_kill = 600
time_pvp_mine = 180
time_pvp_haunt = 600
time_pvp_invest_withdraw = 180
time_pvp = 1800

# Emotes
emote_tacobell = "<:tacobell:431273890195570699>"
emote_pizzahut = "<:pizzahut:431273890355085323>"
emote_kfc = "<:kfc:431273890216673281>"
emote_moon = "<:moon:431418525303963649>"
emote_111 = "<:111:431547758181220377>"
emote_copkiller = "<:copkiller:431275071945048075>"
emote_rowdyfucker = "<:rowdyfucker:431275088076079105>"
emote_theeye = "<:theeye:431429098909466634>"
emote_slime1 = "<:slime1:431564830541873182>"
emote_slime4 = "<:slime4:431570132901560320>"
emote_slime5 = "<:slime5:431659469844381717>"
emote_slimeskull = "<:slimeskull:431670526621122562>"
emote_dice1 = "<:dice1:436942524385329162>"
emote_dice2 = "<:dice2:436942524389654538>"
emote_dice3 = "<:dice3:436942524041527298>"
emote_dice4 = "<:dice4:436942524406300683>"
emote_dice5 = "<:dice5:436942524444049408>"
emote_dice6 = "<:dice6:436942524469346334>"

# Common strings.
str_casino_closed = "The Slime Casino only operates at night."
str_exchange_closed = "The Exchange has closed for the night."
str_exchange_specify = "Specify how much {currency} you will {action}."
str_exchange_channelreq = "You must go to the #" + channel_stockexchange + " to {action} your {currency}."
str_exchange_busy = "You can't {action} right now. Your slimebroker is busy."
str_food_channelreq = "There's no food here. Go to the food court to {action}."
str_weapon_wielding_self = "You are wielding"
str_weapon_wielding = "They are wielding"

# Common database columns
col_id_server = 'id_server'

# Database columns for items
col_id_item = "id_item"
col_item_type = "item_type"
col_time_expir = "time_expir"
col_value = "value"
col_stack_max = 'stack_max'
col_stack_size = 'stack_size'
col_soulbound = 'soulbound'

# Database columns for server
col_icon = "icon"

# Database columns for players
col_avatar = "avatar"
col_display_name = "display_name"

# Database columns for users
col_id_user = 'id_user'
col_slimes = 'slimes'
col_slimelevel = 'slimelevel'
col_hunger = 'hunger'
col_totaldamage = 'totaldamage'
col_kills = 'kills'
col_weapon = 'weapon'
col_weaponskill = 'weaponskill'
col_trauma = 'trauma'
col_slimecredit = 'slimecredit'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'
col_bounty = 'bounty'
col_weaponname = 'weaponname'
col_name = 'name'
col_inebriation = 'inebriation'
col_ghostbust = 'ghostbust'
col_faction = 'faction'
col_poi = 'poi'
col_life_state = 'life_state'

# Database columns for markets
col_rate_market = 'rate_market'
col_rate_exchange = 'rate_exchange'
col_slimes_casino = 'slimes_casino'
col_boombust = 'boombust'
col_time_lasttick = 'time_lasttick'
col_slimes_revivefee = 'slimes_revivefee'
col_negaslime = 'negaslime'
col_clock = 'clock'
col_weather = 'weather'

# Database columns for stats
col_total_slime = 'total_slime'
col_total_slimecredit = 'total_slimecredit'
col_total_players = 'total_players'
col_total_players_pvp = 'total_players_pvp'
col_timestamp = 'timestamp'

# Item type names
it_medal = "medal"
it_slimepoudrin = "slimepoudrin"

# The highest level your weaponskill may be on revive. All skills over this level reset to this level.
weaponskill_max_onrevive = 3

# Places you might get !shot
hitzone_list = [
	"wrist",
	"leg",
	"arm",
	"upper back",
	"foot",
	"shoulder",
	"neck",
	"kneecap",
	"obliques",
	"solar plexus",
	"Achilles' tendon",
	"jaw",
	"ankle",
	"trapezius",
	"thigh",
	"chest",
	"gut",
	"abdomen",
	"lower back",
	"calf"
]

# A Weapon Effect Function for "gun". Takes an EwEffectContainer as ctn.
def wef_gun(ctn = None):
	aim = (random.randrange(10) + 1)

	if aim == 1:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim == 10:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "rifle"
def wef_rifle(ctn = None):
	aim = (random.randrange(10) + 1)

	if aim <= 2:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= 9:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "nun-chucks"
def wef_nunchucks(ctn = None):
	ctn.strikes = 0
	count = 5
	while count > 0:
		if random.randrange(3) == 1:
			ctn.strikes += 1

		count -= 1

	if ctn.strikes == 5:
		ctn.crit = True
	elif ctn.strikes == 0:
		ctn.miss = True
		ctn.user_data.slimes -= int(ctn.slimes_damage / 2)

# weapon effect function for "katana"
def wef_katana(ctn = None):
	ctn.miss = False
	ctn.slimes_damage = int(0.8 * ctn.slimes_damage)
	if(random.randrange(10) + 1) == 10:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "bat"
def wef_bat(ctn = None):
	aim = (random.randrange(21) - 10)
	if aim <= -9:
		ctn.miss = True
		ctn.slimes_damage = 0

	ctn.slimes_damage = int(ctn.slimes_damage * (1 + (aim / 10)))

	if aim >= 9:
		ctn.crit = True
		ctn.slimes_damage = int(ctn.slimes_damage * 1.5)

# weapon effect function for "garrote"
def wef_garrote(ctn = None):
	ctn.slimes_damage *= 0.5
	aim = (random.randrange(100) + 1)
	if aim <= 50:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim == 100:
		ctn.slimes_damage *= 100
		ctn.crit = True

# weapon effect function for "brassknuckles"
def wef_brassknuckles(ctn = None):
	aim1 = (random.randrange(21) - 10)
	aim2 = (random.randrange(21) - 10)
	whiff1 = 1
	whiff2 = 1

	if aim1 == -9:
		whiff1 = 0
	if aim2 == -9:
		whiff2 = 0

	if whiff1 == 0 and whiff2 == 0:
		ctn.miss = True
		ctn.slimes_damage = 0
	else:
		ctn.slimes_damage = int((((ctn.slimes_damage * (1 + (aim1 / 20))) * whiff1) / 2) + (((ctn.slimes_damage * (1 + (aim2 / 20))) * whiff2) / 2))

# weapon effect function for "molotov"
def wef_molotov(ctn = None):
	ctn.slimes_damage += int(ctn.slimes_damage / 2)
	aim = (random.randrange(100) + 1)

	if aim <= 10:
		ctn.crit = True
		ctn.user_data.slimes -= ctn.slimes_damage
	elif aim > 10 and aim <= 20:
		ctn.miss = True
		ctn.slimes_damage = 0

# weapon effect function for "knives"
def wef_knives(ctn = None):
	ctn.user_data.slimes += int(ctn.slimes_spent * 0.33)
	ctn.slimes_damage = int(ctn.slimes_damage * 0.85)
	aim = (random.randrange(10) + 1)

	if aim <= 1:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= 10:
		ctn.crit = True
		ctn.slimes_damage = int(ctn.slimes_damage * 2)

# weapon effect function for "scythe"
def wef_scythe(ctn = None):
	ctn.user_data.slimes -= int(ctn.slimes_spent * 0.33)
	ctn.slimes_damage = int(ctn.slimes_damage * 1.25)
	aim = (random.randrange(10) + 1)

	if aim <= 2:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= 9:
		ctn.crit = True
		ctn.slimes_damage *= 2

# All weapons in the game.
weapon_list = [
	EwWeapon( # 1
		id_weapon = "gun",
		alias = [
			"pistol",
			"pistols",
			"dualpistols"
		],
		str_crit = "**Critical Hit!** {name_player} has put dealt {name_target} a serious wound!",
		str_miss = "**You missed!** Your shot failed to land!",
		str_equip = "You equip the dual pistols.",
		str_weapon = "dual pistols",
		str_weaponmaster_self = "You are a rank {rank} master of the dual pistols.",
		str_weaponmaster = "They are a rank {rank} master of the dual pistols.",
		str_trauma_self = "You have scarring on both temples, which occasionally bleeds.",
		str_trauma = "They have scarring on both temples, which occasionally bleeds.",
		str_kill = "{name_player} puts their gun to {name_target}'s head. **BANG**. Execution-style. Blood pools across the hot asphalt. {emote_skull}",
		str_damage = "{name_target} takes a bullet to the {hitzone}!!",
		str_duel = "**BANG BANG.** {name_player} and {name_target} practice their quick-draw, bullets whizzing past one another's heads.",
		fn_effect = wef_gun
	),
	EwWeapon( # 2
		id_weapon = "rifle",
		alias = [
			"assaultrifle",
			"machinegun"
		],
		str_crit = "**Critical hit!!** You unload an entire magazine into the target!!",
		str_miss = "**You missed!** Not one of your bullets connected!!",
		str_equip = "You equip the assault rifle.",
		str_weapon = "an assault rifle",
		str_weaponmaster_self = "You are a rank {rank} master of the assault rifle.",
		str_weaponmaster = "They are a rank {rank} master of the assault rifle.",
		str_trauma_self = "Your torso is riddled with scarred-over bulletholes.",
		str_trauma = "Their torso is riddled with scarred-over bulletholes.",
		str_kill = "**RAT-TAT-TAT-TAT-TAT!!** {name_player} rains a hail of bullets directly into {name_target}!! They're officially toast! {emote_skull}",
		str_damage = "Bullets rake over {name_target}'s {hitzone}!!",
		str_duel = "**RAT-TAT-TAT-TAT-TAT!!** {name_player} and {name_target} practice shooting at distant targets with quick, controlled bursts.",
		fn_effect = wef_rifle
	),
	EwWeapon( # 3
		id_weapon = "nun-chucks",
		alias = [
			"nanchacku",
			"numchucks",
			"nunchucks"
		],
		str_crit = "**COMBO!** {name_player} strikes {name_target} with a flurry of 5 vicious blows!",
		str_miss = "**Whack!!** {name_player} fucks up his kung-fu routine and whacks himself in the head with his own nun-chucks!!",
		str_equip = "You equip the nun-chucks.",
		str_weapon = "nun-chucks",
		str_weaponmaster_self = "You are a rank {rank} kung-fu master.",
		str_weaponmaster = "They are a rank {rank} kung-fu master.",
		str_trauma_self = "You are covered in deep bruises. You hate martial arts of all kinds.",
		str_trauma = "They are covered in deep bruises. They hate martial arts of all kinds.",
		str_kill = "**HIIII-YAA!!** With expert timing, {name_player} brutally batters {name_target} to death, then strikes a sweet kung-fu pose. {emote_skull}",
		str_damage = "{name_target} takes {strikes} nun-chuck whacks directly in the {hitzone}!!",
		str_duel = "**HII-YA! HOOOAAAAAHHHH!!** {name_player} and {name_target} twirl wildly around one another, lashing out with kung-fu precision.",
		fn_effect = wef_nunchucks
	),
	EwWeapon( # 4
		id_weapon = "katana",
		alias = [
			"sword",
			"ninjasword",
			"samuraisword",
			"blade"
		],
		str_crit = "**Critical hit!!** {name_target} is cut deep!!",
		str_miss = "",
		str_equip = "You equip the katana.",
		str_weapon = "a katana",
		str_weaponmaster_self = "You are a rank {rank} blademaster.",
		str_weaponmaster = "They are a rank {rank} blademaster.",
		str_trauma_self = "A single clean scar runs across the entire length of your body.",
		str_trauma = "A single clean scar runs across the entire length of their body.",
		str_kill = "Faster than the eye can follow, {name_player}'s blade glints in the greenish light. {name_target} falls over, now in two pieces. {emote_skull}",
		str_damage = "{name_target} is slashed across the {hitzone}!!",
		str_duel = "**CRACK!! THWACK!! CRACK!!** {name_player} and {name_target} duel with bamboo swords, viciously striking at head, wrist and belly.",
		fn_effect = wef_katana
	),
	EwWeapon( # 5
		id_weapon = "bat",
		alias = [
			"club",
			"batwithnails",
			"nailbat",
		],
		str_crit = "**Critical hit!!** {name_player} has bashed {name_target} up real bad!",
		str_miss = "**MISS!!** {name_player} swung wide and didn't even come close!",
		str_equip = "You equip the bat with nails in it.",
		str_weaponmaster_self = "You are a rank {rank} master of the nailbat.",
		str_weaponmaster = "They are a rank {rank} master of the nailbat.",
		str_weapon = "a bat full of nails",
		str_trauma_self = "Your head appears to be slightly concave on one side.",
		str_trauma = "Their head appears to be slightly concave on one side.",
		str_kill = "{name_player} pulls back for a brutal swing! **CRUNCCHHH.** {name_target}'s brains splatter over the sidewalk. {emote_skull}",
		str_damage = "{name_target} is struck with a hard blow to the {hitzone}!!",
		str_duel = "**SMASHH! CRAASH!!** {name_player} and {name_target} run through the neighborhood, breaking windshields, crushing street signs, and generally having a hell of a time.",
		fn_effect = wef_bat
	),
	EwWeapon( # 6
		id_weapon = "garrote",
		alias = [
			"wire",
			"garrotewire",
			"garrottewire"
		],
		str_crit = "**CRITICAL HIT!!** {name_player} got lucky and caught {name_target} completely unaware!!",
		str_miss = "**MISS!** {name_player}'s target got away in time!",
		str_equip = "You equip the garrotte wire.",
		str_weapon = "a garrotte wire",
		str_weaponmaster_self = "You are a rank {rank} master of the garrotte.",
		str_weaponmaster = "They are a rank {rank} master of the garrotte.",
		str_trauma_self = "There is noticeable bruising and scarring around your neck.",
		str_trauma = "There is noticeable bruising and scarring around their neck.",
		str_kill = "{name_player} quietly moves behind {name_target} and... **!!!** After a brief struggle, only a cold body remains. {emote_skull}",
		str_damage = "{name_target} is ensnared by {name_player}'s wire!!",
		str_duel = "{name_player} and {name_target} compare their dexterity by playing Cat's Cradle with deadly wire.",
		fn_effect = wef_garrote
	),
	EwWeapon( # 7
		id_weapon = "brassknuckles",
		alias = [
			"knuckles",
			"knuckledusters",
			"dusters"
		],
		str_crit = "",
		str_miss = "**MISS!** {name_player} couldn't land a single blow!!",
		str_equip = "You equip the brass knuckles.",
		str_weapon = "brass knuckles",
		str_weaponmaster_self = "You are a rank {rank} master pugilist.",
		str_weaponmaster = "They are a rank {rank} master pugilist.",
		str_trauma_self = "You've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_trauma = "They've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_kill = "{name_player} slugs {name_target} right between the eyes! *POW! THWACK!!* **CRUNCH.** Shit. May have gotten carried away there. Oh, well. {emote_skull}",
		str_damage = "{name_target} is socked in the {hitzone}!!",
		str_duel = "**POW! BIFF!!** {name_player} and {name_target} take turns punching each other in the abs. It hurts so good.",
		fn_effect = wef_brassknuckles
	),
	EwWeapon( # 8
		id_weapon = "molotov",
		alias = [
			"firebomb",
			"molotovcocktail",
			"bomb",
			"bombs"
		],
		str_crit = "**Oh, the humanity!!** The bottle bursts in {name_player}'s hand, burning them terribly!!",
		str_miss = "**A dud!!** the rag failed to ignite the molotov!",
		str_equip = "You equip the molotov cocktail.",
		str_weapon = "molotov cocktails",
		str_weaponmaster_self = "You are a rank {rank} master arsonist.",
		str_weaponmaster = "They are a rank {rank} master arsonist.",
		str_trauma_self = "You're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_trauma = "They're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_kill = "**SMASH!** {name_target}'s front window shatters and suddenly flames are everywhere!! The next morning, police report that {name_player} is suspected of arson. {emote_skull}",
		str_damage = "{name_target} dodges a bottle, but is singed on the {hitzone} by the blast!!",
		str_duel = "{name_player} and {name_target} compare notes on frontier chemistry, seeking the optimal combination of combustibility and fuel efficiency.",
		fn_effect = wef_molotov
	),
	EwWeapon( # 9
		id_weapon = "knives",
		alias = [
			"knife",
			"dagger",
			"daggers",
			"throwingknives",
			"throwingknife"
		],
		str_crit = "**Critical hit!!** {name_player}'s knife strikes a vital point!",
		str_miss = "**MISS!!** {name_player}'s knife missed its target!",
		str_equip = "You equip the throwing knives.",
		str_weapon = "throwing knives",
		str_weaponmaster_self = "You are a rank {rank} master of the throwing knife.",
		str_weaponmaster = "They are a rank {rank} master of the throwing knife.",
		str_trauma_self = "You are covered in scarred-over lacerations and puncture wounds.",
		str_trauma = "They are covered in scarred-over lacerations and puncture wounds.",
		str_kill = "A blade flashes through the air!! **THUNK.** {name_target} is a goner, but {name_player} slits their throat before fleeing the scene, just to be safe. {emote_skull}",
		str_damage = "{name_target} is stuck by a knife in the {hitzone}!!",
		str_duel = "**TING! TING!!** {name_player} and {name_target} take turns hitting one another's knives out of the air.",
		fn_effect = wef_knives
	),
	EwWeapon( # 10
		id_weapon = "scythe",
		alias = [
			"sickle"
		],
		str_crit = "**Critical hit!!** {name_target} is carved by the wicked curved blade!",
		str_miss = "**MISS!!** {name_player}'s swings wide of the target!",
		str_equip = "You equip the scythe.",
		str_weapon = "a scythe",
		str_weaponmaster_self = "You are a rank {rank} master of the scythe.",
		str_weaponmaster = "They are a rank {rank} master of the scythe.",
		str_trauma_self = "You are wrapped tightly in bandages that hold your two halves together.",
		str_trauma = "They are wrapped tightly in bandages that hold their two halves together.",
		str_kill = "**SLASHH!!** {name_player}'s scythe cleaves the air, and {name_target} staggers. A moment later, {name_target}'s torso topples off their waist. {emote_skull}",
		str_damage = "{name_target} is cleaved through the {hitzone}!!",
		str_duel = "**WHOOSH, WHOOSH** {name_player} and {name_target} swing their blades in wide arcs, dodging one another's deadly slashes.",
		fn_effect = wef_scythe
	)
]

# A map of id_weapon to EwWeapon objects.
weapon_map = {}

# A list of weapon names
weapon_names = []

# Populate weapon map, including all aliases.
for weapon in weapon_list:
	weapon_map[weapon.id_weapon] = weapon
	weapon_names.append(weapon.id_weapon)

	for alias in weapon.alias:
		weapon_map[alias] = weapon

# All weather effects in the game.
weather_list = [
	EwWeather(
		name = "sunny",
		sunrise = "The smog is beginning to clear in the sickly morning sunlight.",
		day = "The sun is blazing on the cracked streets, making the air shimmer.",
		sunset = "The sky is darkening, the low clouds an iridescent orange.",
		night = "The moon looms yellow as factories belch smoke all through the night."
	),
	EwWeather(
		name = "rainy",
		sunrise = "Rain gently beats against the pavement as the sky starts to lighten.",
		day = "Rain pours down, collecting in oily rivers that run down sewer drains.",
		sunset = "Distant thunder rumbles as it rains, the sky now growing dark.",
		night = "Silverish clouds hide the moon, and the night is black in the heavy rain."
	),
	EwWeather(
		name = "windy",
		sunrise = "Wind whips through the city streets as the sun crests over the horizon.",
		day = "Paper and debris are whipped through the city streets by the winds, buffetting pedestrians.",
		sunset = "The few trees in the city bend and strain in the wind as the sun slowly sets.",
		night = "The dark streets howl, battering apartment windows with vicious night winds."
	),
	EwWeather(
		name = "lightning",
		sunrise = "An ill-omened morning dawns as lighting streaks across the sky in the sunrise.",
		day = "Flashes of bright lightning and peals of thunder periodically startle the citizens out of their usual stupor.",
		sunset = "Bluish white arcs of electricity tear through the deep red dusky sky.",
		night = "The dark night periodically lit with bright whitish-green bolts that flash off the metal and glass of the skyscrapers."
	),
	EwWeather(
		name = "cloudy",
		sunrise = "The dim morning light spreads timidly across the thickly clouded sky.",
		day = "The air hangs thick, and the pavement is damp with mist from the clouds overhead.",
		sunset = "The dusky light blares angry red on a sky choked with clouds and smog.",
		night = "Everything is dark and still but the roiling clouds, reflecting the city's eerie light."
	),
	EwWeather(
		name = "snow",
		sunrise = "The morning sun glints off the thin layer or powdery snow that blankets the city.",
		day = "Flakes of snow clump together and whip through the bitter cold air in the winder wind.",
		sunset = "The cold air grows colder as the sky darkens and the snow piles higher in the streets.",
		night = "Icy winds whip through the city, white snowflakes glittering in the black of night."
	),
		EwWeather(
		name = "foggy",
		sunrise = "Fog hangs thick in the air, stubbornly refusing to dissipate as the sun clears the horizon.",
		day = "You can barely see to the next block in the sickly greenish NLAC smog.",
		sunset = "Visibility only grows worse in the fog as the sun sets and the daylight fades.",
		night = "Everything is obscured by the darkness of night and the thick city smog."
	),
		EwWeather(
		name = "gray",
		sunrise = "Everything is still and gray.",
		day = "Everything is still and gray.",
		sunset = "Everything is still and gray.",
		night = "Everything is still and gray."
	)
]

# Food vendor names
vendor_slipperymolotov = 'The Slippery Molotov Bar & Lounge'
vendor_pizzahut = 'Pizza Hut'
vendor_tacobell = 'Taco Bell'
vendor_kfc = 'KFC'
vendor_mtndew = 'Mtn Dew Fountain'

# A map of name to EwWeather objects.
weather_map = {}
for weather in weather_list:
	weather_map[weather.name] = weather

# All food items in the game.
food_list = [
	EwFood(
		id_food = "slimentonic",
		alias = [
			"tonic",
		],
		recover_hunger = 20,
		price = 160,
		inebriation = 2,
		str_name = 'slime n\' tonic',
		vendor = vendor_slipperymolotov,
		str_eat = "You stir your slime n' tonic with a thin straw before chugging it lustily."
	),
	EwFood(
		id_food = "slimacolada",
		alias = [
			"colada",
		],
		recover_hunger = 25,
		price = 200,
		inebriation = 2,
		str_name = 'slima colada',
		vendor = vendor_slipperymolotov,
		str_eat = "Slurping down this tropicalish drink gives you a brain freeze. You drink faster to numb the pain."
	),
	EwFood(
		id_food = "slimekashot",
		alias = [
			"shot",
			"slimeka",
		],
		recover_hunger = 5,
		price = 90,
		inebriation = 2,
		str_name = 'shot of slimeka',
		vendor = vendor_slipperymolotov,
		str_eat = "Your throat burns as you toss back a mouthful of the glowing, hissing liquid. You might need a doctor."
	),
	EwFood(
		id_food = "cabernetslimeignon",
		alias = [
			"wine",
			"cabernet",
			"slimeignon",
			"bottle",
		],
		recover_hunger = 40,
		price = 3000,
		inebriation = 4,
		str_name = 'bottle of vintage cabernet slimeignon',
		vendor = vendor_slipperymolotov,
		str_eat = "Ahh, you have a keen eye. 19XX was an excellent year. You pop the cork and gingerly have a sniff. Then you gulp the whole bottle down in seconds, because fuck it."
	),
	EwFood(
		id_food = "slimynipple",
		alias = [
			"",
		],
		recover_hunger = 10,
		price = 180,
		inebriation = 2,
		str_name = 'slimy nipple',
		vendor = vendor_slipperymolotov,
		str_eat = "You drink the small glass of creamy, greenish layered fluids in one gulp."
	),
	EwFood(
		id_food = "slimeonthebeach",
		alias = [
			"beach",
		],
		recover_hunger = 30,
		price = 240,
		inebriation = 2,
		str_name = 'slime on the beach',
		vendor = vendor_slipperymolotov,
		str_eat = "You look pretty stupid holding this fluorescent drink with a lil umbrella in it, but you don't care. Bottoms up!"
	),
		EwFood(
		id_food = "goobalibre",
		alias = [
			"goo",
		],
		recover_hunger = 30,
		price = 160,
		inebriation = 2,
		str_name = 'goo-ba libre',
		vendor = vendor_slipperymolotov,
		str_eat = "The drink oozes tartly down your throat. It's pretty nasty, but you still like it."
	),
		EwFood(
		id_food = "manhattanproject",
		alias = [
			"manhattan",
		],
		recover_hunger = 25,
		price = 200,
		inebriation = 3,
		str_name = 'slime on the beach',
		vendor = vendor_slipperymolotov,
		str_eat = "Downing your drink, the alcohol hits your bloodstream with the force of an atomic bomb."
	),
	EwFood(
		id_food = "slimymary",
		alias = [
			"mary",
		],
		recover_hunger = 35,
		price = 140,
		inebriation = 2,
		str_name = 'slimy mary',
		vendor = vendor_slipperymolotov,
		str_eat = "This drink smells pretty nasty even by NLACakaNM standards. But what are you gonna do, NOT drink it?"
	),
	EwFood(
		id_food = "slimestout",
		alias = [
			"stout",
			"beer",
		],
		recover_hunger = 30,
		price = 150,
		inebriation = 2,
		str_name = 'stein of dark slime stout',
		vendor = vendor_slipperymolotov,
		str_eat = "The bartender pours you a rich, dark-green slime stout from the tap, with a head so thick you could rest a SlimeCoin on it."
	),
	EwFood(
		id_food = "water",
		alias = [
			"",
		],
		recover_hunger = 0,
		price = 0,
		inebriation = 0,
		str_name = 'glass of water',
		vendor = vendor_slipperymolotov,
		str_eat = "The bartender sighs as he hands you a glass of water. You drink it. You're not sure why you bothered, though."
	),
	EwFood(
		id_food = "pizza",
		alias = [
			"pizzaslice",
		],
		recover_hunger = 40,
		price = 70,
		inebriation = 0,
		str_name = 'slice of pizza',
		vendor = vendor_pizzahut,
		str_eat = "You grab a hot slice of that cheesy pie! Radical!!"
	),
	EwFood(
		id_food = "pepperoni",
		alias = [
			"peperoni",
		],
		recover_hunger = 60,
		price = 110,
		inebriation = 0,
		str_name = 'slice of pepperoni pizza',
		vendor = vendor_pizzahut,
		str_eat = "You chomp into the spicy sausage slice, bro! Cowabunga!!"
	),
	EwFood(
		id_food = "meatlovers",
		alias = [
			"meatpizza",
		],
		recover_hunger = 70,
		price = 160,
		inebriation = 0,
		str_name = 'slice of Meat Lover\'s pizza',
		vendor = vendor_pizzahut,
		str_eat = "You scarf down a meaty slice! You're sickened and nauseated by the sheer volume of animal fat you're ingesting! Tubular!!"
	),
	EwFood(
		id_food = "wings",
		alias = [
			"buffalowings",
		],
		recover_hunger = 90,
		price = 175,
		inebriation = 0,
		str_name = 'buffalo wings',
		vendor = vendor_pizzahut,
		str_eat = "Aw yeah! Your mouth burns with passion!! Your lips are in agony!! You've never felt so alive!!!"
	),
	EwFood(
		id_food = "taco",
		alias = [
			"softtaco",
		],
		recover_hunger = 30,
		price = 50,
		inebriation = 0,
		str_name = 'soft taco',
		vendor = vendor_tacobell,
		str_eat = "It's a taco. Pretty good, you guess. But it's missing something... a blast of flavor perhaps?"
	),
	EwFood(
		id_food = "nachocheesetaco",
		alias = [
			"nachocheese",
			"nachotaco"
		],
		recover_hunger = 40,
		price = 70,
		inebriation = 0,
		str_name = 'Nacho Cheese taco',
		vendor = vendor_tacobell,
		str_eat = "You slam your filthy mouth into a cheesy blast of nacho flavor!! *YEEAAAHHHH!!!*"
	),
	EwFood(
		id_food = "coolranchtaco",
		alias = [
			"ranchtaco",
		],
		recover_hunger = 40,
		price = 70,
		inebriation = 0,
		str_name = 'Cool Ranch taco',
		vendor = vendor_tacobell,
		str_eat = "You crash your teeth into an explosion of cool ranch taco flavor!! *YEEAAAHHHH!!!*"
	),
	EwFood(
		id_food = "quesarito",
		alias = [
			"gordita",
		],
		recover_hunger = 60,
		price = 100,
		inebriation = 0,
		str_name = 'chicken quesarito',
		vendor = vendor_tacobell,
		str_eat = "It's a burrito, or something. It's got cheese in it. Whatever. You eat it and embrace nothingness."
	),
	EwFood(
		id_food = "steakvolcanoquesomachorito",
		alias = [
			"machorito",
			"quesomachorito"
		],
		recover_hunger = 140,
		price = 250,
		inebriation = 0,
		str_name = 'SteakVolcanoQuesoMachoRito',
		vendor = vendor_tacobell,
		str_eat = "It's a big fucking mess of meat, vegetables, tortilla, cheese, and whatever else happened to be around. You gobble it down greedily!!"
	),
	EwFood(
		id_food = "coleslaw",
		alias = [
			"slaw",
		],
		recover_hunger = 20,
		price = 55,
		inebriation = 0,
		str_name = 'tub of cole slaw',
		vendor = vendor_kfc,
		str_eat = "It's a cup of some gross white cabbage swimming in watery mayo. Why the fuck would you order this?"
	),
	EwFood(
		id_food = "biscuitngravy",
		alias = [
			"biscuit",
			"gravy"
		],
		recover_hunger = 30,
		price = 55,
		inebriation = 0,
		str_name = 'biscuit with a side of gravy',
		vendor = vendor_kfc,
		str_eat = "You get a biscuit and a small bucket of brown gravy. You dip the biscuit, scarf it down, then chug the gravy. *burp.*"
	),
	EwFood(
		id_food = "chickenbucket",
		alias = [
			"bucket",
			"chicken",
		],
		recover_hunger = 120,
		price = 220,
		inebriation = 0,
		str_name = '8-piece fried chicken bucket',
		vendor = vendor_kfc,
		str_eat = "You feast on hot, crispy, dripping white meat. Your fingers and tongue are scalded and you don't give a shit."
	),
	EwFood(
		id_food = "famousbowl",
		alias = [
			"gordita",
		],
		recover_hunger = 70,
		price = 130,
		inebriation = 0,
		str_name = 'Famous Mashed Potato Bowl',
		vendor = vendor_kfc,
		str_eat = "You scarf down a shitty plastic bowl full of jumbled-up bullshit. It really hits the spot!"
	),
	EwFood(
		id_food = "barbecuesauce",
		alias = [
			"bbqsauce",
			"sauce",
			"saucepacket",
		],
		recover_hunger = 5,
		price = 10,
		inebriation = 0,
		str_name = 'packet of BBQ Sauce',
		vendor = vendor_kfc,
		str_eat = "You disgard what's left of your dignity and purchace a packet of barbeque sauce to slurp down."
	),
	EwFood(
		id_food = "mtndew",
		alias = [
			"dew",
			"mountaindew",
			"greendew"
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with vivid green swill and gulp it down."
	),
	EwFood(
		id_food = "bajablast",
		alias = [
			"bluedew",
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew Baja Blast',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with light bluish swill and gulp it down."
	),
	EwFood(
		id_food = "codered",
		alias = [
			"reddew",
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew Code Red',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with red swill and gulp it down."
	),
	EwFood(
		id_food = "pitchblack",
		alias = [
			"blackdew",
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew Pitch Black',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with dark purple swill and gulp it down."
	),
	EwFood(
		id_food = "whiteout",
		alias = [
			"whitedew",
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew White-Out',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with pale cloudy swill and gulp it down."
	),
	EwFood(
		id_food = "livewire",
		alias = [
			"orangedew",
		],
		recover_hunger = 20,
		price = 35,
		inebriation = 0,
		str_name = 'Mtn Dew Livewire',
		vendor = vendor_mtndew,
		str_eat = "You fill your jumbo fountain drink vessel with orange swill and gulp it down."
	)
]

# A map of id_food to EwFood objects.
food_map = {}

# A list of food names
food_names = []

# A map of vendor names to their foods.
food_vendor_inv = {}

# Populate food map, including all aliases.
for food in food_list:
	food_map[food.id_food] = food
	food_names.append(food.id_food)

	# Add food to its vendor's list.
	vendor_list = food_vendor_inv.get(food.vendor)
	if vendor_list == None:
		vendor_list = []
		food_vendor_inv[food.vendor] = vendor_list

	vendor_list.append(food.id_food)

	for alias in food.alias:
		food_map[alias] = food

howls = [
	'**AWOOOOOOOOOOOOOOOOOOOOOOOO**',
	'**5 6 7 0 9**',
	'**awwwwwWWWWWooooOOOOOOOOO**',
	'**awwwwwwwwwooooooooooooooo**',
	'*awoo* *awoo* **AWOOOOOOOOOOOOOO**',
	'*awoo* *awoo* *awoo*',
	'**awwwwwWWWWWooooOOOOOOOoo**',
	'**AWOOOOOOOOOOOOOOOOOOOOOOOOOOOOO**',
	'**AWOOOOOOOOOOOOOOOOOOOO**',
	'**AWWWOOOOOOOOOOOOOOOOOOOO**'
]

"""
	The list of item definitions. Instances of items are always based on these
	skeleton definitions.
"""
item_def_list = [
	EwItemDef(
		# Unique item identifier. Not shown to players.
		item_type = "demo",

		# The name of the item that players will see.
		str_name = "Demo",

		# The description shown when you look at an item.
		str_desc = "A demonstration item."
	),

	# A customizable award object.
	EwItemDef(
		item_type = it_medal,
		str_name = "{medal_name}",
		str_desc = "{medal_desc}",
		soulbound = True,
		item_props = {
			'medal_name': 'Blank Medal',
			'medal_desc': 'An uninscribed medal with no remarkable features.'
		}
	),

	EwItemDef(
		item_type = it_slimepoudrin,
		str_name = "Slime Poudrin",
		str_desc = "A dense, crystalized chunk of precious slime."
	),
]

# A map of item_type to EwItemDef objects.
item_def_map = {}

# Populate the item def map.
for item_def in item_def_list:
	item_def_map[item_def.item_type] = item_def

poi_list = [
	EwPoi( # 1
		id_poi = poi_id_downtown,
		alias = [
			"central",
			"dt",
		],
		str_name = "Downtown NLACakaNM",
		str_desc = "Skyscrapers tower over every street as far as the eye can see. Fluorescent signs flash advertisements in strange glyphs and the streets roar with the sound of engines and scraping metal from the subway deep underground.\n\nThis area contains the Slime Stock Exchange. To the north is Smogsburg. To the East is the Green Light District. To the South is the Rowdy Roughhouse. To the Southwest is Poudrin Alley. To the West is Krak Bay. To the Northwest is Cop Killtown.",
		coord = (23, 16),
		channel = "downtown",
		role = "Downtown"
	),
	EwPoi( # 2
		id_poi = "smogsburg",
		alias = [
			"smog",
			"smogs",
		],
		str_name = "Smogsburg",
		str_desc = "The pavement rumbles as subway trains grind along their tracks far beneath your feet. In every direction, smokestacks belch sickly clouds into the sky.\n\nThis area contains the Bazaar. To the North is Arsonbrook. To the Northeast is Little Chernobyl. To the East is Old New Yonkers. To the South is Downtown NLACakaNM. To the West is Cop Killtown. To the Northwest is Astatine Heights.",
		coord = (23, 11),
		channel = "smogsburg",
		role = "Smogsburg"
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
		str_desc = "Deep indigo edifices of metal and brick rise above the pavement. Apartment windows glint in the blue and purple light of neon signs, and a menacing cathedral looms darkly on the horizon.\n\nTo the North is Astatine Heights. To the Northeast is Little Chernobyl. To the East is Smogsburg. To the Southeast is Downtown NLACakaNM. To the West is Vandal Park. To the Northwest is Gatlingsdale.",
		coord = (17, 13),
		channel = "cop-killtown",
		role = "Cop Killtown",
		pvp = False,
		factions = [
			faction_killers
		]
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
		str_desc = "Off the nearby riverbank, rusty barges churn their way along the Slime River. Posh riverside apartments taunt you with their cheap opulence.\n\nThis area contains the Food Court. To the East is Downtown NLACakaNM. To the Southeast is Poudrin Alley. To the South is Ooze Gardens. To the Southwest is South Sleezeborough. To the West is North Sleezeborough. To the Northwest is Glocksbury.",
		coord = (16, 19),
		channel = "krak-bay",
		role = "Krak Bay"
	),
	EwPoi( # 5
		id_poi = "poudrinalley",
		alias = [
			"poudrin"
		],
		str_name = "Poudrin Alley",
		str_desc = "Bent and broken streetlights spark and flicker over the cracked, derelict pavement. The 7-11 stands dimly opposite a row of apartments, its CLOSED sign crooked and dusty.\n\nThis area contains the 7-11. To the Northeast is Downtown NLACakaNM. To the East is the Rowdy Roughhouse. To the South is Cratersville. To the Southwest is Ooze Gardens. To the Northwest is Krak Bay.",
		coord = (19, 23),
		channel = "poudrin-alley",
		role = "Poudrin Alley"
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
		str_desc = "Rusted pink metal shanties are hastily constructed as far as the eye can see, sometimes stacked on top of one another, forming high towers and densely populated mazes.\n\nTo the North is Downtown NLACakaNM. To the South is Wreckington. To the Southwest is Cratersville. To the West is Poudrin Alley.",
		coord = (25, 21),
		channel = "rowdy-roughhouse",
		role = "Rowdy Roughhouse",
		pvp = False,
		factions = [
			faction_rowdys
		]
	),
	EwPoi( # 7
		id_poi = "greenlightdistrict",
		alias = [
			"greenlight"
		],
		str_name = "Green Light District",
		str_desc = "Fluorescent signs flicker bright glyphs over smooth freshly-paved streets, promising all conceivable earthly pleasures. The ground is tacky with some unknown but obviously sinful grime.\n\nThis area contains the Slime Casino. To the East is Juvie's Row. To the West is Downtown NLACakaNM.",
		coord = (29, 14),
		channel = "green-light-district",
		role = "Green Light District"
	),
	EwPoi( # 8
		id_poi = "oldnewyonkers",
		str_name = "Old New Yonkers",
		str_desc = "Rows of three-story brick and stone condominiums with white marble moulding wind along lanes of chipped cobblestone. Wrought-iron spikes jut from windows and balconies.\n\nTo the Northeast is New New Yonkers. To the Southeeast is Vagrant's Corner. To the Southwest is Smogsburg. To the East is Little Chernobyl. To the Northwest is Brawlden.",
		coord = (32, 9),
		channel = "old-new-yonkers",
		role = "Old New Yonkers"
	),
	EwPoi( # 9
		id_poi = "littlechernobyl",
		alias = [
			"chernobyl"
		],
		str_name = "Little Chernobyl",
		str_desc = "Pathetic little gardens front the uneven parking lots of corporate complexes housing dentists, fortune-tellers, real estate agencies, and other equally dull and pointless ventures.\n\nTo the North is Brawlden. To the East is Old New Yonkers. To the West is Arsonbrook.",
		coord = (25, 7),
		channel = "little-chernobyl",
		role = "Little Chernobyl"
	),
	EwPoi( # 10
		id_poi = "arsonbrook",
		alias = [
			"arson"
		],
		str_name = "Arsonbrook",
		str_desc = "North of the bridge, you see large swathes of what were once suburbs blackened and flat, occasionally still smoking. Legends say a Starbucks tried to open here once.\n\nTo the East is Brawlden. To the Southeast is Little Chernobyl. To the South is Smogsburg. To the West is Astatine Heights.",
		coord = (21, 3),
		channel = "arsonbrook",
		role = "Arsonbrook"
	),
	EwPoi( # 11
		id_poi = "astatineheights",
		alias = [
			"astatine"
		],
		str_name = "Astatine Heights",
		str_desc = "Modern high-rise condos just from the steep hills to the north. To the south, classical stone and brick houses with columns command disgustingly decadent wide grassy yards.\n\nThis area contains NLACakaNM Cinemas. To the East is Arsonbrook. To the Southeast is Smogsburg. To the South is Cop Killtown. To the Southwest is Gatlingsdale. To the West is Toxington.",
		coord = (17, 6),
		channel = "astatine-heights",
		role = "Astatine Heights"
	),
	EwPoi( # 12
		id_poi = "gatlingsdale",
		alias = [
			"gatlings",
		],
		str_name = "Gatlingsdale",
		str_desc = "The brightest young minds of NLACakaNM fritter away their time here, amid hallowed halls of learning ringed endlessly by foreign book stores and vintage clothing shops.\n\nTo the Northeast is Astatine Heights. To the Southeast is Cop Killtown. To the Southwest is Vandal Park. To the West is Polonium Hill. To the Northwest is Toxington.",
		coord = (13, 9),
		channel = "gatlingsdale",
		role = "Gatlingsdale"
	),
	EwPoi( # 13
		id_poi = "vandalpark",
		alias = [
			"vandal",
		],
		str_name = "Vandal Park",
		str_desc = "The more-or-less clean air carries the roar of the crowd across the grassy fields surrounding the Battle Arena.\n\nThis area contains the Battle Arena. To the Northeast is Gatlingsdale. To the East is Cop Killtown. To the South is Glocksbury. To the Southwest is West Glocksbury. To the Northwest is Polonium Hill.",
		coord = (10, 12),
		channel = "vandal-park",
		role = "Vandal Park"
	),
	EwPoi( # 14
		id_poi = "glocksbury",
		alias = [
			"glocks"
		],
		str_name = "Glocksbury",
		str_desc = "You smell bacon. *Figurative* bacon. The streets are too orderly here... the cops must be about. Absolutely vile.\n\nTo the North is Vandal Park. To the Southeast is Krak Bay. To the South is North Sleezeborough. To the West is West Glocksbury.",
		coord = (9, 16),
		channel = "glocksbury",
		role = "Glocksbury"
	),
	EwPoi( # 15
		id_poi = "northsleezeborough",
		alias = [
			"northsleezeboro",
			"nsleezeborough",
			"nsleezeboro"
		],
		str_name = "North Sleezeborough",
		str_desc = "Young jobless adults walk around in plaid and suspenders with curious facial hair, stopping into the occasional store front to buy a vinyl recording or an ironic knick-knack.\n\nTo the North is Glocksbury. To the East is Krak Bay. To the South is South Sleezeborough.",
		coord = (11, 19),
		channel = "north-sleezeborough",
		role = "North Sleezeborough"
	),
	EwPoi( # 16
		id_poi = "southsleezeborough",
		alias = [
			"southsleezeboro",
			"ssleezeborough",
			"ssleezeboro"
		],
		str_name = "South Sleezeborough",
		str_desc = "The streets are empty. The residents of this neighborhood have all lost their nerve and are hiding in their hovels in a futile attempts to stay safe from gang violence.\n\nThis area contains the Dojo. To the North is North Sleezeborough. To the Northeast is Krak Bay, To the East is Ooze Gardens.",
		coord = (12, 22),
		channel = "south-sleezeborough",
		role = "South Sleezeborough"
	),
	EwPoi( # 17
		id_poi = "oozegardens",
		alias = [
			"ooze"
		],
		str_name = "Ooze Gardens",
		str_desc = "A bird chirps its last before falling dead from a withered tree. A trickle of slime runs down its bark. The resident's attempts to beautify the neighborhood with foliage have really backfired, aesthetically speaking.\n\nTo the North is Krak Bay. To the Northeast is Poudrin Alley. To the East is Cratersville. To the West is South Sleezeborough.",
		coord = (14, 25),
		channel = "ooze-gardens",
		role = "Ooze Gardens"
	),
	EwPoi( # 18
		id_poi = "cratersville",
		alias = [
			"craters"
		],
		str_name = "Cratersville",
		str_desc = "The people here hurry to their destinations, avoiding eye contact. They must be wary after seeing gang members level the next town over not too long ago.\n\nTo the North is Poudrin Alley. To the Northeast is the Rowdy Roughhouse. To the East is Wreckington. To the West is Ooze Gardens.",
		coord = (19, 28),
		channel = "cratersville",
		role = "Cratersville"
	),
	EwPoi( # 19
		id_poi = "wreckington",
		alias = [
			"wrecking"
		],
		str_name = "Wreckington",
		str_desc = "You step over piles of rubble that once housed the now-displaced population of this neighborhood. A recent a dramatic victim of rampant gang warfare.\n\nTo the North is the Rowdy Roughhouse. To the West is Cratersville.",
		coord = (27, 24),
		channel = "wreckington",
		role = "Wreckington"
	),
	EwPoi( # 20
		id_poi = "juviesrow",
		alias = [
			"juvies",
		],
		str_name = "Juvie's Row",
		str_desc = "Quaint little Juvie shanties pepper the landscape around the entrance to the slime mines. Pale rocks and sticks are arranged in sad fascimiles of white picket fences. You're filled with pity, as well as disgust.\n\nTo the Northeast is Vagrant's Corner. To the Northwest is the Green Light District.",
		coord = (32, 18),
		channel = "juvies-row",
		role = "Juvie's Row",
		pvp = False
	),
	EwPoi( # 21
		id_poi = "slimesend",
		alias = [
			"slimes"
		],
		str_name = "Slime's End",
		str_desc = "The narrow peninsula is bordered on both sides by the Slime Sea. The phosphorescence of the Sea illuminates the land and sky with an eerily even green glow.\n\n To the North is Vagrant's Corner.",
		coord = (40, 16),
		channel = "slimes-end",
		role = "Slime's End"
	),
	EwPoi( # 22
		id_poi = "vagrantscorner",
		alias = [
			"vagrants"
		],
		str_name = "Vagrant's Corner",
		str_desc = "The glow of the Slime Sea illumunates the undersides of the docks and the heavy industrial machinery designed to pump slime into the cargo holds of outbound barges.\n\nThis area contains The King's Wife's Son Speakeasy. To the North is New New Yonkers. To the Northeast is Assault Flats Beach Resort. To the South is Slime's End. To the Southwest is Juvie's Row. To the West is the Green Light District. To the Northwest is Old New Yonkers.",
		coord = (37, 11),
		channel = "vagrants-corner",
		role = "Vagrant's Corner"
	),
	EwPoi( # 23
		id_poi = "assaultflatsbeachresort",
		alias = [
			"assaultflatsbeach",
			"assaultflats",
			"beach",
			"resort",
			"assault",
			"flats",
			"assflats"
		],
		str_name = "Assault Flats Beach Resort",
		str_desc = "The white imported sand of the beach stretches toward the horizon, lapped by gentle waves of slime. Gleaming hotels jut out of the rock formations just off the beachfront.\n\nTo the South is Vagrant's Corner. To the West is New New Yonkers.",
		coord = (40, 6),
		channel = "assault-flats-beach-resort",
		role = "Assault Flats Beach Resort"
	),
	EwPoi( # 24
		id_poi = "newnewyonkers",
		str_name = "New New Yonkers",
		str_desc = "Trendy restaurants and clubs sit empty in this sparsely-populated failed gentrification experiment.\n\nTo the East is Assault Flats Beach Resort. To the South is Vagrant's Corner. To the Southwest is Old New Yonkers. To the West is Brawlden.",
		coord = (36, 4),
		channel = "new-new-yonkers",
		role = "New New Yonkers"
	),
	EwPoi( # 25
		id_poi = "brawlden",
		alias = [
		],
		str_name = "Brawlden",
		str_desc = "Rough-looking bewifebeatered citizens are everywhere, doing unspecified maintenence on strange machines propped up on cinderblocks. A SlimeCorp Laboratory hums and whirrs in the distance, day and night.\n\nThis area contains the Slimeoid Laboratory. To the East is New New Yonkers. To the Southeast is Old New Yonkers. To the South is Little Chernobyl. To the West is Arsonbrook.",
		coord = (28, 3),
		channel = "brawlden",
		role = "Brawlden"
	),
	EwPoi( # 26
		id_poi = "toxington",
		str_name = "Toxington",
		str_desc = "You cover your mouth in a futile attempt to avoid breathing choking acidic vapor that continually rises off of the nearby lake.\n\nTo the East is Astatine Heights. To the Southeast is Gatlingsdale. To the South is Polonium Hill. To the East is Charcoal Park.",
		coord = (9, 4),
		channel = "toxington",
		role = "Toxington"
	),
	EwPoi( # 27
		id_poi = "charcoalpark",
		alias = [
			"charcoal"
		],
		str_name = "Charcoal Park",
		str_desc = "The soil here is mostly black soot and the charred remains of a now long-gone series of low-income apartment complexes. A few shantytowns have been constructed as some of the only living trees in NLACakaNM have sprouted out of the ashes.\n\nTo the East is Toxington. To the South is Polonium Hill.",
		coord = (3, 3),
		channel = "charcoal-park",
		role = "Charcoal Park"
	),
	EwPoi( # 28
		id_poi = "poloniumhill",
		alias = [
			"polonium"
		],
		str_name = "Polonium Hill",
		str_desc = "The gently rolling terrain is speckled with hideous minimansions that obviously cost a fortune and look like complete shit.\n\nTo the North is Charcoal Park. To the Northeast is Toxington. To the East is Gatlingsdale. To the Southeast is Vandal park. To the South is West Glocksbury.",
		coord = (5, 9),
		channel = "polonium-hill",
		role = "Polonium Hill"
	),
	EwPoi( # 29
		id_poi = "westglocksbury",
		alias = [
			"westglocks",
			"wglocks"
		],
		str_name = "West Glocksbury",
		str_desc = "Gunshots ring out periodically from somewhere in the distance, hidden by laundromats and barber shops. Even the most jaded NLACakaNMite may get a bit nervous 'round these parts.\n\n To the North is Polonium Hill. To the Northeast is Vandal Park. To the East is Glocksbury",
		coord = (4, 14),
		channel = "west-glocksbury",
		role = "West Glocksbury"
	),
	EwPoi( # the-sewers
		id_poi = poi_id_thesewers,
		alias = [
			"sewers",
			"sewer"
		],
		str_name = "The Sewers",
		str_desc = "A vast subterranean maze of concrete tunnels, eternally echoing with the dripping of water and decayed slime runoff. All the waste of NLACakaNM eventually winds up here, citizens included.",
		channel = channel_sewers,
		life_states = [
			life_state_corpse
		],
		role = "Sewers",
		pvp = False
	),
	EwPoi( # stock-exchange
		id_poi = poi_id_stockexchange,
		alias = [
			"stocks",
			"exchange",
			"stockexchange",
			"slimestockexchange"
		],
		str_name = "The Slime Stock Exchange",
		str_desc = "A large interior space filled with vacant teller booths and data screens designed to dissplay market data, all powered off. Punch cards and ticker tape are strewn about the silent, empty floor.\n\nExits into Downtown NLACakaNM.",
		channel = channel_stockexchange,
		role = "Stock Exchange",
		coord = (21, 16),
		pvp = False
	),
	EwPoi( # the-bazaar
		id_poi = poi_id_bazaar,
		alias = [
			"bazaar",
			"market"
		],
		str_name = "The Bazaar",
		str_desc = "An open-air marketplace where professional merchants and regular citizens alike can hock their wares. It's currently completely barren.\n\nExits into Brawlden.",
		channel = channel_bazaar,
		role = "Bazaar",
		coord = (21, 11),
		pvp = False
	),
	EwPoi( # the-cinema
		id_poi = poi_id_cinema,
		alias = [
			"nlacakanmcinema",
			"cinema",
			"cinemas",
			"theater",
			"movie",
			"movies"
		],
		str_name = "NLACakaNM Cinemas",
		str_desc = "A delightfully run-down movie theater, with warm carpeted walls fraying ever so slightly. Films hand picked by the Rowdy Fucker and/or Cop Killer are regularly screened.\n\nExits into Astatine Heights.",
		channel = channel_cinema,
		role = "Cinema",
		coord = (17, 4),
		pvp = False
	),
	EwPoi( # food-court
		id_poi = poi_id_foodcourt,
		alias = [
			"thenlacakanmfoodcourt",
			"food",
			"foodcourt",
			"pizzahut",
			"tacobell",
			"kfc"
		],
		str_name = "The NLACakaNM Food Court",
		str_desc = "A large, brightly-lit area with tiled walls and floors, lined on all sides with Yum! Brand food vendors, surrounding the city's prized MTN DEW Fountain. The place is completely dead.\n\nExits into Krak Bay.",
		channel = channel_foodcourt,
		role = "Food Court",
		coord = (16, 17),
		pvp = False
	),
	EwPoi( # nlac-u
		id_poi = poi_id_nlacu,
		alias = [
			"nlacu",
			"university",
			"nlacuniversity",
			"college",
			"uni"
		],
		str_name = "New Los Angeles City University",
		str_desc = "An expansive campus housing massive numbers of students and administrators, all here in pursuit of knowledge. The campus is open to visitors, but there's nobody here.\n\nExits into Gatlingsdale.",
		channel = channel_nlacu,
		role = "NLAC U",
		coord = (14, 10),
		pvp = False
	),
	EwPoi( # battle-arena
		id_poi = poi_id_arena,
		alias = [
			"thearena",
			"arena",
			"battlearena"
		],
		str_name = "The Battle Arena",
		str_desc = "A huge arena stadium capable of housing tens of thousands of battle enthusiasts, ringing a large field where Slimeoid Battles are held. All the seats are empty.\n\nExits into Vandal Park.",
		channel = channel_arena,
		role = "Arena",
		coord = (10, 10),
		pvp = False
	),
	EwPoi( # the-dojo
		id_poi = poi_id_dojo,
		alias = [
			"dojo",
			"training",
			"sparring",
			"thedojo"
		],
		str_name = "The Dojo",
		str_desc = "A modest, easily overlooked building, but containing all the facilities necessary for becoming a killing machine. Bamboo and parchment walls separate the dojo floor into large tatami-matted sections.\n\nExits into South Sleezeborough.",
		channel = channel_dojo,
		role = "Dojo",
		coord = (11, 23),
		pvp = False
	),
	EwPoi( # speakeasy
		id_poi = poi_id_speakeasy,
		alias = [
			"kingswifessonspeakeasy",
			"kingswifesson",
			"speakeasy",
			"bar"
		],
		str_name = "The King's Wife's Son Speakeasy",
		str_desc = "A rustic tavern with dark wooden walls and floor, bearing innumerable knickknacks on the walls and high wooden stools arranged in front of a bar made of patina'd copper. There's nobody here.\n\nExits into Vagrant's Corner.",
		channel = channel_speakeasy,
		role = "Speakeasy",
		coord = (39, 11),
		pvp = False
	),
	EwPoi( # 7-11
		id_poi = poi_id_711,
		alias = [
			"outsidethe7-11",
			"outside7-11",
			"outside711",
			"7-11",
			"711",
			"seveneleven",
			"outsideseveneleven"
		],
		str_name = "Outside the 7-11",
		str_desc = "The darkened derelict 7-11 stands as it always has, a steadfast pillar of NLACakaNM culture. On its dirty exterior walls are spraypainted messages about \"patch notes\", \"github\", and other unparseable nonsense.\n\nExits into Poudrin Alley.",
		channel = channel_711,
		role = "7-11",
		coord = (20, 24),
		pvp = False
	),
	EwPoi( # the-labs
		id_poi = poi_id_slimeoidlab,
		alias = [
			"lab",
			"labs",
			"laboratory",
			"slimecorpslimeoidlaboratory",
			"slimecorpslimeoidlab",
			"slimecorplab",
			"slimecorplabs",
			"slimeoidlaboratory",
			"slimeoidlab",
			"slimeoidlabs"
		],
		str_name = "SlimeCorp Slimeoid Laboratory",
		str_desc = "A nondescript building containing mysterious SlimeCorp industrial equipment. Large glass tubes and metallic vats seem to be designed to serve as incubators. The lab is empty and the equipment is not being powered.\n\nExits into Brawlden.",
		channel = channel_slimeoidlab,
		role = "Slimeoid Lab",
		coord = (28, 1),
		pvp = False
	),
	EwPoi( # the-mines
		id_poi = poi_id_mine,
		alias = [
			"mines",
			"mine"
		],
		str_name = "The Mines",
		str_desc = "", # TODO
		coord = (34, 18),
		channel = channel_mines,
		role = "Mines",
		str_closed = "The negaslime's tendrils clog the entrance to the mines. It is currently inaccessable.",
		pvp = False,
		closed = True
	),
	EwPoi( # the-casino
		id_poi = poi_id_thecasino,
		alias = [
			"casino",
			"slimecasino",
			"theslimecasino"
		],
		str_name = "The Casino",
		str_desc = "The casino is filled with tables and machines for playing games of chance, and garishly decorated wall-to-wall. Lights which normally flash constantly cover everything, but now they all sit unlit.",
		coord = (29, 16),
		channel = channel_casino,
		role = "Casino",
		pvp = False
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
