import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
from community_detection_algorithm import detect_communities

def returnSelectedSetNeighbours(graph,selectedSet):
    selectedSetCover = set()
    for node in selectedSet:
        for neighbour in graph.neighbors(node):
                selectedSetCover.add(neighbour)   
    return selectedSetCover

def randomCommunityGreedySelection(graph,k, communities):
    selectedSet = set()
    setSelectedCommunity = set()
    exhaustedCommunity = set()
    neighboursVisited = set()

    while len(selectedSet) < k:

        #Select a community randomly
        community_id = random.choice(range(0,len(communities)))
        
        #Reset the community set if all communities have been visited atleast once
        if len(selectedSet) < k and len(setSelectedCommunity)==len(communities):
            setSelectedCommunity = set()
        
        itr = 0
        for community in communities:
            if(itr == community_id and itr in exhaustedCommunity):
                # Tall nodes from this community have been selected
                break
            if(itr == community_id and itr not in exhaustedCommunity):
                if set(community).issubset(set(selectedSet)):
                    #add to exhaust if all elements in the community has been selected.
                    exhaustedCommunity.add(itr)
                    break                            
                if community_id not in setSelectedCommunity:
                    setSelectedCommunity.add(community_id)
                    if len(selectedSet)==0:
                        potentialNode = random.choice(community)
                    else:
                        potentialNode = -1
                        potentialNodeMaxCover = -1
                        selectedSetCover = returnSelectedSetNeighbours(graph,selectedSet)
                        for node in community:
                            if node not in selectedSet:
                                potentialSetCover = set()
                                for neighbour in graph.neighbors(node):
                                    potentialSetCover.add(neighbour)
                                not_in_selectedSet = set()
                                for element in potentialSetCover:
                                    if element not in selectedSetCover:
                                        not_in_selectedSet.add(element)
                                if int(potentialNodeMaxCover) < len(not_in_selectedSet):
                                    potentialNodeMaxCover = len(not_in_selectedSet)
                                    potentialNode = node
                    selectedSet.add(potentialNode)
            itr = itr + 1
    return selectedSet