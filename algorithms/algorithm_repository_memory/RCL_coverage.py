import sys
sys.path.append('../')
import imports
from imports import *

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

def selectMaxSetElement(fullDict,rcl,selectedSet):
    maxElementKey = None
    maxSetLength = 0
    for key,value in fullDict.items():
        if key in rcl:
            if len(value) > maxSetLength:
                maxElementKey = key
                maxSetLength = len(value)
    if maxSetLength == 0 or maxElementKey == None:
        maxElementKey = random.choice(list(rcl))
        # while maxElementKey in selectedSet:
        #     maxElementKey = random.choice(list(rcl))
    # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
    return maxElementKey

def rclCoverageSelection(graphNodes,nodesReq,frac=5): 
    selectedNodesTemp = set()
    graph = list(graphNodes.iterNodes())
    if nodesReq*frac > len(graph):
        nodesToSelect = len(graph) - 1
    else :
        nodesToSelect = nodesReq*frac

    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(graph)))
    fullDictionary =  createDictionary(graph,graphNodes)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) <nodesReq:
        key = selectMaxSetElement(fullDictionary,selectedNodesTemp,selectedSet)
        selectedSet.add(int(key))
        fullDictionary.pop(key)
        coveredSet.add(key)
        for neighbour in list(graphNodes.iterNeighbors(key)):
            coveredSet.add(neighbour)
        fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet

def rclCoverageSelectionWithSubset(graphNodes,nodesReq,occupiedNodes, percent=0.1): 
    selectedNodesTemp = set()
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    if percent>1:
        percent = 0.95
    elif percent<0:
        percent = 0.1
    nodesToSelect = len(graph)*percent
    
    while nodesReq>nodesToSelect:
        nodesToSelect +=1
    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(graph)))
    fullDictionary =  createDictionary(graph,graphNodes)
    selectedSet = set()
    coveredSet = set()

    while len(selectedSet) < nodesReq:
            if(len(fullDictionary)==0):
                elementAdd = random.choice(graph)
                selectedSet.add(int(elementAdd))
                occupiedNodes.add(int(elementAdd))
            else:
                key = selectMaxSetElement(fullDictionary,selectedNodesTemp,selectedSet)
                if key not in selectedSet:
                    selectedSet.add(int(key))
                    occupiedNodes.add(int(key))
                    fullDictionary.pop(key)
                    coveredSet.add(key)
                    for neighbour in list(graphNodes.iterNeighbors(key)):
                        coveredSet.add(neighbour)
                    fullDictionary = updateDictionary(fullDictionary,coveredSet)

    return selectedSet, occupiedNodes


# G = nk.generators.BarabasiAlbertGenerator(2,40).generate()


# print(rclCoverageSelection(G, 20))