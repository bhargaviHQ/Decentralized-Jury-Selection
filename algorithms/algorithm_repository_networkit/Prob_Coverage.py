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

def randomGreedyProbSelection(graph, k):
    fullDictionary = createDictionary(graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <k:
        prob = random.random()
        if prob > 0.3 :  
                randomFirstNode = random.choice(list(fullDictionary.keys()))
                selectedSet.add(int(randomFirstNode))
                fullDictionary.pop(randomFirstNode)
                coveredSet.add(randomFirstNode)
                for neighbour in graph.neighbors(randomFirstNode):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",randomFirstNode)
        else:
                key = selectMaxSetElement(fullDictionary)
                selectedSet.add(int(key))
                fullDictionary.pop(key)
                coveredSet.add(key)
                for neighbour in graph.neighbors(key):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",key)

    return selectedSet
    

# def randomGreedyProbSelectionWithProb(graph, k,probab):
#     fullDictionary = createDictionary(graph)
#     # covEelements(fullDictionary)
#     selectedSet = set()
#     coveredSet = set()

#     while len(selectedSet) <k:
#         prob = random.random()
#         if prob > probab :  
#                 randomFirstNode = random.choice(list(fullDictionary.keys()))
#                 selectedSet.add(int(randomFirstNode))
#                 fullDictionary.pop(randomFirstNode)
#                 coveredSet.add(randomFirstNode)
#                 for neighbour in graph.neighbors(randomFirstNode):
#                     coveredSet.add(neighbour)
#                 fullDictionary = updateDictionary(fullDictionary,coveredSet)
#                 # print("Selected element is : ",randomFirstNode)
#         else:
#                 key = selectMaxSetElement(fullDictionary)
#                 selectedSet.add(int(key))
#                 fullDictionary.pop(key)
#                 coveredSet.add(key)
#                 for neighbour in graph.neighbors(key):
#                     coveredSet.add(neighbour)
#                 fullDictionary = updateDictionary(fullDictionary,coveredSet)
#                 # print("Selected element is : ",key)

#     return selectedSet
    

def coverageSelectionWithProb(graph, k,probab=0.3):
    fullDictionary = createDictionary(list(graph.iterNodes()),graph)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <k:
        prob = random.random()
        if prob > probab :  
                randomFirstNode = random.choice(list(fullDictionary.keys()))
                selectedSet.add(randomFirstNode)
                fullDictionary.pop(randomFirstNode)
                coveredSet.add(randomFirstNode)
                for neighbour in list(graph.iterNeighbors(randomFirstNode)):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",randomFirstNode)
        else:
                key = selectMaxSetElement(fullDictionary)
                selectedSet.add(key)
                fullDictionary.pop(key)
                coveredSet.add(key)
                for neighbour in list(graph.iterNeighbors(key)):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)


    return selectedSet

# G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


# print(coverageSelectionWithProb(G, 4))