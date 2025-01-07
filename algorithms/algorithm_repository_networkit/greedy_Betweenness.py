import sys
sys.path.append('../')
import imports
from imports import *

def createDictionary(graphNodes, graph):
    fullDict = {} 
    bc = nk.centrality.Betweenness(graph, normalized=True)
    bc.run()
    betweenness_values = bc.scores()
    for nodex in graphNodes: 
        fullDict[nodex] = betweenness_values[nodex]
    return fullDict


def greedyBetweennessSelection(graphNodes, nodesToSelect): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    fullDictionary =  createDictionary(graph,graphNodes)

    while (len(selectedNodes) < nodesToSelect):
        candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
        candidatesize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
        selectedNodes.add(int(candidate))
        fullDictionary.pop(candidate)
        # candidate = betweenness_values.index(max(betweenness_values))
        # betweenness_values.pop(betweenness_values.index(max(betweenness_values))) 
        # selectedNodes.add(int(candidate))
    return selectedNodes


# G = nk.generators.BarabasiAlbertGenerator(2,500).generate()

# print(greedyBetweennessSelection(G,8))