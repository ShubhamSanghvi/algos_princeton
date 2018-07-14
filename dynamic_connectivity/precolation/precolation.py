import sys
import random
import pygame
import time
import math
import statistics

# aesthetics 
def draw_grid(vals):
	pygame.init()
	#set color with rgb
	white,black,gray,cyan = (255,255,255),(0,0,0),(100,100,100),(0,160,255)
	#set display
	gameDisplay = pygame.display.set_mode((800,800))
	#Size of squares
	#size = 40
	#size = int(600/(len(vals)*2))
	size = 20

	if(len(vals) > 625):
		print("Out of range for display!!")
		return

	boardLength = int(math.sqrt(len(vals)))
	gameDisplay.fill(white)

	for i in range(1,boardLength+1):
	    for z in range(1,boardLength+1):

	        if vals[((i-1)*boardLength)+(z-1)] == 1 :
	            pygame.draw.rect(gameDisplay, white,[size*z,size*i,size,size])
	        elif vals[((i-1)*boardLength)+(z-1)] == 2:
	            pygame.draw.rect(gameDisplay, cyan, [size*z,size*i,size,size])
	        else:
		        pygame.draw.rect(gameDisplay, black, [size*z,size*i,size,size])

	        pygame.draw.rect(gameDisplay, gray,[size*z,size*i,size,size],1)
	#Add a nice border
	pygame.draw.rect(gameDisplay,black,[size,size,boardLength*size,boardLength*size],1)
	pygame.display.update()


# Primary data structure
class grid_WQU:
	def __init__(self,n):
		self.size = n
		# added 2 for the 2 virtual nodes at the top and bottom
		# n^2 nodes have index from 0 to n^2 -1
		# n^2 is the top node and n^2+1 is the bottom node
		self.ids = [i for i in range(0,(n*n)+2)]
		self.weights = [1 for i in self.ids]
		# 0 is blocked, 1 is open and 2 is flowed(aesthetics)
		# 2 will only be used while visualizing
		self.is_open = [0 for i in self.ids]

		# Managing the 2 virtual sites
		self.top_id = n*n
		self.bottom_id = self.top_id+1

		self.is_open[-2:] = [1,1]

		# connect the first row with the top id
		for i,id in enumerate(self.ids[0:n]):
			self.union(i,self.top_id)

		# connect the bottom row with the bottom id
		for i,id in enumerate(self.ids[-(n+2):-2]):
			# Crap the indexing isnt elegant
			# workaround?
			self.union(i+((n-1)*n),self.bottom_id)


	def disp(self):
		for i,ids in enumerate(self.ids[:-2]):
			if self.root(ids) == self.root(self.top_id):
				self.is_open[i] = 2
		draw_grid(self.is_open)

	def class_print(self):
		print self.size * self.size * 4 * '-'
		print "num:", range(0, (self.size * self.size) + 2)
		print "ids:", self.ids
		print "weights:", self.weights
		print "is_open:", self.is_open
		print self.size * 4 * '-'
		
	def root(self,id):
		if self.ids[id] != id:
			self.ids[id] = self.ids[self.ids[id]]
			id = self.ids[id]
		return id

	def union(self,p,q):
		root_p = self.root(p)
		root_q = self.root(q)

		if root_p != root_q:
			if self.weights[root_p] > self.weights[root_q]:
				self.ids[root_q] = root_p
				self.weights[root_p] += self.weights[root_q]
			else:
				self.ids[root_p] = root_q
				self.weights[root_q] += self.weights[root_p]


	def find(self,p,q):
		return self.root(p) == self.root(q)

	def opensite(self,id):
		if self.is_open[id] != 0:
			#site already open
			return
		
		self.is_open[id] = 1

		# find co-ordinates in the array
		row = id/self.size
		column = id%self.size

		n = self.size

		if (row-1) >= 0:
			id_above = ((row-1)*n) + column
			if self.is_open[id_above]:
				self.union(id,id_above)

		if (row+1) < n:
			id_below = ((row+1)*n) + column
			if self.is_open[id_below]:
				self.union(id,id_below)

		if (column-1) >= 0:
			id_left = (row*n) + column - 1
			if (self.is_open[id_left]):
				self.union(id,id_left)

		if (column+1) < n:
			id_right = (row*n) + column + 1 
			if (self.is_open[id_right]):
				self.union(id,id_right)

	def is_precolated(self):
		return self.find(self.top_id,self.bottom_id)

	def total_opensites(self):
		count = 0
		for i in self.is_open[:-2]:
			if i:
				count += 1
		return count

def main():
	print "Kar har maidan fateh"

	sys.argv = sys.argv[1:]
	
	if not (len(sys.argv) and sys.argv[0].isdigit()):
		print 'ERROR: Please provide  grid size'
		print 'usage:\n\tweightedQuickUnion <grid size> [iteration, default=100]'
		exit()

	N = int(sys.argv[0])

	display_grid = 0;
	if '-d' in sys.argv:
		display_grid = 1;

	if (len(sys.argv)>1 and sys.argv[1].isdigit()) :
		count = int(sys.argv[1])
	else:
		count = 100

	# print "size" , grid.size
	# print grid.ids
	# print len(grid.weights)

	# grid.disp()
	precolation_count = []

	for i in range(0,count):
		grid = grid_WQU(N)
		while not grid.is_precolated():
			id = random.choice(range(0,N*N))
			grid.opensite(id)

		if display_grid:
			grid.disp()
		#print 'YAYYYA YAYYA YAYYAY PERCOLATED'
		#print 'total_opensites(self): ', grid.total_opensites()
		precolation_count.append(grid.total_opensites())

#		raw_input("Paused")

	precolation_count_float = []
	for i,pre_count in enumerate(precolation_count):
	 precolation_count_float.append(float(pre_count) / (N*N))

	mean_test = statistics.mean(precolation_count_float)
	stdev_test = statistics.pstdev(precolation_count_float)

	#print precolation_count_float
	print 'Grid:',N,'x',N,' Count:',count
	print 'Mean:', mean_test
	print 'Std dev:', stdev_test

	range_low = mean_test - (1.96 * stdev_test/math.sqrt(count))
	range_high = mean_test + (1.96 * stdev_test/math.sqrt(count))

	print 'Range: [', range_low,',',range_high,']'

if __name__ == '__main__':
	main()
