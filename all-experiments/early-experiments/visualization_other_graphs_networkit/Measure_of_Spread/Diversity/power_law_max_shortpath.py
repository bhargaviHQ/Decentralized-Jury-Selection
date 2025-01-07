import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability
from algorithm_repository import RCL_DegreeCentrality

from metrics.Measure_of_Spread.Diversity import maximum_shortest_path

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 1000,randomEdge = 2, rewire_prob = 0.2):
        self.nodes = nodes
        self.randomEdge = randomEdge 
        self.rewire_prob  = rewire_prob
    def getParams (self):
        print("Nodes : ", self.nodes, " average degree : ",self.randomEdge, " rewire : ", self.rewire_prob)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, m=self.randomEdge, p=self.rewire_prob)
        return G

    def graphGeneratorRandEdge(self, randomEdge):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, m=randomEdge, p=self.rewire_prob)
        return G

    def graphGeneratorRewireProb(self, rewire_prob):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, m=self.randomEdge, p=rewire_prob)
        return G

    def graphGeneratorparam(self, randomEdge, rewire_prob):
        # Create the powerlaw-clustered network
        G = nx.powerlaw_cluster_graph(self.nodes, m=randomEdge, p=rewire_prob)
        
        return G
def plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(xplotList,algorithm_1, label="Random")
    plt.plot(xplotList,algorithm_2, label="Greedy")
    plt.plot(xplotList,algorithm_3, label="Greedy Probability")
    plt.plot(xplotList,algorithm_4, label="RCL DC")
    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Avg distance b/w juror to juror ', fontsize=10)
    plt.title('Avg distance b/w juror to juror for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph):
    iterations = 100
    avgDistList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1


    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    return  np.mean(avgDistList)

def variationOfNetworkParams(graph_param_list,xplotList, jurySize, fileName,xplotName):
    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    itr = 0
    for obj in graph_param_list:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                itr = itr + 1
    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize)
   
def variationOfJurySize(graph_param_list,xplotList, fileName,xplotName):
    

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for jurySize in xplotList:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize)

def variationOfRandomEdge(graph_param_list,xplotList,jurySize, fileName,xplotName):
    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for randEdge in xplotList:
                graph = obj.graphGeneratorRandEdge(randEdge)
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize)

def variationOfRewireProb(graph_param_list,xplotList,jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for rewireProb in xplotList:
                graph = obj.graphGeneratorRewireProb(rewireProb)
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize)


graph_param_list_Networks = [
        graphObject(100, 5,0.2),
        graphObject(1000, 5,0.2),
        graphObject(5000,5,0.2),
        graphObject(10000, 5,0.2),
        graphObject(25000, 5,0.2),
        graphObject(50000, 5,0.2)
        ]
   
graph_param_list = [
        graphObject(2500, 2,0.2)
        ]
        
#############
# VARYING VALUES OF Network
#############
xplotName = "Network size"
xplotList = [100,1000,5000,10000,25000,50000]
variationOfNetworkParams(graph_param_list_Networks,xplotList,7,"screenshots_max_short_path/max_short_path_closeness_network.jpg",xplotName)

#############
# VARYING VALUES OF jury size
#############

xplotName = "Jury size"
xplotList =  [4,7,10,12,15]
variationOfJurySize(graph_param_list,xplotList,"screenshots_max_short_path/max_short_path_closeness_jury.jpg",xplotName)


#############
# VARYING VALUES OF Average Degree
#############

xplotName = "Number of random Edges"
xplotList =  [1,2,3,4,5,6,7]
variationOfRandomEdge(graph_param_list,xplotList,7,"screenshots_max_short_path/max_short_path_closeness_randomedge.jpg",xplotName)


#############
# VARYING VALUES OF rewiring probability
#############

xplotName = "Rewiring probabilities"
xplotList = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
variationOfRewireProb(graph_param_list,xplotList,7,"screenshots_max_short_path/max_short_path_closeness_rewire.jpg",xplotName)