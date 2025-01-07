import sys
sys.path.append('../../../')
import imports
from imports import *
nk.engineering.setNumberOfThreads(32)
from graph_generator import generator

from algorithm_repository_memory import greedy_Betweenness
from algorithm_repository_memory import greedy_coverage
from algorithm_repository_memory import Prob_Betweenness
from algorithm_repository_memory import Prob_Coverage
from algorithm_repository_memory import random_select
from algorithm_repository_memory import RCL_Betweenness
from algorithm_repository_memory import RCL_coverage
from algorithm_repository_memory import Seed_Betweenness
from algorithm_repository_memory import Seed_Coverage


from metrics.Fairness import equality_of_selection
from metrics.Measure_of_Spread.Diversity import overlapping_coverage


#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250):
        self.nodes = nodes

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        lfr = nk.generators.LFRGenerator(1000)
        lfr.generatePowerlawDegreeSequence(25, 50, -3)
        lfr.generatePowerlawCommunitySizeSequence(25, 50, -1.5)
        lfr.setMu(0.2)
        lfrG = lfr.generate()
        return lfrG


def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Betweenness")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")

    
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
    iterations = 100
    fullDictionary = {}
    occupiedNodes = set()
    if algoIndex == 1:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,occupiedNodes,seed)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 2:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes,seed)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
                
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
    return  disparity


def variationOfNetworkParams(xplot,graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    itr = 0
    for obj in graph_param_list:
        for size in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,size)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,size)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)

graph_param_list = [
        graphObject(500)
        ]

xplot = [0.1,0.25,0.5,0.75,0.95]        
xplotName="Varying Pool Size"
jurySize = int(1000*0.05)
print("Running for jurySize :",jurySize)
variationOfNetworkParams(xplot,graph_param_list,jurySize,"screenshots_disparity/LFR_disparity_poolsize_trend.jpg",xplotName)
