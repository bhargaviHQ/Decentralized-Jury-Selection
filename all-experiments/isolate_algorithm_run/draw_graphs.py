import sys
sys.path.append('../')
import imports
from imports import *

from graph_generator import generator
import seaborn as sns

nk.engineering.setNumberOfThreads(32)
from algorithm_repository_networkit import greedy_Betweenness
from algorithm_repository_networkit import greedy_coverage
from algorithm_repository_networkit import Prob_Betweenness
from algorithm_repository_networkit import Prob_Coverage
from algorithm_repository_networkit import random_select
from algorithm_repository_networkit import RCL_Betweenness
from algorithm_repository_networkit import RCL_coverage
from algorithm_repository_networkit import Seed_Betweenness
from algorithm_repository_networkit import Seed_Coverage

from metrics.Fairness import equality_of_selection
from metrics.Measure_of_Spread.Diversity import overlapping_coverage

#returns the sum of minimum distance
#of all unselected nodes to selected nodes

class graphObject:
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = 1
        self.probability = 0.1
 
    def getParams (self):
        print("Nodes : ", self.nodes, " edges : ",self.edges)

    def graphGeneratorBA(self,n):
        # Create the powerlaw-clustered network
        # G = nx.barabasi_albert_graph(self.nodes,self.edges)
        G = nk.generators.BarabasiAlbertGenerator(self.edges,n).generate()
        return G

    def graphGeneratorLFR(self,n):
        lfr = nk.generators.LFRGenerator(n)
        lfr.generatePowerlawDegreeSequence(5, 10, -2.5)
        lfr.generatePowerlawCommunitySizeSequence(5, 10, -1)
        lfr.setMu(0.2)
        lfrG = lfr.generate()
        return lfrG
    def graphGeneratorER(self,n):
        erg = nk.generators.ErdosRenyiGenerator(n, self.probability)
        ergG = erg.generate()
        return ergG

graph_param = [
        # graphObject(25),
        graphObject(50)
        ]
it = 0
size = 0
for obj in graph_param:      
    size = 50
    graphBA = obj.graphGeneratorBA(size)  

    graphLFR = obj.graphGeneratorLFR(size) 

    graphER = obj.graphGeneratorER(size) 

    G_nxba = nk.nxadapter.nk2nx(graphBA)
    pos = nx.spring_layout(G_nxba)
    nx.draw(G_nxba, pos, with_labels=False,node_size=50, font_size=5)
    print("Size : ",size, " --> number of nodes : ",G_nxba.number_of_nodes())
    plt.title('Networkit Graph Visualization Barabási - Albert n={}'.format((size)))
    plt.savefig("newtmp/BA_plt_"+str(size)+"_fig.jpg")

    # G_nxlfr = nk.nxadapter.nk2nx(graphLFR)
    # pos = nx.spring_layout(G_nxlfr)
    # nx.draw(G_nxlfr, pos, with_labels=False,node_size=50, font_size=5)
    # plt.title('Networkit Graph Visualization LFR n={}'.format((size)))
    # plt.savefig("newtmp/LFR_plt_"+str(size)+"_fig.jpg")
    # print("Size : ",size, " --> number of nodes : ",G_nxlfr.number_of_nodes())

    # G_nxlER = nk.nxadapter.nk2nx(graphER)
    # pos = nx.spring_layout(G_nxlER)
    # nx.draw(G_nxlER, pos, with_labels=False,node_size=50, font_size=5)
    # plt.title('Networkit Graph Visualization ER n={}'.format((size)))
    # plt.savefig("newtmp/ER_plt_"+str(size)+"_fig.jpg")
    # print("Size : ",size, " --> number of nodes : ",G_nxlER.number_of_nodes())
    # it = it + 1