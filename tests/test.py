
def arpen_damage(arpen):
	armor = 7200 # base
	armor -= 2600 # sunder
	armor -= 610 # faerie fire
	armor -= 800 # curse of reck

	armor -= arpen

	mit = (armor / (armor - 22167.5 + 467.5 * 73))

	print(mit)

arpen_damage(700)
