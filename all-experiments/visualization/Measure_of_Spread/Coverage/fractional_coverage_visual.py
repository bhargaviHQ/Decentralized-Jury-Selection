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

from metrics.Measure_of_Spread.Coverage import fractional_coverage

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

    def setGraphObjectMuVariation(self,mu_list):
        graph_object_list = []
        #mu_list = [0.1,0.4,0.6,0.8]
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

def variationOfJurySizePlotAlgo(algoIndex, jurySizeList, graph,radius):
    fractNodeCovList = [0]*len(jurySizeList)

    if algoIndex == 1:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_select.randomSelection(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            fractNodeCovList[itr] = round(fractNodeCov)
            itr += 1    

    elif algoIndex == 2:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            fractNodeCovList[itr] = round(fractNodeCov)
            itr += 1    
    
    elif algoIndex == 3:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            fractNodeCovList[itr] = round(fractNodeCov)
            itr += 1    
    
    elif algoIndex == 4:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            fractNodeCovList[itr] = round(fractNodeCov)
            itr += 1    
 
    elif algoIndex == 5:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            fractNodeCovList[itr] = round(fractNodeCov)
            itr += 1    

    return  fractNodeCovList

def variationOfJurySize():
    radius = generator.radius
    graph_param = [graphObject(2500, 10, 20, 20, 50)]
    #graph_param = generator.graph_param_jury_size
    for obj in graph_param:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
                fractNodeCovList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph,radius)
                fractNodeCovList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph,radius)
                fractNodeCovList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph,radius)
                fractNodeCovList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph,radius)
                fractNodeCovList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph,radius)

                plt.plot(jurySizeList,fractNodeCovList_01, label="randomSelection")
                plt.plot(jurySizeList,fractNodeCovList_02, label="randomGreedySelection")
                plt.plot(jurySizeList,fractNodeCovList_03, label="randomCommunityGreedySelection")
                plt.plot(jurySizeList,fractNodeCovList_04, label="randomCommunitySelection")
                plt.plot(jurySizeList,fractNodeCovList_05, label="runRandomProbSelect")

                plt.xlabel('jury size', fontsize=10)
                plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
                plt.title("Comparision of Fractional Node Coverage within radius for varying jury size")

                plt.legend()
                #plt.show()
                plt.savefig("../../../snapshots/Measure_of_Spread/Coverage/fractional_cov/variationOfJurySize.jpg")

def variationRunAlgo(algoIndex, jurySize, graph, radius):

    if algoIndex == 1:
            selectedSet = rand_select.randomSelection(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)

    elif algoIndex == 2:
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
    
    elif algoIndex == 3:
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)

    elif algoIndex == 4:
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
 
    elif algoIndex == 5:
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            fractNodeCov  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
    return  fractNodeCov

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
    radius = generator.radius

    fractNodeCovList_01 = [0]*len(networkSizeList)
    fractNodeCovList_02 = [0]*len(networkSizeList)
    fractNodeCovList_03 = [0]*len(networkSizeList)
    fractNodeCovList_04 = [0]*len(networkSizeList)
    fractNodeCovList_05 = [0]*len(networkSizeList)
    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObject()
            print("length of the graph objects is : ", len(graphObjects))
            for graph in graphObjects:
                
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)
        
                fractNodeCov_01 = variationRunAlgo(1,jurySize,graph,radius)
                fractNodeCov_02 = variationRunAlgo(2,jurySize,graph,radius)
                fractNodeCov_03 = variationRunAlgo(3,jurySize,graph,radius)
                fractNodeCov_04 = variationRunAlgo(4,jurySize,graph,radius)
                fractNodeCov_05 = variationRunAlgo(5,jurySize,graph,radius)

                fractNodeCovList_01[itr] = fractNodeCov_01
                fractNodeCovList_02[itr] = fractNodeCov_02
                fractNodeCovList_03[itr] = fractNodeCov_03
                fractNodeCovList_04[itr] = fractNodeCov_04
                fractNodeCovList_05[itr] = fractNodeCov_05
    
                itr = itr + 1

    plt.plot(networkSizeList,fractNodeCovList_01, label="randomSelection")
    plt.plot(networkSizeList,fractNodeCovList_02, label="randomGreedySelection")
    plt.plot(networkSizeList,fractNodeCovList_03, label="randomCommunityGreedySelection")
    plt.plot(networkSizeList,fractNodeCovList_04, label="randomCommunitySelection")
    plt.plot(networkSizeList,fractNodeCovList_05, label="runRandomProbSelect")

    plt.xlabel('Network Size', fontsize=10)
    plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
    plt.title("Comparision of Fractional Node Coverage within radius for varying network size")

    plt.legend()
    #plt.show()
    plt.savefig("../../../snapshots/Measure_of_Spread/Coverage/fractional_cov/variationOfNetworkSize.jpg")


def variationOfMuValues():
    graph_param_list = [
       graphObject(2500, 10, 20, 20, 50)
        ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    mu_list = generator.mu_list
    radius = generator.radius
    fractNodeCovList_01 = [0]*len(mu_list)
    fractNodeCovList_02 = [0]*len(mu_list)
    fractNodeCovList_03 = [0]*len(mu_list)
    fractNodeCovList_04 = [0]*len(mu_list)
    fractNodeCovList_05 = [0]*len(mu_list)

    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObjectMuVariation(mu_list)
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)

                fractNodeCov_01 = variationRunAlgo(1,jurySize,graph,radius)
                fractNodeCov_02 = variationRunAlgo(2,jurySize,graph,radius)
                fractNodeCov_03 = variationRunAlgo(3,jurySize,graph,radius)
                fractNodeCov_04 = variationRunAlgo(4,jurySize,graph,radius)
                fractNodeCov_05 = variationRunAlgo(5,jurySize,graph,radius)

                fractNodeCovList_01[itr] = fractNodeCov_01
                fractNodeCovList_02[itr] = fractNodeCov_02
                fractNodeCovList_03[itr] = fractNodeCov_03
                fractNodeCovList_04[itr] = fractNodeCov_04
                fractNodeCovList_05[itr] = fractNodeCov_05

                itr = itr + 1
    
    plt.plot(mu_list,fractNodeCovList_01, label="randomSelection")
    plt.plot(mu_list,fractNodeCovList_02, label="randomGreedySelection")
    plt.plot(mu_list,fractNodeCovList_03, label="randomCommunityGreedySelection")
    plt.plot(mu_list,fractNodeCovList_04, label="randomCommunitySelection")
    plt.plot(mu_list,fractNodeCovList_05, label="runRandomProbSelect")

    plt.xlabel('fraction of inter-community edges', fontsize=10)
    plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
    plt.title("Comparision of Fractional Node Coverage within radius for varying fraction of inter-community edges")

    plt.legend()
    #plt.show()
    plt.savefig("../../../snapshots/Measure_of_Spread/Coverage/fractional_cov/variationOfMuValues.jpg")

def variationOfRadiusSize():
    graph_param_list = [
       graphObject(2500, 10, 20, 20, 50)
        ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    #mu_list = generator.mu_list
    #radius = generator.radius
    radius_list = [1,2,3,4,5]
    fractNodeCovList_01 = [0]*len(radius_list)
    fractNodeCovList_02 = [0]*len(radius_list)
    fractNodeCovList_03 = [0]*len(radius_list)
    fractNodeCovList_04 = [0]*len(radius_list)
    fractNodeCovList_05 = [0]*len(radius_list)

    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                for radius in radius_list:
                    networkSize = len(graph.nodes)
                    jurySize = round(networkSize*0.05)

                    fractNodeCov_01 = variationRunAlgo(1,jurySize,graph,radius)
                    fractNodeCov_02 = variationRunAlgo(2,jurySize,graph,radius)
                    fractNodeCov_03 = variationRunAlgo(3,jurySize,graph,radius)
                    fractNodeCov_04 = variationRunAlgo(4,jurySize,graph,radius)
                    fractNodeCov_05 = variationRunAlgo(5,jurySize,graph,radius)

                    fractNodeCovList_01[itr] = fractNodeCov_01
                    fractNodeCovList_02[itr] = fractNodeCov_02
                    fractNodeCovList_03[itr] = fractNodeCov_03
                    fractNodeCovList_04[itr] = fractNodeCov_04
                    fractNodeCovList_05[itr] = fractNodeCov_05

                    itr = itr + 1
        
    plt.plot(radius_list,fractNodeCovList_01, label="randomSelection")
    plt.plot(radius_list,fractNodeCovList_02, label="randomGreedySelection")
    plt.plot(radius_list,fractNodeCovList_03, label="randomCommunityGreedySelection")
    plt.plot(radius_list,fractNodeCovList_04, label="randomCommunitySelection")
    plt.plot(radius_list,fractNodeCovList_05, label="runRandomProbSelect")

    plt.xlabel('radius size', fontsize=10)
    plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
    plt.title("Comparision of Fractional Node Coverage within radius for varying radius size")

    plt.legend()
    #plt.show()
    plt.savefig("../../../snapshots/Measure_of_Spread/Coverage/fractional_cov/variationOfRadiusSize.jpg")



variationOfJurySize()
variationOfNetworkSize()
variationOfMuValues()
variationOfRadiusSize()