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
    plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
    plt.title('Fractional Node Coverage of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph, poolsize, radius=0.5):
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
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,occupiedNodes,poolsize)
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
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes,poolsize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
                
    return  np.mean(fractNodeCovList)

def variationOfPoolSize(xplot,graph_param_list, jurySize, fileName,xplotName):

    fractNodeCovList_01 = [0]*len(xplot)
    fractNodeCovList_02 = [0]*len(xplot)

    itr = 0
    for obj in graph_param_list:
        for size in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                fractNodeCovList_01[itr] = variationRunAlgo(1,jurySize,graph,size,2)
                fractNodeCovList_02[itr] = variationRunAlgo(2,jurySize,graph,size,2)
                itr = itr + 1

    plotGraph(fractNodeCovList_01,fractNodeCovList_02,fileName,xplotName,jurySize,xplot)
   
graph_param_list = [
        graphObject(500)
        ]
        
xplot = [0.1,0.25,0.5,0.75,0.95]         
xplotName = "Varying Pool size"
jurySize = int(1000*0.05)
print("Running for jurySize :",jurySize)
variationOfPoolSize(xplot,graph_param_list,jurySize,"screenshots_fractional_cov/LFR_fractional_cov_pool_size.jpg",xplotName)
