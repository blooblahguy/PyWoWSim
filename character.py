# from numpy import *
from functions import *
from __init__ import *
from classes.actions import *
import random
# from numba import njit, prange

# 15.77 Hit Rating = 1% Hit
# 3.9423 Expertise Rating = 1 Expertise = -0.25% Dodge/Parry
# 22.08 Crit Rating = 1% Crit
# 15.77 Haste Rating = 1% Haste
# 1 Strength = 2 Attack Power
# 33 Agility = 1% Crit

class CharacterClass:
	def __init__(self, Sim):
		self.Sim = Sim

		self.items = {
			"helm": False,
			"neck": False,
			"shoulders": False,
			"back": False,
			"chest": False,
			"bracers": False,
			"gloves": False,
			"belt": False,
			"legs": False,
			"boots": False,
			"ring1": False,
			"ring2": False,
			"trinket1": False,
			"trinket2": False,
			"ranged": False,
			"mainhand": False,
			"offhand": False,
		}

		self.next_swing = {
			"mainhand": 0,
			"offhand": 0,
		}

		# naked stats for level 70
		self.race = "human"

		# add in all static sources of stats
		self.strength_mult = 1 # kings base
		self.agility_mult = 1 # kings base
		self.character_stats = stat_struct.copy() # stats when naked
		self.character_stats["strength"] = 145
		self.character_stats["attack_power"] = 190
		self.character_stats["agility"] = 96
		self.gear_stats = stat_struct.copy() # stats from gear
		self.buffs = stat_struct.copy() # tracking active buffs and stats
		self.cooldowns = stat_struct.copy() # tracking procs (active or not) and stats
		self.procs = {} # tracking procs (active or not) and stats
		self.stats = stat_struct.copy() # final calculated stats

		# formula stats
		self.rage = 0
		self.level = 70
		self.rage_factor = .0091107836 * (self.level ** 2) + 3.225598133 * (self.level) + 4.2652911

		# quick talents
		self.talents = {
			"weapon_mastery": 2,
			"improved_heroic_strike": 3,
			"impale": 2,
			"cruelty": 5,
			"commanding_presence": 5,
			"dual_wield_specialization": 5,
			"improved_berserker_stance": 5,
		}

		# combat variables
		self.queue_heroic_strike = False
		self.last_anger_rage = 0
		self.last_bloodrage = 0
		self.blood_rage_total = 0
		self.blood_rage_active = False
		self.flurry = 0
		self.last_wf = -3

		#gcd
		self.base_gcd = 1.5
		self.gcd = self.base_gcd
		self.off_gcd = True
		self.next_gcd = 0
		self.last_gcd = 10
		self.reported_gcd1 = False
		self.reported_gcd2 = False

		# add_action("combat_tick_first", self.update)

	# add buffs to character
	def apply_buffs(self, combat_time = 0):
		# apply the buff callbacks
		self.buffs = stat_struct.copy()
		for name in Buffs:
			if (Buffs[name].enabled):
				# print(name)
				Buffs[name].apply(self, self.Target, combat_time)

	# equip item to character
	def equip(self, itemName, slot = False):
		if (not slot):
			slot = Items[itemName].slot
		self.items[slot] = Items[itemName]

	# unequip and remove stats
	def unequip(self, itemName, slot = False):
		if (not slot):
			slot = Items[itemName].slot
		self.items[slot] = False
	
	###############
	# calculate stats
	###############
	def calculate_stats(self):
		self.stats = stat_struct.copy() # reset calculated stat array

		# naked stats
		self.stats['strength'] = self.character_stats["strength"]
		self.stats['agility'] = self.character_stats["agility"]
		self.stats['attack_power'] = self.character_stats["attack_power"]

		# add gear in
		self.calculate_gear_stats()

		# add buffs in
		self.apply_buffs()

		# add talents in
		self.calculate_talent_stats()

		# cooldowns that are active
		self.calculate_cooldowns()

		# turn final strength into additional AP
		self.stats_finalize()

		self.update_gcd()
		self.update_haste()

		# print("calculated stats")

	def stats_finalize(self):
		# add gear
		for stat in self.gear_stats:
			self.stats[stat] += self.gear_stats[stat]

		# add buffs
		# print(self.buffs[stat])
		for stat in self.buffs:
			try:
				self.stats[stat] += self.buffs[stat]
			except:
				pass

		# calculate hit
		self.stats['hit_chance'] = max(self.stats['hit_rating'] / 15.77, 0)

		# calculate expertise
		self.stats['expertise'] = min(((self.stats['expertise_rating'] / 3.9423) * 0.25) + self.talents["weapon_mastery"], 6.5)

		# calculate crit chance
		self.stats['crit_rating'] += (22.08 * 3) # berserker stance
		self.stats['crit_chance'] = self.stats['crit_rating'] / 22.08
		self.stats['crit_chance'] += self.stats['agility'] / 33

		# calculate haste rating
		self.stats['haste'] = (self.stats['haste_rating'] / 15.77) / 100

		# apply kings
		self.stats['strength'] *= self.strength_mult
		self.stats['agility'] *= self.agility_mult

		# lastly add strength to AP
		self.stats['attack_power'] += self.stats['strength'] * 2

		# unleashed rage?
		self.stats['attack_power'] *= 1.1

		# imp berserker stance
		self.stats['attack_power'] *= 1 + (.02 * self.talents['improved_berserker_stance'])
	
	# tally talent stats and place in storage
	def calculate_talent_stats(self):
		self.Sim.Abilities['heroic_strike'].cost = 15 - self.talents['improved_heroic_strike']
		self.gear_stats['crit_rating'] += (22.08 * self.talents['cruelty'])

	# tally gear stats and place in storage
	def calculate_gear_stats(self):
		self.gear_stats = stat_struct.copy() # reset gear stats

		# add enchants to gear (those that aren't procs)
		for key in Enchants:
			for stat in Enchants[key].stats:
				self.gear_stats[stat] += Enchants[key].stats[stat]

		# loop through items and tally
		for slot in self.items:
			item = self.items[slot]
			if (item):
				for stat in item.stats:
					try:
						self.gear_stats[stat] += item.stats[stat]
					except:
						pass

		# add expertise if human
		if (self.race == "human" and (self.items['mainhand'].stats["class"] == "sword" or self.items['mainhand'].stats["class"] == "mace")):
			self.gear_stats['expertise_rating'] += (3.9423 * 5)

	def calculate_cooldowns(self):
		for stat in self.cooldowns:
			if (self.cooldowns[stat] > 0):
				self.stats[stat] += self.cooldowns[stat]

	def gain_rage(self, rage):
		self.rage += rage
		if (self.rage > 100):
			self.Sim.overcapped_rage += self.rage - 100
			self.rage = 100

	def spend_rage(self, rage):
		self.rage -= rage
		if (self.rage < 0):
			print('error with rage going sub 0')
	
	# generate rage from auto attack
	def generate_rage(self, damage, weapon, crit = False):
		if (damage == 0): return

		# weapon rage factor from mh/oh crit/nocrit
		wep_factor = 0
		if (weapon == "mainhand"):
			wep_factor = crit and 7 or 3.5
		elif (weapon == "offhand"):
			wep_factor = crit and 3.5 or 1.75

		# normalized weapon speed
		wep_speed_normal = 0
		if (self.items[weapon].stats["type"] == "1h"):
			wep_speed_normal = 2.4
		elif (self.items[weapon].stats["type"] == "2h"):
			wep_speed_normal = 3.3
		elif (self.items[weapon].stats["type"] == "dagger"):
			wep_speed_normal = 1.7
		
		# final rage formula
		rage = (((damage / self.rage_factor) * 7.5) + (wep_speed_normal * wep_factor)) / 2		

		self.gain_rage(rage)

		return rage
	
	# generate rage from damage taken
	def generate_rage_taken(self, damage):
		rage = (5/2) * (damage / self.rage_factor)
		self.gain_rage(rage)
		return rage
		

	# whenever we swing or cast, lets try to proc stuff
	def attempt_procs():
		pass

	def normalize_swing(self, weapon, min_dmg, max_dmg, bonus = 0, wep_speed = 2.4):
		damage = random.randint(min_dmg, max_dmg) + bonus

		wep_speed = 2.4 # normalized for 1h non-daggers
		# 1.7 for daggers
		# 2.4 for other one-handed weapons
		# 3.3 for two-handed weapons
		# 2.8 for ranged weapons

		damage += (self.stats['attack_power']) / 14 * wep_speed

		if (weapon == "offhand"):
			damage *= 1 + (.05 * self.talents['dual_wield_specialization']) # talents
			damage /= 2

		return damage

	def apply_flurry(self):
		# update the haste with new / old flurry
		self.flurry = 3
		self.update_haste()

	# now swing with given weapon
	def swing(self, weapon, combat_time, force = False):
		if (combat_time >= self.next_swing[weapon] or force): # force for windfury
			self.next_swing[weapon] = combat_time + self.items[weapon].stats['speed'] # reset swing timer

			# use up a flurry charge
			self.flurry = max(self.flurry - 1, 0)

			# check if we're doing heroic strike
			if (self.queue_heroic_strike):
				self.queue_heroic_strike = False 
				damage, hitType = self.cast("heroic_strike", combat_time)

				if (hitType == "crit"):
					self.apply_flurry()

				return

			# white hit damage
			damage = self.normalize_swing(weapon, self.items[weapon].stats['min_damage'], self.items[weapon].stats['max_damage'])

			# calculate the swing against the hit table
			damage, hitType = self.HitTable.calc_white_hit(damage)

			# generate some rage
			self.generate_rage(damage, weapon, hitType == "crit" and True or False)

			# log this automatically
			self.Sim.log(weapon, damage, hitType)

			if (hitType == "crit"):
				self.apply_flurry()

			# try to proc windfury (yes even off of heroic strike)
			if (combat_time > self.last_wf + 3):
				self.last_wf = combat_time
				roll = random.randint(0, 100)
				if (roll > 20):
					self.stats['attack_power'] += 445
					self.swing("mainhand", combat_time, True) # force a new melee, since we procced WF
					self.stats['attack_power'] -= 445

			# return hit data
			return damage, hitType
		
		return False, False

	def update_gcd(self):
		# change gcd with haste
		self.gcd = max(1, self.base_gcd - ((self.base_gcd / 2) * self.stats['haste']))

	def update_haste(self):
		# print(time.time(), "updating haste")
		# increase weapon speed with haste
		self.items["mainhand"].stats['speed'] = self.items["mainhand"].stats['base_speed'] / ((self.stats['haste']) + 1)
		self.items["offhand"].stats['speed'] = self.items["offhand"].stats['base_speed'] / ((self.stats['haste']) + 1)

		# increase weapons speed with flurry
		if (self.flurry > 0):
			self.items["mainhand"].stats['speed'] = self.items["mainhand"].stats['speed'] / ((100 + 25) / 100)
			self.items["offhand"].stats['speed'] = self.items["offhand"].stats['speed'] / ((100 + 25) / 100)
	
	def off_gcd_check(self, combat_time):
		if (combat_time >= self.next_gcd):
			return True
		return False

	def cast(self, name, combat_time):
		ability = self.Sim.Abilities[name]
		# ability.update(self, self.Target, combat_time)

		# print(combat_time, name, self.off_gcd_check(combat_time), ability.can_cast(combat_time), self.rage >= ability.cost)

		if (self.off_gcd_check(combat_time) and ability.can_cast(combat_time) and self.rage >= ability.cost):

			self.spend_rage(ability.cost)

			# raw damage
			damage = ability.cast(self, self.Target, combat_time)

			# now reduce/filter it
			if (damage == 0 or damage == False):
				hitType = "cast"
			else:
				damage, hitType = self.HitTable.calc_special_hit(damage)

			# log this automatically
			self.Sim.log(name, damage, hitType)

			# log this automatically
			self.Sim.log(name, damage, hitType)

			# print(combat_time, ":", name, "!", damage)

			# ok we're casting it, set the last GCD to now
			if (ability.triggersGCD):
				self.last_gcd = combat_time
				self.next_gcd = combat_time + self.gcd

			return damage, hitType

		return False, False