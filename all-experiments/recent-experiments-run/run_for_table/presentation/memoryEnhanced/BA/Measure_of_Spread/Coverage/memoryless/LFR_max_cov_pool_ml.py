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

from metrics.Measure_of_Spread.Coverage import maximum_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes = 250):
        self.nodes = nodes

    def getParams (self):
        print("Nodes : ", self.nodes)

    def graphGenerator(self):
        lfr2 = nk.generators.LFRGenerator(5000)
        lfr2.generatePowerlawDegreeSequence(25, 50, -3)
        lfr2.generatePowerlawCommunitySizeSequence(25, 100, -1.5)
        lfr2.setMu(0.2)
        lfrG2 = lfr2.generate()
        return lfrG2
        
# def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

#     plt.clf()
#     plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")
    
#     plt.xlabel(xplotName, fontsize=10)
#     plt.ylabel('Minimum distance of selection', fontsize=10)
#     plt.title('Minimum distance of selection for varying {}'.format(xplotName))

#     plt.legend()
#     plt.savefig(fileName)

#     with open('max_cover_ba_memEnhanced.txt', 'a') as file:
#         file.write(str("\n"))
#         file.write(str(algorithm_2))
        
def variationRunAlgo(algoIndex, graph, betweenness_values):

    iterations = 100
    fullDictionary = {}
    occupiedNodes = set()
    maxNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubsetBetween(graph, 25,occupiedNodes,betweenness_values, 0.25)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 2:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, 25,occupiedNodes, 0.25)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 3:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProbBetween(graph, 25,occupiedNodes,betweenness_values, 0.3)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 4:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, 25,occupiedNodes, 0.3)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 5:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSizeBetween(graph, 25,occupiedNodes,betweenness_values, 10)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()

    elif algoIndex == 6:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = Seed_Coverage.seedCoverSelectionWithSize(graph, 25,occupiedNodes, 10)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()


    elif algoIndex == 7:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            selectedSet,occupiedNodes = random_select.randomSelection(graph, 25,occupiedNodes)
            maxNodeCovList[itr]  = maximum_coverage.maximumCoverageSetFinal(graph, selectedSet)
            occupiedNodes = set()


    return  np.mean(maxNodeCovList)

def variationOfPoolSize(graph_param_list, jurySize, fileName,xplotName,xplot):

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
    for q in range(3):
        for obj in graph_param_list:
                    graph = obj.graphGenerator()
                    obj.getParams()
                    ########
                    #Calculate Betweenness centrality
                    ########
                    bc = nk.centrality.Betweenness(graph, normalized=True)
                    bc.run()
                    betweenness_values = bc.scores()

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
    with open("LFR_max_cover_algo_complete_ML.txt", 'a') as file:
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

    # plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot)

graph_param_list = [
    graphObject(5000,2)
        ]
jurySize = 25       
print("Running for jurySize :",jurySize)
xplot = ["Pool Btw","Pool Cov","Prob Btw","Prob Cov","Seed Btw","Seed Cov"]  
start_time = time.time()

process = psutil.Process()
xplotName = "Network size"
variationOfPoolSize(graph_param_list,jurySize,"screenshots_max_cov/max_cov_network_size.jpg",xplotName,xplot)

end_time = time.time()
elapsed_time_ms = (end_time - start_time)

print("Program took", elapsed_time_ms, "seconds to run")
cpu_percent = process.cpu_percent(interval=1)  # CPU usage over a 1-second interval
memory_info = process.memory_info()

# Print the statistics
print(f"CPU Usage: {cpu_percent}%")
print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")