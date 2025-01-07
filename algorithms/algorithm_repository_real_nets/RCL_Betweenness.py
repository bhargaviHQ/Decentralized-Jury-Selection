import sys
sys.path.append('../')
import imports
from imports import *

def rclBetweenCSelection(graphNodes,nodesReq,frac=5): 
    selectedNodesTemp = set()
    selectedNodes = set()
    nodesToSelect = nodesReq*frac
    dict = {}
    deg_centrality = nx.betweenness_centrality(graphNodes)
    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(list(graphNodes))))
    for node in selectedNodesTemp:
        dict[node] = deg_centrality[str(node)]
    top_keys = sorted(dict, key=lambda k: dict[k], reverse=True)[:nodesReq]
    for key in top_keys:
        selectedNodes.add(int(key))
    return selectedNodes

# graph = LFR_benchmark_graph(10,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)

# print(rclDegreeCSelection(2))