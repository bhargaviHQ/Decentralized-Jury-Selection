import sys
sys.path.append('../../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select

#length of the fractional coverage 
#returns the number of nodes covered 
#within radius from some
def fractionalCoverage(graph, selectedSet, radius):
    fractionalCoverageSet = set()
    for nodex in graph:
        for nodey in selectedSet:
            if nodex not in fractionalCoverageSet:
                if not nx.has_path(graph, str(nodex), str(nodey)):
                    continue
                shortest_path = nx.shortest_path(graph, str(nodex), str(nodey))
                if len(shortest_path) <= radius:
                    fractionalCoverageSet.add(int(nodex))
    return len(fractionalCoverageSet)/len(graph.nodes)


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