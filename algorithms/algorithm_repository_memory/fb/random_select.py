import sys
sys.path.append('../')
import imports
from imports import *

def randomSelection(graph,k, occupiedNodes):   
    graphNodes = list(graph.iterNodes())
    graphNodes = list(set(graphNodes).difference(occupiedNodes))
    numNodes = len(graphNodes)
    selectedNodes = set()


    v = random.randint(100, numNodes)
    if v > numNodes:
        v = numNodes -1 

    eligibleNodeSet = random.sample(graphNodes, v)
    # print("eligibleNodeSet : len( )", len(eligibleNodeSet))
    # print("before : len(graph : )", numNodes)
    # graphNodes = list(set(graphNodes).difference(eligibleNodeSet))
    # numNodes = len(graphNodes)

    while (len(selectedNodes) < k):
        elementAdd = random.choice(list(eligibleNodeSet))
        selectedNodes.add(elementAdd)
        occupiedNodes.add(elementAdd)
    return selectedNodes, occupiedNodes

# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


# print(randomSelection(G, 4))