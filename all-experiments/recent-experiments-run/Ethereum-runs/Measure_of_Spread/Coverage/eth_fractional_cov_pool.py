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

from metrics.Measure_of_Spread.Coverage import fractional_coverage


def plotGraph(algorithm_1,algorithm_3,fileName,xplotName,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Candidate Pool-Coverage")
    # plt.plot(xplot,algorithm_2, linestyle='--', label="Greedy Coverage")
    plt.plot(xplot,algorithm_3, linestyle='--', label="Random selection")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage with radius = 2', fontsize=10)
    plt.title('Fractional Node Coverage of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)


    with open('ETH_POOL_frac_cover_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_1))

    with open('ETH_Random_frac_cover_ba_memenhanced.txt', 'a') as file:
        file.write(str("\n"))
        file.write(str(algorithm_3))
        
def variationRunAlgo(algoIndex, jurySize, graph, radius=0.5):

    iterations = 50
    fullDictionary = {}
    occupiedNodes = set()
    # fractNodeCovList = [0]*iterations
    fractNodeCovList = np.zeros(iterations)
    itr = 0
    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            print("# 1 - > Iteration : ",i)
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes= RCL_coverage_large_tb.rclCoverageSelectionWithSubset_large_tb(graph, jurySize,occupiedNodes,0.25)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverageLARGETB(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
        print("Done Index : ",algoIndex)

    elif algoIndex == 2:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            # selectedSet,occupiedNodes= greedy_coverage_large_tb.greedyCoverageSelection(graph, jurySize,occupiedNodes)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverageLARGETB(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
        print("Done Index : ",algoIndex)

    elif algoIndex == 3:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            print("# 3 - > Iteration : ",i)
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes= random_select.randomSelection(graph, jurySize,occupiedNodes)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverageLARGETB(graph, selectedSet, radius)
            itr = itr + 1
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
        print("Done Index : ",algoIndex)

    print("done all ")
    return  np.mean(fractNodeCovList)

def variationOfJurySize(xplot,graph,fileName,xplotName):

    fractNodeCovList_01 = [0]*len(xplot)
    # fractNodeCovList_02 = [0]*len(xplot)
    fractNodeCovList_03 = [0]*len(xplot)
    numNodes = G.numberOfNodes()

    itr = 0
    for jurySize in xplot:
                size = int(jurySize*numNodes)
                print("jurySize : ",size, " jury % - ",jurySize)
                fractNodeCovList_01[itr] = variationRunAlgo(1,size,graph,2)
                # fractNodeCovList_02[itr] = variationRunAlgo(2,size,graph,2)
                fractNodeCovList_03[itr] = variationRunAlgo(3,size,graph,2)
                itr = itr + 1

    plotGraph(fractNodeCovList_01,fractNodeCovList_03,fileName,xplotName,xplot)
   

xplot = [0.000003,0.0000075]    
xplotName = "Jury size" 
print("Loading....")
graphETH = pickle.load(open("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/ETH/eth_graphobj.pickle", 'rb'))
G = nk.nxadapter.nx2nk(graphETH, weightAttr=None)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())
variationOfJurySize(xplot,G,"screenshots_fractional_cov/fractional_cov_pool_jury.jpg",xplotName)

