import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability

from metrics.Measure_of_Spread.Coverage import maximum_coverage

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

    def setGraphObjectMu(self,mu):
        graph_object_list = []
        graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

def variationRunAlgo(algoIndex, jurySize, graph):
    iterations = 100
    maxNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverage(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverage(graph, selectedSet)
            itr = itr + 1
    
    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverage(graph, selectedSet)
            itr = itr + 1

    return  np.mean(maxNodeCovList)


def variationOfNetworkSize(graph_param_list, jurySize, fileName, mu):
    # graph_param_list = [
    #     graphObject(15, 5, 10, 5, 10)
    #     ]
    networkSizeList = generator.networkSizeList
    disparity =  [0]*3
    distanceList_01 = [0]*len(networkSizeList)
    distanceList_02 = [0]*len(networkSizeList)
    distanceList_03 = [0]*len(networkSizeList)
    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObjectMu(mu)
            for graph in graphObjects:
                
                networkSize = len(graph.nodes)
                # jurySize = round(networkSize*0.09)
        
                disparity[0] = variationRunAlgo(1,jurySize,graph)
                disparity[1] = variationRunAlgo(2,jurySize,graph)
                disparity[2] = variationRunAlgo(3,jurySize,graph)
                
                # distanceList_01[itr] = distance_01
                # distanceList_02[itr] = distance_02
                # distanceList_03[itr] = distance_03
    
                itr = itr + 1
    
    algoList = ["Random","Greedy","Greedy Probability"]
    print("max Coverage : ::: ", disparity)
    fig, ax = plt.subplots()
    ax.bar(algoList, disparity, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Minimum distance of selection')
    ax.set_xticks(algoList)
    ax.set_xticklabels(algoList)
    # ax.set_title('Minimum distance')
    ax.set_title('Minimum distance of selection n = {}; j = {}; mu={} '.format(networkSize,jurySize,mu))
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig(fileName)
    #plt.show()



    output = PrettyTable(['Algorithm','Network Size', 'Avg probability of node selection'])

    output.add_row(['Random Selection',networkSizeList[0],round(distanceList_01[0],10)])
    output.add_row(['Greedy Selection',networkSizeList[1],round(distanceList_02[0],10)])
    output.add_row(['Greedy Probabiity Selection',networkSizeList[2],round(distanceList_03[0],10)])

    
    # print(output)

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
    variationOfNetworkSize(graph_param_list_01,12,"screenshots_max_cov/max_cov_n_100_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 2",)
    variationOfNetworkSize(graph_param_list_02,12,"screenshots_max_cov/max_cov_n_500_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 3",)
    variationOfNetworkSize(graph_param_list_03,12,"screenshots_max_cov/max_cov_n_1000_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 4",)
    variationOfNetworkSize(graph_param_list_04,12,"screenshots_max_cov/max_cov_n_2500_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 5",)
    variationOfNetworkSize(graph_param_list_05,12,"screenshots_max_cov/max_cov_n_10000_j_12_mu_"+str(mu)+".jpg",mu)
    
    print("Running ... mu value : ",mu," network: 6",)
    variationOfNetworkSize(graph_param_list_06,12,"screenshots_max_cov/max_cov_n_30000_j_12_mu_"+str(mu)+".jpg",mu)

juryList = [4,7,10,12,15,20]
for jury in juryList:
    print("Running ... jury Size : ",jury," network: 1",)
    variationOfNetworkSize(graph_param_list_01,jury,"screenshots_max_cov/max_cov_n_100_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 2",)
    variationOfNetworkSize(graph_param_list_02,jury,"screenshots_max_cov/max_cov_n_500_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 3",)
    variationOfNetworkSize(graph_param_list_03,jury,"screenshots_max_cov/max_cov_n_1000_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 4",)
    variationOfNetworkSize(graph_param_list_04,jury,"screenshots_max_cov/max_cov_n_2500_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 5",)
    variationOfNetworkSize(graph_param_list_05,jury,"screenshots_max_cov/max_cov_n_10000_j_"+str(jury)+"_mu_0.1.jpg",0.1)
    
    print("Running ... jury Size : ",jury," network: 6",)
    variationOfNetworkSize(graph_param_list_06,jury,"screenshots_max_cov/max_cov_n_30000_j_"+str(jury)+"_mu_0.1.jpg",0.1)