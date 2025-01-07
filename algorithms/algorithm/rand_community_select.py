import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
from community_detection_algorithm import detect_communities

def randomCommunitySelection(graph, k, communities):
    
    selectedSet = set()
    setSelectedCommunity = set()
    exhaustedCommunity = set()

    while len(selectedSet) < k:
        community_id = random.choice(range(0,len(communities)))
        itr = 0
        #Reset the community set if all communities have been visited atleast once
        if len(selectedSet) < k and len(setSelectedCommunity)==len(communities):
            setSelectedCommunity = set()

        for community in communities:
            if(itr == community_id and itr in exhaustedCommunity):
                # This community has no elements
                break
            if(itr == community_id and itr not in exhaustedCommunity):
                if set(community).issubset(set(selectedSet)):
                    #add to exhaust if all elements in the community has been selected.
                    exhaustedCommunity.add(itr)
                    break

                if community_id not in setSelectedCommunity:
                    setSelectedCommunity.add(community_id)
                    selectedNode = random.choice(community)
                    marked_nodes = set()
                    flag = 0
                    for select in selectedSet:
                        if selectedNode in graph.neighbors(select):
                            marked_nodes.add(selectedNode)
                            flag = 1
                            break
                            
                    while(selectedNode in marked_nodes):
                        flag = 0
                        selectedNode = random.choice(community)
                        for select in selectedSet:
                            if selectedNode in graph.neighbors(select):
                                marked_nodes.add(selectedNode)
                                flag = 1
                                break

                        if len(marked_nodes) == len(community) or flag == 1:
                            selectedNode = random.choice(community)
                            break
                            
                    selectedSet.add(selectedNode)
                    break
            itr = itr + 1
    return selectedSet


# k=8

# for obj in generator.graph_param_list:
#     graphObjects = obj.setGraphObject()
#     for graph in graphObjects:
#         print(graph.number_of_nodes())
#         for func in detect_communities.cd_function_list:
#             print(" ->  fun:  <-",func, " - > selected set : ",randomCommunitySelection(graph, k, func(graph).communities))
        