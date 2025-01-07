import sys
sys.path.append('../../../')
import imports
from imports import *

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability

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

    def setGraphObjectMu(self,mu):
        graph_object_list = []
        graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

def variationRunAlgo(algoIndex, jurySize, graph, radius):
    iterations = 100
    fractNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
    
    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    return  np.mean(fractNodeCovList)

def variationOfRadiusSize(graph_param_list, jurySize, fileName, mu):
    # graph_param_list = [
    #     graphObject(15, 5, 10, 5, 10)
    #     ]
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
            graphObjects = obj.setGraphObjectMu(mu)
            for graph in graphObjects:
                for radius in radius_list:
                    networkSize = len(graph.nodes)
                    # jurySize = round(networkSize*0.05)

                    fractNodeCov_01 = variationRunAlgo(1,jurySize,graph,radius)
                    fractNodeCov_02 = variationRunAlgo(2,jurySize,graph,radius)
                    fractNodeCov_03 = variationRunAlgo(3,jurySize,graph,radius)

                    fractNodeCovList_01[itr] = fractNodeCov_01
                    fractNodeCovList_02[itr] = fractNodeCov_02
                    fractNodeCovList_03[itr] = fractNodeCov_03

                    itr = itr + 1
    plt.clf()
    plt.plot(radius_list,fractNodeCovList_01, label="Random")
    plt.plot(radius_list,fractNodeCovList_02, label="Greedy")
    plt.plot(radius_list,fractNodeCovList_03, label="Greedy Probability")
    
    plt.xlabel('radius size', fontsize=10)
    plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
    # plt.title("Comparision of Fractional Node Coverage for varying radius size n={}".format(networkSize))
    plt.title('Fractional Node Coverage for varying radius size n={}; j = {}; mu={} '.format(networkSize,jurySize,mu))


    plt.legend()
    plt.savefig(fileName)
    #plt.show()

# variationOfRadiusSize()

graph_param_list_01 = [
        graphObject(100, 5, 10, 5, 10)
        ]
graph_param_list_02 = [
    graphObject(500, 5, 10, 10, 20)
        ]
graph_param_list_03 = [
    graphObject(1000, 5, 10, 10, 20)
        ]
graph_param_list_04 = [
    graphObject(2500, 5, 10, 15, 25)
        ]
graph_param_list_05 = [
    graphObject(10000, 5, 10, 20, 35)
        ]
graph_param_list_06 = [
    graphObject(30000, 5, 10, 25, 40)
        ]


muList = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

for mu in muList:
    print("Running ... mu value : ",mu," network: 1",)
    variationOfRadiusSize(graph_param_list_01,12,"NEWIMGS/frac_cov_n_100_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 2",)
    variationOfRadiusSize(graph_param_list_02,12,"NEWIMGS/frac_cov_n_500_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 3",)
    variationOfRadiusSize(graph_param_list_03,12,"screenshots_fractional_cov/frac_cov_n_1000_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 4",)
    variationOfRadiusSize(graph_param_list_04,12,"screenshots_fractional_cov/frac_cov_n_2500_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 5",)
    variationOfRadiusSize(graph_param_list_05,12,"screenshots_fractional_cov/frac_cov_n_10000_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 6",)
    variationOfRadiusSize(graph_param_list_06,12,"screenshots_fractional_cov/frac_cov_n_30000_j_12_mu_"+str(mu)+".jpg",mu)



juryList = [4,7,10,12,15,20]
for jury in juryList:
    print("Running ... jury Size : ",jury," network: 1",)
    variationOfRadiusSize(graph_param_list_01,jury,"NEWIMGS/frac_cov_n_100_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 2",)
    variationOfRadiusSize(graph_param_list_02,jury,"NEWIMGS/frac_cov_n_500_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 3",)
    variationOfRadiusSize(graph_param_list_03,jury,"screenshots_fractional_cov/frac_cov_n_1000_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 4",)
    variationOfRadiusSize(graph_param_list_04,jury,"screenshots_fractional_cov/frac_cov_n_2500_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 5",)
    variationOfRadiusSize(graph_param_list_05,jury,"screenshots_fractional_cov/frac_cov_n_10000_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 6",)
    variationOfRadiusSize(graph_param_list_06,jury,"screenshots_fractional_cov/frac_cov_n_30000_j_"+str(jury)+"_mu_0.1.jpg",0.1)
