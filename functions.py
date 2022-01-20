# store results in here
results = {}
log = {}

damage_format = {
	"damage": 0,
	"crit": False,
	"miss": False,
	"dodge": False,
}

def log_damage(name, damage, hitType):
	data = damage_format.copy()
	data['damage'] = damage
	data[hitType] = True
	log[len(log) + 1] = [name, data]

def merge_dmg(dict1, dict2):
	for key in damage_format:
		dict1[key] += dict2[key]
	return dict1