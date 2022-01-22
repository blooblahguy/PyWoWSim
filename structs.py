def not_implemented():
	return

## stat names we'll use
stat_struct = {
	"strength": 0,
	"agility": 0,
	"attack_power": 0,
	"crit_rating": 0,
	"hit_rating": 0,
	"expertise_rating": 0,
	"armor_pen": 0,
	"haste_rating": 0,
	"crit_mult": 0,
	"damage_mult": 0,
	"oh_damage": 0,
}

# for creating new items
item_struct = stat_struct.copy()
item_struct["is_weapon"] = False
item_struct["base_speed"] = 0
item_struct["speed"] = 0 # after haste
item_struct["min_damage"] = 0
item_struct["max_damage"] = 0
item_struct["gems"] = {
	"meta": False,
	"yellow": 0,
	"red": 0,
	"blue": 0,
	"bonus": stat_struct.copy(),
}
item_struct["proc"] = {
	"last_proc": 0,
	"icd": 0,
	"callback": not_implemented,
}

ability_struct = {
	"callback": not_implemented,
	"cooldown": 6,
	"last_used": 6,
	"cost": 25,
}

procs_default = {
	"icd": 60,
	"chance": 0.02,
	"callback": not_implemented,
}

# default damage_format
damage_format = {
	"damage": 0,
	"crit": False,
	"crits": 0,
	"miss": False,
	"misses": 0,
	"dodge": False,
	"dodges": 0,
	"casts": 0,
}