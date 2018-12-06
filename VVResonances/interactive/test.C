void test(){
    
    
    TFile* file = TFile::Open("/home/dschaefer/DiBoson3D/test_kernelSmoothing_pythia/workspace_pythia_nominal.root");
    RooWorkspace* w = (RooWorkspace*) file->Get("w");
    RooSimultaneousOpt* pdf = (RooSimultaneousOpt*) w->obj("model_b");
    FastVerticalInterpHistPdf3D* pdfhist = (FastVerticalInterpHistPdf3D*) w->obj("shapeBkg_nonRes_JJ_HPHP_13TeV");
    std::cout << "pdfhist " <<  pdfhist << std::endl;
    
//    w->Print();
//     RooRealVar* MJ1= new RooRealVar("MJ1","MJ1",55,210);
//     RooRealVar* MJ2= new RooRealVar("MJ2","MJ2",55,210);
//     RooRealVar* MJJ= new RooRealVar("MJJ","MJJ",1000,5000);
    
    RooRealVar* MJ1=(RooRealVar*) w->var("MJ1");
    RooRealVar* MJ2=(RooRealVar*) w->var("MJ2");
    RooRealVar* MJJ=(RooRealVar*) w->var("MJJ");
    
    
     RooArgSet*s = new RooArgSet();
     s->add(*MJJ);
     s->add(*MJ2);
     s->add(*MJJ);
     
//      std::cout << pdf->expectedEvents(s) <<std::endl;
// //      MJJ->setVal(1200);
// //      MJ1->setVal(80);
// //      MJ2->setVal(80);
//      std::cout << pdf->expectedEvents(s) <<std::endl;
//    std::cout << pdf->expectedEvents(s) <<std::endl;
     
     
     
      RooAbsPdf* p1 = pdf->getPdf("shapeBkg_nonRes_JJ_HPHP_13TeV");
      std::cout << p1 <<std::endl;
      RooAbsPdf* p2 = pdf->getPdf("JJ_HPHP_13TeV");
      std::cout << p2 <<std::endl;
      float norm = p2->getNorm();
      std::cout << "normalized? " <<norm <<std::endl;
      RooAbsPdf* p3 = pdf->getPdf("n_exp_binJJ_HPHP_13TeV_proc_nonRes");
      std::cout << p3 <<std::endl;
      
      
      MJ1->setVal(80);
      MJ2->setVal(80);
  
//       for( int i=0;i<20;i++){
//       float val = 1200+i*10.;
//       MJJ->setVal(val);
//       std::cout << pdfhist->getVal(s) <<std::endl;
//       std::cout <<"JJ_HPHP_13TeV   MJJ " << val << " : "<< p2->getVal(s) <<std::endl;
//       
// }

RooDataHist* data = (RooDataHist*) w->data("data_obs");      
//pdfhist->fitTo(*w->data("data_obs"),SumW2Error(kTRUE));
TFile* finMC = new TFile("JJ_pythia_HPHP.root","READ");
TH3F* hinMC = (TH3F*)finMC->Get("nonRes");
//double norm3 = data->sumEntries();//hinMC->Integral();
double norm3 = hinMC->Integral();
int Nz = hinMC->GetNbinsZ();
float minz = hinMC->GetZaxis()->GetXmin();
float maxz = hinMC->GetZaxis()->GetXmax();

std::cout << Nz << " "<<minz << " "<<maxz << std::endl;
std::cout << "bin 25 " << hinMC->GetXaxis()->GetBinCenter(70) <<std::endl;

TH1F* kernelHisto = new TH1F("kernelHisto","kernelHisto",Nz,minz,maxz);
TH1F* dataHisto = new TH1F("dataHisto","dataHisto",Nz,minz,maxz);

//for(int j =0; j< 78;j++){
//    std::cout << 55+2*j <<std::endl;
// MJ1->setVal(55+2*j);
 MJ1->setVal(80);
 MJ2->setVal(204);


      for( int i=0;i<Nz;i++){
      float val = hinMC->GetZaxis()->GetBinCenter(i);
      MJJ->setVal(val);
      float w = pdfhist->getVal(s);
      kernelHisto->Fill(val,w);
      dataHisto->Fill(val,data->weight(*s));
      std::cout << val << " "<< w <<std::endl;
      
}
//}

TH1D* pnz  = hinMC->ProjectionZ("pnz",13,13,75,75);
double norm1 =  dataHisto->Integral();//pnz->Integral();
std::cout << norm1/pnz->Integral() <<std::endl;
std::cout << norm3 <<std::endl;
TCanvas* c = new TCanvas("c","c",400,400);
c->SetLogy();
double norm2 = kernelHisto->Integral();
kernelHisto->SetLineColor(kRed);
//kernelHisto->Scale(norm1/norm2);
kernelHisto->Scale(norm3);
//kernelHisto->Scale(1/norm2);
//dataHisto->Scale(1/norm1);
//kernelHisto->Scale(norm3);
//pnz->Scale(1/pnz->Integral());
//dataHisto->Draw();
pnz->Draw();
kernelHisto->Draw("histsame");
c->SaveAs("test.pdf");

MJ1->setVal(192);
MJ2->setVal(214);
MJJ->setVal(1580);
std::cout << pdfhist->getVal(s) <<std::endl;

     
} 






