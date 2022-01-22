from structs import *
import random

class Ability:
	def __init__(self, name, callback, cost = 0, cooldown = 0, triggersGCD = True, duration = 0, expire_callback = False):
		self.name = name
		self.callback = callback
		self.expire_callback = expire_callback
		self.cost = cost
		self.cooldown = cooldown
		self.duration = duration
		self.triggersGCD = triggersGCD
		self.last_casted = 0
		self.unused_off_cooldown = 0

	def on_cooldown(self, combat_time):
		if (self.last_used + self.cooldown > combat_time):
			return True
		else:
			return False
	def cast(self, Player, Target, combat_time):
		self.last_casted = combat_time
		return self.callback(Player, Target)

	def update(self, Player, Target, combat_time):
		if (self.duration == 0 or not self.expire_callback): 
			return
		if (self.last_casted != 0 and combat_time > float(self.last_casted) + float(self.duration)):
			self.last_casted = 0
			self.expire_callback(Player, Target)

#blood rage
def bloodrage(Player, Target):
	Player.gain_rage(10)
	return 0

#heroic strike
def heroic_strike(Player, Target):
	damage = Player.normalize_swing("mainhand", Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	damage += 176
	return damage

#bloodthirst
def bloodthirst(Player, Target):
	return (Player.stats['attack_power'] * 45) / 100

#whirlwind
def whirlwind(Player, Target):
	mh_damage = random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	oh_damage = (random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage']) + Player.stats['oh_damage'])

	oh_damage *= 1 + 0.05 * Player.talents['dual_wield_specialization'] # add talent damage
	oh_damage /= 2 # offhand penalty

	mh_damage = mh_damage + (Player.stats['attack_power'] * (Player.items["mainhand"].stats['speed'] / 14))
	oh_damage = oh_damage + (Player.stats['attack_power'] * (Player.items["offhand"].stats['speed'] / 14))

	return mh_damage + oh_damage

#death wish
def death_wish(Player, Target):
	Player.stats['damage_mult'] += 0.2
	return 0

def death_wish_remove(Player, Target):
	Player.stats['damage_mult'] -= 0.2
	return False # false stops this from being logged

#heroism
def heroism(Player, Target):
	Player.stats['haste'] += .3 #(15.77 * 30)
	# print(Player.stats['haste'])
	return 0

def heroism_remove(Player, Target):
	Player.stats['haste'] -= .3 #(15.77 * 30)
	# print(Player.stats['haste'])
	return False # false stops this from being logged

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

def create_abilities():
	global death_wish, death_wish_remove, bloodrage, heroic_strike, bloodthirst, whirlwind, execute

	# abilities
	Abilities = {}

	Abilities["bloodrage"] = Ability("bloodrage", bloodrage, 0, 60, False)
	Abilities["heroic_strike"] = Ability("heroic_strike", heroic_strike, 15, 0)
	Abilities["bloodthirst"] = Ability("bloodthirst", bloodthirst, 30, 6)
	Abilities["whirlwind"] = Ability("whirlwind", whirlwind, 30, 9)
	Abilities["execute"] = Ability("execute", execute, 15, 0)

	# cooldowns
	Abilities["death_wish"] = Ability("death_wish", death_wish, 10, 180, True, 30, death_wish_remove)
	Abilities["heroism"] = Ability("heroism", heroism, 0, 600, False, 40, heroism_remove)
	# Abilities["heroism"] = Ability("heroism", heroism, 0, 600, False, 40, heroism_remove)

	return Abilities