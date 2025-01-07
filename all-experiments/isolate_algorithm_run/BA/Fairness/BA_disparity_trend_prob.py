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
from metrics.Measure_of_Spread.Diversity import overlapping_coverage


#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250, edges = 2):
        self.nodes = nodes
        self.edges = edges 

    def getParams (self):
        print("Nodes : ", self.nodes, " edges : ",self.edges)

    def graphGenerator(self):
        # Create the powerlaw-clustered network
        # G = nx.barabasi_albert_graph(self.nodes,self.edges)
        G = nk.generators.BarabasiAlbertGenerator(self.edges,self.nodes).generate()
        return G

    def graphGeneratoredges(self, edges):
        # Create the powerlaw-clustered network
        #G = nx.barabasi_albert_graph(self.nodes,edges)
        G = nk.generators.BarabasiAlbertGenerator(edges,self.nodes).generate()
        return G

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Betweenness centrality")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")

    plt.gca().invert_xaxis()
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Disparity in Probabilities of selection', fontsize=10)
    plt.title('Disparity in Probabilities of selection for  {}'.format(xplotName))

    plt.legend()
    #plt.show()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph,prob):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 0
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize, prob)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Prob_Coverage.coverageSelectionWithProb(graph, jurySize, prob)
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
    return  disparity


def variationOfNetworkParams(xplot,graph_param_list, jurySize, fileName,xplotName):

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
        graphObject(500,2)
        ]
        
xplot = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]    
xplotName="Increasing randomness probabilities"
variationOfNetworkParams(xplot,graph_param_list,6,"screenshots_disparity/disparity_prob_trend.jpg",xplotName)
