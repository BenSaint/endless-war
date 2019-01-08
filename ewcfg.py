import random

from ewcosmeticitem import EwCosmeticItem
from ewwep import EwWeapon
from ewweather import EwWeather
from ewfood import EwFood
from ewitem import EwItemDef
from ewmap import EwPoi
from ewslimeoid import EwBody, EwHead, EwMobility, EwOffense, EwDefense, EwSpecial, EwBrain

# Global configuration options.
version = "v2.15a"
dir_msgqueue = 'msgqueue'

# Update intervals
update_hookstillactive = 60 * 60 * 3
update_twitch = 60
update_pvp = 60
update_market = 900 #15 min

# Market delta
max_iw_swing = 30

# Life states. How the player is living (or deading) in the database
life_state_corpse = 0
life_state_juvenile = 1
life_state_enlisted = 2
life_state_grandfoe = 8
life_state_kingpin = 10

# slimeoid life states
slimeoid_state_none = 0
slimeoid_state_forming = 1
slimeoid_state_active = 2
slimeoid_state_stored = 3

# ID tags for points of interest that are needed in code.
poi_id_thesewers = "thesewers"
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
poi_id_endlesswar = "endlesswar"
poi_id_slimecorphq = "slimecorphq"
poi_id_cv_mines = "cratersvillemines"
poi_id_tt_mines = "toxingtonmines"
poi_id_diner = "smokerscough"
poi_id_seafood = "redmobster"
poi_id_jr_farms = "juviesrowfarms"
poi_id_og_farms = "oozegardensfarms"
poi_id_ab_farms = "arsonbrookfarms"

# district pois
poi_id_downtown = "downtown"
poi_id_smogsburg = "smogsburg"
poi_id_copkilltown = "copkilltown"
poi_id_krakbay = "krakbay"
poi_id_poudrinalley = "poudrinalley"
poi_id_rowdyroughhouse = "rowdyroughhouse"
poi_id_greenlightdistrict = "greenlightdistrict"
poi_id_oldnewyonkers = "oldnewyonkers"
poi_id_littlechernobyl = "littlechernobyl"
poi_id_arsonbrook = "arsonbrook"
poi_id_astatineheights = "astatineheights"
poi_id_gatlingsdale = "gatlingsdale"
poi_id_vandalpark = "vandalpark"
poi_id_glocksbury = "glocksbury"
poi_id_northsleezeborough = "northsleezeborough"
poi_id_southsleezeborough = "southsleezeborough"
poi_id_oozegardens = "oozegardens"
poi_id_cratersville = "cratersville"
poi_id_wreckington = "wreckington"
poi_id_juviesrow = "juviesrow"
poi_id_slimesend = "slimesend"
poi_id_vagrantscorner = "vagrantscorner"
poi_id_assaultflatsbeachresort = "assaultflatsbeachresort"
poi_id_newnewyonkers = "newnewyonkers"
poi_id_brawlden = "brawlden"
poi_id_toxington = "toxington"
poi_id_charcoalpark = "charcoalpark"
poi_id_poloniumhill = "poloniumhill"
poi_id_westglocksbury = "westglocksbury"

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
role_grandfoe = "grandfoe"

# Faction names
faction_killers = "killers"
faction_rowdys = "rowdys"
factions = [faction_killers, faction_rowdys]

# Channel names
channel_mines = "the-mines"
channel_downtown = "downtown"
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
channel_slimecorphq = "slimecorp-hq"
channel_leaderboard = "leaderboard"
channel_cv_mines = "cratersville-mines"
channel_tt_mines = "toxington-mines"
channel_diner = "smokers-cough"
channel_seafood = "red-mobster"
channel_jr_farms = "juvies-row-farms"
channel_og_farms = "ooze-gardens-farms"
channel_ab_farms = "arsonbrook-farms"
channel_rowdyroughhouse = "rowdy-roughhouse"
channel_copkilltown = "cop-killtown"

hideout_channels = [channel_rowdyroughhouse, channel_copkilltown]
hideout_by_faction = {
	faction_rowdys: channel_rowdyroughhouse,
	faction_killers: channel_copkilltown
}

# Commands
cmd_prefix = '!'
cmd_enlist = cmd_prefix + 'enlist'
cmd_revive = cmd_prefix + 'revive'
cmd_kill = cmd_prefix + 'kill'
cmd_shoot = cmd_prefix + 'shoot'
cmd_attack = cmd_prefix + 'attack'
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
cmd_salute = cmd_prefix + 'salute'
cmd_unsalute = cmd_prefix + 'unsalute'
cmd_spar = cmd_prefix + 'spar'
cmd_suicide = cmd_prefix + 'suicide'
cmd_haunt = cmd_prefix + 'haunt'
cmd_slimepachinko = cmd_prefix + 'slimepachinko'
cmd_slimeslots = cmd_prefix + 'slimeslots'
cmd_slimecraps = cmd_prefix + 'slimecraps'
cmd_slimeroulette = cmd_prefix + 'slimeroulette'
cmd_slimebaccarat = cmd_prefix + 'slimebaccarat'
cmd_deadmega = cmd_prefix + 'deadmega'
cmd_donate = cmd_prefix + 'donate'
cmd_slimecredit = cmd_prefix + 'slimecoin'
cmd_slimecredit_alt1 = cmd_prefix + 'slimecredit'
cmd_withdraw = cmd_prefix + 'withdraw'
cmd_exchangerate = cmd_prefix + 'exchangerate'
cmd_exchangerate_alt1 = cmd_prefix + 'exchange'
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
cmd_annoint_alt1 = cmd_prefix + 'anoint'
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
cmd_halt = cmd_prefix + 'halt'
cmd_halt_alt1 = cmd_prefix + 'stop'
cmd_inspect = cmd_prefix + 'inspect'
cmd_look = cmd_prefix + 'look'
cmd_map = cmd_prefix + 'map'
cmd_wiki = cmd_prefix + 'wiki'
cmd_booru = cmd_prefix + 'booru'
cmd_pardon = cmd_prefix + 'pardon'
cmd_writhe = cmd_prefix + 'writhe'
cmd_use = cmd_prefix + 'use'
cmd_news = cmd_prefix + 'news'
cmd_buy = cmd_prefix + 'buy'
cmd_thrash = cmd_prefix + 'thrash'
cmd_dab = cmd_prefix + 'dab'
cmd_russian = cmd_prefix + 'russianroulette'
cmd_accept = cmd_prefix + 'accept'
cmd_refuse = cmd_prefix + 'refuse'
cmd_reap = cmd_prefix + 'reap'
cmd_sow = cmd_prefix + 'sow'
cmd_smelt = cmd_prefix + 'smelt'
cmd_adorn = cmd_prefix + 'adorn'
cmd_create = cmd_prefix + 'create'
cmd_give = cmd_prefix + 'give'

#slimeoid commands
cmd_incubateslimeoid = cmd_prefix + 'incubateslimeoid'
cmd_growbody = cmd_prefix + 'growbody'
cmd_growhead = cmd_prefix + 'growhead'
cmd_growlegs = cmd_prefix + 'growlegs'
cmd_growweapon = cmd_prefix + 'growweapon'
cmd_growarmor = cmd_prefix + 'growarmor'
cmd_growspecial = cmd_prefix + 'growspecial'
cmd_growbrain = cmd_prefix + 'growbrain'
cmd_nameslimeoid = cmd_prefix + 'nameslimeoid'
cmd_raisemoxie = cmd_prefix + 'raisemoxie'
cmd_lowermoxie = cmd_prefix + 'lowermoxie'
cmd_raisegrit = cmd_prefix + 'raisegrit'
cmd_lowergrit = cmd_prefix + 'lowergrit'
cmd_raisechutzpah = cmd_prefix + 'raisechutzpah'
cmd_lowerchutzpah = cmd_prefix + 'lowerchutzpah'
cmd_spawnslimeoid = cmd_prefix + 'spawnslimeoid'
cmd_dissolveslimeoid = cmd_prefix + 'dissolveslimeoid'
cmd_slimeoid = cmd_prefix + 'slimeoid'
cmd_challenge = cmd_prefix + 'challenge'
cmd_instructions = cmd_prefix + 'instructions'
cmd_playfetch = cmd_prefix + 'playfetch'
cmd_petslimeoid = cmd_prefix + 'petslimeoid'
cmd_walkslimeoid = cmd_prefix + 'walkslimeoid'
cmd_observeslimeoid = cmd_prefix + 'observeslimeoid'
cmd_slimeoidbattle = cmd_prefix + 'slimeoidbattle'

# Slime costs/values
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 0
slimes_perspar_base = 0
slimes_hauntratio = 40
slimes_hauntmax = 20000
slimes_perslot = 100
slimes_perpachinko = 500
slimecoin_exchangerate = 100

# hunger
min_stamina = 100
hunger_pershot = 10
hunger_perspar = 30
hunger_permine = 1
hunger_pertick = 3

#inebriation
inebriation_max = 20
inebriation_pertick = 2

# max item amounts
max_food_in_inv_mod = 8  # modifier for how much food you can carry. the player's slime level is divided by this number to calculate the number of carriable food items
max_adorn_mod = 4

# price multipliers
togo_price_increase = 2

# standard food expiration in seconds
std_food_expir = 12 * 3600  # 12 hours

# property classes
property_class_s = "s"
property_class_a = "a"
property_class_b = "b"
property_class_c = "c"

# district capturing
capture_tick_length = 10  # in seconds; also affects how much progress is made per tick so that 1 second = 1 capture point
max_capture_points_s = 7200  # 120 min
max_capture_points_a = 3600  # 60 min
max_capture_points_b = 1800  # 30 min
max_capture_points_c = 900   # 15 min

# district capture rates assigned to property classes
max_capture_points = {
	property_class_s: max_capture_points_s,
	property_class_a: max_capture_points_a,
	property_class_b: max_capture_points_b,
	property_class_c: max_capture_points_c
}

# capture messages
capture_milestone = 5  # after how many percent of progress the players are notified of the progress


# district de-capturing
decapture_speed_multiplier = 2  # how much faster de-capturing is than capturing

# district control decay
decay_modifier = 2  # more means slower

# time values
seconds_per_ingame_day = 21600
ticks_per_day = seconds_per_ingame_day / update_market  # how often the kingpins receive slime per in-game day

# kingpin district control slime yields (per tick, i.e. in-game-hourly)
slime_yield_class_s = int(60000 / ticks_per_day)  # dividing the daily amount by the amount of method calls per day
slime_yield_class_a = int(40000 / ticks_per_day)
slime_yield_class_b = int(30000 / ticks_per_day)
slime_yield_class_c = int(20000 / ticks_per_day)

# district control slime yields assigned to property classes
district_control_slime_yields = {
	property_class_s: slime_yield_class_s,
	property_class_a: slime_yield_class_a,
	property_class_b: slime_yield_class_b,
	property_class_c: slime_yield_class_c
}

# Slime decay rate
slime_half_life = 60 * 60 * 24 * 14 #two weeks

# Poudrin rarity (for enlisted players)
poudrin_rarity = 2400

# Lifetimes
invuln_onrevive = 0

# farming
crops_time_to_grow = 720  # in minutes; 720 minutes are 12 hours
reap_gain = 120000

# Cooldowns
cd_kill = 5
cd_spar = 600
cd_haunt = 600
cd_invest = 1200
cd_boombust = 22
#For possible time limit on russian roulette
cd_rr = 600
#slimeoid downtime after a defeat
cd_slimeoiddefeated = 900

# PvP timer pushouts
time_pvp_kill = 600
time_pvp_mine = 180
time_pvp_haunt = 600
time_pvp_invest_withdraw = 180
time_pvp = 1800

# time to get kicked out of subzone
time_kickout = 3 * 60 * 60  # 3 hours

# Emotes
emote_tacobell = "<:tacobell:431273890195570699>"
emote_pizzahut = "<:pizzahut:431273890355085323>"
emote_kfc = "<:kfc:431273890216673281>"
emote_moon = "<:moon:431418525303963649>"
emote_111 = "<:111:431547758181220377>"

emote_copkiller = "<:copkiller:431275071945048075>"
emote_rowdyfucker = "<:rowdyfucker:431275088076079105>"
emote_ck = "<:ck:504173691488305152>"
emote_rf = "<:rf:504174176656162816>"

emote_theeye = "<:theeye:431429098909466634>"
emote_slime1 = "<:slime1:431564830541873182>"
emote_slime2 = "<:slime2:431570132901560320>"
emote_slime3 = "<:slime3:431659469844381717>"
emote_slime4 = "<:slime4:431570132901560320>"
emote_slime5 = "<:slime5:431659469844381717>"
emote_slimeskull = "<:slimeskull:431670526621122562>"
emote_slimeheart = "<:slimeheart:431673472687669248>"
emote_dice1 = "<:dice1:436942524385329162>"
emote_dice2 = "<:dice2:436942524389654538>"
emote_dice3 = "<:dice3:436942524041527298>"
emote_dice4 = "<:dice4:436942524406300683>"
emote_dice5 = "<:dice5:436942524444049408>"
emote_dice6 = "<:dice6:436942524469346334>"
emote_negaslime = "<:negaslime:453826200616566786>"
emote_bustin = "<:bustin:455194248741126144>"
emote_ghost = "<:lordofghosts:434002083256205314>"
emote_slimefull = "<:slimefull:496397819154923553>"
emote_purple = "<:purple:496397848343216138>"
emote_pink = "<:pink:496397871180939294>"
emote_slimecoin = "<:slimecoin:440576133214240769>"
emote_slimegun = "<:slimegun:436500203743477760>"
emote_slimecorp = "<:slimecorp:522416869127225344>"
emote_nlacakanm = "<:nlacakanm:499615025544298517>"

# Emotes for the negaslime writhe animation
emote_vt = "<:vt:492067858160025600>"
emote_ve = "<:ve:492067844930928641>"
emote_va = "<:va:492067850878451724>"
emote_v_ = "<:v_:492067837565861889>"
emote_s_ = "<:s_:492067830624157708>"
emote_ht = "<:ht:492067823150039063>"
emote_hs = "<:hs:492067783396294658>"
emote_he = "<:he:492067814933266443>"
emote_h_ = "<:h_:492067806465228811>"
emote_blank = "<:blank:492087853702971403>"

# Common strings.
str_casino_closed = "The Slime Casino only operates at night."
str_exchange_closed = "The Exchange has closed for the night."
str_exchange_specify = "Specify how much {currency} you will {action}."
str_exchange_channelreq = "You must go to the #" + channel_stockexchange + " to {action} your {currency}."
str_exchange_busy = "You can't {action} right now. Your slimebroker is busy."
str_food_channelreq = "There's no food here. Go to the Food Court, the Smoker's Cough, the Red Mobster, or the Speakeasy to {action}."
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
col_busted = 'busted'
col_rrchallenger = 'rr_challenger_id'
col_time_lastsow = 'time_lastsow'
col_farm = 'farm'
col_time_last_action = 'time_last_action'

#Database columns for slimeoids
col_id_slimeoid = 'id_slimeoid'
col_body = 'body'
col_head = 'head'
col_legs = 'legs'
col_armor = 'armor'
col_weapon = 'weapon'
col_special = 'special'
col_ai = 'ai'
col_type = 'type'
col_name = 'name'
col_atk = 'atk'
col_defense = 'defense'
col_intel = 'intel'
col_level = 'level'
col_time_defeated = 'time_defeated'

# Database columns for user statistics
col_stat_metric = 'stat_metric'
col_stat_value = 'stat_value'

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
col_day = 'day'
col_decayed_slimes = 'decayed_slimes'

# Database columns for stats
col_total_slime = 'total_slime'
col_total_slimecredit = 'total_slimecredit'
col_total_players = 'total_players'
col_total_players_pvp = 'total_players_pvp'
col_timestamp = 'timestamp'

# Database columns for districts
col_district = 'district'
col_controlling_faction = 'controlling_faction'
col_capturing_faction = 'capturing_faction'
col_capture_points = 'capture_points'

# Item type names
it_medal = "medal"
it_slimepoudrin = "slimepoudrin"
it_questitem = "questitem"
it_food = "food"
it_weapon = "weapon"

it_cosmetic = 'cosmetic'

# Cosmetic item rarities
rarity_plebeian = "Plebeian"
rarity_patrician = "Patrician"
rarity_princeps = "Princeps"

# Leaderboard score categories
leaderboard_slimes = "SLIMIEST"
leaderboard_slimecredit = "SLIMECOIN BARONS"
leaderboard_ghosts = "ANTI-SLIMIEST"
leaderboard_podrins = "PODRIN LORDS"
leaderboard_bounty = "MOST WANTED"
leaderboard_kingpins = "KINGPINS' COFFERS"
leaderboard_districts = "DISTRICTS CONTROLLED"

# leaderboard entry types
entry_type_player = "player"
entry_type_districts = "districts"

# district control channel topic text
control_topic_killers = "Currently controlled by the killers."
control_topic_rowdys = "Currently controlled by the rowdys."
control_topic_neutral = "Currently controlled by no one."

control_topics = {
	faction_killers: control_topic_killers,
	faction_rowdys: control_topic_rowdys,
	"": control_topic_neutral  # no faction
}

# district control actors
actor_decay = "decay"

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

# User statistics we track
stat_max_slimes = 'max_slimes'
stat_lifetime_slimes = 'lifetime_slimes'
stat_lifetime_slimeloss = 'lifetime_slime_loss'
stat_lifetime_slimesdecayed = 'lifetime_slimes_decayed'
stat_slimesmined = 'slimes_mined'
stat_max_slimesmined = 'max_slimes_mined'
stat_lifetime_slimesmined = 'lifetime_slimes_mined'
stat_slimesfromkills = 'slimes_from_kills'
stat_max_slimesfromkills = 'max_slimes_from_kills'
stat_lifetime_slimesfromkills = 'lifetime_slimes_from_kills'
stat_lifetime_slimeshaunted = 'lifetime_slimes_haunted'
stat_max_level = 'max_level'
stat_max_ghost_level = 'max_ghost_level'
stat_max_hitsurvived = 'max_hit_survived'
stat_max_hitdealt = 'max_hit_dealt'
stat_max_hauntinflicted = 'max_haunt_inflicted'
stat_kills = 'kills'
stat_max_kills = 'max_kills'
stat_biggest_kill = 'biggest_kill'
stat_lifetime_kills = 'lifetime_kills'
stat_lifetime_ganks = 'lifetime_ganks'
stat_lifetime_takedowns = 'lifetime_takedowns'
stat_max_wepskill = 'max_wep_skill'
stat_max_slimecredit = 'max_slime_coins'
stat_lifetime_slimecredit = 'lifetime_slime_coins'
stat_slimecredit_spent_on_revives = 'slimecoins_spent_on_revives'
stat_biggest_casino_win = 'biggest_casino_win'
stat_biggest_casino_loss = 'biggest_casino_loss'
stat_lifetime_casino_winnings = 'lifetime_casino_winnings'
stat_lifetime_casino_losses = 'lifetime_casino_losses'
stat_bounty_collected = 'bounty_collected'
stat_max_bounty = 'max_bounty'
stat_ghostbusts = 'ghostbusts'
stat_biggest_bust_level = 'biggest_bust_level'
stat_lifetime_ghostbusts = 'lifetime_ghostbusts'
stat_max_ghostbusts = 'max_ghostbusts'
stat_max_poudrins = 'max_poudrins'
stat_poudrins_looted = 'poudrins_looted'
stat_lifetime_poudrins = 'lifetime_poudrins'
stat_lifetime_damagedealt = 'lifetime_damage_dealt'
stat_lifetime_selfdamage = 'lifetime_self_damage'
stat_lifetime_deaths = 'lifetime_deaths'
stat_lifetime_pve_deaths = 'lifetime_pve_deaths'
#Track revolver trigger pulls survived?
stat_lifetime_spins_survived = 'lifetime_spins_survived'
stat_max_spins_survived = 'max_spins_survived'
stat_capture_points_contributed = 'capture_points_contributed'

# Categories of events that change your slime total, for statistics tracking
source_mining = 0
source_damage = 1
source_killing = 2
source_self_damage = 3
source_busting = 4
source_haunter = 5
source_haunted = 6
source_spending = 7
source_decay = 8
source_ghostification = 9

# Categories of events that change your slimecoin total, for statistics tracking
coinsource_spending = 0
coinsource_donation = 1
coinsource_bounty = 2
coinsource_revival = 3
coinsource_casino = 4
coinsource_transfer = 5

# Causes of death, for statistics tracking
cause_killing = 0
cause_mining = 1
cause_grandfoe = 2
cause_donation = 3
cause_busted = 4
cause_suicide = 5

# List of user statistics that reset to 0 on death
stats_clear_on_death = [
	stat_slimesmined,
	stat_slimesfromkills,
	stat_kills,
	stat_ghostbusts
]

# Seeds you might !Sow
seed_list = [
		"Pink Rowddish",
		"Sludgeberry",
		"Pulp Gourd",
		"Joybean",
		"Brightshade",
		"Dire Apple",
		"Purple Killiflower",
		"Razornut",
		"Poke-tubers",
		"Suganma Nuts",
		"Dankwheat",
		"Black Limes",
		"Phosphorpoppy",
		"Sour Potato",
		"Blood Cabbage"
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
	dmg = ctn.slimes_damage
	ctn.slimes_damage = 0

	for count in range(5):
		if random.randint(1, 3) == 1:
			ctn.strikes += 1
			ctn.slimes_damage += int(dmg / 2)

	if ctn.strikes == 5:
		ctn.crit = True
	elif ctn.strikes == 0:
		ctn.miss = True
		ctn.user_data.change_slimes(n = (-ctn.slimes_damage / 2), source = source_self_damage)

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
		ctn.user_data.change_slimes(n = -ctn.slimes_damage, source = source_self_damage)
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
	ctn.user_data.change_slimes(n = (-ctn.slimes_spent * 0.33), source = source_self_damage)
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
		str_killdescriptor = "gunned down",
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
		str_killdescriptor = "gunned down",
		str_damage = "Bullets rake over {name_target}'s {hitzone}!!",
		str_duel = "**RAT-TAT-TAT-TAT-TAT!!** {name_player} and {name_target} practice shooting at distant targets with quick, controlled bursts.",
		fn_effect = wef_rifle
	),
	EwWeapon( # 3
		id_weapon = "nun-chucks",
		alias = [
			"nanchacku",
			"nunchaku",
			"chucks",
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
		str_killdescriptor = "fatally bludgeoned",
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
		str_killdescriptor = "bisected",
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
		str_killdescriptor = "nail bat battered",
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
		str_killdescriptor = "garrote wired",
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
		str_killdescriptor = "pummeled to death",
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
		str_killdescriptor = "exploded",
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
		str_killdescriptor = "knifed",
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
		str_killdescriptor = "sliced in twain",
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
	)
]

# Food vendor names
vendor_bar = 'bar'
vendor_pizzahut = 'Pizza Hut'
vendor_tacobell = 'Taco Bell'
vendor_kfc = 'KFC'
vendor_mtndew = 'Mtn Dew Fountain'
vendor_vendingmachine = 'vending machine'
vendor_seafood = 'Red Mobster Seafood'
vendor_diner = "Smoker's Cough"

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
		price = 18,
		inebriation = 2,
		str_name = 'slime n\' tonic',
		vendors = [vendor_bar],
		str_eat = "You stir your slime n' tonic with a thin straw before chugging it lustily.",
		str_desc = "The drink that has saved more juveniles’ lives than any trip to the nurse’s office could."
	),
	EwFood(
		id_food = "slimacolada",
		alias = [
			"colada",
		],
		recover_hunger = 25,
		price = 22,
		inebriation = 2,
		str_name = 'slima colada',
		vendors = [vendor_bar],
		str_eat = "Slurping down this tropicalish drink gives you a brain freeze. You drink faster to numb the pain.",
		str_desc = "Perfect for if you like getting caught in acid rain, or if you enjoy gunning down grandmas in the dunes out of town."
	),
	EwFood(
		id_food = "slimekashot",
		alias = [
			"shot",
			"slimeka",
		],
		recover_hunger = 5,
		price = 10,
		inebriation = 2,
		str_name = 'shot of slimeka',
		vendors = [vendor_bar],
		str_eat = "Your throat burns as you toss back a mouthful of the glowing, hissing liquid. You might need a doctor.",
		str_desc = "Made with 100% unfiltered sludge from the city's harbor. Less internally damaging than a sawed-off shotgun blast to the colon, but not by much."
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
		price = 99,
		inebriation = 4,
		str_name = 'bottle of vintage cabernet slimeignon',
		vendors = [vendor_bar],
		str_eat = "Ahh, you have a keen eye. 19XX was an excellent year. You pop the cork and gingerly have a sniff. Then you gulp the whole bottle down in seconds, because fuck it.",
		str_desc = "A sophisticated drink for a sophisticated delinquent gangster with blood on his hands such as yourself."
	),
	EwFood(
		id_food = "slimynipple",
		alias = [
			"",
		],
		recover_hunger = 10,
		price = 16,
		inebriation = 2,
		str_name = 'slimy nipple',
		vendors = [vendor_bar],
		str_eat = "You drink the small glass of creamy, greenish layered fluids in one gulp.",
		str_desc = "Of the drinks with terrible names, this is the least amusing."
	),
	EwFood(
		id_food = "slimeonthebeach",
		alias = [
			"beach",
		],
		recover_hunger = 30,
		price = 24,
		inebriation = 2,
		str_name = 'slime on the beach',
		vendors = [vendor_bar],
		str_eat = "You look pretty stupid holding this fluorescent drink with a lil umbrella in it, but you don't care. Bottoms up!",
		str_desc = "When you told the bartender you wanted Slime on the Beach, about a dozen other guys at the speakeasy all collectively and hilariously added"
			" “Yeah, wouldn’t we all”, chuckled under their breath, and beat the shit out of you outside afterward."
	),
		EwFood(
		id_food = "goobalibre",
		alias = [
			"goo",
		],
		recover_hunger = 30,
		price = 22,
		inebriation = 2,
		str_name = 'goo-ba libre',
		vendors = [vendor_bar],
		str_eat = "The drink oozes tartly down your throat. It's pretty nasty, but you still like it.",
		str_desc = "You’re lucky you got this glass so easily. Last time you had tried to convince the bartender you were over 21 for half an hour before you finally cracked and just ordered a coke."
	),
		EwFood(
		id_food = "manhattanproject",
		alias = [
			"manhattan",
		],
		recover_hunger = 25,
		price = 20,
		inebriation = 3,
		str_name = 'manhattan project',
		vendors = [vendor_bar],
		str_eat = "Downing your drink, the alcohol hits your bloodstream with the force of an atomic bomb.",
		str_desc = "We got tired of waiting for the bombs to drop so we made our own."
	),
	EwFood(
		id_food = "slimymary",
		alias = [
			"mary",
		],
		recover_hunger = 25,
		price = 20,
		inebriation = 2,
		str_name = 'slimy mary',
		vendors = [vendor_bar],
		str_eat = "This drink smells pretty nasty even by NLACakaNM standards. But what are you gonna do, NOT drink it?",
		str_desc = "To get this drink you have to stand in the bathroom with the lights off and your back turned to the mirror. "
			"Say it’s name three times, turn around and open your eyes. Congratulations your wallet’s missing "
			"and I'm fucking your girlfriend."
	),
	EwFood(
		id_food = "slimestout",
		alias = [
			"stout",
			"beer",
		],
		recover_hunger = 30,
		price = 21,
		inebriation = 2,
		str_name = 'stein of dark slime stout',
		vendors = [vendor_bar],
		str_eat = "The bartender pours you a rich, dark-green slime stout from the tap, with a head so thick you could rest a SlimeCoin on it.",
		str_desc = "Fun fact; Munchy and Ben actually stole the Blarney stone and use it as a doorstop. We are wanted terrorists in Ireland."
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
		vendors = [vendor_bar],
		str_eat = "The bartender sighs as he hands you a glass of water. You drink it. You're not sure why you bothered, though.",
		str_desc = "It’s a room temperature glass of tap water. Abstaining from drinking calories has never tasted this adequate!"
	),
	EwFood(
		id_food = "pizza",
		alias = [
			"pizzaslice",
		],
		recover_hunger = 40,
		price = 12,
		inebriation = 0,
		str_name = 'slice of pizza',
		vendors = [vendor_pizzahut],
		str_eat = "You grab a hot slice of that cheesy pie! Radical!!",
		str_desc = "A supposedly hot slice of cheese pizza. Some of it’s pre-grated cheese hasn't fully melted yet, and it’s crust is hard and chewy. Reality is a cruel mistress."
	),
	EwFood(
		id_food = "pepperoni",
		alias = [
			"peperoni",
		],
		recover_hunger = 50,
		price = 13,
		inebriation = 0,
		str_name = 'slice of pepperoni pizza',
		vendors = [vendor_pizzahut],
		str_eat = "You chomp into the spicy sausage slice, bro! Cowabunga!!",
		str_desc = "An apparently appetizing slice of pepperoni pizza. It’s crust is limp and soggy from the excess"
			" grease it's slathered in, which is about the only thing you can taste on it as well."
	),
	EwFood(
		id_food = "meatlovers",
		alias = [
			"meatpizza",
		],
		recover_hunger = 100,
		price = 17,
		inebriation = 0,
		str_name = 'slice of Meat Lover\'s pizza',
		vendors = [vendor_pizzahut],
		str_eat = "You scarf down a meaty slice! You're sickened and nauseated by the sheer volume of animal fat you're ingesting! Tubular!!",
		str_desc = "A thoroughly revolting slice Meat Lover's® pizza. You like meat, but you aren't sure if you're ready to love again."
	),
	EwFood(
		id_food = "wings",
		alias = [
			"buffalowings",
		],
		recover_hunger = 125,
		price = 19,
		inebriation = 0,
		str_name = 'buffalo wings',
		vendors = [vendor_pizzahut],
		str_eat = "Aw yeah! Your mouth burns with passion!! Your lips are in agony!! You've never felt so alive!!!",
		str_desc = "Alright, some quick backstory: https://youtu.be/lqAh0jJTqvo"
	),
	EwFood(
		id_food = "taco",
		alias = [
			"softtaco",
		],
		recover_hunger = 30,
		price = 11,
		inebriation = 0,
		str_name = 'soft taco',
		vendors = [vendor_tacobell],
		str_eat = "It's a taco. Pretty good, you guess. But it's missing something... a blast of flavor perhaps?",
		str_desc = "A limp, pitiful soft shell taco. Mirroring its own weak exterior, it is the perfect food for weak-willed men"
			" without the strong moral character needed to tame the wild, wicked blast of flavor in more iconic Taco Bell tacos."
	),
	EwFood(
		id_food = "nachocheesetaco",
		alias = [
			"nachocheese",
			"nachotaco"
		],
		recover_hunger = 30,
		price = 13,
		inebriation = 0,
		str_name = 'Nacho Cheese taco',
		vendors = [vendor_tacobell],
		str_eat = "You slam your filthy mouth into a cheesy blast of nacho flavor!! *YEEAAAHHHH!!!*",
		str_desc = "This flavor…!! It’s an explosion of artificial cheese flavors and shrapnel sized bits of soggy shell that vaguely reminds you of world famous Nacho Cheese Doritos!!"
	),
	EwFood(
		id_food = "coolranchtaco",
		alias = [
			"ranchtaco",
		],
		recover_hunger = 30,
		price = 13,
		inebriation = 0,
		str_name = 'Cool Ranch taco',
		vendors = [vendor_tacobell],
		str_eat = "You crash your teeth into an explosion of cool ranch taco flavor!! *YEEAAAHHHH!!!*",
		str_desc = "This flavor…?? It’s a mushy mess of poorly seasoned mystery meat and pre-grated cheese powdered in preservatives"
			" trapped in a miserable shell that unfortunately reminds you of Doritos’ *other flavor* that isn't Nacho Cheese."
	),
	EwFood(
		id_food = "quesarito",
		alias = [
			"gordita",
		],
		recover_hunger = 65,
		price = 15,
		inebriation = 0,
		str_name = 'chicken quesarito',
		vendors = [vendor_tacobell],
		str_eat = "It's a burrito, or something. It's got cheese in it. Whatever. You eat it and embrace nothingness.",
		str_desc = "This travesty reminds you of your favorite My Little Pony: Friendship is Magic character Fluttershy for reasons you can't"
			" quite remember and that are pushed out of your mind from embarrassment before you can remember which"
			" analysis video you learned the joke from."
	),
	EwFood(
		id_food = "steakvolcanoquesomachorito",
		alias = [
			"machorito",
			"quesomachorito"
		],
		recover_hunger = 240,
		price = 29,
		inebriation = 0,
		str_name = 'SteakVolcanoQuesoMachoRito',
		vendors = [vendor_tacobell],
		str_eat = "It's a big fucking mess of meat, vegetables, tortilla, cheese, and whatever else happened to be around. You gobble it down greedily!!",
		str_desc = "This pound of greasy, soggy, and flavorless artificially flavored fast food just broke through the damp, leaking"
			" paper bag you doubled wrapped it in. Guess you're going to have to eat it off the floor."
	),
	EwFood(
		id_food = "coleslaw",
		alias = [
			"slaw",
		],
		recover_hunger = 10,
		price = 12,
		inebriation = 0,
		str_name = 'tub of cole slaw',
		vendors = [vendor_kfc],
		str_eat = "It's a cup of some gross white cabbage swimming in watery mayo. Why the fuck would you order this?",
		str_desc = "This side is so horrific you might just start seeing dead people if you eat it."
	),
	EwFood(
		id_food = "biscuitngravy",
		alias = [
			"biscuit",
			"gravy"
		],
		recover_hunger = 20,
		price = 10,
		inebriation = 0,
		str_name = 'biscuit with a side of gravy',
		vendors = [vendor_kfc],
		str_eat = "You get a biscuit and a small bucket of brown gravy. You dip the biscuit, scarf it down, then chug the gravy. *burp.*",
		str_desc = "A cold biscuit that could break the glass if you threw it at window and scalding hot gravy that they let burn"
			" away the filth and grime in their pots so they don't have to clean them."
	),
	EwFood(
		id_food = "chickenbucket",
		alias = [
			"bucket",
			"chicken",
		],
		recover_hunger = 280,
		price = 32,
		inebriation = 0,
		str_name = '8-piece fried chicken bucket',
		vendors = [vendor_kfc],
		str_eat = "You feast on hot, crispy, dripping white meat. Your fingers and tongue are scalded and you don't give a shit.",
		str_desc = "Children are starving in Africa and you order a bucket of fried chicken just for yourself."
			" Well, to be honest I don't even think the starving African children would touch KFC."
	),
	EwFood(
		id_food = "famousbowl",
		alias = [
			"gordita",
		],
		recover_hunger = 80,
		price = 16,
		inebriation = 0,
		str_name = 'Famous Mashed Potato Bowl',
		vendors = [vendor_kfc],
		str_eat = "You scarf down a shitty plastic bowl full of jumbled-up bullshit. It really hits the spot!",
		str_desc = "It’s just not a meal unless it’s a potato-based meal with a calorie count in the six digits."
	),
	EwFood(
		id_food = "barbecuesauce",
		alias = [
			"bbqsauce",
			"sauce",
			"saucepacket",
		],
		recover_hunger = 0,
		price = 0,
		inebriation = 0,
		str_name = 'packet of BBQ Sauce',
		vendors = [vendor_kfc],
		str_eat = "You discard what's left of your dignity and purchace a packet of barbeque sauce to slurp down.",
		str_desc = "You're not alone. Confidential help is available for free. Call the suicide hotline if you're having thoughts of eating this."
	),
	EwFood(
		id_food = "mtndew",
		alias = [
			"dew",
			"mountaindew",
			"greendew"
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with vivid green swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial various citrus flavorings. Sick!!"
	),
	EwFood(
		id_food = "bajablast",
		alias = [
			"bluedew",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew Baja Blast',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with light bluish swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial lime flavoring. Cool!!"
	),
	EwFood(
		id_food = "codered",
		alias = [
			"reddew",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew Code Red',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with red swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial cherry flavoring. Sweet!!"
	),
	EwFood(
		id_food = "pitchblack",
		alias = [
			"blackdew",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew Pitch Black',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with dark purple swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial grape flavoring. Gnarly!!"
	),
	EwFood(
		id_food = "whiteout",
		alias = [
			"whitedew",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew White-Out',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with pale cloudy swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial lemon flavoring. Bodacious!!"
	),
	EwFood(
		id_food = "livewire",
		alias = [
			"orangedew",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'Mtn Dew Livewire',
		vendors = [vendor_mtndew, vendor_vendingmachine],
		str_eat = "You fill your jumbo fountain drink vessel with orange swill and gulp it down.",
		str_desc = "Ah, a nice cold brew resembling a mix between battery acid and artificial orange flavoring. Tubular!!"
	),
	EwFood(
		id_food = "shrimpcocktail",
		alias = [
			"shimp",
			"cocktail",
		],
		recover_hunger = 200,
		price = 34,
		inebriation = 0,
		str_name = 'a shrimp cocktail',
		vendors = [vendor_seafood],
		str_eat = "You pull out the prawns and pop ‘em into your mouth one after without removing their shell. To wash down the shards of crustacean getting lodged in the roof of your mouth, you take vigorous swigs of the cocktail sauce straight out of the glass.",
		str_desc = "A wavy glass of some shelled shrimp dipped in a weird, bitter ketchup that assaults your snout and mouth with unfortunate strength. Nothing is sacred."
	),
	EwFood(
		id_food = "halibut",
		alias = [
			"halibut",
		],
		recover_hunger = 280,
		price = 42,
		inebriation = 0,
		str_name = 'a grilled halibut',
		vendors = [vendor_seafood],
		str_eat = "You scarf down some delicious grilled halibut for the helluvit and it’s accompanying sides for the sidesuvit.",
		str_desc = "A grilled hunk of halibut, served with chipotle dirty rice and corn."
	),
	EwFood(
		id_food = "salmon",
		alias = [
			"salmon",
		],
		recover_hunger = 280,
		price = 45,
		inebriation = 0,
		str_name = 'a wood fired salmon',
		vendors = [vendor_seafood],
		str_eat = "You swallow the wood fired salmon without saving any of its smoky aftertaste! Aww man, so much for the extra 2 SlimeCoin…",
		str_desc = "A wood fired slice of salmon, served with a Dijon glaze and scalloped potatoes and broccoli on the side."
	),
	EwFood(
		id_food = "mahimahi",
		alias = [
			"mahimahi",
		],
		recover_hunger = 280,
		price = 42,
		inebriation = 0,
		str_name = 'a sauteed mahi mahi',
		vendors = [vendor_seafood],
		str_eat = "You gobble up the sauteed mahi mahi with lighting speed, reducing the proud fish into liquid in a matter of seconds.",
		str_desc = "A sauteed measurement of mahi mahi, with a lemon pepper crust and served with scalloped potatoes and spinach."
	),
	EwFood(
		id_food = "scallops",
		alias = [
			"scallops",
		],
		recover_hunger = 240,
		price = 39,
		inebriation = 0,
		str_name = 'pan-seared scallops',
		vendors = [vendor_seafood],
		str_eat = "You lean your head back, grab a few scallops, and try throwing them up into air and landing them in your mouth. This goes extremely poorly.",
		str_desc = "Some pan-seared scallops, served with goat cheese grits, sweet corn, and asparagus."
	),
	EwFood(
		id_food = "clamchowder",
		alias = [
			"clam",
			"chowder",
		],
		recover_hunger = 175,
		price = 30,
		inebriation = 0,
		str_name = 'a cup of clam chowder',
		vendors = [vendor_seafood],
		str_eat = "You scoop out a glob of the hearty chowder and clench your fist above your head, letting it drizzle down all over your face and into your eager mouth. You’re a fucking freak.",
		str_desc = "A bowl of New England clam chowder, served to you cold and runny in Arizona."
	),
	EwFood(
		id_food = "steaknlobster",
		alias = [
			"lobster",
		],
		recover_hunger = 500,
		price = 66,
		inebriation = 0,
		str_name = 'a rock lobster tail and a sirloin steak',
		vendors = [vendor_seafood],
		str_eat = "You discard the napkin immediately, along with the silverware trapped inside of it, opting to instead to eat the meal with your hands. You pry the lobster from its shell first, ramming it into your mouth and taking a shot of melted butter to soften it up while you chew. You continue onto the steak, carefully sliced against the grain, and smother it in half a bottle of A1 sauce and just start to suck on the two inch pieces as if they were a jawbreaker or some other hard candy. You suck on the dead animal until it moistens to the point of liquefying, a solid hour and a half each. You burp loudly. Man, what an unforgettable dinner!",
		str_desc = "A grilled 12oz sirloin steak and similarly sized rock lobster tail, served with scalloped potatoes, broccoli, asparagus, shallot herb butter along side a portrait of the chef that was autographed and kissed with a vibrant red lipstick. From his loving wife, or something? You break the portrait with your fist and your hand starts to bleed."
	),
	EwFood(
		id_food = "kingpincrab",
		alias = [
			"crab",
			"kingpin",
		],
		recover_hunger = 450,
		price = 61,
		inebriation = 0,
		str_name = 'an Arizonian Kingpin Crab',
		vendors = [vendor_seafood],
		str_eat = "You’re too weak to properly crack the mighty crabs’ carapaces, even with the proper crab carapace cracking crackers. After about 10 minutes of desperately trying to, you just whip out whatever weapon you currently have quiped and start to viciously strike the crustaceans in a vain attempt to release their inner, delectable meat. You just end up destroying the entire table you’re eating at.",
		str_desc = "Two imposing 1½ lb Arizonian Kingpin Crabs, steamed and split, served with a small side of melted butter. Their unique pink and purple carapaces that distinguish them are purely cosmetic, but you’ll always think one color tastes better than the other. D’awww..."
	),
	EwFood(
		id_food = "champagne",
		alias = [
			"champagne",
		],
		recover_hunger = 40,
		price = 99,
		inebriation = 99,
		str_name = 'a bottle of champagne',
		vendors = [vendor_seafood],
		str_eat = "You shake the bottle violently before popping off the cork and letting the geyser of pink alcohol blast your waiter in the face. Haha, what a fucking dumbass.",
		str_desc = "The bubbly, carbonated bright pink liquid contained inside this bottle is very reminiscent of of the alcohol in Disney’s The Great Mouse Detective, otherwise known as most appealing liquid on Earth until you remember it’s not straight edge."
	),
	EwFood(
		id_food = "sparklingwater",
		alias = [
			"sparklingwater",
		],
		recover_hunger = 5,
		price = 10,
		inebriation = 0,
		str_name = 'a glass of sparkling water',
		vendors = [vendor_seafood],
		str_eat = "You savor every bubble in the lightly carbonated bliss. ‘Ah, just like in Roma,’ you think to yourself, eyes watering",
		str_desc = "You savor every bubble of this lightly carbonated bliss. Your eyes begin to tear up as you fondly regard your own ecstasy. ‘Ah, just like in Roma…’"
	),
	EwFood(
		id_food = "juviesroe",
		alias = [
			"roe",
		],
		recover_hunger = 40,
		price = 99,
		inebriation = 0,
		str_name = 'a bowl of decadent Juvie’s Roe',
		vendors = [vendor_seafood],
		str_eat = "You don’t really know how to eat caviar, so you just scoop some of the disgusting slop out of the tin with your bare hands and get crushed eggs all over your mouth as you shovel it into your uncultured maw. It tastes, uh… high class? This was a waste of money.",
		str_desc = "A small tin of wild, matured Juvie’s roe. A highly sought after delicacy by the upper crust of the critical improshived juveniles of the city. Considered by many to be the height of luxury, and utterly decadent show of unrivalled epicurean ecstasy. Sure, maybe the indescribable bursts of flavor that terrorize and confuse the uncultured masses COULD be described as non-existent, reducing the whole dish to a weird, goopy mess, BUT YOU KNOW BETTER!!!!"

	),
	EwFood(
		id_food = "homefries",
		alias = [
			"fries",
		],
		recover_hunger = 10,
		price = 9,
		inebriation = 0,
		str_name = 'home fries',
		vendors = [vendor_diner],
		str_eat = "You cram as many overcooked cubes of potato into your oversized maw as possible.You choke painfully on some of the tiny bits that that bypass your attempts at chewing and lodge themselves into your windpipe. You hunger for more.",
		str_desc = "A greasy, over salted, crispy pile of miniature potato chunks, ranging from the average cubes to smaller irregularly shaped, condensed bits of pure fried potato skin. With a calorie count well above your recommended daily consumption in just a handful, you could subsist on these preservative riddled species of spud for well over a week and still gain weight. Too bad you can’t stop yourself from guzzling an entire plates worth in 5 minutes. Oops."
	),
	EwFood(
		id_food = "pancakes",
		alias = [
			"flapjacks",
		],
		recover_hunger = 40,
		price = 9,
		inebriation = 0,
		str_name = 'three pancakes',
		vendors = [vendor_diner],
		str_eat = "You drench your three flapjacks in a generous helping of maple syrup and slap a stick of butter on top for good measure. It’s a good thing you’ve drowned your pancakes in all this excess shit, or you might have actually tasted them! The soggy, limp fried dough is so much more appetizing when all it’s innate flavor is overrun by pure sugary excess.",
		str_desc = "Pancakes are usually a pretty safe bet, no matter where you are. You can’t really mess up a pancake unless you’re specifically trying to burn it. Luckily, the dedicated chefs in the kitchen are doing just that! Thank God, you almost got a good meal in this city."
	),
	EwFood(
		id_food = "chickennwaffles",
		alias = [
			"belgium",
			"cnw",
		],
		recover_hunger = 65,
		price = 11,
		inebriation = 0,
		str_name = 'two chicken strips and a waffle',
		vendors = [vendor_diner],
		str_eat = "You promptly seperate the two chicken strips and waffle on to separate plates, quarantining them off completely from one another. You dip the chicken strips into some ketchup and drizzle some syrup onto the waffles, making sure to NEVER combine the two bitter rivals and to cleanse your palette before switching between them. Ah, the life of a picky eater, it’s hard and no one understands.",
		str_desc = "Waffles are the perfect test subject. Whether it’s a good waffle or a bad waffle, they’re all going to hover around the same average quality. So, whenever you’re in a new town and you wanna judge the quality of any given breakfast diner, order the waffle and rest easy knowing that even the worst waffle isn’t really that bad. Oh, this waffle? It’s terrible. At least you have two chicken strips that were clearly frozen and only heated up a couple of minutes before you received them. For all of the loss in quality and flavor, you can fuck up microwaving something."
	),
	EwFood(
		id_food = "frenchtoast",
		alias = [
			"toast",
		],
		recover_hunger = 40,
		price = 9,
		inebriation = 0,
		str_name = 'four slices of french toast',
		vendors = [vendor_diner],
		str_eat = "You brace untold misery, for your hopes and dreams to be smashed utterly and irreparably, and most importantly to have wasted 12 SlimeCoin on the worst meal of your life. Every hair on your body stands upright, as if preparing for a betrayal fueled stroke. You bite into the toast, and as soon as the sweet pastry touches your tongue you feel as though you finally resonate with the ending of critically acclaimed children’s movie Ratatouille. The bread is fluffy, light, and pleasantly moist, the perfect distribution of cinnamon and nutmeg, mixed with light sprinkles of sugar and vanilla, create a french toast that is sweet but not sickeningly so. You can’t believe you’re saying this, but… it’s perfect! Your compliments to the chef, you guess.",
		str_desc = "French toast is the hardest to perfect out of the legendary fried dough trio. Requiring even cursory amounts of knowledge or expertise in the kitchen proves to be too much for the chefs of diners nationwide. And unlike both the pancake and the waffle, there is a huge difference between a good french toast and a bad french toast. There is nothing more euphoric than biting into a fluffy, moist, and sweet piece of good french toast, while conversely there is nothing that invokes the image of pigs greedily eating trash in their trough than the feeling of a sticky glob of undercooked dough slide down your throat from a bad french toast. You really have to be sure that the restaurant you’re ordering french toast knows what they’re doing, or else your night is ruined. Now, take a wild guess if the chefs at the Smoker’s Cough know what they’re doing."
	),
	EwFood(
		id_food = "friedeggs",
		alias = [
			"eggs",
		],
		recover_hunger = 30,
		price = 8,
		inebriation = 0,
		str_name = 'two sunny side up eggs',
		vendors = [vendor_diner],
		str_eat = "You isolate the yolks from your two fried eggs with surgical precision, leaving a clump of egg whites scraps and two perfectly contained yellow bubbles waiting to burst. You salt and pepper them both thoroughly before eating one after another, first chewing on the slightly discolored egg whites and then bursting each egg yolk whole in your mouth and letting the runny, golden goo to coat your insides.",
		str_desc = "Sure, you like your egg yolks runny, but given by their snotty, green discoloration, it’s pretty likely these eggs were severely undercooked. Oh well, salmonella here we come!"
	),
	EwFood(
		id_food = "eggsbenedict",
		alias = [
			"benedict",
			"benny",
		],
		recover_hunger = 30,
		price = 9,
		inebriation = 0,
		str_name = 'an eggs benedict',
		vendors = [vendor_diner],
		str_eat = "Even though you’re pretty sure you know what an eggs benedict is, you aren’t sure you know how to eat it. You pick up the muffin and just take a bite out of it directly, hollandaise sauce and egg yolk coat your nostrils and generally splatters all over your face. Who would eat something like this????",
		str_desc = "An English muffin topped off with some ham, a poached egg, and hollandaise sauce. It seems like the sort of food that’d you would enjoy, it’s customizable and leans itself to quirky variants, it’s pretty easy to make, it has an egg on it… still, the food comes across as menacing. It’s thick sauce masks it’s ingredients, what secrets could it be hiding? You guess there’s only one way to find out. Gulp!"
	),
	EwFood(
		id_food = "scrambledeggs",
		alias = [
			"scrambled",
		],
		recover_hunger = 30,
		price = 8,
		inebriation = 0,
		str_name = 'two scrambled eggs',
		vendors = [vendor_diner],
		str_eat = "You attempt to strangle your ketchup bottle for the state mandated dollop of ketchup to be adequately mixed into your scrambled egg when tragedy strikes! The bottle is empty! It blasts out specs of ketchup and a funny noise a few times before you throw it against the wall in ballistic anger. You are forced to eat the eggs… plain. DEAR GOD!!!!",
		str_desc = "Some scrambled eggs. Come on, you know what scrambled eggs are, right? Do I have to spell out everything for you? Do you want me to stay awake all night and come up with immature jokes and puns for every one of these fucking things? Come on kid, get real."
	),
	EwFood(
		id_food = "omelette",
		alias = [
			"omelette",
		],
		recover_hunger = 50,
		price = 9,
		inebriation = 0,
		str_name = 'a western omelette',
		vendors = [vendor_diner],
		str_eat = "You pour plenty of hot sauce all over your omelette and shove bite after bite into your slobbering mouth. The heat from the sauce and the bell peppers builds to a breaking point, causing you to blackout. You wake up an indeterminate amount of time later, covered in dried tears and sweat and your abdomen feeling as though you’re pregnant with Satan. You love pain.",
		str_desc = "A delicious Denver omelette, stuffed with diced ham, onions, and green peppers. Looks great! Hm? Excuse me? What the fuck is a ‘western omelette’? Do people on the east coast seriously call Denver omelettes that? Are you joking me? You ask anyone on the sensible half of the country what the name of the best omelette is and they’ll bark back the long and storied history of John D. Omelette and his rough-and-tumble youth growing up in the mean streets of the great state of Colorado’s capital. Do they not know what Denver is? Do they think everything past the Appalachians are uncharted wilderness? Man, fuck you guys. We know were New York is, we know where Boston is, we know where Cincinnati is, we know our geography of the east coast like the back of our hand and it’s about time you start memorizing ours. Eat shit."
	),
	EwFood(
		id_food = "orangejuice",
		alias = [
			"oj",
			"juice",
		],
		recover_hunger = 10,
		price = 6,
		inebriation = 0,
		str_name = 'a glass of orange juice',
		vendors = [vendor_diner],
		str_eat = "You swish around the decadent, pulpy orange juice in your mouth. This exacerbates your already poor dental hygiene, sending shockwaves of pain through your mouth as the sugary liquid washes up against dozens of cavities all throughout your mouth. But, you don’t care. You’re in heaven.",
		str_desc = "A cavity creating, dental decaying, and enamel eroding glass of delicious orange juice. This vibrant citrus drink hits the spot any day of the week, any minute of the day, and every second of your short, pathetic life. Coffee is a myth, water is a joke, soda is piss. #juiceprideworldwide"
	),
	EwFood(
		id_food = "milk",
		alias = [
			"cow juice"
		],
		recover_hunger = 10,
		price = 6,
		inebriation = 0,
		str_name = 'a glass of milk',
		vendors = [vendor_diner],
		str_eat = "You take a swig of a nice, cold glass of whole milk and your palette is instantly clear of any sugary or syrupy foods you may have been eating. You are left in total cow induced euphoria.",
		str_desc = "A simple glass of milk. No more, no less. "
	),
	EwFood(
		id_food = "steakneggs",
		alias = [
			"steak",
		],
		recover_hunger = 80,
		price = 12,
		inebriation = 0,
		str_name = "two steak tips and two sunny side up eggs",
		vendors = [vendor_diner],
		str_eat = "You break the yolk of your two fried eggs immediately, letting the yolk run and pool around the steak tips, acting as a dipping sauce. With each mouthwatering bite of juicy, medium rare steak coated in delicious, runny yolk, you reach a higher level of christ consciousness. How does no one else but you do this?",
		str_desc = "The only actually filling meal they serve at the diner. Between the two medium rare steak tips and the perfectly cooked sunny side up eggs, you’ve got enough protein in this one meal to grow an extra muscle."
	),
	EwFood(
		id_food = "doubledown",
		alias = [
			"double",
			"down",
			"dd",
		],
		recover_hunger = 150,
		price = 21,
		inebriation = 0,
		str_name = 'Double Down',
		vendors = [vendor_kfc],
		str_eat = "You chomp into the meaty pseudo-sandwich! The Colonol's Special Sauce oozes over your lips and fingers, making you feel absolutely filthy.",
		str_desc = "From between two crispy chicken filets oozes the Colonel's Special Sauce. Haha, nasty!"
	),
	EwFood(
		id_food = "familymeal",
		alias = [
			"family",
			"meal",
			"fm",
		],
		recover_hunger = 360,
		price = 39,
		inebriation = 0,
		str_name = 'KFC Family Meal',
		vendors = [vendor_kfc],
		str_eat = "You stuff your face full of all manner of southern-style delicacies! You chew and chew until your jaw aches and tears stream down your cheeks.",
		str_desc = "A veritable menagerie of homestyle goodness. Chicken, mashed potatoes, mac n' cheese, biscuits and gravy, the list goes on and on."
	),
	EwFood(
		id_food = "plutoniumchicken",
		alias = [
			"pc",
			"pluto",
			"plutonium",
			"pchicken",
		],
		recover_hunger = 450,
		price = 46,
		inebriation = 0,
		str_name = 'whole plutonium-battered fried chicken',
		vendors = [vendor_kfc],
		str_eat = "You crunch into the remains of this once-majestic animal. The odd metallic taste makes your tongue tingle in a most unsettling way.",
		str_desc = "It resembles a cooked chicken, save for an extra wing or two, encrusted with an odd greenish-brown coating. May adversely affect sperm count."
	),
	EwFood(
		id_food = "giantdeepdish",
		alias = [
			"gdd",
			"deepdish",
		],
		recover_hunger = 320,
		price = 35,
		inebriation = 0,
		str_name = 'giant deep-dish pizza',
		vendors = [vendor_pizzahut],
		str_eat = "You slurp down slice after slice of sopping sauce-soaked pizza in a gruesome red runny spectacle.",
		str_desc = "The sauce and cheese of this delicacy is like quicksand, anything falling in will sink to the bottom, never to be seen again."
	),
	EwFood(
		id_food = "whackcalzone",
		alias = [
			"wc",
			"whack",
			"calzone",
		],
		recover_hunger = 500,
		price = 50,
		inebriation = 0,
		str_name = 'Whack Calzone',
		vendors = [vendor_pizzahut],
		str_eat = "Chomping into this collossal italian confection, searing hot cheese explodes out from the edges in every direction. De-LISH!!!",
		str_desc = "It's literally just an upside-down pizza on top of another pizza."
	),
	EwFood(
		id_food = "nachosupreme",
		alias = [
			"ns",
			"nacho",
			"nachos",
			"supreme",
		],
		recover_hunger = 175,
		price = 23,
		inebriation = 0,
		str_name = 'Nacho Supreme',
		vendors = [vendor_tacobell],
		str_eat = "You shovel fistfuls of nacho detritus into your gaping maw. Your gums are savaged by the sharp edges of the crips corny chips.",
		str_desc = "A plate full of crisp tortilla chips onto which ground beef, sour cream, cheese, tomatoes, and various assorted bullshit has been dumped."
	),
	EwFood(
		id_food = "energytaco",
		alias = [
			"et",
			"energy",
			"etaco",
		],
		recover_hunger = 400,
		price = 42,
		inebriation = 0,
		str_name = 'Energy Taco',
		vendors = [vendor_tacobell],
		str_eat = "Biting into this taco, your mouth is numbed by a sudden discharge of stored energy, accompanied by a worrisome flash of greenish light. You can't say for sure if it tasted good or not.",
		str_desc = "This resembles a normal taco, but where the cheese might normally be is a strange glowing green fluid. It occasionally sparks and crackles with limic energy."
	),
	EwFood(
		id_food = "mtndewsyrup",
		alias = [
			"syrup",
			"mdsyrup",
			"mds",
			"greensyrup",
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous green fluid reeks with a sickly-sweet citrusy odor."
	),
	EwFood(
		id_food = "bajablastsyrup",
		alias = [
			"bbsyrup",
			"bbs",
			"bluesyrup",
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW Baja Blast syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous blue fluid reeks with a sickly-sweet tropical odor."
	),
	EwFood(
		id_food = "coderedsyrup",
		alias = [
			"crsyrup",
			"crs",
			"redsyrup",
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW Code Red syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous red fluid reeks with a sickly-sweet cherry odor."
	),
	EwFood(
		id_food = "pitchblacksyrup",
		alias = [
			"pbsyrup",
			"pbs",
			"blacksyrup",
			"purplesyrup"
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW Pitch Black syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous purple fluid reeks with a sickly-sweet grapey odor."
	),
	EwFood(
		id_food = "whiteoutsyrup",
		alias = [
			"wosyrup",
			"wos",
			"whitesyrup",
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW White Out syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous pale fluid reeks with a sickly-sweet citrusy odor."
	),
	EwFood(
		id_food = "livewiresyrup",
		alias = [
			"lwsyrup",
			"lws",
			"orangesyrup",
		],
		recover_hunger = 200,
		price = 26,
		inebriation = 0,
		str_name = 'cup of pure undiluted MTN DEW Livewire syrup',
		vendors = [vendor_mtndew],
		str_eat = "You pour the molasses-like liquid down your throat. It stings your teeth and clings to your esophagus on the way down, but you feel suddenly invigorated as your blood sugar skyrockets!!",
		str_desc = "This thick, viscous orange fluid reeks with a sickly-sweet orangey odor."
	),
	EwFood(
		id_food = "razornuts",
		alias = [
			"rn",
			"razor",
			"nuts",
		],
		recover_hunger = 25,
		price = 5,
		inebriation = 0,
		str_name = 'packet of salted razornuts',
		vendors = [vendor_bar],
		str_eat = "You tear into the packet and eat the small, pointy nuts one at a time, carefully avoiding any accidental lacerations.",
		str_desc = "It's a packet of locally-grown razornuts, roasted and salted to perfection. Perfect for snacking!"
	),
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

	# Add food to its vendors' lists.
	for vendor in food.vendors:
		vendor_list = food_vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			food_vendor_inv[vendor] = vendor_list

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

	EwItemDef(
		item_type = it_questitem,
		str_name = "{qitem_name}",
		str_desc = "{qitem_desc}",
		soulbound = True,
		item_props = {
			'qitem_name': 'Quest Item',
			'qitem_desc': 'Something important to somebody.'
		}
	),

	EwItemDef(
		item_type = it_food,
		str_name = "{food_name}",
		str_desc = "{food_desc}",
		soulbound = False,
		item_props = {
			'food_name': 'Food Item',
			'food_desc': 'Food.',
			'recover_hunger': 0,
			'price': 0,
			'inebriation': 0,
			'vendor': None,
			'str_eat': 'You eat the food item.',
			'time_expir': std_food_expir
		}
	),

	EwItemDef(
		item_type = it_weapon,
		str_name = "{weapon_name}",
		str_desc = "{weapon_desc}",
		soulbound = False,
		item_props = {
			'weapon_name': 'Weapon',
			'weapon_desc': 'It\'s a weapon of some sort.'
		}
	),
	EwItemDef(
		item_type = it_cosmetic,
		str_name = "{cosmetic_name}",
		str_desc = "{cosmetic_desc}",
		soulbound = False,
		item_props = {
			'cosmetic_name': 'Cosmetic Item',
			'cosmetic_desc': 'Cosmetic Item.',
			'rarity': rarity_plebeian
		}
	)
]

# A map of item_type to EwItemDef objects.
item_def_map = {}

# Populate the item def map.
for item_def in item_def_list:
	item_def_map[item_def.item_type] = item_def

poi_list = [
	EwPoi( # ENDLESS WAR
		id_poi = poi_id_endlesswar,
		alias = [
			"obelisk",
			"war",
			"ew"
		],
		str_in = "at the base of",
		str_enter = "arrive at",
		str_name = "ENDLESS WAR",
		str_desc = "ENDLESS WAR towers above you, its gray color almost making it seem to disappear against the gray of the sky. Its eye is closed, motionless.",
		coord = (27, 16),
		channel = channel_endlesswar,
		role = "Endless War"
	),
	EwPoi( # slimecorp HQ
		id_poi = poi_id_slimecorphq,
		alias = [
			"slimecorp",
			"hq",
		],
		str_name = "SlimeCorp HQ",
		str_desc = "Within the gleaming metal hull of the towering SlimeCorp HQ, brightly lit sterile white hallways wind like a maze, past countless receptionists' desks, waiting rooms, and high-tech stainless steel vault doors.",
		coord = (27, 18),
		channel = channel_slimecorphq,
		role = "SlimeCorp HQ",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_downtown
	),
	EwPoi( # 1
		id_poi = poi_id_downtown,
		alias = [
			"central",
			"dt",
		],
		str_name = "Downtown NLACakaNM",
		str_desc = "Skyscrapers tower over every street as far as the eye can see. Fluorescent signs flash advertisements in strange glyphs and the streets roar with the sound of engines and scraping metal from the subway deep underground.\n\nThis area contains ENDLESS WAR, SlimeCorp HQ and the Slime Stock Exchange. To the north is Smogsburg. To the East is the Green Light District. To the South is the Rowdy Roughhouse. To the Southwest is Poudrin Alley. To the West is Krak Bay. To the Northwest is Cop Killtown.",
		coord = (23, 16),
		coord_alias = [
			(24, 16),
			(25, 16),
			(25, 17),
			(25, 18)
		],
		channel = "downtown",
		role = "Downtown",
		property_class = property_class_s,
		is_capturable = True
	),
	EwPoi( # 2
		id_poi = poi_id_smogsburg,
		alias = [
			"smog",
			"smogs",
			"sb"
		],
		str_name = "Smogsburg",
		str_desc = "The pavement rumbles as subway trains grind along their tracks far beneath your feet. In every direction, smokestacks belch sickly clouds into the sky.\n\nThis area contains the Bazaar. To the North is Arsonbrook. To the Northeast is Little Chernobyl. To the East is Old New Yonkers. To the South is Downtown NLACakaNM. To the West is Cop Killtown. To the Northwest is Astatine Heights.",
		coord = (23, 11),
		channel = "smogsburg",
		role = "Smogsburg",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 3
		id_poi = poi_id_copkilltown,
		alias = [
			"cop",
			"cops",
			"killers",
			"killer",
			"killtown",
			"copkt",
			"ck"
		],
		str_name = "Cop Killtown",
		str_desc = "Deep indigo edifices of metal and brick rise above the pavement. Apartment windows glint in the blue and purple light of neon signs, and a menacing cathedral looms darkly on the horizon.\n\nTo the North is Astatine Heights. To the East is Smogsburg. To the Southeast is Downtown NLACakaNM. To the West is Vandal Park. To the Northwest is Gatlingsdale.",
		coord = (17, 13),
		channel = channel_copkilltown,
		role = "Cop Killtown",
		factions = [
			faction_killers
		],
		pvp = False,
		property_class = property_class_a
	),
	EwPoi( # 4
		id_poi = poi_id_krakbay,
		alias = [
			"krak",
			"kb"
		],
		str_name = "Krak Bay",
		str_desc = "Off the nearby riverbank, rusty barges churn their way along the Slime River. Posh riverside apartments taunt you with their cheap opulence.\n\nThis area contains the Food Court. To the East is Downtown NLACakaNM. To the Southeast is Poudrin Alley. To the South is Ooze Gardens. To the Southwest is South Sleezeborough. To the West is North Sleezeborough. To the Northwest is Glocksbury.",
		coord = (16, 19),
		channel = "krak-bay",
		role = "Krak Bay",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 5
		id_poi = poi_id_poudrinalley,
		alias = [
			"poudrin",
			"pa"
		],
		str_name = "Poudrin Alley",
		str_desc = "Bent and broken streetlights spark and flicker over the cracked, derelict pavement. The 7-11 stands dimly opposite a row of apartments, its CLOSED sign crooked and dusty.\n\nThis area contains the 7-11. To the Northeast is Downtown NLACakaNM. To the East is the Rowdy Roughhouse. To the South is Cratersville. To the Southwest is Ooze Gardens. To the Northwest is Krak Bay.",
		coord = (19, 23),
		channel = "poudrin-alley",
		role = "Poudrin Alley",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 6
		id_poi = poi_id_rowdyroughhouse,
		alias = [
			"rowdy",
			"rowdys",
			"rowdies",
			"roughhouse",
			"rowdyrh",
			"rr"
		],
		str_name = "Rowdy Roughhouse",
		str_desc = "Rusted pink metal shanties are hastily constructed as far as the eye can see, sometimes stacked on top of one another, forming high towers and densely populated mazes.\n\nTo the North is Downtown NLACakaNM. To the South is Wreckington. To the Southwest is Cratersville. To the West is Poudrin Alley.",
		coord = (25, 21),
		channel = channel_rowdyroughhouse,
		role = "Rowdy Roughhouse",
		factions = [
			faction_rowdys
		],
		pvp = False,
		property_class = property_class_a
	),
	EwPoi( # 7
		id_poi = poi_id_greenlightdistrict,
		alias = [
			"greenlight",
			"gld"
		],
		str_name = "Green Light District",
		str_desc = "Fluorescent signs flicker bright glyphs over smooth freshly-paved streets, promising all conceivable earthly pleasures. The ground is tacky with some unknown but obviously sinful grime.\n\nThis area contains the Slime Casino. To the East is Vagrant's Corner. To the Southeast is Juvie's Row. To the West is Downtown NLACakaNM.",
		coord = (29, 14),
		channel = "green-light-district",
		role = "Green Light District",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 8
		id_poi = poi_id_oldnewyonkers,
		alias = [
			"ony"
		],
		str_name = "Old New Yonkers",
		str_desc = "Rows of three-story brick and stone condominiums with white marble moulding wind along lanes of chipped cobblestone. Wrought-iron spikes jut from windows and balconies.\n\nTo the Northeast is New New Yonkers. To the Southeeast is Vagrant's Corner. To the Southwest is Smogsburg. To the East is Little Chernobyl. To the Northwest is Brawlden.",
		coord = (32, 9),
		channel = "old-new-yonkers",
		role = "Old New Yonkers",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 9
		id_poi = poi_id_littlechernobyl,
		alias = [
			"chernobyl",
			"lilchernobyl",
			"lilchern",
			"lc"
		],
		str_name = "Little Chernobyl",
		str_desc = "Pathetic little gardens front the uneven parking lots of corporate complexes housing dentists, fortune-tellers, real estate agencies, and other equally dull and pointless ventures.\n\nTo the North is Brawlden. To the East is Old New Yonkers. To the West is Arsonbrook.",
		coord = (25, 7),
		channel = "little-chernobyl",
		role = "Little Chernobyl",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 10
		id_poi = poi_id_arsonbrook,
		alias = [
			"arson",
			"ab"
		],
		str_name = "Arsonbrook",
		str_desc = "North of the bridge, you see large swathes of what were once suburbs blackened and flat, occasionally still smoking. Legends say a Starbucks tried to open here once.\n\nTo the East is Brawlden. To the Southeast is Little Chernobyl. To the South is Smogsburg. To the West is Astatine Heights.",
		coord = (21, 3),
		channel = "arsonbrook",
		role = "Arsonbrook",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 11
		id_poi = poi_id_astatineheights,
		alias = [
			"astatine",
			"heights",
			"ah"
		],
		str_name = "Astatine Heights",
		str_desc = "Modern high-rise condos just from the steep hills to the north. To the south, classical stone and brick houses with columns command disgustingly decadent wide grassy yards.\n\nThis area contains NLACakaNM Cinemas. To the East is Arsonbrook. To the Southeast is Smogsburg. To the South is Cop Killtown. To the Southwest is Gatlingsdale. To the West is Toxington.",
		coord = (17, 6),
		coord_alias = [
			(17, 5),
			(17, 4),
			(17, 3)
		],
		channel = "astatine-heights",
		role = "Astatine Heights",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 12
		id_poi = poi_id_gatlingsdale,
		alias = [
			"gatlings",
			"gatling",
			"gd"
		],
		str_name = "Gatlingsdale",
		str_desc = "The brightest young minds of NLACakaNM fritter away their time here, amid hallowed halls of learning ringed endlessly by foreign book stores and vintage clothing shops.\n\nTo the Northeast is Astatine Heights. To the Southeast is Cop Killtown. To the Southwest is Vandal Park. To the West is Polonium Hill. To the Northwest is Toxington.",
		coord = (13, 9),
		channel = "gatlingsdale",
		role = "Gatlingsdale",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 13
		id_poi = poi_id_vandalpark,
		alias = [
			"vandal",
			"park",
			"vp"
		],
		str_name = "Vandal Park",
		str_desc = "The more-or-less clean air carries the roar of the crowd across the grassy fields surrounding the Battle Arena.\n\nThis area contains the Battle Arena. To the Northeast is Gatlingsdale. To the East is Cop Killtown. To the South is Glocksbury. To the Southwest is West Glocksbury. To the Northwest is Polonium Hill.",
		coord = (10, 12),
		channel = "vandal-park",
		role = "Vandal Park",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 14
		id_poi = poi_id_glocksbury,
		alias = [
			"glocks",
			"glock",
			"gb"
		],
		str_name = "Glocksbury",
		str_desc = "You smell bacon. *Figurative* bacon. The streets are too orderly here... the cops must be about. Absolutely vile.\n\nTo the North is Vandal Park. To the Southeast is Krak Bay. To the South is North Sleezeborough. To the West is West Glocksbury.",
		coord = (9, 16),
		channel = "glocksbury",
		role = "Glocksbury",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 15
		id_poi = poi_id_northsleezeborough,
		alias = [
			"northsleezeboro",
			"nsleezeborough",
			"nsleezeboro",
			"nsleeze",
			"northsleeze",
			"nsb",
			"ns"
		],
		str_name = "North Sleezeborough",
		str_desc = "Young jobless adults walk around in plaid and suspenders with curious facial hair, stopping into the occasional store front to buy a vinyl recording or an ironic knick-knack.\n\nTo the North is Glocksbury. To the East is Krak Bay. To the South is South Sleezeborough.",
		coord = (11, 19),
		channel = "north-sleezeborough",
		role = "North Sleezeborough",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 16
		id_poi = poi_id_southsleezeborough,
		alias = [
			"southsleezeboro",
			"ssleezeborough",
			"ssleezeboro",
			"ssleeze",
			"southsleeze",
			"ssb",
			"ss"
		],
		str_name = "South Sleezeborough",
		str_desc = "The streets are empty. The residents of this neighborhood have all lost their nerve and are hiding in their hovels in a futile attempts to stay safe from gang violence.\n\nThis area contains the Dojo. To the North is North Sleezeborough. To the Northeast is Krak Bay, To the East is Ooze Gardens.",
		coord = (12, 22),
		channel = "south-sleezeborough",
		role = "South Sleezeborough",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 17
		id_poi = poi_id_oozegardens,
		alias = [
			"ooze",
			"gardens",
			"og"
		],
		str_name = "Ooze Gardens",
		str_desc = "A bird chirps its last before falling dead from a withered tree. A trickle of slime runs down its bark. The resident's attempts to beautify the neighborhood with foliage have really backfired, aesthetically speaking.\n\nTo the North is Krak Bay. To the Northeast is Poudrin Alley. To the East is Cratersville. To the West is South Sleezeborough.",
		coord = (14, 25),
		channel = "ooze-gardens",
		role = "Ooze Gardens",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 18
		id_poi = poi_id_cratersville,
		alias = [
			"craters",
			"cville",
			"cv"
		],
		str_name = "Cratersville",
		str_desc = "The people here hurry to their destinations, avoiding eye contact. They must be wary after seeing gang members level the next town over not too long ago.\n\nTo the North is Poudrin Alley. To the Northeast is the Rowdy Roughhouse. To the East is Wreckington. To the West is Ooze Gardens.",
		coord = (19, 28),
		channel = "cratersville",
		role = "Cratersville",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 19
		id_poi = poi_id_wreckington,
		alias = [
			"wrecking",
			"wton",
			"ton",
			"wt"
		],
		str_name = "Wreckington",
		str_desc = "You step over piles of rubble that once housed the now-displaced population of this neighborhood. A recent a dramatic victim of rampant gang warfare.\n\nTo the North is the Rowdy Roughhouse. To the West is Cratersville.",
		coord = (27, 24),
		channel = "wreckington",
		role = "Wreckington",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 20
		id_poi = poi_id_juviesrow,
		alias = [
			"juvies",
			"jrow",
			"jr"
		],
		str_name = "Juvie's Row",
		str_desc = "Quaint little Juvie shanties pepper the landscape around the entrance to the slime mines. Pale rocks and sticks are arranged in sad fascimiles of white picket fences. You're filled with pity, as well as disgust.\n\nTo the Northeast is Vagrant's Corner. To the Northwest is the Green Light District.",
		coord = (32, 18),
		channel = "juvies-row",
		role = "Juvie's Row",
		pvp = False,
		property_class = property_class_a
	),
	EwPoi( # 21
		id_poi = poi_id_slimesend,
		alias = [
			"slimes",
			"send",
			"end",
			"se"
		],
		str_name = "Slime's End",
		str_desc = "The narrow peninsula is bordered on both sides by the Slime Sea. The phosphorescence of the Sea illuminates the land and sky with an eerily even green glow.\n\n To the North is Vagrant's Corner.",
		coord = (40, 16),
		channel = "slimes-end",
		role = "Slime's End",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 22
		id_poi = poi_id_vagrantscorner,
		alias = [
			"vagrants",
			"vcorner",
			"vc"
		],
		str_name = "Vagrant's Corner",
		str_desc = "The glow of the Slime Sea illumunates the undersides of the docks and the heavy industrial machinery designed to pump slime into the cargo holds of outbound barges.\n\nThis area contains The King's Wife's Son Speakeasy. To the North is New New Yonkers. To the Northeast is Assault Flats Beach Resort. To the South is Slime's End. To the Southwest is Juvie's Row. To the West is the Green Light District. To the Northwest is Old New Yonkers.",
		coord = (37, 11),
		channel = "vagrants-corner",
		role = "Vagrant's Corner",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 23
		id_poi = poi_id_assaultflatsbeachresort,
		alias = [
			"assaultflatsbeach",
			"assaultflats",
			"beach",
			"resort",
			"assault",
			"flats",
			"af",
			"br",
			"assflats",
			"afbr"
		],
		str_name = "Assault Flats Beach Resort",
		str_desc = "The white imported sand of the beach stretches toward the horizon, lapped by gentle waves of slime. Gleaming hotels jut out of the rock formations just off the beachfront.\n\nTo the South is Vagrant's Corner. To the West is New New Yonkers.",
		coord = (40, 6),
		channel = "assault-flats-beach-resort",
		role = "Assault Flats Beach Resort",
		property_class = property_class_s,
		is_capturable = True
	),
	EwPoi( # 24
		id_poi = poi_id_newnewyonkers,
		alias = [
			"nnewyonkers",
			"nnyonkers",
			"nny"
		],
		str_name = "New New Yonkers",
		str_desc = "Trendy restaurants and clubs sit empty in this sparsely-populated failed gentrification experiment.\n\nTo the East is Assault Flats Beach Resort. To the South is Vagrant's Corner. To the Southwest is Old New Yonkers. To the West is Brawlden.",
		coord = (36, 4),
		channel = "new-new-yonkers",
		role = "New New Yonkers",
		property_class = property_class_b,
		is_capturable = True
	),
	EwPoi( # 25
		id_poi = poi_id_brawlden,
		alias = [
			"den",
			"bd"
		],
		str_name = "Brawlden",
		str_desc = "Rough-looking bewifebeatered citizens are everywhere, doing unspecified maintenence on strange machines propped up on cinderblocks. A SlimeCorp Laboratory hums and whirrs in the distance, day and night.\n\nThis area contains the Slimeoid Laboratory. To the East is New New Yonkers. To the Southeast is Old New Yonkers. To the South is Little Chernobyl. To the West is Arsonbrook.",
		coord = (28, 3),
		channel = "brawlden",
		role = "Brawlden",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 26
		id_poi = poi_id_toxington,
		alias = [
			"tox",
			"tton",
			"ttn",
			"tt",
			"tx"
		],
		str_name = "Toxington",
		str_desc = "You cover your mouth in a futile attempt to avoid breathing choking acidic vapor that continually rises off of the nearby lake.\n\nTo the East is Astatine Heights. To the Southeast is Gatlingsdale. To the South is Polonium Hill. To the East is Charcoal Park.",
		coord = (9, 4),
		channel = "toxington",
		role = "Toxington",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 27
		id_poi = poi_id_charcoalpark,
		alias = [
			"charcoal",
			"park2",
			"cpark",
			"awkwardinitials",
			"cp",
			"ch"
		],
		str_name = "Charcoal Park",
		str_desc = "The soil here is mostly black soot and the charred remains of a now long-gone series of low-income apartment complexes. A few shantytowns have been constructed as some of the only living trees in NLACakaNM have sprouted out of the ashes.\n\nTo the East is Toxington. To the South is Polonium Hill.",
		coord = (3, 3),
		channel = "charcoal-park",
		role = "Charcoal Park",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # 28
		id_poi = poi_id_poloniumhill,
		alias = [
			"polonium",
			"hill",
			"phill",
			"ph"
		],
		str_name = "Polonium Hill",
		str_desc = "The gently rolling terrain is speckled with hideous minimansions that obviously cost a fortune and look like complete shit.\n\nTo the North is Charcoal Park. To the Northeast is Toxington. To the East is Gatlingsdale. To the Southeast is Vandal park. To the South is West Glocksbury.",
		coord = (5, 9),
		channel = "polonium-hill",
		role = "Polonium Hill",
		property_class = property_class_a,
		is_capturable = True
	),
	EwPoi( # 29
		id_poi = poi_id_westglocksbury,
		alias = [
			"wglocksbury",
			"westglocks",
			"wglocks",
			"wglock",
			"wgb",
			"wg"
		],
		str_name = "West Glocksbury",
		str_desc = "Gunshots ring out periodically from somewhere in the distance, hidden by laundromats and barber shops. Even the most jaded NLACakaNMite may get a bit nervous 'round these parts.\n\n To the North is Polonium Hill. To the Northeast is Vandal Park. To the East is Glocksbury",
		coord = (4, 14),
		channel = "west-glocksbury",
		role = "West Glocksbury",
		property_class = property_class_c,
		is_capturable = True
	),
	EwPoi( # the-sewers
		id_poi = poi_id_thesewers,
		alias = [
			"drain",
			"sewers",
			"sewer",
			"ghost",
			"ghosts",
			"ts",
			"s"
		],
		str_name = "The Sewers",
		str_desc = "A vast subterranean maze of concrete tunnels, eternally echoing with the dripping of water and decayed slime runoff. All the waste of NLACakaNM eventually winds up here, citizens included.",
		channel = channel_sewers,
		life_states = [
			life_state_corpse
		],
		role = "Sewers"
	),
	EwPoi( # stock-exchange
		id_poi = poi_id_stockexchange,
		alias = [
			"stocks",
			"stock",
			"exchange",
			"sexchange",
			"stockexchange",
			"slimestockexchange",
			"sex",  # slime's end is "se"
			"sec",
			"sx"
		],
		str_name = "The Slime Stock Exchange",
		str_desc = "A large interior space filled with vacant teller booths and data screens designed to dissplay market data, all powered off. Punch cards and ticker tape are strewn about the silent, empty floor.\n\nExits into Downtown NLACakaNM.",
		channel = channel_stockexchange,
		role = "Stock Exchange",
		coord = (21, 16),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_downtown
	),
	EwPoi( # the-bazaar
		id_poi = poi_id_bazaar,
		alias = [
			"bazaar",
			"market",
			"bz",
			"b"
		],
		str_name = "The Bazaar",
		str_desc = "An open-air marketplace where professional merchants and regular citizens alike can hock their wares. It's currently completely barren.\n\nExits into Brawlden.",
		channel = channel_bazaar,
		role = "Bazaar",
		coord = (21, 11),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_smogsburg
	),
	EwPoi( # the-cinema
		id_poi = poi_id_cinema,
		alias = [
			"nlacakanmcinema",
			"cinema",
			"cinemas",
			"theater",
			"movie",
			"movies",
			"nc"
		],
		str_name = "NLACakaNM Cinemas",
		str_desc = "A delightfully run-down movie theater, with warm carpeted walls fraying ever so slightly. Films hand picked by the Rowdy Fucker and/or Cop Killer are regularly screened.\n\nExits into Astatine Heights.",
		channel = channel_cinema,
		role = "Cinema",
		coord = (19, 3),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_astatineheights
	),
	EwPoi( # food-court
		id_poi = poi_id_foodcourt,
		alias = [
			"thenlacakanmfoodcourt",
			"food",
			"foodcourt",
			"food-court",
			"pizzahut",
			"tacobell",
			"kfc",
			"fcourt",
			"fc"
		],
		str_name = "The NLACakaNM Food Court",
		str_desc = "A large, brightly-lit area with tiled walls and floors, lined on all sides with Yum! Brand food vendors, surrounding the city's prized MTN DEW Fountain. The place is completely dead.\n\nExits into Krak Bay.",
		channel = channel_foodcourt,
		role = "Food Court",
		coord = (16, 17),
		pvp = False,
		vendors = [
			vendor_pizzahut,
			vendor_tacobell,
			vendor_kfc,
			vendor_mtndew
		],
		is_subzone = True,
		mother_district = poi_id_krakbay
	),
	EwPoi( # nlac-u
		id_poi = poi_id_nlacu,
		alias = [
			"nlacu",
			"university",
			"nlacuniversity",
			"college",
			"uni",
			"nu"
		],
		str_name = "New Los Angeles City University",
		str_desc = "An expansive campus housing massive numbers of students and administrators, all here in pursuit of knowledge. The campus is open to visitors, but there's nobody here.\n\nExits into Gatlingsdale.",
		channel = channel_nlacu,
		role = "NLAC U",
		coord = (15, 9),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_gatlingsdale
	),
	EwPoi( # battle-arena
		id_poi = poi_id_arena,
		alias = [
			"thearena",
			"arena",
			"battlearena",
			"a",
			"ba"
		],
		str_name = "The Battle Arena",
		str_desc = "A huge arena stadium capable of housing tens of thousands of battle enthusiasts, ringing a large field where Slimeoid Battles are held. All the seats are empty.\n\nExits into Vandal Park.",
		channel = channel_arena,
		role = "Arena",
		coord = (10, 10),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_vandalpark
	),
	EwPoi( # the-dojo
		id_poi = poi_id_dojo,
		alias = [
			"dojo",
			"training",
			"sparring",
			"thedojo",
			"td",
			"d"
		],
		str_name = "The Dojo",
		str_desc = "A modest, easily overlooked building, but containing all the facilities necessary for becoming a killing machine. Bamboo and parchment walls separate the dojo floor into large tatami-matted sections.\n\nExits into South Sleezeborough.",
		channel = channel_dojo,
		role = "Dojo",
		coord = (11, 23),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_southsleezeborough
	),
	EwPoi( # speakeasy
		id_poi = poi_id_speakeasy,
		alias = [
			"kingswifessonspeakeasy",
			"kingswifesson",
			"speakeasy",
			"bar",
			"sons",
			"sez",  # se is already slime's end
			"ez",
			"kws"
		],
		str_name = "The King's Wife's Son Speakeasy",
		str_desc = "A rustic tavern with dark wooden walls and floor, bearing innumerable knickknacks on the walls and high wooden stools arranged in front of a bar made of patina'd copper. There's nobody here.\n\nExits into Vagrant's Corner.",
		channel = channel_speakeasy,
		role = "Speakeasy",
		coord = (39, 11),
		pvp = False,
		vendors = [
			vendor_bar
		],
		is_subzone = True,
		mother_district = poi_id_vagrantscorner
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
		coord = (19, 25),
		pvp = False,
		vendors = [
			vendor_vendingmachine
		],
		is_subzone = True,
		mother_district = poi_id_poudrinalley
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
			"slimeoidlabs",
			"slab",
			"sl"
		],
		str_name = "SlimeCorp Slimeoid Laboratory",
		str_desc = "A nondescript building containing mysterious SlimeCorp industrial equipment. Large glass tubes and metallic vats seem to be designed to serve as incubators. There is a notice from SlimeCorp on the entranceway explaining the use of its equipment. Use !instructions to read it.\n\nExits into Brawlden.",
		channel = channel_slimeoidlab,
		role = "Slimeoid Lab",
		coord = (28, 1),
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_brawlden
	),
	EwPoi( # the-mines
		id_poi = poi_id_mine,
		alias = [
			"mines",
			"mine",
			"m",
			"tm",
			"jrm"
		],
		str_name = "The Mines",
		str_desc = "A veritable slime-mine of slime, rejuvinated by the revival of ENDLESS WAR.\n\nExits into Juvie's Row.",
		coord = (34, 18),
		channel = channel_mines,
		role = "Mines",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_juviesrow
	),
	EwPoi( # the-casino
		id_poi = poi_id_thecasino,
		alias = [
			"casino",
			"slimecasino",
			"theslimecasino",
			"tc",  # the casino
			"sc",  # slime casino
			"cas",
			"c"
		],
		str_name = "The Casino",
		str_desc = "The casino is filled with tables and machines for playing games of chance, and garishly decorated wall-to-wall. Lights which normally flash constantly cover everything, but now they all sit unlit.",
		coord = (29, 16),
		channel = channel_casino,
		role = "Casino",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_greenlightdistrict
	),
	EwPoi(  # cratersville mines
		id_poi = poi_id_cv_mines,
		alias = [
			"mines2",
			"cvmines",
			"cmines",
			"cvm",
			"cm",
			"cratersvillemine",
			"cratersvillem"
		],
		str_name = "The Cratersville Mines",
		str_desc = "A veritable slime-mine of slime, rejuvenated by the revival of ENDLESS WAR.\n\nExits into Cratersville.",
		coord = (19, 30),
		channel = channel_cv_mines,
		role = "Cratersville Mines",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_cratersville
	),
	EwPoi(  # toxington mines
		id_poi = poi_id_tt_mines,
		alias = [
			"mines3",
			"ttmines",
			"ttm",
			"toxm",
			"toxingtonmine",
			"toxingtonm"
		],
		str_name = "The Toxington Mines",
		str_desc = "A veritable slime-mine of slime, rejuvinated by the revival of ENDLESS WAR.\n\nExits into Toxington.",
		coord = (9, 2),
		channel = channel_tt_mines,
		role = "Toxington Mines",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_toxington
	),
	EwPoi( # smokers-cough
		id_poi = poi_id_diner,
		alias = [
			"diner",
			"smokers",
			"cough",
			"smc", 
			"wf", #wreckington food
			"rf" #rowdy food
		],
		str_name = "The Smoker's Cough",
		str_desc = "A quaint hole-in-the-wall vintage diner. The wallpaper may be peeling and the ‘80s paint job might be faded, but you’ll be damned if this place didn’t make an aesthetic stomping grounds for cheapskate juveniles like yourself. All the staff know you by name, they’ve memorized your order, and frankly they love you. You’re like a ninth son to the inbred owner and his many, many wives. It’s a cramped space, only fitting about 20 people maximum. The fluorescent lighting from the ceiling lamps invade every nook and cranny of the cyan and purple diner, even when the natural daylight could easily illuminate it just as well. You think you can see some mold on certain corners of the floor. Oh man, so cool.",
		coord = (29, 24),
		channel = channel_diner,
		role = "Smoker's Cough",
		pvp = False,
		vendors = [
			vendor_diner
		],
		is_subzone = True,
		mother_district = poi_id_wreckington
	),
	EwPoi( # Red Mobster
		id_poi = poi_id_seafood,
		alias = [
			"seafood",
			"redmobster",
			"red",
			"mobster",
			"rm",
			"mob",
			"kf" #killer food
		],
		str_name = "Red Mobster Seafood",
		str_desc = "The last bastion of sophistication in this godforsaken city. A dimly lit, atmospheric fine dining restaurant with waiters and tables and archaic stuff like that. Upper crust juveniles and older fugitives make up the majority of the patrons, making you stick out like a sore thumb. Quiet, respectable murmurs pollute the air alongside the scrapping of silverware and the occasional hoity toity laugh. Everything about this place makes you sick.",
		coord = (17, 1),
		channel = channel_seafood,
		role = "Red Mobster Seafood",
		pvp = False,
		vendors = [
			vendor_seafood
		],
		is_subzone = True,
		mother_district = poi_id_astatineheights
	),
	EwPoi( # JR Farm
		id_poi = poi_id_jr_farms,
		alias = [
			"jrf", #juviesrow farms
			"jrp", #juviesrow plantation
			"jrfarms",
			"jrfarm",
			"jrplantation",
			"jrplant",
			"juviesrowf",
			"juviesrowfarm"
		],
		str_name = "The Juvie's Row Farms",
		str_desc = "An array of haphazardly placed farms dot the already dense, crowded areas between mining shaft entrances and impoverished juvenile housing. Pollution is rampant here, with the numerous trash heaps and sludge refineries enjoying the majority of earth under the smoke-smuggered stars. It’s soil is irradiated and barely arable, but it will do. It has to.",
		coord = (32, 20),
		channel = channel_jr_farms,
		role = "Juvie's Row Farms",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_juviesrow
	),
	EwPoi( # OG Farm
		id_poi = poi_id_og_farms,
		alias = [
			"ogf",  # OozeGardens farms
			"ogp",  # OozeGardens plantation
			"ogfarms",
			"ogfarm",
			"ogplantation",
			"ogplant",
			"oozegardenfarms",
			"oozegardenfarm",
			"oozegardensf",
			"oozegardensfarm"
		],
		str_name = "The Ooze Gardens Farms",
		str_desc = "An impressive host of unique and exotic flora are grown here. Originally on private property, the expansive greenhouses were the weekly meeting place for the city’s botanical society. They have since been seized by imminent domain and are now a public park. It’s type of soil is vast and varied depending on where you choose to plant. Surely, anything can grow here.",
		coord = (14, 27),
		channel = channel_og_farms,
		role = "Ooze Gardens Farms",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_oozegardens
	),
	EwPoi( # AB Farm
		id_poi = poi_id_ab_farms,
		alias = [
			"abf", #ArsonBrook farms
			"abp", #ArsonBrook plantation
			"abfarms",
			"abfarm",
			"abplantation",
			"abplant",
			"arsonbrookf",
			"arsonbrookfarm"
		],
		str_name = "The Arsonbrook Farms",
		str_desc = "A series of reedy creeks interspersed with quiet farms and burnt, black trees. It’s overcast skies make the embers from frequent forest fires glow even brighter by comparison. It’s soil is fertile with copious amounts of soot and accompanying nutrients.",
		coord = (21, 1),
		channel = channel_ab_farms,
		role = "Arsonbrook Farms",
		pvp = False,
		is_subzone = True,
		mother_district = poi_id_arsonbrook
	)
]

id_to_poi = {}
coord_to_poi = {}
alias_to_coord = {}
capturable_districts = []

for poi in poi_list:
	if poi.coord != None:
		# Populate the map of coordinates to their point of interest, for looking up from the map.
		coord_to_poi[poi.coord] = poi

		# Populate the map of coordinate aliases to the main coordinate.
		for coord_alias in poi.coord_alias:
			alias_to_coord[coord_alias] = poi.coord

	# Populate the map of point of interest names/aliases to the POI.
	id_to_poi[poi.id_poi] = poi
	for alias in poi.alias:
		id_to_poi[alias] = poi

	# if it's a district and not RR, CK, or JR, add it to a list of capturable districts
	if poi.is_capturable:
		capturable_districts.append(poi.id_poi)

cosmetic_items_list = [
	EwCosmeticItem(
		name = "propeller hat",
		description = "A simple multi-color striped hat with a propeller on top. A staple of every juvenile’s youth.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "mining helmet",
		description = "A typical construction hard hat with a head lamp strapped onto it.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "pickelhaube",
		description = "A traditional Prussian spiked helmet from the nineteenth century.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "fedora",
		description = "A soft brimmed hat with a pinched crown. A classic piece of vintage Americana and a staple of film noir. Not to be confused with the trilby, the fedora is a hat befitting the hardboiled men of it’s time.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "baseball cap",
		description = "A classic baseball cap. A staple of American culture and subsequently freedom from tyranny. If you don’t own at least one of these hats you might as well have hopped the fence from Tijuana last night. Yeah, I’m racist, that going to be a problem for you??",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "backwards baseball cap",
		description = "A classic baseball cap… with an urban twist! Heh, 'sup dawg? Nothing much, man. You know me, just mining some goddamn slime. Word 'n shit. Hell yeah.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "pirate hat",
		description = "A swashbuckling buccaneer’s tricorne, stylized with a jolly roger on the front.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "eyepatch",
		description = "A black eyepatch. A striking accessory for the particularly swashbuckling, chauvinistic, or generally hardboiled of you. Genuine lack of two eyes optional and not recommended.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "cigarette",
		description = "A single cigarette sticking out of your mouth. You huff these things down in seconds but you’re never seen without one. Everyone thinks you’re really, really cool.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "headband",
		description = "A headband wrapped tightly around your forehead with long, flowing ends.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "handkerchief",
		description = "A bandanna tied on your head, creating a simple cap.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "bandanna",
		description = "A handkerchief tied around your neck and covering your lower face.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "sunglasses",
		description = "An iconic pair of black sunglasses. Widely recognized as the coolest thing you can wear.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "glasses",
		description = "A simple pair of eyeglasses. You have perfectly serviceable eyesight, but you are a sucker for the bookworm aesthetic. People with actual issues with sight hate you.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "birthday hat",
		description = "A striped, multi-color birthday hat. ",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "scarf",
		description = "A very thick striped wool scarf, in case 110° degrees is too nippy for you.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "witch hat",
		description = "A pointy, cone-shaped hat with a wide brim. It exudes a spooky essence.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "bomer hat",
		description = "A thick fur and leather aviator’s hat.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "tuxedo",
		description = "A classy, semi-formal suit for dashing rogues you can’t help but love. Instant charisma granted upon each !adorn.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "beanie",
		description = "A simple beanie with a pointed top and a slip stitch brim.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "jester's hat",
		description = "A ridiculous, multi-colored hat with four bells dangling from protruding sleeves.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "3D glasses",
		description = "A pair of totally tubular, ridiculously radical 3D glasses. Straight up stereoscopic, dude!",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "necktie",
		description = "A vintage necktie, reeking of coffee, college, and shaving cream.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "viking helmet",
		description = "A pointy bronze helmet with two sharp horns jutting out of the base.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "flip flops",
		description = "A pair of loud, obnoxious flip flops. The price of your comfort is higher than you could ever know.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "fez",
		description = "A short fez with a tassel attached to the top. Fezzes are cool. Or, are bowties cool? You forget, and frankly you’re embarrassed you remember either one of them.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "bowtie",
		description = "A quite dapper, neatly tied butterfly bowtie. Bowties are cool. Or, are fezzes cool? You forget, and frankly you’re embarrassed you remember either one of them.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "cowboy",
		description = "An essential piece of Wild West memorabilia, a bonafide ten gallon Stetson. Befitting the individualistic individuals that made them famous. Yeehaw, and all that stuff.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "kepi",
		description = "A short kepi with a sunken top and an insignia on the front.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "tam o' shanter'",
		description = "A traditional Scottish wool bonnet with a plaid pattern.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "ushanka",
		description = "A traditional Russian fur cap with thick wool ear flaps.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "karategi",
		description = "A traditional Japanese karateka’s outfiit, complete with a belt with extended ends that easily flow in the wind for dramatic effect.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "turban",
		description = "A traditional Arabian headdress, lavishly decorated with a single large jewel and protruding peacock feather.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "nemes",
		description = "The traditional ancient Egyptian pharaoh's striped head cloth.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "varsity jacket",
		description = "An American baseball jacket, with a large insignia on the left side of the chest.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "sombrero",
		description = "A traditional Mexican sombrero, with an extra-wide brim to protect you from the blistering Arizonian sun.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "hawaiian shirt",
		description = "A brightly colored Hawaiian shirt with a floral pattern. It reeks of slima colada and the complementary shampoo from Assault Flats Beach Resort.",
		rarity = rarity_plebeian
	),
	EwCosmeticItem(
		name = "fursuit",
		description = "A fursuit. Custom-made and complete with high quality faux fur, padded digitigrade legs, follow-me eyes, adjustable facial expressions, and a fan in the head. It is modeled off your original character, also known as your fursona. Some would call it’s character design “ugly” or “embarrassing,” but you think it’s perfect.",
		rarity = rarity_patrician
	),
	EwCosmeticItem(
		name = "diadem",
		description = "The traditional Greco-Roman laurel wreath symbolizing sovereignty and power. Be careful about wearing this around in public, you might just wake up with 23 stab wounds.",
		rarity = rarity_patrician
	),
	EwCosmeticItem(
		name = "Bill's Hat",
		description = "A military beret with a shield insignia on the front.",
		rarity = rarity_patrician
	),
	EwCosmeticItem(
		name = "wedding ring",
		description = "A silver ring with a decently large diamond on top. For the person you love most in the entire world. <3",
		rarity = rarity_patrician
	),
	EwCosmeticItem(
		name = "earbuds",
		description = "A pair of white standard iPod earbuds. Who knows what sort of tasty jams you must be listening to while walking down the street?",
		rarity = rarity_patrician
	)
]

# Slimeoid attributes.

# All body attributes in the game.
body_list = [
	EwBody( # body 1
		id_body = "teardrop",
		alias = [
			"tear",
			"drop",
			"oblong",
			"a"
		],
		str_create = "You press a button on the body console labelled 'A'. Through the observation port, you see the rapidly congealing proto-Slimeoid take on a roughly teardrop-shaped form.",
		str_body = "It is teardrop-shaped.",
		str_observe = "{slimeoid_name} is bobbing its top-heavy body back and forth."
	),
	EwBody( # body 2
		id_body = "wormlike",
		alias = [
			"long",
			"serpent",
			"serpentine",
			"b"
		],
		str_create = "You press a button on the body console labelled 'B'. Through the observation port, you see the rapidly congealing proto-Slimeoid begin to stretch into an elongated form.",
		str_body = "It is long and wormlike.",
		str_observe = "{slimeoid_name} is twisting itself around, practicing tying its knots."
	),
	EwBody( # body 3
		id_body = "spherical",
		alias = [
			"sphere",
			"orb",
			"ball",
			"c"
		],
		str_create = "You press a button on the body console labelled 'C'. Through the observation port, you see the rapidly congealing proto-Slimeoid take on a roughly spherical form.",
		str_body = "It is generally orb-shaped.",
		str_observe = "{slimeoid_name} flops over onto one side of its round body."
	),
	EwBody( # body 4
		id_body = "humanoid",
		alias = [
			"biped",
			"human",
			"d"
		],
		str_create = "You press a button on the body console labelled 'D'. Through the observation port, you see the rapidly congealing proto-Slimeoid curl into a foetal, vaguely humanoid form.",
		str_body = "It is vaguely humanoid.",
		str_observe = "{slimeoid_name} is scraping at something on the ground with its arms."
	),
	EwBody( # body 5
		id_body = "tentacled",
		alias = [
			"squid",
			"squidlike",
			"tentacle",
			"tentacles",
			"e"
		],
		str_create = "You press a button on the body console labelled 'E'. Through the observation port, you see the rapidly congealing proto-Slimeoid begin to sprout long tendrils from its nucleus.",
		str_body = "It is a mass of tendrils.",
		str_observe = "{slimeoid_name} is moving its tentacles around, running them over one another."
	),
	EwBody( # body 6
		id_body = "amorphous",
		alias = [
			"none",
			"formless",
			"f"
		],
		str_create = "You press a button on the body console labelled 'F'. Through the observation port, you see the rapidly congealing proto-Slimeoid accreting itself together with no distinct shape to speak of.",
		str_body = "It has no defined shape.",
		str_observe = "{slimeoid_name}'s body is spread out on the floor like a kind of living puddle."
	),
	EwBody( # body 7
		id_body = "quadruped",
		alias = [
			"animal",
			"g"
		],
		str_create = "You press a button on the body console labelled 'G'. Through the observation port, you see the rapidly congealing proto-Slimeoid beginning to grow bones and vertebrae as it starts to resemble some kind of quadruped.",
		str_body = "It has a body shape vaguely reminiscent of a quadruped.",
		str_observe = "{slimeoid_name} has its hindquarters lowered in a sort of sitting position."
	)
]

# A map of id_body to EwBody objects.
body_map = {}

# A list of body names
body_names = []

# Populate body map, including all aliases.
for body in body_list:
	body_map[body.id_body] = body
	body_names.append(body.id_body)

	for alias in body.alias:
		body_map[alias] = body

# All head attributes in the game.
head_list = [
	EwHead( # head 1
		id_head = "eye",
		alias = [
			"cyclops",
			"a"
		],
		str_create = "You press a button on the head console labelled 'A'. Through the observation port, you see a dark cluster within the proto-Slimeoid begin to form into what looks like a large eye.",
		str_head = "Its face is a single huge eye.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name}'s huge eye follows the ball's arc, and it makes a leap to catch it!!\n\n...only to get socked right in the eye, sending it to the floor in pain. Depth perception... it's truly a gift."
	),
	EwHead( # head 2
		id_head = "maw",
		alias = [
			"mouth",
			"b"
		],
		str_create = "You press a button on the head console labelled 'B'. Through the observation port, you see an opening form in what you think is the proto-Slimeoid's face, which begins to sprout large pointed teeth.",
		str_head = "Its face is a huge toothy mouth.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} slavers and drools as it awaits the throw, and when it sees the ball start to fly, it lunges to grab it out of the air in its huge toothy maw, slicing it to shreds with its teeth in seconds."
	),
	EwHead( # head 3
		id_head = "void",
		alias = [
			"hole",
			"c"
		],
		str_create = "You press a button on the head console labelled 'C'. Through the observation port, you see what you thought was the proto-Slimeoid's face suddenly sucked down into its body, as though by a black hole.",
		str_head = "Its face is an empty black void.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} positions itself to catch the ball in it's... face? The ball falls into the empty void of {slimeoid_name}'s face, then just keeps falling, falling, falling, down into the depths, falling so far it dissapears forever."
	),
	EwHead( # head 4
		id_head = "beast",
		alias = [
			"animal",
			"dragon",
			"d"
		],
		str_create = "You press a button on the head console labelled 'D'. Through the observation port, you see the beginnings of an animal-like face forming on your proto-Slimeoid, with what might be eyes, a nose, teeth... maybe.",
		str_head = "Its face is that of a vicious beast.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} focuses its eyes and bares its teeth, then makes a flying leap, snapping the ball clean out of the air in its jaws! It comes back to you and drops the ball at your feet. Good boy!"
	),
	EwHead( # head 5
		id_head = "insect",
		alias = [
			"bug",
			"insectoid",
			"e"
		],
		str_create = "You press a button on the head console labelled 'E'. Through the observation port, you see the proto-Slimeoid suddenly bulge with a series of hard orbs which congeal into what appear to be large compound eyes.",
		str_head = "It has bulging insectoid eyes and mandibles.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} stands motionless, presumably watching the ball with its large compound eyes, before darting toward it as it sails through the air, snapping its mandibles around the ball and slicing it cleanly in two."
	),
	EwHead( # head 6
		id_head = "skull",
		alias = [
			"skeleton",
			"f"
		],
		str_create = "You press a button on the head console labelled 'F'. Through the observation port, you see the proto-Slimeoid's frontal features twist into a ghastly death's-head.",
		str_head = "Its face resembles a skull.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} moves as quickly as it can to make the catch, making it just before the ball lands! With a thunk, the ball lodges itself in {slimeoid_name}'s open eye socket. {slimeoid_name} yanks it out and tosses the ball back to you. Euughh."
	),
	EwHead( # head 7
		id_head = "none",
		alias = [
			"g"
		],
		str_create = "You press a button on the head console labelled 'G'. Through the observation port, you see the proto-Slimeoid's front end melt into an indistinct mass.",
		str_head = "It has no discernable head.",
		str_feed = "",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} moves under the ball as it flies through the air, but makes no attempt to catch it in its mouth on account of having none. The ball lands next to {slimeoid_name}, who merely looks on. Actually, you can't tell where it's looking."
	)
]

# A map of id_head to EwBody objects.
head_map = {}

# A list of head names
head_names = []

# Populate head map, including all aliases.
for head in head_list:
	head_map[head.id_head] = head
	head_names.append(head.id_head)

	for alias in head.alias:
		head_map[alias] = head

# All mobility attributes in the game.
mobility_list = [
	EwMobility( # mobility 1
		id_mobility = "legs",
		alias = [
			"animal",
			"quadruped",
			"biped",
			"jointed",
			"limbs",
			"a"
		],
		str_advance = "{active} barrels toward {inactive}!",
		str_retreat = "{active} leaps away from {inactive}!",
		str_advance_weak = "{active} limps toward {inactive}!",
		str_retreat_weak = "{active} limps away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'A'. Through the observation port, you see jointed limbs begin to sprout from the proto-Slimeoid's underside.",
		str_mobility = "It walks on legs.",
		str_defeat = "{slimeoid_name}'s knees buckle under it as it collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} walks along beside you."
	),
	EwMobility( # mobility 2
		id_mobility = "rolling",
		alias = [
			"roll",
			"b"
		],
		str_advance = "{active} rolls itself toward {inactive}!",
		str_retreat = "{active} rolls away from {inactive}!",
		str_advance_weak = "{active} rolls itself unsteadily towards {inactive}!",
		str_retreat_weak = "{active} rolls unsteadily away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'B'. Through the observation port, you see the proto-Slimeoid becoming smoother and rounder.",
		str_mobility = "It moves by rolling its body around.",
		str_defeat = "{slimeoid_name} rolls itself over before collapsing on the ground, defeated!",
		str_walk = "{slimeoid_name} rolls itself along the ground behind you."
	),
	EwMobility( # mobility 3
		id_mobility = "flagella",
		alias = [
			"flagella",
			"tendrils",
			"tentacles",
			"c"
		],
		str_advance = "{active} slithers toward {inactive}!",
		str_retreat = "{active} slithers away from {inactive}!",
		str_advance_weak = "{active} drags itself toward {inactive}!",
		str_retreat_weak = "{active} drags itself away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'C'. Through the observation port, you see masses of writhing flagella begin to protrude from the proto-Slimeoid's extremities.",
		str_mobility = "It moves by pulling itself around with its flagella.",
		str_defeat = "{slimeoid_name}'s flagella go limp as it collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} writhes its way along the ground on its flagella next to you."
	),
	EwMobility( # mobility 4
		id_mobility = "jets",
		alias = [
			"fluid",
			"jet",
			"d"
		],
		str_advance = "{active} propels itself toward {inactive}!",
		str_retreat = "{active} propels itself away from {inactive}!",
		str_advance_weak = "{active} sputters towards {inactive}!",
		str_retreat_weak = "{active} sputters away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'D'. Through the observation port, you see openings forming in the proto-Slimeoid's body, which begin to vent fluid.",
		str_mobility = "It moves via jet-propulsion by squirting fluids.",
		str_defeat = "{slimeoid_name} fires its fluid jets wildly in a panic until it completely deflates and collapses, defeated!",
		str_walk = "{slimeoid_name} tries to keep pace with you, spurting jets of fluid to propel itself along behind you."
	),
	EwMobility( # mobility 5
		id_mobility = "slug",
		alias = [
			"undulate",
			"e"
		],
		str_advance = "{active} undulates its way toward {inactive}!",
		str_retreat = "{active} undulates itself away from {inactive}!",
		str_advance_weak = "{active} heaves itself slowly toward {inactive}!",
		str_retreat_weak = "{active} heaves itself slowly away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'E'. Through the observation port, you see the base of the proto-Slimeoid's body widen and flatten out.",
		str_mobility = "It moves like a slug, undulating its underside along the ground.",
		str_defeat = "{slimeoid_name} stops moving entirely and collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} glacially drags its way along behind you in its slug-like way. Your walk ends up taking fucking forever."
	),
	EwMobility( # mobility 5
		id_mobility = "float",
		alias = [
			"gas",
			"f"
		],
		str_advance = "{active} floats toward {inactive}!",
		str_retreat = "{active} floats away from {inactive}!",
		str_advance_weak = "{active} bobs unsteadily through the air towards {inactive}!",
		str_retreat_weak = "{active} bobs unsteadily away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'F'. Through the observation port, you see the of the proto-Slimeoid's body start to inflate itself.",
		str_mobility = "It floats in the air with the use of super-low-density gas bladders.",
		str_defeat = "{slimeoid_name} spins wildly in the air before careening to the ground, defeated!",
		str_walk = "{slimeoid_name} bobs along next to you on its leash like a balloon."
	),
	EwMobility( # mobility 5
		id_mobility = "wings",
		alias = [
			"fly",
			"g"
		],
		str_advance = "{active} darts through the air toward {inactive}!",
		str_retreat = "{active} flaps away from {inactive}!",
		str_advance_weak = "{active} flaps its way doggedly towards {inactive}!",
		str_retreat_weak = "{active} flaps doggedly away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'G'. Through the observation port, you see the proto-slimeoid start to sprout wide, flat, thin appendages.",
		str_mobility = "It moves by making short flights through the air with its wings.",
		str_defeat = "{slimeoid_name} flaps helplessly as it spins out and crashes into the ground, defeated!",
		str_walk = "{slimeoid_name} flaps along through the air next to you, occasionally perching in trees or windowsills along the route."
	)
]

# A map of id_mobility to EwBody objects.
mobility_map = {}

# A list of mobility names
mobility_names = []

# Populate mobility map, including all aliases.
for mobility in mobility_list:
	mobility_map[mobility.id_mobility] = mobility
	mobility_names.append(mobility.id_mobility)

	for alias in mobility.alias:
		mobility_map[alias] = mobility

# All offense attributes in the game.
offense_list = [
	EwOffense( # offense 1
		id_offense = "blades",
		alias = [
			"edged",
			"edges",
			"edgy",
			"bladed",
			"blade",
			"a"
		],
		str_attack = "{active} slashes {inactive} with its blades!",
		str_attack_weak = "{active} desperately swipes at {inactive} with its blades!",
		str_attack_coup = "{active} slices deep into {inactive}! Green goo splatters onto the ground from the wound!!",
		str_create = "You press a button on the weapon console labelled 'A'. Through the observation port, you see long, sharp protrusions begin to form on the proto-Slimeoid's extremities.",
		str_offense = "It slices foes with retractible blades.",
		str_observe = "{slimeoid_name} is sharpening its retractible blades on a stone nearby."
	),
	EwOffense( # offense 2
		id_offense = "teeth",
		alias = [
			"bite",
			"biting",
			"crunch",
			"crunching",
			"b"
		],
		str_attack = "{active} sinks its teeth into {inactive}!",
		str_attack_weak = "{active} gnashes its teeth, biting {inactive} wherever it can!",
		str_attack_coup = "{active} bites hard into {inactive}, tearing off a piece and chewing it hungrily!",
		str_create = "You press a button on the weapon console labelled 'B'. Through the observation port, you see large bony structures resembling teeth forming in the proto-Slimeoid's... mouth?",
		str_offense = "It can bite foes with deadly fangs.",
		str_observe = "{slimeoid_name} is idly picking its sharp teeth."
	),
	EwOffense( # offense 3
		id_offense = "grip",
		alias = [
			"squeeze",
			"grab",
			"squeezing",
			"grabbing",
			"gripping",
			"constrict",
			"constriction",
			"c"
		],
		str_attack = "{active} grabs {inactive} and squeezes hard!",
		str_attack_weak = "{active} grabs at {inactive}, trying to fend it off!",
		str_attack_coup = "{active} grips {inactive} like a vice, squeezing until you hear a sickening pop!",
		str_create = "You press a button on the weapon console labelled 'C'. Through the observation port, you see the proto-Slimeoid's limbs becoming thicker and stronger, beginning to twist and writhe, seeking something to grip onto.",
		str_offense = "It can grab and crush its foes with its limbs.",
		str_observe = "{slimeoid_name} picks up a rock off the ground and squeezes it like a stress ball."
	),
	EwOffense( # offense 4
		id_offense = "bludgeon",
		alias = [
			"strike",
			"striking",
			"smash",
			"smashing",
			"bash",
			"bashing",
			"crush",
			"crushing",
			"d"
		],
		str_attack = "{active} bashes {inactive} with its limbs!",
		str_attack_weak = "{active} flails its limbs to strike back at {inactive}!",
		str_attack_coup = "{active} winds back and smashes {inactive}, dealing a knockout blow!",
		str_create = "You press a button on the weapon console labelled 'D'. Through the observation port, you see the ends of the proto-Slimeoid's limbs becoming harder and heavier.",
		str_offense = "It can smash foes with one or more of its limbs.",
		str_observe = "{slimeoid_name} spots an insect on the ground nearby and smashes it."
	),
	EwOffense( # offense 5
		id_offense = "spikes",
		alias = [
			"puncture",
			"spear",
			"e"
		],
		str_attack = "{active} skewers {inactive} with its spikes!",
		str_attack_weak = "{active} tries to defend itself from {inactive} with its spikes!",
		str_attack_coup = "{active} punctures {inactive} with its spikes, opening a hole that oozes green fluid all over the ground!",
		str_create = "You press a button on the weapon console labelled 'E'. Through the observation port, you see hard spikes forming out of the congealing slime biomatter.",
		str_offense = "It can puncture its enemies with the spikes on its body.",
		str_observe = "{slimeoid_name} carefully adjusts its position so as not to prick itself with its own spikes."
	),
	EwOffense( # offense 6
		id_offense = "electricity",
		alias = [
			"strike",
			"f"
		],
		str_attack = "{active} unleashes a pent-up electrical discharge into {inactive}!",
		str_attack_weak = "{active} sparks and flickers with electricity, shocking {inactive}!",
		str_attack_coup = "{active} charges up and sends a bolt of electricity through {inactive}, making it sizzle!",
		str_create = "You press a button on the weapon console labelled 'F'. Through the observation port, you see the proto-Slimeoid begin to spark with small electrical discharges.",
		str_offense = "It crackles with stored electrical energy.",
		str_observe = "A fly flies a little too near {slimeoid_name} and is zapped with a tiny bolt of electricity, killing it instantly."
	),
	EwOffense( # offense 7
		id_offense = "slam",
		alias = [
			"bodyslam",
			"g"
		],
		str_attack = "{active} slams its entire body into {inactive}!",
		str_attack_weak = "{active} flails itself back against {inactive}'s onslaught!",
		str_attack_coup = "{active} hurls its whole weight into {inactive}, crushing it to the ground!",
		str_create = "You press a button on the weapon console labelled 'G'. Through the observation port, you see the ends of the proto-Slimeoid's congealing body condense, becoming heavier and more robust.",
		str_offense = "It can slam its body into its foes with tremendous force.",
		str_observe = "{slimeoid_name} shifts its weight back and forth before settling down in a kind of sumo-squat position."
	)
]

# A map of id_offense to EwBody objects.
offense_map = {}

# A list of offense names
offense_names = []

# Populate offense map, including all aliases.
for offense in offense_list:
	offense_map[offense.id_offense] = offense
	offense_names.append(offense.id_offense)

	for alias in offense.alias:
		offense_map[alias] = offense

# All defense attributes in the game.
defense_list = [
	EwDefense( # defense 1
		id_defense = "scales",
		alias = [
			"scale",
			"scaled",
			"scaly",
			"a"
		],
		str_defense = "",
		str_pet = "You carefully run your hand over {slimeoid_name}'s hide, making sure to go with the grain so as not to slice your fingers open on its sharp scales.",
		str_create = "You press a button on the armor console labelled 'A'. Through the observation port, you see the proto-Slimeoid's skin begin to glint as it sprouts roughly-edged scales.",
		str_armor = "It is covered in scales."
	),
	EwDefense( # defense 2
		id_defense = "boneplates",
		alias = [
			"bone",
			"bony",
			"bones",
			"plate",
			"plates",
			"armor",
			"plating",
			"b"
		],
		str_defense = "",
		str_pet = "You pat one of the hard, bony plates covering {slimeoid_name}'s skin.",
		str_create = "You press a button on the armor console labelled 'B'. Through the observation port, you see hard bony plates begin to congeal on the proto-Slimeoid's surface.",
		str_armor = "It is covered in bony plates."
	),
	EwDefense( # defense 3
		id_defense = "quantumfield",
		alias = [
			"quantum",
			"field",
			"energy",
			"c"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, and your hand tingles as it passes through the quantum field that surrounds its body.",
		str_create = "You press a button on the armor console labelled 'C'. Through the observation port, start to notice the proto-Slimeoid begin to flicker, and you hear a strange humming sound.",
		str_armor = "It is enveloped in a field of quantum uncertainty."
	),
	EwDefense( # defense 4
		id_defense = "formless",
		alias = [
			"amorphous",
			"shapeless",
			"squishy",
			"d"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, its fluid, shapeless body squishing and deforming in response to even slight pressure.",
		str_create = "You press a button on the armor console labelled 'D'. Through the observation port, you see the proto-Slimeoid suddenly begin to twist itself, stretching and contracting as its shape rapidly shifts.",
		str_armor = "It is malleable and can absorb blows with ease."
	),
	EwDefense( # defense 5
		id_defense = "regeneration",
		alias = [
			"healing",
			"regen",
			"e"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}. Its skin is hot, and you can feel it pulsing rhythmically.",
		str_create = "You press a button on the armor console labelled 'E'. Through the observation port, you see the proto-Slimeoid begin to pulse, almost like a beating heart.",
		str_armor = "It can regenerate damage to its body rapidly."
	),
	EwDefense( # defense 6
		id_defense = "stench",
		alias = [
			"stink",
			"smell",
			"f"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, taking care not to inhale through your nose, as one whiff of its odor has been known to make people lose their lunch.",
		str_create = "You press a button on the armor console labelled 'F'. Through the observation port, you see the proto-Slimeoid suddenly begin to twist itself, stretching and contracting as its shape rapidly shifts.",
		str_armor = "It exudes a horrible stench."
	),
	EwDefense( # defense 7
		id_defense = "oil",
		alias = [
			"slick",
			"g"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}'s slick wet skin, and your hand comes away coated in a viscous, slippery oil.",
		str_create = "You press a button on the armor console labelled 'G'. Through the observation port, you see the surface of the proto-Slimeoid become shiny with some kind of oily fluid.",
		str_armor = "It is covered in a coating of slippery oil."
	)
]

# A map of id_defense to EwBody objects.
defense_map = {}

# A list of defense names
defense_names = []

# Populate defense map, including all aliases.
for defense in defense_list:
	defense_map[defense.id_defense] = defense
	defense_names.append(defense.id_defense)

	for alias in defense.alias:
		defense_map[alias] = defense

# All special attributes in the game.
special_list = [
	EwSpecial( # special 1
		id_special = "spit",
		alias = [
			"spitting",
			"spray",
			"squirt",
			"spraying",
			"squirting",
			"liquid",
			"fluid",
			"acid",
			"acidic",
			"toxic",
			"poison",
			"a"
		],
		str_special_attack = "{active} spits acidic ooze onto {inactive}!",
		str_special_attack_weak = "{active} coughs and spurts up a sputtering spray of acid at {inactive}!",
		str_special_attack_coup = "{active} vomits a torrent of acid onto {inactive}, deteriorating it to the point that it can no longer fight!",
		str_create = "You press a button on the special attack console labelled 'A'. Through the observation port, you see the proto-Slimeoid's body begin to excrete a foul, toxic ooze.",
		str_special = "It can spit acidic ooze.",
		str_observe = "A bit of acidic fluid drips from {slimeoid_name} onto the ground, where it smokes and sizzles."
	),
	EwSpecial( # special 2
		id_special = "laser",
		alias = [
			"beam",
			"energy",
			"radiation",
			"b"
		],
		str_special_attack = "{active} sears {inactive} with a blast of radiation!",
		str_special_attack_weak = "{active} starts to flicker before firing an unsteady beam of light at {inactive}!",
		str_special_attack_coup = "{active} blasts {inactive} with a beam of green energy, searing it all over its body!",
		str_create = "You press a button on the special attack console labelled 'B'. Through the observation port, you see the proto-Slimeoid's body begin to glow with energy as the gestation vat's built-in Geiger Counter begins to click frantically.",
		str_special = "It can fire beams of radiation.",
		str_observe = "{slimeoid_name} suddenly glows with radioactive energy. Best not to look directly at it until it settles down..."
	),
	EwSpecial( # special 3
		id_special = "spines",
		alias = [
			"spikes",
			"spiky",
			"spiny",
			"quills",
			"c"
		],
		str_special_attack = "{active} fires a volley of quills into {inactive}!",
		str_special_attack_weak = "{active} desperately fires a few of its last quills into {inactive}!",
		str_special_attack_coup = "{active} fires a rapid burst of sharp quills into {inactive}, filling it like a pincushion!",
		str_create = "You press a button on the special attack console labelled 'C'. Through the observation port, you see the proto-Slimeoid's congealing body suddenly protruding with long, pointed spines, which quickly retract back into it.",
		str_special = "It can fire sharp quills.",
		str_observe = "{slimeoid_name} shudders and ejects a few old quills onto the ground. You can see new ones already growing in to replace them."
	),
	EwSpecial( # special 4
		id_special = "throw",
		alias = [
			"throwing",
			"hurling",
			"hurl",
			"d"
		],
		str_special_attack = "{active} picks up a nearby {object} and hurls it into {inactive}!",
		str_special_attack_weak = "{active} unsteadily hefts a nearby {object} before throwing it into {inactive}!",
		str_special_attack_coup = "{active} hurls a {object}, which smashes square into {inactive}, knocking it to the ground! A direct hit!",
		str_create = "You press a button on the special attack console labelled 'D'. Through the observation port, you see the proto-Slimeoid's limbs become more articulate.",
		str_special = "It can hurl objects at foes.",
		str_observe = "{slimeoid_name} is idly picking up stones and seeing how far it can toss them."
	),
	EwSpecial( # special 5
		id_special = "TK",
		alias = [
			"telekinesis",
			"psychic",
			"e"
		],
		str_special_attack = "{active} focuses on {inactive}... {inactive} convulses in pain!",
		str_special_attack_weak = "{active}'s cranium bulges and throbs! {inactive} convulses!",
		str_special_attack_coup = "{active} emanates a strange static sound as {inactive} is inexplicably rendered completely unconscious!",
		str_create = "You press a button on the special attack console labelled 'E'. You momentarily experience an uncomfortable sensation, sort of like the feeling you get when you know there's a TV on in the room even though you can't see it.",
		str_special = "It can generate harmful frequencies with its brainwaves.",
		str_observe = "You momentarily black out. When you come to, your nose is bleeding. {slimeoid_name} tries to look innocent."
	),
	EwSpecial( # special 6
		id_special = "fire",
		alias = [
			"chemical",
			"breath",
			"breathe",
			"f"
		],
		str_special_attack = "{active} ejects a stream of fluid which ignites in the air, burning {inactive}!",
		str_special_attack_weak = "{active} fires an unsteady, sputtering stream of fluid that ignites and singes {inactive}!",
		str_special_attack_coup = "{active} empties its fluid bladders in a final burst of liquid! {inactive} is completely engulfed in the conflagration!",
		str_create = "You press a button on the special attack console labelled 'F'. Through the observation port, you see fluid bladders forming deep under the still-forming proto-Slimeoid's translucent skin.",
		str_special = "It can fire a stream of pyrophoric fluid at its foes.",
		str_observe = "A bit of fluid drips from {slimeoid_name} onto the floor and ignites, but you manage to smother the small flame quickly before it spreads."
	),
	EwSpecial( # special 7
		id_special = "webs",
		alias = [
			"webbing",
			"web",
			"g"
		],
		str_special_attack = "{active} fires a stream of sticky webbing onto {inactive}!",
		str_special_attack_weak = "{active} is running out of webbing! It shoots as much as it can onto {inactive}!",
		str_special_attack_coup = "{active} gathers itself up before spurting a blast of webbing that coats {inactive}'s body, completely ensnaring it!",
		str_create = "You press a button on the special attack console labelled 'G'. Through the observation port, you see large glands forming near the surface of the still-forming proto-Slimeoid's translucent skin.",
		str_special = "It can spin webs and shoot webbing fluid to capture prey.",
		str_observe = "{slimeoid_name} is over in the corner, building itself a web to catch prey in."
	)
]

# A map of id_special to EwBody objects.
special_map = {}

# A list of special names
special_names = []

# Populate special map, including all aliases.
for special in special_list:
	special_map[special.id_special] = special
	special_names.append(special.id_special)

	for alias in special.alias:
		special_map[alias] = special

# All brain attributes in the game.
brain_list = [
	EwBrain( # brain 1
		id_brain = "a",
		alias = [
			"typea",
			"type a"
		],
		str_create = "You press a button on the brain console labelled 'A'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to move, thrashing about as if in frustration.",
		str_brain = "It is extremely irritable.",
		str_observe = "{slimeoid_name} is snarling. You're not sure if it's angry at you, or at the world in general.",
		str_pet = "{slimeoid_name} hisses at you.",
		str_walk = "You wrestle {slimeoid_name} down and force a leash onto it, as it angrily snarls and hisses at you in protest.",
		str_kill = "{slimeoid_name} howls with savage delight at the bloodshed!!",
		str_death = "{slimeoid_name} howls in fury at its master's death! It tears away in a blind rage!",
		str_victory = "{slimeoid_name} roars in triumph!!",
		str_battlecry = "{slimeoid_name} roars with bloodlust!! ",
		str_battlecry_weak = "{slimeoid_name} is too breathless to roar, but is still filled with bloodlust!! ",
		str_movecry = "{slimeoid_name} snarls at its prey! " ,
		str_movecry_weak = "{slimeoid_name}  hisses with frustrated rage! ",
		str_revive = "{slimeoid_name} howls at your return, annoyed to have been kept waiting.",
		str_spawn = "{slimeoid_name} shakes itself off to get rid of some excess gestation fluid, then starts to hiss at you. Seems like a real firecracker, this one.",
		str_dissolve = "{slimeoid_name} hisses and spits with fury as you hold it over the SlimeCorp Dissolution Vats. Come on, get in there...\n{slimeoid_name} claws at you, clutching at the edge of the vat, screeching with rage even as you hold its head under the surface and wait for the chemical soup to do its work. At last, it stops fighting.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 2
		id_brain = "b",
		alias = [
			"typeb",
			"type b"
		],
		str_create = "You press a button on the brain console labelled 'B'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to move about its gestation tank, exploring its surroundings.",
		str_brain = "It is enthusiastic about almost everything.",
		str_observe = "{slimeoid_name} notices you looking at it and seems delighted!",
		str_pet = "{slimeoid_name} purrs happily.",
		str_walk = "{slimeoid_name} is so excited for its walk, it can barely hold still enough to let you put the leash on it!",
		str_kill = "{slimeoid_name} gives a bestial woop of excitement for your victory!",
		str_death = "{slimeoid_name} gives a wail of grief at its master's death, streaking away from the scene.",
		str_victory = "{slimeoid_name} woops with delight at its victory!",
		str_battlecry = "{slimeoid_name} lets out a loud war woop! " ,
		str_battlecry_weak = "{slimeoid_name} is determined not to lose! ",
		str_movecry = "{slimeoid_name} is thrilled by the battle! " ,
		str_movecry_weak = "{slimeoid_name} seems a little less thrilled now... ",
		str_revive = "{slimeoid_name} is waiting patiently downtown when you return from your time as a corpse. It knew you'd be back!",
		str_spawn = "{slimeoid_name} gets up off the ground slowly at first, but then it notices you and leaps into your arms. It sure seems glad to see you!",
		str_dissolve = "You order {slimeoid_name} into the Dissolution Vats. It's initially confused, but realization of what you're asking slowly crawks across its features.\nIt doesn't want to go, but after enough stern commanding, it finally pitches itself into the toxic sludge, seemingly too heartbroken to fear death.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 3
		id_brain = "c",
		alias = [
			"typec",
			"type c"
		],
		str_create = "You press a button on the brain console labelled 'C'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid draws its congealing body together, as if trying to gather its strength.",
		str_brain = "It is quiet and withdrawn.",
		str_observe = "{slimeoid_name} seems to be resting, possibly deep in thought.",
		str_pet = "{slimeoid_name} doesn't react.",
		str_walk = "{slimeoid_name} holds still as you place the leash on it. It regards the leash, seemingly pontificating.",
		str_kill = "{slimeoid_name} regards the corpse of your former adversary with an unknowable expression.",
		str_death = "{slimeoid_name} stares at the killer, memorizing their face before fleeing the scene.",
		str_victory = "{slimeoid_name} silently turns away from its defeated opponent.",
		str_battlecry = "{slimeoid_name} carefully regards its opponent. ",
		str_battlecry_weak = "{slimeoid_name} tries to steady itself. ",
		str_movecry = "{slimeoid_name} seems to be getting impatient. " ,
		str_movecry_weak = "{slimeoid_name} is losing its composure just a little! ",
		str_revive = "{slimeoid_name} is downtown when you return from the sewers. You find it staring silently up at ENDLESS WAR.",
		str_spawn = "{slimeoid_name} regards you silently from the floor. You can't tell if it likes you or not, but it starts to follow you regardless.",
		str_dissolve = "You pick up {slimeoid_name} and hurl it into the SlimeCorp Dissolution Vats before it starts to suspect anything. It slowly sinks into the chemical soup, kind of like Arnold at the end of Terminator 2, only instead of giving you a thumbs-up, it stares at you with an unreadable expression. Betrayal? Confusion? Hatred? Yeah, probably.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 4
		id_brain = "d",
		alias = [
			"typed",
			"type d"
		],
		str_create = "You press a button on the brain console labelled 'D'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid lazily turns over in its gestation vat, floating and doing little else.",
		str_brain = "It is usually staring off into space.",
		str_observe = "{slimeoid_name} stares off into the distance. Who knows if it's actually looking at anything in particular.",
		str_pet = "{slimeoid_name} is startled out of a stupor by your touch.",
		str_walk = "{slimeoid_name} hardly seems to notice you fastening it with a leash.",
		str_kill = "{slimeoid_name} wasn't paying attention and missed the action.",
		str_death = "{slimeoid_name} is startled to realize its master has died. It blinks in confusion before fleeing.",
		str_victory = "{slimeoid_name} keeps attacking for a moment before realizing it's already won.",
		str_battlecry = "{slimeoid_name} is weighing its options! ",
		str_battlecry_weak = "{slimeoid_name} is desperately trying to come up with a plan! ",
		str_movecry = "{slimeoid_name} Isn't really feeling this. " ,
		str_movecry_weak = "{slimeoid_name} tries to buy itself some time to think! ",
		str_revive = "{slimeoid_name} is exactly where you left it when you died.",
		str_spawn = "{slimeoid_name} flops over on the floor and stares up at you. Its gaze wanders around the room for a while before it finally picks itself up to follow you.",
		str_dissolve = "You lead {slimeoid_name} up to the edge of the Dissolution Vats and give a quick 'Hey, look, a distraction!'. {slimeoid_name} is immediately distracted and you shove it over the edge. Landing in the vat with a sickening *gloop* sound, it sinks quickly under the fluid surface, flailing madly in confusion and desperation.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 5
		id_brain = "e",
		alias = [
			"typee",
			"type e"
		],
		str_create = "You press a button on the brain console labelled 'E'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid starts to sporadically twitch and shiver.",
		str_brain = "It is extremely skittish and jumpy.",
		str_observe = "{slimeoid_name} is glancing around furtively, seemingly scanning for threats.",
		str_pet = "{slimeoid_name} flinches nervously at your touch.",
		str_walk = "{slimeoid_name} shivers in place as you're fastening the leash, then starts to pull and tug at it, seemingly perturbed.",
		str_kill = "{slimeoid_name} peers out from behind its master, hoping the violence is over.",
		str_death = "{slimeoid_name} is overcome with terror, skittering away from the killer in a mad panic!",
		str_victory = "{slimeoid_name} is deeply relieved that the battle is over.",
		str_battlecry = "{slimeoid_name} chitters fearfully! ",
		str_battlecry_weak = "{slimeoid_name} squeals in abject terror! ",
		str_movecry = "{slimeoid_name} makes a break for it! " ,
		str_movecry_weak = "{slimeoid_name} is in a full-blown panic! ",
		str_revive = "{slimeoid_name} peeks out from behind some trash cans before rejoining you. It seems relieved to have you back.",
		str_spawn = "{slimeoid_name}'s eyes dart frantically around the room. Seeing you, it darts behind you, as if for cover from an unknown threat.",
		str_dissolve = "{slimeoid_name} is looking around the lab nervously, obviously unnerved by the Slimeoid technology. Its preoccupation makes it all too easy to lead it to the Dissolution Vats and kick its legs out from under it, knocking it in. As it falls and hits the solvent chemicals, it wails and screeches in shock and terror, but the noise eventually quiets as it dissolves into a soft lump, then disintegrates altogether.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 6
		id_brain = "f",
		alias = [
			"typef",
			"type f"
		],
		str_create = "You press a button on the brain console labelled 'F'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid darts to the opposite side of the gestation vat. You're not sure, but you feel like it's watching you.",
		str_brain = "It acts secretive, as though it's up to something.",
		str_observe = "{slimeoid_name} is moving around, apparently searching for... something.",
		str_pet = "{slimeoid_name} seems nonplussed, but doesn't object.",
		str_walk = "{slimeoid_name} exasperatedly lets you fit it with a leash for a walk.",
		str_kill = "{slimeoid_name} rifles through your victim's pockets for food.",
		str_death = "{slimeoid_name} rifles through its dead master's pockets for whatever it can find before slinking away.",
		str_victory = "{slimeoid_name} shakes itself off after the battle.",
		str_battlecry = "{slimeoid_name} makes its move! ",
		str_battlecry_weak = "{slimeoid_name}, backed into a corner, tries to counterattack! ",
		str_movecry = "{slimeoid_name} decides on a tactical repositioning. " ,
		str_movecry_weak = "{slimeoid_name} thinks it'd better try something else, and fast! ",
		str_revive = "{slimeoid_name} starts following you around again not long after you have returned from the dead.",
		str_spawn = "{slimeoid_name} picks itself up off the floor and regards you coolly. It seems as if it's gauging your usefulness.",
		str_dissolve = "{slimeoid_name} eyes you suspiciously as you approach the Dissolution Vats. It's on to you. Before it has a chance to bolt, you grab it, hoist it up over your head, and hurl it into the chemical soup. {slimeoid_name} screeches in protest, sputtering and hissing as it thrashes around in the vat, but the chemicals work quickly and it soon dissolves into nothing.\n\n{slimeoid_name} is no more."
	),
	EwBrain( # brain 7
		id_brain = "g",
		alias = [
			"typeg",
			"type g"
		],
		str_create = "You press a button on the brain console labelled 'G'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to flit around the gestation vat, seemingly unsure where to go.",
		str_brain = "It seems to have no idea what it's doing.",
		str_observe = "{slimeoid_name} seems unsure of whether it wants to wander around or just stay put.",
		str_pet = "{slimeoid_name} seems confused about how to react.",
		str_walk = "{slimeoid_name} lets you put its leash on it, but immediately starts to trip over it and get tangled in it.",
		str_kill = "{slimeoid_name} seems unsure of whether to celebrate the victory or to mourn the decline of your civilization into rampant youth violence.",
		str_death = "{slimeoid_name} starts to approach its master's body, then changes its mind and starts to run away. It trips over itself and falls on its way out.",
		str_victory = "{slimeoid_name} looks around, apparently shocked that it somehow won.",
		str_battlecry = "{slimeoid_name} decides to actually do something for once! ",
		str_battlecry_weak = "{slimeoid_name} decides to actually do something for once, now that it's probably too late.",
		str_movecry = "{slimeoid_name} is moving around aimlessly! " ,
		str_movecry_weak = "{slimeoid_name} is limping around aimlessly! ",
		str_revive = "{slimeoid_name} wanders by, seemingly by accident, but thinks it probably ought to start following you again.",
		str_spawn = "{slimeoid_name} starts to pick itself up off the floor, then changes its mind and lies back down. Then it gets up again. Lies down again. Up. Down. Up. Ok, this time it stays up.",
		str_dissolve = "{slimeoid_name} is perplexed by the laboratory machinery. Taking advantage of its confusion, you point it towards the Dissolution Vats, and it gormlessly meanders up the ramp and over the edge. You hear a gloopy SPLOOSH sound, then nothing. You approach the vats and peer over the edge, but see no trace of your former companion.\n\n{slimeoid_name} is no more."
	)
]

# A map of id_brain to EwBrain objects.
brain_map = {}

# A list of brain names
brain_names = []

# Populate brain map, including all aliases.
for brain in brain_list:
	brain_map[brain.id_brain] = brain
	brain_names.append(brain.id_brain)

	for alias in brain.alias:
		brain_map[alias] = brain

# Things a slimeoid might throw
thrownobjects_list = [
	"sewer cap",
	"boulder",
	"chunk of broken asphalt",
	"broken fire hydrant",
	"SlimeCorp-Brand Slime Containment Vessel (tm)",
	"piece of sheet metal",
	"burning tire",
	"hapless bystander",
	"completely normal small mammal",
	"heap of broken glass",
	"stereotypical nautical anchor",
	"piece of an iron girder",
	"pile of lumber",
	"pile of bricks",
	"unrecognizably decayed animal carcass",
	"very fortuitously abandoned javelin",
	"large rock",
	"small motor vehicle",
	"chunk of broken concrete",
	"piece of rusted scrap metal"
]

# lists of all the discord server objects served by bot, identified by the server id
server_list = {}

"""
	store a server in a dictionary
"""
def update_server_list(server):
	server_list[server.id] = server


clients = []

"""
	save the discord client of this bot
"""
def set_client(cl):
	clients.append(cl)
