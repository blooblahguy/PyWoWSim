import random
from functions import *
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
		self.race = "human"
		self.gcd = 1.5

		self.ability_casts = {}
		for key in Abilities:
			self.ability_casts[key] = 0

		# add in all static sources of stats
		self.character_stats = stat_struct.copy() # stats when naked
		self.character_stats["strength"] = 145
		self.character_stats["agility"] = 96
		self.gear_stats = stat_struct.copy() # stats from gear
		self.buffs = stat_struct.copy() # tracking active buffs and stats
		self.procs = {} # tracking procs (active or not) and stats
		self.stats = stat_struct.copy() # final calculated stats

		# formula stats
		self.rage = 0
		self.level = 70
		self.rage_factor = .0091107836 * (self.level ** 2) + 3.225598133 * (self.level) + 4.2652911

		# quick talents
		self.talents = {
			"weapon_mastery": 2,
			"impale": 2,
		}

		self.off_gcd = True
		self.last_gcd = 10

	# add buffs to character
	def apply_buffs(self, combat_time = 0):
		self.buffs = stat_struct.copy()
		for name in Buffs:
			if (Buffs[name].enabled):
				Buffs[name].apply(self, self.Target, combat_time)

	def calculate_buff_stats(self):
		for stat in self.buffs:
			self.stats[stat] += self.buffs[stat]

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

	# talents
	def has_talent(self, name):
		return True
		# return self.talents[name]
	
	###############
	# calculate stats
	###############
	def calculate_stats(self):
		self.stats = stat_struct.copy() # reset calculated stat array

		# naked stats
		self.stats['strength'] = self.character_stats["strength"]
		self.stats['strength'] = self.character_stats["agility"]

		# add gear in
		self.calculate_gear_stats()

		# add talents in
		self.calculate_talent_stats()

		# add buffs in
		self.apply_buffs()
		self.calculate_buff_stats()

		# turn final strength into additional AP
		self.stats_finalize()

		print(self.stats)

	def stats_finalize(self):
		# add gear
		for stat in self.gear_stats:
			self.stats[stat] += self.gear_stats[stat]

		# add buffs
		# for stat in self.buffs:
		# 	self.stats[stat] += self.buffs[stat]

		# calculate hit
		self.stats['hit_chance'] = self.stats['hit_rating'] / 15.77

		# calculate expertise
		self.stats['expertise'] = ((self.stats['expertise_rating'] / 3.9423) * 0.25) + self.talents["weapon_mastery"]

		# calculate crit chance
		self.stats['crit_chance'] = self.stats['crit_rating'] / 22.08
		self.stats['crit_chance'] += self.stats['agility'] / 33

		# calculate haste rating
		self.stats['haste'] = self.stats['haste_rating'] / 15.77

		# lastly add strength to AP
		self.stats['attack_power'] += self.stats['strength'] * 2
	
	# tally talent stats and place in storage
	def calculate_talent_stats(self):
		pass

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
		if (self.race == "human" and (self.items['mainhand'].stats["type"] == "sword" or self.items['mainhand'].stats["type"] == "mace")):
			self.gear_stats['expertise_rating'] += (3.9423 * 5)

	def calculate_proc_stats(self):
		pass

	def gain_rage(self, rage):
		self.rage += rage
		if (self.rage > 100):
			self.Sim.overcapped_rage += self.rage - 100
		self.rage = min(self.rage, 100)
		# print("gain rage", rage)

	def spend_rage(self, rage):
		self.rage -= rage
		if (self.rage < 0):
			print('error with rage going sub 0')
	
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

	# whenever we swing or cast, lets try to proc stuff
	def attempt_procs():
		pass

	def normalize_swing(self, weapon, min_dmg, max_dmg, bonus = 0):
		damage = random.randrange(min_dmg, max_dmg) + bonus
		wep_type = 2.4
		# 1.7 for daggers
		# 2.4 for other one-handed weapons
		# 3.3 for two-handed weapons
		# 2.8 for ranged weapons

		damage += (wep_type * self.stats['attack_power'] / 14)
		if (weapon == "offhand"):
			damage /= 2

		return damage

	# now swing with given weapon
	def swing(self, weapon, combat_time):
		if (self.swing_ready(weapon, combat_time)):
			self.items[weapon].last_hit = combat_time # reset swing timer

			# white hit damage
			damage = self.normalize_swing(weapon, self.items[weapon].stats['min_damage'], self.items[weapon].stats['max_damage'])

			# calculate the swing against the hit table
			damage, hitType = self.HitTable.calc_white_hit(damage)

			# generate some rage
			self.generate_rage(damage, weapon, hitType == "crit" and True or False)

			# return hit data
			return damage, hitType
		
		return False, False

	def remaining_cooldown(self, name, combat_time):
		ability = Abilities[name]
		last_used = self.ability_casts[name]

		return round(float(last_used + ability.cooldown) - combat_time, 2)
	
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

	def cast(self, name, combat_time, triggersGCD = True):
		if (self.can_cast(name, combat_time)):
			ability = Abilities[name]

			# ok we're casting it, set the last GCD to now
			if (triggersGCD):
				self.last_gcd = combat_time
				self.off_gcd = False

			# spend the rage, and put it on cooldown
			self.spend_rage(ability.cost)
			self.ability_casts[name] = combat_time # we casted this, put it on CD

			# raw damage
			damage = ability.cast(self, self.Target)

			# now reduce/filter it
			damage, hitType = self.HitTable.calc_special_hit(damage)
			log_combat(combat_time, name, "!", damage, hitType)

			return damage, hitType


		return False, False



# Player = CharacterClass()
# Player.equip("Dragonstrike")
# Player.equip("Spiteblade")
# Player.equip("Warbringer Battle-Helm")
# Player.equip("Pendant of the Perilous")
# Player.equip("Warbringer Shoulderplates")
# Player.equip("Vengeance Wrap")
# Player.equip("Bloodsea Brigand's Vest")
# Player.equip("Bracers of Eradication")
# Player.equip("Destroyer Gauntlets")
# Player.equip("Red Belt of Battle")
# Player.equip("Destroyer Greaves")
# Player.equip("Warboots of Obliteration")
# Player.equip("Ring of a Thousand Marks", "ring1")
# Player.equip("Ring of Lethality", "ring2")
# Player.equip("Bloodlust Brooch", "trinket1")
# Player.equip("Empty Mug of Direbrew", "trinket2")
# Player.equip("Serpentshrine Shuriken", "ranged")
# Player.calculate_stats()