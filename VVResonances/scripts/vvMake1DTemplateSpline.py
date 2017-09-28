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
ROOT.gErrorIgnoreLevel = ROOT.kWarning

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-f","--factor",dest="factor",type=int,help="factor to reduce stats",default=1)

(options,args) = parser.parse_args()

def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        up=histo.GetBinContent(i)/intUp
        nominal=histoNominal.GetBinContent(i)/intNominal
        newHisto.SetBinContent(i,nominal*nominal/up)
    return newHisto         

def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        nominal=histo.GetBinContent(i)
        factor = alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD        


def expandHisto(histo,histogram):
    graph=ROOT.TGraph(histo)
    for j in range(1,histogram.GetNbinsX()+1):
        x=histogram.GetXaxis().GetBinCenter(j)
        histogram.SetBinContent(j,graph.Eval(x,0,"S"))




random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')
dataPlotters=[]

for filename in os.listdir(args[0]):
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')
            dataPlotters[-1].filename=fname
	    
data=MergedPlotter(dataPlotters)

mjet_nominal = ROOT.TH1F("mjet_nominal","mjet_nominal",options.binsx,options.minx,options.maxx)
mjet_nominal.Sumw2()

mjet_altshapeUp = ROOT.TH1F("mjet_altshapeUp","mjet_altshapeUp",options.binsx,options.minx,options.maxx)
mjet_altshapeUp.Sumw2()

mjet_altshape2 = ROOT.TH1F("mjet_altshape2","mjet_altshape2",options.binsx,options.minx,options.maxx)
mjet_altshape2.Sumw2()

histogram_nominal=ROOT.TH1F("histo_nominal","histo_nominal",options.binsx,options.minx,options.maxx)
histogram_nominal.Sumw2()

histoCoarse_nominal=ROOT.TH1F("histoCoarse_nominal","histoCoarse_nominal",options.binsx/options.factor,options.minx,options.maxx)
histoCoarse_nominal.Sumw2()

histogram_altshapeUp=ROOT.TH1F("histo_altshapeUp","histo_altshapeUp",options.binsx,options.minx,options.maxx)
histogram_altshapeUp.Sumw2()

histoCoarse_altshapeUp=ROOT.TH1F("histoCoarse_altshapeUp","histoCoarse_altshapeUp",options.binsx/options.factor,options.minx,options.maxx)
histoCoarse_altshapeUp.Sumw2()

histogram_altshape2=ROOT.TH1F("histo_altshape2","histo_altshape2",options.binsx,options.minx,options.maxx)
histogram_altshape2.Sumw2()

histoCoarse_altshape2=ROOT.TH1F("histoCoarse_altshape2","histoCoarse_altshape2",options.binsx/options.factor,options.minx,options.maxx)
histoCoarse_altshape2.Sumw2()

for plotter in dataPlotters:

 if plotter.filename.find(sampleTypes[0]) != -1: #nominal histo

  print "Preparing nominal and smoothed histograms for sampletype " ,sampleTypes[0], " and file ",plotter.filename
		 
  histoCoarseTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx/options.factor,options.minx,options.maxx)
  mjetTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx,options.minx,options.maxx)
  if mjetTMP.Integral()>0:
   mjet_nominal.Add(mjetTMP)
   histoCoarse_nominal.Add(histoCoarseTMP)
  mjetTMP.Delete() 
  histoCoarseTMP.Delete()
  
 if len(sampleTypes)<2: continue 
 elif plotter.filename.find(sampleTypes[1]) != -1: #alternative shape Herwig

  print "Preparing nominal and smoothed histograms for sampletype " ,sampleTypes[1], " and file ",plotter.filename

  histoCoarseTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx/options.factor,options.minx,options.maxx)
  mjetTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx,options.minx,options.maxx)
  if mjetTMP.Integral()>0:
   mjet_altshapeUp.Add(mjetTMP)
   histoCoarse_altshapeUp.Add(histoCoarseTMP)
  mjetTMP.Delete() 
  histoCoarseTMP.Delete()

 if len(sampleTypes)<3: continue 
 elif plotter.filename.find(sampleTypes[2]) != -1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)

  print "Preparing nominal and smoothed histograms for sampletype " ,sampleTypes[2], " and file ",plotter.filename

  histoCoarseTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx/options.factor,options.minx,options.maxx)
  mjetTMP = plotter.drawTH1(options.var,options.cut,"1",options.binsx,options.minx,options.maxx)
  if mjetTMP.Integral()>0:
   mjet_altshape2.Add(mjetTMP)
   histoCoarse_altshape2.Add(histoCoarseTMP)
  mjetTMP.Delete() 
  histoCoarseTMP.Delete()
  
#histoCoarse=data.drawTH1(options.var,options.cut,"1",options.binsx/options.factor,options.minx,options.maxx)
expandHisto(histoCoarse_nominal,histogram_nominal)
expandHisto(histoCoarse_altshapeUp,histogram_altshapeUp)
expandHisto(histoCoarse_altshape2,histogram_altshape2)

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

mjet_nominal.Write()
mjet_altshapeUp.Write()
mjet_altshape2.Write()
histoCoarse_nominal.Write()
histogram_nominal.Write()
histoCoarse_altshapeUp.Write()
histogram_altshapeUp.Write()
histogram_altshape2.Write()

histogram_altshapeDown=mirror(histogram_altshapeUp,histogram_nominal,"histo_altshapeDown")
histogram_altshapeDown.Write()

f.Close()
