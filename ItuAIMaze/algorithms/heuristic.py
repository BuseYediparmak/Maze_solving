#Fadime Buse Yediparmak
#150190053

from algorithms.base import SearchAlgorithmBase

class heuristic(SearchAlgorithmBase):
    node_parent = {}
    node_cost = {}
    direction = 0 # 1:up, 2:right, 3:down, 4:left

    def __init__(self):
        super().__init__()

    def reset(self, grid, start, goal):
        self._grid = grid
        self._start = start
        self._goal = goal
        self._frontier = []
        self._explored = []
        self._path = []
        self._cost = 0
        self._done = False
        self.backtracking_dict = {}

    def isWall(self, node):
        if(self._grid[node[0]][node[1]] == 1):
            return True
        else:
            return False    
        
    def inFrontier(self, node):
        if not node in self.getFrontier():
            return False
        else: 
            return True
    
    def isExplored(self, node):
        if node in self.getExplored():
            return True
        else: 
            return False
        
    def get_path(self,node):
        self._path.append(node)
        if node != self._start:
            self.get_path(self.node_parent.get(node))

    def ManhattanDistance(self, node):
        return abs(self._goal[0] - node[0]) + abs(self._goal[1] - node[1])
    
    def a_star_cost(self,node):
        return self.node_cost.get(node) + self.ManhattanDistance(node)
        
    def find_direction(self, node, parent): #finds the moving direction
        if node[0]<parent[0]:
            return 1
        elif node[1]>parent[0]:
            return 2
        elif node[0]>parent[0]:
            return 3
        elif node[1]<parent[1]:
            return 4

    def step(self):

        if(len(self.getFrontier()) >0):
            frontier_smallest = self.getFrontier().index(min(self._frontier, key = self.a_star_cost))
            current_node = self.getFrontier().pop(frontier_smallest)
            parent= self.node_parent.get(current_node)
            self.direction = self.find_direction(current_node,parent)
            #keeps the direction so we can understand when it changes

        else:
            current_node = self._start
            self.node_cost.update({current_node:0})

        self._explored.append(current_node)

        if current_node == self._goal:
            self.get_path(current_node)
            self._done = True
            self._cost = self.node_cost.get(current_node)
            return
        
        neighbors=[
            (current_node[0]-1 , current_node[1]), #up
            (current_node[0] , current_node[1]-1), #left
            (current_node[0]+1 , current_node[1]), #down
            (current_node[0] , current_node[1]+1), #right
        ]

        for neighbor in neighbors:
            if (not self.isWall(neighbor) and not self.inFrontier(neighbor) and not self.isExplored(neighbor)):
                self._frontier.append(neighbor)
                self.node_parent.update({neighbor:current_node})
                new_direction = self.find_direction(neighbor,current_node)
                if(new_direction == self.direction or self.direction == 0):
                    self.node_cost.update({neighbor:self.node_cost.get(current_node)+1})
                else:
                    self.node_cost.update({neighbor:self.node_cost.get(current_node)+4})
                    #adds more cost for turning
             