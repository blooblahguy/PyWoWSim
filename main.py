import time
import threading
# import cProfile
# import multiprocessing

from __init__ import *

# from abilities import *
# from structs import *
# from tkinter import *

ability_list = ["mainhand", "offhand", "bloodthirst", "whirlwind", "execute", "heroic_strike"]

class SimClass():
	def __init__(self, name):
		# if (name == False):
		# 	t = threading.current_thread()
		# 	self.name = t.name
		# else:
		self.name = name

		self.start_time = time.time()
		self.total_dmg = 0
		self.combat_time = 0
		self.overcapped_rage = 0
		self.damage_log = {}
		self.mins = {}
		self.maxes = {}
		self.last_wf = 0
		self.Abilities = create_abilities()
		self.Cooldowns = create_cooldowns()
		self.uptimes = {}
		Sims[name] = self

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
		if (hitType != "miss" and hitType != "dodge"):
			data['hits'] += 1

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

	def remaining_time(self):
		pass

	def time_until_execute(self):
		if (self.Target.hp < 20): return 0
		if (settings['execute_range'] == 0): return 0
		return settings['combat_seconds'] * (1 - settings['execute_range'] * .01) - self.combat_time

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
	name = threading.current_thread().name
	Sim = SimClass(name)

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
	# print(Player.stats)

	Sim.Target = Target
	Sim.Player = Player

	# start loop
	combat_time = 0
	while (combat_time < settings['combat_seconds']):
		combat_time += settings['per_second'] # increment by number of commands per second (0.1 default)
		combat_time = round(combat_time, 2) # avoid massive floats for readability
		Sim.combat_time = combat_time
		Target.hp = (100 - combat_time / settings['combat_seconds'] * 100) # set target hp

		# action combat tick
		do_action("combat_tick_first", combat_time, Player, Target)

		# anger management
		if (combat_time >= Player.last_anger_rage + 3):
			Player.last_anger_rage = combat_time
			Player.gain_rage(1)

		# lust first 
		Sim.Cooldowns["heroism"].use(combat_time, Player, Target)

		# auto attack mainhand
		Player.swing("mainhand", combat_time)

		# auto attack offhand
		Player.swing("offhand", combat_time)

		## START APL

		# lets pop cooldowns first, prefer to use them during execute
		# deathwish
		if (Sim.time_until_execute() > 180 or Sim.time_until_execute() == 0): # save for execute if we're only getting one
			Sim.Cooldowns["death_wish"].use(combat_time, Player, Target)

		# trinkets
		if (Sim.time_until_execute() > 120 or Sim.time_until_execute() == 0): # save for execute if we're only getting one
			Sim.Cooldowns["bloodlust_brooch"].use(combat_time, Player, Target)
			if (not Sim.Cooldowns['bloodlust_brooch'].active): # these trinkets share a cooldown / active
				Sim.Cooldowns["empty_diremug"].use(combat_time, Player, Target)

		# bloodrage logic
		if (Player.rage < 30):
			Sim.Cooldowns["bloodrage"].use(combat_time, Player, Target)

		# bloodthirst always #1 priority
		Player.cast("bloodthirst", combat_time)

		# EXECUTE ROTATION HERE
		if (Target.hp <= settings['execute_range']):
			if (Sim.Abilities["bloodthirst"].remaining_cooldown(combat_time) < 2 and Player.rage < 20):
				continue # we'll wait for bloodthirst and make sure we have rage
			Player.cast("execute", combat_time)
			continue # we're in execute range, we've casted execute. nice, move on

		Player.cast("whirlwind", combat_time) # whirlwind

		# should we heroic strike?
		if ((Sim.Abilities["bloodthirst"].remaining_cooldown(combat_time) > 1 and Player.rage >= 60) or Player.rage > 70):
			Player.queue_heroic_strike = True

Sims = {}
sim_start = time.time()
threads = []
for i in range(settings['iterations']):
	# name = str("Thread " + str(i))
	t = threading.Thread(target = combat_loop)
	threads.append(t)
	t.start()

# now join them all and finish up
for t in threads:
	t.join()

# check timings
averages = {
	"dps": 0,
	"overcapped_rage": 0,
}

# total abilities
for ability in ability_list:
	averages[ability] = {
		"damage": 0,
		"casts": 0,
		"hits": 0,
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
		averages[ability]['hits'] += damage['abilities'][ability]['hits']
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

# merge mainhand and offhand into one table
ability_list.append('melee')
averages['melee'] = averages['mainhand']
averages['melee']['damage'] += averages['offhand']['damage']
averages['melee']['hits'] += averages['offhand']['hits']
averages['melee']['casts'] += averages['offhand']['casts']
averages['melee']['min'] = min(averages['melee']['min'], averages['offhand']['min'])
averages['melee']['max'] = max(averages['melee']['max'], averages['offhand']['max'])
ability_list.remove('mainhand')
ability_list.remove('offhand')

# order abilities by damage
order = {}
for ability in ability_list:
	damage = round(averages[ability]['damage']) / settings['iterations']
	order[ability] = damage
order = dict(sorted(order.items(), key = lambda kv: kv[1], reverse = True))

# loop through abilities in damage order and display summary
for ability in order:
	average = {
		"damage": (round(averages[ability]['damage']) / settings['iterations']) / 1000,
		"min": (averages[ability]['max'] > 0 and round(averages[ability]['min'])) / 1000,
		"max": (averages[ability]['max'] > 0 and round(averages[ability]['max'])) / 1000,
		"casts": averages[ability]['casts'] / settings['iterations'],
		"hits": averages[ability]['hits'] / settings['iterations'],
	}

	if (average['casts'] > 0):
		print("[bold magenta]"+ability+"[/bold magenta]", average)

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