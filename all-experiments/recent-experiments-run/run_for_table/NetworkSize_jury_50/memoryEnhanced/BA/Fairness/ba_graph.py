import sys
sys.path.append('../../../../../../')
import imports
from imports import *

from graph_generator import generator


G1 = nk.generators.BarabasiAlbertGenerator(3,15000).generate()
G2 = nk.generators.BarabasiAlbertGenerator(2,5000).generate()


nk.overview(G1)
print("-------------------------------------")
print("-------------------------------------")
nk.overview(G2)
print("-------------------------------------")
print("-------------------------------------")

lfr1 = nk.generators.LFRGenerator(15000)
lfr1.generatePowerlawDegreeSequence(50, 250, -3)
lfr1.generatePowerlawCommunitySizeSequence(50, 250, -1.5)
lfr1.setMu(0.2)
lfrG1 = lfr1.generate()


lfr2 = nk.generators.LFRGenerator(5000)
lfr2.generatePowerlawDegreeSequence(25, 50, -3)
lfr2.generatePowerlawCommunitySizeSequence(25, 100, -1.5)
lfr2.setMu(0.2)
lfrG2 = lfr2.generate()

nk.overview(lfrG1)
print("-------------------------------------")
print("-------------------------------------")
nk.overview(lfrG2)
print("-------------------------------------")
print("-------------------------------------")

erg1 = nk.generators.ErdosRenyiGenerator(15000,0.2)
erg2 = nk.generators.ErdosRenyiGenerator(5000,0.1)
ergG1 = erg1.generate()
ergG2 = erg2.generate()

nk.overview(ergG1)
print("-------------------------------------")
print("-------------------------------------")
nk.overview(ergG2)
print("-------------------------------------")
print("-------------------------------------")

# import sys
# sys.path.append('../../../../')
# import imports
# from imports import *

# from graph_generator import generator

# graphETH = pickle.load(open("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/ETH/eth_graphobj.pickle", 'rb'))
# G = nk.nxadapter.nx2nk(graphETH, weightAttr=None)
# nk.overview(G)