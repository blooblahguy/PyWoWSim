from structs import *
# from numpy import *
import random


class Ability:
	def __init__(self, name, callback, cost = 0, cooldown = 0, triggersGCD = True, duration = 0):
		self.name = name
		self.callback = callback
		self.cost = cost
		self.active = False
		self.cooldown = cooldown
		self.duration = duration
		self.triggersGCD = triggersGCD
		self.next_cast = 0
		self.unused_off_cooldown = 0

	def can_cast(self, combat_time):
		if (combat_time >= self.next_cast or self.next_cast == 0):
			return True
		else:
			return False

	def remaining_cooldown(self, combat_time):
		return self.next_cast - combat_time

	def on_cooldown(self, combat_time):
		if (self.next_cast >= combat_time):
			return True
		else:
			return False
	def cast(self, Player, Target, combat_time):
		self.next_cast = combat_time + self.cooldown
		if (self.duration > 0):
			self.active = True
		return self.callback(Player, Target)

#heroic strike
def heroic_strike(Player, Target, removed = False):
	damage = Player.normalize_swing("mainhand", Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	damage += 176
	return damage

#bloodthirst
def bloodthirst(Player, Target, removed = False):
	return (Player.stats['attack_power'] * 45) / 100

#whirlwind
def whirlwind(Player, Target, removed = False):
	mh_damage = random.randint(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	oh_damage = (random.randint(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage']) + Player.stats['oh_damage'])

	oh_damage *= 1 + 0.05 * Player.talents['dual_wield_specialization'] # add talent damage
	oh_damage /= 2 # offhand penalty

	mh_damage = mh_damage + (Player.stats['attack_power'] * (Player.items["mainhand"].stats['speed'] / 14))
	oh_damage = oh_damage + (Player.stats['attack_power'] * (Player.items["offhand"].stats['speed'] / 14))

	return mh_damage + oh_damage

# execute
def execute(Player, Target):
	damage = 925 + (Player.rage - 15) * 21
	Player.spend_rage(Player.rage) # zero out rage
	return damage

#whirlwind
# def whirlwind_offhand(Player, Target):
# 	damage = Player.normalize_swing("offhand", Player.items["offhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
# 	return damage
# whirlwind_offhand = Ability("whirlwind_offhand", whirlwind_offhand, 30, 8)

def create_abilities():
	global death_wish, death_wish_remove, heroic_strike, bloodthirst, whirlwind, execute

	# def test_ability(Player, Target):
	# 	return 1000

	# abilities
	Abilities = {}

	Abilities["heroic_strike"] = Ability("heroic_strike", heroic_strike, 15, 0)
	Abilities["bloodthirst"] = Ability("bloodthirst", bloodthirst, 30, 6)
	Abilities["whirlwind"] = Ability("whirlwind", whirlwind, 30, 9)
	Abilities["execute"] = Ability("execute", execute, 15, 0)

	# no cost no cooldown, testing gcd stuff
	# Abilities["test_ability"] = Ability("test_ability", test_ability, 0, 0)

	return Abilities