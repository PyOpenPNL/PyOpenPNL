#!/usr/bin/env python
import openpnl
print dir(openpnl)

model = openpnl.pnlExCreateRndArHMM()
#model = openpnl.pnlExCreateKjaerulfsBNet()

pArHMM = openpnl.CDBN_Create(model)
pInfEng = openpnl.C1_5SliceJtreeInfEngine_Create(pArHMM)

nTimeSlices = 5
#pEvidences = openpnl.CEvidence()

pInfEng.DefineProcedure(openpnl.ptSmoothing, nTimeSlices)
#pInfEng.EnterEvidence(pEvidences, nTimeSlices)
#pInfEng.Smoothing()

queryPrior = openpnl.intVector([0])
queryPriorSize = 1
slice_ = 0

#pInfEng.MarginalNodes(queryPrior, queryPriorSize, slice_)
#pQueryJPD = pInfEng.GetQueryJPD();


