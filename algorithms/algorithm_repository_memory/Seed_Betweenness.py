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


def createDictionaryBetween(graphNodes, graph,betweenness_values):
    fullDict = {} 
    for nodex in graphNodes: 
        fullDict[nodex] = betweenness_values[nodex]
    return fullDict


def seedBetweenSelection(graphNodes,nodesReq): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    fullDictionary =  createDictionary(graph,graphNodes)
    # bc = nk.centrality.Betweenness(graphNodes, normalized=True)
    # bc.run()

    # betweenness_values = bc.scores()
    key, val = random.choice(list(fullDictionary.items()))
    selectedNodes.add(key)
    fullDictionary.pop(key)

    while (len(selectedNodes) < nodesReq):
            candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
            candidateSize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
            selectedNodes.add(int(candidate))
            fullDictionary.pop(candidate)
            
    return selectedNodes

def seedBetweenSelectionWithSize(graphNodes, nodesReq, occupiedNodes,seedSize): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    fullDictionary =  createDictionary(graph,graphNodes)
    # bc = nk.centrality.Betweenness(graphNodes, normalized=True)
    # bc.run()
    # betweenness_values = bc.scores()

    while (len(selectedNodes) < nodesReq):
            if len(selectedNodes) < seedSize:
                key, val = random.choice(list(fullDictionary.items()))
                selectedNodes.add(key)
                occupiedNodes.add(key)
                fullDictionary.pop(key)
            else:
                candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
                candidateSize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
                selectedNodes.add(int(candidate))
                occupiedNodes.add(int(candidate))
                fullDictionary.pop(candidate)
            
    return selectedNodes,occupiedNodes


def seedBetweenSelectionWithSizeBetween(graphNodes, nodesReq, occupiedNodes,betweenness_values,seedSize): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    fullDictionary =  createDictionaryBetween(graph,graphNodes,betweenness_values)
    # bc = nk.centrality.Betweenness(graphNodes, normalized=True)
    # bc.run()
    # betweenness_values = bc.scores()

    while (len(selectedNodes) < nodesReq):
            if len(selectedNodes) < seedSize:
                key, val = random.choice(list(fullDictionary.items()))
                selectedNodes.add(key)
                occupiedNodes.add(key)
                fullDictionary.pop(key)
            else:
                candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
                candidateSize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
                selectedNodes.add(int(candidate))
                occupiedNodes.add(int(candidate))
                fullDictionary.pop(candidate)
            
    return selectedNodes,occupiedNodes


# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


# print(seedBetweenSelectionWithSize(G, 5,2))