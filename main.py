import numpy as np
import random
from graph_util import *
from Edge import *
from Path import *

def mutate(path):
    # path is a Path object
    newroute = np.copy(path.route)

    length = newroute.shape[0]

    # choose starting pointers
    index = random.randint(0, length - 1)
    jndex = random.randint(0, length - 2)
    if(jndex >= index):
        jndex += 1

    # switch iteratively at said pointers.
    if(index > jndex):
        # if index starts after jndex, we have to work outwards till one of them crosses over.
        while(index > jndex):
            newroute[[index, jndex]] = newroute[[jndex, index]]
            index = index + 1
            jndex -= 1
            if(jndex < 0):
                jndex = length - 1
                break 
                # this break prevents the case of both index and jndex swapping at the same time.
                # It is accounted for with the check of index < length below.
            if(index >= length):
                index = 0

    while(index < jndex and index < length):
        newroute[[index, jndex]] = newroute[[jndex, index]]
        index += 1
        jndex -= 1

    mutatedPath = Path(newroute)
    return mutatedPath

def nextGeneration(population, G):
    next_gen = []

    usable_population = population[:len(population) // 2]
    pool = usable_population * 4 #python lol
    random.shuffle(pool)
    while(len(pool) > 0):
        parent = pool.pop(0)
        qarent = pool.pop(0)
        next_gen.append(createChild(parent, qarent, G))

    return next_gen

def createChild(parent, qarent, G):
    #inputs two Path objects, returns Path object.
    p = parent.route
    q = qarent.route
    # create a union of both parents' graphs, via a list of sorted edges on weight.
    U = []
    for i in range(len(p) - 2):
        U.append(Edge(p[i], p[i+1], G))
        U.append(Edge(q[i], q[i+1], G))
    U.append(Edge(p[0], p[len(p)-1], G))
    U.append(Edge(q[0], q[len(p)-1], G))

    U.sort()

    #create a child's path
    child = []

    # choose arbitrary vertex to begin with (on the shortest edge)
    starting_e = U.pop(0)
    randomstart = random.randint(0,1)

    child_route = np.array([starting_e.edge[randomstart], starting_e.edge[int(not randomstart)]])
    not_used_vertices = [i for i in range(len(p))]
    not_used_vertices.remove(starting_e.edge[0])
    not_used_vertices.remove(starting_e.edge[1])

    # Next child to add: the vertex that is closest to latest vertex in union.
    # If not found there, then choose something random in not_used_vertices. 

    for i in range(len(not_used_vertices) - 1): # the last not_used_vertex will just be appended normally.
        latest_vertex = child_route[i + 1]

        #check the union to see if it has a vertex to add.
        unionNextVertex = findBestNextVertex(latest_vertex, not_used_vertices, U)
        if(unionNextVertex != -1):
            child_route = np.append(child_route, unionNextVertex)
            not_used_vertices.remove(unionNextVertex)
        else: #on dead end, we append a random vertex and move forward.
            index = random.randint(0, len(not_used_vertices) - 1)
            child_route = np.append(child_route, not_used_vertices[index])
            not_used_vertices.pop(index)

    child_route = np.append(child_route, not_used_vertices[0])
    return Path(child_route)



def main():
    SEED = 42

    random.seed(SEED)
    np.random.seed(SEED)

    num_cities = int(util_get_input("number of cities", 2))
    max_iter = int(util_get_input("number of iterations", 1))
    mutation_rate = util_get_input("proportion of mutation", 0)
    
    #num_cities = 20
    #max_iter = 100
    #mutation_rate = 0.1


    POPULATION = 50
    weights = createGraph(num_cities)

    # we initialize these fully randomly, as in the first implementation of NNX.
    population = initializePaths(POPULATION, num_cities)

    best_tours = [None] * max_iter

    best_found = None
    # NOTE: mutations require us to store the best tour with an additional pointer.

    for i in range(max_iter):
        # initialize weights of all paths

        for path in population:
            if(path.costNotCalculated()):
                path.calculateCost(weights)

        # sort paths based on relative weights

        population.sort(reverse = True) # possible because of __lt__ of Path object

        # update overall_best if needed, then store current best in best_tours.
        
            #update overall_best
        if(best_found == None):
            best_found = population[0]
        
        if(population[0].cost < best_found.cost):
            best_found = population[0]

            #store best weight
        best_tours[i] = best_found

        # create next generation

        population = nextGeneration(population, weights)

        # potentially mutate something in the population

        for i in range(len(population)):
            if(random.uniform(0.0, 1.0) < mutation_rate):
                population[i] = mutate(population[i])

    best_tours[max_iter - 1].calculateCost(weights)

    print("Best known quality:", best_tours[max_iter - 1].cost)
    print("Path:", best_tours[max_iter - 1].displayRoute())
    # save output
    plot_output(best_tours, num_cities)

    

if __name__ == '__main__':
    main()