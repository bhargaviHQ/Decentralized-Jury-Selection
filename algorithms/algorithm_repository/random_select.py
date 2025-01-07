import sys
sys.path.append('../')
import imports
from imports import *

def randomSelection(graph,k):   
    graphNodes = graph.nodes()
    selectedNodes = set()
    while (len(selectedNodes) < k):
        selectedNodes.add(random.choice(list(graphNodes)))
    return selectedNodes

# graph = LFR_benchmark_graph(10,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)

# print(randomSelection(graph, 3))