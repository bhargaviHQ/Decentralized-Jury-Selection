import sys
sys.path.append('../../../')
import imports
from imports import *

from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm import rand_community_greedy_select
from algorithm import rand_community_select
from algorithm import rand_probability_select
from graph_generator import generator

from metrics.Measure_of_Spread.Coverage import maximum_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes
class GraphVisualization:
    def __init__(self):
        self.visual = []
          
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        
        networkSize = len(G.nodes)
        print("Network Size is : ",networkSize)
        return G

def variationOfJurySizePlotAlgo(algoIndex, jurySizeList, graph):
    distanceList = [0]*len(jurySizeList)

    if algoIndex == 1:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_select.randomSelection(graph, jurySize)
            distanceAvg  = maximum_coverage.maximumCoverage(graph, selectedSet)
            distanceList[itr] = round(distanceAvg)
            itr += 1    

    elif algoIndex == 2:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            distanceAvg  = maximum_coverage.maximumCoverage(graph, selectedSet)
            distanceList[itr] = round(distanceAvg)
            itr += 1    
    
    elif algoIndex == 3:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            distanceAvg  = maximum_coverage.maximumCoverage(graph, selectedSet)
            distanceList[itr] = round(distanceAvg)
            itr += 1    
    
    elif algoIndex == 4:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            distanceAvg  = maximum_coverage.maximumCoverage(graph, selectedSet)
            distanceList[itr] = round(distanceAvg)
            itr += 1    
 
    elif algoIndex == 5:
        itr = 0
        for jurySize in jurySizeList:
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            distanceAvg  = maximum_coverage.maximumCoverage(graph, selectedSet)
            distanceList[itr] = round(distanceAvg)
            itr += 1    

    return  distanceList

def runZilliqa(graph):
    graphObjects = [graph]
    for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
                distanceList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph)
                distanceList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph)
                distanceList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph)
                distanceList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph)
                distanceList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph)

                plt.plot(jurySizeList,distanceList_01, label="randomSelection")
                plt.plot(jurySizeList,distanceList_02, label="randomGreedySelection")
                plt.plot(jurySizeList,distanceList_03, label="randomCommunityGreedySelection")
                plt.plot(jurySizeList,distanceList_04, label="randomCommunitySelection")
                plt.plot(jurySizeList,distanceList_05, label="runRandomProbSelect")

                plt.xlabel('jury size', fontsize=10)
                plt.ylabel('Sum of minimum distance from unselected to selected node', fontsize=10)
                plt.title("Comparision of Sum of minimum distance for varying jury size")

                plt.legend()
                #plt.show()
                plt.savefig("plot_maximum_coverage_zilliqa.py")

G = GraphVisualization()

print("Running....")
count = 0 
with open("../../../zilliqa_data_fresh_complete.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
     count +=1
     G.addEdge(row[0] , row[1])
graph = G.visualize()

runZilliqa(graph)