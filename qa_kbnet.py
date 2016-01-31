#!/usr/bin/env python
import sys
sys.path.append(".")
import openpnl
import networkx
import matplotlib.pyplot as plt
import numpy as np


nnodes = 11

# set up the graph
dag = np.zeros([nnodes,nnodes], dtype=np.int32)
print dag.shape
# Dag must be square, with zero diag!
dag[0,1] = 1
dag[3,6] = 1
print dag
pGraph = openpnl.CGraph.CreateNP(dag)

# set up the nodes
types = map(lambda x: openpnl.CNodeType(), range(0,nnodes))

types =  openpnl.pnlNodeTypeVector(nnodes)

nA = [0]*nnodes;
nA[0] = 0; nA[1] = 0; nA[2] = 3;
nodeAssoc = openpnl.toConstIntVector(nA)

print type(nnodes), type(types), type(nodeAssoc), type(pGraph)
print nnodes, types, nodeAssoc, pGraph
pBNet = openpnl.CBNet.Create( nnodes, types, nodeAssoc, pGraph )





