import sys
sys.path.append('../')
import imports
from imports import *

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

def selectMaxSetElement(fullDict,rcl):
    maxElementKey = None
    maxSetLength = 0
    for key,value in fullDict.items():
        if key in rcl:
            if len(value) > maxSetLength:
                maxElementKey = key
                maxSetLength = len(value)
    if maxSetLength == 0 or maxElementKey == None:
        maxElementKey = random.choice(list(rcl))
    # print("Next Element is : ",maxElementKey)
    return maxElementKey

def rclGreedySelection(graphNodes,nodesReq,frac=5): 
    selectedNodesTemp = set()
    nodesToSelect = nodesReq*frac
    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(list(graphNodes))))

    fullDictionary = createDictionary(graphNodes)
    # covEelements(fullDictionary)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <nodesReq:
        key = selectMaxSetElement(fullDictionary,selectedNodesTemp)
        selectedSet.add(int(key))
        fullDictionary.pop(key)
        coveredSet.add(key)
        for neighbour in graphNodes.neighbors(key):
            coveredSet.add(neighbour)
        fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet
