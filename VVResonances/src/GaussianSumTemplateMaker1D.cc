#include "CMGTools/VVResonances/interface/GaussianSumTemplateMaker1D.h"
#include "RooArgSet.h"

using namespace cmg;
GaussianSumTemplateMaker1D::GaussianSumTemplateMaker1D() {}
GaussianSumTemplateMaker1D::~GaussianSumTemplateMaker1D() {}

GaussianSumTemplateMaker1D::GaussianSumTemplateMaker1D(const RooDataSet* dataset, const char* varx,const char* varpt,TH1* hscalex,TH1* hresx,TH1* output,const char* varw,TH1* weightH) {

  double genx,x,scalex,resx,genpt,reweight,genw,genw2;
  genx=0.0;
  scalex=0.0;
  x=0.0;
  resx=0.0;
  genpt=0.0;
  reweight=1.0;
  genw=0.0;
  


  int binw=0;
  int binw2=0;
  unsigned int nevents = dataset->numEntries();
  for (unsigned int entry=0;entry<nevents;++entry) {

    if ((entry % 10000)==0) {
      printf("Processed %d out of %d entries\n",entry,nevents);
    }

    const RooArgSet *line  = dataset->get(entry);
    genx=line->getRealValue(varx);
    genpt=line->getRealValue(varpt);
    if (weightH!=0) {
      genw=line->getRealValue(varpt);
      genw2=line->getRealValue(varw);
      binw=weightH->GetXaxis()->FindBin(genw);
      binw2=weightH->GetXaxis()->FindBin(genw2);
      reweight=weightH->GetBinContent(binw)*weightH->GetBinContent(binw2);
    }
      
    scalex=hscalex->Interpolate(genpt)*genx;
    resx=hresx->Interpolate(genpt)*genx;
    for (int i=0;i<output->GetNbinsX()+1;++i) {
      double w = output->GetXaxis()->GetBinWidth(i);  
      double xmin=output->GetXaxis()->GetBinLowEdge(i);
      double xmax= xmin+w;
      double interval = output->GetXaxis()->GetBinWidth(1)/4.;
      for (int j=0; j <= int(w/interval);j++)
      {
        x = xmin + j* interval;
        if( x >= xmax) continue;
        output->Fill(x,reweight*dataset->weight()*gaus(x,scalex,resx));
      }
    }
  }
}

double GaussianSumTemplateMaker1D::gaus(double x,double genx,double resx) {
  return exp(-0.5*(x-genx)*(x-genx)/(resx*resx))/(2.5066*resx);
} 
