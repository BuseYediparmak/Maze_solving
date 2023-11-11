#Fadime Buse Yediparmak
#150190053

from algorithms.base import SearchAlgorithmBase

class ids(SearchAlgorithmBase):
    node_parent = {}
    node_cost = {}
    limit = 0

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

    def step(self):
            if(not self.getFrontier()): #if the frontier is empty, it resets the maze and starts again with an increased limit
                self.reset(self._grid,self._start,self._goal)
                self.limit+=1

            if(len(self.getFrontier()) >0):             #if the frontier is not empty, it pops
                current_node = self.getFrontier().pop() #the last node that is added to the frontier
            else:
                current_node = self._start #if frontier is empty, we go to the start node
                self.node_cost.update({current_node:0})
            self._explored.append(current_node) #make the visited node explored

            if current_node == self._goal: #if we reach the goal node, it returns path and cost
                self.get_path(current_node)
                self._done = True
                self._cost = self.node_cost.get(current_node)
                return
            
            if(self.node_cost.get(current_node) < self.limit):
                neighbors=[
                    (current_node[0]-1 , current_node[1]), #up
                    (current_node[0] , current_node[1]-1), #left
                    (current_node[0]+1 , current_node[1]), #down
                    (current_node[0] , current_node[1]+1), #right
                ]#keeps the coordinates of the neighbor nodes
        
                #if the neighbor node is not a wall, visited or already in the frontier, it adds it to frontier
                for neighbor in neighbors:
                    if (not self.isWall(neighbor) and not self.inFrontier(neighbor) and not self.isExplored(neighbor)):
                        self._frontier.append(neighbor)
                        self.node_parent.update({neighbor:current_node})
                        self.node_cost.update({neighbor:self.node_cost.get(current_node)+1})
        
