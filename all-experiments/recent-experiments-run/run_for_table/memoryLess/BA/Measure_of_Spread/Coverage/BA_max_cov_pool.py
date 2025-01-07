import sys
sys.path.append('../../../../../../')
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

from metrics.Measure_of_Spread.Coverage import maximum_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250, edges = 1):
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
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Betweenness")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")
    
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Minimum distance of selection', fontsize=10)
    plt.title('Minimum distance of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)
    with open('max_cover_ba_memless.txt', 'a') as file:
        file.write(str(algorithm_1))
        file.write(str("\n"))
        file.write(str(algorithm_2))

def variationRunAlgo(algoIndex, jurySize, graph,poolsize):
    iterations = 100
    maxNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,poolsize)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            itr = itr + 1

    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,poolsize)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            itr = itr + 1
    
    return  np.mean(maxNodeCovList)

def variationOfPoolSize(graph_param_list, jurySize, fileName,xplotName,xplot):

    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    itr = 0
    for obj in graph_param_list:
        for size in xplot:
                print("Pool size :",size)
                graph = obj.graphGenerator()
                obj.getParams()
                algorithm_1[itr] = variationRunAlgo(1,jurySize,graph,size)
                algorithm_2[itr] = variationRunAlgo(2,jurySize,graph,size)

                itr = itr + 1
    plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)
   
   
graph_param_list = [
        graphObject(10000,2)
        ]
jurySize = int(12)
print("Running for jurySize :",jurySize)
xplot = [0.1,0.25,0.5,0.75,0.95]     
xplotName = "Pool size"
variationOfPoolSize(graph_param_list,jurySize,"screenshots_max_cov/max_cov_pool_size.jpg",xplotName,xplot)
