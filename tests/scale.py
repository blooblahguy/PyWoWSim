from __future__ import division

def renormalize(n, range1, range2):
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]

def convertRange( value, min, max ):
	return (value - min) / (max - min)

# tbcsim
tbcsim_weight = {
	'attack_power': 1, 
	'strength': 2.28, 
	'agility': 1.46, 
	'crit_rating': 1.85, 
	'haste': 1.79, 
	'hit': 1.7, 
	'arpen': 0.31, 
	'expertise': 3.19, 
}

# grox
grox_weight = {
	'attack_power': 3.87, 
	'strength': 8.63, 
	'agility': 5.55, 
	'crit_rating': 8.01, 
	'haste': 7.16, 
	'hit': 5.31, 
	'arpen': 1.34, 
	'expertise': 10.26, 
}

# wowtbc
wowtbc_weight = {
	'attack_power': 3.11, 
	'strength': 6.69, 
	'agility': 4.83, 
	'crit_rating': 6.91, 
	'haste': 5.53, 
	'hit': 4.69, 
	'arpen': 0.98, 
	'expertise': 7.85, 
}

# average
average_weights = {
	'attack_power': 0,
	'strength': 0,
	'agility': 0,
	'crit_rating': 0, 
	'haste': 0,
	'hit': 0,
	'arpen': 0,
	'expertise': 0,
}

#rescale
for key in tbcsim_weight:
	tbcsim_weight[key] = round(convertRange(tbcsim_weight[key], 0, 2.28), 2)
	grox_weight[key] = round(convertRange(grox_weight[key], 0, 8.63), 2)
	wowtbc_weight[key] = round(convertRange(wowtbc_weight[key], 0, 6.69), 2)

	average_weights[key] = round((tbcsim_weight[key] + grox_weight[key] + wowtbc_weight[key]) / 3, 2)


print("tbcsim:", tbcsim_weight)
print("grox:", grox_weight)
print("wowtbc:", wowtbc_weight)
print("average:", average_weights)