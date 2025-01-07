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

from metrics.Measure_of_Spread.Diversity import maximum_shortest_path

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
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Betweenness")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Avg distance b/w juror to juror ', fontsize=10)
    plt.title('Avg distance b/w juror to juror for varying {}'.format(xplotName))
    
    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph,size):
    iterations = 500
    avgDistList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,size)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,size)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    return  np.mean(avgDistList)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName,xplot):

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
        
xplot = [0.05,0.1,0.25,0.5,0.75,0.95]   
xplotName = "Varying Pool size"
variationOfSeedSize(graph_param_list,6,"screenshots_max_short_path/ER_max_short_pool.jpg",xplotName,xplot)
