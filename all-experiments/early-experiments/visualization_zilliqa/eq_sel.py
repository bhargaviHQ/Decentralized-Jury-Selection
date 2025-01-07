import sys
sys.path.append('../')
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

def equalityOfSelectionBlockchain(graph, selectedSet,occurrences):
        for item in selectedSet:
            occurrences[item] =  occurrences[item] + 1  
        return occurrences  

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
    

class graphObject:
    def __init__(self, nodes, average_degree = 5, max_degree = 10, min_community = 5, max_community = 10):
        self.nodes = nodes
        self.average_degree = average_degree 
        self.max_degree  = max_degree
        self.min_community = min_community
        self.max_community = max_community

    def setGraphObjectMuVariation(self):
        graph_object_list = []
        mu_list = [0.1,0.4,0.6,0.8]
        for mu in mu_list:
            graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

    def setGraphObject(self):
        graph_object_list = []
        mu_list = [0.1]
        for mu in mu_list:
            graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

#graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)



def variationOfJurySizePlotAlgo(algoIndex, jurySizeList, graph):
    num_nodes = len(graph.nodes)   
    occurrencesList = [0]*len(jurySizeList)
    probability_all = [0]*len(jurySizeList)
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
            for i in range (0,1):
                selectedSet = rand_select.randomSelection(graph, jurySize)
                occurrences = equalityOfSelectionBlockchain(graph, selectedSet,occurrences)

            list = []
            for i in occurrences:
                list.append(occurrences[i])
            finalSum = sum(list)   

            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / finalSum
            
            list2 = []
            for i in probability:
                list2.append(probability[i])
            finalSum2 = sum(list2)       
            print("finalSum2 - -- ",finalSum2)  
            print("len(probability) - -- ",len(probability))  

            probability_all[itr] = finalSum2/len(probability)
            itr += 1
        print(" -- - - --- ",probability_all)

    elif algoIndex == 2:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sum(occurrences)
            probability_all[itr] = sum(probability)/len(probability)
            itr += 1
    elif algoIndex == 3:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sum(occurrences)
            probability_all[itr] = sum(probability)/len(probability)
            itr += 1
    elif algoIndex == 4:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sum(occurrences)
            probability_all[itr] = sum(probability)/len(probability)
            itr += 1

    elif algoIndex == 5:
        for jurySize in jurySizeList:
            for i in range (0,100):
                selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
                occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences) 
            for nodex in graph:
                probability[nodex] =  occurrences[nodex] / sum(occurrences)
            probability_all[itr] = sum(probability)/len(probability)
            itr += 1
    return  probability_all

def variationOfJurySize():
    graph_param = [graphObject(2500, 10, 20, 20, 50)]
    #graph_param = generator.graph_param_jury_size

    #graph_n_4 = LFR_benchmark_graph(200,3,1.5,0.1,average_degree=10,max_degree=20, min_community= 20, max_community = 50, seed=10)
    # graph_n_5 = LFR_benchmark_graph(1000,3,1.5,0.1,average_degree=10,max_degree=20, min_community= 20, max_community = 50, seed=10)
    # graph_n_6 = LFR_benchmark_graph(1200,3,1.5,0.1,average_degree=10,max_degree=20, min_community= 20, max_community = 50, seed=10)


    for obj in graph_param:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                print("Network size :",networkSize)
                jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
                
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

                # plt.plot(jurySizeList,distanceList_01)
                # plt.plot(jurySizeList,distanceList_02)
                # plt.plot(jurySizeList,distanceList_03)
                # plt.plot(jurySizeList,distanceList_04)
                # plt.plot(jurySizeList,distanceList_05)

                # plt.xlabel('jury size', fontsize=10)
                # plt.ylabel('Disparity in frequency of selection', fontsize=10)
                # plt.title("Comparision of Disparity in frequency of selection for varying jury size")

                # plt.legend()
                # plt.show()
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


def variationRunAlgo(algoIndex, jurySize, graph ):
    num_nodes = len(graph.nodes)
    occurrences = [0] * num_nodes
    delta = 5
    probability = [0] * num_nodes
    if algoIndex == 1:
        for i in range (0,100):
            selectedSet = rand_select.randomSelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 2:
        for i in range (0,100):
            selectedSet = rand_greedy_select.randomGreedySelection(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    
    elif algoIndex == 3:
        for i in range (0,100):
            selectedSet = rand_community_greedy_select.randomCommunityGreedySelection(graph, jurySize, algorithms.infomap(graph).communities)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    elif algoIndex == 4:
        for i in range (0,100):
            selectedSet = rand_community_select.randomCommunitySelection(graph, jurySize, algorithms.infomap(graph).communities)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)
 
    elif algoIndex == 5:
        for i in range (0,100):
            selectedSet = rand_probability_select.runRandomProbSelect(graph, jurySize)
            occurrences = equality_of_selection.equalityOfSelection(graph, selectedSet,occurrences)

    for nodex in graph:
        probability[nodex] =  occurrences[nodex] / sum(occurrences)
    probabilityAverage = sum(probability)/len(probability)

    return  probabilityAverage

def variationOfNetworkSize():
    graph_param_list = [
        graphObject(500, 5, 10, 5, 10),
        graphObject(1500, 10, 20, 20, 50),
        graphObject(2500, 10, 20, 20, 50),
        graphObject(5000, 10, 20, 20, 50),
        graphObject(10000, 10, 20, 20, 100)
        ]
    #graph_param_list = generator.graph_param_list
    # networkSizeList = [50,100,200]
    networkSizeList = generator.networkSizeList

    distanceList_01 = [0]*len(networkSizeList)
    distanceList_02 = [0]*len(networkSizeList)
    distanceList_03 = [0]*len(networkSizeList)
    distanceList_04 = [0]*len(networkSizeList)
    distanceList_05 = [0]*len(networkSizeList)
    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObject()
            for graph in graphObjects:
                
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)
        
                distance_01 = variationRunAlgo(1,jurySize,graph)
                distance_02 = variationRunAlgo(2,jurySize,graph)
                distance_03 = variationRunAlgo(3,jurySize,graph)
                distance_04 = variationRunAlgo(4,jurySize,graph)
                distance_05 = variationRunAlgo(5,jurySize,graph)

                distanceList_01[itr] = distance_01
                distanceList_02[itr] = distance_02
                distanceList_03[itr] = distance_03
                distanceList_04[itr] = distance_04
                distanceList_05[itr] = distance_05
    
                itr = itr + 1
    # plt.plot(networkSizeList,distanceList_01)
    # plt.plot(networkSizeList,distanceList_02)
    # plt.plot(networkSizeList,distanceList_03)
    # plt.plot(networkSizeList,distanceList_04)
    # plt.plot(networkSizeList,distanceList_05)
    
    # plt.xlabel('Network Size', fontsize=10)
    # plt.ylabel('Disparity in frequency of selection', fontsize=10)
    # plt.title("Comparision of Disparity in frequency of selection for varying network size")

    # plt.legend()
    # plt.show()



    output = PrettyTable(['Algorithm','Network Size', 'Avg probability of node selection'])
    output.add_row(['randomSelection',networkSizeList[0],round(distanceList_01[0],10)])
    output.add_row(['randomSelection',networkSizeList[1],round(distanceList_01[1],10)])
    output.add_row(['randomSelection',networkSizeList[2],round(distanceList_01[2],10)])
    output.add_row(['randomSelection',networkSizeList[3],round(distanceList_01[3],10)])
    output.add_row(['randomSelection',networkSizeList[4],round(distanceList_01[4],10)])

    output.add_row(['randomGreedySelection',networkSizeList[0],round(distanceList_02[0],10)])
    output.add_row(['randomGreedySelection',networkSizeList[1],round(distanceList_02[1],10)])
    output.add_row(['randomGreedySelection',networkSizeList[2],round(distanceList_02[2],10)])
    output.add_row(['randomGreedySelection',networkSizeList[3],round(distanceList_02[3],10)])
    output.add_row(['randomGreedySelection',networkSizeList[4],round(distanceList_02[4],10)])

    output.add_row(['randomCommunityGreedySelection',networkSizeList[0],round(distanceList_03[0],10)])
    output.add_row(['randomCommunityGreedySelection',networkSizeList[1],round(distanceList_03[1],10)])
    output.add_row(['randomCommunityGreedySelection',networkSizeList[2],round(distanceList_03[2],10)])
    output.add_row(['randomCommunityGreedySelection',networkSizeList[3],round(distanceList_03[3],10)])
    output.add_row(['randomCommunityGreedySelection',networkSizeList[4],round(distanceList_03[4],10)])

    output.add_row(['randomCommunitySelection',networkSizeList[0],round(distanceList_04[0],10)])
    output.add_row(['randomCommunitySelection',networkSizeList[1],round(distanceList_04[1],10)])
    output.add_row(['randomCommunitySelection',networkSizeList[2],round(distanceList_04[2],10)])
    output.add_row(['randomCommunitySelection',networkSizeList[3],round(distanceList_04[3],10)])
    output.add_row(['randomCommunitySelection',networkSizeList[4],round(distanceList_04[4],10)])

    output.add_row(['runRandomProbSelect',networkSizeList[0],round(distanceList_05[0],10)])
    output.add_row(['runRandomProbSelect',networkSizeList[1],round(distanceList_05[1],10)])
    output.add_row(['runRandomProbSelect',networkSizeList[2],round(distanceList_05[2],10)])
    output.add_row(['runRandomProbSelect',networkSizeList[3],round(distanceList_05[3],10)])
    output.add_row(['runRandomProbSelect',networkSizeList[4],round(distanceList_05[4],10)])

    print(output)



def variationOfMuValues():
    graph_param_list = [
       graphObject(2500, 10, 20, 20, 50)
        ]
    #graph_param_list = generator.graph_param_list_mu
    # mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    mu_list = generator.mu_list
    distanceList_01 = [0]*len(mu_list)
    distanceList_02 = [0]*len(mu_list)
    distanceList_03 = [0]*len(mu_list)
    distanceList_04 = [0]*len(mu_list)
    distanceList_05 = [0]*len(mu_list)

    itr = 0
    for obj in graph_param_list:
            graphObjects = obj.setGraphObjectMuVariation()
            for graph in graphObjects:
                networkSize = len(graph.nodes)
                jurySize = round(networkSize*0.05)

                distance_01 = variationRunAlgo(1,jurySize,graph)
                distance_02 = variationRunAlgo(2,jurySize,graph)
                distance_03 = variationRunAlgo(3,jurySize,graph)
                distance_04 = variationRunAlgo(4,jurySize,graph)
                distance_05 = variationRunAlgo(5,jurySize,graph)

                distanceList_01[itr] = distance_01
                distanceList_02[itr] = distance_02
                distanceList_03[itr] = distance_03
                distanceList_04[itr] = distance_04
                distanceList_05[itr] = distance_05 

                itr = itr + 1
    
    # plt.plot(mu_list,distanceList_01)
    # plt.plot(mu_list,distanceList_02)
    # plt.plot(mu_list,distanceList_03)
    # plt.plot(mu_list,distanceList_04)
    # plt.plot(mu_list,distanceList_05)
    
    # plt.xlabel('fraction of inter-community edges', fontsize=10)
    # plt.ylabel('Disparity in frequency of selection', fontsize=10)
    # plt.title("Comparision of Disparity in frequency of selection for varying fraction of inter-community edges")

    # plt.legend()
    # plt.show()

    output = PrettyTable(['Algorithm','mu value', 'Avg probability of node selection'])
    print("Network size : 2500")
    for mu in mu_list:
        output.add_row(['randomSelection',mu,round(distanceList_01[0],10)])
    for mu in mu_list:
        output.add_row(['randomGreedySelection',mu,round(distanceList_02[0],10)])
    for mu in mu_list:
        output.add_row(['randomCommunityGreedySelection',mu,round(distanceList_03[0],10)])
    for mu in mu_list:
        output.add_row(['randomCommunitySelection',mu,round(distanceList_04[0],10)])
    for mu in mu_list:
        output.add_row(['runRandomProbSelect',mu,round(distanceList_05[0],10)])
    
    print(output)


def runZilliqa(graph):

    networkSize = len(graph.nodes)
    print("Network size :",networkSize)
    jurySizeList = [round(networkSize*0.02),round(networkSize*0.05),round(networkSize*0.1),round(networkSize*0.15),round(networkSize*0.2)]
    
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
# variationOfJurySize(graph)
# variationOfNetworkSize()
# variationOfMuValues()

G = GraphVisualization()

# Read from file 
print("Running....")
count = 0 
with open("../../zilliqa_data_fresh_complete.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
     count +=1
     G.addEdge(row[0] , row[1])
     if count >1000:
        break
graph = G.visualize()
print("Size ---------", len(graph.nodes))
print(graph)
runZilliqa(graph)
