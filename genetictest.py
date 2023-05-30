import random
import numpy as np
from Path import *
from Edge import *

def propagate(p, q):
    numcities = len(p.route)

    starting_point = random.randint(0, numcities - 1)

    childone = makeChild(starting_point, p, q) #
    childtwo = makeChild(starting_point, q, p)

    return childone, childtwo

def testNextGeneration():
    pop = []
    pop.append(Path(np.array([1,2,3,0,4])))
    pop.append(Path(np.array([2,0,1,3,4])))
    pop.append("a")
    pop.append("b")

    G = [[0,14,21,31,41],
         [5,13,22,32,42],
         [6,12,23,33,43],
         [8,11,24,34,44],
         [9,19,25,35,45]
    ]
    nextGeneration(pop, G)

testNextGeneration()

def propagateTest():
    path = Path(np.array([1,2,3,4,5,6,7,8,9,0]))
    qath = Path(np.array([1,3,5,7,9,2,4,6,8,0]))
    
    childone, childtwo = propagate(path, qath)
    print(childone.route)
    print(childtwo.route)

    #childpath1, childpath2 = propagate(path, pathtwo)
def mutateTest():
    path = Path(np.array([1,2,3,4,5,6,7,8,9,0]))
    newpath = mutate(path)
    print(path.route)
    print(newpath.route)

#mutateTest()