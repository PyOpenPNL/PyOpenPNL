%module openpnl

%{
#include "pnlConfig.hpp"
#include "pnlTypeDefs.hpp"
#include "pnlObject.hpp"
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
%}

%include "typemaps.i"
%include "std_vector.i"
// Instantiate templates used by example
namespace std {
   %template(intVector) vector<int>;
   %template(intVecVector) vector<vector<int> >;
}


%define PNL_API
%enddef

%template(intVector) std::vector<int>;
%template(intVecVector) std::vector< std::vector< int > >;

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
%include "pnlTypeDefs.hpp"
%include "pnlNodeValues.hpp"
%include "pnl2DBitwiseMatrix.hpp"
%include "pnlMatrix.hpp"
%include "pnlModelTypes.hpp"
%include "pnlFactor.hpp"
%include "pnlFactors.hpp"
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
%include "pnlExampleModels.hpp"
%include "pnlDynamicInferenceEngine.hpp"
%include "pnl2TBNInferenceEngine.hpp"
%include "pnl1_5SliceInferenceEngine.hpp"
%include "pnl1_5SliceJtreeInferenceEngine.hpp"
