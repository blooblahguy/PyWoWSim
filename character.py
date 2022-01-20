import random
from __init__ import *

# 15.77 Hit Rating = 1% Hit
# 3.9423 Expertise Rating = 1 Expertise = -0.25% Dodge/Parry
# 22.08 Crit Rating = 1% Crit
# 15.77 Haste Rating = 1% Haste
# 1 Strength = 2 Attack Power
# 33 Agility = 1% Crit

class CharacterClass:
	def __init__(self):
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

		# naked stats for level 70
		self.naked = stat_struct.copy()
		self.naked["strength"] = 145
		self.naked["agility"] = 96
		self.isHuman = True
		self.gcd = 1.5

		self.ability_casts = {}
		for key in Abilities:
			self.ability_casts[key] = 0

		# add in all static sources of stats
		self.base = stat_struct.copy()

		# calculated stats, take naked, base, buffs, and procs to calculate final values
		self.final_stats = stat_struct.copy()

		# active buffs
		self.buffs = {}

		# formula stats
		self.rage = 0
		self.level = 70
		self.rage_factor = .0091107836 * (self.level ** 2) + 3.225598133 * (self.level) + 4.2652911

		self.off_gcd = True
		self.last_gcd = 10

	# equip item to character
	def equip(self, itemName, slot = False):
		if (not slot):
			slot = items[itemName].slot
		self.items[slot] = items[itemName]

		# add item stats to base
		for stat in items[itemName].stats:
			value = items[itemName].stats[stat]

			# add itemstats to character
			try:
				self.base[stat] += value
			except:
				pass

	# unequip and remove stats
	def unequip(self, itemName, slot = False):
		if (not slot):
			slot = items[itemName].slot
		self.items[slot] = False

		# remove item stats from base
		for stat in items[itemName].stats:
			value = items[itemName].stats[stat]

			# add itemstats to character
			try:
				self.base[stat] -= value
			except:
				pass

	# talents
	def has_talent(self, name):
		return self.talents[name]
	
	###############
	# calculate stats
	###############
	def calculate_stats(self):
		self.final_stats = stat_struct.copy()

		# bring in talents, they may modify everything
		self.talents = {
			"weapon_mastery": 2,
			"impale": 2,
		}

		self.calculate_base_stats()

		# add gear in
		self.calculate_gear_stats()

		# convert ratings to percentages
		self.calculate_crit_chance()
		self.calculate_expertise_chance()
		self.calculate_haste()
		self.calculate_hit_chance()

	def calculate_base_stats(self):
		# add in simple base stats
		for stat in self.base:
			self.final_stats[stat] += self.base[stat]
		
		# add in buffs

	def calculate_crit_chance(self):
		crit_chance = 0
		crit_chance += self.final_stats['crit_rating'] / 22.08
		crit_chance += self.final_stats['agility'] / 33
		self.final_stats['crit_chance'] = crit_chance
		self.final_stats['crit_mult'] = 2
	def calculate_expertise_chance(self):
		# add expertise if human
		if (self.isHuman and (self.items['mainhand'].stats["type"] == "sword" or self.items['mainhand'].stats["type"] == "mace")):
			self.final_stats['expertise_rating'] += (3.9423 * 5)

		# now calculate chance to remove dodge from rating
		expertise = ((self.final_stats['expertise_rating'] / 3.9423) * 0.25) + self.has_talent("weapon_mastery")

		# cap this out at 6.5
		self.final_stats['expertise'] = min(expertise, 6.5)
	def calculate_haste(self):
		self.final_stats['haste'] = self.final_stats['haste_rating'] / 15.77
	def calculate_hit_chance(self):
		self.final_stats['hit_chance'] = self.final_stats['hit_rating'] / 15.77
	
	def calculate_gear_stats(self):
		for slot in self.items:
			item = self.items[slot]
			if (item):
				for stat in item.stats:
					try:
						self.final_stats[stat] += item.stats[stat]
					except:
						pass

	def calculate_buff_stats():
		pass

	def calculate_proc_stats():
		pass

	def calculate_ap(self):
		# self.stats['attack_power'] = 
		pass
		# return self.base['attack_power'] + ((self.base['strength'] + self.bonus_stats['strength']) * 10)

	def gain_rage(self, rage):
		self.rage += rage
		self.rage = min(self.rage, 100)
	
	# generate rage from auto attack
	def generate_rage(self, damage, weapon, crit = False):
		# weapon rage factor from mh/oh crit/nocrit
		wep_factor = 0
		if (weapon == "mainhand"):
			wep_factor = 3.5
			if (crit):
				wep_factor = 7
		elif (weapon == "offhand"):
			wep_factor = 1.75
			if (crit):
				wep_factor = 3.50

		# normalized weapon speed
		wep_speed = 2.4
		# if (self.items[weapon]["type"] == "1h"):
		# 	wep_speed = 2.4
		# elif (self.items[weapon]["type"] == "2h"):
		# 	wep_speed = 3.3
		# elif (self.items[weapon]["type"] == "dagger"):
		# 	wep_speed = 1.7
		
		# final rage formula
		rage = (((damage / self.rage_factor) * 7.5) + (wep_speed * wep_factor)) / 2

		self.gain_rage(rage)

		return rage
	
	# generate rage from damage taken
	def generate_rage_taken(self, damage):
		rage = (5/2) * (damage / self.rage_factor)
		self.gain_rage(rage)
		return rage

	# check if we're allowed to swing at all
	def swing_ready(self, weapon, combat_time):
		if combat_time > self.items[weapon].last_hit + self.items[weapon].stats['speed']:
			return True
		return False

	# now swing with given weapon
	def swing(self, weapon, combat_time):
		if (self.swing_ready(weapon, combat_time)):
			self.items[weapon].last_hit = combat_time # reset swing timer

			# X is:
			# 1.7 for daggers
			# 2.4 for other one-handed weapons
			# 3.3 for two-handed weapons
			# 2.8 for ranged weapons

			# average / random out the weapon damage
			damage = random.randrange(self.items[weapon].stats['min_damage'], self.items[weapon].stats['max_damage'])
			# add ap modifer
			damage = damage + (2.4 * self.final_stats['attack_power'] / 14)
			# reduce damage if offhand
			if (weapon == "offhand"):
				damage /= 2
			
			# calculate the swing against the hit table
			damage, hitType = HitTable.calc_white_hit(damage)

			# generate some rage
			self.generate_rage(damage, weapon, hitType == "crit" and True or False)

			# return hit data
			return damage, hitType
		
		return False, False
	
	def can_cast(self, name, combat_time):
		# off gcd?
		if (self.off_gcd or combat_time >= float(self.last_gcd + self.gcd)):
			self.off_gcd = True

			ability = Abilities[name]
			last_used = self.ability_casts[name]

			# can we afford it?
			if (ability.cost > self.rage):
				return False # no
			# is it off cooldown?
			
			if (combat_time < float(last_used + ability.cooldown)):
				return False
			
			return True
			
		self.off_gcd = False
		return False

	def cast(self, name, combat_time, Target):
		if (self.can_cast(name, combat_time)):
			# ok we're casting it, set the last GCD to now
			self.last_gcd = combat_time
			self.off_gcd = False

		# 	# print(combat_time)
		# 	# print(self.last_gcd, combat_time)
		# 	# self.last_gcd = combat_time
		# 	# print("cast!")
		# 	# self.off_gcd = False

		# 	self.rage -= self.cost
		# 	self.ability_casts[name] = combat_time

			ability = Abilities[name]
			damage = ability.cast(self, Target)
			print(name, "!", damage)

		# return False