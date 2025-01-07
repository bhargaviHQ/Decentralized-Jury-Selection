import sys
sys.path.append('../../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm_repository_memory import random_select
from algorithm_repository_networkit import RCL_coverage
#returns the sum of minimum distance
#of all unselected nodes to selected nodes
# def maximumCoverage(graph, selectedSet):
#     totalMinDistance = 0
#     for nodex in graph:
#         minDistance = float('inf')
#         for nodey in selectedSet:
#             if not nx.has_path(graph, nodex, nodey):
#                 continue
#             shortest_path = nx.shortest_path(graph, nodex, nodey)
#             if len(shortest_path) - 1 < minDistance:
#                 minDistance = len(shortest_path) - 1
#         if minDistance == float('inf'):
#             minDistance = 0
#         totalMinDistance = totalMinDistance + minDistance
#     return totalMinDistance/len(graph.nodes)


# def maximumCoverageSet(graph, selectedSet):
#     maxLengthPath = -1
#     counter = 0
#     for nodex in graph:
#         maxNodePath = -1
#         for nodey in selectedSet:
#             if not nx.has_path(graph, nodex, nodey):
#                 continue
#             shortest_path = nx.shortest_path(graph, nodex, nodey)
            
#             if len(shortest_path) - 1 > maxNodePath:
#                 maxNodePath = len(shortest_path) - 1
#         if maxNodePath == -1:
#             maxNodePath = 0
#         if maxNodePath > maxLengthPath:
#                 maxLengthPath = maxNodePath
#     return maxLengthPath

# def maximumCoverageSetModified(graph, selectedSet):
#     maxLengthPath = -1
#     counter = 0
#     for nodex in graph:
#         minNodePath = float('inf')
#         for nodey in selectedSet:
#             if not nx.has_path(graph, nodex, nodey):
#                 continue
#             shortest_path = nx.shortest_path(graph, nodex, nodey)
#             if len(shortest_path) - 1 < minNodePath:
#                 minNodePath = len(shortest_path) - 1
#         if minNodePath == float('inf'):
#             minNodePath = 0
#         if minNodePath > maxLengthPath:
#                 maxLengthPath = minNodePath
#     return maxLengthPath


def maximumCoverageSetModified(graph, selectedSet):
    maxLengthPath = -1
    counter = 0
    apsp = nk.distance.APSP(graph)
    apsp.run()
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    for nodex in graphNodes:
        minNodePath = float('inf')
        for nodey in selectedSet:
            shortest_path = apsp.getDistance(nodex, nodey)
            if shortest_path < minNodePath:
                minNodePath = shortest_path
        if minNodePath == float('inf'):
            minNodePath = 0
        if minNodePath > maxLengthPath:
                maxLengthPath = minNodePath
    return maxLengthPath

def maximumCoverageSetFinal(graph, selectedSet):
    maxLengthPath = -1
    counter = 0
    apsp = nk.distance.APSP(graph)
    apsp.run()
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    maxList =  [0]*num_nodes
    for nodex in graphNodes:
        minNodePath = float('inf')
        for nodey in selectedSet:
            shortest_path = apsp.getDistance(nodex, nodey)
            if shortest_path < minNodePath:
                minNodePath = shortest_path
        if minNodePath == float('inf'):
            minNodePath = 0
        if minNodePath > maxList[nodex]:
                maxList[nodex] = minNodePath
    return np.mean(maxList)

def maximumCoverageSetFinalLARGETB(graph, selectedSet):
    maxLengthPath = -1
    counter = 0
    apsp = nk.distance.APSP(graph)
    apsp.run()
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    #maxList =  [0]*num_nodes
    maxList =  [0]*len(selectedSet)
    
    fractionalCoverageSet = set()

    for nodex in selectedSet:
        for neighbour in list(graph.iterNeighbors(nodex)):
            fractionalCoverageSet.add(neighbour)
        print("len : ",len(fractionalCoverageSet))
        # minNodePath = float('inf')
        maxNodePath = float('-inf')
        for nodey in graphNodes:
            print("nodey : ",nodey)
            if nodey not in fractionalCoverageSet :
                shortest_path = apsp.getDistance(nodex, nodey)
                if shortest_path > maxNodePath:
                    maxNodePath = shortest_path
        if maxNodePath == float('inf'):
                maxNodePath = 0
        if maxNodePath > maxList[nodex]:
                    maxList[nodex] = maxNodePath

    # for nodex in graphNodes:
    #     minNodePath = float('inf')
    #     for nodey in selectedSet:
    #         shortest_path = apsp.getDistance(nodex, nodey)
    #         if shortest_path < minNodePath:
    #             minNodePath = shortest_path
    #     if minNodePath == float('inf'):
    #         minNodePath = 0
    #     if minNodePath > maxList[nodex]:
    #             maxList[nodex] = minNodePath
    return np.mean(maxList)


    
# G = nk.generators.BarabasiAlbertGenerator(1,40).generate()
# # selectedSet = RCL_coverage.rclCoverageSelection(G, 10)
# occ = set()
# selectedSet = random_select.randomSelection(G,10,occ)
# print(maximumCoverageSetFinalLARGETB(G, selectedSet))

# k = 4
# graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)


# count1 = 0
# count2 = 0
# for i in range (0,100):
#     selection = rand_greedy_select.randomGreedySelection(graph, k, graph)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     count1 = count1 + maximumCoverage(graph, selection)

#     selection2 = rand_select.randomSelection(graph,k,graph)
#     # print(selection2)
#     # print(maximumCoverage(graph, selection2))
#     count2 = count2 + maximumCoverage(graph, selection2)

# print("First : ", count1/100)
# print("Second : ", count2/100)