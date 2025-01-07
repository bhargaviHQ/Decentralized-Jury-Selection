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


def gini(x):
    """
    Compute the Gini coefficient of the input array x.

    Args:
        x (array): The input array.

    Returns:
        float: The Gini coefficient.
    """
    n = len(x)
    sorted_x = np.sort(x)
    cumulative_sum = np.cumsum(sorted_x)
    total_sum = np.sum(x)

    gini_coefficient = 2 * np.sum((cumulative_sum - total_sum / 2) / total_sum) / n
    return gini_coefficient

def lorenz_curve(x):
    """
    Compute the Lorenz curve of the input array x.

    Args:
        x (array): The input array.

    Returns:
        array: The Lorenz curve.
    """
    sorted_x = np.sort(x)
    cumulative_sum = np.cumsum(sorted_x)
    total_sum = np.sum(x)

    lorenz_curve = cumulative_sum / total_sum
    return lorenz_curve

def plot_lorenz_curve(x, fileName, title='Lorenz Curve'):
    """
    Plot the Lorenz curve of the input array x.

    Args:
        x (array): The input array.
        title (str): The title of the plot.
    """
    lorenz_curve2 = lorenz_curve(x)
    perfect_equality_line = np.linspace(0, 1, len(lorenz_curve2))
    plt.clf()
    plt.plot(perfect_equality_line, perfect_equality_line, label='Perfect Equality')
    plt.plot(np.arange(len(lorenz_curve2)) / (len(lorenz_curve2) - 1), lorenz_curve2, label='Lorenz Curve')
    
    plt.fill_between(np.arange(len(lorenz_curve2)) / (len(lorenz_curve2) - 1), lorenz_curve2, perfect_equality_line, color='#FFEFDB', alpha=0.2)

    plt.xlabel('Relative Frequency')
    plt.ylabel('Cumulative Proportion of Occurrences')
    plt.title(title)
    plt.legend()
    plt.savefig(fileName)
    
def variationRunAlgo(algoIndex, jurySize, graph):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    # occurrences = [0] * num_nodes
    # probability = [0] * num_nodes
    occurrences = np.zeros(num_nodes)
    probability = np.zeros(num_nodes)
    
    delta = 0
    element_counts = np.zeros(num_nodes)

    iterations = 1000
    fullDictionary = {}
    occupiedNodes = set()

    if algoIndex == 1:
        print("algoIndex : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, jurySize,occupiedNodes, 0.008)

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

    # for nodex in graphNodes:
    #     probability[nodex] =  occurrences[nodex] / sum(occurrences)


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
    return  occurrences


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
                plot_lorenz_curve(algorithm_1[itr],"rclCoverage_lorenz.jpg")
                plot_lorenz_curve(algorithm_3[itr],"random_lorenz.jpg")
                plot_lorenz_curve(algorithm_4[itr],"random_w_o_window_lorenz.jpg")
                itr = itr + 1



xplot = [0.0015]     
print("Loading....")
G = nk.readGraph("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/SFB/facebook_combined.txt",nk.Format.SNAP)
print("Loaded! nodes : ",G.numberOfNodes()," edges : ",G.numberOfEdges())

variationOfJurySize(xplot,G,"screenshots_disparity/disparity_jury")