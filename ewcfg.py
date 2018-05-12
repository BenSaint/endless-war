from ewwep import EwWeapon

# Global configuration options.
version = "v1.18"

# Update intervals
update_hookstillactive = 60 * 60 * 3
update_twitch = 60
update_pvp = 60
update_market = 900

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
cmd_drink = cmd_prefix + 'drink'
cmd_slimepachinko = cmd_prefix + 'slimepachinko'
cmd_negaslime = cmd_prefix + 'negaslime'
cmd_equip = cmd_prefix + 'equip'
cmd_data = cmd_prefix + 'data'

# Slime costs/values
slimes_tokill = 20
slimes_permine = 20
slimes_perdrink = 500
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 420
slimes_perspar = 2500
slimes_hauntratio = 20
slimes_hauntmax = 1500
slimes_perslot = 100
slimes_perpachinko = 500

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

# Database columns for markets
col_rate_market = 'rate_market'
col_rate_exchange = 'rate_exchange'
col_slimes_casino = 'slimes_casino'
col_boombust = 'boombust'
col_time_lasttick = 'time_lasttick'
col_slimes_revivefee = 'slimes_revivefee'

# Database columns for stats
col_total_slime = 'total_slime'
col_total_slimecredit = 'total_slimecredit'
col_total_players = 'total_players'
col_total_players_pvp = 'total_players_pvp'

# Places you might get !shot
hitzone_list = [
	"wrist",
	"leg"
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

# All weapons in the game.
weapon_list = [
	EwWeapon( # 1
		id_weapon="gun",
		alias=[
			"pistol",
			"pistols",
			"dualpistols"
		],
		str_equip="You equip the dual pistols.",
		str_weapon_self="You are wielding dual pistols.",
		str_weapon="They are wielding dual pistols.",
		str_trauma_self="You have scarring on both templs, which occasionally bleeds.",
		str_trauma="They have scarring on both temples, which occasionally bleeds.",
		str_kill="{name_player} puts their gun to {name_target}'s head. **BANG**. Execution-style. Blood pools across the hot asphalt. {emote_skull}",
		str_damage="{name_target} takes a bullet to the {hitzone}!!",
		str_duel="**BANG BANG.** {name_player} and {name_target} practice their quick-draw, bullets whizzing past one another's heads."
	),
	EwWeapon( # 2
		id_weapon="rifle",
		alias=[
			"assaultrifle",
			"machinegun"
		],
		str_equip="You equip the assault rifle.",
		str_weapon_self="You are wielding an assult rifle.",
		str_weapon="They are wielding an assault rifle.",
		str_trauma_self="Your torso is riddled with scarred-over bulletholes.",
		str_trauma="Their torso is riddled with scarred-over bulletholes.",
		str_kill="**RAT-TAT-TAT-TAT-TAT!!** {name_player} rains a hail of bullets directly into {name_target}!! They're officially toast! {emote_skull}",
		str_damage="Bullets rake over {name_target}'s {hitzone}!!",
		str_duel="**RAT-TAT-TAT-TAT-TAT!!** {name_player} and {name_target} practice shooting at distant targets with quick, controlled bursts."
	),
	EwWeapon( # 3
		id_weapon="nun-chucks",
		alias=[
			"nanchacku",
			"numchucks",
			"nunchucks"
		],
		str_equip="You equip the nun-chucks.",
		str_weapon_self="You are wielding nun-chucks.",
		str_weapon="They are wielding nun-chucks.",
		str_trauma_self="You are covered in deep bruises. You hate martial arts of all kinds.",
		str_trauma="They are covered in deep bruises. They hate martial arts of all kinds.",
		str_kill="**HIIII-YAA!!** With expert timing, {name_player} brutally batters {name_target} to death, then strikes a sweet kung-fu pose. {emote_skull}",
		str_damage="{name_target} takes a nun-chuck directly in the {hitzone}!!",
		str_duel="**HII-YA! HOOOAAAAAHHHH!!** {name_player} and {name_target} twirl wildly around one another, lashing out with kung-fu precision."
	),
	EwWeapon( # 4
		id_weapon="katana",
		alias=[
			"sword",
			"ninjasword",
			"samuraisword",
			"blade"
		],
		str_equip="You equip the katana.",
		str_weapon_self="You are wielding a katana.",
		str_weapon="They are wielding a katana.",
		str_trauma_self="A single clean scar runs across the entire length of your body.",
		str_trauma="A single clean scar runs across the entire length of their body.",
		str_kill="Faster than the eye can follow, {name_player}'s blade glints in the greenish light. {name_target} falls over, now in two pieces. {emote_skull}",
		str_damage="{name_target} is slashed across the {hitzone}!!",
		str_duel="**CRACK!! THWACK!! CRACK!!** {name_player} and {name_target} duel with bamboo swords, viciously striking at head, wrist and belly."
	),
	EwWeapon( # 5
		id_weapon="bat",
		alias=[
			"club",
			"batwithnails",
			"nailbat",
		],
		str_equip="You equip the bat with nails in it.",
		str_weapon_self="You are wielding a bat full of nails.",
		str_weapon="They are wielding a bat full of nails.",
		str_trauma_self="Your head appears to be slightly concave on one side.",
		str_trauma="Their head appears to be slightly concave on one side.",
		str_kill="{name_player} pulls back for a brutal swing! **CRUNCCHHH.** {name_target}'s brains splatter over the sidewalk. {emote_skull}",
		str_damage="{name_target} is struck with a hard blow to the {hitzone}!!",
		str_duel="**SMASHH! CRAASH!!** {name_player} and {name_target} run through the neighborhood, breaking windshields, crushing street signs, and generally having a hell of a time."
	),
	EwWeapon( # 6
		id_weapon="garrote",
		alias=[
			"wire",
			"garrottewire"
		],
		str_equip="You equip the garrotte wire.",
		str_weapon_self="You are wielding a garrotte wire.",
		str_weapon="They are wielding a garrotte wire.",
		str_trauma_self="There is noticeable bruising and scarring around your neck.",
		str_trauma="There is noticeable bruising and scarring around their neck.",
		str_kill="{name_player} quietly moves behind {name_target} and... **!!!** After a brief struggle, only a cold body remains. {emote_skull}",
		str_damage="{name_target} closely escapes strangulation!!",
		str_duel="{name_player} and {name_target} compare their dexterity by playing Cat's Cradle with deadly wire."
	),
	EwWeapon( # 7
		id_weapon="brassknuckles",
		alias=[
			"knuckles",
			"knuckledusters"
		],
		str_equip="You equip the brass knuckles.",
		str_weapon_self="You are wielding brass knuckles.",
		str_weapon="They are wielding brass knuckles.",
		str_trauma_self="You've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_trauma="They've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_kill="{name_player} slugs {name_target} right between the eyes! *POW! THWACK!!* **CRUNCH.** Shit. May have gotten carried away there. Oh, well. {emote_skull}",
		str_damage="{name_target} is socked in the {hitzone}!!",
		str_duel="**POW! BIFF!!** {name_player} and {name_target} take turns punching each other in the abs. It hurts so good."
	),
	EwWeapon( # 8
		id_weapon="molotov",
		alias=[
			"firebomb",
			"molotovcocktail",
			"bomb",
			"bombs"
		],
		str_equip="You equip the molotov cocktail.",
		str_weapon_self="You are wielding molotov cocktails.",
		str_weapon="They are wielding molotov cocktails.",
		str_trauma_self="You're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_trauma="They're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_kill="**SMASH!** {name_target}'s front window shatters and suddenly flames are everywhere!! The next morning, police report that {name_player} is suspected of arson. {emote_skull}",
		str_damage="{name_target} dodges a bottle, but is singed on the {hitzone} by the blast!!",
		str_duel="{name_player} and {name_target} compare notes on frontier chemistry, seeking the optimal combination of combustibility and fuel efficiency."
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
		str_equip="You equip the throwing knives.",
		str_weapon_self="You are wielding throwing knives.",
		str_weapon="They are wielding throwing knives.",
		str_trauma_self="You are covered in scarred-over lacerations and puncture wounds.",
		str_trauma="They are covered in scarred-over lacerations and puncture wounds.",
		str_kill="A blade flashes through the air!! **THUNK.** {name_target} is a goner, but {name_player} slits their throat before fleeing the scene, just to be safe. {emote_skull}",
		str_damage="{name_target} is stuck by a knife in the {hitzone}!!",
		str_duel="**TING! TING!!** {name_player} and {name_target} take turns hitting one another's knives out of the air."
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
