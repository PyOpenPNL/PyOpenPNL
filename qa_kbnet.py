#!/usr/bin/env python
import sys
sys.path.append(".")
import openpnl
import networkx
import matplotlib.pyplot as plt
import numpy as np

print dir(openpnl.pnlNodeTypeVector)
nnodes = 11

# set up the graph
dag = np.zeros([nnodes,nnodes], dtype=np.int32)
print dag.shape
# Dag must be square, with zero diag!
dag[0,1] = 1
dag[3,6] = 1
print dag
pGraph = openpnl.CGraph.CreateNP(dag)

# set up the node types
types =  openpnl.pnlNodeTypeVector()
types.resize(nnodes)
isDiscrete = 1
types[0].SetType( isDiscrete, 3 )
types[1].SetType( isDiscrete, 16 )
types[2].SetType( isDiscrete, 2 )
types[3].SetType( isDiscrete, 10 )
types[4].SetType( isDiscrete, 6 )
types[5].SetType( isDiscrete, 4 )

# node associations
nA = [0]*nnodes;
nA[0] = 0; nA[1] = 0; nA[2] = 3;
nodeAssoc = openpnl.toConstIntVector(nA)


print "make bnet ... "
pBNet = openpnl.CBNet.Create( nnodes, types, nodeAssoc, pGraph )





