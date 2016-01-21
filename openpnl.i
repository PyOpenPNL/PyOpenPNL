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
%}

%include "typemaps.i"
%include "std_vector.i"

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
//%rename(something_else) operator();
%include "pnlMatrix.hpp"
%include "pnlMatrixIterator.hpp"
%template(pnlCMatrixf)  pnl::CMatrix< float >;
%include "pnlDenseMatrix.hpp"
%template(pnlDenseMatrixF) pnl::CDenseMatrix<float>;
%include "pnlNumericDenseMatrix.hpp"
%include "pnlModelTypes.hpp"
%include "pnlFactor.hpp"
%include "pnlFactors.hpp"
%include "pnlIDPotential.hpp"
%include "pnlPotential.hpp"
%include "pnlObject.hpp"
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
%include "pnlInferenceEngine.hpp"
%include "pnlNaiveInferenceEngine.hpp"

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
    }
}

/*
 *  Python SWIG Helper Functions ... is there a better way we should be doing this??
 */
%inline %{

pnl::CEvidence** newCEvidences(int n){
    return new pnl::CEvidence*[n];
}
pnl::CEvidence* mkEvidence(pnl::CGraphicalModel *model, std::vector<int> aa, std::vector<float> ff){
    const pnl::valueVector v( ff.begin(), ff.end());
    const pnl::intVector iv(aa.size());
    return pnl::CEvidence::Create((pnl::CGraphicalModel const *) model,iv,v );
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

%}

//%array_class(struct CEvidence, CEvidences);
