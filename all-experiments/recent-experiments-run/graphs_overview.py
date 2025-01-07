import sys
sys.path.append('../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(8)


graphETH = pickle.load(open("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/ETH/eth_graphobj.pickle", 'rb'))
G1 = nk.nxadapter.nx2nk(graphETH, weightAttr=None)

nk.overview(G1)
print("**********************")

Gfb = nk.readGraph("/home/bhargavi/research_code_run/newcodes/October2023/run_with_memory/SFB/facebook_combined.txt",nk.Format.SNAP)

nk.overview(Gfb)


G1 = nk.generators.BarabasiAlbertGenerator(3,10000).generate()
G1500 = nk.generators.BarabasiAlbertGenerator(2,500).generate()

lfr = nk.generators.LFRGenerator(10000)
lfr.generatePowerlawDegreeSequence(50, 100, -3)
lfr.generatePowerlawCommunitySizeSequence(50, 100, -1.5)
lfr.setMu(0.1)
lfrG = lfr.generate()


lfr500 = nk.generators.LFRGenerator(500)
lfr500.generatePowerlawDegreeSequence(20, 50, -3)
lfr500.generatePowerlawCommunitySizeSequence(10, 50, -1.5)
lfr500.setMu(0.3)
lfrG500 = lfr500.generate()

ergG = nk.generators.ErdosRenyiGenerator(10000, 0.2).generate()
ergG500 = nk.generators.ErdosRenyiGenerator(500, 0.01).generate()

print("BA - ")
nk.overview(G1)
print("**********************")
print("BA 500 - ")
nk.overview(G1500)
print("**********************")
print("LFR - ")
nk.overview(lfrG)
print("**********************")
print("LFR 500 - ")
nk.overview(lfrG500)
print("**********************")
print("ER - ")
nk.overview(ergG)
print("**********************")
print("ER 500 - ")
nk.overview(ergG500)
print("**********************")

