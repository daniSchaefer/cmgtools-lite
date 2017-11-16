#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker.h"
#include "RooArgSet.h"

using namespace cmg;
GaussianSumTemplateMaker::GaussianSumTemplateMaker() {}
GaussianSumTemplateMaker::~GaussianSumTemplateMaker() {}

GaussianSumTemplateMaker::GaussianSumTemplateMaker(const RooDataSet* dataset, const char* varx, const char* vary,const char* varpt,TH1* hscalex,TH1* hscaley,TH1* hresx,TH1* hresy,TH2* output,const char* varw,TH1* weightH) {

  double genx,geny,scalex,scaley,resx,resy,genpt,reweight,genw;
  genx=0.0;
  geny=0.0;
  scalex=0.0;
  scaley=0.0;
  resx=0.0;
  resy=0.0;
  genpt=0.0;
  reweight=1.0;
  genw=0.0;
  
    double gausint[10000];
  for(int i=0; i<10000 ; i++){
    double xval = ((double)i)/1000.;
    gausint[i] = exp(-0.5*xval*xval);
  }
  
  
  int nbinsX = output->GetNbinsX();
  int nbinsY = output->GetNbinsY();
  
  double xs[nbinsX+1];
  double ys[nbinsY+1];
  double histoarray[nbinsX+1][nbinsY+1] = {};
  
  for (int i=1;i<output->GetNbinsX()+1;++i) {
      xs[i]=output->GetXaxis()->GetBinCenter(i);
  }
  for (int j=1;j<nbinsY+1;++j) {
	ys[j]=output->GetYaxis()->GetBinCenter(j);
  }
  
       for (int j=1;j<output->GetNbinsY()+1;++j) {
        double normx = fabs((xs[i]-scalex)/resx);
        unsigned int indexx = int(normx*1000);
        double normy = fabs((ys[j]-scaley)/resy);
        unsigned int indexy = int(normy*1000);
        if(indexx < 9999 && indexy < 9999 ){
        double interpx = gausint[indexx] + ( gausint[indexx] - gausint[indexx+1])*(normx*1000-indexx);
        double interpy = gausint[indexy] + ( gausint[indexy] - gausint[indexy+1])*(normy*1000-indexy);
   
           
        histoarray[i][j] += reweight*dataset->weight()*interpx*interpy/(2.5066*resx*resy);
       }}}

    
    

  } 

     for (int i=1;i<output->GetNbinsX()+1;++i) {
       for (int j=1;j<output->GetNbinsY()+1;++j) {  
         output->SetBinContent(i,j,histoarray[i][j]);
       }}


}


