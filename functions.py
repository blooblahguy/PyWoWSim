from structs import *
# store results in here
results = {}
log = {}

# damage_format = {
# 	"damage": 0,
# 	"crit": False,
# 	"miss": False,
# 	"dodge": False,
# }

def log_combat(*args):
	# print(args)
	pass

# def log_damage(name, damage, hitType):
# 	data = damage_format.copy()
# 	data['damage'] = damage
# 	data[hitType] = True
# 	log[len(log) + 1] = [name, data]

# merge two into one new one
def Merge(dict1, dict2):
	res = {}
	for key in dict1:
		if (not key in res):
			res[key] = dict1[key]
		res[key] += dict2[key]
	return res

def merge_dmg(dict1, dict2):
	# print(dict1, dict2)
	for key in dict2:
		dict1[key] += dict2[key]
	return dict1