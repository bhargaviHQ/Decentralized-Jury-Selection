import sys
sys.path.append('../../../../../../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns
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

from metrics.Fairness import equality_of_selection
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

      
def variationRunAlgo(algoIndex, graph,betweenness_values):
    graphNodes = list(graph.iterNodes())
    num_nodes = len(graphNodes)
    occurrences = [0] * num_nodes
    probability = [0] * num_nodes
    delta = 0
    element_counts = np.zeros(num_nodes)

    iterations = 2000
    fullDictionary = {}
    occupiedNodes = set()

    if algoIndex == 1:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)
            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_Betweenness.rclBetweenSelectionWithSubsetBetween(graph, 25,occupiedNodes,betweenness_values, 0.25)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = RCL_coverage.rclCoverageSelectionWithSubset(graph, 25,occupiedNodes, 0.25)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 3:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Betweenness.betweenSelectionWithProbBetween(graph, 25,occupiedNodes,betweenness_values, 0.3)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 4:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Prob_Coverage.coverageSelectionWithProb(graph, 25,occupiedNodes, 0.3)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 5:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Betweenness.seedBetweenSelectionWithSizeBetween(graph, 25,occupiedNodes,betweenness_values, 10)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 6:
        print("Algo index : ",algoIndex)
        for i in range (0,iterations):
            timeWindow = random.randint(1,20)

            for key, value in fullDictionary.items():
                if value == i:
                    occupiedNodes.remove(key)
            selectedSet,occupiedNodes = Seed_Coverage.seedCoverSelectionWithSize(graph, 25,occupiedNodes, 10)
            
            for nodex in selectedSet:
                fullDictionary[nodex] = int(i + timeWindow)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)


    for nodex in graphNodes:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)

    return  probability

# def plotGraphs(df1,df2,df3,df4,df5,df6,fileName):
#                 custom_palette = ['gray']
#                 plt.figure(figsize=(12, 6))
#                 sns.violinplot(data=df, palette=custom_palette, cut=0)
#                 plt.xlabel("Varying Network size")
#                 plt.ylabel("Probabilities of Occurrence")
#                 plt.title("Coverage Strategy for Network size")
#                 plt.savefig(fileName+"_coverage.jpg") 


def variationOfSeedSize(xplot,graph_param_list, jurySize, fileName):


    algorithm_1 = [0]*len(xplot)
    algorithm_2 = [0]*len(xplot)
    algorithm_3 = [0]*len(xplot)
    algorithm_4 = [0]*len(xplot)
    algorithm_5 = [0]*len(xplot)
    algorithm_6 = [0]*len(xplot)
    itr = 0
    # list_names = [f"algorithm={i}" for i in xplot]
    list_df1 = []
    list_df2 = []
    list_df3 = []
    list_df4 = []
    list_df5 = []
    list_df6 = []
    
    for q in range(3):

        for obj in graph_param_list:
                    graph = obj.graphGenerator()
                    obj.getParams()
                    list_names = [f"{i}" for i in xplot]
                    df1 = pd.DataFrame()
                    df2 = pd.DataFrame()
                    df3 = pd.DataFrame()
                    df4 = pd.DataFrame()
                    df5 = pd.DataFrame()
                    df6 = pd.DataFrame()
                    ########
                    #Calculate Betweenness centrality
                    ########
                    bc = nk.centrality.Betweenness(graph, normalized=True)
                    bc.run()
                    betweenness_values = bc.scores()

                    algorithm_1[itr] = variationRunAlgo(1,graph,betweenness_values)
                    algorithm_2[itr] = variationRunAlgo(2,graph,betweenness_values)
                    algorithm_3[itr] = variationRunAlgo(3,graph,betweenness_values)
                    algorithm_4[itr] = variationRunAlgo(4,graph,betweenness_values)
                    algorithm_5[itr] = variationRunAlgo(5,graph,betweenness_values)
                    algorithm_6[itr] = variationRunAlgo(6,graph,betweenness_values)

                    df1[list_names[itr]] = algorithm_1[itr] 
                    df2[list_names[itr]] = algorithm_2[itr] 
                    df3[list_names[itr]] = algorithm_3[itr] 
                    df4[list_names[itr]] = algorithm_4[itr] 
                    df5[list_names[itr]] = algorithm_5[itr] 
                    df6[list_names[itr]] = algorithm_6[itr] 

                    itr = itr + 1
                    list_df1.append(df1.max().max())
                    list_df2.append(df2.max().max())
                    list_df3.append(df3.max().max())
                    list_df4.append(df4.max().max())
                    list_df5.append(df5.max().max())
                    list_df6.append(df6.max().max())

    with open("BA_disparity_algo_complete.txt", 'a') as file:
                    file.write(str(statistics.mean(list_df1)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_df2)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_df3)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_df4)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_df5)))
                    file.write("\n\n ***")
                    file.write(str(statistics.mean(list_df6)))
                    file.write("\n\n ***")


graph_param_list = [
    graphObject(15000,3)
        ]
jurySize = 25       
print("Running for jurySize :",jurySize)

xplot = ["Pool Btw","Pool Cov","Prob Btw","Prob Cov","Seed Btw","Seed Cov"]  
start_time = time.time()

process = psutil.Process()
variationOfSeedSize(xplot,graph_param_list,jurySize,"screenshots_disparity/disparity_network")

end_time = time.time()
elapsed_time_ms = (end_time - start_time)

print("Program took", elapsed_time_ms, "milliseconds to run")
cpu_percent = process.cpu_percent(interval=1)  # CPU usage over a 1-second interval
memory_info = process.memory_info()

# Print the statistics
print(f"CPU Usage: {cpu_percent}%")
print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")