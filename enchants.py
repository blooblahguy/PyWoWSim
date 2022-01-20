from structs import *

Enchants = {}

class EnchantClass():
	def __init__(self, name, stats = stat_struct.copy()):
		self.enabled = True
		self.name = name
		self.stats = stats

		Enchants[name] = self

# glyph
EnchantClass('helm', {
	"hit_rating": 16,
	"attack_power": 16,
})

# meta
EnchantClass('helm_meta', {
	"agility": 16,
	"crit_mult": .03,
})

EnchantClass('shoulder', {
	"crit_rating": 14,
	"attack_power": 20,
})

EnchantClass('back', {
	"agility": 12,
})

EnchantClass('chest', {
	"agility": 6,
	"strength": 6,
})

EnchantClass('wrist', {
	"strength": 12,
})

EnchantClass('hands', {
	"strength": 15,
})

EnchantClass('legs', {
	"crit_rating": 12,
	"attack_power": 50,
})

EnchantClass('boots', {
	"agility": 6,
})

EnchantClass('adamantite_stone', {
	"oh_damage": 12,
	"crit_rating": 14,
})