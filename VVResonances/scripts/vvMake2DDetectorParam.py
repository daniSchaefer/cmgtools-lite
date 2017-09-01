#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for gen",default='')
parser.add_option("-b","--binsx",dest="binsx",help="bins",default='')
parser.add_option("-g","--genVars",dest="genVars",help="variable for gen",default='')



(options,args) = parser.parse_args()


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
data=MergedPlotter(dataPlotters)



binsxStr=options.binsx.split(',')
binsx=[]
for b in binsxStr:
    binsx.append(float(b))

binsz=[]
for b in range(0,51):
    binsz.append(0.7+0.7*b/50.0)


scalexHisto=ROOT.TH1F("scalexHisto","scaleHisto",len(binsx)-1,array('d',binsx))
resxHisto=ROOT.TH1F("resxHisto","resHisto",len(binsx)-1,array('d',binsx))

scaleyHisto=ROOT.TH1F("scaleyHisto","scaleHisto",len(binsx)-1,array('d',binsx))
resyHisto=ROOT.TH1F("resyHisto","resHisto",len(binsx)-1,array('d',binsx))

variables=options.vars.split(',')
genVariables=options.genVars.split(',')


gaussian=ROOT.TF1("gaussian","gaus",0.5,1.5)


f=ROOT.TFile(options.output,"RECREATE")
f.cd()

superHX=data.drawTH2Binned(variables[0]+'/'+genVariables[0]+':'+genVariables[2],options.cut,"1",binsx,binsz)
superHY=data.drawTH2Binned(variables[1]+'/'+genVariables[1]+':'+genVariables[2],options.cut,"1",binsx,binsz)

for bin in range(1,superHX.GetNbinsX()+1):

    tmp=superHX.ProjectionY("q",bin,bin)
    scalexHisto.SetBinContent(bin,tmp.GetMean())
    scalexHisto.SetBinError(bin,tmp.GetMeanError())
    resxHisto.SetBinContent(bin,tmp.GetRMS())
    resxHisto.SetBinError(bin,tmp.GetRMSError())

    tmp=superHY.ProjectionY("q",bin,bin)
    scaleyHisto.SetBinContent(bin,tmp.GetMean())
    scaleyHisto.SetBinError(bin,tmp.GetMeanError())
    resyHisto.SetBinContent(bin,tmp.GetRMS())
    resyHisto.SetBinError(bin,tmp.GetRMSError())

        
scalexHisto.Write()
scaleyHisto.Write()
resxHisto.Write()
resyHisto.Write()
superHX.Write("dataX")
superHY.Write("dataY")
f.Close()    
