class TargetClass:
	def __init__(self):
		self.level = 73
		self.armor = 7700
		self.hp = 100
		self.debuffs = {}
		self.debuffs['armor'] = 0
		self.final_armor = self.armor

		self.reduce_armor()

	def reduce_armor(self):
		self.armor -= 610 # faerie fire
		self.armor -= 800 # curse of recklessness
		self.armor -= 3075 # expose weakness