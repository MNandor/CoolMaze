import pygame

from generate import *

def frame(fps = None):

	if fps == None:
		clock.tick()
	else:
		clock.tick(fps)
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	


size = 30 #number of squares in a line
sqsize = 20 #for drawing
drawframelen = 20*(size/15)**2


clock = pygame.time.Clock()
screen = pygame.display.set_mode((size*sqsize, size*sqsize))
pygame.display.set_caption("RandBoolMaze")

while True:

	maze = generateMaze(size, size) #get fully random maze
	
	#corners must always be walkable
	maze[0][0] = 1
	maze[size-1][size-1] = 1

	#display uncolored
	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if maze[x][y] == 1:
				pygame.draw.rect(screen, (255,255,255), (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))

	frame(60)
	

	bc = [[0,0,0], [255,255,255]]
	#color blocks
	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if maze[x][y] == 1:
				curBlock = len(bc)
				bc += [[random.randint(0,255) for i in range(3)]]
				queue = [(x, y)]
				while len(queue) > 0:
					mx, my = queue[0]
					queue = queue[1:]
					maze[mx][my] = curBlock
					
					if mx-1 >= 0 and maze[mx-1][my] == 1: queue += [(mx-1, my)]
					if my-1 >= 0 and maze[mx][my-1] == 1: queue += [(mx, my-1)]
					if mx+1 < size and maze[mx+1][my] == 1: queue += [(mx+1, my)]
					if my+1 < size and maze[mx][my+1] == 1: queue += [(mx, my+1)]




	#display colored blocks
	for x in range(len(maze)):
		for y in range(len(maze[x])):
			pygame.draw.rect(screen, bc[maze[x][y]], (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))


	frame(1)


	additions = []
	#connections
	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if maze[x][y] == 0:
				neis = []
				if x-1 >= 0: neis += [maze[x-1][y]]
				if y-1 >= 0: neis += [maze[x][y-1]]
				if x+1 < size: neis += [maze[x+1][y]]
				if y+1 < size: neis += [maze[x][y+1]]
				
				
				neis = [x for x in neis if x != 0 and x != 1]
				neis = list(set(neis))
				
				ms = set([tuple(bc[x]) for x in neis])
				if len(ms) > 1:
					#print(neis, neis[0])
					for i in range(1, len(neis)):
						for mx in range(len(maze)):
							for my in range(len(maze[x])):
								if maze[mx][my] == neis[i]:
									maze[mx][my] = neis[0]
									
						bc[neis[i]] = None
					
					maze[x][y] = neis[0]#1
					additions += [(x, y)]

	print(additions)
		
	if maze[0][0] != maze[size-1][size-1]:
		print("Too easy, I won't even bother")
		continue
		#exit()
		


	#draw
	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if (x, y) in additions:
				pygame.draw.rect(screen, (255,255,255), (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))
			else:
				pygame.draw.rect(screen, bc[maze[x][y]], (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))
			
	frame(1)

	for x in range(len(maze)):
		for y in range(len(maze[x])):
			pygame.draw.rect(screen, bc[maze[x][y]], (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))
			
	frame(1)

	#pathfind
	running = True
	queue = [(0,0)]
	parentMap = {(0,0):None}
	visited = []
	while running:
		mx, my = queue[0]
		queue = queue[1:]

		#draw
		for x in range(len(maze)):
			for y in range(len(maze[x])):
				color = bc[maze[x][y]]
				if (x, y) in visited:
					color = (128,128,128)
				if (x, y) in queue:
					color = (255,255,0)
				if (x, y) == (mx, my):
					color = (255,0,0)
				if (x, y) == (size-1, size-1):
					color = (0,0,255)
				if (x, y) == (0,0):
					color = (0,0,255)
					
				pygame.draw.rect(screen, color, (x*sqsize-1, y*sqsize-1, sqsize-2, sqsize-2))

		
		if (mx, my) == (size-1, size-1): break
		
		toAdd = []
		
		if mx-1 >= 0 and (mx-1, my) not in visited and maze[mx-1][my] != 0:
			toAdd += [(mx-1, my)]
		if my-1 >= 0 and (mx, my-1) not in visited and maze[mx][my-1] != 0:
			toAdd += [(mx, my-1)]
		if mx+1 < size and (mx+1, my) not in visited and maze[mx+1][my] != 0:
			toAdd += [(mx+1, my)]
		if my+1 < size and (mx, my+1) not in visited and maze[mx][my+1] != 0:
			toAdd += [(mx, my+1)]
			
		for c in toAdd:
			queue += [c]
			visited += [c]
			parentMap[c] = (mx, my)
		frame(drawframelen)


	nt = parentMap[(size-1, size-1)]
	while nt != (0,0):
		pygame.draw.rect(screen, (0,255,0), (nt[0]*sqsize-1, nt[1]*sqsize-1, sqsize-2, sqsize-2))
		nt = parentMap[nt]
		frame(drawframelen)
		
	pygame.draw.rect(screen, (0,0,0), (0,0, size*sqsize, size*sqsize))
	frame(1)