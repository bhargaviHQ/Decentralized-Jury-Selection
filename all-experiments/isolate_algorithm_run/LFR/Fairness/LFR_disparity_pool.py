import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns
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

    
def variationRunAlgo(algoIndex, jurySize, graph, poolPer):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 0
    element_counts = np.zeros(num_nodes)

    iterations = 500
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize, poolPer)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    if algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize, poolPer)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

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
        graphObject(500)
        ]
xplot = [0.05,0.1,0.25,0.5,0.75,0.95]        
variationOfSeedSize(xplot,graph_param_list,6,"screenshots_disparity/LFR_disparity_poolsize")