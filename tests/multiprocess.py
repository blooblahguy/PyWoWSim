from msilib.schema import Class
import multiprocessing

class Classtest():
	def __init__(self):
		self.name = "class"


# def test(threadnum, globalarray):
# 	print("hello world")
# 	# classtest = Classtest()
# 	globalarray.append("test")

# if __name__ == '__main__':
# 	globalarray = []
# 	threads = []
# 	for i in range(5):
# 		t = Process(target = test, args = (i, globalarray))
# 		threads.append(t)
# 		t.start()

# 	# await all before continueing
# 	for thread in threads:
# 		thread.join()

# 	print(globalarray)

Sims = {}

def combat_loop(name, queue):
	Sims = queue.get()
	Sims[name] = True

	queue.put(Sims)

if __name__ == '__main__':
	queue = multiprocessing.Queue()
	queue.put(Sims)
	threads = []
	for i in range(5):
		name = "thread " + str(i)
		t = multiprocessing.Process(target = combat_loop, args=(name, queue))
		threads.append(t)
		t.start()

	for thread in threads:
		t.join()

	print(queue.get())
