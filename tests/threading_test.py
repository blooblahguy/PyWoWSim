import threading
import time

Sims = {}

def f(name):
	Sims[name] = True

sim_start = time.time()
processes = []
for i in range(5000):
	name = "thread "+str(i)
	p = threading.Thread(target=f, args=(name, ))
	processes.append(p)
	p.start()

for p in processes:
	p.join()

print("Sim:", "--- %s seconds ---" % round(time.time() - sim_start, 3))
# print(Sims)