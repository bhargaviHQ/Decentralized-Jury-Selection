import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns
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

    
def variationRunAlgo(algoIndex, jurySize, graph, prob):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 0
    element_counts = np.zeros(num_nodes)

    iterations = 100
    fullDictionary = {}
    occupiedNodes = set()
    if algoIndex == 1:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProb(graph, jurySize,occupiedNodes, prob)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    if algoIndex == 2:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, jurySize,occupiedNodes, prob)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)

    probabilityAverage = sum(probability)/len(probability)
    
    probability.sort(reverse=True)
    percentileBefore =  np.percentile(probability, delta)
    percentileAfter = np.percentile(probability, (100 - delta))

    setRemove = set()
    for item in probability:
        if item > percentileAfter or item < percentileBefore:
            setRemove.add(item)
    for setItem in setRemove:
        probability.remove(setItem)
    return  probability


def variationOfSeedSize(xplot,graph_param_list, jurySize, fileName):

    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    itr = 0
    list_names = [f"p={i}" for i in xplot]
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    for obj in graph_param_list:
        for prob in xplot:
                print("Pool size : ",prob)
                graph = obj.graphGenerator()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,prob)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,prob)
                df1[list_names[itr]] = algorithm_1[itr] 
                df2[list_names[itr]] = algorithm_2[itr] 
                itr = itr + 1


    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df1, palette=custom_palette, cut=0)
    plt.xlabel("Decreasing randomness probabilities")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Betweenness Centrality Strategy for varying probabilities")
    plt.savefig(fileName+"_between.jpg")

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df2, palette=custom_palette, cut=0)
    plt.xlabel("Decreasing randomness probabilities")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Coverage Strategy for varying probabilities")

    plt.savefig(fileName+"_coverage.jpg")   
    

graph_param_list = [
        graphObject(10000,3)
        ]
xplot = [0.1,0.3,0.5,0.7,0.9]      
jurySize = int(10000*0.05)
print("Running for jurySize :",jurySize)    
variationOfSeedSize(xplot,graph_param_list,jurySize,"screenshots_disparity/disparity_prob")