import sys
sys.path.append('../')
import imports
from imports import *

def probBetweenSelection(graph,nodesToSelect): 
    selectedNodes = set()
    bc = nk.centrality.Betweenness(graph, normalized=True)
    bc.run()
    betweenness_values = bc.scores()
    while (len(selectedNodes) < nodesToSelect):
        candidate = betweenness_values.index(max(betweenness_values))
        betweenness_values.pop(betweenness_values.index(max(betweenness_values))) 
        selectedNodes.add(int(candidate))
    return selectedNodes

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


def betweenSelectionWithProb(graphNodes, k, occupiedNodes, probab=0.3):
    selectedNodes = set() 
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    fullDictionary =  createDictionary(graph,graphNodes)

    # bc = nk.centrality.Betweenness(graphNodes, normalized=True)
    # bc.run()
    # betweenness_values = bc.scores()

    while len(selectedNodes) <k:
        prob = random.random()
        if prob > probab :  
            #nodeSelected = random.choice(graph)
            key, val = random.choice(list(fullDictionary.items()))
            selectedNodes.add(key)
            occupiedNodes.add(key)
            fullDictionary.pop(key)
        else:
            candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
            # candidateSize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
            selectedNodes.add(int(candidate))
            occupiedNodes.add(int(candidate))
            fullDictionary.pop(candidate)
            # print("Candidate : ",candidate, " size : " , candidateSize)
            
    return selectedNodes, occupiedNodes


def betweenSelectionWithProbBetween(graphNodes, k, occupiedNodes,betweenness_values, probab=0.3):
    selectedNodes = set() 
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    fullDictionary =  createDictionaryBetween(graph,graphNodes,betweenness_values)

    # bc = nk.centrality.Betweenness(graphNodes, normalized=True)
    # bc.run()
    # betweenness_values = bc.scores()

    while len(selectedNodes) <k:
        prob = random.random()
        if prob > probab :  
            #nodeSelected = random.choice(graph)
            key, val = random.choice(list(fullDictionary.items()))
            selectedNodes.add(key)
            occupiedNodes.add(key)
            fullDictionary.pop(key)
        else:
            candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
            # candidateSize = max(zip(fullDictionary.values(), fullDictionary.keys()))[0]  
            selectedNodes.add(int(candidate))
            occupiedNodes.add(int(candidate))
            fullDictionary.pop(candidate)
            # print("Candidate : ",candidate, " size : " , candidateSize)
            
    return selectedNodes, occupiedNodes

# def betweenSelectionWithProb(graphNodes, k,probab=0.3):
#     selectedNodes = set() 
#     graph = list(graphNodes.iterNodes())
#     bc = nk.centrality.Betweenness(graphNodes, normalized=True)
#     bc.run()
#     betweenness_values = bc.scores()

#     while len(selectedNodes) <k:
#         prob = random.random()
#         if prob > probab :  
#             #nodeSelected = random.choice(graph)
#             nodeSelected = betweenness_values.index(random.choice(betweenness_values))
#             selectedNodes.add(nodeSelected)
#             betweenness_values.pop(nodeSelected)
#         else:
#             candidate = betweenness_values.index(max(betweenness_values))
#             betweenness_values.pop(betweenness_values.index(max(betweenness_values))) 
#             selectedNodes.add(int(candidate))
#     return selectedNodes


# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()

# print(betweenSelectionWithProb(G,7))