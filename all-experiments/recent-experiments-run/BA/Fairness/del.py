import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(32)
from algorithm_repository_networkit import Seed_Betweenness
from algorithm_repository_networkit import Seed_Coverage
from algorithm_repository_networkit import random_select

from metrics.Fairness import equality_of_selection

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

def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize):

    plt.clf()
    plt.plot(range(1,jurySize+1),algorithm_1, linestyle='--', label="Seed Betweenness")
    plt.plot(range(1,jurySize+1),algorithm_2, linestyle='--', label="Seed Coverage")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities of selection', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for {}; j = {} '.format(xplotName,jurySize))

    plt.legend()
    plt.savefig(fileName)

def plotBoxGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize):

    plt.clf()
    data_to_plot = [algorithm_1, algorithm_2]

    plt.boxplot(data_to_plot)
    plt.xticks([1, 2], ['Random', 'Seed-coverage'])
    plt.xlabel('Elements')
    plt.ylabel('Standard Deviation')
    plt.title('Standard Deviations of Five Elements')
    plt.show()


def variationRunAlgo(algoIndex, jurySize, graph):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Seed_Coverage.seedCoverSelectionWithSize(graph, jurySize,jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)
    probabilityAverage = sum(probability)/len(probability)
    return  np.std(probability)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*(jurySize)
    algorithm_2 = [0]*(jurySize)

    itr = 0
    for obj in graph_param_list:
        for size in range(1,jurySize+1):
                print("Running jury size  : ",size)
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(2,size,graph)
                algorithm_2[itr] = variationRunAlgo(2,size,graph)
                itr = itr + 1
    print(" -> ", algorithm_2)
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)
    plotBoxGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)
graph_param_list = [
        graphObject(500,2)
        ]
        

xplotName = "Seed size"
variationOfSeedSize(graph_param_list,7,"screenshots_equality/Seed_equality_closeness_network_central.jpg",xplotName)
