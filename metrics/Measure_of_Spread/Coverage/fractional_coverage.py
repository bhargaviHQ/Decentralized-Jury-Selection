import sys
sys.path.append('../../../')
import imports
from imports import *

#length of the fractional coverage 
#returns the number of nodes covered 
#within radius from some
# def fractionalCoverage(graph, selectedSet, radius):
#     fractionalCoverageSet = set()
#     for nodex in graph:
#         for nodey in selectedSet:
#             if nodex not in fractionalCoverageSet:
#                 if not nx.has_path(graph, nodex, nodey):
#                     continue
#                 shortest_path = nx.shortest_path(graph, nodex, nodey)
#                 if len(shortest_path) <= radius:
#                     fractionalCoverageSet.add(nodex)
#     return len(fractionalCoverageSet)/len(graph.nodes)


def fractionalCoverage(graph, selectedSet, radius):
    fractionalCoverageSet = set()
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    apsp = nk.distance.APSP(graph)
    apsp.run()

    for nodex in graphNodes:
        for nodey in selectedSet:
            if nodex not in fractionalCoverageSet:
                shortest_path = apsp.getDistance(nodex, nodey)
                if shortest_path <= radius:
                    fractionalCoverageSet.add(nodex)
    return len(fractionalCoverageSet)/num_nodes

def fractionalCoverageLARGETB(graph, selectedSet, radius):
    fractionalCoverageSet = set()
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    # apsp = nk.distance.APSP(graph)
    # apsp.run()

    for nodex in selectedSet:
        for neighbour in list(graph.iterNeighbors(nodex)):
            fractionalCoverageSet.add(neighbour)
    return len(fractionalCoverageSet)/num_nodes



# G = nk.generators.BarabasiAlbertGenerator(2,3).generate()
# selectedSet = RCL_coverage.rclCoverageSelection(G, 1)
# print(fractionalCoverage(G, selectedSet,3))

# k = 4
# graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)


# count1 = 0
# count2 = 0
# radius = 4
# for i in range (0,100):
#     selection = rand_greedy_select.randomGreedySelection(graph, k)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     count1 = count1 + fractionalCoverage(graph, selection, radius)

#     selection2 = rand_select.randomSelection(graph,k)
#     # print(selection2)
#     # print(maximumCoverage(graph, selection2))
#     count2 = count2 + fractionalCoverage(graph, selection2, radius)
# print("First : ", count1/100)
# print("Second : ", count2/100)