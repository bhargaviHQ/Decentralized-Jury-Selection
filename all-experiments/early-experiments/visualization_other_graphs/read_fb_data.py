from networkit import *  
import networkit as nk 
G = nk.readGraph("facebook_combined.txt",nk.Format.SNAP)
print(G.numberOfNodes(), G.numberOfEdges())