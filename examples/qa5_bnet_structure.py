#!/usr/bin/env python

import openpnl
import numpy as np

n_ex = 128
nodeOrds = [10,7,3,4,2]

bn = openpnl.mkSkelBNet(nodeOrds)
sl = openpnl.mkCMlStaticStructLearnHC(bn)

# set up some evidence data
ev = np.zeros([n_ex,len(nodeOrds)], dtype='int32')
for i in range(0,n_ex):
    for j in range(0,len(nodeOrds)):
        ev[i,j] = np.random.randint(0,nodeOrds[j])

# set data to the learner ..
sl.SetPyData(bn, ev)
# do the structure learning ...
sl.Learn();

# Print learned dependencies 
print "Learned structure dependencies..."
dag = sl.GetResultDAG();
dag.Dump();


