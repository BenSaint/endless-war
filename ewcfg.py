import random

from ewwep import EwWeapon
from ewweather import EwWeather
from ewfood import EwFood

# Global configuration options.
version = "v1.26"

# Update intervals
update_hookstillactive = 60 * 60 * 3
update_twitch = 60
update_pvp = 60
update_market = 900

# Market delta
max_iw_swing = 30

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

# Slime costs/values
slimes_tokill = 20
slimes_permine = 20
slimes_perdrink = 500
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 420
slimes_perspar = 2500
slimes_hauntratio = 40
slimes_hauntmax = 5000
slimes_perslot = 100
slimes_perpachinko = 500

# stamina
stamina_max = 250
stamina_pershot = 1
stamina_perspar = 1
stamina_permine = 1

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
str_food_channelreq = "You must go to the #" + channel_foodcourt + " to {action}."

# Common database columns
col_id_server = 'id_server'

# Database columns for users
col_id_user = 'id_user'
col_slimes = 'slimes'
col_slimelevel = 'slimelevel'
col_stamina = 'stamina'
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
col_time_expirpvp = 'time_expirpvp'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'
col_bounty = 'bounty'
col_slimepoudrins = 'slimepoudrins'

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
def wef_gun(ctn=None):
	aim = (random.randrange(10) + 1)

	if aim == 1:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim == 10:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "rifle"
def wef_rifle(ctn=None):
	aim = (random.randrange(10) + 1)

	if aim <= 2:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= 9:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "nun-chucks"
def wef_nunchucks(ctn=None):
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
def wef_katana(ctn=None):
	ctn.miss = False
	ctn.slimes_damage = int(0.8 * ctn.slimes_damage)
	if(random.randrange(10) + 1) == 10:
		ctn.crit = True
		ctn.slimes_damage *= 2

# weapon effect function for "bat"
def wef_bat(ctn=None):
	aim = (random.randrange(21) - 10)
	if aim <= -9:
		ctn.miss = True
		ctn.slimes_damage = 0

	ctn.slimes_damage = int(ctn.slimes_damage * (1 + (aim / 10)))

	if aim >= 9:
		ctn.crit = True
		ctn.slimes_damage = int(ctn.slimes_damage * 1.5)

# weapon effect function for "garrote"
def wef_garrote(ctn=None):
	ctn.slimes_damage *= 0.5
	aim = (random.randrange(100) + 1)
	if aim <= 50:
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim == 100:
		ctn.slimes_damage *= 100
		ctn.crit = True

# weapon effect function for "brassknuckles"
def wef_brassknuckles(ctn=None):
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
def wef_molotov(ctn=None):
	ctn.slimes_damage += int(ctn.slimes_damage / 2)
	aim = (random.randrange(100) + 1)

	if aim <= 10:
		ctn.crit = True
		ctn.user_data.slimes -= ctn.slimes_damage
	elif aim > 10 and aim <= 20:
		ctn.miss = True
		ctn.slimes_damage = 0

# weapon effect function for "knives"
def wef_knives(ctn=None):
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
def wef_scythe(ctn=None):
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
		id_weapon="gun",
		alias=[
			"pistol",
			"pistols",
			"dualpistols"
		],
		str_crit="**Critical Hit!** {name_player} has put dealt {name_target} a serious wound!",
		str_miss="**You missed!** Your shot failed to land!",
		str_equip="You equip the dual pistols.",
		str_weapon_self="You are wielding dual pistols.",
		str_weapon="They are wielding dual pistols.",
		str_weaponmaster_self="You are a rank {rank} master of the dual pistols.",
		str_weaponmaster="They are a rank {rank} master of the dual pistols.",
		str_trauma_self="You have scarring on both temples, which occasionally bleeds.",
		str_trauma="They have scarring on both temples, which occasionally bleeds.",
		str_kill="{name_player} puts their gun to {name_target}'s head. **BANG**. Execution-style. Blood pools across the hot asphalt. {emote_skull}",
		str_damage="{name_target} takes a bullet to the {hitzone}!!",
		str_duel="**BANG BANG.** {name_player} and {name_target} practice their quick-draw, bullets whizzing past one another's heads.",
		fn_effect=wef_gun
	),
	EwWeapon( # 2
		id_weapon="rifle",
		alias=[
			"assaultrifle",
			"machinegun"
		],
		str_crit="**Critical hit!!** You unload an entire magazine into the target!!",
		str_miss="**You missed!** Not one of your bullets connected!!",
		str_equip="You equip the assault rifle.",
		str_weapon_self="You are wielding an assult rifle.",
		str_weapon="They are wielding an assault rifle.",
		str_weaponmaster_self="You are a rank {rank} master of the assault rifle.",
		str_weaponmaster="They are a rank {rank} master of the assault rifle.",
		str_trauma_self="Your torso is riddled with scarred-over bulletholes.",
		str_trauma="Their torso is riddled with scarred-over bulletholes.",
		str_kill="**RAT-TAT-TAT-TAT-TAT!!** {name_player} rains a hail of bullets directly into {name_target}!! They're officially toast! {emote_skull}",
		str_damage="Bullets rake over {name_target}'s {hitzone}!!",
		str_duel="**RAT-TAT-TAT-TAT-TAT!!** {name_player} and {name_target} practice shooting at distant targets with quick, controlled bursts.",
		fn_effect=wef_rifle
	),
	EwWeapon( # 3
		id_weapon="nun-chucks",
		alias=[
			"nanchacku",
			"numchucks",
			"nunchucks"
		],
		str_crit="**COMBO!** {name_player} strikes {name_target} with a flurry of 5 vicious blows!",
		str_miss="**Whack!!** {name_player} fucks up his kung-fu routine and whacks himself in the head with his own nun-chucks!!",
		str_equip="You equip the nun-chucks.",
		str_weapon_self="You are wielding nun-chucks.",
		str_weapon="They are wielding nun-chucks.",
		str_weaponmaster_self="You are a rank {rank} kung-fu master.",
		str_weaponmaster="They are a rank {rank} kung-fu master.",
		str_trauma_self="You are covered in deep bruises. You hate martial arts of all kinds.",
		str_trauma="They are covered in deep bruises. They hate martial arts of all kinds.",
		str_kill="**HIIII-YAA!!** With expert timing, {name_player} brutally batters {name_target} to death, then strikes a sweet kung-fu pose. {emote_skull}",
		str_damage="{name_target} takes {strikes} nun-chuck whacks directly in the {hitzone}!!",
		str_duel="**HII-YA! HOOOAAAAAHHHH!!** {name_player} and {name_target} twirl wildly around one another, lashing out with kung-fu precision.",
		fn_effect=wef_nunchucks
	),
	EwWeapon( # 4
		id_weapon="katana",
		alias=[
			"sword",
			"ninjasword",
			"samuraisword",
			"blade"
		],
		str_crit="**Critical hit!!** {name_target} is cut deep!!",
		str_miss="",
		str_equip="You equip the katana.",
		str_weapon_self="You are wielding a katana.",
		str_weapon="They are wielding a katana.",
		str_weaponmaster_self="You are a rank {rank} blademaster.",
		str_weaponmaster="They are a rank {rank} blademaster.",
		str_trauma_self="A single clean scar runs across the entire length of your body.",
		str_trauma="A single clean scar runs across the entire length of their body.",
		str_kill="Faster than the eye can follow, {name_player}'s blade glints in the greenish light. {name_target} falls over, now in two pieces. {emote_skull}",
		str_damage="{name_target} is slashed across the {hitzone}!!",
		str_duel="**CRACK!! THWACK!! CRACK!!** {name_player} and {name_target} duel with bamboo swords, viciously striking at head, wrist and belly.",
		fn_effect=wef_katana
	),
	EwWeapon( # 5
		id_weapon="bat",
		alias=[
			"club",
			"batwithnails",
			"nailbat",
		],
		str_crit="**Critical hit!!** {name_player} has bashed {name_target} up real bad!",
		str_miss="**MISS!!** {name_player} swung wide and didn't even come close!",
		str_equip="You equip the bat with nails in it.",
		str_weapon_self="You are wielding a bat full of nails.",
		str_weaponmaster_self="You are a rank {rank} master of the nailbat.",
		str_weaponmaster="They are a rank {rank} master of the nailbat.",
		str_weapon="They are wielding a bat full of nails.",
		str_trauma_self="Your head appears to be slightly concave on one side.",
		str_trauma="Their head appears to be slightly concave on one side.",
		str_kill="{name_player} pulls back for a brutal swing! **CRUNCCHHH.** {name_target}'s brains splatter over the sidewalk. {emote_skull}",
		str_damage="{name_target} is struck with a hard blow to the {hitzone}!!",
		str_duel="**SMASHH! CRAASH!!** {name_player} and {name_target} run through the neighborhood, breaking windshields, crushing street signs, and generally having a hell of a time.",
		fn_effect=wef_bat
	),
	EwWeapon( # 6
		id_weapon="garrote",
		alias=[
			"wire",
			"garrotewire",
			"garrottewire"
		],
		str_crit="**CRITICAL HIT!!** {name_player} got lucky and caught {name_target} completely unaware!!",
		str_miss="**MISS!** {name_player}'s target got away in time!",
		str_equip="You equip the garrotte wire.",
		str_weapon_self="You are wielding a garrotte wire.",
		str_weapon="They are wielding a garrotte wire.",
		str_weaponmaster_self="You are a rank {rank} master of the garrotte.",
		str_weaponmaster="They are a rank {rank} master of the garrotte.",
		str_trauma_self="There is noticeable bruising and scarring around your neck.",
		str_trauma="There is noticeable bruising and scarring around their neck.",
		str_kill="{name_player} quietly moves behind {name_target} and... **!!!** After a brief struggle, only a cold body remains. {emote_skull}",
		str_damage="{name_target} is ensnared by {name_player}'s wire!!",
		str_duel="{name_player} and {name_target} compare their dexterity by playing Cat's Cradle with deadly wire.",
		fn_effect=wef_garrote
	),
	EwWeapon( # 7
		id_weapon="brassknuckles",
		alias=[
			"knuckles",
			"knuckledusters",
			"dusters"
		],
		str_crit="",
		str_miss="**MISS!** {name_player} couldn't land a single blow!!",
		str_equip="You equip the brass knuckles.",
		str_weapon_self="You are wielding brass knuckles.",
		str_weapon="They are wielding brass knuckles.",
		str_weaponmaster_self="You are a rank {rank} master pugilist.",
		str_weaponmaster="They are a rank {rank} master pugilist.",
		str_trauma_self="You've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_trauma="They've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_kill="{name_player} slugs {name_target} right between the eyes! *POW! THWACK!!* **CRUNCH.** Shit. May have gotten carried away there. Oh, well. {emote_skull}",
		str_damage="{name_target} is socked in the {hitzone}!!",
		str_duel="**POW! BIFF!!** {name_player} and {name_target} take turns punching each other in the abs. It hurts so good.",
		fn_effect=wef_brassknuckles
	),
	EwWeapon( # 8
		id_weapon="molotov",
		alias=[
			"firebomb",
			"molotovcocktail",
			"bomb",
			"bombs"
		],
		str_crit="**Oh, the humanity!!** The bottle bursts in {name_player}'s hand, burning them terribly!!",
		str_miss="**A dud!!** the rag failed to ignite the molotov!",
		str_equip="You equip the molotov cocktail.",
		str_weapon_self="You are wielding molotov cocktails.",
		str_weapon="They are wielding molotov cocktails.",
		str_weaponmaster_self="You are a rank {rank} master arsonist.",
		str_weaponmaster="They are a rank {rank} master arsonist.",
		str_trauma_self="You're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_trauma="They're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_kill="**SMASH!** {name_target}'s front window shatters and suddenly flames are everywhere!! The next morning, police report that {name_player} is suspected of arson. {emote_skull}",
		str_damage="{name_target} dodges a bottle, but is singed on the {hitzone} by the blast!!",
		str_duel="{name_player} and {name_target} compare notes on frontier chemistry, seeking the optimal combination of combustibility and fuel efficiency.",
		fn_effect=wef_molotov
	),
	EwWeapon( # 9
		id_weapon="knives",
		alias=[
			"knife",
			"dagger",
			"daggers",
			"throwingknives",
			"throwingknife"
		],
		str_crit="**Critical hit!!** {name_player}'s knife strikes a vital point!",
		str_miss="**MISS!!** {name_player}'s knife missed its target!",
		str_equip="You equip the throwing knives.",
		str_weapon_self="You are wielding throwing knives.",
		str_weapon="They are wielding throwing knives.",
		str_weaponmaster_self="You are a rank {rank} master of the throwing knife.",
		str_weaponmaster="They are a rank {rank} master of the throwing knife.",
		str_trauma_self="You are covered in scarred-over lacerations and puncture wounds.",
		str_trauma="They are covered in scarred-over lacerations and puncture wounds.",
		str_kill="A blade flashes through the air!! **THUNK.** {name_target} is a goner, but {name_player} slits their throat before fleeing the scene, just to be safe. {emote_skull}",
		str_damage="{name_target} is stuck by a knife in the {hitzone}!!",
		str_duel="**TING! TING!!** {name_player} and {name_target} take turns hitting one another's knives out of the air.",
		fn_effect=wef_knives
	),
	EwWeapon( # 10
		id_weapon="scythe",
		alias=[
			"sickle"
		],
		str_crit="**Critical hit!!** {name_target} is carved by the wicked curved blade!",
		str_miss="**MISS!!** {name_player}'s swings wide of the target!",
		str_equip="You equip the scythe.",
		str_weapon_self="You are wielding a scythe.",
		str_weapon="They are wielding a scythe.",
		str_weaponmaster_self="You are a rank {rank} master of the scythe.",
		str_weaponmaster="They are a rank {rank} master of the scythe.",
		str_trauma_self="You are wrapped tightly in bandages that hold your two halves together.",
		str_trauma="They are wrapped tightly in bandages that hold their two halves together.",
		str_kill="**SLASHH!!** {name_player}'s scythe cleaves the air, and {name_target} staggers. A moment later, {name_target}'s torso topples off their waist. {emote_skull}",
		str_damage="{name_target} is cleaved through the {hitzone}!!",
		str_duel="**WHOOSH, WHOOSH** {name_player} and {name_target} swing their blades in wide arcs, dodging one another's deadly slashes.",
		fn_effect=wef_scythe
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
		name="sunny",
		sunrise="The smog is beginning to clear in the sickly morning sunlight.",
		day="The sun is blazing on the cracked streets, making the air shimmer.",
		sunset="The sky is darkening, the low clouds an iridescent orange.",
		night="The moon looms yellow as factories belch smoke all through the night."
	),
	EwWeather(
		name="rainy",
		sunrise="Rain gently beats against the pavement as the sky starts to lighten.",
		day="Rain pours down, collecting in oily rivers that run down sewer drains.",
		sunset="Distant thunder rumbles as it rains, the sky now growing dark.",
		night="Silverish clouds hide the moon, and the night is black in the heavy rain."
	),
	EwWeather(
		name="windy",
		sunrise="Wind whips through the city streets as the sun crests over the horizon.",
		day="Paper and debris are whipped through the city streets by the winds, buffetting pedestrians.",
		sunset="The few trees in the city bend and strain in the wind as the sun slowly sets.",
		night="The dark streets howl, battering apartment windows with vicious night winds."
	),
	EwWeather(
		name="lightning",
		sunrise="An ill-omened morning dawns as lighting streaks across the sky in the sunrise.",
		day="Flashes of bright lightning and peals of thunder periodically startle the citizens out of their usual stupor.",
		sunset="Bluish white arcs of electricity tear through the deep red dusky sky.",
		night="The dark night periodically lit with bright whitish-green bolts that flash off the metal and glass of the skyscrapers."
	),
	EwWeather(
		name="cloudy",
		sunrise="The dim morning light spreads timidly across the thickly clouded sky.",
		day="The air hangs thick, and the pavement is damp with mist from the clouds overhead.",
		sunset="The dusky light blares angry red on a sky choked with clouds and smog.",
		night="Everything is dark and still but the roiling clouds, reflecting the city's eerie light."
	)
]

# A map of name to EwWeather objects.
weather_map = {}
for weather in weather_list:
	weather_map[weather.name] = weather

# All food items in the game.
food_list = [
	EwFood(
		id_food="slimentonic",
		alias=[
			"tonic",
		],
		recover_stamina=250,
		price=500,
		str_name='slime n\' tonic',
		vendor='bar',
		str_eat="You chug a refreshing Slime n' Tonic. Delicious!!!"
	),
	EwFood(
		id_food="pizza",
		alias=[
			"pizzaslice",
		],
		recover_stamina=40,
		price=70,
		str_name='slice of pizza',
		vendor='Pizza Hut',
		str_eat="You grab a hot slice of that cheesy pie! Radical!!"
	),
	EwFood(
		id_food="pepperoni",
		alias=[
			"peperoni",
		],
		recover_stamina=60,
		price=110,
		str_name='slice of pepperoni pizza',
		vendor='Pizza Hut',
		str_eat="You chomp into the spicy sausage slice, bro! Cowabunga!!"
	),
	EwFood(
		id_food="meatlovers",
		alias=[
			"meatpizza",
		],
		recover_stamina=70,
		price=160,
		str_name='slice of Meat Lover\'s pizza',
		vendor='Pizza Hut',
		str_eat="You scarf down a meaty slice! You're sickened and nauseated by the sheer volume of animal fat you're ingesting! Tubular!!"
	),
	EwFood(
		id_food="wings",
		alias=[
			"buffalowings",
		],
		recover_stamina=90,
		price=175,
		str_name='buffalo wings',
		vendor='Pizza Hut',
		str_eat="Aw yeah! Your mouth burns with passion!! Your lips are in agony!! You've never felt so alive!!!"
	),
	EwFood(
		id_food="taco",
		alias=[
			"softtaco",
		],
		recover_stamina=30,
		price=50,
		str_name='soft taco',
		vendor='Taco Bell',
		str_eat="It's a taco. Pretty good, you guess. But it's missing something... a blast of flavor perhaps?"
	),
	EwFood(
		id_food="nachocheesetaco",
		alias=[
			"nachocheese",
			"nachotaco"
		],
		recover_stamina=40,
		price=70,
		str_name='Nacho Cheese taco',
		vendor='Taco Bell',
		str_eat="You slam your filthy mouth into a cheesy blast of nacho flavor!! *YEEAAAHHHH!!!*"
	),
	EwFood(
		id_food="coolranchtaco",
		alias=[
			"ranchtaco",
		],
		recover_stamina=40,
		price=70,
		str_name='Cool Ranch taco',
		vendor='Taco Bell',
		str_eat="You crash your teeth into an explosion of cool ranch taco flavor!! *YEEAAAHHHH!!!*"
	),
	EwFood(
		id_food="quesarito",
		alias=[
			"gordita",
		],
		recover_stamina=60,
		price=100,
		str_name='chicken quesarito',
		vendor='Taco Bell',
		str_eat="It's a burrito, or something. It's got cheese in it. Whatever. You eat it and embrace nothingness."
	),
	EwFood(
		id_food="steakvolcanoquesomachorito",
		alias=[
			"machorito",
			"quesomachorito"
		],
		recover_stamina=140,
		price=250,
		str_name='SteakVolcanoQuesoMachoRito',
		vendor='Taco Bell',
		str_eat="It's a big fucking mess of meat, vegetables, tortilla, cheese, and whatever else happened to be around. You gobble it down greedily!!"
	),
	EwFood(
		id_food="coleslaw",
		alias=[
			"slaw",
		],
		recover_stamina=20,
		price=55,
		str_name='tub of cole slaw',
		vendor='KFC',
		str_eat="It's a cup of some gross white cabbage swimming in watery mayo. Why the fuck would you order this?"
	),
	EwFood(
		id_food="biscuitngravy",
		alias=[
			"biscuit",
			"gravy"
		],
		recover_stamina=30,
		price=55,
		str_name='biscuit with a side of gravy',
		vendor='KFC',
		str_eat="You get a biscuit and a small bucket of brown gravy. You dip the biscuit, scarf it down, then chug the gravy. *burp.*"
	),
	EwFood(
		id_food="chickenbucket",
		alias=[
			"bucket",
			"chicken",
		],
		recover_stamina=120,
		price=220,
		str_name='8-piece fried chicken bucket',
		vendor='KFC',
		str_eat="You feast on hot, crispy, dripping white meat. Your fingers and tongue are scalded and you don't give a shit."
	),
	EwFood(
		id_food="famousbowl",
		alias=[
			"gordita",
		],
		recover_stamina=70,
		price=130,
		str_name='Famous Mashed Potato Bowl',
		vendor='KFC',
		str_eat="You scarf down a shitty plastic bowl full of jumbled-up bullshit. It really hits the spot!"
	),
	EwFood(
		id_food="barbecuesauce",
		alias=[
			"bbqsauce",
			"sauce",
			"saucepacket",
		],
		recover_stamina=5,
		price=10,
		str_name='packet of BBQ Sauce',
		vendor='KFC',
		str_eat="You disgard what's left of your dignity and purchace a packet of barbeque sauce to slurp down."
	),
	EwFood(
		id_food="mtndew",
		alias=[
			"dew",
			"mountaindew",
			"greendew"
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with vivid green swill and gulp it down."
	),
	EwFood(
		id_food="bajablast",
		alias=[
			"bluedew",
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew Baja Blast',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with light bluish swill and gulp it down."
	),
	EwFood(
		id_food="codered",
		alias=[
			"reddew",
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew Code Red',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with red swill and gulp it down."
	),
	EwFood(
		id_food="pitchblack",
		alias=[
			"blackdew",
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew Pitch Black',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with dark purple swill and gulp it down."
	),
	EwFood(
		id_food="whiteout",
		alias=[
			"whitedew",
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew White-Out',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with pale cloudy swill and gulp it down."
	),
	EwFood(
		id_food="livewire",
		alias=[
			"orangedew",
		],
		recover_stamina=20,
		price=35,
		str_name='Mtn Dew Livewire',
		vendor='Mtn Dew Fountain',
		str_eat="You fill your jumbo fountain drink vessel with orange swill and gulp it down."
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
