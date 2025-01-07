import sys
sys.path.append('../../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select

from algorithm_repository_networkit import RCL_coverage

def overlapping_coverage(graph, selectedSet):
    maxUniqueElements = set()
    num_nodes = list(graph.iterNodes())
    for nodex in selectedSet:
        neighbours = graph.iterNeighbors(nodex)
        for nodex in neighbours:
            maxUniqueElements.add(nodex) 
    return len(maxUniqueElements)/(len(num_nodes))

# G = nk.generators.BarabasiAlbertGenerator(2,100).generate()
# selectedSet = RCL_coverage.rclCoverageSelection(G, 6)
# print(overlapping_coverage(G, selectedSet))

# k = 8
# graph = LFR_benchmark_graph(100,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)


# count1 = 0
# count2 = 0
# for i in range (0,100):
#     selection = rand_greedy_select.randomGreedySelection(graph, k)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     count1 = count1 + overlapping_coverage(graph, selection)

#     selection2 = rand_select.randomSelection(graph,k)
#     # print(selection2)
#     # print(maximumCoverage(graph, selection2))
#     count2 = count2 + overlapping_coverage(graph, selection2)

# print("First : ", count1/100)
# print("Second : ", count2/100)