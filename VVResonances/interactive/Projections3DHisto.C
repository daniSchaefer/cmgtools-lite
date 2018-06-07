// Run from command line with
// root .x 'Projections3DHisto.C("JJ_nonRes_HPHP.root","nonRes","JJ_nonRes_3D_HPHP.root","histo","3Dkernels_HPHP")' --> HPHP
// root .x 'Projections3DHisto.C("JJ_nonRes_HPLP.root","nonRes","JJ_nonRes_3D_HPLP.root","histo","3Dkernels_HPLP")' --> HPLP 
// root .x 'Projections3DHisto.C("JJ_nonRes_LPLP.root","nonRes","JJ_nonRes_3D_LPLP.root","histo","3Dkernels_LPLP")' --> LPLP 
void Projections3DHisto(std::string dataFile, std::string hdataName, std::string fitFile, std::string hfitName, std::string outDirName){

std::stringstream ss; ss.str(""); ss << "mkdir " << outDirName << std::endl;
system(ss.str().c_str());

gStyle->SetOptStat(0);
gStyle->SetOptTitle(0);
gROOT->SetBatch(true);

TFile* fin = new TFile(fitFile.c_str(),"READ"); //fitFile: JJ_nonRes_2D_HPHP.root
TH3F* hin = (TH3F*)fin->Get(hfitName.c_str()); //hfitName: histo
hin->Scale(1./hin->Integral());

TFile* finMC = new TFile(dataFile.c_str(),"READ"); //dataFile: JJ_nonRes_HPHP_nominal.root
TH3F* hinMC = (TH3F*)finMC->Get(hdataName.c_str()); //hdataName: nonRes
hinMC->Scale(1./hinMC->Integral());



int binsx = hin->GetNbinsX();
float xmin = hin->GetXaxis()->GetXmin();
float xmax = hin->GetXaxis()->GetXmax();
std::cout << "xmin " << xmin << " xmax " << xmax << " binsx " << binsx << std::endl;

int binsy = hin->GetNbinsY();
float ymin = hin->GetYaxis()->GetXmin();
float ymax = hin->GetYaxis()->GetXmax();
std::cout << "ymin " << ymin << " ymax " << ymax << " binsy " << binsy << std::endl;

int binsz = hin->GetNbinsZ();
float zmin = hin->GetZaxis()->GetXmin();
float zmax = hin->GetZaxis()->GetXmax();
std::cout << "zmin " << zmin << " zmax " << zmax << " binsz " << binsz << std::endl;

std::vector<TH1F*> hx;
std::vector<TH1F*> hy;
std::vector<TH1F*> hz;
std::vector<TH1F*> hxMC;
std::vector<TH1F*> hyMC;
std::vector<TH1F*> hzMC;

std::vector<TH1F*> pullsx;
std::vector<TH1F*> pullsy;
std::vector<TH1F*> pullsz;

int zbinMin[4] = {1,1,hin->GetZaxis()->FindBin(1300),hin->GetZaxis()->FindBin(2000)};
int zbinMax[4] = {binsz,hin->GetZaxis()->FindBin(1300),hin->GetZaxis()->FindBin(2000),binsz};
int colors[5] = {1,99,9,8,94};

float scale[4] = {1.,0.8,2.,20.};


for(int i=0; i<4; ++i){

 std::cout << "Plotting mJJ projections " << zbinMin[i] << " " << zbinMax[i] << std::endl;
 ss.str(""); ss << "px_" << i << std::endl;
 hx.push_back((TH1F*)hin->ProjectionX(ss.str().c_str(),1,binsy,zbinMin[i],zbinMax[i]));
 ss.str(""); ss << "py_" << i << std::endl;
 hy.push_back((TH1F*)hin->ProjectionY(ss.str().c_str(),1,binsx,zbinMin[i],zbinMax[i]));
 ss.str(""); ss << "pxMC_" << i << std::endl;
 hxMC.push_back((TH1F*)hinMC->ProjectionX(ss.str().c_str(),1,binsy,zbinMin[i],zbinMax[i]));
 ss.str(""); ss << "pyMC_" << i << std::endl;
 hyMC.push_back((TH1F*)hinMC->ProjectionY(ss.str().c_str(),1,binsx,zbinMin[i],zbinMax[i])); 

 ss.str(""); ss << "pullsx_" << i << std::endl;
 pullsx.push_back( new TH1F(ss.str().c_str(),ss.str().c_str(),40,-10,10) );
 ss.str(""); ss << "pullsy_" << i << std::endl;
 pullsy.push_back( new TH1F(ss.str().c_str(),ss.str().c_str(),40,-10,10) );
        
}

for(int i=0; i<4; ++i){

 for(int b=1; b<=binsx; ++b){
  if(hxMC[i]->GetBinContent(b) != 0){ pullsx[i]->Fill( (hxMC[i]->GetBinContent(b)-hx[i]->GetBinContent(b))/hxMC[i]->GetBinError(b) ); }
  if(hyMC[i]->GetBinContent(b) != 0){ pullsy[i]->Fill( (hyMC[i]->GetBinContent(b)-hy[i]->GetBinContent(b))/hyMC[i]->GetBinError(b) ); }
 }

}

for(int i=0; i<4; ++i){

 hx[i]->Scale(scale[i]);
 hy[i]->Scale(scale[i]);
 hxMC[i]->Scale(scale[i]);
 hyMC[i]->Scale(scale[i]);
    
 hx[i]->SetLineColor(colors[i]);
 hx[i]->SetMarkerColor(colors[i]);
 hy[i]->SetLineColor(colors[i]);
 hy[i]->SetMarkerColor(colors[i]);
 hxMC[i]->SetLineColor(colors[i]);
 hxMC[i]->SetMarkerColor(colors[i]);
 hxMC[i]->SetMarkerStyle(20);
 hxMC[i]->SetMarkerSize(0.5);
 hyMC[i]->SetLineColor(colors[i]);
 hyMC[i]->SetMarkerColor(colors[i]); 
 hyMC[i]->SetMarkerStyle(20);
 hyMC[i]->SetMarkerSize(0.5);
 
 pullsx[i]->SetLineColor(colors[i]);
 pullsx[i]->SetLineWidth(2);
 pullsx[i]->SetMarkerSize(0);
 pullsy[i]->SetLineColor(colors[i]);
 pullsy[i]->SetLineWidth(2);
 pullsy[i]->SetMarkerSize(0);
  
}
hx[0]->SetMinimum(0);
hx[0]->SetMaximum(0.03);
hy[0]->SetMinimum(0);
hy[0]->SetMaximum(0.03);

TLegend* leg = new TLegend(0.6,0.6,0.85,0.8);
leg->AddEntry(hxMC[0],"Simulation (Pythia8)","LP");
leg->AddEntry(hx[0],"Template","L");
leg->AddEntry(hx[1],"1 < m_{jj} < 1.3 TeV");
leg->AddEntry(hx[2],"1.3 < m_{jj} < 2 TeV");
leg->AddEntry(hx[3],"2 < m_{jj} < 5 TeV");
 
TCanvas* cx = new TCanvas("cx","cx");
cx->cd();
hx[0]->SetMinimum(0);
for(int i=0; i<4; ++i){ hx[i]->Draw("HISTsame"); hxMC[i]->Draw("PEsame");}
hx[0]->GetXaxis()->SetTitle("m_{jet1} (proj. x) [GeV]");
leg->Draw();
cx->SaveAs(TString(outDirName)+TString("/")+TString("cx.png"),"png");

TCanvas* cy = new TCanvas("cy","cy");
cy->cd();
for(int i=0; i<4; ++i){ hy[i]->Draw("HISTsame"); hyMC[i]->Draw("PEsame");}
hy[0]->GetXaxis()->SetTitle("m_{jet2} (proj. y) [GeV]");
leg->Draw();
cy->SaveAs(TString(outDirName)+TString("/")+TString("cy.png"),"png");

// std::string labelsXY[4] = {"All m_{jj} bins","1 < m_{jj} < 1.3 TeV","1.3 < m_{jj} < 2 TeV","2 < m_{jj} < 5 TeV"};
// for(int i=0; i<4; ++i){
//
//  TPaveText* pt = new TPaveText(0.1436782,0.7690678,0.4224138,0.8644068,"brNDC");
//  pt->SetTextFont(42);
//  pt->SetTextSize(0.042);
//  pt->SetTextAlign(22);
//  pt->SetFillColor(0);
//  pt->SetBorderSize(1);
//  pt->SetFillStyle(0);
//  pt->SetLineWidth(2);
//  pt->AddText(labelsXY[i].c_str());
//
//
//
//  ss.str(""); ss << "cpullsx_" << i;
//  TCanvas* cpullsx = new TCanvas(ss.str().c_str(),ss.str().c_str());
//  cpullsx->cd();
//  pullsx[i]->Draw("PE");
//
//  TF1* f = new TF1("func","gaus(0)",-10,10);
//  f->SetParameter(0,10);
//  f->SetParError(0,5);
//  f->SetParameter(1,0);
//  f->SetParError(1,0.5);
//  f->SetParameter(2,4);
//  f->SetParError(2,2);
//  pullsx[i]->Fit("func");
//
//  pt->Draw();
//
//  TPaveText* ptstat = new TPaveText(0.6091954,0.5635593,0.9597701,0.9088983,"brNDC");
//  ptstat->SetTextFont(42);
//  ptstat->SetTextSize(0.042);
//  ptstat->SetTextAlign(12);
//  ptstat->SetFillColor(0);
//  ptstat->SetBorderSize(0);
//  ptstat->SetFillStyle(0);
//
//  ss.str(""); ss << "Constant = " << f->GetParameter(0) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Mean = " << f->GetParameter(1) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Sigma = " << f->GetParameter(2) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "#chi^2/ndf = " << f->GetChisquare() << "/" << f->GetNDF() << std::endl;
//  ptstat->AddText(ss.str().c_str());
//
//  ptstat->Draw();
//
//  cpullsx->SaveAs(TString(outDirName)+TString("/")+TString(cpullsx->GetName())+TString(".png"),"png");
//
// }
//
// for(int i=0; i<4; ++i){
//
//  TPaveText* pt = new TPaveText(0.1436782,0.7690678,0.4224138,0.8644068,"brNDC");
//  pt->SetTextFont(42);
//  pt->SetTextSize(0.042);
//  pt->SetTextAlign(22);
//  pt->SetFillColor(0);
//  pt->SetBorderSize(1);
//  pt->SetFillStyle(0);
//  pt->SetLineWidth(2);
//  pt->AddText(labelsXY[i].c_str());
//
//
//
//  ss.str(""); ss << "cpullsy_" << i;
//  TCanvas* cpullsy = new TCanvas(ss.str().c_str(),ss.str().c_str());
//  cpullsy->cd();
//  pullsy[i]->Draw("PE");
//
//  TF1* f = new TF1("func","gaus(0)",-10,10);
//  f->SetParameter(0,10);
//  f->SetParError(0,5);
//  f->SetParameter(1,0);
//  f->SetParError(1,0.5);
//  f->SetParameter(2,4);
//  f->SetParError(2,2);
//  pullsy[i]->Fit("func");
//
//  pt->Draw();
//
//  TPaveText* ptstat = new TPaveText(0.6091954,0.5635593,0.9597701,0.9088983,"brNDC");
//  ptstat->SetTextFont(42);
//  ptstat->SetTextSize(0.042);
//  ptstat->SetTextAlign(12);
//  ptstat->SetFillColor(0);
//  ptstat->SetBorderSize(0);
//  ptstat->SetFillStyle(0);
//
//  ss.str(""); ss << "Constant = " << f->GetParameter(0) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Mean = " << f->GetParameter(1) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Sigma = " << f->GetParameter(2) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "#chi^2/ndf = " << f->GetChisquare() << "/" << f->GetNDF() << std::endl;
//  ptstat->AddText(ss.str().c_str());
//
//  ptstat->Draw();
//
//  cpullsy->SaveAs(TString(outDirName)+TString("/")+TString(cpullsy->GetName())+TString(".png"),"png");
//
// }

int xbinMin[5] = {1,hin->GetXaxis()->FindBin(55),hin->GetXaxis()->FindBin(70),hin->GetXaxis()->FindBin(100),hin->GetXaxis()->FindBin(150)};
int xbinMax[5] = {binsx,hin->GetXaxis()->FindBin(70),hin->GetXaxis()->FindBin(100),hin->GetXaxis()->FindBin(150),binsx};

float scalez[5] = {1.,1.,0.1,0.01,0.001};

for(int i=0; i<5; ++i){

 std::cout << "Plotting mJ projections " << xbinMin[i] << " " << xbinMax[i] << std::endl;
 ss.str(""); ss << "pz_" << i << std::endl;
 hz.push_back((TH1F*)hin->ProjectionZ(ss.str().c_str(),xbinMin[i],xbinMax[i],xbinMin[i],xbinMax[i]));
 ss.str(""); ss << "pzMC_" << i << std::endl;
 hzMC.push_back((TH1F*)hinMC->ProjectionZ(ss.str().c_str(),xbinMin[i],xbinMax[i],xbinMin[i],xbinMax[i]));

 ss.str(""); ss << "pullsz_" << i << std::endl;
 pullsz.push_back( new TH1F(ss.str().c_str(),ss.str().c_str(),40,-10,10) );
    
}

for(int i=0; i<5; ++i){

 for(int b=1; b<=binsx; ++b){
  if(hzMC[i]->GetBinContent(b) != 0){ pullsz[i]->Fill( (hzMC[i]->GetBinContent(b)-hz[i]->GetBinContent(b))/hzMC[i]->GetBinError(b) ); }
 }

}

for(int i=0; i<5; ++i){
 
 hz[i]->Scale(scalez[i]);
 hzMC[i]->Scale(scalez[i]);
   
 hz[i]->SetLineColor(colors[i]);
 hz[i]->SetMarkerColor(colors[i]);
 hzMC[i]->SetLineColor(colors[i]);
 hzMC[i]->SetMarkerColor(colors[i]);
 hzMC[i]->SetMarkerStyle(20);
 hzMC[i]->SetMarkerSize(0.5);

 pullsz[i]->SetLineColor(colors[i]);
 pullsz[i]->SetLineWidth(2);
 pullsz[i]->SetMarkerSize(0);
     
}

TLegend* leg2 = new TLegend(0.6,0.6,0.85,0.85);
leg2->AddEntry(hzMC[0],"Simulation (Pythia8)","LP");
leg2->AddEntry(hz[0],"Template","L");
leg2->AddEntry(hz[1],"55 < m_{jet} < 70 GeV");
leg2->AddEntry(hz[2],"70 < m_{jet} < 100 GeV");
leg2->AddEntry(hz[3],"100 < m_{jet} < 150 GeV");
leg2->AddEntry(hz[4],"150 < m_{jet} < 215 GeV");

TCanvas* cz = new TCanvas("cz","cz");
cz->SetLogy();
cz->cd();
hz[0]->SetMinimum(1E-09);
hz[0]->SetMaximum(0.5);
for(int i=0; i<5; ++i){ hz[i]->Draw("HISTsame"); hzMC[i]->Draw("PEsame");}
hz[0]->GetXaxis()->SetTitle("m_{jj} (proj. z) [GeV]");
leg2->Draw();
cz->SaveAs(TString(outDirName)+TString("/")+TString("cz.png"),"png");

// std::string labelsZ[5] = {"All m_{jet} bins","55 < m_{jet} < 70 GeV","70 < m_{jet} < 100 GeV","100 < m_{jet} < 150 GeV","150 < m_{jet} < 215 GeV"};
// for(int i=0; i<5; ++i){
//
//  TPaveText* pt = new TPaveText(0.1436782,0.7690678,0.4224138,0.8644068,"brNDC");
//  pt->SetTextFont(42);
//  pt->SetTextSize(0.042);
//  pt->SetTextAlign(22);
//  pt->SetFillColor(0);
//  pt->SetBorderSize(1);
//  pt->SetFillStyle(0);
//  pt->SetLineWidth(2);
//  pt->AddText(labelsZ[i].c_str());
//
//
//
//  ss.str(""); ss << "cpullsz_" << i;
//  TCanvas* cpullsz = new TCanvas(ss.str().c_str(),ss.str().c_str());
//  cpullsz->cd();
//  pullsz[i]->Draw("PE");
//
//  TF1* f = new TF1("func","gaus(0)",-10,10);
//  f->SetParameter(0,10);
//  f->SetParError(0,5);
//  f->SetParameter(1,0);
//  f->SetParError(1,0.5);
//  f->SetParameter(2,4);
//  f->SetParError(2,2);
//  pullsz[i]->Fit("func");
//
//  pt->Draw();
//
//  TPaveText* ptstat = new TPaveText(0.6091954,0.5635593,0.9597701,0.9088983,"brNDC");
//  ptstat->SetTextFont(42);
//  ptstat->SetTextSize(0.042);
//  ptstat->SetTextAlign(12);
//  ptstat->SetFillColor(0);
//  ptstat->SetBorderSize(0);
//  ptstat->SetFillStyle(0);
//
//  ss.str(""); ss << "Constant = " << f->GetParameter(0) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Mean = " << f->GetParameter(1) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "Sigma = " << f->GetParameter(2) << std::endl;
//  ptstat->AddText(ss.str().c_str());
//  ss.str(""); ss << "#chi^2/ndf = " << f->GetChisquare() << "/" << f->GetNDF() << std::endl;
//  ptstat->AddText(ss.str().c_str());
//
//  ptstat->Draw();
//
//  cpullsz->SaveAs(TString(outDirName)+TString("/")+TString(cpullsz->GetName())+TString(".png"),"png");
//
// }

TH3F* hin_PTZUp = (TH3F*)fin->Get("histo_PTZUp"); hin_PTZUp->Scale(1./hin_PTZUp->Integral());
TH3F* hin_PTZDown = (TH3F*)fin->Get("histo_PTZDown"); hin_PTZDown->Scale(1./hin_PTZDown->Integral());
TH3F* hin_OPTZUp = (TH3F*)fin->Get("histo_OPTZUp"); hin_OPTZUp->Scale(1./hin_OPTZUp->Integral());
TH3F* hin_OPTZDown = (TH3F*)fin->Get("histo_OPTZDown"); hin_OPTZDown->Scale(1./hin_OPTZDown->Integral());
TH3F* hin_TRIGUp = (TH3F*)  fin->Get("histo_TRIGUp")  ; hin_TRIGUp->Scale  (1./hin_TRIGUp->Integral());
TH3F* hin_TRIGDown = (TH3F*)fin->Get("histo_TRIGDown"); hin_TRIGDown->Scale(1./hin_TRIGDown->Integral());
TH3F* hin_altshapeUp = (TH3F*)  fin->Get("histo_altshapeUp")  ; hin_altshapeUp->Scale  (1./hin_altshapeUp->Integral());
TH3F* hin_altshapeDown = (TH3F*)fin->Get("histo_altshapeDown"); hin_altshapeDown->Scale(1./hin_altshapeDown->Integral());
TH3F* hin_altshape2Up = (TH3F*)  fin->Get("histo_altshape2Up")  ; hin_altshape2Up->Scale  (1./hin_altshape2Up->Integral());
TH3F* hin_altshape2Down = (TH3F*)fin->Get("histo_altshape2Down"); hin_altshape2Down->Scale(1./hin_altshape2Down->Integral());


TH1F* hz_PTZUp = (TH1F*)hin_PTZUp->ProjectionZ("pz_PTZUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_PTZUp->SetLineColor(kMagenta);
TH1F* hz_PTZDown = (TH1F*)hin_PTZDown->ProjectionZ("pz_PTZDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_PTZDown->SetLineColor(kMagenta);
TH1F* hz_OPTZUp = (TH1F*)hin_OPTZUp->ProjectionZ("pz_OPTZUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_OPTZUp->SetLineColor(210);
TH1F* hz_OPTZDown = (TH1F*)hin_OPTZDown->ProjectionZ("pz_OPTZDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_OPTZDown->SetLineColor(210);

TH1F* hz_TRIGUp = (TH1F*)hin_TRIGUp->ProjectionZ("pz_TRIGUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_TRIGUp->SetLineColor(kBlue);
TH1F* hz_TRIGDown = (TH1F*)hin_TRIGDown->ProjectionZ("pz_TRIGDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_TRIGDown->SetLineColor(kBlue);

TH1F* hz_altshapeUp = (TH1F*)hin_altshapeUp->ProjectionZ("pz_altshapeUp",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_altshapeUp->SetLineColor(kRed);
TH1F* hz_altshapeDown = (TH1F*)hin_altshapeDown->ProjectionZ("pz_altshapeDown",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_altshapeDown->SetLineColor(kRed);

TH1F* hz_altshape2Up = (TH1F*)hin_altshape2Up->ProjectionZ("pz_altshape2Up",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_altshape2Up->SetLineColor(kYellow);
TH1F* hz_altshape2Down = (TH1F*)hin_altshape2Down->ProjectionZ("pz_altshape2Down",xbinMin[0],xbinMax[0],xbinMin[0],xbinMax[0]);
hz_altshape2Down->SetLineColor(kYellow);

TLegend* leg3 = new TLegend(0.6,0.55,0.95,0.8);
leg3->AddEntry(hzMC[0],"Simulation (Pythia8)","LP");
leg3->AddEntry(hz[0],"Template","L");
leg3->AddEntry(hz_PTZUp,"p_{T} syst. up/down","L");
leg3->AddEntry(hz_OPTZUp,"1/p_{T} syst. up/down","L");
leg3->AddEntry(hz_TRIGUp,"Trigger syst. up/down","L");
leg3->AddEntry(hz_altshapeUp,"MadGraph syst. up/down","L");
leg3->AddEntry(hz_altshape2Up,"Herwig syst. up/down","L");

TCanvas* czSyst = new TCanvas("czSyst","czSyst");
czSyst->cd();
czSyst->SetLogy();

hz[0]->SetMinimum(1E-06);
hz[0]->Draw("HIST");
hz_PTZUp->Draw("HISTsame");
hz_PTZDown->Draw("HISTsame"); 
hz_OPTZUp->Draw("HISTsame");
hz_OPTZDown->Draw("HISTsame");
hz_TRIGUp->Draw("HISTsame");
hz_TRIGDown->Draw("HISTsame");
hz_altshapeUp->Draw("HISTsame");
hz_altshapeDown->Draw("HISTsame");
hz_altshape2Up->Draw("HISTsame");
hz_altshape2Down->Draw("HISTsame");

hzMC[0]->Draw("same");
leg3->Draw();
czSyst->SaveAs(TString(outDirName)+TString("/")+TString("czSyst.png"),"png");

TH3F* hin_PTXUp = (TH3F*)fin->Get("histo_PTXYUp"); hin_PTXUp->Scale(1./hin_PTXUp->Integral());
TH3F* hin_PTXDown = (TH3F*)fin->Get("histo_PTXYDown"); hin_PTXDown->Scale(1./hin_PTXDown->Integral());
TH3F* hin_OPTXUp = (TH3F*)fin->Get("histo_OPTXYUp"); hin_OPTXUp->Scale(1./hin_OPTXUp->Integral());
TH3F* hin_OPTXDown = (TH3F*)fin->Get("histo_OPTXYDown"); hin_OPTXDown->Scale(1./hin_OPTXDown->Integral());

TH3F* hin_TRIGXUp   = (TH3F*)fin->Get("histo_TRIGUp")  ; hin_TRIGXUp  ->Scale(1./hin_TRIGXUp->Integral());
TH3F* hin_TRIGXDown = (TH3F*)fin->Get("histo_TRIGDown"); hin_TRIGXDown->Scale(1./hin_TRIGXDown->Integral());

TH3F* hin_altshapeXUp   = (TH3F*)fin->Get("histo_altshapeUp")  ; hin_altshapeXUp  ->Scale(1./hin_altshapeXUp->Integral());
TH3F* hin_altshapeXDown = (TH3F*)fin->Get("histo_altshapeDown"); hin_altshapeXDown->Scale(1./hin_altshapeXDown->Integral());
TH3F* hin_altshape2XUp   = (TH3F*)fin->Get("histo_altshape2Up")  ; hin_altshape2XUp  ->Scale(1./hin_altshape2XUp->Integral());
TH3F* hin_altshape2XDown = (TH3F*)fin->Get("histo_altshape2Down"); hin_altshape2XDown->Scale(1./hin_altshape2XDown->Integral());

TH1F* hx_PTXUp = (TH1F*)hin_PTXUp->ProjectionX("px_PTXUp",1,binsy,zbinMin[0],zbinMax[0]);
hx_PTXUp->SetLineColor(kMagenta);
TH1F* hx_PTXDown = (TH1F*)hin_PTXDown->ProjectionX("px_PTXDown",1,binsy,zbinMin[0],zbinMax[0]);
hx_PTXDown->SetLineColor(kMagenta);
TH1F* hx_OPTXUp = (TH1F*)hin_OPTXUp->ProjectionX("px_OPTXUp",1,binsy,zbinMin[0],zbinMax[0]);
hx_OPTXUp->SetLineColor(210);
TH1F* hx_OPTXDown = (TH1F*)hin_OPTXDown->ProjectionX("px_OPTXDown",1,binsy,zbinMin[0],zbinMax[0]);
hx_OPTXDown->SetLineColor(210);

TH1F* hx_TRIGXUp = (TH1F*)hin_TRIGXUp->ProjectionX("px_TRIGUp",1,binsy,zbinMin[0],zbinMax[0]);
hx_TRIGXUp->SetLineColor(kBlue);
TH1F* hx_TRIGXDown = (TH1F*)hin_TRIGXDown->ProjectionX("px_TRIGDown",1,binsy,zbinMin[0],zbinMax[0]);
hx_TRIGXDown->SetLineColor(kBlue);

TH1F* hx_altshapeXUp = (TH1F*)hin_altshapeXUp->ProjectionX("px_altshapeUp",1,binsy,zbinMin[0],zbinMax[0]);
hx_altshapeXUp->SetLineColor(kRed);
TH1F* hx_altshapeXDown = (TH1F*)hin_altshapeXDown->ProjectionX("px_altshapeDown",1,binsy,zbinMin[0],zbinMax[0]);
hx_altshapeXDown->SetLineColor(kRed);
TH1F* hx_altshape2XUp = (TH1F*)hin_altshape2XUp->ProjectionX("px_altshape2Up",1,binsy,zbinMin[0],zbinMax[0]);
hx_altshape2XUp->SetLineColor(kYellow);
TH1F* hx_altshape2XDown = (TH1F*)hin_altshape2XDown->ProjectionX("px_altshape2Down",1,binsy,zbinMin[0],zbinMax[0]);
hx_altshape2XDown->SetLineColor(kYellow);

TCanvas* cxSyst = new TCanvas("cxSyst","cxSyst");
cxSyst->cd();
hx[0]->Draw("HIST");
hx_PTXUp->Draw("HISTsame");
hx_PTXDown->Draw("HISTsame"); 
hx_OPTXUp->Draw("HISTsame");
hx_OPTXDown->Draw("HISTsame");
hx_TRIGXUp->Draw("HISTsame");
hx_TRIGXDown->Draw("HISTsame");
hx_altshapeXUp->Draw("HISTsame");
hx_altshapeXDown->Draw("HISTsame");
hx_altshape2XUp->Draw("HISTsame");
hx_altshape2XDown->Draw("HISTsame");
hxMC[0]->Draw("same");
leg3->Draw();

cxSyst->SaveAs(TString(outDirName)+TString("/")+TString("cxSyst.png"),"png");

TH3F* hin_PTYUp = (TH3F*)fin->Get("histo_PTXYUp"); hin_PTYUp->Scale(1./hin_PTYUp->Integral());
TH3F* hin_PTYDown = (TH3F*)fin->Get("histo_PTXYDown"); hin_PTYDown->Scale(1./hin_PTYDown->Integral());
TH3F* hin_OPTYUp = (TH3F*)fin->Get("histo_OPTXYUp"); hin_OPTYUp->Scale(1./hin_OPTYUp->Integral());
TH3F* hin_OPTYDown = (TH3F*)fin->Get("histo_OPTXYDown"); hin_OPTYDown->Scale(1./hin_OPTYDown->Integral());

TH3F* hin_TRIGYUp = (TH3F*)fin->Get("histo_TRIGUp"); hin_TRIGYUp->Scale(1./hin_TRIGYUp->Integral());
TH3F* hin_TRIGYDown = (TH3F*)fin->Get("histo_TRIGDown"); hin_TRIGYDown->Scale(1./hin_TRIGYDown->Integral());

TH3F* hin_altshapeYUp = (TH3F*)fin->Get("histo_altshapeUp"); hin_altshapeYUp->Scale(1./hin_altshapeYUp->Integral());
TH3F* hin_altshapeYDown = (TH3F*)fin->Get("histo_altshapeDown"); hin_altshapeYDown->Scale(1./hin_altshapeYDown->Integral());
TH3F* hin_altshape2YUp = (TH3F*)fin->Get("histo_altshape2Up"); hin_altshape2YUp->Scale(1./hin_altshape2YUp->Integral());
TH3F* hin_altshape2YDown = (TH3F*)fin->Get("histo_altshape2Down"); hin_altshape2YDown->Scale(1./hin_altshape2YDown->Integral());


TH1F* hy_PTYUp = (TH1F*)hin_PTYUp->ProjectionY("py_PTYUp",1,binsy,zbinMin[0],zbinMax[0]);
hy_PTYUp->SetLineColor(kMagenta);
TH1F* hy_PTYDown = (TH1F*)hin_PTYDown->ProjectionY("py_PTYDown",1,binsy,zbinMin[0],zbinMax[0]);
hy_PTYDown->SetLineColor(kMagenta);
TH1F* hy_OPTYUp = (TH1F*)hin_OPTYUp->ProjectionY("py_OPTYUp",1,binsy,zbinMin[0],zbinMax[0]);
hy_OPTYUp->SetLineColor(210);
TH1F* hy_OPTYDown = (TH1F*)hin_OPTYDown->ProjectionY("py_OPTYDown",1,binsy,zbinMin[0],zbinMax[0]);
hy_OPTYDown->SetLineColor(210);
TH1F* hy_TRIGYUp = (TH1F*)hin_TRIGYUp->ProjectionY("py_TRIGYUp",1,binsy,zbinMin[0],zbinMax[0]);
hy_TRIGYUp->SetLineColor(kBlue);
TH1F* hy_TRIGYDown = (TH1F*)hin_TRIGYDown->ProjectionY("py_TRIGYDown",1,binsy,zbinMin[0],zbinMax[0]);
hy_TRIGYDown->SetLineColor(kBlue);

TH1F* hy_altshapeYUp = (TH1F*)hin_altshapeYUp->ProjectionY("py_altshapeYUp",1,binsy,zbinMin[0],zbinMax[0]);
hy_altshapeYUp->SetLineColor(kRed);
TH1F* hy_altshapeYDown = (TH1F*)hin_altshapeYDown->ProjectionY("py_altshapeYDown",1,binsy,zbinMin[0],zbinMax[0]);
hy_altshapeYDown->SetLineColor(kRed);

TH1F* hy_altshape2YUp = (TH1F*)hin_altshape2YUp->ProjectionY("py_altshape2YUp",1,binsy,zbinMin[0],zbinMax[0]);
hy_altshape2YUp->SetLineColor(kRed);
TH1F* hy_altshape2YDown = (TH1F*)hin_altshape2YDown->ProjectionY("py_altshape2YDown",1,binsy,zbinMin[0],zbinMax[0]);
hy_altshape2YDown->SetLineColor(kRed);

TCanvas* cySyst = new TCanvas("cySyst","cySyst");
cySyst->cd();
hy[0]->Draw("HIST");
hy_PTYUp->Draw("HISTsame");
hy_PTYDown->Draw("HISTsame"); 
hy_OPTYUp->Draw("HISTsame");
hy_OPTYDown->Draw("HISTsame");
hy_TRIGYUp->Draw("HISTsame");
hy_TRIGYDown->Draw("HISTsame");
hy_altshapeYUp->Draw("HISTsame");
hy_altshapeYDown->Draw("HISTsame");
hy_altshape2YUp->Draw("HISTsame");
hy_altshape2YDown->Draw("HISTsame");
hyMC[0]->Draw("same");
leg3->Draw();

cySyst->SaveAs(TString(outDirName)+TString("/")+TString("cySyst.png"),"png");

TCanvas* cxz = new TCanvas("cxz","cxz");
cxz->cd();
TH2F* hxz = (TH2F*)hin->Project3D("zx");
hxz->Draw("COLZ");

cxz->SaveAs(TString(outDirName)+TString("/")+TString("cxz.png"),"png");

TCanvas* cyz = new TCanvas("cyz","cyz");
cyz->cd();
TH2F* hyz = (TH2F*)hin->Project3D("zy");
hyz->Draw("COLZ");

cyz->SaveAs(TString(outDirName)+TString("/")+TString("cyz.png"),"png");

}
