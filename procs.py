# placeholder function for procs that aren't complete
def undefined(name, Player, Target):
	print("callback undefined")

Procs = {} # main proc dict

# 
class ProcClass():
	def __init__(self, name, on_applied, on_expired):
		self.name = name
		self.cooldown = 0
		self.last_proc = 0
		self.proc_chance = 0
		self.duration = 0
		self.on_applied = on_applied
		self.on_expired = on_expired
		# self.on_proc = 0
		# self.on_unproc = 0

	def attempt_trigger(self):
		pass

	def expire(self):
		pass


# windfury
# "windfury_totem": buff_struct.copy(),