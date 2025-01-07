import sys
sys.path.append('../../../')
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
    plt.plot(range(1,jurySize),algorithm_1, linestyle='--', label="Seed Betweenness")
    plt.plot(range(1,jurySize),algorithm_2, linestyle='--', label="Seed Coverage")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)


def variationRunAlgo(algoIndex, jurySize, graph,seedsize):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = Seed_Betweenness.seedBetweenSelectionWithSize(graph, jurySize,seedsize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = Seed_Coverage.seedCoverSelectionWithSize(graph, jurySize,seedsize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    return  np.std(occurrences),np.mean(probability)

def variationOfSeedSize(graph_param_list, jurySize, fileName,xplotName):

    algorithm_1 = [0]*(jurySize-1)
    algorithm_2 = [0]*(jurySize-1)

    mean1 = [0]*(jurySize)
    mean2 = [0]*(jurySize)

    itr = 0
    for obj in graph_param_list:
        for size in range(1,jurySize):
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr],mean1[itr] = variationRunAlgo(1,jurySize,graph,size)
                algorithm_2[itr],mean2[itr]= variationRunAlgo(2,jurySize,graph,size)
                itr = itr + 1

    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize)
graph_param_list = [
        graphObject(500,1)
        ]
        

xplotName = "Seed size"
variationOfSeedSize(graph_param_list,6,"screenshots_equality/Seed_equality.jpg",xplotName)
