from structs import *
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
		self.last_casted = 0
		self.unused_off_cooldown = 0

	def on_cooldown(self, combat_time):
		if (self.last_used + self.cooldown > combat_time):
			return True
		else:
			return False
	def cast(self, Player, Target, combat_time):
		self.last_casted = combat_time
		if (self.duration > 0):
			self.active = True
		return self.callback(Player, Target)

	def update(self, Player, Target, combat_time):
		if (self.duration == 0):
			return
		if (self.last_casted != 0 and combat_time > float(self.last_casted) + float(self.duration)):
			self.last_casted = 0
			self.active = False
			self.callback(Player, Target, True)

#blood rage
def bloodrage(Player, Target, removed = False):
	Player.gain_rage(10)
	return 0

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
	mh_damage = random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
	oh_damage = (random.randrange(Player.items["mainhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage']) + Player.stats['oh_damage'])

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

#death wish
def death_wish(Player, Target, removed = False):
	if (removed != False):
		Player.stats['damage_mult'] += 0.2
	else:
		Player.stats['damage_mult'] -= 0.2
	return 0

#heroism
def heroism(Player, Target, removed = False):
	if (removed != False):
		Player.stats['haste'] += 0.3
	else:
		Player.stats['haste'] -= 0.3
	return 0

#death wish
def bloodlust_brooch(Player, Target, removed = False):
	if (removed != False):
		Player.stats['attack_power'] += 278
	else:
		Player.stats['attack_power'] -= 278
	return 0

#whirlwind
# def whirlwind_offhand(Player, Target):
# 	damage = Player.normalize_swing("offhand", Player.items["offhand"].stats['min_damage'], Player.items["mainhand"].stats['max_damage'])
# 	return damage
# whirlwind_offhand = Ability("whirlwind_offhand", whirlwind_offhand, 30, 8)

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
	Abilities["death_wish"] = Ability("death_wish", death_wish, 10, 180, True, 30)
	Abilities["bloodlust_brooch"] = Ability("bloodlust_brooch", bloodlust_brooch, 0, 120, False, 20)
	Abilities["empty_diremug"] = Ability("empty_diremug", bloodlust_brooch, 0, 120, False, 20)

	Abilities["heroism"] = Ability("heroism", heroism, 0, 600, False, 40)

	return Abilities