import sys
sys.path.append('../')
import imports
from imports import *
from graph_generator import generator

def label_propagation(graph):
    return algorithms.label_propagation(graph)

def leiden(graph):
    return algorithms.leiden(graph)

def greedy_modularity(graph):
    return algorithms.greedy_modularity(graph)

def infomap(graph):
    return algorithms.infomap(graph)

def louvain(graph):
    return algorithms.louvain(graph)

def walktrap(graph):
    return algorithms.walktrap(graph)

def girvan_newman(graph):
    return algorithms.girvan_newman(graph,1)

cd_function_list = [label_propagation,leiden,greedy_modularity,infomap,louvain,walktrap,girvan_newman]



# ####################################
# ######         USAGE          ######
# ####################################
# for obj in generator.graph_param_list:
#     graphObjects = obj.setGraphObject()
#     for graph in graphObjects:
#         print(graph.number_of_nodes())
#         for func in cd_function_list:
#             print(len(func(graph).communities))
        