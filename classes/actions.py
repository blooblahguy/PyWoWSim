# action class, will be very helpful
Actions = {}
def add_action(name, callback):
	if not name in Actions:
		Actions[name] = []

	Actions[name].append(callback)

def remove_action(name, callback):
	Actions[name].remove(callback)

def do_action(name, *args):
	try:
		for callback in Actions[name]:
			callback(*args)
	except:
		pass