#!/usr/bin/env python
import openpnl
#print dir(openpnl)

model = openpnl.pnlExCreateRndArHMM()
#model = openpnl.pnlExCreateKjaerulfsBNet()

pArHMM = openpnl.CDBN_Create(model)
pInfEng = openpnl.C1_5SliceJtreeInfEngine_Create(pArHMM)
nTimeSlices = 5

# set up evidence ...
pEvidences = openpnl.newCEvidences(nTimeSlices)
for i in range(0,nTimeSlices):
    ev = openpnl.mkEvidence( pArHMM, [1], [1.0] );
    openpnl.assignEvidence( pEvidences, ev, i )

pInfEng.DefineProcedure(openpnl.ptSmoothing, nTimeSlices)
pInfEng.EnterEvidence(pEvidences, nTimeSlices)
pInfEng.Smoothing()

queryPrior = [0]
#queryPrior = openpnl.intVector([0])
queryPriorSize = 1
slice_ = 0

pInfEng.MarginalNodes(queryPrior, queryPriorSize, slice_)
pQueryJPD = pInfEng.GetQueryJPD();

mdl = pQueryJPD.GetModelDomain()
mat = pQueryJPD.GetMatrix(openpnl.matTable)

print openpnl.convertVector(mat.ConvertToDense().GetVector())


