import sys
sys.path.append('../')
import imports
from imports import *
from algorithm import rand_community_greedy_select
from algorithm import rand_community_select
from algorithm import rand_greedy_select
from algorithm import rand_select
from graph_generator import generator
from community_detection_algorithm import detect_communities

def runAlgorithms():
    algorithms_list = [
        rand_community_greedy_select.randomCommunityGreedySelection,
        rand_community_select.randomCommunitySelection,
        rand_greedy_select.randomGreedySelection,
        rand_select.randomSelection
    ]

    k=4

    for listitem in algorithms_list:
        for obj in generator.graph_param_list:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                for func in detect_communities.cd_function_list:
                    #listitem(graph, k, func(graph).communities)
                    print(" ->  fun:  <-",func, " - > selected set : ",listitem(graph, k, func(graph).communities))
# runAlgorithms()