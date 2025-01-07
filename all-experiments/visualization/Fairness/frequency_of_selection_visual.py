import sys
sys.path.append('../../')
import imports
from imports import *

from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm import rand_community_greedy_select
from algorithm import rand_community_select
from algorithm import rand_probability_select
from graph_generator import generator

from metrics.Fairness import frequency_of_selection

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes, average_degree = 5, max_degree = 10, min_community = 5, max_community = 10):
        self.nodes = nodes
        self.average_degree = average_degree 
        self.max_degree  = max_degree
        self.min_community = min_community
        self.max_community = max_community

    def setGraphObjectMuVariation(self):
        graph_object_list = []
        mu_list = [0.1,0.4,0.6,0.8]
        for mu in mu_list:
            graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

    def setGraphObject(self):
        graph_object_list = []
        mu_list = [0.1]
        for mu in mu_list:
            graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

#graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)



def variationOfJurySizePlotAlgo(algoIndex, jurySizeList, graph):
    num_nodes = len(graph.nodes)   
    occurrencesList = [0]*len(jurySizeList)
    disparity = [0]*len(jurySizeList)
    occurrences = [0] * num_nodes
    delta = 5
    itr = 0
    if algoIndex == 1:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_select.randomSelection(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)
            occurrencesList[itr] = occurrences
            itr += 1  

    elif algoIndex == 2:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            occurrencesList[itr] = occurrences
            itr += 1  

    elif algoIndex == 3:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            occurrencesList[itr] = occurrences
            itr += 1  

    elif algoIndex == 4:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            occurrencesList[itr] = occurrences
            itr += 1  

    elif algoIndex == 5:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            occurrencesList[itr] = occurrences
            itr += 1  

    itr = 0
    for occur in occurrencesList:
        occur.sort(reverse=True)
        percentileBefore =  np.percentile(occur, delta)
        percentileAfter = np.percentile(occur, (100 - delta))

        setRemove = set()
        for item in occur:
            if item > percentileAfter or item < percentileBefore:
                setRemove.add(item)
        for setItem in setRemove:
            occur.remove(setItem)
        disparity[itr] = max(occur) - min(occur)
        itr += 1
    return  disparity

def variationOfJurySize():
    # graph_param = [graphObject(100, 5, 10, 5, 10)]
    graph_param = [graphObject(2500, 10, 20, 20, 50)]
    #graph_param = generator.graph_param_jury_size
    for obj in graph_param:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
                distanceList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph)
                distanceList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph)
                distanceList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph)
                distanceList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph)
                distanceList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph)

                plt.plot(jurySizeList,distanceList_01, label="randomSelection")
                plt.plot(jurySizeList,distanceList_02, label="randomGreedySelection")
                plt.plot(jurySizeList,distanceList_03, label="randomCommunityGreedySelection")
                plt.plot(jurySizeList,distanceList_04, label="randomCommunitySelection")
                plt.plot(jurySizeList,distanceList_05, label="runRandomProbSelect")

                plt.xlabel('jury size', fontsize=10)
                plt.ylabel('Disparity in frequency of selection', fontsize=10)
                plt.title("Comparision of Disparity in frequency of selection for varying jury size")

                plt.legend()
                #plt.show()
                plt.savefig("../../snapshots/Fairness/freq_of_select/variationOfJurySize.jpg")


def variationRunAlgo(algoIndex, jurySize, graph ):
    num_nodes = len(graph.nodes)
    occurrences = [0] * num_nodes
    delta = 5

    if algoIndex == 1:
        for i in range (0,100):
            selectedSet = rand_select.randomSelection(graph, jurySize)
            occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,100):
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)

    
    elif algoIndex == 3:
        for i in range (0,100):
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 4:
        for i in range (0,100):
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)
 
    elif algoIndex == 5:
        for i in range (0,100):
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)
 
    occurrences.sort(reverse=True)
    percentileBefore =  np.percentile(occurrences, delta)
    percentileAfter = np.percentile(occurrences, (100 - delta))

    setRemove = set()
    for item in occurrences:
        if item > percentileAfter or item < percentileBefore:
            setRemove.add(item)
    for setItem in setRemove:
        occurrences.remove(setItem)
    disparity = max(occurrences) - min(occurrences)

    return  disparity

def variationOfNetworkSize():
    graph_param_list = [
        graphObject(500, 5, 10, 5, 10),
        graphObject(1500, 10, 20, 20, 50),
        graphObject(2500, 10, 20, 20, 50),
        graphObject(5000, 10, 20, 20, 50),
        graphObject(10000, 10, 20, 20, 100)
        ]
    #graph_param_list = generator.graph_param_list
    # networkSizeList = [50,100,200]
    networkSizeList = generator.networkSizeList

    distanceList_01 = [0]*len(networkSizeList)
    distanceList_02 = [0]*len(networkSizeList)
    distanceList_03 = [0]*len(networkSizeList)
    distanceList_04 = [0]*len(networkSizeList)
    distanceList_05 = [0]*len(networkSizeList)
    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)
        
                distance_01 = variationRunAlgo(1,jurySize,graph)
                distance_02 = variationRunAlgo(2,jurySize,graph)
                distance_03 = variationRunAlgo(3,jurySize,graph)
                distance_04 = variationRunAlgo(4,jurySize,graph)
                distance_05 = variationRunAlgo(5,jurySize,graph)

                distanceList_01[itr] = distance_01
                distanceList_02[itr] = distance_02
                distanceList_03[itr] = distance_03
                distanceList_04[itr] = distance_04
                distanceList_05[itr] = distance_05
    
                itr = itr + 1
    plt.plot(networkSizeList,distanceList_01, label="randomSelection")
    plt.plot(networkSizeList,distanceList_02, label="randomGreedySelection")
    plt.plot(networkSizeList,distanceList_03, label="randomCommunityGreedySelection")
    plt.plot(networkSizeList,distanceList_04, label="randomCommunitySelection")
    plt.plot(networkSizeList,distanceList_05, label="runRandomProbSelect")
   
    plt.xlabel('Network Size', fontsize=10)
    plt.ylabel('Disparity in frequency of selection', fontsize=10)
    plt.title("Comparision of Disparity in frequency of selection for varying network size")

    plt.legend()
    #plt.show()
    plt.savefig("../../snapshots/Fairness/freq_of_select/variationOfNetworkSize.jpg")


def variationOfMuValues():
    graph_param_list = [
       graphObject(2500, 10, 20, 20, 50)
        ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    mu_list = generator.mu_list
    distanceList_01 = [0]*len(mu_list)
    distanceList_02 = [0]*len(mu_list)
    distanceList_03 = [0]*len(mu_list)
    distanceList_04 = [0]*len(mu_list)
    distanceList_05 = [0]*len(mu_list)

    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObjectMuVariation()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)

                distance_01 = variationRunAlgo(1,jurySize,graph)
                distance_02 = variationRunAlgo(2,jurySize,graph)
                distance_03 = variationRunAlgo(3,jurySize,graph)
                distance_04 = variationRunAlgo(4,jurySize,graph)
                distance_05 = variationRunAlgo(5,jurySize,graph)

                distanceList_01[itr] = distance_01
                distanceList_02[itr] = distance_02
                distanceList_03[itr] = distance_03
                distanceList_04[itr] = distance_04
                distanceList_05[itr] = distance_05

                itr = itr + 1
    
    plt.plot(mu_list,distanceList_01, label="randomSelection")
    plt.plot(mu_list,distanceList_02, label="randomGreedySelection")
    plt.plot(mu_list,distanceList_03, label="randomCommunityGreedySelection")
    plt.plot(mu_list,distanceList_04, label="randomCommunitySelection")
    plt.plot(mu_list,distanceList_05, label="runRandomProbSelect")


    plt.xlabel('fraction of inter-community edges', fontsize=10)
    plt.ylabel('Disparity in frequency of selection', fontsize=10)
    plt.title("Comparision of Disparity in frequency of selection for varying fraction of inter-community edges")

    plt.legend()
    #plt.show()
    plt.savefig("../../snapshots/Fairness/freq_of_select/variationOfMuValues.jpg")

variationOfJurySize()
variationOfNetworkSize()
variationOfMuValues()