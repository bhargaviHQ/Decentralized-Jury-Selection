import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(32)
from algorithm_repository_networkit import Seed_Betweenness
from algorithm_repository_networkit import Seed_Coverage
from algorithm_repository_networkit import random_select

from metrics.Fairness import equality_of_selection

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250):
        self.nodes = nodes

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        lfr = nk.generators.LFRGenerator(self.nodes)
        lfr.generatePowerlawDegreeSequence(20, 50, -3)
        lfr.generatePowerlawCommunitySizeSequence(10, 50, -1.5)
        lfr.setMu(0.3)
        lfrG = lfr.generate()
        return lfrG

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(range(1,jurySize),algorithm_1, linestyle='--', label="Seed Betweenness")
    plt.plot(range(1,jurySize),algorithm_2, linestyle='--', label="Seed Coverage")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)


def variationRunAlgo(algoIndex, jurySize, graph,seedsize):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Seed_Betweenness.seedBetweenSelectionWithSize(graph, jurySize,seedsize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Seed_Coverage.seedCoverSelectionWithSize(graph, jurySize,seedsize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    return  np.std(occurrences),np.mean(probability)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*(jurySize-1)
    algorithm_2 = [0]*(jurySize-1)

    mean1 = [0]*(jurySize)
    mean2 = [0]*(jurySize)

    itr = 0
    for obj in graph_param_list:
        for size in range(1,jurySize):
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr],mean1[itr] = variationRunAlgo(1,jurySize,graph,size)
                algorithm_2[itr],mean2[itr]= variationRunAlgo(2,jurySize,graph,size)
                itr = itr + 1

    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)
graph_param_list = [
        graphObject(500)
        ]

xplotName = "Varying Seed size"
variationOfSeedSize(graph_param_list,6,"screenshots_equality/LFR_Seed_equality.jpg",xplotName)