import pygame
import numpy
from os.path import exists, dirname, join

from .utils import *

class maze:

    window_size = (706, 706)
    cell_properties = {"height":20,"width":20,"margin":2}
    sizes = (33,33)
    timeout = 100000
    done = False
    found = False
    start_exist = False
    end_exist = False
    start = None
    end = None
    algorithm = None
    algorithm_name = ""
    path = []

    def __init__(self, algorithm_name="") -> None:
        self.loadAlgorithm(algorithm_name,initial=True)
        pygame.init()
        pygame.display.set_caption("MAZE")
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.grid = numpy.zeros(self.sizes)
        self.drawingLoop()

    def __del__(self) -> None:
        pygame.quit()

    def loadAlgorithm(self, algorithm_name, initial=False):
        module = "algorithms."+algorithm_name
        if exists(join(dirname(dirname(__file__)),"algorithms",algorithm_name)+".py"):
            m = __import__(module)
            algo = getattr(m, algorithm_name)
            self.algo = getattr(algo, algorithm_name)
            self.algorithm_name = algorithm_name
            print(algorithm_name, "is loaded")
        else:
            self.algorithm_name = ""
            if not initial:
                print("No algorithm loaded. Could not find",algorithm_name, "algorithm")
            else:
                print("No algorithm loaded")
            return False
        return True

    def savegrid(self) -> None:
        numpy.savetxt("./mazes/maze.txt",self.grid)

    def loadgrid(self, path) -> None:
        self.grid = numpy.loadtxt(path)
        for row in range(self.sizes[0]):
            for column in range(self.sizes[1]):
                if self.grid[row][column] == 2:
                    self.start_exist = True
                    self.start = (row,column)
                elif self.grid[row][column] == 3:
                    self.end_exist = True
                    self.end = (row,column)

    def resetgrid(self,fill=False) -> None:
        if fill:
            self.grid = numpy.ones(self.sizes)
        else:
            self.grid = numpy.zeros(self.sizes)
        self.start_exist = False
        self.end_exist = False

    def runAlgorithm(self):
        if self.algorithm_name == "":
            print("No algorithm selected")
            return
        self.algorithm = self.algo()
        if not self.start_exist:
            print("Start position is not set")
        elif not self.end_exist:
            print("End position is not set")
        else:
            count = 0
            self.algorithm.reset(self.grid, self.start, self.end)
            while count<self.timeout and not self.algorithm.isDone():
                pygame.event.get() #to prevent freezing
                self.algorithm.step()
                self.draw()
            if count>=self.timeout:
                print("Timeout")
            else:
                print("Found Path with", self.algorithm.getCost(),"cost")
                print("Expanded", self.algorithm.getNumberOfExpanded(),"nodes")
                all_path = self.algorithm.getPath()
                for p in all_path:
                    self.path.append(p)
                    self.draw()

    def draw(self) -> None:
        f = []
        e = []
        if self.algorithm:
            f = self.algorithm.getFrontier()
            e = self.algorithm.getExplored()
            
        self.screen.fill(colors[-1])
        for row in range(self.sizes[0]):
            for column in range(self.sizes[1]):
                if self.grid[row][column] in colors:
                    if (row,column) in self.path:
                        color = colors[6]
                    elif (row,column) in e:
                        color = colors[5]
                    elif (row,column) in f:
                        color = colors[4]
                    else:
                        color = colors[self.grid[row][column]]
                pygame.draw.rect(self.screen, color, 
                [self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["width"]) * column, 
                self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["height"]) * row, 
                self.cell_properties["width"], self.cell_properties["height"]])
        pygame.display.flip()
        self.clock.tick(60)

    def drawingLoop(self) -> None:
        while not self.done:
            self.draw()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.done = True
                    break
                elif event.type == pygame.KEYDOWN:
                    self.algorithm = None
                    self.path = []
                    if event.key == pygame.K_ESCAPE:
                            print("Exit")
                            pygame.quit()
                            self.done = True
                            break
                    elif event.key == pygame.K_a:
                        algorithm = input("Enter the algorithm:")
                        print("Loading",algorithm)
                        self.loadAlgorithm(algorithm)
                    elif event.key == pygame.K_f:
                        print("Filling Maze")
                        self.resetgrid(fill=True)
                    elif event.key == pygame.K_r:
                        print("Reseting Maze")
                        self.resetgrid(fill=False)
                    elif event.key == pygame.K_s:
                        print("Saving Maze")
                        self.savegrid()
                    elif event.key == pygame.K_l:
                        print("Loading Maze")
                        self.loadgrid("./mazes/maze.txt")
                    elif event.key == pygame.K_RETURN:
                        self.runAlgorithm()
                    else:
                        index = pygame.key.name(event.key)
                        path = "./mazes/maze{}.txt".format(index)
                        if exists(path):
                            print("Loading Maze {}".format(index))
                            self.loadgrid(path)
                        else:
                            print("Maze {} does not exist".format(index))
                elif pygame.mouse.get_pressed()[0]: #left click
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (self.cell_properties["width"] + self.cell_properties["margin"])
                    row = pos[1] // (self.cell_properties["height"] + self.cell_properties["margin"])
                    if(self.grid[row][column] == 2):
                        self.start_exist = False
                    elif(self.grid[row][column] == 3):
                        self.end_exist = False
                    self.grid[row][column] = 1
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (self.cell_properties["width"] + self.cell_properties["margin"])
                    row = pos[1] // (self.cell_properties["height"] + self.cell_properties["margin"])
                    
                    if(self.grid[row][column] == 2):
                        self.grid[row][column] = 0
                        self.start_exist = False
                    elif(self.grid[row][column] == 3):
                        self.grid[row][column] = 0
                        self.end_exist = False
                    elif(not self.start_exist):
                        self.grid[row][column] = 2
                        self.start_exist = True
                        self.start = (row,column)
                    elif(not self.end_exist):
                        self.grid[row][column] = 3
                        self.end_exist = True
                        self.end = (row,column)
                    else:
                        self.grid[row][column] = 0