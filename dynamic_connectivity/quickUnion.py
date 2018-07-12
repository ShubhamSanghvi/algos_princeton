import sys
import os
import re

class quickUnion:
	def __init__(self,size):
		#initialize the grid with the ids
		self.ids = range(0,size)
		self.size = size

	def find(self,p,q):
		return (self.root(p) == self.root(q))

	def union(self,p,q):
		root_p = self.root(p)
		self.ids[root_p] = self.root(q)

	def root(self,id):
		# Loop untill you find a parent
		while(self.ids[id]!=id):
			id = self.ids[id]

		return id


	def view(self):
		print self.size * 4 * '-'
		print "num:", range(0,self.size)
		print "ids:", self.ids
		print self.size * 4 * '-'



def main():

	print "Kar har maidan Fateh!"

	sys.argv = sys.argv[1:]
	
	if not (len(sys.argv) and os.path.isfile(sys.argv[0])):
		print 'ERROR: Please provide a valid path!!'
		print 'usage:\n\tquickUnion <test filename>'
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
	
	grid = quickUnion(N)

	for connection in connections:
		#grid.view()
		is_connected = grid.find(connection[0],connection[1])
		print connection, is_connected
		if not is_connected:
			grid.union(connection[0],connection[1])

	grid.view()


if __name__ == '__main__':
	main()
