from structs import *
import random

Abilities = {}

class Ability:
	def __init__(self, name, callback, cost = 0, cooldown = 0, triggersGCD = True):
		self.name = name
		self.callback = callback
		self.cost = cost
		self.cooldown = cooldown
		self.triggersGCD = triggersGCD

		Abilities[name] = self
	def on_cooldown(self, combat_time):
		if (self.last_used + self.cooldown > combat_time):
			return True
		else:
			return False
	def cast(self, Player, Target):
		return self.callback(Player, Target)

#blood rage
def bloodrage(Player, Target):
	Player.gain_rage(10)
	return 0
bloodrage = Ability("bloodrage", bloodrage, 0, 60, False)

#heroic strike
def heroic_strike(Player, Target):
	damage = Player.normalize_swing("mainhand", Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	damage += 176
	return damage
heroic_strike = Ability("heroic_strike", heroic_strike, 15, 0)

#bloodthirst
def bloodthirst(Player, Target):
	return (Player.stats['attack_power'] * 45) / 100
bloothirst = Ability("bloodthirst", bloodthirst, 30, 6)

#whirlwind
def whirlwind(Player, Target):
	mh_damage = random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	oh_damage = (random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage']) + Player.stats['oh_damage'])

	oh_damage *= 1 + 0.05 * Player.talents['dual_wield_specialization'] # add talent damage
	oh_damage /= 2 # offhand penalty

	mh_damage = mh_damage + (Player.stats['attack_power'] * (Player.items["mainhand"].stats['speed'] / 14))
	oh_damage = oh_damage + (Player.stats['attack_power'] * (Player.items["offhand"].stats['speed'] / 14))

	return mh_damage + oh_damage
whirlwind = Ability("whirlwind", whirlwind, 30, 9)

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