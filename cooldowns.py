from classes.actions import *

class CooldownClass:
	def __init__(self, name, callback, cost = 0, cooldown = 0, duration = 0, triggersGCD = True):
		global add_action
		self.name = name
		self.callback = callback
		self.cost = cost
		self.active = False
		self.cooldown = cooldown
		self.duration = duration
		self.triggersGCD = triggersGCD
		self.next_use = 0
		self.last_use = 0
		self.uptime = 0

		add_action("combat_tick_first", self.update)

	# this gets called on every tick to see if we need to remove this cooldown
	def update(self, combat_time, Player, Target):
		if (self.active):
			self.uptime += 0.1

			if (combat_time >= self.expire):
				# print(combat_time, self.name, " being removed")
				self.active = False
				self._remove(combat_time, Player, Target)
				Player.calculate_stats()

	def remaining_cooldown(self, combat_time):
		return self.next_use - combat_time

	def on_cooldown(self, combat_time):
		if (combat_time >= self.next_use or self.next_use == 0):
			return False
		else:
			return True

	def use(self, combat_time, Player, Target):
		if (not self.on_cooldown(combat_time)):
			# print(combat_time, self.name, " being used", self.duration)
			self.active = True
			self.next_use = combat_time + self.cooldown
			self.expire = combat_time + self.duration
			self._apply(combat_time, Player, Target)
			Player.calculate_stats()
			return
	
	def _apply(self, combat_time, Player, Target):
		self.callback(combat_time, Player, Target, "apply")

	def _remove(self, combat_time, Player, Target):
		self.callback(combat_time, Player, Target, "remove")

def create_cooldowns():
	Cooldowns = {}

	# bloodrage
	def bloodrage_tick(combat_time, Player, Target):
		if (Player.bloodrage_active and combat_time >= Player.bloodrage_last + 1):
			Player.gain_rage(1)
			Player.bloodrage_last = combat_time
			Player.bloodrage_total += 1
			if (Player.bloodrage_total >= 10):
				Player.bloodrage_total = 0
				Player.bloodrage_active = False
		pass

	def bloodrage(combat_time, Player, Target, action):
		if (action == "apply"):
			Player.gain_rage(10)
			Player.bloodrage_last = combat_time
			Player.bloodrage_total = 0
			Player.bloodrage_active = True

			add_action("combat_tick_first", bloodrage_tick)
			return 0
		else:
			remove_action("combat_tick_first", bloodrage_tick)
			return False

	#death wish
	def death_wish(combat_time, Player, Target, action):
		if (action == "apply"):
			Player.cooldowns['damage_mult'] += 0.2
			return 0
		else:
			Player.cooldowns['damage_mult'] -= 0.2
			return False

	#heroism
	def heroism(combat_time, Player, Target, action):
		if (action == "apply"):
			Player.cooldowns['haste_rating'] += (15.77 * 30)
			return 0
		else:
			Player.cooldowns['haste_rating'] -= (15.77 * 30)
			return False

	#death wish, also diremug
	def bloodlust_brooch(combat_time, Player, Target, action):
		if (action == "apply"):
			Player.cooldowns['attack_power'] += 278
			return 0
		else:
			Player.cooldowns['attack_power'] -= 278
			return False

	# name, callback, cost = 0, cooldown = 0, duration = 0, triggersGCD = True
	Cooldowns["death_wish"] = CooldownClass("death_wish", death_wish, 10, 180, 30, True)
	Cooldowns["bloodlust_brooch"] = CooldownClass("bloodlust_brooch", bloodlust_brooch, 0, 120, 20)
	Cooldowns["empty_diremug"] = CooldownClass("empty_diremug", bloodlust_brooch, 0, 120, 20)
	Cooldowns["heroism"] = CooldownClass("heroism", heroism, 0, 600, 40)
	Cooldowns["bloodrage"] = CooldownClass("bloodrage", bloodrage, 0, 60, 11)

	return Cooldowns