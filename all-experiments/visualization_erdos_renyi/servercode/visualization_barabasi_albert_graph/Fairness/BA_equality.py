import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository import random_select
from algorithm_repository import greedy
from algorithm_repository import greedy_probability
from algorithm_repository import RCL_DegreeCentrality
from algorithm_repository import RCL_ClosenessCentral
from algorithm_repository import RCL_Betweenness
from algorithm_repository import RCL_eigenvector

from metrics.Fairness import equality_of_selection
from metrics.Measure_of_Spread.Diversity import overlapping_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 1000, edges = 2):
        self.nodes = nodes
        self.edges = edges 

    def getParams (self):
        print("Nodes : ", self.nodes, " edges : ",self.edges)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        G = nx.barabasi_albert_graph(self.nodes,self.edges)
        return G

    def graphGeneratoredges(self, edges):
        # Create the powerlaw-clustered network
        G = nx.barabasi_albert_graph(self.nodes,edges)
        return G

def plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(xplotList,algorithm_1, label="Random")
    plt.plot(xplotList,algorithm_2, label="Greedy")
    plt.plot(xplotList,algorithm_3, label="Greedy Probability")
    plt.plot(xplotList,algorithm_4, label="RCL DC")
    plt.plot(xplotList,algorithm_5, label="RCL BC")
    plt.plot(xplotList,algorithm_6, label="RCL CC")
    plt.plot(xplotList,algorithm_7, label="RCL EC")
    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities of selection', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph):
    num_nodes = len(graph.nodes)
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


    elif algoIndex == 4:
        for i in range (0,100):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        for i in range (0,100):
            selectedSet = RCL_Betweenness.rclBetweenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 6:
        for i in range (0,100):
            selectedSet = RCL_ClosenessCentral.rclCloseCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 7:
        for i in range (0,100):
            selectedSet = RCL_eigenvector.rclEigenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graph:
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
                itr = itr + 1
    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize)
   
def variationOfJurySize(graph_param_list,xplotList, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    
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
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize)

def variationOfedges(graph_param_list,xplotList,jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    
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
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize)

graph_param_list_Networks = [
        graphObject(100,2),
        graphObject(250,2),
        graphObject(500, 2),
        graphObject(750,2)
        ]
   
graph_param_list = [
        graphObject(500,2)
        ]
        
#############
# VARYING VALUES OF Network
#############
xplotName = "Network size"
xplotList = [100,500,1000,1200]
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

