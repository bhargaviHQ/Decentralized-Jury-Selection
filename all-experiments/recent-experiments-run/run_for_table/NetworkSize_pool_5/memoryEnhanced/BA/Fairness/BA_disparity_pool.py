import sys
sys.path.append('../../../../../../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns
nk.engineering.setNumberOfThreads(4)
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
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,occupiedNodes, poolPer)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    if algoIndex == 2:
        for i in range (0,iterations):

            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes, poolPer)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
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
    list_names = [f"networkSize={i}" for i in xplot]
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    for obj in graph_param_list:
                graph = obj.graphGenerator()
                obj.getParams()
                list_names = [f"networkSize={i}" for i in xplot]
                df1 = pd.DataFrame()
                df2 = pd.DataFrame()
                # algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,0.25)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,0.5)
                # df1[list_names[itr]] = algorithm_1[itr] 
                df2[list_names[itr]] = algorithm_2[itr] 
                itr = itr + 1

                custom_palette = ['gray']
                plt.figure(figsize=(12, 6))
                sns.violinplot(data=df2, palette=custom_palette, cut=0)
                plt.xlabel("Varying Network size")
                plt.ylabel("Probabilities of Occurrence")
                plt.title("Coverage Strategy for Network size")
                plt.savefig(fileName+"_coverage.jpg") 
                
                txtfile2 = fileName+'_coverage_memEnhanced.txt'  
                max_values2 = df2.max()
                minval2 = df2.min()

                CQ1 = df2.quantile(0.25)
                CQ2 = df2.quantile(0.5) 
                CQ3 = df2.quantile(0.75)

                with open(txtfile2, 'a') as file:
                    file.write(str("_coverage"))
                    file.write(str(max_values2))
                    file.write(str(minval2))
                    file.write(str(CQ1))
                    file.write(str(CQ2))
                    file.write(str(CQ3))
                    file.write("\n\n ***")


graph_param_list = [
        graphObject(2500,2),
        graphObject(5000,2),
        graphObject(7500,2),
        graphObject(10000,3),
        graphObject(15000,3),
        graphObject(20000,5),
        graphObject(50000,10)
        ]
jurySize = 25       
print("Running for jurySize :",jurySize)
xplot = [2500,5000,7500,10000,15000,20000,50000]            
variationOfSeedSize(xplot,graph_param_list,jurySize,"screenshots_disparity/disparity_network")