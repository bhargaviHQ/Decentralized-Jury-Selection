import sys
sys.path.append('../')
import imports
from imports import *

def randomSelection(graph,k, occupiedNodes):   
    graphNodes = list(graph.iterNodes())
    graphNodes = list(set(graphNodes).difference(occupiedNodes))
    selectedNodes = set()
    while (len(selectedNodes) < k):
        elementAdd = random.choice(list(graphNodes))
        selectedNodes.add(elementAdd)
        occupiedNodes.add(elementAdd)
    return selectedNodes, occupiedNodes

# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


# print(randomSelection(G, 4))