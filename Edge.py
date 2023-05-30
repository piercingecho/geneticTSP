class Edge:
    def __init__(self, i, j, G):
        self.edge = (i,j)
        self.weight = G[i][j]
    def __lt__(self, that):
        return self.weight < that.weight
    
    def otherEdge(self, i):
        if(i == self.edge[0]):
            return self.edge[1]
        elif (i == self.edge[1]):
            return self.edge[0]
        else:
            return -1