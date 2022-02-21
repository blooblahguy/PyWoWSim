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

		self.apply_gems()

		Items[name] = self
	def apply_gems(self):
		use_gems = {
			"yellow": {
				"crit_rating": 8,
			},
			"blue": {
				"crit_rating": 4,
			},
			"red": {
				"crit_rating": 4,
				"strength": 4,
			},
		}

		for color in use_gems:
			# add gems by color
			try:
				if (self.stats["gems"][color] > 0):
					# print("add", color, self.stats["gems"][color])
					for i in range(1, self.stats["gems"][color] + 1):
						for stat in use_gems[color]:
							self.stats[stat] += use_gems[color][stat]
			except:
				pass
		
		try:
			for stat in self.stats["gems"]['bonus']:
				value = self.stats["gems"]['bonus'][stat]
				if (value > 0):
					self.stats[stat] += value
					# print(stat, value)
		except:
			pass
			# if (self.stats["gems"][color] != 0):
			# 	print(self.stats["gems"][color])
			# 	# self.stats[]


############################
## weapons
############################
Item('Dragonstrike', "mainhand", {
	"type": "1h",
	"class": "sword",
	"base_speed": 2.7,
	"min_damage": 184,
	"max_damage": 343,
})

Item('Spiteblade', "offhand", {
	"type": "1h",
	"class": "sword",
	"base_speed": 2.7,
	"min_damage": 165,
	"max_damage": 308,
	"agility": 14,
})

Item('Merciless Gladiator\'s Slicer', "offhand", {
	"type": "1h",
	"class": "sword",
	"base_speed": 2.6,
	"min_damage": 203,
	"max_damage": 305,
	"hit_rating": 10,
	"crit_rating": 19,
	"attack_power": 30,
})

Item('Talon of Azshara', {
	"type": "1h",
	"class": "sword",
	"base_speed": 2.7,
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
			"hit_rating": 2
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
			"attack_power": 8,
			"strength": 5, # we used a strength gem
			"crit_rating": -4, # which means we should force out our basic 4 crit 4 stam gem
		}
	},
	"crit_rating": 36,
	"hit_rating": 27,
	"attack_power": 92,
})

Item("Bracers of Eradication", "bracers", {
	"gems": {
		"blue": 1,
		# "bonus": {
		# 	"strength": 2
		# }
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
		# "bonus": {
		# 	"crit_rating": 3
		# }
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
	"strength": 44,
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

Item("Sunfury Bow of the Phoenix", "ranged", {
	"agility": 19,
	"attack_power": 34,
})

Item("Serpentshrine Shuriken", "ranged", {
	"crit_rating": 20,
	"hit_rating": 12,
})