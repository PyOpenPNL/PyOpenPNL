#!/usr/bin/env python

import openpnl
import numpy as np

# number of random example rows to generate
n_ex = 128

# Each item in this list is one node, the value represents the cardinality of the node variable
nodeOrds = [10,7,3,4,2]

###### Make Example BNet #######

bn = openpnl.pnlExCreateWaterSprinklerBNet();

# Make a random BN which complies to this node structure
bn = openpnl.mkSkelBNet(nodeOrds)

########## FABRICATE EVIDENCE ##########

# set up some evidence data
ev = np.zeros([n_ex,len(nodeOrds)], dtype='int32')
for i in range(0,n_ex):
    for j in range(0,len(nodeOrds)):
        ev[i,j] = np.random.randint(0,nodeOrds[j])

########## DAG LEARNING #################

# Allocate a structure learner for this BN
sl = openpnl.mkCMlStaticStructLearnHC(bn)

# set the evidence into the learner for learning
sl.SetPyData(bn, ev)
# do the structure learning ...
sl.Learn();

# Print learned dependencies 
print "Learned BN DAG structure dependencies..."
dag = sl.GetResultDAG();
dag.Dump();

############# CPD LEARNING ###############

# Set up EM CPD Learner
pl = openpnl.CEMLearningEngine.Create(bn)

# Set evidence to learn on
pl.SetPyData(bn, ev)

# Learn CPDsa
pl.Learn()

################# DAG INFERENCE ###########

infeng = openpnl.CNaiveInfEngine.Create( bn )

nodes = [0,3,4]
vals  = [2,3,1]
a = np.vstack([nodes,vals]).astype('int32')
print a

infeng.enterEvidence(bn, a)
infeng.sampleNodes([1,2])

infeng.sampleNodes([1])
infeng.sampleNodes([2])



