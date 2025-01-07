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
    def __init__(self, nodes = 1000, prob = 0.02):
        self.nodes = nodes
        self.prob = prob 

    def getParams (self):
        print("Nodes : ", self.nodes, " prob : ",self.prob)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        G = nx.erdos_renyi_graph(self.nodes,self.prob)
        return G

    def graphGeneratorProb(self, prob):
        # Create the powerlaw-clustered network
        G = nx.erdos_renyi_graph(self.nodes,prob)
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
    plt.ylabel('Disparity in Probabilities of selection', fontsize=10)
    plt.title('Disparity in Probabilities of selection for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph):
    num_nodes = len(graph.nodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 5
    iterations = 100
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

     
    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 6:
        for i in range (0,iterations):
            selectedSet = RCL_ClosenessCentral.rclCloseCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 7:
        for i in range (0,iterations):
            selectedSet = RCL_eigenvector.rclEigenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graph:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)

    probabilityAverage = sum(probability)/len(probability)
    
    probability.sort(reverse=True)
    percentileBefore =  np.percentile(probability, delta)
    percentileAfter = np.percentile(probability, (100 - delta))

    setRemove = set()
    for item in probability:
        if item > percentileAfter or item < percentileBefore:
            setRemove.add(item)
    for setItem in setRemove:
        probability.remove(setItem)
    disparity = max(probability) - min(probability)

    return  disparity


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

def variationOfProb(graph_param_list,xplotList,jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    
    for obj in graph_param_list:
        itr = 0
        for prob in xplotList:
                graph = obj.graphGeneratorProb(prob)
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
        graphObject(100,0.1),
        graphObject(500,0.1),
        graphObject(1000, 0.1),
        graphObject(1200,0.1)
        ]
   
graph_param_list = [
        graphObject(500,0.1)
        ]
        
#############
# VARYING VALUES OF Network
#############
xplotName = "Network size"
xplotList = [100,500,1000,1200]
variationOfNetworkParams(graph_param_list_Networks,xplotList,7,"screenshots_disparity/disparity_closeness_network_central.jpg",xplotName)

#############
# VARYING VALUES OF jury size
#############

xplotName = "Jury size"
xplotList =  [4,7,10,12,15]
variationOfJurySize(graph_param_list,xplotList,"screenshots_disparity/disparity_closeness_jury_central.jpg",xplotName)


#############
# VARYING VALUES OF Average Degree
#############

xplotName = "Probability range"
xplotList =  [0.001,0.005,0.01,0.05,0.1,0.2,0.3,0.4,0.8,0.9]
variationOfProb(graph_param_list,xplotList,7,"screenshots_disparity/disparity_closeness_prob_central.jpg",xplotName)