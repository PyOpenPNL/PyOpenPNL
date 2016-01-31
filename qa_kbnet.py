#!/usr/bin/env python
import sys
sys.path.append(".")
import openpnl
import networkx
import matplotlib.pyplot as plt
import numpy as np

nnodes = 4

# set up the graph
# Dag must be square, with zero diag!
dag = np.zeros([nnodes,nnodes], dtype=np.int32)
dag[0,[1,2]] = 1
dag[2,3] = 1
dag[1,3] = 1
pGraph = openpnl.CGraph.CreateNP(dag)
print dag

# set up the node types
types =  openpnl.pnlNodeTypeVector()
types.resize(nnodes)
isDiscrete = 1
types[0].SetType( isDiscrete, 2 )
types[1].SetType( isDiscrete, 2 )
types[2].SetType( isDiscrete, 2 )
types[3].SetType( isDiscrete, 4 )

# node associations
nA = [0]*nnodes;
nA[0] = 0; nA[1] = 0; nA[2] = 3;
nodeAssoc = openpnl.toConstIntVector(nA)

# make the bayes net ...
pBNet = openpnl.CBNet.Create( nnodes, types, nodeAssoc, pGraph )

for (node, cpdvals) in [
    (0, [0.5,0.5]),
    (1, [0.8, 0.2, 0.2, 0.8]),
    (2, [0.5, 0.9, 0.5, 0.1]),
    (3, [1, 0.1, 0.1, 0.01, 0, 0.9, 0.9, 0.99])]:

    md = openpnl.CModelDomain.Create( 1 )
    tba = openpnl.mkCMatrixF1( np.array( cpdvals, dtype=np.float32 ) )
    cf = openpnl.CTabularCPD.Create( md, openpnl.toConstIntVector([node]), tba)
    pBNet.AttachFactor(cf)



