import sys
import os
import re

class quickFind:
	def __init__(self,size):
		#initialize the grid with the ids
		self.ids = range(0,size)
		self.size = size

	def find(self,p,q):
		return self.ids[p] == self.ids[q]

	# Note that a single union command has a worst-case timing
	# of accessing all the elemets of the grid which is O(N)
	# for N such union commands, the cost will be N*N = N^2
	# Qudratic is anathema to programmers

	def union(self,p,q):
		change_id = self.ids[p]
		target_id = self.ids[q]
		if not change_id == target_id:
			for id in range(0,self.size):
				if self.ids[id] == change_id:
					self.ids[id] = target_id

	def view(self):
		print self.size * 4 * '-'
		print "num:", range(0,self.size)
		print "ids:", self.ids
		print self.size * 4 * '-'



def main():

	print "Kar har maidan Fateh!"

	# remove the name of the program from arg list
	# TODO: use argparse when using more arguments

	sys.argv = sys.argv[1:]
	
	if not (len(sys.argv) and os.path.isfile(sys.argv[0])):
		print 'ERROR: Please provide a valid path!!'
		print 'usage:\n\tquickFind <test filename>'
		exit()

	testfile = open(sys.argv[0],'r')
	contents = testfile.read()
	match = re.search(r'^(\d+)\n',contents)
	
	if match:
		N = int(match.group(1))
	else:
		print 'ERROR: Test file does not have grid size on first line.'
		print 'Please provide a valid test file'
		print 'Exiting...'
		exit()

	connections_str = re.findall(r'^(\d+),(\d+)$',contents,re.MULTILINE)
	connections = [ (int(x),int(y))for (x,y) in connections_str]
	
	grid = quickFind(N)

	for connection in connections:
		is_connected = grid.find(connection[0],connection[1])
		print connection, is_connected
		if not is_connected:
			grid.union(connection[0],connection[1])

	grid.view()


if __name__ == '__main__':
	main()
