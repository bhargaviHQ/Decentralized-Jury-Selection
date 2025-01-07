import sys
sys.path.append('../../../')
import imports
from imports import *
nk.engineering.setNumberOfThreads(32)
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
from metrics.Measure_of_Spread.Diversity import overlapping_coverage


#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250,probability = 0.01):
        self.nodes = nodes
        self.probability = probability

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        erg = nk.generators.ErdosRenyiGenerator(self.nodes, self.probability)
        ergG = erg.generate()
        return ergG

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(range(1,jurySize),algorithm_1, linestyle='--', label="Seed Betweenness")
    plt.plot(range(1,jurySize),algorithm_2, linestyle='--', label="Seed Coverage")

    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Disparity in Probabilities of selection', fontsize=10)
    plt.title('Disparity in Probabilities of selection for  {}'.format(xplotName))

    plt.legend()
    #plt.show()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph,seed):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 0
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Seed_Betweenness.seedBetweenSelectionWithSize(graph, jurySize,seed)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Seed_Coverage.seedCoverSelectionWithSize(graph, jurySize,seed)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)

    probabilityAverage = sum(probability)/len(probability)
    occurrences.sort(reverse=True)
    # percentileBefore =  np.percentile(occurrences, delta)
    # percentileAfter = np.percentile(occurrences, (100 - delta))
    # setRemove = set()
    # counter = 0
    # for item in occurrences:
    #     if item > percentileAfter or item <= percentileBefore:
    #         counter += 1
    #         setRemove.add(item)
    # for setItem in setRemove:
    #     # probability.remove(setItem)
    #     element_count = occurrences.count(setItem)
    #     for i in range(element_count):
    #             occurrences.remove(setItem)
        
    disparity = max(occurrences) - min(occurrences)
    #print(max(occurrences), " - " ,min(occurrences))
    return  disparity


def variationOfNetworkParams(graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*(jurySize-1)
    algorithm_2 = [0]*(jurySize-1)
    itr = 0
    for obj in graph_param_list:
        for size in range(1,jurySize):
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,size)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,size)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)

graph_param_list = [
        graphObject(500)
        ]

xplotName = "Varying Seed size"
variationOfNetworkParams(graph_param_list,6,"screenshots_disparity/ER_disparity_seed_trend.jpg",xplotName)