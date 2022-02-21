from multiprocessing import Pool

class SimClass():
	def __init__(self, name):
		self.name = name

def f(index):
	name = "thread "+str(index)
	Sim = SimClass(name)
	return Sim

if __name__ == '__main__':
	Sims = []
	with Pool(500) as p:
		# print(f)
		Sims = p.map(f, range(1, 5))
		print(Sims)