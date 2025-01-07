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
    def __init__(self, nodes = 250,probability = 0.2):
        self.nodes = nodes
        self.probability = probability

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        erg = nk.generators.ErdosRenyiGenerator(self.nodes, self.probability)
        ergG = erg.generate()
        return ergG

    
def variationRunAlgo(algoIndex, jurySize, graph, poolPer):
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
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,occupiedNodes,poolPer)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    if algoIndex == 2:
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize, occupiedNodes,poolPer)
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
    list_names = [f"poolSize={i}" for i in xplot]
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    for obj in graph_param_list:
        for poolPer in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                print("Pool size : ",poolPer)
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,poolPer)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,poolPer)
                df1[list_names[itr]] = algorithm_1[itr] 
                df2[list_names[itr]] = algorithm_2[itr] 
                itr = itr + 1


    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df1, palette=custom_palette, cut=0)
    plt.xlabel("Varying Pool Size")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Betweenness Centrality Strategy for varying Pool size")
    plt.savefig(fileName+"_between.jpg")

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df2, palette=custom_palette, cut=0)
    plt.xlabel("Varying Pool size")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Coverage Strategy for varying Pool size")

    plt.savefig(fileName+"_coverage.jpg")   
    

graph_param_list = [
        graphObject(1000,0.2)
        ]
xplot = [0.1,0.25,0.5,0.75,0.95]   
jurySize = int(10000*0.05)
print("Running for jurySize :",jurySize)    
variationOfSeedSize(xplot,graph_param_list,jurySize,"screenshots_disparity/ER_disparity_poolsize")