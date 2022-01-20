import time
import threading
from __init__ import *
# from tkinter import *

def calculate_totals():
	damage = {
		"totals": damage_format.copy(),
		"abilities": {
			"mainhand": damage_format.copy(),
			"offhand": damage_format.copy(),
			"heroic_strike": damage_format.copy(),
			"cleave": damage_format.copy(),
			"bloodthirst": damage_format.copy(),
			"whirlwind_mh": damage_format.copy(),
			"whirlwind_oh": damage_format.copy(),
			"execute": damage_format.copy(),
			"sweeping_strikes": damage_format.copy(),
			"deep_wound": damage_format.copy(),
		},
	}

	# loop through combat log
	for key in log:
		name, data = log[key]

		damage['totals']['damage'] += data['damage']
		damage['totals']['miss'] += data['miss']
		damage['totals']['crit'] += data['crit']
		damage['totals']['dodge'] += data['dodge']

		damage['abilities'][name] = merge_dmg(damage['abilities'][name], data)

	return damage

damage = {
	"mainhand": damage_format.copy,
	"offhand": damage_format.copy,
	"abilities": {
		"heroic_strike": damage_format.copy,
		"cleave": damage_format.copy,
		"bloodthirst": damage_format.copy,
		"whirlwind_mh": damage_format.copy,
		"whirlwind_oh": damage_format.copy,
		"execute": damage_format.copy,
		"sweeping_strikes": damage_format.copy,
		"deep_wound": damage_format.copy,
	},
	"total": 0
}

def combat_loop():
	# thread information
	t = threading.current_thread()
	name = t.name

	# start time and total dmg
	start_time = time.time()
	total_dmg = 0

	# target
	Target = TargetClass()

	# hit table
	HitTable = HitTableClass()

	# initialize things inside of this thread
	Player = CharacterClass()
	Player.HitTable = HitTable
	Player.Target = Target
	HitTable.Player = Player
	Player.equip("Dragonstrike")
	Player.equip("Spiteblade")
	Player.equip("Warbringer Battle-Helm")
	Player.equip("Pendant of the Perilous")
	Player.equip("Warbringer Shoulderplates")
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
	Player.equip("Serpentshrine Shuriken", "ranged")

	Player.calculate_stats()

	# start loop
	combat_time = 0
	while (combat_time < settings['combat_seconds']):
		combat_time += settings['per_second'] # increment by number of commands per second (0.1 default)
		combat_time = round(combat_time, 2) # avoid massive floats

		# set target hp
		Target.hp = (100 - combat_time / settings['combat_seconds'] * 100)

		# auto attack mainhand
		if (Player.swing_ready("mainhand", combat_time)):
			# check if we're doing heroic strike
			damage, hitType = Player.swing("mainhand", combat_time)
			if (damage != False):
				total_dmg += damage
				log_damage("mainhand", damage, hitType)

		# auto attack offhand
		if (Player.swing_ready("offhand", combat_time)):
			damage, hitType = Player.swing("offhand", combat_time)
			if (damage != False):
				total_dmg += damage
				log_damage("offhand", damage, hitType)

		# print(combat_time)
		# START CASTING SPELLS
		# do execute rotation?
		if (Target.hp <= settings['execute_range']):
			pass
		
		# do normal rotation
		# if (Player.rage >= 60):
			# queue heroic strike
			# pass

		# print(combat)

		if (Player.cast("bloodthirst", combat_time, Target)):
			pass

		if (Player.cast("whirlwind", combat_time, Target)):
			pass

		# print(combat_time)

	# log results
	results[name] = "--- %s seconds ---" % round(time.time() - start_time, 3)

	damage = calculate_totals()
	dps = damage['totals']['damage'] / settings['combat_seconds']

	print(damage['totals']['damage'], "damage done", dps, "dps")

combat_loop()

# create combat threads
# threads = []
# for i in range(5):
# 	name = "Thread " + str(i)
# 	t = threading.Thread(name = name, target = combat_loop)
# 	threads.append(t)
# 	t.start()

# # now join them all and finish up
# for t in threads:
# 	t.join()

# # check timings
for res in results:
	print(res, results[res])

# use gui interface
# class Root(Tk):
#     def __init__(self):
#         super(Root,self).__init__()
 
#         self.title("Python Tkinter")
#         self.minsize(500,400)
 
# root = Root()
# root.mainloop()