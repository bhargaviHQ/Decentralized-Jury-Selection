import sys
sys.path.append('../../../../../../')
import imports
from imports import *

from graph_generator import generator


erg = nk.generators.ErdosRenyiGenerator(15000,0.3)
ergG = erg.generate()

nk.overview(ergG)
