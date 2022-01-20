def armor_test(armor, level):
	DR = armor / (armor - 22167.5 + 467.5 * level)
	return DR

def armor_test_2(armor, level):
	return 1 - (10557.5 / (10557.5 + armor))
	