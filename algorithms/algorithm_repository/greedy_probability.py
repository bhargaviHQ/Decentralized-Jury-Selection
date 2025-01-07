import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
from community_detection_algorithm import detect_communities

def createDictionary(graph):
    fullDict = {}
    for nodex in graph:
        neighbours = set()
        for neighbour in graph.neighbors(nodex):
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
    return maxElementKey

def randomGreedyProbSelection(graph, k):
    fullDictionary = createDictionary(graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <k:
        prob = random.random()
        if prob > 0.2 :  
                randomFirstNode = random.choice(list(fullDictionary.keys()))
                selectedSet.add(randomFirstNode)
                fullDictionary.pop(randomFirstNode)
                coveredSet.add(randomFirstNode)
                for neighbour in graph.neighbors(randomFirstNode):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",randomFirstNode)
        else:
                key = selectMaxSetElement(fullDictionary)
                selectedSet.add(key)
                fullDictionary.pop(key)
                coveredSet.add(key)
                for neighbour in graph.neighbors(key):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",key)

    return selectedSet
    

def randomGreedyProbSelectionWithProb(graph, k,probab):
    fullDictionary = createDictionary(graph)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <k:
        prob = random.random()
        if prob > probab :  
                randomFirstNode = random.choice(list(fullDictionary.keys()))
                selectedSet.add(randomFirstNode)
                fullDictionary.pop(randomFirstNode)
                coveredSet.add(randomFirstNode)
                for neighbour in graph.neighbors(randomFirstNode):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",randomFirstNode)
        else:
                key = selectMaxSetElement(fullDictionary)
                selectedSet.add(key)
                fullDictionary.pop(key)
                coveredSet.add(key)
                for neighbour in graph.neighbors(key):
                    coveredSet.add(neighbour)
                fullDictionary = updateDictionary(fullDictionary,coveredSet)
                # print("Selected element is : ",key)

    return selectedSet

# k=3

# # for obj in generator.graph_param_list:
# #     graphObjects = obj.setGraphObject()
# #     for graph in graphObjects:
# #         print(graph.number_of_nodes())
# #         print( "- > selected set : ",randomGreedySelection(graph, k))
        

# graph = LFR_benchmark_graph(10,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)

# randomGreedySelection(graph, k)