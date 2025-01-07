import sys
sys.path.append('../../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(32)
from algorithm_repository_networkit import greedy_Betweenness
from algorithm_repository_networkit import greedy_coverage
from algorithm_repository_networkit import Prob_Betweenness
from algorithm_repository_networkit import Prob_Coverage
from algorithm_repository_networkit import random_select
from algorithm_repository_networkit import RCL_Betweenness
from algorithm_repository_networkit import RCL_coverage
from algorithm_repository_networkit import Seed_Betweenness
from algorithm_repository_networkit import Seed_Coverage

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

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Betweenness centrality")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.gca().invert_xaxis()
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Ratio of Uniquely covered nodes to total nodes ', fontsize=10)
    plt.title('Ratio of Unique coverage for {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph,prob):
    iterations = 500
    uniqueElementList = [0]*iterations
    itr = 0

    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize, prob)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Prob_Coverage.coverageSelectionWithProb(graph, jurySize, prob)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1

    return  np.mean(uniqueElementList)

def variationOfPoolsize(graph_param_list, jurySize, fileName,xplotName,xplot):

    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    itr = 0
    for obj in graph_param_list:
        for prob in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,prob)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,prob)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)

graph_param_list = [
        graphObject(500)
        ]
        
xplot = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]    
xplotName="Increasing randomness probabilities"
variationOfPoolsize(graph_param_list,6,"screenshot_overlapping_cov/ER_overlapping_cov_prob.jpg",xplotName,xplot)
