
import networkx as nx
from google.cloud import bigquery
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import csv
import numpy as np
import pickle
##
# For differnt values of K 
##
class GraphVisualization:
         
    def __init__(self):
        self.visual = []
          
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)

        # save graph object to file
        pickle.dump(G, open('eth_graphobj.pickle', 'wb'))

        # load graph object from file
        Graph1 = pickle.load(open('eth_graphobj.pickle', 'rb'))
        print(Graph1.number_of_edges())
        # pos = nx.spring_layout(Graph1,k=0.0005)
        # nx.draw_networkx_edges(Graph1, pos, alpha=0.2)
        # plt.show()
    
G = GraphVisualization()


# Read from file 
with open("eth_data.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
     G.addEdge(row[0] , row[1])

G.visualize()