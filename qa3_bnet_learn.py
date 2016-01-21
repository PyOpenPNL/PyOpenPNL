#!/usr/bin/env python
import openpnl

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


