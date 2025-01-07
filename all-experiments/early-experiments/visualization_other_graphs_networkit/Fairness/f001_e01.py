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
            selectedSet = RCL_Betweenness.rclBetweenCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        for i in range (0,100):
            selectedSet = RCL_DegreeCentrality.rclDegreeCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 6:
        for i in range (0,100):
            selectedSet = RCL_ClosenessCentral.rclCloseCSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 7:
        for i in range (0,100):
            selectedSet = RCL_greedy.rclGreedySelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graph:
        probability[int(nodex)] =  occurrences[int(nodex)] / sum(occurrences)
    probabilityAverage = sum(probability)/len(probability)
    return  np.std(probability)

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
# variationOfJurySize(G,xplotList,"fb_equality_001.jpg",xplotName)


graph2 = nx.barabasi_albert_graph(4000,4)

degree_sequence2 = sorted([d for n, d in graph2.degree()], reverse=True) # used for degree distribution and powerlaw test

degree_sequence = sorted([d for n, d in G.degree()], reverse=True) # used for degree distribution and powerlaw test
plt.hist(degree_sequence2, bins=np.logspace(0, np.log10(max(degree_sequence2)), 50), density=True)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Degree")
plt.ylabel("Probability")
plt.title("Degree Distribution")
plt.show()

import powerlaw

# Create a PowerLaw object and fit the data
fit = powerlaw.Fit(degree_sequence2)

# Get the estimated scaling exponent (power-law coefficient)
alpha = fit.alpha

print(f"Power-Law Coefficient (Scaling Exponent): {alpha}")