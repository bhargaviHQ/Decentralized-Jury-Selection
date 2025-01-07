import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability

from metrics.Fairness import equality_of_selection
from networkit import *  
import networkit as nk 


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
    num_nodes = graph.numberOfNodes()
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    if algoIndex == 1:
        for i in range (0,100):
            selectedSet = random_select.randomSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,100):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    
    elif algoIndex == 3:
        for i in range (0,100):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in list(graph.iterNodes()):
        probability[nodex] =  occurrences[nodex] / sum(occurrences)

    return  np.mean(probability), np.std(probability)

def variationOfNetworkSize(graph, jurySize, fileName, mu):
    # graph_param_list = [
    #     graphObject(2000, 5, 10, 10, 20)
    #     ]
    networkSizeList = generator.networkSizeList
    meanList =  [0]*3
    stdList =  [0]*3
    distanceList_01 = [0]*len(networkSizeList)
    distanceList_02 = [0]*len(networkSizeList)
    distanceList_03 = [0]*len(networkSizeList)
    itr = 0
    networkSize = graph.numberOfNodes()
    meanList[0],stdList[0] = variationRunAlgo(1,jurySize,graph)
    meanList[1],stdList[1] = variationRunAlgo(2,jurySize,graph)
    meanList[2],stdList[2] = variationRunAlgo(3,jurySize,graph)

    algoList = ["Random","Greedy","Greedy Probability"]
    
    fig, ax = plt.subplots()
    ax.bar(algoList, stdList, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Standard Deviation of Probabilities of selection')
    ax.set_xticks(algoList)
    ax.set_xticklabels(algoList)
    # ax.set_title('Equality of Selectionn n={}'.format(networkSize))
    ax.set_title('Equality of Selection n = {}; j = {}; mu={} '.format(networkSize,jurySize,mu))
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig(fileName)



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

G = nk.readGraph("/Users/bhargavi/Documents/research work/research_code/August 2023/visualization_other_graphs/facebook_combined.txt",nk.Format.SNAP)
print(G.numberOfNodes(), G.numberOfEdges())

variationOfNetworkSize(G,4,"screenshots_equality/fb_disparity_n_100_j_4_mu_01.jpg",0.1)

