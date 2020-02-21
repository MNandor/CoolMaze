import random

def generateMaze(w = 20, h = 20):
	ar = [[random.randint(0, 1) for x in range(w)] for y in range(h)]
	
	
	return ar