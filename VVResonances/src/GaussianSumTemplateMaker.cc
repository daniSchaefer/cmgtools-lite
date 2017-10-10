#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker.h"
#include "RooArgSet.h"
#include "TCanvas.h"

using namespace cmg;
GaussianSumTemplateMaker::GaussianSumTemplateMaker() {}
GaussianSumTemplateMaker::~GaussianSumTemplateMaker() {}

GaussianSumTemplateMaker::GaussianSumTemplateMaker(const RooDataSet* dataset, const char* varx, const char* vary,const char* varpt,TH1* hscalex,TH1* hscaley,TH1* hresx,TH1* hresy,TH2* output,const char* varw,TH1* weightH) {

  double genx,geny,x,y,scalex,scaley,resx,resy,genpt,reweight,genw;
  genx=0.0;
  geny=0.0;
  scalex=0.0;
  scaley=0.0;
  x=0.0;
  y=0.0;
  resx=0.0;
  resy=0.0;
  genpt=0.0;
  reweight=1.0;
  genw=0.0;
  
  int binw=0;
  unsigned int nevents = dataset->numEntries();
  for (unsigned int entry=0;entry<nevents;++entry) {

    if ((entry % 10000)==0) {
      printf("Processed %d out of %d entries\n",entry,nevents);
    }

    const RooArgSet *line  = dataset->get(entry);
    genx=line->getRealValue(varx);
    geny=line->getRealValue(vary);
    genpt=line->getRealValue(varpt);
    if (weightH!=0) {
      genw=line->getRealValue(varw);
      binw=weightH->GetXaxis()->FindBin(genw);
      reweight=weightH->GetBinContent(binw);
    }
      
   

    scalex=hscalex->Interpolate(genpt)*genx;
    scaley=hscaley->Interpolate(genpt)*geny;
    resx=hresx->Interpolate(genpt)*genx;
    resy=hresy->Interpolate(genpt)*geny;
    for (int i=1;i<output->GetNbinsX()+1;++i) {
      x=output->GetXaxis()->GetBinCenter(i);
      for (int j=1;j<output->GetNbinsY()+1;++j) {
	y=output->GetYaxis()->GetBinCenter(j);
	//	bin=output->GetBin(i,j);
	output->Fill(x,y,reweight*dataset->weight()*gaus2D(x,y,scalex,scaley,resx,resy));
      }
    }

  } 




}



double GaussianSumTemplateMaker::gaus2D(double x, double y,double genx,double geny,double resx,double resy) {
  return exp(-0.5*(x-genx)*(x-genx)/(resx*resx)-0.5*(y-geny)*(y-geny)/(resy*resy))/(2.5066*resx*resy);
} 
