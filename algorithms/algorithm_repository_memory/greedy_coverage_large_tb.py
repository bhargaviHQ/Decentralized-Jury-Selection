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
    maxElementKey = max(fullDict, key=lambda k: fullDict[k])
    maxSetLength = max(fullDict.values())

    # for key,value in fullDict.items():
    #     if len(value) > maxSetLength:
    #         maxElementKey = key
    #         maxSetLength = len(value)
    if maxSetLength == 0 or maxElementKey == None:
        maxElementKey = random.choice(list(fullDict.keys()))
    # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
    return maxElementKey



def greedyCoverageSelection(graph, k, occupiedNodes):
    graphNode = list(graph.iterNodes())
    graphNode = list(set(graphNode).difference(occupiedNodes))
    fullDictionary =  createDictionary(graphNode,graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()
    while len(selectedSet) <k:
        key = selectMaxSetElement(fullDictionary)
        selectedSet.add(int(key))
        occupiedNodes.add(int(key))
        fullDictionary.pop(key)
        coveredSet.add(key)
        for neighbour in list(graph.iterNeighbors(key)):
            coveredSet.add(neighbour)
        fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet,occupiedNodes
    
# G = nk.generators.BarabasiAlbertGenerator(2,10).generate()
# occupiedNodes = set()
# print(greedyCoverageSelection(G,2,occupiedNodes))