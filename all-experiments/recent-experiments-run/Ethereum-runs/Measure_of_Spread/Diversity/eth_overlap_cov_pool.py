import sys
sys.path.append('../../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(2)
from algorithm_repository_memory import greedy_Betweenness
from algorithm_repository_memory import greedy_coverage
from algorithm_repository_memory import Prob_Betweenness
from algorithm_repository_memory import Prob_Coverage
from algorithm_repository_memory import random_select
from algorithm_repository_memory import RCL_Betweenness
from algorithm_repository_memory import RCL_coverage
from algorithm_repository_memory import Seed_Betweenness
from algorithm_repository_memory import Seed_Coverage
from algorithm_repository_memory import RCL_coverage_large_tb
from algorithm_repository_memory import greedy_coverage_large_tb

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

def plotGraph(algorithm_1,algorithm_3,fileName,xplotName,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Coverage")
    # plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.plot(xplot,algorithm_3, linestyle='--', label="Random selection")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Ratio of Uniquely covered nodes to total nodes ', fontsize=10)
    plt.title('Ratio of Uniquely covered nodes to total nodes for {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)


    with open('ETH_POOL_overlap_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_1))

    with open('ETH_Random_overlap_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_3))

def variationRunAlgo(algoIndex, jurySize, graph):

    iterations = 50
    fullDictionary = {}
    occupiedNodes = set()
    # uniqueElementList = [0]*iterations
    uniqueElementList = np.zeros(iterations)
    itr = 0

    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage_large_tb.rclCoverageSelectionWithSubset_large_tb(graph, jurySize,occupiedNodes,0.25)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 2:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            # selectedSet,occupiedNodes= greedy_coverage_large_tb.greedyCoverageSelection(graph, jurySize,occupiedNodes)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 3:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes= random_select.randomSelection(graph, jurySize,occupiedNodes)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
                
    return  np.mean(uniqueElementList)

def variationOfJurySize(graph, fileName,xplotName,xplot):

    algorithm_1 = [0]*len(xplot)
    # algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    numNodes = G.numberOfNodes()
    itr = 0
    for jurySize in xplot:
                size = int(jurySize*numNodes)
                print("jurySize : ",size, " jury % - ",jurySize)
                algorithm_1[itr] = variationRunAlgo(1,size,graph)
                # algorithm_2[itr] = variationRunAlgo(2,size,graph)
                algorithm_3[itr] = variationRunAlgo(3,size,graph)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_3,fileName,xplotName,xplot)


xplot = [0.000003,0.0000075]     
xplotName = "Jury size" 
print("Loading....")
graphETH = pickle.load(open("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/ETH/eth_graphobj.pickle", 'rb'))
G = nk.nxadapter.nx2nk(graphETH, weightAttr=None)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())
variationOfJurySize(G,"screenshot_overlapping_cov/overlapping_cov_pool_jury.jpg",xplotName,xplot)
