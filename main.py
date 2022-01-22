import time
import threading
from __init__ import *
# from abilities import *
# from structs import *
# from tkinter import *

ability_list = ["mainhand", "offhand"]

Sims = {}
class SimClass():
	def __init__(self):
		t = threading.current_thread()

		self.name = t.name
		self.start_time = time.time()
		self.total_dmg = 0
		self.combat_time = 0
		self.overcapped_rage = 0
		self.damage_log = {}
		self.mins = {}
		self.maxes = {}
		self.last_wf = 0
		self.Abilities = create_abilities()
		Sims[name] = self

		for ability in self.Abilities:
			if not ability in ability_list:
				ability_list.append(ability)

		for ability in ability_list:
			self.mins[ability] = 10000
			self.maxes[ability] = 0

	def log(self, name, damage, hitType):
		if (damage != 0 and damage == False):
			return
		# damage = damage != False and damage or 0

		data = damage_format.copy()
		data['damage'] = damage
		data['casts'] += 1
		if (hitType == "miss"):
			data['misses'] += 1
		elif (hitType == "dodge"):
			data['dodges'] += 1
		elif (hitType == "crit"):
			data['crits'] += 1

		self.total_dmg += damage
		self.total_dmg += damage

		self.mins[name] = damage > 0 and min(self.mins[name], damage) or self.mins[name]
		self.maxes[name] = max(self.maxes[name], damage)

		# place in the log
		self.damage_log[len(self.damage_log) + 1] = [name, data]

	def calculate_totals(self):
		damage = {
			"totals": damage_format.copy(),
			"abilities": {
				"mainhand": damage_format.copy(),
				"offhand": damage_format.copy(),
			},
		}

		for ability in self.Abilities:
			damage['abilities'][ability] = damage_format.copy()

		# loop through combat log
		for key in self.damage_log:
			name, data = self.damage_log[key]

			damage['totals']['damage'] += data['damage']
			damage['totals']['miss'] += data['miss']
			damage['totals']['crit'] += data['crit']
			damage['totals']['dodge'] += data['dodge']

			# print(damage['abilities'], data)

			damage['abilities'][name] = merge_dmg(damage['abilities'][name], data)

		return damage

def combat_loop():
	# this is a new sim thread
	Sim = SimClass()

	# target
	Target = TargetClass()
	Target.armor = 8800 # void reaver
	Target.reduce_armor()

	# hit table
	HitTable = HitTableClass()

	# initialize things inside of this thread
	Player = CharacterClass(Sim)
	Player.HitTable = HitTable
	Player.Target = Target
	HitTable.Player = Player
	HitTable.Target = Target
	Player.equip("Dragonstrike")
	Player.equip("Merciless Gladiator's Slicer")
	Player.equip("Destroyer Battle-Helm")
	Player.equip("Pendant of the Perilous")
	Player.equip("Destroyer Shoulderblades")
	Player.equip("Vengeance Wrap")
	Player.equip("Bloodsea Brigand's Vest")
	Player.equip("Bracers of Eradication")
	Player.equip("Destroyer Gauntlets")
	Player.equip("Red Belt of Battle")
	Player.equip("Destroyer Greaves")
	Player.equip("Warboots of Obliteration")
	Player.equip("Ring of a Thousand Marks", "ring1")
	Player.equip("Ring of Lethality", "ring2")
	Player.equip("Bloodlust Brooch", "trinket1")
	Player.equip("Empty Mug of Direbrew", "trinket2")
	Player.equip("Sunfury Bow of the Phoenix", "ranged")

	Player.calculate_stats()

	# start loop
	combat_time = 0
	while (combat_time < settings['combat_seconds']):
		combat_time += settings['per_second'] # increment by number of commands per second (0.1 default)
		combat_time = round(combat_time, 2) # avoid massive floats for readability
		Sim.combat_time = combat_time
		Target.hp = (100 - combat_time / settings['combat_seconds'] * 100) # set target hp

		# lust first 
		Player.cast("heroism", combat_time)

		# anger management
		if (combat_time > Player.last_anger_rage + 3):
			Player.last_anger_rage = combat_time
			Player.gain_rage(1)
		
		# bloodrage logic
		if (Player.remaining_cooldown("bloodrage", combat_time) == 0 and Player.rage < 30):
			Player.cast("bloodrage", combat_time)
			Player.last_bloodrage = combat_time
			Player.blood_rage_total = 0
			Player.blood_rage_active = True

		# gain rage overtime from bloodrage
		if (Player.blood_rage_active and combat_time > Player.last_bloodrage + 1):
			Player.last_bloodrage = combat_time
			Player.gain_rage(1)
			Player.blood_rage_total += 1
			if (Player.blood_rage_total >= 10):
				Player.blood_rage_total = 0
				Player.blood_rage_active = False


		# lets pop cooldowns first
		# deathwish
		Player.cast("death_wish", combat_time)
		Player.cast("bloodlust_brooch", combat_time)
		if (not Sim.Abilities['bloodlust_brooch'].active):
			Player.cast("empty_diremug", combat_time)

		# trinkets
		# Player.cast("Bloodlust Brooch", combat_time)

		# auto attack mainhand
		if (Player.swing_ready("mainhand", combat_time)):
			# check if we're doing heroic strike
			if (Player.queue_heroic_strike):
				Player.queue_heroic_strike = False 
				Player.items["mainhand"].last_hit = combat_time # reset swing timer
				Player.cast("heroic_strike", combat_time)
			else:
				# if not, then swing mainhand
				Player.swing("mainhand", combat_time)

			# try to proc windfury (yes even off of heroic strike)
			if (combat_time > Sim.last_wf + 3):
				Sim.last_wf = combat_time
				roll = random.randrange(0, 100)
				if (roll > 20):
					Player.stats['attack_power'] += 445
					Player.swing("mainhand", combat_time, True)
					Player.stats['attack_power'] -= 445

		# auto attack offhand
		Player.swing("offhand", combat_time)

		# START CASTING SPELLS
		# do execute rotation?
		if (Target.hp <= settings['execute_range']):
			if (Player.remaining_cooldown("bloodthirst", combat_time) < 2.6 and Player.rage < 30):
				continue # we'll wait for bloodthirst and make sure we have rage

			Player.cast("bloodthirst", combat_time)
			Player.cast("execute", combat_time)

			continue # we've casted execute. nice, move on

		# bloodthirst
		Player.cast("bloodthirst", combat_time)

		# whirlwind
		Player.cast("whirlwind", combat_time)

		# should we heroic strike?
		if (Target.hp > settings['execute_range']): # not during execute
			if ((Player.remaining_cooldown("bloodthirst", combat_time) > 1 and (Player.remaining_cooldown("whirlwind", combat_time) > 1 and Player.rage >= 60)) or Player.rage > 80):
				Player.queue_heroic_strike = True

	# log results
	results[Sim.name] = "--- %s seconds ---" % round(time.time() - Sim.start_time, 3)

	# damage = Sim.calculate_totals()
	# dps = damage['totals']['damage'] / settings['combat_seconds']

	# print(Sim.overcapped_rage, "rage overcapped")
	# print(round(damage['totals']['damage'], 2), "damage done", dps, "dps")

# combat_loop()

# create combat threads
sim_start = time.time()
threads = []
for i in range(settings['iterations']):
	name = "Thread " + str(i)
	t = threading.Thread(name = name, target = combat_loop)
	threads.append(t)
	t.start()

# # # now join them all and finish up
for t in threads:
	t.join()

# check timings
averages = {
	"dps": 0,
	"overcapped_rage": 0,
}

# averages[ability]

# total abilities
for ability in ability_list:
	averages[ability] = {
		"damage": 0,
		"casts": 0,
		"min": 10000,
		"max": 0,
		"unused_off_cooldown": 0,
	}

print("")
print("=================== SIM TOTALS ===================")
for name in Sims:
	Sim = Sims[name]

	damage = Sim.calculate_totals()
	dps = damage['totals']['damage'] / settings['combat_seconds']

	averages["dps"] += dps
	averages["overcapped_rage"] += Sim.overcapped_rage

	# total abilities
	for ability in ability_list:
		averages[ability]['damage'] += damage['abilities'][ability]['damage']
		averages[ability]['casts'] += damage['abilities'][ability]['casts']
		averages[ability]['min'] = min(Sim.mins[ability], averages[ability]['min'])
		averages[ability]['max'] = max(Sim.maxes[ability], averages[ability]['max'])
		try:
			# print(Sim.Abilities[ability].unused_off_cooldown)
			averages[ability]['unused_off_cooldown'] += Sim.Abilities[ability].unused_off_cooldown
		except:
			pass

print("Sim:", "--- %s seconds ---" % round(time.time() - sim_start, 3))
print("DPS:", round(averages["dps"] / settings['iterations'], 1))
print("Rage Overcap:", round(averages["overcapped_rage"] / settings['iterations']))
for ability in ability_list:
	casts = averages[ability]['casts'] / settings['iterations']
	damage = "{:,}".format(round(averages[ability]['damage']) / settings['iterations'])
	min = "{:,}".format(averages[ability]['max'] > 0 and round(averages[ability]['min']))
	max = "{:,}".format(averages[ability]['max'] > 0 and round(averages[ability]['max']))
	unused_off_cooldown = 0
	try:
		unused_off_cooldown = "{:,}".format(round(averages[ability]['unused_off_cooldown']) / settings['iterations'])
	except:
		pass

	if (casts > 0):
		print(ability,": ", "Damage:", damage, "Casts: ", casts, "Min:", min, "Max:", max, "Unused:", unused_off_cooldown)


	# buff uptimes?

	# dodges/misses?

	# item upgrades?

# for res in results:
# 	print(res, results[res])

# use gui interface
# class Root(Tk):
#     def __init__(self):
#         super(Root,self).__init__()
 
#         self.title("Python Tkinter")
#         self.minsize(500,400)
 
# root = Root()
# root.mainloop()