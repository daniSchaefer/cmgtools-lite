
import ROOT
from CMGTools.VVResonances.plotting.RooPlotter import *
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os,copy, random
from array import array
from time import sleep
from datetime import datetime
import argparse
startTime = datetime.now()

H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref
ROOT.gROOT.SetBatch(True)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-b','--batch', action='store_true', help="stop at generation step", default = False)
#     args = parser.parse_args()

directory='control_plots_noTrigWeight'
try: os.stat(directory)
except: os.mkdir(directory)
	
lumi_13TeV = "41.4 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=0
iPosX = 11
cuts={}
lumi=41367.929231882

def GetRatioPad():
  c1_1 = rt.TPad("c1_1", "newpad1",0.,0.,1,0.2)
  c1_1.Draw()
  c1_1.cd()
  c1_1.SetTopMargin(0)
  c1_1.SetBottomMargin( 3*B/H )
  c1_1.SetLeftMargin( L/W )
  c1_1.SetRightMargin( R/W )
  c1_1.SetFillStyle(0)
  c1_1.SetFrameFillStyle(4000)
  c1_1.SetGrid(1)
  return c1_1


def GetMainPad():
  c1_2 = rt.TPad("c1_2", "newpad2",0.,0.2,1,1)
  c1_2.Draw()
  c1_2.cd()
  c1_2.SetTopMargin( 1.5*T/H )
  c1_2.SetBottomMargin(0.013)
  c1_2.SetLeftMargin( L/W )
  c1_2.SetRightMargin( R/W )
  c1_2.SetFillStyle(0)
  #c1_2.SetGrid(1)
  return c1_2
  

def getCanvas(name="c1"):
    
    canvas = ROOT.TCanvas(name,name,50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    # canvas.SetLeftMargin( L/W )
    # canvas.SetRightMargin( R/W )
    # canvas.SetTopMargin( T/H )
    # canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    canvas.cd()
    legend = ROOT.TLegend(0.6884422,0.4798951,0.9974874,0.8295455,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    
    return canvas,legend
    
def plot(dir,data,qcd,mcs,sigs,legDat,legqcd,legMCs,legSigs,logY=0):
  
  histnames = []
  fdata = ROOT.TFile.Open ( dir + data ,'READ')   
  
  for hist in fdata.GetListOfKeys():
    histnames.append(hist.GetName()) 
  fdata.Close()  
  
  fmcs = []
  fsigs = []
 
  #Open files
  for f in mcs : 
    fmc   = ROOT.TFile.Open ( dir + f   ,'READ'); 
    fmcs.append(fmc)   
    print "opened file " ,fmc.GetName()
  for f in sigs: 
    fsig  = ROOT.TFile.Open ( dir + f   ,'READ'); 
    fsigs.append(fsig)    
  
  # histnames=["looseSel_Leading_jet_softdrop_mass"]
  for h in histnames:
    # if not h.find("looseSel")!=-1: continue
    hmcs  = []
    hsigs = []
    print "Histogram: ", h
    histname = h.replace("Leading_jet","Jet_1").replace("Second_leading_jet","Jet_2")
    for fmc in fmcs: 
      htmp  = fmc.Get(histname);
      print htmp.GetName()
      hmc = copy.deepcopy(htmp)
      hmc .SetName(fmc .GetName()+"_"+histname+"_hmc") ; 
      hmc .Scale(lumi)
      if fmc .GetName().find("WJets")!=-1: 
        print "Sample is WJets!! Scale by " , float(33.7/98.4)
        hmc .Scale(float(33.7/98.4))
      if fmc .GetName().find("ZJets")!=-1: 
        print "Sample is ZJets!! Scale by " , float(14.16/41.34)
        hmc .Scale( float(14.16/41.34))
      hmcs.append(hmc)
      
    for i,fsig in enumerate(fsigs ): 
      htmp = fsig.Get(histname);
      hsig = copy.deepcopy(htmp)
      hsig.SetName(fsig.GetName()+"_"+histname+"_hsig"); 
      hsig.Scale(float(lumi)) ; 
      hsigs.append(hsig);
    
    
   
    fdata = ROOT.TFile.Open ( dir + data ,'READ')
    hdata = copy.deepcopy(fdata.Get(h))
    hdata .SetName(histname+"hdata")
  
    
    
    fqcd  = ROOT.TFile.Open ( dir + qcd ,'READ')   
    hqcd = copy.deepcopy(fqcd.Get(histname))
    hqcd .SetName(histname+"hqcd")
   
    hqcd.Scale(lumi)
    
    minorbkgs = 0.
    for h in hmcs: 
      minorbkgs += h.Integral()
    SF = float(((hdata.Integral()-minorbkgs)/hqcd.Integral()))
    print "QCD scalefactor = ", SF
    hqcd.Scale(SF)
    hqcd.SetFillColor(36)
    c = [ROOT.kMagenta+2,ROOT.kOrange+7,ROOT.kGreen+2]
    s = [1,2,9]*3
    for i,h in enumerate (hsigs):
      h.Scale(0.2*(hdata.Integral()/h.Integral()))
      h.SetLineColor(c[i]);
      h.SetLineStyle(s[i]);
      h.SetFillColor(0)

    c = [629,21,47]*3
    for i,h in enumerate(hmcs): h.SetFillColor(c[i])
    
    canvas, legend = getCanvas(histname)
    canvas.Range(0,0,1,1)

    # ratio pad
    c1_1 = GetRatioPad()
    canvas.cd()

    #main pad
    c1_2 = GetMainPad()
 
    logY = 0
    if histname.find("Dijet")!=-1 or histname.find("_jet_p_T")!=-1: 
      logY=1
      for h in hsigs: h.Scale(0.0002)
      # if histname.find("Dijet")!=-1:
 #           #hmc =  hmc.Rebin(len(xbins)-1 ,"hmc_rebinned",xbins)
 #           #for h in hsigs: h.Rebin(2).Rebin(len(xbins)-1,"hsig_rebinned",xbins)
 #           #hdata= hdata.Rebin(len(xbins)-1,"hdata_rebinned",xbins)
 #         for h in hsigs: h.Rebin(2)
 #         hdata.GetYaxis().SetTitle("Events / 200 GeV")
    
    legend.AddEntry(hdata ,legDat,"LEP")
    legend.AddEntry(hqcd  ,legqcd,"F")
    for h,leg in zip(hmcs,legMCs)  : legend.AddEntry(h,leg,"F")
    for h,leg in zip(hsigs,legSigs): legend.AddEntry(h,leg,"L")
    c1_2.cd()
    
    hdata.GetXaxis().SetLabelSize(0.)
    hdata.GetXaxis().SetTitleSize(0.)
    hdata.Draw("EP")
    hmcs.reverse()
    ths1 = ROOT.THStack ("test1","test1")
    for hh in hmcs: 
      ths1.Add(hh)
    ths1.Add(hqcd)
    ths1.Draw("HISTsame")
    for h in hsigs: 
      h.Draw("HISTCSAME")
    hdata.Draw("EPSAME")
    maxY = hdata.GetMaximum()*1.6
    hdata.GetYaxis().SetRangeUser(0.0,maxY)
    hdata.GetYaxis().SetTitleSize(0.04)
    xtitle = hdata.GetXaxis().GetTitle().replace("Leading jet","Jet 1").replace("Second leading jet","Jet 2")
    hdata.GetXaxis().SetTitle(xtitle)
    if logY:
      c1_2.SetLogy()
      maxY = maxY*100
      hdata.GetYaxis().SetRangeUser(0.1,maxY)

    
    legend.Draw()

    cmslabel_prelim(c1_2,'2017',11)
    canvas.Update()
    
    c1_1.cd()
    hsum = hqcd.Clone("qcdhist%i" %random.randint(0,10000))
    for h in hmcs: 
      hsum.Add(h)
    ratiohist = hdata.Clone("ratiohist%i" %random.randint(0,10000))
    ratiohist.Divide(hsum)
    ratiohist.SetMarkerColor(1)
    # ratiohist.SetLineColor(1)
    ratiohist.SetMarkerSize(1)
    ratiohist.GetXaxis().SetLabelSize(0.14)
    ratiohist.GetXaxis().SetTitleSize(0.17)
    ratiohist.GetXaxis().SetTitleOffset(0.)
    ratiohist.GetYaxis().SetLabelSize(0.14)
    ratiohist.GetYaxis().SetTitleSize(0.16)
    ratiohist.GetYaxis().SetTitleOffset(0.2)
    ratiohist.GetYaxis().CenterTitle()
    ratiohist.GetYaxis().SetTitle("Data/MC")
    ratiohist.GetXaxis().SetTitle(xtitle)
    ratiohist.GetYaxis().SetRangeUser(0.2,1.8)
    ratiohist.SetNdivisions(505,"x")
    ratiohist.SetNdivisions(105,"y")
    ratiohist.Draw("")
    ratiohist.GetXaxis().SetTitleOffset(0.98)
    canvas.Update()
    c1_2.RedrawAxis()
    oname = directory+"/"+canvas.GetName()+"_htbinned"
    canvas.SaveAs(oname+".pdf")
    canvas.SaveAs(oname+".png")
    canvas.SaveAs(oname+".C")
    # sleep(100)
    
if __name__ == '__main__':
  #2017 names
  BulkGravWWTemplate ="BulkGravToWW_narrow_M_2000."
  BulkGravZZTemplate ="BulkGravToZZ_narrow_M_2000."
  WprimeTemplate     ="WprimeToWZToWhadZhad_narrow_M_2000."
  
  # #2016 names
  # BulkGravWWTemplate ="BulkGravToWW_narrow_2000"
  # BulkGravZZTemplate ="BulkGravToZZToZhadZhad_narrow_2000"
  # WprimeTemplate     ="WprimeToWZToWhadZhad_narrow_2000"
  
  dataTemplate       ="JetHT"
  nonResTemplate     ="QCD_HT"
  WJetsTemplate     ="WJetsToQQ_HT800toInf."
  ZJetsTemplate     ="ZJetsToQQ_HT800toInf"
  ttTemplate        ="TTHad_pow"

  wait = True
  from modules.submitJobs import submitCPs
  template=','.join([BulkGravWWTemplate, BulkGravZZTemplate, WprimeTemplate, nonResTemplate,ttTemplate,WJetsTemplate,ZJetsTemplate,dataTemplate])
  
   
  pwd = os.getcwd()
  # samples = pwd +"/samples" #For 2016 CPs
  samples = '/eos/cms/store/cmst3/group/exovv/VVtuple/VV3Dproduction/2017_JEC_V4/' #For 2017 CPs
  samples = '/eos/cms/store/cmst3/group/exovv/VVtuple/VV3Dproduction/2017_JEC_V6/'
  samples = '/eos/user/t/thaarres/2017_JECV6_PURew/'
  jobname = "noW"
  # submitCPs(samples,template,wait,jobname)
  # mergeCPs(template,jobname)
  dir = "res"+jobname+"/"
  plot(dir,"data.root" , "qcdht.root",["controlplots_2017_TTHad_pow.root",'controlplots_2017_WJetsToQQ_HT800toInf.root','controlplots_2017_ZJetsToQQ_HT800toInf.root'] , ["controlplots_2017_WprimeToWZToWhadZhad_narrow_M_2000.root"  , "controlplots_2017_BulkGravToWW_narrow_M_2000.root" , "controlplots_2017_BulkGravToZZ_narrow_M_2000.root"],"Data (2017)" , "QCD HT-binned",["t#bar{t}","W+jets","Z+jets"] , ["W'(2 TeV)#rightarrowWZ" , "G_{Bulk}(2 TeV)#rightarrowWW" , "G_{Bulk}(2 TeV)#rightarrowZZ"])
  # plot(dir,"data.root" , "QCD_Pt_15to7000_TuneCUETHS1_Flat.root_out.root",["TTHad_pow.root_out.root",'WJetsToQQ_HT800toInf.root_out.root','WJetsToQQ_HT800toInf.root_out.root'] , ["WprimeToWZToWhadZhad_narrow_M_2000.root_out.root"  , "BulkGravToWW_narrow_M_2000.root_out.root" , "BulkGravToZZ_narrow_M_2000.root_out.root"],"Data (2017)" , "QCD HT-binned",["t#bar{t}","W+jets","Z+jets"] , ["W'(2 TeV)#rightarrowWZ" , "G_{Bulk}(2 TeV)#rightarrowWW" , "G_{Bulk}(2 TeV)#rightarrowZZ"])
