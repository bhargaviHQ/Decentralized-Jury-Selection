import sys
sys.path.append('../../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(32)
from algorithm_repository_memory import greedy_Betweenness
from algorithm_repository_memory import greedy_coverage
from algorithm_repository_memory import Prob_Betweenness
from algorithm_repository_memory import Prob_Coverage
from algorithm_repository_memory import random_select
from algorithm_repository_memory import RCL_Betweenness
from algorithm_repository_memory import RCL_coverage
from algorithm_repository_memory import Seed_Betweenness
from algorithm_repository_memory import Seed_Coverage

from metrics.Measure_of_Spread.Diversity import overlapping_coverage

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
    plt.ylabel('Unique Coverage of juror ', fontsize=10)
    plt.title('Unique Coverage of juror for {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph,seedSize):
    iterations = 100
    fullDictionary = {}
    occupiedNodes = set()
    uniqueElementList = [0]*iterations
    itr = 0

    if algoIndex == 1:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSize(graph, jurySize,occupiedNodes,seedSize)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 2:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Coverage.seedCoverSelectionWithSize(graph, jurySize,occupiedNodes,seedSize)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
                
    return  np.mean(uniqueElementList)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName):


    algorithm_1 = [0]*(jurySize-1)
    algorithm_2 = [0]*(jurySize-1)
    itr = 0
    for obj in graph_param_list:
        for seedSize in range(1,jurySize):
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,seedSize)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,seedSize)

                itr = itr + 1
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)

graph_param_list = [
        graphObject(1000,0.2)
        ]
         
xplotName = "Varying Seed size"
jurySize = int(1000*0.05)
print("Running for jurySize :",jurySize)
variationOfSeedSize(graph_param_list,jurySize,"screenshot_overlapping_cov/ER_overlapping_cov_seed.jpg",xplotName)
