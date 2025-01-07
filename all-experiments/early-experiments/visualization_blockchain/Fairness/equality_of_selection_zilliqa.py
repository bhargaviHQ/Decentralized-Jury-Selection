import sys
sys.path.append('../../')
import imports
from imports import *

from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm import rand_community_greedy_select
from algorithm import rand_community_select
from algorithm import rand_probability_select
from graph_generator import generator

from metrics.Fairness import equality_of_selection
from metrics.Fairness import equality_of_selection

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
    num_nodes = len(graph.nodes)   
    occurrencesList = [0]*len(jurySizeList)
    std_dev_all = [0]*len(jurySizeList)
    # probability = [0] * num_nodes
    #occurrences = [0] * num_nodes
    occurrences = {}
    for i in graph.nodes:
        occurrences[i] = 0
    probability = {}
    for i in graph.nodes:
        probability[i] = 0
    delta = 5
    itr = 0

    if algoIndex == 1:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_select.randomSelection(graph, jurySize)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

            occurrencesList = []
            for i in occurrences:
                occurrencesList.append(occurrences[i])
            sumOccurence = sum(occurrencesList)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sumOccurence

            probabilityList = []
            for i in probability:
                probabilityList.append(probability[i])

            std_dev_all[itr] = statistics.stdev(probabilityList)
            itr += 1

    elif algoIndex == 2:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            occurrencesList = []
            for i in occurrences:
                occurrencesList.append(occurrences[i])
            sumOccurence = sum(occurrencesList)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sumOccurence

            probabilityList = []
            for i in probability:
                probabilityList.append(probability[i])

            std_dev_all[itr] = statistics.stdev(probabilityList)
            itr += 1
    elif algoIndex == 3:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            occurrencesList = []
            for i in occurrences:
                occurrencesList.append(occurrences[i])
            sumOccurence = sum(occurrencesList)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sumOccurence

            probabilityList = []
            for i in probability:
                probabilityList.append(probability[i])

            std_dev_all[itr] = statistics.stdev(probabilityList)
            itr += 1
    elif algoIndex == 4:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            occurrencesList = []
            for i in occurrences:
                occurrencesList.append(occurrences[i])
            sumOccurence = sum(occurrencesList)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sumOccurence

            probabilityList = []
            for i in probability:
                probabilityList.append(probability[i])

            std_dev_all[itr] = statistics.stdev(probabilityList)
            itr += 1

    elif algoIndex == 5:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            occurrencesList = []
            for i in occurrences:
                occurrencesList.append(occurrences[i])
            sumOccurence = sum(occurrencesList)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sumOccurence

            probabilityList = []
            for i in probability:
                probabilityList.append(probability[i])

            std_dev_all[itr] = statistics.stdev(probabilityList)
            itr += 1
    return  std_dev_all

def runZilliqa(graph):

    networkSize = len(graph.nodes)
    print("Network size :",networkSize)
    jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
    print(" - 00 ")
    distanceList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph)
    print(" - 01 ")
    distanceList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph)
    print(" - 02 ")
    distanceList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph)
    print(" - 03 ")
    distanceList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph)
    print(" - 04 ")
    distanceList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph)
    print(" - 05 ")

    output = PrettyTable(['Algorithm','Jury Size', 'Avg probability of node selection'])
    for jurySize in jurySizeList:
        output.add_row(['randomSelection',jurySize,round(distanceList_01[0],10)])
    for jurySize in jurySizeList:
        output.add_row(['randomGreedySelection',jurySize,round(distanceList_02[0],10)])
    for jurySize in jurySizeList:
        output.add_row(['randomCommunityGreedySelection',jurySize,round(distanceList_03[0],10)])
    for jurySize in jurySizeList:
        output.add_row(['randomCommunity',jurySize,round(distanceList_04[0],10)])
    for jurySize in jurySizeList:
        output.add_row(['runRandomProbSelect',jurySize,round(distanceList_05[0],10)])
                
    print(output)

G = GraphVisualization()

print("Running....")
count = 0 
with open("../../zilliqa_data_fresh_complete.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
     count +=1
     G.addEdge(row[0] , row[1])
graph = G.visualize()
runZilliqa(graph)
# print("Network size is : ", len(graph.nodes))
# nx.draw(graph)
# #plt.show()
# plt.savefig("zilliqa_network.jpg")