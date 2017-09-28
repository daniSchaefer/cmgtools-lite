import ROOT
from ROOT import *
import sys, os, time, optparse
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

def diffTrees(t,T,tname,Tname,debug):

 nEv = 0
 common = 0
 for e in range(t.GetEntries()):
 
  t.GetEntry(e)
  ev = t.evt
  lumi = t.lumi
  if T.GetEntries("lumi==%i&&evt==%i"%(lumi,ev)) == 0:
  
   nEv+=1
   if debug:
    print "Event %i Lumi %i not found in %s ntuple, show variables for %s ntuple:"%(ev,lumi,Tname,tname)
    print "gen mjj %.2f"%(t.jj_gen_partialMass[0])
    print "reco mjj %.2f"%(t.jj_LV_mass[0])
    print "l1 gen softdrop mass %.2f"%(t.jj_l1_gen_softDrop_mass[0])
    print "l1 reco softdrop mass %.2f"%(t.jj_l1_softDrop_mass[0])
    print "l1 gen pt %.2f"%(t.jj_l1_gen_pt[0])
    print "l1 reco pt %.2f"%(t.jj_l1_pt[0])
    print "l2 gen softdrop mass %.2f"%(t.jj_l2_gen_softDrop_mass[0])
    print "l2 reco softdrop mass %.2f"%(t.jj_l2_softDrop_mass[0])
    print "l2 gen pt %.2f"%(t.jj_l2_gen_pt[0])
    print "l2 reco pt %.2f"%(t.jj_l2_pt[0])
  
  else: common+=1
  
 return [nEv,common] 

parser = optparse.OptionParser()
parser.add_option("-f","--file1",dest="fname1",help="Name of the first file",default='CMGtree.root')
parser.add_option("-F","--file2",dest="fname2",help="Name of the second file",default='VVanalysis.QstarQW.synchM2000.root')
parser.add_option("-t","--treename",dest="tname",help="Name of the tree in the files",default='tree')
parser.add_option("-d","--debug",dest="debug",help="Debug print out",type=int,default=0)
(options,args) = parser.parse_args() 

#cmg tree
f1 = TFile.Open(options.fname1,'READ')
t1 = f1.Get(options.tname)
n1 = t1.GetEntries()

#uzh tree
f2 = TFile.Open(options.fname2,'READ')
t2 = f2.Get(options.tname)
n2 = t2.GetEntries()

print "Events in %s ntuple: %i"%(options.fname1.replace('.root',''),n1)
print "Events in %s ntuple: %i"%(options.fname2.replace('.root',''),n2)
events = diffTrees(t1,t2,options.fname1.replace('.root',''),options.fname2.replace('.root',''),options.debug)
print "Events in %s ntuple NOT present in %s ntuple: %i"%(options.fname1.replace('.root',''),options.fname2.replace('.root',''),events[0])
events = diffTrees(t2,t1,options.fname2.replace('.root',''),options.fname1.replace('.root',''),options.debug)
print "Events in %s ntuple NOT present in %s ntuple: %i"%(options.fname2.replace('.root',''),options.fname1.replace('.root',''),events[0])
print "Common events: ",events[1]

#connect the two ntuples
t1.BuildIndex("lumi","evt")
t2.BuildIndex("lumi","evt")
t1.AddFriend(t2)

#book synch histos
h_gen_jj_mass_1 = ROOT.TH1F("h_gen_jj_mass_1","gen mJJ",200,0,5000)
h_gen_jj_mass_2 = ROOT.TH1F("h_gen_jj_mass_2","gen mJJ",200,0,5000)
h_l1_gen_mass_1 = ROOT.TH1F("h_l1_gen_mass_1","l1 gen softdrop mass",200,0,600)
h_l1_gen_mass_2 = ROOT.TH1F("h_l1_gen_mass_2","l1 gen softdrop mass",200,0,600)
h_l2_gen_mass_1 = ROOT.TH1F("h_l2_gen_mass_1","l2 gen softdrop mass",200,0,600)
h_l2_gen_mass_2 = ROOT.TH1F("h_l2_gen_mass_2","l2 gen softdrop mass",200,0,600)
h_l1_gen_pt_1 = ROOT.TH1F("h_l1_gen_pt_1","l1 gen pt",200,0,5000)
h_l1_gen_pt_2 = ROOT.TH1F("h_l1_gen_pt_2","l1 gen pt",200,0,5000)
h_l2_gen_pt_1 = ROOT.TH1F("h_l2_gen_pt_1","l2 gen pt",200,0,5000)
h_l2_gen_pt_2 = ROOT.TH1F("h_l2_gen_pt_2","l2 gen pt",200,0,5000)

h_reco_jj_mass_1 = ROOT.TH1F("h_reco_jj_mass_1","reco mJJ",200,0,5000)
h_reco_jj_mass_2 = ROOT.TH1F("h_reco_jj_mass_2","reco mJJ",200,0,5000)
h_l1_reco_mass_1 = ROOT.TH1F("h_l1_reco_mass_1","l1 reco softdrop mass",200,0,600)
h_l1_reco_mass_2 = ROOT.TH1F("h_l1_reco_mass_2","l1 reco softdrop mass",200,0,600)
h_l2_reco_mass_1 = ROOT.TH1F("h_l2_reco_mass_1","l2 reco softdrop mass",200,0,600)
h_l2_reco_mass_2 = ROOT.TH1F("h_l2_reco_mass_2","l2 reco softdrop mass",200,0,600)
h_l1_reco_pt_1 = ROOT.TH1F("h_l1_reco_pt_1","l1 reco pt",200,0,5000)
h_l1_reco_pt_2 = ROOT.TH1F("h_l1_reco_pt_2","l1 reco pt",200,0,5000)
h_l2_reco_pt_1 = ROOT.TH1F("h_l2_reco_pt_1","l2 reco pt",200,0,5000)
h_l2_reco_pt_2 = ROOT.TH1F("h_l2_reco_pt_2","l2 reco pt",200,0,5000)

n=0
for e in range(n1):

 t1.GetEntry(e)
 if t1.evt == t2.evt and t1.lumi == t2.lumi:
 
  if options.debug:
   print "------ Lumi ", t1.lumi," Event ", t1.evt,"------"
   print "UZH/CMG variables:"
   print "gen mjj %.2f/%.2f"%(t2.jj_gen_partialMass,t1.jj_gen_partialMass[0])
   print "reco mjj %.2f/%.2f"%(t2.jj_LV_mass,t1.jj_LV_mass[0])
   print "l1 gen softdrop mass %.2f/%.2f"%(t2.jj_l1_gen_softDrop_mass,t1.jj_l1_gen_softDrop_mass[0])
   print "l1 reco softdrop mass %.2f/%.2f"%(t2.jj_l1_softDrop_mass,t1.jj_l1_softDrop_mass[0])
   print "l1 gen pt %.2f/%.2f"%(t2.jj_l1_gen_pt,t1.jj_l1_gen_pt[0])
   print "l1 reco pt %.2f/%.2f"%(t2.jj_l1_pt,t1.jj_l1_pt[0])
   print "l2 gen softdrop mass %.2f/%.2f"%(t2.jj_l2_gen_softDrop_mass,t1.jj_l2_gen_softDrop_mass[0])
   print "l2 reco softdrop mass %.2f/%.2f"%(t2.jj_l2_softDrop_mass,t1.jj_l2_softDrop_mass[0])
   print "l2 gen pt %.2f/%.2f"%(t2.jj_l2_gen_pt,t1.jj_l2_gen_pt[0])
   print "l2 reco pt %.2f/%.2f"%(t2.jj_l2_pt,t1.jj_l2_pt[0])
      
  h_gen_jj_mass_1.Fill(t1.jj_gen_partialMass[0])
  h_gen_jj_mass_2.Fill(t2.jj_gen_partialMass)
  
  h_l1_gen_mass_1.Fill(t1.jj_l1_gen_softDrop_mass[0])
  h_l1_gen_mass_2.Fill(t2.jj_l1_gen_softDrop_mass)    
  h_l2_gen_mass_1.Fill(t1.jj_l2_gen_softDrop_mass[0])
  h_l2_gen_mass_2.Fill(t2.jj_l2_gen_softDrop_mass)

  h_l1_gen_pt_1.Fill(t1.jj_l1_gen_pt[0])
  h_l1_gen_pt_2.Fill(t2.jj_l1_gen_pt)    
  h_l2_gen_pt_1.Fill(t1.jj_l2_gen_pt[0])
  h_l2_gen_pt_2.Fill(t2.jj_l2_gen_pt)

  h_reco_jj_mass_1.Fill(t1.jj_LV_mass[0])
  h_reco_jj_mass_2.Fill(t2.jj_LV_mass)
  
  h_l1_reco_mass_1.Fill(t1.jj_l1_softDrop_mass[0])
  h_l1_reco_mass_2.Fill(t2.jj_l1_softDrop_mass)    
  h_l2_reco_mass_1.Fill(t1.jj_l2_softDrop_mass[0])
  h_l2_reco_mass_2.Fill(t2.jj_l2_softDrop_mass)

  h_l1_reco_pt_1.Fill(t1.jj_l1_pt[0])
  h_l1_reco_pt_2.Fill(t2.jj_l1_pt)    
  h_l2_reco_pt_1.Fill(t1.jj_l2_pt[0])
  h_l2_reco_pt_2.Fill(t2.jj_l2_pt)
  
  n+=1

histos_1 = []
histos_2 = []

histos_1.append(h_gen_jj_mass_1)
histos_2.append(h_gen_jj_mass_2)

histos_1.append(h_l1_gen_mass_1)
histos_2.append(h_l1_gen_mass_2)
histos_1.append(h_l2_gen_mass_1)
histos_2.append(h_l2_gen_mass_2)

histos_1.append(h_l1_gen_pt_1)
histos_2.append(h_l1_gen_pt_2)
histos_1.append(h_l2_gen_pt_1)
histos_2.append(h_l2_gen_pt_2)

histos_1.append(h_reco_jj_mass_1)
histos_2.append(h_reco_jj_mass_2)

histos_1.append(h_l1_reco_mass_1)
histos_2.append(h_l1_reco_mass_2)
histos_1.append(h_l2_reco_mass_1)
histos_2.append(h_l2_reco_mass_2)

histos_1.append(h_l1_reco_pt_1)
histos_2.append(h_l1_reco_pt_2)
histos_1.append(h_l2_reco_pt_1)
histos_2.append(h_l2_reco_pt_2)

for h in range(len(histos_1)):

 histos_1[h].SetLineColor(kBlack)
 histos_1[h].SetLineWidth(2)
 histos_2[h].SetMarkerColor(kRed)
 histos_2[h].SetMarkerStyle(20)
 
 c = TCanvas("c","c")
 c.cd()
 
 pt1 = TPaveText(0.704023,0.8177966,0.9612069,0.9597458,"NDC")
 pt1.SetTextFont(42)
 pt1.SetTextSize(0.031)
 pt1.SetTextAlign(12)
 pt1.SetFillColor(0)
 text = pt1.AddText("CMG ntuple:")
 text.SetTextFont(62)
 pt1.AddText("Mean = %.2f"%(histos_1[h].GetMean()))
 pt1.AddText("RMS = %.2f"%(histos_1[h].GetRMS()))

 pt2 = TPaveText(0.704023,0.64,0.9612069,0.78,"NDC")
 pt2.SetTextColor(kRed)
 pt2.SetTextFont(42)
 pt2.SetTextSize(0.031)
 pt2.SetTextAlign(12)
 pt2.SetFillColor(0)
 text = pt2.AddText("UZH ntuple:")
 text.SetTextFont(62)
 pt2.AddText("Mean = %.2f"%(histos_2[h].GetMean()))
 pt2.AddText("RMS = %.2f"%(histos_2[h].GetRMS()))
  
 if histos_1[h].GetMaximum() < histos_2[h].GetMaximum(): histos_1[h].SetMaximum(histos_2[h].GetMaximum()+300)
 
 histos_1[h].Draw("HIST")
 histos_2[h].Draw("Psame")
 pt1.Draw()
 pt2.Draw()
 
 c.SaveAs("c_"+histos_1[h].GetName()+".png") 
 

