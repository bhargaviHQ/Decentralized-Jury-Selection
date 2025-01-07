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
from metrics.Fairness import frequency_of_selection


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

def returnDisparity(occur,delta):
            keys = list(occur.keys())
            values = list(occur.values())

            sorted_value_index = np.argsort(values)
            occur_sorted = {keys[i]: values[i] for i in sorted_value_index}
            # occur.sort(reverse=True)
            percentileBefore =  np.percentile(list(occur_sorted.values()), delta)
            percentileAfter = np.percentile(list(occur_sorted.values()), (100 - delta))

            setRemove = set()
            for item, itemValue in occur_sorted.items():
            # for item in occur_sorted:
                if itemValue > percentileAfter or itemValue < percentileBefore:
                    setRemove.add(item)
            for setItem in setRemove:
                #occur_sorted.remove(setItem)
                occur_sorted.pop(setItem)
            return max(list(occur_sorted.values())) - min(list(occur_sorted.values()))

def variationOfJurySizePlotAlgo(algoIndex, jurySizeList, graph):
    num_nodes = len(graph.nodes)   
    occurrencesList = []
    disparity = [0]*len(jurySizeList)
    # occurrences = [0] * num_nodes
    occurrences = {}
    for i in graph.nodes:
        occurrences[i] = 0
    delta = 5
    itr = 0
    if algoIndex == 1:
        itr = 0
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0

            for i in range (0,100):
                selectedSet = rand_select.randomSelection(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences)
    
            disparity[itr] = returnDisparity(occurrences,delta)
            itr = itr + 1  

    elif algoIndex == 2:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0

            for i in range (0,100):
                selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            # occurrencesList[itr] = occurrences
            disparity[itr] = returnDisparity(occurrences,delta)
            itr = itr + 1  

    elif algoIndex == 3:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            disparity[itr] = returnDisparity(occurrences,delta)
            itr = itr + 1  

    elif algoIndex == 4:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            disparity[itr] = returnDisparity(occurrences,delta)
            itr = itr + 1  

    elif algoIndex == 5:
        for jurySize in jurySizeList:
            for i in graph.nodes:
                occurrences[i] = 0
            for i in range (0,100):
                selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
                occurrences = frequency_of_selection.frequencyOfSelection(graph, selectedSet,occurrences) 
            disparity[itr] = returnDisparity(occurrences,delta)
            itr = itr + 1  

    # itr = 0
    # for pos in range(0,len(occurrencesList)):
    #     occur = occurrencesList[pos]
    #     print(" - - --",max(list(occur.values())))
    #     keys = list(occur.keys())
    #     values = list(occur.values())

    #     sorted_value_index = np.argsort(values)
    #     occur_sorted = {keys[i]: values[i] for i in sorted_value_index}
    #     # occur.sort(reverse=True)
    #     percentileBefore =  np.percentile(list(occur_sorted.values()), delta)
    #     percentileAfter = np.percentile(list(occur_sorted.values()), (100 - delta))

    #     setRemove = set()
    #     for item, itemValue in occur_sorted.items():
    #     # for item in occur_sorted:
    #         if itemValue > percentileAfter or itemValue < percentileBefore:
    #             setRemove.add(item)
    #     for setItem in setRemove:
    #         #occur_sorted.remove(setItem)
    #         occur_sorted.pop(setItem)
    #     print(" MAX : ", max(list(occur_sorted.values())))
    #     print(" mins : ", min(list(occur_sorted.values())))
    #     disparity[itr] = max(list(occur_sorted.values())) - min(list(occur_sorted.values()))
    #     itr += 1
    return  disparity

def runZilliqa(graph):
    graphObjects = [graph]
    for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
                distanceList_01 = variationOfJurySizePlotAlgo(1,jurySizeList,graph)
                print("done 01 : ", distanceList_01)
                distanceList_02 = variationOfJurySizePlotAlgo(2,jurySizeList,graph)
                print("done 01 : ", distanceList_01)
                distanceList_03 = variationOfJurySizePlotAlgo(3,jurySizeList,graph)
                print("done 01 : ", distanceList_01)
                distanceList_04 = variationOfJurySizePlotAlgo(4,jurySizeList,graph)
                print("done 01 : ", distanceList_01)
                distanceList_05 = variationOfJurySizePlotAlgo(5,jurySizeList,graph)
                print("done 01 : ", distanceList_01)

                plt.plot(jurySizeList,distanceList_01, label="randomSelection")
                plt.plot(jurySizeList,distanceList_02, label="randomGreedySelection")
                plt.plot(jurySizeList,distanceList_03, label="randomCommunityGreedySelection")
                plt.plot(jurySizeList,distanceList_04, label="randomCommunitySelection")
                plt.plot(jurySizeList,distanceList_05, label="runRandomProbSelect")

                plt.xlabel('jury size', fontsize=10)
                plt.ylabel('Disparity in frequency of selection', fontsize=10)
                plt.title("Comparision of Disparity in frequency of selection for varying jury size")

                plt.legend()
                #plt.show()
                plt.savefig("plot_frequency_of_selection_zilliqa.jpg")

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