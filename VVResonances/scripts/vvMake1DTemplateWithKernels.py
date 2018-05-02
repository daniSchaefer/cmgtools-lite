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
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-H","--resHisto",dest="resHisto",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--var",dest="var",help="variable for x",default='')
parser.add_option("-b","--bins",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("-u","--usegenmass",dest="usegenmass",action="store_true",help="use gen mass for det resolution",default=False)
parser.add_option("-e","--firstEv",dest="firstEv",type=int,help="first event",default=0)
parser.add_option("-E","--lastEv",dest="lastEv",type=int,help="last event",default=-1)

(options,args) = parser.parse_args()     


def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        up=histo.GetBinContent(i)/intUp
        nominal=histoNominal.GetBinContent(i)/intNominal
        newHisto.SetBinContent(i,histoNominal.GetBinContent(i)*nominal/up)
    return newHisto      

def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        nominal=histo.GetBinContent(i)
        factor = 1+alpha*pow(x,power) 
        newHistoU.SetBinContent(i,nominal*factor)
        newHistoD.SetBinContent(i,nominal/factor)
    return newHistoU,newHistoD 
    	
def smoothTail1D(proj):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral() 
    proj.Scale(1.0/scale)
    
    
    beginFitX = 2100
    expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000) 
    expo.SetParameters(0,16.,2.)
    expo.SetParLimits(2,1.,20.)
    proj.Fit(expo,"LLMR","",beginFitX,8000)
    c = ROOT.TCanvas("c","c",400,400)
    c.SetLogy()
    proj.Draw("hist")
    proj.Draw("funcsame")
    c.SaveAs(proj.GetName()+".pdf")
    beginsmooth = False
    print proj.GetNbinsX()+1
    for j in range(1,proj.GetNbinsX()+1):
        x=proj.GetXaxis().GetBinCenter(j)
        if x>beginFitX:
            if beginsmooth==False:
               if x<3000: 
                   if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00009:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                    print beginFitX
                    print "begin smoothing at " +str(x)
                    beginsmooth = True 
               if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                   print beginFitX
                   print "begin smoothing at " +str(x)
                   beginsmooth = True 
            if beginsmooth:
                proj.SetBinContent(j,expo.Eval(x))
    return 1
weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')

print "Creating datasets for samples: " ,sampleTypes
dataPlotters=[]
dataPlottersNW=[]
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
            for w in weights_:
	     if w != '': dataPlotters[-1].addCorrectionFactor(w,'branch')
            dataPlotters[-1].filename=fname
            dataPlottersNW.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlottersNW[-1].addCorrectionFactor('puWeight','tree')
            dataPlottersNW[-1].addCorrectionFactor('genWeight','tree')
            for w in weights_: 
             if w != '': dataPlottersNW[-1].addCorrectionFactor(w,'branch')
            dataPlottersNW[-1].filename=fname
	    
data=MergedPlotter(dataPlotters)
fcorr=ROOT.TFile(options.res)

scale = fcorr.Get("scale"+options.resHisto+"Histo")
res   = fcorr.Get("res"  +options.resHisto+"Histo")

scaleUp = ROOT.TH1F(scale)
scaleUp.SetName("scaleUp")
scaleDown = ROOT.TH1F(scale)
scaleDown.SetName("scaleDown")
for i in range(1,res.GetNbinsX()+1):
    if options.resHisto=="x":
        scaleUp.SetBinContent(i,scale.GetBinContent(i)+0.1)
        scaleDown.SetBinContent(i,scale.GetBinContent(i)-0.1)
    else:
        scaleUp.SetBinContent(i,scale.GetBinContent(i)+0.3)
        scaleDown.SetBinContent(i,scale.GetBinContent(i)-0.3)
	
#distribution of mjet from simulation --> use to validate kernel
mjet_nominal=ROOT.TH1F("mjet_nominal","mjet_nominal",options.binsx,options.minx,options.maxx)
mjet_nominal.Sumw2()
histogram_nominal=ROOT.TH1F("histo_nominal","histo_nominal",options.binsx,options.minx,options.maxx)
histogram_nominal.Sumw2()
histogram_nominal_scale_up=ROOT.TH1F("histo_nominal_ScaleUp","histo_nominal_ScaleUp",options.binsx,options.minx,options.maxx)
histogram_nominal_scale_up.Sumw2()
histogram_nominal_scale_down=ROOT.TH1F("histo_nominal_ScaleDown","histo_nominal_ScaleDown",options.binsx,options.minx,options.maxx)
histogram_nominal_scale_down.Sumw2()

mjet_altshapeUp=ROOT.TH1F("mjet_altshapeUp","mjet_altshapeUp",options.binsx,options.minx,options.maxx)
mjet_altshapeUp.Sumw2()
histogram_altshapeUp=ROOT.TH1F("histo_altshapeUp","histo_altshapeUp",options.binsx,options.minx,options.maxx)
histogram_altshapeUp.Sumw2()
histogram_altshape_scale_up=ROOT.TH1F("histo_altshape_ScaleUp","histo_altshape_ScaleUp",options.binsx,options.minx,options.maxx)
histogram_altshape_scale_up.Sumw2()
histogram_altshape_scale_down=ROOT.TH1F("histo_altshape_ScaleDown","histo_altshape_ScaleDown",options.binsx,options.minx,options.maxx)
histogram_altshape_scale_down.Sumw2()

mjet_altshape2=ROOT.TH1F("mjet_altshape2","mjet_altshape2",options.binsx,options.minx,options.maxx)
mjet_altshape2.Sumw2()
histogram_altshape2=ROOT.TH1F("histo_altshape2","histo_altshape2",options.binsx,options.minx,options.maxx)
histogram_altshape2.Sumw2()

histograms=[
    mjet_nominal,
    histogram_nominal,
    histogram_nominal_scale_up,
    histogram_nominal_scale_down,
    mjet_altshapeUp,
    histogram_altshapeUp,
    histogram_altshape_scale_up,
    histogram_altshape_scale_down,
    mjet_altshape2,
    histogram_altshape2
	]

leg = options.var.split('_')[1]

maxEvents = -1
#ok lets populate!
for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):

 #Nominal histogram Pythia8
 if plotter.filename.find(sampleTypes[0].replace('.root','')) != -1: 
   print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
   print "filename: ", plotter.filename, " preparing central values histo"
   
   #histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)   
   histI2=plotter.drawTH1('jj_%s_softDrop_mass'%leg,options.cut,"1",options.binsx,options.minx,options.maxx)

   print " - Creating dataset - "   
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_%s_gen_pt,%s'%(leg,options.var),options.cut,options.firstEv,options.lastEv)     

   print " - Creating 1D gaussian template - "   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)   
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scale,res,histTMP) 
   
   #if histTMP.Integral()>0:
   # histTMP.Scale(histI.Integral()/histTMP.Integral())
   # histogram_nominal.Add(histTMP)
   # mjet_nominal.Add(histI2)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mjet_nominal.Add(histI2)
    
   histTMP.Delete()

   print " - Creating 1D gaussian template scale up - "
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scaleUp,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scaleUp,res,histTMP) 
   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal_scale_up.Add(histTMP)

   histTMP.Delete()

   print " - Creating 1D gaussian template scale down - "   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scaleDown,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scaleDown,res,histTMP) 
   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal_scale_down.Add(histTMP)
   
   histTMP.Delete()
   histI2.Delete()
    	
 if len(sampleTypes)<2: continue
 elif plotter.filename.find(sampleTypes[1].replace('.root','')) != -1: #alternative shape Herwig
   print "Preparing alternative shapes for sampletype " ,sampleTypes[1]
   print "filename: ", plotter.filename, " preparing alternate shape histo"
   
   #histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
   histI2=plotter.drawTH1('jj_%s_softDrop_mass'%leg,options.cut,"1",options.binsx,options.minx,options.maxx)

   print " - Creating dataset - "
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_%s_gen_pt,%s'%(leg,options.var),options.cut,options.firstEv,options.lastEv)     

   print " - Creating 1D gaussian template - "   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)    
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scale,res,histTMP) 
   
   #if histTMP.Integral()>0:
   # histTMP.Scale(histI.Integral()/histTMP.Integral())
   # histogram_altshapeUp.Add(histTMP)
   # mjet_altshapeUp.Add(histI2)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshapeUp.Add(histTMP)
    mjet_altshapeUp.Add(histI2)
    
   histTMP.Delete()

   print " - Creating 1D gaussian template scale up - "
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scaleUp,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scaleUp,res,histTMP) 
   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshape_scale_up.Add(histTMP)

   histTMP.Delete()

   print " - Creating 1D gaussian template scale down - "   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scaleDown,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scaleDown,res,histTMP) 
   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshape_scale_down.Add(histTMP)
   
   histTMP.Delete()
   histI2.Delete()
   		          	      
 if len(sampleTypes)<3: continue
 elif plotter.filename.find(sampleTypes[2].replace('.root','')) != -1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)
   print "Preparing alternative shapes for sampletype " ,sampleTypes[2]
   print "filename: ", plotter.filename, " preparing alternate shape histo"
   
   #histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
   histI2=plotter.drawTH1('jj_%s_softDrop_mass'%leg,options.cut,"1",options.binsx,options.minx,options.maxx)
 
   print " - Creating dataset - "
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_%s_gen_pt,%s'%(leg,options.var),options.cut,options.firstEv,options.lastEv)     
   
   print " - Creating 1D gaussian template - "
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)    
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_pt'%leg,scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_%s_gen_softDrop_mass'%leg,scale,res,histTMP) 
   
   #if histTMP.Integral()>0:
   # histTMP.Scale(histI.Integral()/histTMP.Integral())
   # histogram_altshape2.Add(histTMP)
   # mjet_altshape2.Add(histI2)

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshape2.Add(histTMP)
    mjet_altshape2.Add(histI2)
    
   histTMP.Delete()


print " ********** ALL DONE, now save in output file ", options.output
f=ROOT.TFile(options.output,"RECREATE")
f.cd()
finalHistograms={}
for hist in histograms:
 # hist.Write(hist.GetName()+"_raw")
 # smoothTail(hist)
 if (options.output).find("VJets")!=-1:
     print "smooth tails of 1D histogram for vjets background"
     smoothTail1D(histo)
     histo.Scale(1/histo.Integral())
 hist.Write(hist.GetName())
 finalHistograms[hist.GetName()]=hist

#histogram_altshapeDown=mirror(finalHistograms['histo_altshapeUp'],finalHistograms['histo_nominal'],"histo_altshapeDown")
#histogram_altshapeDown.Write()

f.Close()
print "***********DONE***********************"

'''
histograms.append(histogram_altshapeDown)
print "Drawing debugging plot ", "debug_"+options.output.replace(".root",".png") 
canv = ROOT.TCanvas("c1","c1",800,600)
leg = ROOT.TLegend(0.55010112,0.7183362,0.70202143,0.919833)
canv.cd()
for i,hist in enumerate(histograms):
 hist.SetLineWidth(3)
 hist.Rebin(2)
 hist.GetXaxis().SetTitle("Mass (GeV)")
 hist.GetXaxis().SetNdivisions(9,1,0)
 hist.GetYaxis().SetNdivisions(9,1,0)
 hist.GetYaxis().SetTitle("A.U")
 hist.GetXaxis().SetRangeUser(options.minx,options.maxx)
 hist.SetLineColor((i+1)*2)
 hist.DrawNormalized("HISTsame")
 leg.AddEntry(hist,hist.GetName(),"L")
leg.Draw("same")
canv.SaveAs("debug_"+options.output.replace(".root",".png") )
'''



