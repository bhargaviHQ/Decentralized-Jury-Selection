import sys
import imports
from imports import *

def createDictionary(fullDict,candidate,timeWindow):
   
    return fullDict

def randomSelection(graph,k):   
    trials = 10
    graphNodes = list(graph.iterNodes())
    selectedNodes = set()
    fullDictionary = {}
    occupiedNodes = set()
    for iteration in range(0, trials):
        print("TRIAL : : : :  ", iteration)
        selectedNodes = set()
        timeWindow = random.randint(1,10)
        for key, value in fullDictionary.items():
            if value == iteration:
                occupiedNodes.remove(key)
                print("Node remove from occupied status : ", key)
        while (len(selectedNodes) < k):
            #print("Size : ",len(list(set(graphNodes).difference(occupiedNodes))))
            candidate = random.choice(list(set(graphNodes).difference(occupiedNodes)))
            selectedNodes.add(candidate)        
            occupiedNodes.add(candidate)
            fullDictionary[candidate] = int(iteration + timeWindow)
        print("Selected set : ", selectedNodes, " inactive till trial : ", int(iteration + timeWindow))
        # print("Size of occupiedNodes : ", len(occupiedNodes))
            

    return "yes"

G = nk.generators.BarabasiAlbertGenerator(2,50).generate()


print(randomSelection(G, 4))