#include "RooDataSet.h"
#include "TH2.h"
#include "TH1.h"
namespace cmg {

class GaussianSumTemplateMaker1D{
 public:
  GaussianSumTemplateMaker1D();
  ~GaussianSumTemplateMaker1D();
  GaussianSumTemplateMaker1D(const RooDataSet* dataset,const char* varx,const char* varpt, TH1* sx,TH1* resx,TH1* out,const char* varw =0, TH1 *weight=0 );

 private:
  double gaus(double, double,double);
};


}
