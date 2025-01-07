import sys
sys.path.append('../')
import imports
from imports import *

def createDictionary(graphNodes, graph):
    fullDict = {} 
    bc = nk.centrality.Betweenness(graph, normalized=True)
    bc.run()
    betweenness_values = bc.scores()
    for nodex in graphNodes: 
        fullDict[nodex] = betweenness_values[nodex]
    return fullDict

def rclBetweenSelection(graphNodes,nodesReq,frac=5): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    selectedNodesTemp = set()
    fullDictionary =  createDictionary(graph,graphNodes)
    if nodesReq*frac > len(graph):
        nodesToSelect = len(graph) - 1
    else :
        nodesToSelect = nodesReq*frac

    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(graph)))

    while (len(selectedNodes) < nodesReq):
            candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
            if (candidate in selectedNodesTemp):
                selectedNodes.add(int(candidate))
            fullDictionary.pop(candidate)
            
    # candidate = betweenness_values.index(max(betweenness_values))
    # if (candidate in selectedNodesTemp):
    #     selectedNodes.add(int(candidate))
    # betweenness_values.pop(betweenness_values.index(max(betweenness_values)))
        
    return selectedNodes


def rclBetweenSelectionWithSubset(graphNodes,nodesReq,occupiedNodes,percent=0.1): 
    selectedNodes = set()
    graph = list(graphNodes.iterNodes())
    graph = list(set(graph).difference(occupiedNodes))

    selectedNodesTemp = set()
    fullDictionary =  createDictionary(graph,graphNodes)
    if percent>1:
        percent = 0.95
    elif percent<0:
        percent = 0.1
    nodesToSelect = len(graph)*percent
    while (len(selectedNodesTemp) < nodesToSelect):
        selectedNodesTemp.add(int(random.choice(graph)))

    while (len(selectedNodes) < nodesReq):
            if(len(fullDictionary)==0):
                elementAdd = random.choice(graph)
                selectedNodes.add(int(elementAdd))
                occupiedNodes.add(int(elementAdd))
            else:
                candidate = max(zip(fullDictionary.values(), fullDictionary.keys()))[1]  
                if (candidate in selectedNodesTemp):
                    selectedNodes.add(int(candidate))
                    occupiedNodes.add(int(candidate))
                fullDictionary.pop(candidate)
                
    return selectedNodes, occupiedNodes
# G = nk.generators.BarabasiAlbertGenerator(2,40).generate()


# print(rclBetweenSelection(G, 10))