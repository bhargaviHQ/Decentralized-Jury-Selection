import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# from google.cloud import bigquery
# from google.cloud import storage
import io
import time
import networkx as nx
# from google.cloud import bigquery
import matplotlib.pyplot as plt
# import community as community_louvain
import matplotlib.cm as cm
# import igraph as ig
# import leidenalg as la
import csv
import numpy as np
from cdlib import algorithms, viz
import statistics

from cdlib import algorithms as al
from cdlib import ensemble as en
from cdlib import evaluation as ev
import networkx as nx
from cdlib import evaluation
from networkx.generators.community import LFR_benchmark_graph
from cdlib import NodeClustering
import math
from itertools import chain
# from community import community_louvain
from prettytable import PrettyTable
from networkit import *  
import networkit as nk 
import random
import seaborn as sns

import timeit

import pickle
import psutil