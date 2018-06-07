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
parser.add_option("--corrFactorW",dest="corrFactorW",type=float,help="add correction factor xsec",default=1.)
parser.add_option("--corrFactorZ",dest="corrFactorZ",type=float,help="add correction factor xsec",default=41.34/581.8)
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
NRes = [0,0]
NnonRes= [0,0]
legs=["l1","l2"]


#dataPlotters=[]
#dataPlottersNW=[]
#for name in samples.keys():
   
            #dataPlotters.append(TreePlotter(args[0]+'/'+samples[name]+'.root','tree'))
            #dataPlotters[-1].setupFromFile(args[0]+'/'+samples[name]+'.pck')
            #dataPlotters[-1].addCorrectionFactor('xsec','tree')
            #dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            #dataPlotters[-1].addCorrectionFactor('puWeight','tree')
            
            #dataPlotters[-1].filename=fname
            #dataPlottersNW.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            #dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
            #dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
            
            #dataPlottersNW[-1].filename=fname



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
    if samples[name].find('Z') != -1: 
        corrFactor = options.corrFactorZ
        names.append("Z+jets")
    if samples[name].find('W') != -1: 
        corrFactor = options.corrFactorW
        names.append("W+jets")
    if samples[name].find('TT') != -1: 
        names.append("t #bar{t}")
    plotters[-1].addCorrectionFactor(corrFactor,'flat')
    

print samplenames
print samples
print samples.keys()
    
#plotter=MergedPlotter(dataPlotters)        

print 'Fitting Mjet:' 

for leg in legs:
 tmp=[]
 fitter=Fitter(['x'])
 fitter.jetResonanceVjets('model','x')
 #fitter.gaus('model','x')

 if options.fixPars!="1":
     fixedPars =options.fixPars.split(',')
     if len(fixedPars) > 0:
      print "   - Fix parameters: ", fixedPars
      for par in fixedPars:
       if par=="c_0" or par =="c_1" or par=="c_2": continue
       parVal = par.split(':')
       fitter.w.var(parVal[0]).setVal(float(parVal[1]))
       fitter.w.var(parVal[0]).setConstant(1)

 #histo = plotter.drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)","1",80,options.mini,options.maxi)
 
 histo = ROOT.TH1F("res","resonant backgrounds",30,55,125)

 c = ROOT.TCanvas("c","c",400,400)
 stack = ROOT.THStack("stackplot","stackplot")
 
 c.SetLeftMargin(0.15)
 legend = ROOT.TLegend(0.6,0.7,0.8,0.8)
 histo.SetLineColor(ROOT.kBlack)
 #histo.Draw("hist")
 print "number of plotter "+str(len(plotters))
 for p in range(0,len(plotters)):
     tmp .append( plotters[p].drawTH1("jj_"+leg+"_softDrop_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)*(jj_"+leg+"_softDrop_mass>55&&jj_"+leg+"_softDrop_mass<215)","1",30,55,125))
     tmp[-1].SetName(str(p))
     tmp[-1].SetFillColorAlpha(ROOT.kBlue,0.6)
     tmp[-1].SetLineColor(ROOT.kBlue)
     text = names[p]
     if p==0:
         tmp[-1].SetLineColor(ROOT.kRed)
         tmp[-1].SetFillColorAlpha(ROOT.kRed, 0.6)
         tmp[-1].SetMaximum(0.006)

     if p==2:
         tmp[-1].SetLineColor(ROOT.kGreen)
         tmp[-1].SetFillColorAlpha(ROOT.kGreen, 0.6)
         
     legend.AddEntry(tmp[-1],text ,"l")
     #tmp[-1].Draw("histsame")
     print tmp[-1].Integral()
 print tmp
 for t in range(0,len(tmp)):
     histo.Add(tmp[t])
     stack.Add(tmp[t])
 print histo.Integral()
 if leg.find("l1")!=-1:
     NRes[0] += histo.Integral()
 else:
     NRes[1] += histo.Integral()
 
 
 fitter.importBinnedData(histo,['x'],'data')
 fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Save(1)])
 #ROOT.RooFit.Minos(ROOT.kTRUE)
 
 histo.Draw()
 histo.GetXaxis().SetTitle("m_{jet}")
 histo.GetYaxis().SetTitle("arbitrary scale")
 histo.GetYaxis().SetTitleOffset(1.55)
 stack.Draw("histsame")
 legend.Draw("same")
 histo.Draw("same")
 c.SaveAs("test.pdf")
 

 fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_Res.png")
 params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}, "alpha":{ "val": fitter.w.var("alpha").getVal(), "err": fitter.w.var("alpha")},"alpha2":{"val": fitter.w.var("alpha2").getVal(),"err": fitter.w.var("alpha2").getError()},"n":{ "val": fitter.w.var("n").getVal(), "err": fitter.w.var("n").getError()},"n2": {"val": fitter.w.var("n2").getVal(), "err": fitter.w.var("n2").getError()}}
 
 
 #params[label+"_Res_"+leg]={"mean": {"val": fitter.w.var("mean").getVal(), "err": fitter.w.var("mean").getError()}, "sigma": {"val": fitter.w.var("sigma").getVal(), "err": fitter.w.var("sigma").getError()}}

 #if leg.find("l1")!=-1:
     #NnonRes[0] += histo.Integral()
 #else:
     #NnonRes[1] += histo.Integral()
          
#print 'fitting MJJ: ' 

#fitter=Fitter(['MVV'])
#fitter.qcd('model','MVV',False)

#if options.fixPars!="":
    #fixedPars =options.fixPars.split(',')
    #for par in fixedPars:
     #if len(fixedPars) > 1:
        #if par!="c_0" and par!="c_1" and par!="c_2": continue
        #parVal = par.split(':')
        #fitter.w.var(parVal[0]).setVal(float(parVal[1]))
        #fitter.w.var(parVal[0]).setConstant(1)

#binning=getBinning(options.binsMVV,options.minMVV,options.maxMVV,1000)
#roobins = ROOT.RooBinning(len(binning)-1,array("d",binning))
#histo = plotter.drawTH1Binned("jj_LV_mass",options.cut+"*(jj_"+leg+"_mergedVTruth==1)","1",binning)
##histo.Scale(40000.)
#fitter.importBinnedData(histo,['MVV'],'data')
#fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Save(1)])
##fitter.projection("model","data",'MVV',"debugMVV_"+options.output+".png",roobins)
#fitter.projection("model","data",'MVV',"debugMVV_log_"+options.output+".png",roobins,True)
#print "save plot "+"debugMVV_log_"+options.output+".png"
#params[label+"_MVV"]={"CMS_p0": {"val":fitter.w.var("c_0").getVal(), "err":fitter.w.var("c_0").getError() }, "CMS_p1":{ "val": fitter.w.var("c_1").getVal(), "err": fitter.w.var("c_1").getError()}, "CMS_p2":{ "val":  fitter.w.var("c_2").getVal(), "err": fitter.w.var("c_2").getError()}}
    

        
if options.store!="":
    f=open(options.store,"w")
    for par in params:
        f.write(str(par)+ " = " +str(params[par])+"\n")
    #print NRes
    #print NnonRes
    #f.write(label+"_ratio_l1 = "+str(NRes[0]/(NRes[0]+NnonRes[0]))+"\n")
    #f.write(label+"_ratio_l2 = "+str(NRes[1]/(NRes[1]+NnonRes[1]))+"\n")

