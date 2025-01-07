import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

from algorithm_repository_real_nets import random_select
from algorithm_repository_real_nets import greedy
from algorithm_repository_real_nets import greedy_probability
from algorithm_repository_real_nets import RCL_DegreeCentrality
from algorithm_repository_real_nets import RCL_Betweenness
from algorithm_repository_real_nets import RCL_ClosenessCentral
from algorithm_repository_real_nets import RCL_greedy

from metrics.Fairness import equality_of_selection
from metrics.Measure_of_Spread.Diversity import overlapping_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

def plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(xplotList,algorithm_1, label="Random")
    plt.plot(xplotList,algorithm_2, label="Greedy")
    plt.plot(xplotList,algorithm_3, label="Greedy Probability")
    plt.plot(xplotList,algorithm_4, label="RCL BC")
    # plt.plot(xplotList,algorithm_5, label="RCL DC")
    # plt.plot(xplotList,algorithm_6, label="RCL CC")
    # plt.plot(xplotList,algorithm_7, label="RCL Greedy")
    
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
            selectedSet = RCL_Betweenness.rclBetweenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        for i in range (0,iterations):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 6:
        for i in range (0,iterations):
            selectedSet = RCL_ClosenessCentral.rclCloseCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 7:
        for i in range (0,iterations):
            selectedSet = RCL_greedy.rclGreedySelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graph:
        probability[int(nodex)] =  occurrences[int(nodex)] / sum(occurrences)

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

def variationOfJurySize(graph,xplotList, fileName,xplotName):

    algorithm_1 = [0]*len(xplotList)
    algorithm_2 = [0]*len(xplotList)
    algorithm_3 = [0]*len(xplotList)
    algorithm_4 = [0]*len(xplotList)
    algorithm_5 = [0]*len(xplotList)
    algorithm_6 = [0]*len(xplotList)
    algorithm_7 = [0]*len(xplotList)
    
    itr = 0
    for jurySize in xplotList:
                print("Running jury size -",jurySize)
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph)
                algorithm_3[itr] = variationRunAlgo(3,jurySize,graph)
                algorithm_4[itr] = variationRunAlgo(4,jurySize,graph)
                # algorithm_5[itr] = variationRunAlgo(5,jurySize,graph)
                # algorithm_6[itr] = variationRunAlgo(6,jurySize,graph)
                # algorithm_7[itr] = variationRunAlgo(7,jurySize,graph)
                itr = itr + 1

    plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,algorithm_5,algorithm_6,algorithm_7,fileName,xplotName,jurySize)

#############
# VARYING VALUES OF jury size
#############

xplotName = "Jury size"
xplotList =  [4,7,10,12,15,20]

file = "/Users/bhargavi/Documents/research work/research_code/August 2023/visualization_other_graphs/facebook_combined.txt"

G = nx.read_edgelist(file, delimiter=' ', create_using=nx.Graph())

variationOfJurySize(G,xplotList,"fb_disparity_001.jpg",xplotName)
