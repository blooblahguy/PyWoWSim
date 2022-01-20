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
	return (Player.stats['attack_power'] * 45) / 100
bloothirst = Ability("bloodthirst", bloodthirst, 30, 6)

#whirlwind
def whirlwind(Player, Target):
	damage = Player.normalize_swing("mainhand", Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	damage += Player.normalize_swing("offhand", Player.items["offhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	return damage
whirlwind = Ability("whirlwind", whirlwind, 30, 8)

#whirlwind
# def whirlwind_offhand(Player, Target):
# 	damage = Player.normalize_swing("offhand", Player.items["offhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
# 	return damage
# whirlwind_offhand = Ability("whirlwind_offhand", whirlwind_offhand, 30, 8)

#whirlwind
def execute(Player, Target):
	damage = 925 + (Player.rage - 15) * 21
	Player.spend_rage(Player.rage) # zero out rage
	return damage
execute = Ability("execute", execute, 15, 0)