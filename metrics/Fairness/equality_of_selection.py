import sys
sys.path.append('../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select

def equalityOfSelection(graph, selectedSet,occurrences):
        for item in selectedSet:
            occurrences[item] =  occurrences[item] + 1  
        return occurrences  


# k = 4
# graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)
# count1 = 0
# count2 = 0
# num_nodes = len(graph.nodes)
# occurrences = [0] * num_nodes

# for i in range (0,100):
#     selection = rand_select.randomSelection(graph,k,graph)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     occurrences = equalityOfSelection(graph, selection, occurrences)

#     # selection2 = rand_select.randomSelection(graph,k,graph)
#     # # print(selection2)
#     # # print(maximumCoverage(graph, selection2))
#     # count2 = count2 + fractionalCoverage(graph, selection2)
# prob_all = [0] * num_nodes

# for nodex in graph:
#     prob_all[nodex] =  occurrences[nodex] / sum(occurrences)

# print((prob_all))