import sys
sys.path.append('../../../')
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


from metrics.Measure_of_Spread.Coverage import fb_fractional_coverage
from metrics.Measure_of_Spread.Coverage import fractional_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

def plotGraph(xplotList,algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(xplotList,algorithm_1, label="Random")
    plt.plot(xplotList,algorithm_2, label="Greedy")
    plt.plot(xplotList,algorithm_3, label="Greedy Probability")
    plt.plot(xplotList,algorithm_4, label="RCL BC")
    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
    plt.title('Fractional Node Coverage of selection for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph, radius=0.2):
    iterations = 100
    fractNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            fractNodeCovList[itr]  = fb_fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = greedy.randomGreedySelection(graph, jurySize)
            fractNodeCovList[itr]  = fb_fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = greedy_probability.randomGreedyProbSelection(graph, jurySize)
            fractNodeCovList[itr]  = fb_fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1


    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenCSelection(graph, jurySize)
            fractNodeCovList[itr]  = fb_fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1


    return  np.mean(fractNodeCovList)

def variationOfJurySize(graph,xplotList, fileName,xplotName):
    
    fractNodeCovList_01 = [0]*len(xplotList)
    fractNodeCovList_02 = [0]*len(xplotList)
    fractNodeCovList_03 = [0]*len(xplotList)
    fractNodeCovList_04 = [0]*len(xplotList)
    itr = 0
    for jurySize in xplotList:
                print("Running jury size - ",jurySize)
                fractNodeCovList_01[itr] = variationRunAlgo(1,jurySize,graph,2)
                fractNodeCovList_02[itr] = variationRunAlgo(2,jurySize,graph,2)
                fractNodeCovList_03[itr] = variationRunAlgo(3,jurySize,graph,2)
                fractNodeCovList_04[itr] = variationRunAlgo(4,jurySize,graph,2)
                itr = itr + 1

    plotGraph(xplotList,fractNodeCovList_01,fractNodeCovList_02,fractNodeCovList_03,fractNodeCovList_04,fileName,xplotName,jurySize)

#############
# VARYING VALUES OF jury size
#############

xplotName = "Jury size"
xplotList =  [4,7,10,12,15,20]

file = "/Users/bhargavi/Documents/research work/research_code/August 2023/visualization_other_graphs/facebook_combined.txt"

G = nx.read_edgelist(file, delimiter=' ', create_using=nx.Graph())

variationOfJurySize(G,xplotList,"fb_frac_cov_001.jpg",xplotName)
