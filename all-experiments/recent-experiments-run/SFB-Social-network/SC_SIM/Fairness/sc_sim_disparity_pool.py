import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns
nk.engineering.setNumberOfThreads(2)
from algorithm_repository_memory.fb  import greedy_Betweenness
from algorithm_repository_memory.fb  import greedy_coverage
from algorithm_repository_memory.fb  import Prob_Betweenness
from algorithm_repository_memory.fb  import Prob_Coverage
from algorithm_repository_memory.fb  import random_select
from algorithm_repository_memory.fb  import RCL_Betweenness
from algorithm_repository_memory.fb  import RCL_coverage
from algorithm_repository_memory.fb  import Seed_Betweenness
from algorithm_repository_memory.fb  import Seed_Coverage
from algorithm_repository_memory.fb  import greedy_coverage_large_tb

from metrics.Fairness import equality_of_selection
from metrics.Measure_of_Spread.Diversity import overlapping_coverage

def variationRunAlgo(algoIndex, jurySize, graph):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    # occurrences = [0] * num_nodes
    # probability = [0] * num_nodes
    occurrences = np.zeros(num_nodes)
    probability = np.zeros(num_nodes)
    
    delta = 0
    element_counts = np.zeros(num_nodes)

    iterations = 5000
    fullDictionary = {}
    occupiedNodes = set()

    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes, 0.25)

            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    # if algoIndex == 2:
    #     print("algoIndex : ",algoIndex)
    #     for i in range (0,iterations):
    #         timeWindow = random.randint(1,20)
    #         for key, value in fullDictionary.items():
    #             if value == i:
    #                 occupiedNodes.remove(key)
    #         selectedSet,occupiedNodes = greedy_coverage_large_tb.greedyCoverageSelection(graph, jurySize,occupiedNodes)
            
    #         for nodex in selectedSet:
    #             fullDictionary[nodex] = int(i + timeWindow)
    #         occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    elif algoIndex == 3:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = random_select.randomSelection(graph, jurySize,occupiedNodes)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    # for nodex in graphNodes:
    #     probability[nodex] =  occurrences[nodex] / sum(occurrences)


    elif algoIndex == 4:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            occupiedNodes = set()
            selectedSet,occupiedNodes = random_select.randomSelection(graph, jurySize,occupiedNodes)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)


    # probabilityAverage = sum(probability)/len(probability)
    
    # probability.sort(reverse=True)
    # percentileBefore =  np.percentile(probability, delta)
    # percentileAfter = np.percentile(probability, (100 - delta))

    # setRemove = set()
    # for item in probability:
    #     if item > percentileAfter or item < percentileBefore:
    #         setRemove.add(item)
    # for setItem in setRemove:
    #     probability.remove(setItem)
    return  probability


def variationOfJurySize(xplot,G, fileName):

    algorithm_1 = [0]*len(xplot)
    # algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    algorithm_4 = [0]*len(xplot)
    numNodes = G.numberOfNodes()
    itr = 0
    list_names = [f"jurySize={i*numNodes}" for i in xplot]
    df1 = pd.DataFrame()
    # df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    df4 = pd.DataFrame()

    print("No. of nodes : ",G.numberOfNodes(),"No. of edges : ", G.numberOfEdges())
    for jurySize in xplot:
                size = int(jurySize*numNodes)
                print("jurySize : ",size, " jury % - ",jurySize)
                algorithm_1[itr] = variationRunAlgo(1,size,G)
                # algorithm_2[itr] = variationRunAlgo(2,size,G)
                algorithm_3[itr] = variationRunAlgo(3,size,G)
                algorithm_4[itr] = variationRunAlgo(4,size,G)
                df1[list_names[itr]] = algorithm_1[itr] 
                # df2[list_names[itr]] = algorithm_2[itr] 
                df3[list_names[itr]] = algorithm_3[itr] 
                df4[list_names[itr]] = algorithm_4[itr] 
                itr = itr + 1

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df1, palette=custom_palette, cut=0)
    plt.xlabel("Varying Jury Size")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Candidate pool selection with Coverage and memory ")
    plt.savefig(fileName+"_coverage.jpg")
    
    txtfile2 = fileName+'_FB__coverage_memEnhanced.txt'  
    max_values2 = df1.max()
    minval2 = df1.min()

    CQ1 = df1.quantile(0.25)
    CQ2 = df1.quantile(0.5) 
    CQ3 = df1.quantile(0.75)

    with open(txtfile2, 'a') as file:
                    file.write(str("_coverage"))
                    file.write(str(df1.max()))
                    file.write(str(minval2))
                    file.write(str(CQ1))
                    file.write(str(CQ2))
                    file.write(str(CQ3))
                    file.write("\n\n ***")
    # custom_palette = ['gray']
    # plt.figure(figsize=(12, 6))
    # sns.violinplot(data=df2, palette=custom_palette, cut=0)
    # plt.xlabel("Varying Jury size")
    # plt.ylabel("Probabilities of Occurrence")
    # plt.title("Greedy selection with memory")
    # plt.savefig(fileName+"_greedy.jpg")   

    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df3, palette=custom_palette, cut=0)
    plt.xlabel("Varying Jury size")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Random selection with memory")
    plt.savefig(fileName+"_random.jpg")   

    txtfile2 = fileName+'_FB_random_memEnhanced.txt'  
    max_values2 = df3.max()
    minval2 = df3.min()

    CQ1 = df3.quantile(0.25)
    CQ2 = df3.quantile(0.5) 
    CQ3 = df3.quantile(0.75)

    with open(txtfile2, 'a') as file:
                    file.write(str("_random"))
                    file.write(str(df3.max()))
                    file.write(str(minval2))
                    file.write(str(CQ1))
                    file.write(str(CQ2))
                    file.write(str(CQ3))
                    file.write("\n\n ***")




    custom_palette = ['gray']
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df4, palette=custom_palette, cut=0)
    plt.xlabel("Varying Jury size")
    plt.ylabel("Probabilities of Occurrence")
    plt.title("Random selection with memory")
    plt.savefig(fileName+"_random.jpg")   

    txtfile2 = fileName+'_FB_W_0_random_memEnhanced.txt'  
    max_values2 = df4.max()
    minval2 = df4.min()

    CQ1 = df4.quantile(0.25)
    CQ2 = df4.quantile(0.5) 
    CQ3 = df4.quantile(0.75)

    with open(txtfile2, 'a') as file:
                    file.write(str("_random"))
                    file.write(str(df4.max()))
                    file.write(str(minval2))
                    file.write(str(CQ1))
                    file.write(str(CQ2))
                    file.write(str(CQ3))
                    file.write("\n\n ***")


xplot = [0.0015,0.003,0.005,0.0065]     
print("Loading....")
G = nk.readGraph("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/SFB/facebook_combined.txt",nk.Format.SNAP)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())

variationOfJurySize(xplot,G,"screenshots_disparity/disparity_jury")