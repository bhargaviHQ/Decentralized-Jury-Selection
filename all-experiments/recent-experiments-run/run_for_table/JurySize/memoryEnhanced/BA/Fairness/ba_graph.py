import sys
sys.path.append('../../../')
import imports
from imports import *

from graph_generator import generator

nk.engineering.setNumberOfThreads(32)

G1 = nk.generators.BarabasiAlbertGenerator(1,10000).generate()

lfr = nk.generators.LFRGenerator(10000)
lfr.generatePowerlawDegreeSequence(50, 100, -3)
lfr.generatePowerlawCommunitySizeSequence(50, 100, -1.5)
lfr.setMu(0.1)
lfrG = lfr.generate()


nk.overview(G1)
nk.overview(lfrG)

erg = nk.generators.ErdosRenyiGenerator(10000, 0.2)
ergG = erg.generate()
