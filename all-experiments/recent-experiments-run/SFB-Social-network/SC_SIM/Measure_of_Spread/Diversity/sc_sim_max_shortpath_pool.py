import sys
sys.path.append('../../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(2)
from algorithm_repository_memory.fb import greedy_Betweenness
from algorithm_repository_memory.fb import greedy_coverage
from algorithm_repository_memory.fb import Prob_Betweenness
from algorithm_repository_memory.fb import Prob_Coverage
from algorithm_repository_memory.fb import random_select
from algorithm_repository_memory.fb import RCL_Betweenness
from algorithm_repository_memory.fb import RCL_coverage
from algorithm_repository_memory.fb import Seed_Betweenness
from algorithm_repository_memory.fb import Seed_Coverage
from metrics.Measure_of_Spread.Diversity import maximum_shortest_path
from algorithm_repository_memory.fb import greedy_coverage_large_tb

def plotGraph(algorithm_1,algorithm_3,algorithm_4,fileName,xplotName,xplot):


    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Coverage")
    # plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.plot(xplot,algorithm_3, linestyle='--', label="Random selection")
    plt.plot(xplot,algorithm_4, linestyle='--', label="Random selection w/o window")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Avg distance b/w juror to juror ', fontsize=10)
    plt.title('Avg distance b/w juror to juror for varying {}'.format(xplotName))
    
    plt.legend()
    plt.savefig(fileName)


    with open('FB_POOL_max_short_path_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_1))

    with open('FB_Random_max_short_path_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_3))

    with open('FB_W_0_Random_max_short_path_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_4))

def variationRunAlgo(algoIndex, jurySize, graph):

    iterations = 2000
    fullDictionary = {}
    occupiedNodes = set()
    # avgDistList = [0]*iterations
    avgDistList = np.zeros(iterations)
    itr = 0
    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            print("# 1 - > Iteration : ",i)
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes,0.25)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
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
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
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
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 4:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            occupiedNodes = set()
            selectedSet,occupiedNodes= random_select.randomSelection(graph, jurySize,occupiedNodes)
            avgDistList[itr]  = maximum_shortest_path.maximumShortestPath(graph, selectedSet)
            itr = itr + 1

    return  np.mean(avgDistList)

def variationOfJurySize(graph, fileName,xplotName,xplot):

    algorithm_1 = [0]*len(xplot)
    # algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    algorithm_4 = [0]*len(xplot)
    numNodes = G.numberOfNodes()
    itr = 0
    plotNames = []
    for jurySize in xplot:
                size = int(jurySize*numNodes)
                plotNames.append(size)
                print("jurySize : ",size, " jury % - ",jurySize)
                algorithm_1[itr] = variationRunAlgo(1,size,graph)
                # algorithm_2[itr] = variationRunAlgo(2,size,graph)
                algorithm_3[itr] = variationRunAlgo(3,size,graph)
                algorithm_4[itr] = variationRunAlgo(4,size,graph)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_3,algorithm_4,fileName,xplotName,plotNames)


xplot = [0.0015,0.003,0.005,0.0065]      
xplotName = "Jury size" 
print("Loading....")
G = nk.readGraph("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/SFB/facebook_combined.txt",nk.Format.SNAP)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())

variationOfJurySize(G,"screenshots_max_short_path/max_short_pool_jury.jpg",xplotName,xplot)


