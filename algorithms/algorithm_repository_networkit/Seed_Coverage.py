import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
from community_detection_algorithm import detect_communities

def createDictionary(graphNodes, graph):
    fullDict = {} 
    for nodex in graphNodes:
        neighbours = set()
        for neighbour in list(graph.iterNeighbors(nodex)):
            neighbours.add(neighbour)   
        fullDict[nodex] = neighbours
    return fullDict

def updateDictionary(fullDict, coveredSet):
    for key,value in fullDict.items():
        fullDict[key] = fullDict[key] - coveredSet
    return fullDict

def printDictionary(fullDict):
    for key,value in fullDict.items():
        print(key, " : { ",value," } ")

def covEelements(fullDict):
    for key,value in fullDict.items():
        print(key, " : { ",len(value)," } ")

def selectMaxSetElement(fullDict):
    maxElementKey = None
    maxSetLength = 0
    for key,value in fullDict.items():
        if len(value) > maxSetLength:
            maxElementKey = key
            maxSetLength = len(value)
    if maxSetLength == 0 or maxElementKey == None:
        maxElementKey = random.choice(list(fullDict.keys()))
    # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
    return maxElementKey

def seedCoverSelection(graph, k):
    fullDictionary = createDictionary(list(graph.iterNodes()),graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()
    randomFirstNode = random.choice(list(fullDictionary.keys()))
    selectedSet.add(int(randomFirstNode))
    fullDictionary.pop(randomFirstNode)
    coveredSet.add(randomFirstNode)
    for neighbour in list(graph.iterNeighbors(randomFirstNode)):
        coveredSet.add(neighbour)
    fullDictionary = updateDictionary(fullDictionary,coveredSet)
    while len(selectedSet) <k:
        key = selectMaxSetElement(fullDictionary)
        selectedSet.add(int(key))
        fullDictionary.pop(key)
        coveredSet.add(key)
        for neighbour in list(graph.iterNeighbors(key)):
            coveredSet.add(neighbour)
        fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet
    
    
def seedCoverSelectionWithSize(graph, k, seedSize):
    fullDictionary = createDictionary(list(graph.iterNodes()),graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()
    while len(selectedSet) < k:
        if len(selectedSet) < seedSize:
            randomFirstNode = random.choice(list(fullDictionary.keys()))
            selectedSet.add(int(randomFirstNode))
            fullDictionary.pop(randomFirstNode)
            coveredSet.add(randomFirstNode)
            for neighbour in list(graph.iterNeighbors(randomFirstNode)):
                coveredSet.add(neighbour)
            fullDictionary = updateDictionary(fullDictionary,coveredSet)
        else:
            key = selectMaxSetElement(fullDictionary)
            selectedSet.add(int(key))
            fullDictionary.pop(key)
            coveredSet.add(key)
            for neighbour in list(graph.iterNeighbors(key)):
                coveredSet.add(neighbour)
            fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet


# G = nk.generators.BarabasiAlbertGenerator(2,40).generate()

# k = 6
# print(seedCoverSelectionWithSize(G, 5,4))

# k=11

# # for obj in generator.graph_param_list:
# #     graphObjects = obj.setGraphObject()
# #     for graph in graphObjects:
# #         print(graph.number_of_nodes())
# #         print( "- > selected set : ",randomGreedySelection(graph, k))
        

# graph = LFR_benchmark_graph(10,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)

# randomGreedySelection(graph, k)