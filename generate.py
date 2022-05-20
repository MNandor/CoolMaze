import random

def generateMaze(w = 20, h = 20):
	ar = [[random.randint(0, 1) for y in range(h)] for x in range(w)]
	
	
	return ar
