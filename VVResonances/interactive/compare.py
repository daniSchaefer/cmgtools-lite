import ROOT
import os,sys
sys.path.append(os.path.abspath("/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/python/plotting/"))
from PlotterBase import *
from TreePlotter import *
from MergedPlotter import *
ROOT.gROOT.SetBatch(True)


def plotTwoHistos(hist1,hist2,outname,dolog=False ,label=""):
    c= ROOT.TCanvas("c","c",400,400)
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetFillColor(0)
    hist2.SetFillColor(0)
    hist1.SetLineWidth(2)
    hist2.SetLineColor(ROOT.kRed)
    hist2.SetLineWidth(2)
    hist1.Draw("hist")
    hist2.Draw("histsame")
    
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
    leg.AddEntry(hist1,"old","l")
    leg.AddEntry(hist2,'new',"l")
    leg.Draw("same")
    if dolog:
        c.SetLogy()
    text = ROOT.TLatex() 
    if label.find("mjet")!=-1:
        text.DrawLatex(1100,0.003,label)
    else:
        text.DrawLatex(32,0.01,label)
    c.SaveAs("debug/"+outname)
    
    
def plotTwoHistos3(hist1,hist2,hist3,outname,dolog=False ,label=""):
    c= ROOT.TCanvas("c","c",400,400)
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetFillColor(0)
    hist2.SetFillColor(0)
    hist1.SetLineWidth(2)
    hist2.SetLineColor(ROOT.kRed)
    hist2.SetLineWidth(2)
    hist3.SetLineColor(ROOT.kGreen)
    hist3.SetFillColor(0)
    hist3.SetFillColor(0)
    
    
    
    hist3.Draw("hist")
    hist1.Draw("histsame")
    hist2.Draw("histsame")
    
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
    leg.AddEntry(hist1,"old","l")
    leg.AddEntry(hist2,'new',"l")
    leg.AddEntry(hist3,'data',"l")
    leg.Draw("same")
    if dolog:
        c.SetLogy()
    text = ROOT.TLatex() 
    if label.find("mjet")!=-1:
        text.DrawLatex(1100,0.003,label)
    else:
        text.DrawLatex(32,0.01,label)
    c.SaveAs("debug/"+outname)    
    
    
    
def makeProjections(kernelHisto,sampleHisto,NominalHisto):
    Nx = kernelHisto.GetNbinsX()
    Ny = kernelHisto.GetNbinsY()
    kernelHisto.GetXaxis().SetTitle("MVV (GeV)")
    kernelHisto.GetYaxis().SetTitle("m_{jet} (GeV)")
    print Nx
    print Ny
    for i in range(1,Ny+1):
        nom = NominalHisto.ProjectionX("projx3",i,i)
        nom.Scale(1/nom.Integral())
        proj = kernelHisto.ProjectionX("projx",i,i)
        proj2 = sampleHisto.ProjectionX("projx2",i,i)
        proj2.Scale(1/proj2.Integral())
        proj.Scale(1/proj.Integral())
        #proj2.SetAxisRange(0.,1,"Y")
        proj2.SetMinimum(0.00000001)
        label = "mjet "+str(round(kernelHisto.GetYaxis().GetBinCenter(i),1))
        plotTwoHistos3(proj,proj2,nom ,"ProjInMjetBin"+str(i)+"overMVV.pdf",True,label)
    for i in range(1,Nx+1):
        proj = kernelHisto.ProjectionY("projy",i,i)
        proj2 = sampleHisto.ProjectionY("projy2",i,i)
        nom = NominalHisto.ProjectionY("projy3",i,i)
        nom.Scale(1/nom.Integral())
        label = "mVV "+str(round(kernelHisto.GetXaxis().GetBinCenter(i),1))
        if proj.Integral()!=0 and proj2.Integral()!=0:
            proj2.Scale(1/proj2.Integral())
            proj.Scale(1/proj.Integral())
            plotTwoHistos3(proj,proj2,nom,"ProjInMVVBin"+str(i)+"overMjet.pdf",False,label)    
    
if __name__=="__main__":
    infile1 ="JJ_nonRes_MVV_HP.root"
    infile2 ="JJ_nonRes_MVV_HP_pythia.root"
    f1 = ROOT.TFile(infile1,"READ")
    f2 = ROOT.TFile(infile2,"READ")
    
    histo1 = f1.Get("histo_nominal")
    histo2 = f2.Get("histo_nominal")
    
    plotTwoHistos(histo1,histo2,"testMVV.pdf",True)
    
    
    infile1 ="JJ_nonRes_COND2D_HP.root"
    infile2 ="JJ_nonRes_COND2D_HP_pythia_withSmoothing.root"
    f1 = ROOT.TFile(infile1,"READ")
    f2 = ROOT.TFile(infile2,"READ")
    
    histo1 = f1.Get("histo_nominal")
    histo1.SetName("histo_old")
    histo2 = f2.Get("histo_nominal")
    histo3 = f2.Get("mjet_mvv_nominal")
    
    makeProjections(histo1,histo2,histo3)
    
    
    
    
    
