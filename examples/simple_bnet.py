#!/usr/bin/env python
import sys
sys.path.append(".")
import openpnl
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# ** Set up the BNet/DBN
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
types[3].SetType( isDiscrete, 2 )

# node associations
nodeAssoc = openpnl.toConstIntVector([0]*nnodes)

# make the bayes net ...
pBNet = openpnl.CBNet.Create( nnodes, types, nodeAssoc, pGraph )
pBNet.AllocFactors()

for (node, cpdvals) in [
    (0, [0.5,0.5]),
    (1, [0.8, 0.2, 0.2, 0.8]),
    (2, [0.5, 0.5, 0.9, 0.1]),
    (3, [1, 0, 0.1, 0.9, 0.1, 0.9, 0.01, 0.99]),
    ]:

    parents = pGraph.GetParents(node);
    print "node: ", node, " parents: ", parents
    domain = list(parents) + [node]
    cCPD = openpnl.CTabularCPD.Create( pBNet.GetModelDomain() , openpnl.toConstIntVector(domain) )
    cCPD.AllocMatrix( cpdvals, openpnl.matTable )
    cCPD.NormalizeCPD()
    pBNet.AttachFactor(cCPD)


# Set up the inference engine
infEngine = openpnl.CPearlInfEngine.Create( pBNet );

# Problem 1 P(W|C=0)
ev = openpnl.mkEvidence( pBNet, [0], [0] )
infEngine.EnterEvidence(ev)
infEngine.pyMarginalNodes( [3], 0 )
infEngine.GetQueryJPD().Dump()
m = openpnl.convertVector(infEngine.GetQueryJPD().GetMatrix(openpnl.matTable).ConvertToDense().GetVector())
index = np.arange(0,2,1)
plt.figure()
plt.bar(index, m)
plt.title("Marginal of P(WetGrass|Cloudy=False)")
plt.ylabel("P(WetGress = x)");
plt.xticks(index+0.5, ('WetGrass=False', "WetGrass=True"))


# Problem 1 P(W|C=1)
ev = openpnl.mkEvidence( pBNet, [0], [1] )
infEngine.EnterEvidence(ev)
infEngine.pyMarginalNodes( [3], 0 )
infEngine.GetQueryJPD().Dump()
m = openpnl.convertVector(infEngine.GetQueryJPD().GetMatrix(openpnl.matTable).ConvertToDense().GetVector())
plt.figure()
plt.bar(index, m)
plt.title("Marginal of P(WetGrass|Cloudy=True)")
plt.ylabel("P(WetGress = x)");
plt.xticks(index+0.5, ('WetGrass=False', "WetGrass=True"))


# Visualization ... 
plt.figure()
l = {0:"Cloudy",1:"Rain",2:"Sprinkler",3:"WetGrass"}
D = nx.DiGraph(dag, labels=l)
v = nx.draw(D, labels=l)
plt.show()

