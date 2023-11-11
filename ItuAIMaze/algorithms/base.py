class SearchAlgorithmBase:
    _frontier = []
    _explored = []
    _path = []
    _cost = 0
    _grid = None
    _done = False
    _goal = None
    _start = None
    def __init__(self) -> None:
        pass
    def isDone(self) -> bool:
        return self._done
    def getFrontier(self) -> list:
        return self._frontier
    def getExplored(self) -> list:
        return self._explored
    def getPath(self) -> list:
        return self._path
    def getCost(self) -> int:
        return self._cost
    def getNumberOfExpanded(self) -> int:
        return len(self._explored)
    def reset(self, grid, start, goal):
        pass
    def step(self):
        pass