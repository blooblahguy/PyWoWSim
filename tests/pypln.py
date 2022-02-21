from loky import get_reusable_executor
import numpy as np
import time

Sims = []

abilities = ["one", "two"]

class SimClass():
	def __init__(self, name):
		self.name = name

def combat_loop(index):
	name = "thread" + str(index)
	Sim = SimClass(name)
	Sim.abilities = abilities

	return Sim

	# Sims.append(Sim)
	# return k

# print([j for j in np.random.random((512, 5))])

# jobs = get_jobs()

start_time = time.time()

executor = get_reusable_executor(max_workers=4)
Sims = list(executor.map(combat_loop, range(10), chunksize=16))

finish_time = time.time()
print("Sim:", "--- %s seconds ---" % round(finish_time - start_time, 3))
