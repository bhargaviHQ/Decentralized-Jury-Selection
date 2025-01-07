import sys
sys.path.append('../../../../../../../')
import imports
from imports import *

from graph_generator import generator

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

# def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

#     plt.clf()
#     plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")

#     plt.xlabel(xplotName, fontsize=10)
#     plt.ylabel('Ratio of Uniquely covered nodes to total nodes ', fontsize=10)
#     plt.title('Ratio of Uniquely covered nodes to total nodes for {}'.format(xplotName))

#     plt.legend()
#     plt.savefig(fileName)

#     with open('overlap_ba_memEnhanced.txt', 'a') as file:
#         file.write(str("\n"))
#         file.write(str(algorithm_2))


def variationRunAlgo(algoIndex, graph, betweenness_values):

    iterations = 2000
    fullDictionary = {}
    occupiedNodes = set()
    uniqueElementList = [0]*iterations
    itr = 0

    if algoIndex == 1:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubsetBetween(graph, 25,occupiedNodes,betweenness_values, 0.25)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 2:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, 25,occupiedNodes, 0.25)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 3:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProbBetween(graph, 25,occupiedNodes,betweenness_values, 0.3)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 4:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, 25,occupiedNodes, 0.3)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 5:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSizeBetween(graph, 25,occupiedNodes,betweenness_values, 10)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 6:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Seed_Coverage.seedCoverSelectionWithSize(graph, 25,occupiedNodes, 10)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 7:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = random_select.randomSelection(graph, 25,occupiedNodes)
            uniqueElementList[itr]  = overlapping_coverage.overlapping_coverage(graph, selectedSet)
            occupiedNodes = set()

    return  np.mean(uniqueElementList)

def variationOfPoolsize(graph_param_list, jurySize, fileName,xplotName,xplot):
    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    algorithm_4 = [0]*len(xplot)
    algorithm_5 = [0]*len(xplot)
    algorithm_6 = [0]*len(xplot)
    algorithm_7 = [0]*len(xplot)

    itr = 0
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
    list_7 = []

    for obj in graph_param_list:
                    graph = obj.graphGenerator()
                    obj.getParams()
                    ########
                    #Calculate Betweenness centrality
                    ########
                    bc = nk.centrality.Betweenness(graph, normalized=True)
                    bc.run()
                    betweenness_values = bc.scores()

                    for q in range(3):
                        algorithm_1[itr]= variationRunAlgo(1,graph,betweenness_values)
                        algorithm_2[itr]= variationRunAlgo(2,graph,betweenness_values)
                        algorithm_3[itr]= variationRunAlgo(3,graph,betweenness_values)
                        algorithm_4[itr]= variationRunAlgo(4,graph,betweenness_values)
                        algorithm_5[itr]= variationRunAlgo(5,graph,betweenness_values)
                        algorithm_6[itr]= variationRunAlgo(6,graph,betweenness_values)
                        algorithm_7[itr]= variationRunAlgo(7,graph,betweenness_values)
                        

                        list_1.append(algorithm_1[itr])
                        list_2.append(algorithm_2[itr])
                        list_3.append(algorithm_3[itr])
                        list_4.append(algorithm_4[itr])
                        list_5.append(algorithm_5[itr])
                        list_6.append(algorithm_6[itr])
                        list_7.append(algorithm_7[itr])

                        itr = itr + 1
    #plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)
    with open("BA_overlap_algo_complete_random_inc_allalgo_ML.txt", 'a') as file:
                    file.write(str(statistics.mean(list_1)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_2)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_3)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_4)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_5)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_6)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_7)))
                    file.write("\n\n ***")


graph_param_list = [
    graphObject(5000,2)
        ]
jurySize = 25       
print("Running for jurySize :",jurySize)
xplot = ["Pool Btw","Pool Cov","Prob Btw"]  
start_time = time.time()
process = psutil.Process()

xplotName = "Network size"
variationOfPoolsize(graph_param_list,jurySize,"screenshot_overlapping_cov/overlapping_cov_network_random_inc.jpg",xplotName,xplot)
end_time = time.time()
elapsed_time_ms = (end_time - start_time)

print("Program took", elapsed_time_ms, "seconds to run")
cpu_percent = process.cpu_percent(interval=1)  # CPU usage over a 1-second interval
memory_info = process.memory_info()

# Print the statistics
print(f"CPU Usage: {cpu_percent}%")
print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")