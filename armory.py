from structs import *

Items = {}

class Item:
	def __init__(self, name = "unnamed", slot = "", stats = {}):
		self.name = name
		self.slot = slot
		self.stats = item_struct.copy()
		for key in stats:
			self.stats[key] = stats[key]
		if (slot == "mainhand" or slot == "offhand"):
			self.stats['is_weapon'] = True
			self.last_hit = -10

		Items[name] = self


############################
## weapons
############################
Item('Dragonstrike', "mainhand", {
	"speed": 2.7,
	"type": "sword",
	"min_damage": 184,
	"max_damage": 343,
})

Item('Spiteblade', "offhand", {
	"speed": 2.7,
	"type": "sword",
	"min_damage": 165,
	"max_damage": 308,
	"agility": 14,
})

Item('Merciless Gladiator\'s Slicer', "offhand", {
	"speed": 2.6,
	"type": "sword",
	"min_damage": 203,
	"max_damage": 305,
	"hit_rating": 10,
	"crit_rating": 19,
	"attack_power": 30,
})

Item('Talon of Azshara', {
	"slot": "offhand",
	"type": "sword",
	"min_damage": 182,
	"max_damage": 339,
	"agility": 15,
	"hit_rating": 20,
	"attack_power": 40,
})


############################
## Armor
############################
Item('Destroyer Battle-Helm', "helm", {
	"gems": {
		"meta": True,
		"blue": 1,
		"bonus": {
			"strength": 4
		},
	},
	"strength": 47,
	"hit_rating": 21,
	"crit_rating": 36,
})

Item('Pendant of the Perilous', "neck", {
	"strength": 32,
	"crit_rating": 23,
})

Item('Destroyer Shoulderblades', "shoulders", {
	"strength": 36,
	"gems": {
		"yellow": 1,
		"blue": 1,
		"bonus": {
			"strength": 3
		}
	},
	"hit_rating": 18,
	"crit_rating": 20,
})

Item('Vengeance Wrap', "back", {
	"gems": {
		"red": 1,
		"bonus": {
			"hit_rating": 3
		}
	},
	"crit_rating": 23,
	"attack_power": 52,
})

Item("Bloodsea Brigand's Vest", "chest", {
	"gems": {
		"yellow": 2,
		"blue": 1,
		"bonus": {
			"attack_power": 8
		}
	},
	"crit_rating": 36,
	"hit_rating": 27,
	"attack_power": 92,
})

Item("Bracers of Eradication", "bracers", {
	"gems": {
		"blue": 1,
		"bonus": {
			"strength": 2
		}
	},
	"strength": 25,
	"crit_rating": 24,
	"hit_rating": 17,
})

Item("Destroyer Gauntlets", "gloves", {
	"strength": 44,
	"crit_rating": 30,
})

Item("Red Belt of Battle", "belt", {
	"gems": {
		"yellow": 1,
		"blue": 1,
		"bonus": {
			"crit_rating": 3
		}
	},
	"strength": 41,
	"crit_rating": 24,
	"hit_rating": 14,
})

Item("Destroyer Greaves", "legs", {
	"gems": {
		"red": 1,
		"bonus": {
			"crit_rating": 2
		}
	},
	"strength": 52,
	"crit_rating": 32,
	"hit_rating": 22,
})

Item("Warboots of Obliteration", "boots", {
	"strength": 4,
	"crit_rating": 31,
})

Item("Ring of a Thousand Marks", "ring", {
	"crit_rating": 23,
	"hit_rating": 19,
	"attack_power": 44,
})

Item("Ring of Lethality", "ring", {
	"agility": 24,
	"hit_rating": 19,
	"attack_power": 50,
})

Item("Bloodlust Brooch", "trinket", {
	"attack_power": 72,
})

Item("Empty Mug of Direbrew", "trinket", {
	"attack_power": 72,
})

Item("Serpentshrine Shuriken", "ranged", {
	"crit_rating": 20,
	"hit_rating": 12,
})