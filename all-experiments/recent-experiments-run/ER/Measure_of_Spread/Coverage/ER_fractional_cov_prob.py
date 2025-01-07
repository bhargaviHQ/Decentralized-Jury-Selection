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
    def __init__(self, nodes = 250,probability = 0.01):
        self.nodes = nodes
        self.probability = probability

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        erg = nk.generators.ErdosRenyiGenerator(self.nodes, self.probability)
        ergG = erg.generate()
        return ergG

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Betweenness centrality")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.gca().invert_xaxis()
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
    plt.title('Fractional Node Coverage for {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph, prob, radius=0.5):
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
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize,occupiedNodes, prob)
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
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, jurySize,occupiedNodes, prob)
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
        for prob in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                fractNodeCovList_01[itr] = variationRunAlgo(1,jurySize,graph,prob,2)
                fractNodeCovList_02[itr] = variationRunAlgo(2,jurySize,graph,prob,2)
                itr = itr + 1

    plotGraph(fractNodeCovList_01,fractNodeCovList_02,fileName,xplotName,jurySize,xplot)
   
graph_param_list = [
        graphObject(1000,0.2)
        ]
        
xplot = [0.1,0.3,0.5,0.7,0.9]      
xplotName="Increasing randomness probabilities" 
jurySize = int(1000*0.05)
print("Running for jurySize :",jurySize)
variationOfPoolSize(xplot,graph_param_list,jurySize,"screenshots_fractional_cov/ER_fractional_cov_prob.jpg",xplotName)
