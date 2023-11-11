#Fadime Buse Yediparmak
#150190053

from algorithms.base import SearchAlgorithmBase
import math

class a_star(SearchAlgorithmBase):
    node_parent = {}
    node_cost = {}

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

    def isWall(self, node): #checks if the node is a wall or available to visit
        if(self._grid[node[0]][node[1]] == 1):
            return True
        else:
            return False    
        
    def inFrontier(self, node): #checks if the node is already in frontier
        if not node in self.getFrontier():
            return False
        else: 
            return True
    
    def isExplored(self, node): #checks if the node is already explored
        if node in self.getExplored():
            return True
        else: 
            return False
        
    def get_path(self,node): #finds the final path
        self._path.append(node)
        if node != self._start:
            self.get_path(self.node_parent.get(node))
            
    def ManhattanDistance(self, node): #calculates the manhattan distance
        return abs(self._goal[0] - node[0]) + abs(self._goal[1] - node[1])
    
    def a_star_cost(self,node): #summation of manhattan distance and cost
        return self.node_cost.get(node) + self.ManhattanDistance(node)
        

    def step(self):

        if(len(self.getFrontier()) >0):
            #pops the value that has the smallest A* value and continues to search from that node
            frontier_smallest = self.getFrontier().index(min(self._frontier, key = self.a_star_cost))
            current_node = self.getFrontier().pop(frontier_smallest)
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
                self.node_cost.update({neighbor:self.node_cost.get(current_node)+1})
               
        
