#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import copy
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")

parser = optparse.OptionParser()
parser.add_option("-i","--infile",dest="infile",help="Infile",default='')
parser.add_option("-H","--weightHisto",dest="weightHisto",help="res",default='trigWeight.root')

(options,args) = parser.parse_args()

fWeights=ROOT.TFile(options.weightHisto)
weights = fWeights.Get("h_eff_exp")

def getBinning(histo):
    b = []
    for i in range(1,histo.GetNbinsX()+2):
        b.append(histo.GetBinLowEdge(i))
    return array('d',b)
        
infile=ROOT.TFile(options.infile,"UPDATE")
for key in infile.GetListOfKeys():
        kname = key.GetName()
        if "TRIG" in kname:
                print "Deleting ", kname
                infile.Delete(kname)
                infile.Delete(kname+";*")

histo = infile.Get("histo")
hx = histo.ProjectionX("projX")
hz = histo.ProjectionZ("projZ")
binningx= getBinning(hx)
binningz= getBinning(hz)
    
scaleUP   = ROOT.TH3F("histo_TRIGUp"  ,"histo_TRIGUp"  ,len(binningx)-1,binningx,len(binningx)-1,binningx,len(binningz)-1,binningz)
scaleDOWN = ROOT.TH3F("histo_TRIGDown","histo_TRIGDown",len(binningx)-1,binningx,len(binningx)-1,binningx,len(binningz)-1,binningz)

for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
                for k in range(1,histo.GetNbinsZ()+1):

                        mj1 = histo.GetXaxis().GetBinCenter(i)
                        mj2 = histo.GetYaxis().GetBinCenter(j)
                        mjj = histo.GetZaxis().GetBinCenter(k)
                        # print "mj1 = " ,mj1; print "mj2 = " ,mj2; print "mjj = " ,mjj
                        tw = weights.GetBinContent(weights.GetXaxis().FindBin(mj1), weights.GetYaxis().FindBin(mj2), weights.GetZaxis().FindBin(mjj))
                        c = histo.GetBinContent(i,j,k)
                        # print "bin content = " ,c ; print "tw = " ,tw
                        # print "SCALE UP bin content = " ,c/tw ; print "SCALE DOWN bin content = " ,c*tw
                        scaleUP  .SetBinContent(i,j,k,(c/tw))
                        scaleDOWN.SetBinContent(i,j,k,(c*tw))
            

print " Trigger weights done! Saving everything to " ,infile.GetName()
# f=ROOT.TFile(options.outfile,"RECREATE")
infile.cd()
scaleUP   .Write(scaleUP   .GetName())
scaleDOWN .Write(scaleDOWN .GetName())


infile.Close()