#!/usr/bin/env python
import openpnl
import numpy as np
np.random.seed(1337)
# Still broken ...

print " *** SET UP MODEL **"
model = openpnl.pnlExCreateRndArHMM()
model.GetGraph().Dump()
pArHMM = openpnl.CDBN_Create(model)
pInfEng = openpnl.C1_5SliceJtreeInfEngine_Create(pArHMM)

# generate random slices
print " *** SET UP RANDOM SLICES  **"
nTimeSeries = 500
nSlices = np.random.randint(3,20,nTimeSeries);
print nSlices

print " *** GENERATE SAMPLES *** "
evidencesOut = pArHMM.GenerateSamples2( nSlices );
pDBN = openpnl.CDBN.Create(openpnl.pnlExCreateRndArHMM());
print evidencesOut 
print pDBN

print " *** LEARNING *** "
pLearn = openpnl.CEMLearningEngineDBN.Create( pDBN );
pLearn.SetData(evidencesOut)
pLearn.Learn()

print " *** model before learning ... "
for i in range(0,4):
    pCPD1 = pArHMM.GetFactor(i)
    pMat = pCPD1.GetMatrix(openpnl.matTable)
    cpd = openpnl.convertVector(pMat.ConvertToDense().GetVector())
    print cpd
    
print " *** model after learning ... "
for i in range(0,4):
    pCPD2 = pDBN.GetFactor(i)
    pMat = pCPD2.GetMatrix(openpnl.matTable)
    cpd = openpnl.convertVector(pMat.ConvertToDense().GetVector())
    print cpd


