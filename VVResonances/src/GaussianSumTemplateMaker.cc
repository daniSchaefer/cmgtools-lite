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
  double histoarray[nbinsX+1][nbinsY+1] = {};
  for (int i=1;i<output->GetNbinsX()+1;++i) {
      xs[i]=output->GetXaxis()->GetBinCenter(i);
  }

  std::vector<double> yv;
  std::vector<int> biny;
  for (int j=1;j<nbinsY+1;++j) {
      double w = output->GetYaxis()->GetBinWidth(j);  
      double ymin=output->GetYaxis()->GetBinLowEdge(j);
      double ymax= ymin+w;
      double interval = 20.;
      for (int k=0;k<=int(w/interval);k++)
      {
        double y = ymin + k* interval;
        if( y >= ymax) continue;
        yv.push_back(y);
        biny.push_back(j);
      }
  }
  
  
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
       for (unsigned int j=0;j< yv.size();++j) {
        double normx = fabs((xs[i]-scalex)/resx);
        unsigned int indexx = int(normx*1000);
        double normy = fabs((yv[j]-scaley)/resy);
        unsigned int indexy = int(normy*1000);
        if(indexx < 9999 && indexy < 9999 ){
        double interpx = gausint[indexx] + ( gausint[indexx] - gausint[indexx+1])*(normx*1000-indexx);
        double interpy = gausint[indexy] + ( gausint[indexy] - gausint[indexy+1])*(normy*1000-indexy);
   
        int bin = biny.at(j);   
        histoarray[i][bin] += reweight*dataset->weight()*interpx*interpy/(2.5066*resx*resy);
        
        
       }}}

    
    

  } 

     for (int i=1;i<output->GetNbinsX()+1;++i) {
       for (int j=1;j<output->GetNbinsY()+1;++j) {  
         output->SetBinContent(i,j,histoarray[i][j]);
         //std::cout << i << " "<< j << " "<< histoarray[i][j] << std::endl;
       }}


}


