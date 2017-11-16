#include "RooDataSet.h"
#include "TH2.h"
#include "TH1.h"
namespace cmg {

class GaussianSumTemplateMaker {
 public:
  GaussianSumTemplateMaker();
  ~GaussianSumTemplateMaker();
  GaussianSumTemplateMaker(const RooDataSet* dataset,const char* varx, const char* vary,const char* varpt, TH1* sx,TH1* sy,TH1* resx,TH1* resy,TH2* out,const char* varw =0, TH1 *weight=0 );


};

}
