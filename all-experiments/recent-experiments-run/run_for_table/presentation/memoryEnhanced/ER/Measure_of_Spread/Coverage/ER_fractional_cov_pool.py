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

from metrics.Measure_of_Spread.Coverage import fractional_coverage

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

# def plotGraph(algorithm_1,algorithm_2,fileName,xplotName,jurySize,xplot):

#     plt.clf()
#     plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")

#     plt.xlabel(xplotName, fontsize=10)
#     plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
#     plt.title('Fractional Node Coverage of selection for varying {}'.format(xplotName))

#     plt.legend()
#     plt.savefig(fileName)
    
#     with open('frac_cover_ba_memEnhanced.txt', 'a') as file:
#         file.write(str("\n"))
#         file.write(str(algorithm_2))


def variationRunAlgo(algoIndex, graph,betweenness_values, radius=0.5):

    iterations = 2000
    fullDictionary = {}
    occupiedNodes = set()
    fractNodeCovList = [0]*iterations
    itr = 0

    if algoIndex == 1:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubsetBetween(graph, 25,occupiedNodes,betweenness_values, 0.25)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 2:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, 25,occupiedNodes, 0.25)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 3:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProbBetween(graph, 25,occupiedNodes,betweenness_values, 0.3)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)  

    elif algoIndex == 4:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, 25,occupiedNodes, 0.3)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 5:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSizeBetween(graph, 25,occupiedNodes,betweenness_values, 10)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 6:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Coverage.seedCoverSelectionWithSize(graph, 25,occupiedNodes, 10)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)   

    return  np.mean(fractNodeCovList)

def variationOfPoolSize(xplot,graph_param_list, jurySize, fileName):

    fractNodeCovList_01 = [0]*len(xplot)
    fractNodeCovList_02 = [0]*len(xplot)
    fractNodeCovList_03 = [0]*len(xplot)
    fractNodeCovList_04 = [0]*len(xplot)
    fractNodeCovList_05 = [0]*len(xplot)
    fractNodeCovList_06 = [0]*len(xplot)

    itr = 0
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []
    list_5 = []
    list_6 = []
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

                    fractNodeCovList_01[itr] = variationRunAlgo(1,graph,betweenness_values,2)
                    fractNodeCovList_02[itr] = variationRunAlgo(2,graph,betweenness_values,2)
                    fractNodeCovList_03[itr] = variationRunAlgo(3,graph,betweenness_values,2)
                    fractNodeCovList_04[itr] = variationRunAlgo(4,graph,betweenness_values,2)
                    fractNodeCovList_05[itr] = variationRunAlgo(5,graph,betweenness_values,2)
                    fractNodeCovList_06[itr] = variationRunAlgo(6,graph,betweenness_values,2)
                    
                    list_1.append(fractNodeCovList_01[itr])
                    list_2.append(fractNodeCovList_02[itr])
                    list_3.append(fractNodeCovList_03[itr])
                    list_4.append(fractNodeCovList_04[itr])
                    list_5.append(fractNodeCovList_05[itr])
                    list_6.append(fractNodeCovList_06[itr])
        
                    itr = itr + 1

    with open("ER_frac_cover_algo_complete.txt", 'a') as file:
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
    # plotGraph(fractNodeCovList_01,fractNodeCovList_02,fileName,xplotName,jurySize,xplot)
graph_param_list = [
        graphObject(15000,0.2)
        ]
jurySize = 25       
print("Running for jurySize :",jurySize)
xplot = ["Pool Btw","Pool Cov","Prob Btw","Prob Cov","Seed Btw","Seed Cov"]  
start_time = time.time()

process = psutil.Process()
variationOfPoolSize(xplot,graph_param_list,jurySize,"screenshots_fractional_cov/fractional_cov_network_size.jpg")


end_time = time.time()
elapsed_time_ms = (end_time - start_time)

print("Program took", elapsed_time_ms, "seconds to run")
cpu_percent = process.cpu_percent(interval=1)  # CPU usage over a 1-second interval
memory_info = process.memory_info()

# Print the statistics
print(f"CPU Usage: {cpu_percent}%")
print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")