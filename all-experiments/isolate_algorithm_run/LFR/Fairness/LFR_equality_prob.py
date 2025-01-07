import sys
sys.path.append('../../../')
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
        
def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Betweenness centrality")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.gca().invert_xaxis()
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities', fontsize=10)
    plt.title('Standard Deviation of selection for {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)


def variationRunAlgo(algoIndex, jurySize, graph,prob):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize, prob)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Prob_Coverage.coverageSelectionWithProb(graph, jurySize, prob)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    return  np.std(occurrences),np.mean(probability)

def variationOfPoolSize(xplot, graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)

    mean1 = [0]*len(xplot)
    mean2 = [0]*len(xplot)

    itr = 0
    for obj in graph_param_list:
        for prob in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr],mean1[itr] = variationRunAlgo(1,jurySize,graph,prob)
                algorithm_2[itr],mean2[itr]= variationRunAlgo(2,jurySize,graph,prob)
                itr = itr + 1

    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)

graph_param_list = [
        graphObject(500)
        ]
        
xplot = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]    
xplotName="Increasing randomness probabilities"  
variationOfPoolSize(xplot,graph_param_list,6,"screenshots_equality/LFR_prob_equality.jpg",xplotName)
