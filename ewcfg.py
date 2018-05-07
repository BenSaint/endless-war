# Global configuration options.
version = "v1.16"

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
cmd_equip = cmd+prefix + 'equip'

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
col_weapon = 'weapon'
col_trauma = 'trauma'
col_slimecredit = 'slimecredit'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_expirpvp = 'time_expirpvp'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'

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
