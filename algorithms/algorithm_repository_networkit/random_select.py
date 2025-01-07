import sys
sys.path.append('../')
import imports
from imports import *

def randomSelection(graph,k):   
    graphNodes = list(graph.iterNodes())
    selectedNodes = set()
    while (len(selectedNodes) < k):
        selectedNodes.add(random.choice(list(graphNodes)))
    return selectedNodes

# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


# print(randomSelection(G, 4))