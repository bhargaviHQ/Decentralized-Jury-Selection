import sys
sys.path.append('../')
import imports
from imports import *
from cdlib import algorithms

class graphObject:
    def __init__(self, nodes, average_degree = 5, max_degree = 10, min_community = 5, max_community = 10):
        self.nodes = nodes
        self.average_degree = average_degree 
        self.max_degree  = max_degree
        self.min_community = min_community
        self.max_community = max_community

    def setGraphObject(self):
        graph_object_list = []
        print("Mu list : ->")
        mu_list = [0.1,0.2,0.4,0.6,0.8]
        for mu in mu_list:
            graph_object_list.append(LFR_benchmark_graph(self.nodes,3,1.5,mu,average_degree=self.average_degree,
        max_degree=self.max_degree, min_community=self.min_community, max_community = self.max_community, seed=10))

        return graph_object_list

#graph = LFR_benchmark_graph(25,3,1.5,0.1,average_degree=5,max_degree=10, min_community= 5, max_community = 10, seed=10)

graph_param_list = [
    graphObject(50, 5, 10, 5, 10),
    # graphObject(1000, 5, 10, 5, 10),
    # graphObject(5000, 5, 10, 5, 10),
    # graphObject(20000, 5, 10, 5, 10),
    # graphObject(40000, 5, 10, 5, 10)
]


#ONE GRAPH FOR JURY SIZE VARIATION
graph_param_jury_size = [graphObject(2500, 10, 20, 20, 50)]

#VARYING NETWORK SIZE :    
graph_param_list = [
        graphObject(500, 5, 10, 5, 10),
        graphObject(1500, 10, 20, 20, 50),
        graphObject(2500, 10, 20, 20, 50),
        graphObject(5000, 10, 20, 20, 50),
        graphObject(10000, 10, 20, 20, 50)
        ]
networkSizeList = [500,1500,2500,5000,10000]


   
#One graph for mu variation 
graph_param_list_mu = [
        graphObject(2500, 10, 20, 20, 50)
        ]
mu_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

#fractional coverage
radius = 5
