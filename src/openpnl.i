%module openpnl

%{
#include "pnlConfig.hpp"
#include "pnlTypeDefs.hpp"
#include "pnlObject.hpp"
#include "pnlVector.hpp"
#include "pnlMatrix.hpp"
#include "pnlGraph.hpp"
#include "pnlDAG.hpp"
#include "pnlGraphicalModel.hpp"
#include "pnlStaticGraphicalModel.hpp"
#include "pnlDynamicGraphicalModel.hpp"
#include "pnlEvidence.hpp"
#include "pnlNodeValues.hpp"
#include "pnl2DBitwiseMatrix.hpp"
#include "pnlMatrix.hpp"
#include "pnlFactors.hpp"
#include "pnlDBN.hpp"
#include "pnlExampleModels.hpp"
#include "pnl1_5SliceJtreeInferenceEngine.hpp"
#include "pnlIDPotential.hpp"
#include "pnlExInferenceEngine.hpp"
#include "pnlEmLearningEngineDBN.hpp"
#include "pnlEmLearningEngine.hpp"
#include "pnlNodeType.hpp"
#include "pnlTabularCPD.hpp"
#include "pnlBKInferenceEngine.hpp"
#include "pnlPearlInferenceEngine.hpp"
#include "pnlJunctionTree.hpp"
#include "pnlJtreeInferenceEngine.hpp"
#include "pnlMlStaticStructLearnHC.hpp"
#include "pnlMlStaticStructLearn.hpp"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"
%include "std_vector.i"
%include "numpy.i"
%init %{
import_array();
%}

%numpy_typemaps(double, NPY_DOUBLE, int)
%numpy_typemaps(float,  NPY_FLOAT, int)
%numpy_typemaps(int,    NPY_INT   , int)

%define PNL_API
%enddef

%template(floatVector)  ::std::vector<float>;
%template(intVector)    ::std::vector<int>;
%template(intVecVector) ::std::vector< std::vector< int > >;


namespace pnl {

  class CPNLBase
  {
    protected:
      CPNLBase();
  };
  class Value
  {
    public:
      int   GetInt() const { return m_tVal; }
      float GetFlt() const { return m_cVal; }
      void SetInt(int v)     { m_tVal = v; m_cVal = float(v); m_bInt = true; }
      void SetFlt(float v)   { m_tVal = int(v);   m_cVal = v; m_bInt = false; }
      void SetUnknownAsFlt(float v) { m_tVal = int(v); m_cVal = v; m_bInt = 2; }
      Value( int v ):   m_bInt(true),  m_tVal(v), m_cVal(float(v)) {}
      Value( float v ): m_bInt(false), m_tVal(int(v)), m_cVal(v) {}
   };
};

%include "pnlConfig.hpp"
%include "pnlVector.hpp"
%include "pnlTypeDefs.hpp"
%include "pnlMatrix.hpp"
%include "pnlNodeValues.hpp"
%include "pnl2DBitwiseMatrix.hpp"
%include "pnlReferenceCounter.hpp"
%include "pnlMatrix.hpp"
%include "pnlMatrixIterator.hpp"
%template(pnlCMatrixf)  pnl::CMatrix< float >;
%template(pnlCMatrixi)  pnl::CMatrix< int >;
%include "pnlDenseMatrix.hpp"
%template(pnlDenseMatrixF) pnl::CDenseMatrix<float>;
%template(pnlDenseMatrixI) pnl::CDenseMatrix<int>;
%include "pnlNumericDenseMatrix.hpp"
%include "pnlModelTypes.hpp"
%include "pnlModelDomain.hpp"
%include "pnlFactor.hpp"
%include "pnlFactors.hpp"
%include "pnlIDPotential.hpp"
%include "pnlPotential.hpp"
%include "pnlObject.hpp"
%include "pnlNodeType.hpp"
%template(foo12345) std::vector< pnl::CNodeType,pnl::GeneralAllocator< pnl::CNodeType > >;
%template(foo123456) std::vector< pnl::Value const *,pnl::GeneralAllocator< pnl::Value const * > >;
%template(pnlNodeTypeVector) pnl::pnlVector< pnl::CNodeType>;
%include "pnlCPD.hpp"
%include "pnlTabularCPD.hpp"
%include "pnlGraph.hpp"
%include "pnlDAG.hpp"
%include "pnlGraphicalModel.hpp"
%include "pnlStaticGraphicalModel.hpp"
%include "pnlDynamicGraphicalModel.hpp"
%include "pnlEvidence.hpp"
%include "pnlDBN.hpp"
%include "pnlBNet.hpp"
%include "pnlMNet.hpp"
%include "pnlMRF2.hpp"
%include "pnlExInferenceEngine.hpp"
%include "pnlExampleModels.hpp"
%include "pnlDynamicInferenceEngine.hpp"
%include "pnl2TBNInferenceEngine.hpp"
%include "pnl1_5SliceInferenceEngine.hpp"
%include "pnl1_5SliceJtreeInferenceEngine.hpp"
%include "pnlLearningEngine.hpp"
%include "pnlDynamicLearningEngine.hpp"
%include "pnlEmLearningEngineDBN.hpp"
%include "pnlEmLearningEngine.hpp"
%include "pnlInferenceEngine.hpp"
%include "pnlNaiveInferenceEngine.hpp"
%include "pnlBKInferenceEngine.hpp"
%include "pnlPearlInferenceEngine.hpp"
%include "pnlMlStaticStructLearn.hpp"
%include "pnlMlStaticStructLearnHC.hpp"


namespace pnl {
    %template(floatVectorPNLAlloc) ::std::vector< float,pnl::GeneralAllocator< float > >;
    %template(floatVectorPNLAlloc2) ::pnl::pnlVector< float,pnl::GeneralAllocator< float > >;
    %template(valueVector) ::std::vector<pnl::Value>;
    %template(floatVectorPNL) ::pnl::pnlVector<float>;
    %template(pEvidencesVecVectorCrazyAllocator) ::std::vector< pnl::pnlVector< pnl::CEvidence *,pnl::GeneralAllocator< pnl::CEvidence * > >,pnl::GeneralAllocator< pnl::pnlVector< pnl::CEvidence *,pnl::GeneralAllocator< pnl::CEvidence * > > > >;

    %template(pEvidencesVecVector) ::pnl::pnlVector< pEvidencesVector>;
    %template(pConstValueVector)   ::pnl::pnlVector< const Value*>;
    %extend CDynamicInfEngine
    {
        void MarginalNodes(std::vector<int> iv,int n1,int n2){
            pnl::intVector v(iv.begin(), iv.end());
            self->pnl::CDynamicInfEngine::MarginalNodes(v,n1,n2);
        }
    }
    %extend pnlDenseMatrix<float>
    {
        std::vector<float> getVector(){
            int nEl;
            const float* data;
            pnlDenseMatrixF_GetRawData(nEl, data);
            std::vector<float> v;
            v.assign(data, data+nEl)
            return v;
        }
    }
    %extend CDBN
    {
        pnl::pEvidencesVecVector GenerateSamples2(std::vector<int> ns){
            const pnl::intVector iv(&ns[0], &ns[ns.size()]);
            pnl::pEvidencesVecVector pvv;
            self->GenerateSamples(&pvv,iv);
            return pvv;
        }
    }



    %extend CNaiveInfEngine
    {
        void MarginalNodes( std::vector<int> queryNds ){
            self->MarginalNodes( (const int*) &queryNds[0], queryNds.size() );
        }
        void enterEvidence( const CBNet* bn, int DIM1, int DIM2, int* IN_ARRAY2 ){
            if(not (DIM1 == 2)){
                throw std::runtime_error("DIM1 must be 2, (nodes, vals)!");
            }
            int nObsNds = DIM2;
            int *obsNds = new int[DIM2];
            pnl::valueVector obsVals;
            obsVals.resize(nObsNds);
            for(int i=0; i<nObsNds; i++){
                obsNds[i] = IN_ARRAY2[i];
                obsVals[i] = IN_ARRAY2[i+DIM2];
                }
            pnl::CEvidence* pEvid = pnl::CEvidence::Create(bn, nObsNds, obsNds, obsVals );
            self->EnterEvidence(pEvid);
        }

        PyObject* sampleNodes( int DIM1, int* IN_ARRAY1){
            self->MarginalNodes( IN_ARRAY1, DIM1 );
            const pnl::CPotential* pMarg = self->GetQueryJPD();
            
            int nnodes;
            const int * domain;

            pMarg->GetDomain( &nnodes, &domain );

            pnl::CMatrix<float>* pMat = pMarg->GetMatrix(pnl::matTable);

            int nEl;
            const float* data;
            static_cast<pnl::CNumericDenseMatrix<float>*>(pMat)->GetRawData(&nEl, &data);

            int nd = 1;
            npy_intp * dims = new npy_intp[1];
            dims[0] = nEl;
            
            PyObject *obj = PyArray_SimpleNewFromData(nd, dims, NPY_FLOAT32, (void*)data);
            return obj;
        }
    }
    %extend CGraph
    {
        static CGraph* CreateNP( int* IN_ARRAY2, int DIM1, int DIM2 ){
            int dims[2]; dims[0] = DIM1; dims[1] = DIM2; int clamp = 0;
            pnl::CMatrix<int> *m = pnl::CDenseMatrix<int>::Create( 2, dims, IN_ARRAY2, clamp );
            pnl::CGraph* a = pnl::CGraph::Create(m);
            return a;
        }
        std::vector<int> GetParents(int node){
            pnl::intVector v;
            self->GetParents(node, &v);
            return std::vector<int>(&v[0], &v[v.size()]);
        }
    }
    %extend CFactor
    {
        void AllocMatrix( std::vector<float> data, EMatrixType mType ){
            self->AllocMatrix( (const float*) &data[0], mType);
        }
    }
    %extend CInfEngine
    {
        void pyMarginalNodes( std::vector<int> nodes, int notExpandJPD = 0 ){
            const pnl::intVector iv(&nodes[0], &nodes[nodes.size()]);
            self->MarginalNodes( iv, notExpandJPD );
        }
    }
    %extend CDynamicInfEngine
    {

        void pyMarginalNodes( std::vector<int> nodes, int time, int notExpandJPD = 0 ){
            const pnl::intVector iv(&nodes[0], &nodes[nodes.size()]);
            self->MarginalNodes(iv, time, notExpandJPD);
        }
    }

    %extend CMlStaticStructLearnHC
    {
        void SetPyData( pnl::CBNet* pBNet, int* IN_ARRAY2, int DIM1, int DIM2 ){
          int nEv = DIM1;
          int nnodes = DIM2; // TODO: make sure this matches model nnodes
          pnl::CEvidence **pEvidences = new pnl::CEvidence *[nEv];
          int* obs_nodes = new int[nnodes];
          for(int i=0; i<nnodes; i++){
            obs_nodes[i] = i;
            }
          pnl::valueVector input_data;
          input_data.resize(nnodes);

          // make a pEvidence for each example
          for(int i=0; i<nEv; i++){
            for(int j=0; j<nnodes; j++){
              input_data[j].SetInt(IN_ARRAY2[i*DIM2+j]);
            }
            pEvidences[i] = pnl::CEvidence::Create(pBNet, nnodes, obs_nodes, input_data);
          }
          // pass pEvidences to learner setData
          self->SetData(nEv, pEvidences);
        }
    }

    // return 2D Numpy adjacency matrix 
    %extend CDAG 
    {
        // return a 2D adjacency matrix as a 1D flattened matrix 
        // TODO: return this as a proper 2D matrix ...
        void adjMatrix(int DIM1, int* ARGOUT_ARRAY1){
            int h = self->m_pAncesstorMatrix->GetHeight();
            int w = self->m_pAncesstorMatrix->GetWidth();
 
            // set the output from our internal array
            for(int i=0; i<h; i++){
                for(int j=0; j<w; j++){
                    if(self->m_pAncesstorMatrix->GetValue(i, j)){
                        ARGOUT_ARRAY1[j+i*w] = 1;
                    } else {
                        ARGOUT_ARRAY1[j+i*w] = 0;
                    }
                }
            }
        }
    }

    %extend CEMLearningEngine
    {
        void SetPyData( pnl::CBNet* pBNet, int* IN_ARRAY2, int DIM1, int DIM2 ){
          int nEv = DIM1;
          int nnodes = DIM2; // TODO: make sure this matches model nnodes
          pnl::CEvidence **pEvidences = new pnl::CEvidence *[nEv];
          int* obs_nodes = new int[nnodes];
          for(int i=0; i<nnodes; i++){
            obs_nodes[i] = i;
            }
          pnl::valueVector input_data;
          input_data.resize(nnodes);

          // make a pEvidence for each example
          for(int i=0; i<nEv; i++){
            for(int j=0; j<nnodes; j++){
              input_data[j].SetInt(IN_ARRAY2[i*DIM2+j]);
            }
            pEvidences[i] = pnl::CEvidence::Create(pBNet, nnodes, obs_nodes, input_data);
          }
          // pass pEvidences to learner setData
          self->SetData(nEv, pEvidences);
        }
    }
}

/*
 *  Python SWIG Helper Functions
 */
%inline %{

pnl::CMatrix<float>* mkCMatrixF2( float* IN_ARRAY2, int DIM1, int DIM2 ){
    int dims[2]; dims[0] = DIM1; dims[1] = DIM2; int clamp = 0;
    return pnl::CDenseMatrix<float>::Create( 2, dims, IN_ARRAY2, clamp);
}
pnl::CMatrix<float>* mkCMatrixF1( float* IN_ARRAY1, int DIM1 ){
    int dims[1]; dims[0] = DIM1; int clamp = 0;
    return pnl::CDenseMatrix<float>::Create( 1, dims, IN_ARRAY1, clamp);
}
pnl::CEvidence** newCEvidences(int n){
    return new pnl::CEvidence*[n];
}
pnl::CEvidence* mkEvidence(pnl::CGraphicalModel *model, std::vector<int> aa, std::vector<float> ff){
    const pnl::valueVector v( ff.begin(), ff.end());
    const pnl::intVector iv(aa.begin(), aa.end());
    return pnl::CEvidence::Create((pnl::CGraphicalModel const *) model,iv,v );
    }
pnl::CNodeType* mkNodeTypeVector(int nnodes){
    pnl::CNodeType* nTs = new pnl::CNodeType[nnodes];
    return nTs;
    }
void assignEvidence(pnl::CEvidence** evidences, pnl::CEvidence* evidence, int index){
    evidences[index] = evidence;
}
std::vector<float> convertVector(pnl::floatVector f){
    std::vector<float> f2;
    f2.assign( &f[0], &f[0]+f.size() );
    return f2;
}
pnl::intVector* toIntVector(std::vector<int> v){
    pnl::intVector* iv = new pnl::intVector();
    iv->assign(&v[0], &v[0]+v.size());
    return iv;
}
const pnl::intVector* toConstIntVector(std::vector<int> v){
    return (const pnl::intVector*) toIntVector(v);
}
pnl::pEvidencesVecVector* toEvidencesVecVector(pnl::CEvidence** ev, int n){
    pnl::pEvidencesVecVector *v = new pnl::pEvidencesVecVector();
    for(int i=0; i<n; i++){
        pnl::pEvidencesVector subv;
        subv.push_back(ev[i]);
        v->push_back(subv);
    }
    return v;
}

pnl::CBNet* mkSkelBNet(int* IN_ARRAY1, int DIM1){
        int i;
        int numOfNds = DIM1;
        std::cout << "Number of nodes: " << numOfNds << "\n";
        for(i=0; i<numOfNds; i++){
            std::cout << "Node("<<i<<") Size: "<<IN_ARRAY1[i] <<"\n";
            }

        // greate pGraph with crap edges
        pnl::CGraph *pGraph = pnl::CGraph::Create(0, NULL, NULL, NULL);
        pGraph->AddNodes(numOfNds);

        // set up the bnet template
        pnl::CNodeType *nodeTypes = new pnl::CNodeType [numOfNds];
        for(i=0; i< numOfNds; i++){
            nodeTypes[i].SetType(1,IN_ARRAY1[i]);
            }
        int *nodeAssociation = new int[numOfNds];
        for(i=0; i<numOfNds; i++){
            nodeAssociation[i] = i;
        }
        pnl::CBNet *pBNet = pnl::CBNet::Create( numOfNds, numOfNds, nodeTypes, nodeAssociation, pGraph );

        // Set up factors ...
        pnl::CModelDomain* pMD = pBNet->GetModelDomain();
        pnl::CFactor **myParams = new pnl::CFactor*[numOfNds];
        int *nodeNumbers = new int [numOfNds];
        int **domains = new int*[numOfNds];
        for(i=0; i<numOfNds; i++){
            nodeNumbers[i] = 1;
            int *domain_i = new int[nodeNumbers[i]];
            domain_i[0] = i;
            domains[i] = domain_i;
           }
        pBNet->AllocFactors();
        for( i = 0; i < numOfNds; i++ )
        {
            myParams[i] = pnl::CTabularCPD::Create( domains[i], nodeNumbers[i], pMD);
        }
        for( i = 0; i < numOfNds; i++ )
        {
            try {
              pBNet->AttachFactor(myParams[i]);
            } catch(pnl::CException &ex) {
            std::cout << "\n\nException breaks normal program execution: " << ex.GetMessage() << "\n";
            }
        }
        pBNet = pnl::CBNet::CreateWithRandomMatrices( pGraph, pBNet->GetModelDomain() );
        return pBNet;
}

pnl::CMlStaticStructLearnHC* mkCMlStaticStructLearnHC(pnl::CBNet* pBNet, int max_fan_in=4, int n_restarts=1){

        // set up the learner
        pnl::intVector vA, vD;
        pnl::CMlStaticStructLearnHC* pLearnS;

        try {
          pLearnS = pnl::CMlStaticStructLearnHC::Create(pBNet,
                            pnl::itStructLearnML, // Learning Type
                            pnl::StructLearnHC,   // EOptimizeTypes
                            pnl::BIC,             // ScoreType
                            max_fan_in,
                            vA,
                            vD,
                            n_restarts);
        } catch(pnl::CException &ex) {
            std::cout << "\n\nException breaks normal program execution: " << ex.GetMessage() << "\n";
        }

        return pLearnS;
}


%}
