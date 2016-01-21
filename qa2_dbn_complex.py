#!/usr/bin/env python
import openpnl
import numpy as np
# Still broken ...

print " *** SET UP MODEL **"
model = openpnl.pnlExCreateRndArHMM()
pArHMM = openpnl.CDBN_Create(model)
pInfEng = openpnl.C1_5SliceJtreeInfEngine_Create(pArHMM)

# generate random slices
print " *** SET UP RANDOM SLICES  **"
nTimeSeries = 500
nSlices = np.random.randint(3,20,nTimeSeries);

print " *** GENERATE SAMPLES *** "
evidencesOut = pArHMM.GenerateSamples2( nSlices );

pDBN = openpnl.CDBN.Create(openpnl.pnlExCreateRndArHMM());
pLearn = openpnl.CEMLearningEngineDBN.Create( pDBN );
pLearn.SetData(evidencesOut)
print " *** LEARNING *** "
pLearn.Learn()

for i in range(0,4):
    pCPD1 = pArHMM.GetFactor(i)
    pMat = pCPD1.GetMatrix(openpnl.matTable)
    print pMat
#    print pMat.GetRawData()

    
