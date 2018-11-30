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


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=1)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="1")
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary

samples={}
graphs={'mean':ROOT.TGraphErrors(),'sigma':ROOT.TGraphErrors(),'alpha':ROOT.TGraphErrors(),'n':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors(),'alpha2':ROOT.TGraphErrors(),'n2':ROOT.TGraphErrors(),'slope':ROOT.TGraphErrors()}
if options.sample.find("hbb")!=-1:
    graphs={'mean':ROOT.TGraphErrors(),'sigma':ROOT.TGraphErrors(),'alpha':ROOT.TGraphErrors(),'n':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors(),'meanH':ROOT.TGraphErrors(),'sigmaH':ROOT.TGraphErrors(),'alphaH':ROOT.TGraphErrors(),'nH':ROOT.TGraphErrors()} 
for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        
    if fname.split('_')[-1].find("HT")!=-1:
        mass = 1500
    else:
        mass = float(fname.split('_')[-1])
    
    if mass < options.minMX or mass > options.maxMX: continue	

        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 

leg = options.mvv.split('_')[1]

#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
#    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
#    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.triggerW == True:
        plotter.addCorrectionFactor('triggerWeight','tree')
       
        
    fitter=Fitter(['x'])
    if options.doExp==1:
            fitter.jetResonance('model','x')
    else:
            if options.sample.find("hbb")!=-1:
                fitter.jetDoublePeakH("model",'x')
                print "use double peak for H -> bb and W"
            else:
                fitter.jetResonanceNOEXP('model','x')

    print options.sample
    if options.fixPars!="1":
        fixedPars =options.fixPars.split(',')
        for par in fixedPars:
            parVal = par.split(':')
	    if len(parVal) > 1:
             fitter.w.var(parVal[0]).setVal(float(parVal[1]))
             fitter.w.var(parVal[0]).setConstant(1)
             print "set value constant "+str(parVal[0])


#    fitter.w.var("MH").setVal(mass)
    print options.mvv
    print options.mini
    print options.maxi
    histo = plotter.drawTH1(options.mvv,options.cut,"1",80,options.mini,options.maxi)

    fitter.importBinnedData(histo,['x'],'data')
    if options.sample.find("hbb")!=-1:
        window = {1200:[2.1,2.6,3,3.4], 1400: [2,2.4,2.7,3.4],1600:[1.7,2.3,2.6,3.3],1800:[1.7,2.3,2.5,3.1],2000:[1.6,2,2.5,3], 2500:[1.3,1.8,2.3,2.9],3000:[1.2,1.7,2.1,2.6],3500:[1,1.5,2,2.5], 4000:[0.7,1.5,1.7,2.4],4500:[0.6,1.3,1.6,2.3] }
        
        
        gauss  = ROOT.TF1("gauss" ,"gaus",window[mass][0],window[mass][1])
        histo.Fit(gauss,"R")
        mean = gauss.GetParameter(1)
        sigma = gauss.GetParameter(2)
        print "set paramters of double CB constant aground the ones from gaussian fit"
        fitter.w.var("mean").setVal(mean)
        fitter.w.var("mean").setConstant(1)
        #fitter.w.var("sigma").setVal(sigma)
        #fitter.w.var("sigma").setConstant(1)
        
        gaussH  = ROOT.TF1("gaussH" ,"gaus",window[mass][2],window[mass][3])
        histo.Fit(gaussH,"R")
        mean = gaussH.GetParameter(1)
        sigma = gaussH.GetParameter(2)
        print "set paramters of double CB constant aground the ones from gaussian fit"
        fitter.w.var("meanH").setVal(mean)
        fitter.w.var("meanH").setConstant(1)
        fitter.w.var("sigmaH").setVal(sigma)
        fitter.w.var("sigmaH").setConstant(1)
        
    
    
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])
    fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_"+str(mass)+".png")

    for var,graph in graphs.iteritems():
        print "this was value "+str(var)
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
    N=N+1
    print "coming to here "
    
plotter.close()    
print "bla"    
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
    print "write graph "+str(name)
F.Close()
print "write output file "+str(options.output)
del graphs,plotter,fitter
            

print options.sample
