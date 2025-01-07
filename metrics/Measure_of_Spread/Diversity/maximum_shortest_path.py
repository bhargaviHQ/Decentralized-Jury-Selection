import sys
sys.path.append('../../../')
import imports
from imports import *
from algorithm import rand_greedy_select
from algorithm import rand_select
from algorithm_repository_networkit import RCL_coverage

def maximumShortestPath(graph, selectedSet):
    allDistance = [0]*(len(selectedSet))
    allDistanceCounter = 0
    averageDistance = 0
    apsp = nk.distance.APSP(graph)
    apsp.run()
    for nodex in selectedSet:
        nodexDistance = [0]*(len(selectedSet))
        nodexDistanceCounter = 0
        minDistance = float('inf')
        graphNodes = list(graph.iterNodes())
        num_nodes = len(graphNodes)
        for nodey in selectedSet:
            if nodex != nodey:
                # if not nx.has_path(graph, nodex, nodey):
                #     #print("No path")
                #     continue
                shortest_path = apsp.getDistance(nodex, nodey)
                minDistance = shortest_path
                if minDistance == float('inf'):
                    minDistance = 0
                nodexDistance[nodexDistanceCounter] = minDistance
                nodexDistanceCounter = nodexDistanceCounter + 1
        allDistance[allDistanceCounter] =  sum(nodexDistance)/len(nodexDistance)
        allDistanceCounter = allDistanceCounter + 1
    averageDistance = sum(allDistance)/len(allDistance)
    return  averageDistance

def maximumShortestPathLargeTable(graph, selectedSet):
    allDistance = [0]*(len(selectedSet))
    allDistanceCounter = 0
    averageDistance = 0
    # apsp = nk.distance.APSP(graph)
    # apsp.run()
    for nodex in selectedSet:
        nodexDistance = [0]*(len(selectedSet))
        nodexDistanceCounter = 0
        minDistance = float('inf')
        graphNodes = list(graph.iterNodes())
        num_nodes = len(graphNodes)
        for nodey in selectedSet:
            print("node y : ",nodey, " nodex : ",nodex)
            if nodex != nodey:
                # if not nx.has_path(graph, nodex, nodey):
                #     #print("No path")
                #     continue
                bfs = nk.distance.BFS(graph, nodex, True, False, nodey)
                bfs.run()
                shortest_path = bfs.distance(nodey)
                #shortest_path = apsp.getDistance(nodex, nodey)
                minDistance = shortest_path
                if minDistance == float('inf'):
                    minDistance = 0
                nodexDistance[nodexDistanceCounter] = minDistance
                nodexDistanceCounter = nodexDistanceCounter + 1
        allDistance[allDistanceCounter] =  sum(nodexDistance)/len(nodexDistance)
        allDistanceCounter = allDistanceCounter + 1
    averageDistance = sum(allDistance)/len(allDistance)
    return  averageDistance

# G = nk.generators.BarabasiAlbertGenerator(2,20).generate()
# selectedSet = RCL_coverage.rclCoverageSelection(G, 6)
# print(maximumShortestPath(G, selectedSet))

# k = 8
# graph = LFR_benchmark_graph(100,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)


# count1 = 0
# count2 = 0
# for i in range (0,100):
#     selection = rand_greedy_select.randomGreedySelection(graph, k)
#     # print(selection)
#     # print(maximumCoverage(graph, selection))
#     count1 = count1 + maximumShortestPath(graph, selection)

#     selection2 = rand_select.randomSelection(graph,k)
#     # print(selection2)
#     # print(maximumCoverage(graph, selection2))
#     count2 = count2 + maximumShortestPath(graph, selection2)

# print("First : ", count1/100)
# print("Second : ", count2/100)