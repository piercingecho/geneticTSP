import numpy as np

class Path:
    def __init__(self, route):
        self.route = route
        self.cost = -1 # meaning cost not yet calculated

    def __lt__(self, that):
        return self.cost < that.cost
    
    def displayRoute(self):
        s = ""
        for vertex in self.route:
            s += str(vertex)
            s += " "
        return s[:-1]

    def calculateCost(self, G):
        numcities = len(self.route)

        self.cost = 0
        for i in range(numcities - 1):
            self.cost += G[self.route[i]][self.route[i+1]]

        self.cost += G[self.route[0]][self.route[numcities - 1]]

    def costNotCalculated(self):
        return self.cost == -1