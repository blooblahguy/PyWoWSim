import random

class HitTableClass():
	def __init__(self):
		self.miss = 28 # dual wielding
		self.dodge = 6.5 # from the back
		self.glance = 24 # flat chance for 73
		self.glance_dr = 25 # flat reduction
		self.crit = 0 # filler stat
		self.modifier = [] # calculate what a diminished or amplified attack should look like
		self.Player = False
		self.Target = False

	def calc_white_hit(self, damage):
		self.glance = 24
		self.miss = 28
		crit_mult = 1 + (2 * (1 + self.Player.stats['crit_mult']) - 1)
		self.modifier = [(100 - self.glance_dr) / 100, crit_mult]
		# print("white", crit_mult)

		return self._calc_hit(damage, False)
		
	def calc_special_hit(self, damage):
		self.glance = 0
		self.miss = 9
		crit_mult = 1 + (2 * (1 + self.Player.stats['crit_mult']) - 1) * (1 + 0.1 * self.Player.talents["impale"])
		self.modifier = [0, crit_mult]
		# print("sepcial", crit_mult)

		return self._calc_hit(damage, True)

	def _calc_hit(self, damage, special):
		if (not self.Player):
			print("error: player not defined in hitTable")
			return

		damage *= self.Player.stats['damage_mult']

		# print(self.miss, self.Player.stats['hit_chance'])
		self.miss = max(self.miss - self.Player.stats['hit_chance'], 0.0)
		self.dodge = 6.5 - min(self.Player.stats['expertise'], 6.5)
		self.crit = self.Player.stats['crit_chance']

		roll = random.randrange(0, 100)
		calc_miss = self.miss
		calc_dodge = self.miss + self.dodge
		calc_glance = self.miss + self.dodge + self.glance
		calc_crit = self.miss + self.dodge + self.glance + self.crit

		# print(roll)
		# if (special):
		# 	print("miss", calc_miss)
		# 	print("dodge", calc_dodge, "(", self.dodge, ")")
		# 	print("glance", calc_glance, "(", self.glance, ")")
		# 	print("crit", calc_crit, "(", self.crit, ")")
		# 	print("remainder", 100 - calc_crit)

		# reduce from armor now
		reduce = 1 - (self.Target.armor / (self.Target.armor - 22167.5 + 467.5 * 70))
		damage *= reduce
		# print(reduce)

		# roll
		if (roll < calc_miss):
			# print(0.0, "miss")
			return 0.0, "miss"
		if (roll < calc_dodge):
			# print(0.0, "dodge")
			return 0.0, "dodge"
		if (roll < calc_glance):
			# print(damage, self.modifier[0], "glance")
			return damage * self.modifier[0], "glance"
		if (roll < calc_crit):
			# print(damage, self.modifier[1], "crit")
			return damage * self.modifier[1], "crit"

		# print(damage, "hit")
		return damage, "hit"