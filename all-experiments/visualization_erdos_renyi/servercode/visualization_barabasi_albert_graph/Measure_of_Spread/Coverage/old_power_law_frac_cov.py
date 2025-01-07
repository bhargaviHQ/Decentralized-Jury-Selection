import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability
from algorithm_repository import RCL_DegreeCentrality

from metrics.Measure_of_Spread.Coverage import fractional_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 1000,average_degree = 5, rewire_prob = 0.2):
        self.nodes = nodes
        self.average_degree = average_degree 
        self.rewire_prob  = rewire_prob
    def getParams (self):
        print("Nodes : ", self.nodes, " average degree : ",self.average_degree, " rewire : ", self.rewire_prob)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, self.average_degree, self.rewire_prob)
        return G

    def graphGeneratorparam(self, average_degree, rewire_prob):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, average_degree, rewire_prob)
        return G
        
def variationRunAlgo(algoIndex, jurySize, graph, radius=0.2):
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

    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    return  np.mean(fractNodeCovList)



def variationOfRadiusSize(graph_param_list, xplotList, jurySize, fileName):
    # graph_param_list = [
    #     graphObject(15, 5, 10, 5, 10)
    #     ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    #mu_list = generator.mu_list
    #radius = generator.radius
    radius_list = [1,2,3]
    fractNodeCovList_01 = [0]*len(radius_list)
    fractNodeCovList_02 = [0]*len(radius_list)
    fractNodeCovList_03 = [0]*len(radius_list)
    fractNodeCovList_04 = [0]*len(radius_list)
    fractNodeCovList_05 = [0]*len(radius_list)

    itr = 0
    for obj in graph_param_list:
                graph = obj.graphGenerator()
                obj.getParams()
                networkSize = len(graph.nodes)
                networkSize = len(graph.nodes)
                fractNodeCovList_01[itr] = variationRunAlgo(1,jurySize,graph,2)
                fractNodeCovList_02[itr] = variationRunAlgo(2,jurySize,graph,2)
                fractNodeCovList_03[itr] = variationRunAlgo(3,jurySize,graph,2)
                fractNodeCovList_04[itr] = variationRunAlgo(4,jurySize,graph,2)
                itr = itr + 1

    plt.clf()
    plt.plot(xplotList,fractNodeCovList_01, label="Random")
    plt.plot(xplotList,fractNodeCovList_02, label="Greedy")
    plt.plot(xplotList,fractNodeCovList_03, label="Greedy Probability")
    plt.plot(xplotList,fractNodeCovList_04, label="RCL DC")
    
    plt.xlabel('radius size', fontsize=10)
    plt.ylabel('Fractional Node Coverage within radius', fontsize=10)
    # plt.title("Comparision of Fractional Node Coverage for varying radius size n={}".format(networkSize))
    plt.title('Fractional Node Coverage for varying radius size n={}; j = {}; '.format(networkSize,jurySize))


    plt.legend()
    plt.show()
   

graph_param_list_01 = [
        graphObject(100, 5,0.3),
        graphObject(500, 5,0.3),
        graphObject(1000,5,0.3)
        ]
#xplotList = [0.1,0.2,0.3,0.4]
xplotList = [100,500,1000]
# xplotList = [5,10,15,20]

variationOfRadiusSize(graph_param_list_01,xplotList,7,"screenshots_equality/equality.jpg")
