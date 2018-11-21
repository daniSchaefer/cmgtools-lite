#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    

def getBinning(binsMVV,minx,maxx,bins):
    l=[]
    if binsMVV=="":
        for i in range(0,bins+1):
            l.append(minx + i* (maxx - minx)/bins)
        
    else:
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
            
    return l

def truncate(binning,mmin,mmax):
    res=[]
    for b in binning:
        if b >= mmin and b <= mmax:
            res.append(b)
    return res

parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='1')
parser.add_option("--fix",dest="fixPars",help="Fixed parameters",default="")
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary

samples={}
graphs={'MEAN':ROOT.TGraphErrors(),'SIGMA':ROOT.TGraphErrors(),'ALPHA':ROOT.TGraphErrors(),'N':ROOT.TGraphErrors(),'SCALESIGMA':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors()}

for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        
    
    mass = float(fname.split('_')[-1])
    if mass < options.minMX or mass > options.maxMX: continue
        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 



scaleFactors=options.scaleFactors.split(',')


#Now we have the samples: Sort the masses and run the fits
N=0

Fhists=ROOT.TFile("massHISTOS_"+options.output,"RECREATE")

for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.triggerW: plotter.addCorrectionFactor('triggerWeight','tree')	
    if options.scaleFactors!='':
        for s in scaleFactors:
            plotter.addCorrectionFactor(s,'tree')
       
    fitter=Fitter(['MVV'])
    fitter.signalResonanceCBGaus('model','MVV',mass)
    #if options.fixPars!="":
    if options.fixPars!="1":
        fixedPars =options.fixPars.split(',')
        print fixedPars
        for par in fixedPars:
            parVal = par.split(':')
	    if len(parVal) > 1:
             fitter.w.var(parVal[0]).setVal(float(parVal[1]))
             fitter.w.var(parVal[0]).setConstant(1)
    fitter.w.var("MH").setVal(mass)

    binning= truncate(getBinning(options.binsMVV,options.min,options.max,1000),0.75*mass,1.25*mass)    
    histo = plotter.drawTH1Binned(options.mvv,options.cut+"*(jj_LV_mass>%f&&jj_LV_mass<%f)"%(0.75*mass,1.25*mass),"1",binning)

    #gauss  = ROOT.TF1("gauss" ,"gaus",0.95*mass,1.05*mass)  
    #histo.Fit(gauss,"R")
    #mean = gauss.GetParameter(1)
    #sigma = gauss.GetParameter(2)
 
    #print "____________________________________"
    #print "mean "+str(mean)
    #print "sigma "+str(sigma)
    #print "set paramters of double CB constant aground the ones from gaussian fit"
    #fitter.w.var("mean").setVal(mean)
    #fitter.w.var("mean").setConstant(1)
    #fitter.w.var("sigma").setVal(sigma)
    #fitter.w.var("sigma").setConstant(1)
    #print "_____________________________________"



    Fhists.cd()
    histo.Write("%i"%mass)

    fitter.importBinnedData(histo,['MVV'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])

    roobins = ROOT.RooBinning(len(binning)-1,array("d",binning))
    fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".png",roobins)

    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
Fhists.Write()
Fhists.Close()        
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()

del graphs,plotter,fitter
            
