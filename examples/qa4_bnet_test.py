#!/usr/bin/env python
import sys
sys.path.append(".")
import openpnl
import networkx
import matplotlib.pyplot as plt

nnodes = 26
G = networkx.gn_graph(nnodes)
mp = {}
for i in range(0,nnodes):
    mp[i+1] = chr(ord('A')+i-1)
G = networkx.relabel_nodes(G, mp)
networkx.draw(G)
plt.show()



pWSBnet = openpnl.pnlExCreateWaterSprinklerBNet()
pWSBnet.GetGraph().Dump();

pEvidForWS = openpnl.mkEvidence( pWSBnet, [0], [1] )
pNaiveInf = openpnl.CNaiveInfEngine.Create( pWSBnet )
pNaiveInf.EnterEvidence( pEvidForWS );

nodes = [1,3]
pNaiveInf.MarginalNodes( nodes );

pMarg = pNaiveInf.GetQueryJPD()

obsVls = openpnl.pConstValueVector()
#print obsVls
#pEvidForWS.GetObsNodesWithValues( openpnl.toIntVector(nodes), obsVls )


print openpnl.convertVector( pMarg.GetMatrix(openpnl.matTable).ConvertToDense().GetVector() )


