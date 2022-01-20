from structs import *

Buffs = {}

class BuffClass():
	def __init__(self, name, sub_callback = not_implemented):
		self.name = name
		self.enabled = True
		self.sub_callback = sub_callback

		Buffs[name] = self

	def apply(self, Player, Target = False, combat_time = 0):
		self.sub_callback(Player, Target, combat_time)

# raid Buffs. we count deBuffs as Buffs for simplicity sake

#todo
# berserker rage
# trueshot_aura
# grace_of_air
# blood_frenzy

# buff functions

# do this first
def flask_of_relentless_assault(Player, Target, combat_time):
	Player.buffs['attack_power'] += 120
BuffClass('flask_of_relentless_assault', flask_of_relentless_assault)

def roasted_clefthoof(Player, Target, combat_time):
	Player.buffs['strength'] += 20
BuffClass('roasted_clefthoof', roasted_clefthoof)

def strength_scroll(Player, Target, combat_time):
	Player.buffs['strength'] += 20
BuffClass('strength_scroll', strength_scroll)

def agility_scroll(Player, Target, combat_time):
	Player.buffs['agility'] += 20
BuffClass('agility_scroll', agility_scroll)

# now apply kings
def blessing_of_kings(Player, Target, combat_time):
	Player.buffs['agility'] *= 1.1
	Player.buffs['strength'] *= 1.1
BuffClass('blessing_of_kings', blessing_of_kings)

def leader_of_the_pack(Player, Target, combat_time):
	Player.buffs['crit_rating'] += (22.08 * 5)
BuffClass('leader_of_the_pack', leader_of_the_pack)

def battle_shout(Player, Target, combat_time):
	Player.buffs['attack_power'] += 306
BuffClass('battle_shout', battle_shout)

def gift_of_the_wild(Player, Target, combat_time):
	Player.buffs['agility'] += 14
	Player.buffs['strength'] += 14
BuffClass('gift_of_the_wild', gift_of_the_wild)

def blessing_of_might(Player, Target, combat_time):
	Player.buffs['attack_power'] += 220
BuffClass('blessing_of_might', blessing_of_might)

def hunters_mark(Player, Target, combat_time):
	Player.buffs['attack_power'] += 110
BuffClass('hunters_mark', hunters_mark)

def curse_of_recklessness(Player, Target, combat_time):
	Target.debuffs['armor'] -= 800
BuffClass('curse_of_recklessness', curse_of_recklessness)

def sunder_armor(Player, Target, combat_time):
	Target.debuffs['armor'] -= 2600
BuffClass('sunder_armor', sunder_armor)

def fearie_fire(Player, Target, combat_time):
	Target.debuffs['armor'] -= 610
BuffClass('fearie_fire', fearie_fire)

def imp_fearie_fire(Player, Target, combat_time):
	Player.buffs['hit_rating'] += (15.77 * 3)
BuffClass('imp_fearie_fire', imp_fearie_fire)

def strength_of_earth(Player, Target, combat_time):
	Player.buffs['strength'] += 86
BuffClass('strength_of_earth', strength_of_earth)

def imp_seal_of_the_crusader(Player, Target, combat_time):
	Player.buffs['crit_rating'] += (22.08 * 3)
BuffClass('imp_seal_of_the_crusader', imp_seal_of_the_crusader)

def imp_sanctity_aura(Player, Target, combat_time):
	Player.buffs['damage_mult'] = 1.02
BuffClass('imp_sanctity_aura', imp_sanctity_aura)

def heroic_presense(Player, Target, combat_time):
	Player.buffs['hit_rating'] += (15.77 * 1)
BuffClass('heroic_presense', heroic_presense)

enchants = {
	"mongoose": {
		"proc": {
			"icd": 60,
			"chance": .02,
			"duration": 12,
			"callback": ""
		},
	},
}