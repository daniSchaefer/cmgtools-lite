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
ROOT.gStyle.SetOptStat(0)

parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("--store",dest="store",type=str,help="store fitted parameters in this file",default="")
parser.add_option("--corrFactorW",dest="corrFactorW",type=float,help="add correction factor xsec",default=0.205066345)
parser.add_option("--corrFactorZ",dest="corrFactorZ",type=float,help="add correction factor xsec",default=0.09811023622)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="1")
parser.add_option("--minMVV","--minMVV",dest="minMVV",type=float,help="mVV variable",default=1)
parser.add_option("--maxMVV","--maxMVV",dest="maxMVV",type=float, help="mVV variable",default=1)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)


(options,args) = parser.parse_args()
samples={}


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


def doFits(fitter,histo,histo_nonRes,label,leg):
  params={}
  print "fitting "+histo.GetName()+" contribution "    
  exp  = ROOT.TF1("gaus" ,"gaus",55,215)  
  histo_nonRes.Fit(exp,"R")
 
  gauss  = ROOT.TF1("gauss" ,"gaus",74,94)  
  histo.Fit(gauss,"R")
  mean = gauss.GetParameter(1)
  sigma = gauss.GetParameter(2)
 
  print "____________________________________"
  print "mean "+str(mean)
  print "sigma "+str(sigma)
  print "set paramters of double CB constant aground the ones from gaussian fit"
  fitter.w.var("mean").setVal(mean)
  fitter.w.var("mean").setConstant(1)
  fitter.w.var("sigma").setVal(sigma)
  fitter.w.var("sigma").setConstant(1)
  print "_____________________________________"
  fitter.importBinnedData(histo,['x'],'data')
  fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Save(1),ROOT.RooFit.Range(55,120)]) #55,140 works well with fitting only the resonant part
 #ROOT.RooFit.Minos(ROOT.kTRUE)
  fitter.projection("model","data","x","debugJ"+leg+"_"+label+"_Res.png")
  c= ROOT.TCanvas("c","C",600,400)
  histo_nonRes.SetMarkerStyle(1)
  histo_nonRes.SetMarkerColor(ROOT.kBlack)
  histo_nonRes.GetXaxis().SetTitle("m_{jet}")
  histo_nonRes.GetYaxis().SetTitle("events")
  histo_nonRes.Draw("p")
  exp.SetLineColor(ROOT.kRed)
  exp.Draw("same")
  c.SaveAs("debugJ"+leg+"_"+label+"_nonRes.png")
  
  
  
  
  params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}, "alpha":{ "val": fitter.w.var("alpha").getVal(), "err": fitter.w.var("alpha").getError()},"alpha2":{"val": fitter.w.var("alpha2").getVal(),"err": fitter.w.var("alpha2").getError()},"n":{ "val": fitter.w.var("n").getVal(), "err": fitter.w.var("n").getError()},"n2": {"val": fitter.w.var("n2").getVal(), "err": fitter.w.var("n2").getError()}}
  params[label+"_nonRes_"+leg]={"mean": {"val":exp.GetParameter(1),"err":exp.GetParError(1)},"sigma": {"val":exp.GetParameter(2),"err":exp.GetParError(2)}}
  return params




    

label = options.output.split(".root")[0]
t  = label.split("_")
el=""
for words in t:
    if words.find("HP")!=-1 or words.find("LP")!=-1:
        continue
    el+=words+"_"
label = el

samplenames = options.sample.split(",")
for filename in os.listdir(args[0]):
    for samplename in samplenames:
        if not (filename.find(samplename)!=-1):
            continue


        fnameParts=filename.split('.')
        fname=fnameParts[0]
        ext=fnameParts[1]
        if ext.find("root") ==-1:
            continue
    
        name = fname.split('_')[0]
    
        samples[name] = fname

        print 'found',filename

sigmas=[]

params={}
legs=["l1","l2"]


plotters=[]
names = []
for name in samples.keys():
    plotters.append(TreePlotter(args[0]+'/'+samples[name]+'.root','tree'))
    plotters[-1].setupFromFile(args[0]+'/'+samples[name]+'.pck')
    plotters[-1].addCorrectionFactor('xsec','tree')
    plotters[-1].addCorrectionFactor('genWeight','tree')
    plotters[-1].addCorrectionFactor('puWeight','tree')
    if options.triggerW: plotters[-1].addCorrectionFactor('triggerWeight','tree')	
    corrFactor = options.corrFactorW
    if samples[name].find('Z') != -1: corrFactor = options.corrFactorZ
    if samples[name].find('W') != -1: corrFactor = options.corrFactorW
    plotters[-1].addCorrectionFactor(corrFactor,'flat')
    

print samplenames
print samples
print samples.keys()
    
print 'Fitting Mjet:' 

for leg in legs:
 histos = {}
 histos_nonRes = {}
 scales={}
 scales_nonRes={}
 
 purity = "LPLP"
 if options.output.find("HPHP")!=-1:purity = "HPHP"
 if options.output.find("HPLP")!=-1:purity = "HPLP"
 
 
 fitter=Fitter(['x'])
 fitter.jetResonanceVjets('model','x')
 
 if options.fixPars!="1":
     fixedPars =options.fixPars.split(',')
     if len(fixedPars) > 0:
      print "   - Fix parameters: ", fixedPars
      for par in fixedPars:
       parVal = par.split(':')
       fitter.w.var(parVal[0]).setVal(float(parVal[1]))
       fitter.w.var(parVal[0]).setConstant(1) 
 


 for p in range(0,len(plotters)):
     key ="Wjets"
     if str(p).find("Z")!=-1: key = "Zjets"
     if str(p.find("TT")!=-1: key = "TTbar"
     histos_nonRes [key] = plotters[p].drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==0)*(jj_"+leg+"_softDrop_mass>55&&jj_"+leg+"_softDrop_mass<215)","1",80,55,215)
     histos  [key] = plotters[p].drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)*(jj_"+leg+"_softDrop_mass>55&&jj_"+leg+"_softDrop_mass<215)","1",80,55,215)
     
     histos_nonRes[key].SetName(str(p)+"_nonRes")
     histos [key].SetName(str(p))
     scales [key] = histos[key].Integral()
     scales_nonRes [key] = histos_nonRes[key].Integral()
     
     
 # combine ttbar and wjets contributions:  
 Wjets = histos["Wjets"]
 Wjets_nonRes = histos_nonRes["Wjets"]
 if histos.keys().find("TTbar")!=-1: Wjets.Add(histos["TTbar"]); Wjets_nonRes.Add(histos_nonRes["TTbar"])
 Zjets = histos["Zjets"]
 Zjets_nonRes = histos_nonRes["Zjets"]
 
 Wjets_params = doFit(fitter,Wjets,Wjets_nonRes,"Wjets+TTbar",leg)
 Zjets_params = doFit(fitter,Zjets,Zjets_nonRes,"Zjets",leg)
  
 
 fitter.drawVjets("Vjets_mjetRes_"+leg+"_"+purity+".pdf",histos,histos_nonRes,scales,scales_nonRes)
 

 params["ratio_Res_nonRes_"+leg]= {'ratio':{"val" : scales["Wjets"]/scales_nonRes["WJets"] }, 'ratio_Z': {"val": scales["Zjets"]/scales_nonRes["Zjets"]}'ratio_TT': {"val": scales["TTbar"]/scales_nonRes["TTbar"]}}
     
        
if options.store!="":
    f=open(options.store,"w")
    for par in params:
        f.write(str(par)+ " = " +str(params[par])+"\n")

 

 #fitter.importBinnedData(histo,['x'],'data')
 #fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Save(1),ROOT.RooFit.Range(55,120)])
 #fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_Res.png")

 #fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_Res.root")
 #if options.output.find("TT")!=-1: 
   #params[label+"_Res_"+leg]={"meanW": {"val": fitter.w.var("meanW").getVal(), "err": fitter.w.var("meanW").getError()},"meanW": {"val": fitter.w.var("meanTop").getVal(), "err": fitter.w.var("meanTop").getError()}, "sigmaW": {"val": fitter.w.var("sigmaW").getVal(), "err": fitter.w.var("sigmaW").getError()}, "sigmaTop": {"val": fitter.w.var("sigmaTop").getVal(), "err": fitter.w.var("sigmaTop").getError()}, "alphaW":{ "val": fitter.w.var("alphaW").getVal(), "err": fitter.w.var("alphaW").getError()},"alphaW2":{"val": fitter.w.var("alphaW2").getVal(), "err": fitter.w.var("alphaW2").getError()},"alphaTop":{ "val": fitter.w.var("alphaTop").getVal(), "err": fitter.w.var("alphaTop")},"alphaTop2":{"val": fitter.w.var("alphaTop2").getVal(),"err": fitter.w.var("alpha2").getError()},"n":{ "val": fitter.w.var("n").getVal(), "err": fitter.w.var("n").getError()}}
 #else:
   #params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}, "alpha":{ "val": fitter.w.var("alpha").getVal(), "err": fitter.w.var("alpha")},"alpha2":{"val": fitter.w.var("alpha2").getVal(),"err": fitter.w.var("alpha2").getError()},"n":{ "val": fitter.w.var("n").getVal(), "err": fitter.w.var("n").getError()},"n2": {"val": fitter.w.var("n2").getVal(), "err": fitter.w.var("n2").getError()}}
   ##params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}}

