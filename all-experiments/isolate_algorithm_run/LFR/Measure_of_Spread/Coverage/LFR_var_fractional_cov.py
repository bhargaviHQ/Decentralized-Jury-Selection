import sys
sys.path.append('../../../../')
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


from metrics.Measure_of_Spread.Coverage import fractional_coverage

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

def plotGraphstd(algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize,xplot):
    
    plt.clf()

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=algorithm_1, palette=custom_palette)
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage', fontsize=10)
    plt.title('Pure Greedy(LFR): Fractional Coverage for varying {}'.format(xplotName))
    plt.savefig(fileName+"_box_pure_greedy.jpg")

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=algorithm_2, palette=custom_palette)
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage', fontsize=10)
    plt.title('Pool-Coverage(LFR): Fractional Coverage for varying {}'.format(xplotName))
    plt.savefig(fileName+"_box_pool_cov.jpg")

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=algorithm_3, palette=custom_palette)
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage', fontsize=10)
    plt.title('Pure Random(LFR): Fractional Coverage for varying {}'.format(xplotName))
    plt.savefig(fileName+"_box_pure_random.jpg")

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=algorithm_4, palette=custom_palette)
    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage', fontsize=10)
    plt.title('Pool-Betweenness(LFR): Fractional Coverage for varying {}'.format(xplotName))
    plt.savefig(fileName+"_box_pool_between.jpg")

def plotGraph(algorithm_1,algorithm_2,algorithm_3,algorithm_4,fileName,xplotName,jurySize,xplot):

    plt.clf()
    plt.plot(xplot,algorithm_1, linestyle='--', label="Pure Greedy")
    plt.plot(xplot,algorithm_2, linestyle='--', label="Candidate Pool-Coverage")
    plt.plot(xplot,algorithm_3, linestyle='--', label="Pure Random")
    plt.plot(xplot,algorithm_4, linestyle='--', label="Candidate Pool-Betweenness")

    plt.xlabel(xplotName, fontsize=10)
    plt.ylabel('Fractional Node Coverage', fontsize=10)
    plt.title('Fractional Node Coverage of selection for varying {}'.format(xplotName))

    plt.legend()
    plt.savefig(fileName)

def variationRunAlgo(algoIndex, jurySize, graph, radius=0.5):
    iterations = 500
    fractNodeCovList = [0]*iterations
    itr = 0
    if algoIndex == 1:
        for i in range (0,iterations):
            selectedSet = greedy_coverage.greedyCoverageSelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1


    elif algoIndex == 2:
        for i in range (0,iterations):
            selectedSet = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,0.5)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    elif algoIndex == 3:
        for i in range (0,iterations):
            selectedSet = random_select.randomSelection(graph, jurySize)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1

    elif algoIndex == 4:
        for i in range (0,iterations):
            selectedSet = RCL_Betweenness.rclBetweenSelectionWithSubset(graph, jurySize,0.5)
            fractNodeCovList[itr]  = fractional_coverage.fractionalCoverage(graph, selectedSet, radius)
            itr = itr + 1
    return  np.mean(fractNodeCovList),fractNodeCovList

def variationOfRadiusSize(xplot,graph_param_list, jurySize, fileName,xplotName):

    fractNodeCovList_01 = [0]*len(xplot)
    fractNodeCovList_02 = [0]*len(xplot)
    fractNodeCovList_03 = [0]*len(xplot)
    fractNodeCovList_04 = [0]*len(xplot)

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()
    list_names = [f"radius={i}" for i in xplot]

    itr = 0
    for obj in graph_param_list:
        for radius in xplot:
                graph = obj.graphGenerator()
                obj.getParams()
                fractNodeCovList_01[itr],df1[list_names[itr]] = variationRunAlgo(1,jurySize,graph,radius)
                fractNodeCovList_02[itr],df2[list_names[itr]] = variationRunAlgo(2,jurySize,graph,radius)
                fractNodeCovList_03[itr],df3[list_names[itr]] = variationRunAlgo(3,jurySize,graph,radius)
                fractNodeCovList_04[itr],df4[list_names[itr]] = variationRunAlgo(4,jurySize,graph,radius)
                itr = itr + 1

    plotGraph(fractNodeCovList_01,fractNodeCovList_02,fractNodeCovList_03,fractNodeCovList_04,fileName,xplotName,jurySize,xplot)
    plotGraphstd(df1,df2,df3,df4,fileName,xplotName,jurySize,xplot) 

graph_param_list = [
        graphObject(500)
        ]
  
xplot = [1,2,3,4,5]
xplotName = "Radius size"
variationOfRadiusSize(xplot,graph_param_list,6,"screenshots_fractional_cov/LFR_fractional_cov_radius_size",xplotName)
