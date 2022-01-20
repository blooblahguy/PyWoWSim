import time
import threading
from __init__ import *
# from tkinter import *

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
		Sims[name] = self

	def log(self, name, damage, hitType):
		# damage = hitinfo[0][0] # there's gotta be a better way?
		# hitType = hitinfo[0][1] # there's gotta be a better way?
		if (damage == False):
			return
		
		data = damage_format.copy()
		data['damage'] = damage
		data[hitType] = True
		self.total_dmg += damage

		# place in the log
		self.damage_log[len(self.damage_log) + 1] = [name, data]

	def calculate_totals(self):
		damage = {
			"totals": damage_format.copy(),
			"abilities": {
				"mainhand": damage_format.copy(),
				"offhand": damage_format.copy(),
				"heroic_strike": damage_format.copy(),
				"cleave": damage_format.copy(),
				"bloodthirst": damage_format.copy(),
				"whirlwind": damage_format.copy(),
				"execute": damage_format.copy(),
				"sweeping_strikes": damage_format.copy(),
				"deep_wound": damage_format.copy(),
			},
		}

		# loop through combat log
		for key in self.damage_log:
			name, data = self.damage_log[key]

			damage['totals']['damage'] += data['damage']
			damage['totals']['miss'] += data['miss']
			damage['totals']['crit'] += data['crit']
			damage['totals']['dodge'] += data['dodge']

			damage['abilities'][name] = merge_dmg(damage['abilities'][name], data)

		return damage

def combat_loop():
	# this is a new sim thread
	Sim = SimClass()

	# target
	Target = TargetClass()

	# hit table
	HitTable = HitTableClass()

	# initialize things inside of this thread
	Player = CharacterClass()
	Player.HitTable = HitTable
	Player.Target = Target
	Player.Sim = Sim
	HitTable.Player = Player
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
	Player.equip("Serpentshrine Shuriken", "ranged")

	Player.calculate_stats()

	# start loop
	combat_time = 0
	while (combat_time < settings['combat_seconds']):
		combat_time += settings['per_second'] # increment by number of commands per second (0.1 default)
		combat_time = round(combat_time, 2) # avoid massive floats for readability
		Sim.combat_time = combat_time
		Target.hp = (100 - combat_time / settings['combat_seconds'] * 100) # set target hp

		# anger management
		if (combat_time > Player.last_anger_rage + 3):
			Player.last_anger_rage = combat_time
			Player.gain_rage(1)

		# bloodrage
		# print(combat_time, Player.can_cast("bloodrage", combat_time))
		
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

print("")
print("=================== SIM TOTALS ===================")
for name in Sims:
	Sim = Sims[name]
	# print(name, ":", "--- %s seconds ---" % round(time.time() - Sim.start_time, 3))

	damage = Sim.calculate_totals()
	dps = damage['totals']['damage'] / settings['combat_seconds']

	averages["dps"] += dps
	averages["overcapped_rage"] += Sim.overcapped_rage

	# print(Sim.combat_time)
	# print(round(Sim.overcapped_rage), "rage overcapped")
	# print(round(damage['totals']['damage'], 1), "damage done", round(dps, 1), "dps")
	# print("")

print("sim finals:", "--- %s seconds ---" % round(time.time() - sim_start, 3))
print("Averages")
print("DPS:", round(averages["dps"] / settings['iterations'], 1))
print("Overcap:", round(averages["overcapped_rage"] / settings['iterations']))

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