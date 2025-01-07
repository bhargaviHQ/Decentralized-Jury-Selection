import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
from community_detection_algorithm import detect_communities

def runRandomProbSelect(graph, numNodes):
    
    allNodes = set(graph.nodes())
    totalNodes = graph.number_of_nodes()
    selectedSet = set()
    coveredSet = set()
    #randomFirstNode = random.choice(range(0,len(allNodes)))
    randomFirstNode = random.choice(list(allNodes))
    selectedSet.add(randomFirstNode)
    for neighbour in graph.neighbors(randomFirstNode):
        coveredSet.add(neighbour)
    allNodes.remove(randomFirstNode)

    while len(selectedSet) < numNodes:
        prob = random.random()
        if prob > 0.3 :    
            randomNode = random.choice(range(0,len(allNodes)))
            #randomNode = random.choice(list(allNodes))
            if randomNode in selectedSet :
                continue
            selectedSet.add(randomNode)
            for neighbour in graph.neighbors(randomNode):
                coveredSet.add(neighbour)
            allNodes.remove(randomNode)
        else :
            maxCoverage = 0
            maxCoverageNode = -1
            for node in allNodes:
                if node not in selectedSet:
                    nodeCovers = set()
                    for neighbour in graph.neighbors(node):
                        nodeCovers.add(neighbour)
                    lenNodeCovers = len(nodeCovers.intersection(coveredSet))
                    if(lenNodeCovers > maxCoverage):
                        maxCoverageNode = node
                        maxCoverage = lenNodeCovers
            selectedSet.add(maxCoverageNode)
            for neighbour in graph.neighbors(maxCoverageNode):
                coveredSet.add(neighbour)
            allNodes.remove(maxCoverageNode)
        
    return selectedSet

# k=4

# for obj in generator.graph_param_list:
#     graphObjects = obj.setGraphObject()
#     for graph in graphObjects:
#         print(graph.number_of_nodes())
#         print( "- > selected set : ",runRandomProbSelect(graph, k))