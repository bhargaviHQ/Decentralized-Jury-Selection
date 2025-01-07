import sys
sys.path.append('../../../')
import imports
from imports import *

from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm import rand_community_greedy_select
from algorithm import rand_community_select
from algorithm import rand_probability_select
from graph_generator import generator

from metrics.Measure_of_Spread.Diversity import overlapping_coverage

# The average distance returned by the function is 
# What is the average distance of jurorx to all jurors
# find the average distance for all jurorx in jurorSet
# find the average distance of the average distance for all jurors
#On an average this is the distance from one juror to another juror
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
    uniqueElementsList = [0]*len(jurySizeList)

    if algoIndex == 1:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_select.randomSelection(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            uniqueElementsList[itr] = round(uniqueElements)
            itr += 1    

    elif algoIndex == 2:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            uniqueElementsList[itr] = round(uniqueElements)
            itr += 1    
    
    elif algoIndex == 3:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            uniqueElementsList[itr] = round(uniqueElements)
            itr += 1    
    
    elif algoIndex == 4:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            uniqueElementsList[itr] = round(uniqueElements)
            itr += 1    
 
    elif algoIndex == 5:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            uniqueElementsList[itr] = round(uniqueElements)
            itr += 1    

    return  uniqueElementsList

def variationOfJurySize():
    graph_param = [graphObject(2500, 10, 20, 20, 50)]
    #graph_param = generator.graph_param_jury_size
    for obj in graph_param:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
                uniqueElementsList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph)
                uniqueElementsList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph)
                uniqueElementsList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph)
                uniqueElementsList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph)
                uniqueElementsList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph)

                plt.plot(jurySizeList,uniqueElementsList_01, label="randomSelection")
                plt.plot(jurySizeList,uniqueElementsList_02, label="randomGreedySelection")
                plt.plot(jurySizeList,uniqueElementsList_03, label="randomCommunityGreedySelection")
                plt.plot(jurySizeList,uniqueElementsList_04, label="randomCommunitySelection")
                plt.plot(jurySizeList,uniqueElementsList_05, label="runRandomProbSelect")

                plt.xlabel('jury size', fontsize=10)
                plt.ylabel('# of Unique Elements covered by jurors', fontsize=10)
                plt.title("Comparision of # of Unique Elements covered by jurors for varying jury size")

                plt.legend()
                #plt.show()
                plt.savefig("../../../snapshots/Measure_of_Spread/Diversity/overlap_cov/variationOfJurySize.jpg")

def variationRunAlgo(algoIndex, jurySize, graph ):

    if algoIndex == 1:
            selectedSet = rand_select.randomSelection(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet) 

    elif algoIndex == 2:
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet) 
    
    elif algoIndex == 3:
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet) 

    elif algoIndex == 4:
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet) 
 
    elif algoIndex == 5:
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            uniqueElements  = overlapping_coverage.overlapping_coverage(graph, selectedSet) 
    return  uniqueElements

def variationOfNetworkSize():
    graph_param_list = [
        graphObject(500, 5, 10, 5, 10),
        graphObject(1500, 10, 20, 20, 50),
        graphObject(2500, 10, 20, 20, 50),
        graphObject(5000, 10, 20, 20, 50),
        graphObject(10000, 10, 20, 20, 100)
        ]
    # graph_param_list = generator.graph_param_list
    # networkSizeList = [50,100,200]
    networkSizeList = generator.networkSizeList
    uniqueElementsList_01 = [0]*len(networkSizeList)
    uniqueElementsList_02 = [0]*len(networkSizeList)
    uniqueElementsList_03 = [0]*len(networkSizeList)
    uniqueElementsList_04 = [0]*len(networkSizeList)
    uniqueElementsList_05 = [0]*len(networkSizeList)
    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)
        
                uniqueElements_01 = variationRunAlgo(1,jurySize,graph)
                uniqueElements_02 = variationRunAlgo(2,jurySize,graph)
                uniqueElements_03 = variationRunAlgo(3,jurySize,graph)
                uniqueElements_04 = variationRunAlgo(4,jurySize,graph)
                uniqueElements_05 = variationRunAlgo(5,jurySize,graph)

                uniqueElementsList_01[itr] = uniqueElements_01
                uniqueElementsList_02[itr] = uniqueElements_02
                uniqueElementsList_03[itr] = uniqueElements_03
                uniqueElementsList_04[itr] = uniqueElements_04
                uniqueElementsList_05[itr] = uniqueElements_05
    
                itr = itr + 1

    plt.plot(networkSizeList,uniqueElementsList_01, label="randomSelection")
    plt.plot(networkSizeList,uniqueElementsList_02, label="randomGreedySelection")
    plt.plot(networkSizeList,uniqueElementsList_03, label="randomCommunityGreedySelection")
    plt.plot(networkSizeList,uniqueElementsList_04, label="randomCommunitySelection")
    plt.plot(networkSizeList,uniqueElementsList_05, label="runRandomProbSelect")

    plt.xlabel('Network Size', fontsize=10)
    plt.ylabel('# of Unique Elements covered by jurors', fontsize=10)
    plt.title("Comparision of # of Unique Elements covered by jurors for varying network size")

    plt.legend()
    #plt.show()
    plt.savefig("../../../snapshots/Measure_of_Spread/Diversity/overlap_cov/variationOfNetworkSize.jpg")


def variationOfMuValues():
    graph_param_list = [
        graphObject(2500, 10, 20, 20, 50)
        ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    mu_list = generator.mu_list
    uniqueElementsList_01 = [0]*len(mu_list)
    uniqueElementsList_02 = [0]*len(mu_list)
    uniqueElementsList_03 = [0]*len(mu_list)
    uniqueElementsList_04 = [0]*len(mu_list)
    uniqueElementsList_05 = [0]*len(mu_list)

    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObjectMuVariation()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)

                uniqueElements_01 = variationRunAlgo(1,jurySize,graph)
                uniqueElements_02 = variationRunAlgo(2,jurySize,graph)
                uniqueElements_03 = variationRunAlgo(3,jurySize,graph)
                uniqueElements_04 = variationRunAlgo(4,jurySize,graph)
                uniqueElements_05 = variationRunAlgo(5,jurySize,graph)

                uniqueElementsList_01[itr] = uniqueElements_01
                uniqueElementsList_02[itr] = uniqueElements_02
                uniqueElementsList_03[itr] = uniqueElements_03
                uniqueElementsList_04[itr] = uniqueElements_04
                uniqueElementsList_05[itr] = uniqueElements_05

                itr = itr + 1
    
    plt.plot(mu_list,uniqueElementsList_01, label="randomSelection")
    plt.plot(mu_list,uniqueElementsList_02, label="randomGreedySelection")
    plt.plot(mu_list,uniqueElementsList_03, label="randomCommunityGreedySelection")
    plt.plot(mu_list,uniqueElementsList_04, label="randomCommunitySelection")
    plt.plot(mu_list,uniqueElementsList_05, label="runRandomProbSelect")

    plt.xlabel('fraction of inter-community edges', fontsize=10)
    plt.ylabel('# of Unique Elements covered by jurors', fontsize=10)
    plt.title("Comparision of # of Unique Elements covered by jurors for varying fraction of inter-community edges")

    plt.legend()
    #plt.show()
    plt.savefig("../../../snapshots/Measure_of_Spread/Diversity/overlap_cov/variationOfMuValues.jpg")

variationOfJurySize()
variationOfNetworkSize()
variationOfMuValues()