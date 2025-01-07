import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository_networkit import greedy_Betweenness
from algorithm_repository_networkit import greedy_coverage
from algorithm_repository_networkit import Prob_Betweenness
from algorithm_repository_networkit import Prob_Coverage
from algorithm_repository_networkit import random_select
from algorithm_repository_networkit import RCL_Betweenness
from algorithm_repository_networkit import RCL_coverage
from algorithm_repository_networkit import Seed_Betweenness
from algorithm_repository_networkit import Seed_Coverage

from metrics.Fairness import equality_of_selection

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250, edges = 2):
        self.nodes = nodes
        self.edges = edges 

    def getParams (self):
        print("Nodes : ", self.nodes, " edges : ",self.edges)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        # G = nx.barabasi_albert_graph(self.nodes,self.edges)
        G = nk.generators.BarabasiAlbertGenerator(self.edges,self.nodes).generate()
        return G

    def graphGeneratoredges(self, edges):
        # Create the powerlaw-clustered network
        #G = nx.barabasi_albert_graph(self.nodes,edges)
        G = nk.generators.BarabasiAlbertGenerator(edges,self.nodes).generate()
        return G

def plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,algorithm_8,algorithm_9,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(xplotList,algorithm_1, linestyle='--', label="GB")
    plt.plot(xplotList,algorithm_2, linestyle='--', label="GC")
    plt.plot(xplotList,algorithm_3, label="PB")
    plt.plot(xplotList,algorithm_4, label="PC")
    plt.plot(xplotList,algorithm_5, linestyle='--', label="R")
    plt.plot(xplotList,algorithm_6, label="CB")
    plt.plot(xplotList,algorithm_7, label="CC")
    plt.plot(xplotList,algorithm_8, label="SB")
    plt.plot(xplotList,algorithm_9, label="SC")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities of selection', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    iterations = 100
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = greedy_Betweenness.greedyBetweennessSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy_coverage.greedyCoverageSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

     
    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = Prob_Coverage.coverageSelectionWithProb(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 6:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 7:
        for i in range (0,iterations):
            selectedSet = RCL_coverage.rclCoverageSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 8:
        for i in range (0,iterations):
            selectedSet = Seed_Betweenness.seedBetweenSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 9:
        for i in range (0,iterations):
            selectedSet = Seed_Coverage.seedCoverSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)
    probabilityAverage = sum(probability)/len(probability)
    return  np.std(probability)

def variationOfNetworkParams(graph_param_list,xplotList, jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    algorithm_8 = [0]*len(xplotList)
    algorithm_9 = [0]*len(xplotList)

    itr = 0
    for obj in graph_param_list:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                algorithm_5[itr] = variationRunAlgo(5,jurySize,graph)
                algorithm_6[itr] = variationRunAlgo(6,jurySize,graph)
                algorithm_7[itr] = variationRunAlgo(7,jurySize,graph)
                algorithm_8[itr] = variationRunAlgo(8,jurySize,graph)
                algorithm_9[itr] = variationRunAlgo(9,jurySize,graph)
                itr = itr + 1
    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,algorithm_8,algorithm_9,fileName,xplotName,jurySize)
   
def variationOfJurySize(graph_param_list,xplotList, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    algorithm_8 = [0]*len(xplotList)
    algorithm_9 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for jurySize in xplotList:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                algorithm_5[itr] = variationRunAlgo(5,jurySize,graph)
                algorithm_6[itr] = variationRunAlgo(6,jurySize,graph)
                algorithm_7[itr] = variationRunAlgo(7,jurySize,graph)
                algorithm_8[itr] = variationRunAlgo(8,jurySize,graph)
                algorithm_9[itr] = variationRunAlgo(9,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,algorithm_8,algorithm_9,fileName,xplotName,jurySize)

def variationOfedges(graph_param_list,xplotList,jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    algorithm_8 = [0]*len(xplotList)
    algorithm_9 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for edges in xplotList:
                graph = obj.graphGeneratoredges(edges)
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                algorithm_5[itr] = variationRunAlgo(5,jurySize,graph)
                algorithm_6[itr] = variationRunAlgo(6,jurySize,graph)
                algorithm_7[itr] = variationRunAlgo(7,jurySize,graph)
                algorithm_8[itr] = variationRunAlgo(8,jurySize,graph)
                algorithm_9[itr] = variationRunAlgo(9,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,algorithm_8,algorithm_9,fileName,xplotName,jurySize)

graph_param_list_Networks = [
        graphObject(100,2),
        graphObject(250,2),
        graphObject(500,2),
        graphObject(750,2)
        ]
   
graph_param_list = [
        graphObject(250,2)
        ]
        
#############
# VARYING VALUES OF Network
#############
xplotName = "Network size"
xplotList = [100,250,500,750]
variationOfNetworkParams(graph_param_list_Networks,xplotList,7,"screenshots_equality/equality_closeness_network_central.jpg",xplotName)

#############
# VARYING VALUES OF jury size
#############

xplotName = "Jury size"
xplotList =  [4,7,10,12,15]
variationOfJurySize(graph_param_list,xplotList,"screenshots_equality/equality_closeness_jury_central.jpg",xplotName)


#############
# VARYING VALUES OF Average Degree
#############

xplotName = "No. of edges to attach"
xplotList =  [1,2,3,4,5]
variationOfedges(graph_param_list,xplotList,7,"screenshots_equality/equality_closeness_randomEdge_central.jpg",xplotName)

