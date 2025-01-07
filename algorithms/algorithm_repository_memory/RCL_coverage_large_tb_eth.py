import sys
sys.path.append('../')
import imports
from imports import *

def createDictionary(graphNodes, graph,selectedNodesTemp):
    fullDict = {} 
    for nodex in graphNodes:
        if nodex in selectedNodesTemp:
            neighbours = set()
            for neighbour in list(graph.iterNeighbors(nodex)):
                neighbours.add(neighbour)   
            fullDict[nodex] = neighbours

    nodes = np.array(list(fullDict.keys()))
    elements = np.array([fullDict[node] for node in nodes])    
    return fullDict,nodes,elements

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

def selectMaxElementFromList(elements,rcl):
    maxElementKey = None
    maxSetLength = 0
    max_element_index = np.argmax([len(subarray) for subarray in elements])

    # maxElementKey = max(fullDict, key=lambda k: fullDict[k])
    # maxSetLength = max(fullDict.values())
    # print("max key : ", maxElementKey, " maxSetLength : ", maxSetLength)

    # for key,value in fullDict.items():
    #     if len(value) > maxSetLength:
    #         maxElementKey = key
    #         maxSetLength = len(value)
    if max_element_index == None:
        maxElementKey = random.choice(list(rcl))
    # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
    return max_element_index


def selectMaxSetElement(fullDict,rcl):
    maxElementKey = None
    maxSetLength = 0
    maxElementKey = max(fullDict, key=lambda k: fullDict[k])
    maxSetLength = max(fullDict.values())
    # print("max key : ", maxElementKey, " maxSetLength : ", maxSetLength)

    # for key,value in fullDict.items():
    #     if len(value) > maxSetLength:
    #         maxElementKey = key
    #         maxSetLength = len(value)
    if maxSetLength == 0 or maxElementKey == None:
        maxElementKey = random.choice(list(rcl))
    # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
    return maxElementKey

# def selectMaxSetElement(fullDict,rcl,selectedSet):
#     maxElementKey = None
#     maxSetLength = 0
#     for key,value in fullDict.items():
#         if key in rcl:
#             if len(value) > maxSetLength:
#                 maxElementKey = key
#                 maxSetLength = len(value)
#     if maxSetLength == 0 or maxElementKey == None:
#         maxElementKey = random.choice(list(rcl))
#         # while maxElementKey in selectedSet:
#         #     maxElementKey = random.choice(list(rcl))
#     # print("Next Element is : ",maxElementKey, " value : ", maxSetLength)
#     return maxElementKey

# def rclCoverageSelection_large_tb(graphNodes,nodesReq,frac=5): 
#     selectedNodesTemp = set()
#     graph = list(graphNodes.iterNodes())
#     if nodesReq*frac > len(graph):
#         nodesToSelect = len(graph) - 1
#     else :
#         nodesToSelect = nodesReq*frac

#     while (len(selectedNodesTemp) < nodesToSelect):
#         selectedNodesTemp.add(int(random.choice(graph)))
#     fullDictionary =  createDictionary(graph,graphNodes)
#     selectedSet = set()
#     coveredSet = set()

#     while len(selectedSet) <nodesReq:
#         key = selectMaxSetElement(fullDictionary,selectedNodesTemp,selectedSet)
#         selectedSet.add(int(key))
#         fullDictionary.pop(key)
#         coveredSet.add(key)
#         for neighbour in list(graphNodes.iterNeighbors(key)):
#             coveredSet.add(neighbour)
#         fullDictionary = updateDictionary(fullDictionary,coveredSet)

#     return selectedSet
                                            
def rclCoverageSelectionWithSubset_large_tb(graphNodes,nodesReq,occupiedNodes, percent=0.1): 
    selectedNodesTemp = set()
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))
    if percent>1:
        percent = 0.95
    elif percent<0:
        percent = 0.1
    nodesToSelect = len(graph)*percent
    print(" nodesToSelect : ", nodesToSelect)
    while nodesReq>nodesToSelect:
        nodesToSelect +=1
    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(graph)))

    fullDictionary,nodes,elements =  createDictionary(graph,graphNodes,selectedNodesTemp)

    selectedSet = set()
    coveredSet = set()
    print("Nodes required are : ", nodesReq, " nodesToSelect: ", nodesToSelect)
    print("Elements : \n", elements)
    itrr = 0
    while (itrr == 0):
                    key = selectMaxElementFromList(elements,selectedNodesTemp)
                
                    print("Key : ", key)
                    if key not in selectedSet:
                        selectedSet.add(int(key))
                        occupiedNodes.add(int(key))
                        # nodes.pop(key)
                        np.delete(nodes, key)
                        print("After remove  :",nodes)
                        # fullDictionary.pop(key)
                        coveredSet.add(key)
                        for neighbour in list(graphNodes.iterNeighbors(key)):
                            coveredSet.add(neighbour)
                        # fullDictionary = updateDictionary(fullDictionary,coveredSet)
                        # elements = updateDictionary(elements,coveredSet)
                        print(coveredSet)
                        print("BEFORE : \n",elements)
                        for list1 in elements:
                            for item in list1:
                                if item in coveredSet:
                                   list1.remove(item)
                            
                            
                        print("AFTER : \n",elements[0])
                        print("AFTER : \n",elements[1])
                    itrr = 3

    # while len(selectedSet) < nodesReq:
    #         if(len(nodes)==0):
    #             elementAdd = random.choice(graph)
    #             selectedSet.add(int(elementAdd))
    #             occupiedNodes.add(int(elementAdd))
    #         else:
    #             #key = selectMaxSetElement(fullDictionary,selectedNodesTemp)
    #             key = selectMaxElementFromList(elements,selectedNodesTemp)
                
    #             print("Key : ", key)
    #             if key not in selectedSet:
    #                 selectedSet.add(int(key))
    #                 occupiedNodes.add(int(key))
    #                 # nodes.pop(key)
    #                 np.delete(nodes, key)
    #                 print("After remove  :",nodes)
    #                 # fullDictionary.pop(key)
    #                 coveredSet.add(key)
    #                 for neighbour in list(graphNodes.iterNeighbors(key)):
    #                     coveredSet.add(neighbour)
    #                 # fullDictionary = updateDictionary(fullDictionary,coveredSet)
    #                 # elements = updateDictionary(elements,coveredSet)
    #                 print("BEFORE : \n",elements)
    #                 for list1 in elements:
    #                     list1 = [x for x in list1 if x not in coveredSet]
                        
    #                 print("AFTER : \n",elements[0])
    #                 print("AFTER : \n",elements[1])

    return selectedSet, occupiedNodes


G = nk.generators.BarabasiAlbertGenerator(2,40).generate()

occupiedNodes = set()
print(rclCoverageSelectionWithSubset_large_tb(G, 3,occupiedNodes,0.7))