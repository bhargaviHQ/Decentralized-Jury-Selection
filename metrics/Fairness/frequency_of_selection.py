import sys
sys.path.append('../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select

def frequencyOfSelection(graph, selectedSet,occurrences):
        for item in selectedSet:
            occurrences[item] =  occurrences[item] + 1  
        return occurrences  

# k = 4
# delta = 5
# graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)
# count1 = 0
# count2 = 0
# num_nodes = len(graph.nodes)
# occurrences = [0] * num_nodes

# for i in range (0,100):
#     selection = rand_greedy_select.randomGreedySelection(graph,k,graph)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     occurrences = frequencyOfSelection(graph, selection, occurrences)

#     # selection2 = rand_select.randomSelection(graph,k,graph)
#     # # print(selection2)
#     # # print(maximumCoverage(graph, selection2))
#     # count2 = count2 + fractionalCoverage(graph, selection2)
# occurrences.sort(reverse=True)


# percentileBefore =  np.percentile(occurrences, delta)
# percentileAfter = np.percentile(occurrences, (100 - delta))
# counterReset = 0
# # print("Before : ", np.percentile(occurrences, delta), " After : ",np.percentile(occurrences, (100 - delta)))

# # counter = 0
# # for item in occurrences:
# #     print(item)
# #     counter +=1
# # print("Counter : ",counter)

# setRemove = set()
# for item in occurrences:
#     if item > percentileAfter or item < percentileBefore:
#         # print("Yes : ", item)
#         setRemove.add(item)
#         # occurrences.remove(item)
# # print(setRemove)
# # print(" ---> " , len(occurrences))

# for setItem in setRemove:
#     # print("items removing : ", setItem)
#     occurrences.remove(setItem)

# print(max(occurrences) - min(occurrences))