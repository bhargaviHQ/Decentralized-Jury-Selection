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


from metrics.Measure_of_Spread.Coverage import fractional_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes
class graphObject:
    def __init__(self, nodes = 250):
        self.nodes = nodes

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        lfr = nk.generators.LFRGenerator(10000)
        lfr.generatePowerlawDegreeSequence(50, 250, -3)
        lfr.generatePowerlawCommunitySizeSequence(100, 300, -1.5)
        lfr.setMu(0.2)
        lfrG = lfr.generate()
        return lfrG



def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(range(1,jurySize),algorithm_1, linestyle='--', label="Seed Betweenness")
    plt.plot(range(1,jurySize),algorithm_2, linestyle='--', label="Seed Coverage")

    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
    plt.title('Fractional Node Coverage of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph, seedSize, radius=0.5):
    iterations = 100
    fullDictionary = {}
    occupiedNodes = set()
    fractNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSize(graph, jurySize,occupiedNodes,seedSize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
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
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
                
    return  np.mean(fractNodeCovList)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName):


    fractNodeCovList_01 = [0]*(jurySize-1)
    fractNodeCovList_02 = [0]*(jurySize-1)

    itr = 0
    for obj in graph_param_list:
        for size in range(1,jurySize):
                graph = obj.graphGenerator()
                obj.getParams()
                fractNodeCovList_01[itr] = variationRunAlgo(1,jurySize,graph,size,2)
                fractNodeCovList_02[itr] = variationRunAlgo(2,jurySize,graph,size,2)
                itr = itr + 1

    plotGraph(fractNodeCovList_01,fractNodeCovList_02,fileName,xplotName,jurySize)
graph_param_list = [
        graphObject(500)
        ]
            
xplotName = "Varying Seed size"
jurySize = int(10000*0.05)
print("Running for jurySize :",jurySize)
variationOfSeedSize(graph_param_list,jurySize,"screenshots_fractional_cov/LFR_fractional_cov_seed.jpg",xplotName)