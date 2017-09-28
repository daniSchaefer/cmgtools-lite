#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='')

(options,args) = parser.parse_args()
#define output dictionary

ROOT.gROOT.SetBatch(True)

samples={}
graphs={'MEAN':ROOT.TGraphErrors(),'SIGMA':ROOT.TGraphErrors(),'ALPHA':ROOT.TGraphErrors(),'N':ROOT.TGraphErrors(),'SCALESIGMA':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors()}

for filename in os.listdir(args[0]):
    print filename
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        

    mass = float(fname.split('_')[-1])

        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 



scaleFactors=options.scaleFactors.split(',')


#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):
    if mass>6000: continue
    print 'fitting',str(mass) 
    print args[0]+'/'+samples[mass]+'.root'
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.scaleFactors!='':
        for s in scaleFactors:
            plotter.addCorrectionFactor(s,'tree')
       
    fitter=Fitter(['MVV'])
    fitter.signalResonanceCBGaus('model','MVV',mass)
    fitter.w.var("MH").setVal(mass)

    histo = plotter.drawTH1(options.mvv,options.cut+"*(jj_LV_mass>%f&&jj_LV_mass<%f)"%(0.8*mass,1.2*mass),"1",140,700,8000)


    fitter.importBinnedData(histo,['MVV'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])#,ROOT.RooFit.Range(1000,8000)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])#,ROOT.RooFit.Range(1000,8000)])
    # fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])#,ROOT.RooFit.Range(1000,8000)])

    #fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".root")
    fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".png","M_{jj} (GeV)",mass)
    fitter.w.Print()
    for var,graph in graphs.iteritems():

        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
        
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
