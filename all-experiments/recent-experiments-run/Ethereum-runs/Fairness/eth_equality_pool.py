import sys
sys.path.append('../../../')
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

from metrics.Fairness import equality_of_selection


def plotGraph(algorithm_1,algorithm_3,fileName,xplotName,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Coverage")
    # plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.plot(xplot,algorithm_3, linestyle='--', label="Random selection")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Standard Deviation of Probabilities', fontsize=10)
    plt.title('Standard Deviation of Probabilities of selection for varying {}'.format(xplotName))
    plt.xticks(xplot)
    plt.legend()
    plt.savefig(fileName)

    with open('ETH_POOL_equality_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_1))

    with open('ETH_Random_equality_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_3))

def variationRunAlgo(algoIndex, jurySize, graph):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    # occurrences = [0] * num_nodes
    # probability = [0] * num_nodes
    occurrences = np.zeros(num_nodes)
    probability = np.zeros(num_nodes)

    iterations = 50
    fullDictionary = {}
    occupiedNodes = set()
    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage_large_tb.rclCoverageSelectionWithSubset_large_tb(graph, jurySize,occupiedNodes,0.25)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)            

    elif algoIndex == 2:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            # selectedSet,occupiedNodes = greedy_coverage_large_tb.greedyCoverageSelection(graph, jurySize,occupiedNodes)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    elif algoIndex == 3:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = random_select.randomSelection(graph, jurySize,occupiedNodes)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)

    return  np.std(occurrences),np.mean(probability)

def variationOfJurySize(xplot, graph, fileName,xplotName):

    algorithm_1 = [0]*len(xplot)
    # algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    numNodes = G.numberOfNodes()

    mean1 = [0]*len(xplot)
    # mean2 = [0]*len(xplot)
    mean3 = [0]*len(xplot)

    itr = 0
    for jurySize in xplot:
                size = int(jurySize*numNodes)
                print("jurySize : ",size, " jury % - ",jurySize)
                algorithm_1[itr],mean1[itr]= variationRunAlgo(1,size,graph)
                # algorithm_2[itr],mean2[itr]= variationRunAlgo(2,size,graph)
                algorithm_3[itr],mean3[itr]= variationRunAlgo(3,size,graph)
                itr = itr + 1
    plotGraph(algorithm_1,algorithm_3,fileName,xplotName,xplot)

xplot = [0.000003,0.0000075]       
print("Loading....")
graphETH = pickle.load(open("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/ETH/eth_graphobj.pickle", 'rb'))
G = nk.nxadapter.nx2nk(graphETH, weightAttr=None)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())
variationOfJurySize(xplot,G,"screenshots_equality/pool_equality_jury.jpg","Varying jury Size")