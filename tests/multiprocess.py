from multiprocessing import Process, Manager
import threading
import time

def f(name, Sims):
	Sims[name] = True

if __name__ == '__main__':
	
	with Manager() as manager:
		Sims = manager.dict()

		sim_start = time.time()
		processes = []
		for i in range(500):
			name = "thread "+str(i)
			p = Process(target=f, args=(name, Sims))
			processes.append(p)
			p.start()

		for p in processes:
			p.join()

		print("Sim:", "--- %s seconds ---" % round(time.time() - sim_start, 3))
		# print(Sims)