from structs import *

# raid buffs
buffs = {
	"battle_shout": buff_struct.copy(),
	"berserkers_rage": buff_struct.copy(),
	"gift_of_the_wild": buff_struct.copy(),
	"leader_of_the_pack": buff_struct.copy(),
	"trueshot_aura": buff_struct.copy(),
	"improved_hunters_mark": buff_struct.copy(),
	"expose_weakness": buff_struct.copy(),
	"blessing_of_kings": buff_struct.copy(),
	"blessing_of_might": buff_struct.copy(),
	"windfury_totem": buff_struct.copy(),
	"strength_of_earth": buff_struct.copy(),
	"grace_of_air": buff_struct.copy(),
	"imp_seal_of_the_crusader": buff_struct.copy(),
	"imp_sanctity_aura": buff_struct.copy(),
	"blood_frenzy": buff_struct.copy(),
	"heroic_presense": buff_struct.copy(),
	"flask_of_relentless_assault": buff_struct.copy(),
	"roasted_clefthoof": buff_struct.copy(),
}

# buff functions
def battle_shout(name, player, target, combat_time):
	player['attack_power'] += 306
buffs['battle_shout']['callback'] = battle_shout

def gift_of_the_wild(name, player, target, combat_time):
	player['agility'] += 14
	player['strength'] += 14
buffs['gift_of_the_wild']['callback'] = gift_of_the_wild

def blessing_of_kings(name, player, target, combat_time):
	player['agility'] *= 1.1
	player['strength'] *= 1.1
buffs['blessing_of_kings']['callback'] = blessing_of_kings

def blessing_of_might(name, player, target, combat_time):
	player['attack_power_rating'] += 220
buffs['blessing_of_might']['callback'] = blessing_of_might

def leader_of_the_pack(name, player, target, combat_time):
	player['crit_chance'] *= 1.05
buffs['leader_of_the_pack']['callback'] = leader_of_the_pack

ench_default = {
	"enabled": 0,
	"strength": 0,
	"agility": 0,
	"expertise": 0,
	"hit": 0,
	"attack_power": 0,
	"crit_rating": 0,
	"crit_mult": 0,
	"haste": 0,
	"armor_pen": 0,
	"proc": {
		"icd": 0,
		"chance": 0,
		"duration": 0,
		"callback": ""
	},
}

enchants = {
	"helm": {
		"hit": 16,
		"attack_power_rating": 16,
	},
	"helm_meta": {
		"agility": 16,
		"crit_mult": .03,
	},
	"shoulder": {
		"crit_rating": 14,
		"attack_power_rating": 20,
	},
	"back": {
		"agility": 12,
	},
	"chest": {
		"agility": 6,
		"strength": 6,
	},
	"wrist": {
		"strength": 12,
	},
	"hands": {
		"strength": 15,
	},
	"legs": {
		"crit_rating": 12,
		"attack_power_rating": 50,
	},
	"boots": {
		"agility": 6,
	},
	"mongoose": {
		"proc": {
			"icd": 60,
			"chance": .02,
			"duration": 12,
			"callback": ""
		},
	},
	"adamantite_stone": {
		"enabled": 1,
		"oh_damage": 12,
		"crit_rating": 14,
	}
}