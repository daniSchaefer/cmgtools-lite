import ROOT
import os,sys
sys.path.append(os.path.abspath("/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/python/plotting/"))
from PlotterBase import *
from TreePlotter import *
from MergedPlotter import *
ROOT.gROOT.SetBatch(True)


def plotTwoHistos(hist1,hist2,outname,dolog=False ,hist3=0,label=""):
    c= ROOT.TCanvas("c","c",400,400)
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetLineWidth(2)
    hist2.SetLineColor(ROOT.kRed)
    hist2.SetLineWidth(2)
    hist1.Draw("hist")
    if hist3!=0:
        hist3.SetLineColor(ROOT.kGreen)
        hist3.SetLineWidth(2)
        hist3.Draw("histsame")
    hist2.Draw("histsame")
    
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
    leg.AddEntry(hist1,"mjet 30 to 40 ","l")
    leg.AddEntry(hist2,'mjet 40 to 50',"l")
    if hist3!=0:
        leg.AddEntry(hist3,'mjet 50 to 60',"l")
    leg.Draw("same")
    if dolog:
        c.SetLogy()
    text = ROOT.TLatex() 
    if label.find("mjet")!=-1:
        text.DrawLatex(1100,0.003,label)
    else:
        text.DrawLatex(32,0.01,label)
    c.SaveAs(""+outname)
    
    

    

#Q: why does the kernel only go up to 5000 GeV in MVV?

#x-Axis : MVV spectrum   => projection X gives the projection of m_jet along the MVV axis
#y-Axis : mjet spectrum  => projection Y gives the projection of MVV along the m_jet dimension   



if __name__=="__main__":
    cuts={}
    minMJJ=30.0
    maxMJJ=610.0

    minMVV=1000.0
    maxMVV=6000.0

    binsMJJ=290
    binsMVV=160
    
    HISTO2D = ROOT.TH2F( "HISTO2D" ,"jet_puppi_softdrop_jet1:MVV" ,binsMVV,minMVV,maxMVV,binsMJJ,minMJJ,maxMJJ)
    fullpath = "/storage/jbod/dschaefer/AnalysisOutput/80X/Bkg/Summer16/QCD_Pt_2Dfit.root"
    filetmp = ROOT.TFile.Open(fullpath,"READ") 
    intree = filetmp.Get("tree")
    for event in intree:
        if event.MVV< minMVV:
            continue
        if event.MVV> maxMVV+1000:
            continue
        if event.jet_puppi_softdrop_jet1 < 30:
            continue
        if event.jet_puppi_softdrop_jet1 > 610:
            continue
        if event.jet_puppi_tau2tau1_jet1 > 0.35:
            continue
        
        HISTO2D.Fill(event.MVV,event.jet_puppi_softdrop_jet1,event.weight)
    
    
    proj = HISTO2D.ProjectionX("projx",1,5)
    proj.Scale(1/proj.Integral())
    print str(HISTO2D.GetYaxis().GetBinCenter(1))+" "+str(HISTO2D.GetYaxis().GetBinCenter(5))
    
    proj2 = HISTO2D.ProjectionX("projx2",5,10)
    proj2.Scale(1/proj2.Integral())
    print str(HISTO2D.GetYaxis().GetBinCenter(5))+" "+str(HISTO2D.GetYaxis().GetBinCenter(10))
    
    
    proj3 = HISTO2D.ProjectionX("projx3",10,15)
    proj3.Scale(1/proj3.Integral())
    print str(HISTO2D.GetYaxis().GetBinCenter(10))+" "+str(HISTO2D.GetYaxis().GetBinCenter(15))
    
    plotTwoHistos(proj,proj2,"histosfromOldSetup.pdf",True ,proj3,label="")
   
    outfile = ROOT.TFile.Open("histosfromOldSetup.root","RECREATE")
    HISTO2D.Write()
    outfile.Close()
    
    
     
  
