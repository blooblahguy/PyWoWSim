from structs import *

Abilities = {}
class Ability:
	def __init__(self, name, callback, cost = 0, cooldown = 0):
		self.name = name
		self.data = ability_struct.copy()
		self.callback = callback
		self.cost = cost
		self.cooldown = cooldown
		self.last_used = 500

		Abilities[name] = self
	def on_cooldown(self, combat_time):
		if (self.data.last_used + self.data.cooldown > combat_time):
			return True
		else:
			return False
	def cast(self, Player, Target):
		return self.callback(Player, Target)

#bloodthirst
def bloodthirst(Player, Target):
	# double damage = (state.special_stats.attack_power * 0.45 + state.special_stats.bonus_damage) * (100 + 5 * has_onslaught_4_set_) / 100;
	return (Player.final_stats['attack_power'] * 45) / 100
bloothirst = Ability("bloodthirst", bloodthirst, 30, 6)

#whirlwind
def whirlwind(Player, Target):
	return Player['mainhand']['min_damage'] + Player['offhand']['min_damage'], Player['mainhand']['max_damage'] + Player['offhand']['max_damage']
whirlwind = Ability("whirlwind", whirlwind, 30, 8)