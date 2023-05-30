import numpy as np
from Path import *
import matplotlib.pyplot as plt

def plot_output(best_tours, num_cities):

    x_data = np.array(list(i for i in range(len(best_tours))))
    y_data = list(path.cost for path in best_tours)

    plt.plot(x_data, y_data, linestyle='-', marker='o')
    plt.xlabel('Generation number ($N$)')
    plt.ylabel('Total Tour Distance')
    plt.title('Solution Quality over Time')
    plt.ylim(0, num_cities * 2)
    fig = plt.gcf() # In order to save, this line MUST be in the same cell as plt.plot()!
    fig.savefig("fig.png")

def util_get_input(s, minval):
    while True:
        # exit when try statement succeeds
        try:
            num = float(input("Please input " + s + ", >=" + str(minval) + ": "))
            if(num < minval):
                raise ValueError()
            return num
        except:
            print("Invalid input.")


def initializePaths(num_paths, num_cities):
    paths = []
    for i in range(num_paths):
        curr = np.array(list(i for i in range(num_cities)))

        np.random.shuffle(curr)
        paths.append(Path(curr))

    return paths

def distance(this, that):
    # this and that are both tuples of x and y coordinates.
    squared_dist = (this[0] - that[0]) ** 2 + (this[1] - that[1]) ** 2
    
    return squared_dist ** (1/2)

def createGraph(num_cities):
    # Create a NumPy random generator object
    rng = np.random.default_rng(seed=42) 
    # ^^ Set seed to 42, for repeatability when testing. Remove when debugging is complete
    # Create an array of random cities
    cities = rng.normal(0, 1, (num_cities, 2))
    G = np.zeros(shape=(num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if(i == j):
                continue
            dist = distance(cities[i], cities[j])
            G[i][j] = dist

    return G

            
def makeChild(start, main, sharent): #share parent
    #inputs paths, returns path
    TRADE_LENGTH = 3
    main_path = main.route
    sharent_path = sharent.route
    num_cities = len(main_path)

    child_path = np.zeros(num_cities)
    child_path.fill(-1) # so that 0 doesn't confuse the matrix later on.

    # first take the sharent's segment
    for i in range(TRADE_LENGTH):
        index = (i + start) % num_cities
        child_path[i] = sharent_path[index]

    child_length = TRADE_LENGTH
    # then fill with the sequence of the main path
    for j in range(num_cities):
        index = (j + start) % num_cities
        if(not main_path[index] in child_path):
            child_path[child_length] = main_path[index]
            child_length += 1

    return Path(child_path)

def findBestNextVertex(curr_vertex, not_used_vertices, union):
    # finds the best next vertex to add to the child route given the current vertex,
    # not used edges, and the sorted union of parent edges. 
    for edge in union:
        pair = edge.edge
        if(curr_vertex in pair):
            vertex = pair[0]
            other_vertex = pair[1]
            if(curr_vertex == vertex):
                candidate = other_vertex
            else:
                candidate = vertex

            if(candidate in not_used_vertices):
                return candidate



    # no edge found in union that fits.
    return -1