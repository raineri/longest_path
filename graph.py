class Point:
	x = None
	y = None
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __repr__(self):
		return "P(%s, %s)" % (self.x, self.y)

class Vertex:
	row = None
	pos = None
	tree = None
	children = None
	point = None
	
	def __init__(self, row, pos, tree=None):
		self.row = row
		self.pos = pos
		self.tree = tree
		
	def __repr__(self):
		return "V(%s)" % (self.tree[self.row][self.pos])
		
	def __str__(self):
		return "V(%s)" % (self.tree[self.row][self.pos])
		
	def get_value(self, G=None):
		if G == None:
			return self.tree[self.row][self.pos]
		else:
			return G[self.row][self.pos]
		
	def get_position(self):
		return (self.pos, self.row)
		
class Edge:
	source = None
	destination = None
	weight = None
	
	def __init__(self, source=None, destination=None, weight=None):
		self.source = source
		self.destination = destination
		self.weight = weight
		
	def length(self, length_to):
		return length_to[self.source] + self.weight
		
	def get_path(self):
		return "%s->%s" % (self.source.get_value(), self.destination.get_value())
		
	def __repr__(self):
		return "E(%s->%s)" % (self.source.get_value(), self.destination.get_value())
		
		
class LongestPath:
	vertex_tree = []
	vertex_list = []
	length_to = {}
	sum_to = {}
	edge_hash = {}
	vertex_hash = {}
	cordinate_hash = {}
	path = {}
	max_edge = {"id": None, "value": None}
	line_path = []
	P = []
	VP = []
	seed = None
	sum = 0
	display_width = 1440
	display_height = 750
	tree = None

	def __init__(self, data=None):
		self.vertex_tree = []
		self.vertex_list = []
		self.length_to = {}
		self.sum_to = {}
		self.edge_hash = {}
		self.vertex_hash = {}
		self.cordinate_hash = {}
		self.path = {}
		self.max_edge = {"id": None, "value": None}
		self.line_path = []
		self.P = []
		self.VP = []
		self.seed = None
		self.sum = 0
		self.display_width = 1440
		self.display_height = 750
		self.tree = None

		data = self.generate_tree()
		data = data.split('\n')

		# create initial tree
		self.tree = []
		for ln in data:
			ln = ln.strip().split(' ')
			if ln[0] == '':
				continue
			tmp = []
			for el in ln:
				tmp.append(int(el))
			self.tree.append(tmp)
		print self.tree

		# create vertex tree
		for row in range(0, len(self.tree)):
			self.vertex_tree.append([])
			for pos in range(0, len(self.tree[row])):
				v = Vertex(row, pos, self.tree)
				self.vertex_tree[row].append(v)

		# create vertex and edge list
		for row in range(0, len(self.vertex_tree)):
			for pos in range(0, len(self.vertex_tree[row])):
				self.length_to[self.vertex_tree[row][pos]] = 0
				self.sum_to[self.vertex_tree[row][pos]] = 0
				self.vertex_list.append(self.vertex_tree[row][pos])
				if row < len(self.vertex_tree)-1:
					self.vertex_tree[row][pos].children = [self.vertex_tree[row+1][pos], self.vertex_tree[row+1][pos+1]]
					print row, pos
					edge_1 = Edge(self.vertex_tree[row][pos], self.vertex_tree[row+1][pos], self.tree[row][pos]+self.tree[row+1][pos])
					edge_2 = Edge(self.vertex_tree[row][pos], self.vertex_tree[row+1][pos+1], self.tree[row][pos]+self.tree[row+1][pos+1])
					self.edge_hash[self.vertex_tree[row][pos]] = [edge_1, edge_2]

		# calculate the largest path
		self.seed = self.vertex_tree[0][0]
		for vertex in self.vertex_list:
			try:
				for edge in self.edge_hash[vertex]:
					if self.length_to[edge.destination] <= self.length_to[edge.source] + edge.weight:
						self.length_to[edge.destination] = self.length_to[edge.source] + edge.weight
						if edge.source == self.seed:
							self.sum_to[edge.destination] = edge.source.get_value() + edge.destination.get_value()
						else:
							self.sum_to[edge.destination] = self.sum_to[edge.source] + edge.destination.get_value()
			except KeyError:
				pass

		# find the maximum sum
		max = self.seed
		for v in self.length_to:
				if self.length_to[v] > self.length_to[max]:
					max = v
				else:
					continue
		self.sum = self.sum_to[max]
		print self.sum

		# calculate the x, y position for the nodes		
		start = self.display_width/2-(self.display_width/4)
		previous_point = None
		for row in range(0, len(self.vertex_tree)):	
			for pos in range(0, len(self.vertex_tree[row])):
				x = start+(pos+1)*60
				y = (self.display_height/4)+(row*40)
				self.vertex_tree[row][pos].point = Point(x,y)
			start -= 30

		# find the relation of the nodes and their connecting edge
		R = []; A = []
		for x in self.vertex_tree:
			for vertex in x:
				try:
					for edge in self.edge_hash[vertex]:
						A.append(edge.length(self.length_to))
						R.append((edge.destination, edge.source, edge))
						if self.vertex_hash.has_key(edge.destination):
							if self.vertex_hash[edge.destination].length(self.length_to) <= edge.length(self.length_to):
								self.vertex_hash[edge.destination] = edge
						else:
							self.vertex_hash[edge.destination] = edge		
				except KeyError:
					pass

		# find the highest weighted node
		for i in range(0,len(R)):
			if A[i] > self.max_edge['value']:
				self.max_edge["id"] = R[i][2]
				self.max_edge["value"] = A[i]

		# record the path back towards the top
		self.path = []
		current_vertex = self.max_edge['id'].destination
		while current_vertex != self.seed:
			self.path.append(self.vertex_hash[current_vertex])
			current_vertex = self.vertex_hash[current_vertex].source
		self.path.reverse()

		# P contains the cordinates of all nodes
		for row in range(0, len(self.vertex_tree)):	
			for pos in range(0, len(self.vertex_tree[row])):
				if self.vertex_tree[row][pos].children != None:
					for node in self.vertex_tree[row][pos].children:
						self.P.append((self.vertex_tree[row][pos].point, node.point))

		# find the x, y cordinate for the second graph
		start = self.display_width/2+(self.display_width/8)
		for row in range(0, len(self.vertex_tree)):	
			for pos in range(0, len(self.vertex_tree[row])):
				for edge in self.path:
					if (self.vertex_tree[row][pos] == edge.source) or (self.vertex_tree[row][pos] == edge.destination):
						x = start+(pos+1)*60
						y = (self.display_height/4)+(row*40)
						p = Point(x,y)
						self.line_path.append(p)
						self.cordinate_hash[p] = self.vertex_tree[row][pos]
			start -= 30

		# VP contains the list of a all nodes
		for row in range(0, len(self.vertex_tree)):	
			for pos in range(0, len(self.vertex_tree[row])):
				self.VP.append(self.vertex_tree[row][pos])

	def generate_tree(self):
		import random
		li = ['']
		for i in range(0,random.randint(3,15)):
			for j in range(0,i):
				li.append(str(random.randint(1,99)))
			li.append('\n')
		return ' '.join(li)