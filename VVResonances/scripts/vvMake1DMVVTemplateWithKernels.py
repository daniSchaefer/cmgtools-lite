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
ROOT.gStyle.SetOptStat(0)

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
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")

(options,args) = parser.parse_args()


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
	
def smoothTail1D(proj):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral() 
    proj.Scale(1.0/scale)
    
    
    beginFitX = 1500
    expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000) 
    expo.SetParameters(0,16.,2.)
    expo.SetParLimits(2,1.,20.)
    proj.Fit(expo,"LLMR","",beginFitX,8000)
    beginsmooth = False
    print proj.GetNbinsX()+1
    for j in range(1,proj.GetNbinsX()+1):
        x=proj.GetXaxis().GetBinCenter(j)
        if x>beginFitX:
            if beginsmooth==False:
                if x<2100: 
                   if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00009:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                    print beginFitX
                    print "begin smoothing at " +str(x)
                    beginsmooth = True 
               #if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                   #print beginFitX
                   #print "begin smoothing at " +str(x)

                   #beginsmooth = True 
                else: beginsmooth = True
            if beginsmooth:
                proj.SetBinContent(j,expo.Eval(x))
    return 1

weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

sampleTypes=options.samples.split(',')

stack = ROOT.THStack("stack","")

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

binning = getBinning(options.binsMVV,options.minx,options.maxx,options.binsx)
print binning


#distribution of mjet from simulation --> use to validate kernel
mvv_nominal=ROOT.TH1F("mvv_nominal","mvv_nominal",options.binsx,array('f',binning))
mvv_nominal.Sumw2()

mvv_altshapeUp=ROOT.TH1F("mvv_altshapeUp","mvv_altshapeUp",options.binsx,array('f',binning))
mvv_altshapeUp.Sumw2()

mvv_altshape2=ROOT.TH1F("mvv_altshape2","mvv_altshape2",options.binsx,array('f',binning))
mvv_altshape2.Sumw2()

histogram_nominal=ROOT.TH1F("histo_nominal","histo_nominal",options.binsx,array('f',binning))
histogram_nominal.Sumw2()

histogram_altshapeUp=ROOT.TH1F("histo_altshapeUp","histo_altshapeUp",options.binsx,array('f',binning))
histogram_altshapeUp.Sumw2()

histogram_altshape2=ROOT.TH1F("histo_altshape2","histo_altshape2",options.binsx,array('f',binning))
histogram_altshape2.Sumw2()

histograms=[
    histogram_nominal,
    histogram_altshapeUp,
    histogram_altshape2,
    mvv_nominal,
    mvv_altshapeUp,
    mvv_altshape2
	]

maxEvents = -1
#ok lets populate!
for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):

 #Nominal histogram Pythia8
 c=0
 if plotter.filename.find(sampleTypes[0].replace('.root','')) != -1: 
   print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
   print "filename: ", plotter.filename, " preparing central values histo"
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
   
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)     
   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning)) 
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP) 

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_nominal.Add(histTMP)
    mvv_nominal.Add(histI2)
    histI2.SetFillColorAlpha(ROOT.kRed+c,0.6)
    if c==0: 
        histI2.SetFillColorAlpha(ROOT.kRed,0.6)
    if c==1:
        histI2.SetFillColorAlpha(ROOT.Green,0.6)
    if c ==2: 
        histI2.SetFillColorAlpha(ROOT.kBlue,0.6)
    
    print "add stack histo "
    stack.Add(histTMP)
   c+=1 
   histI2.Delete()
   histTMP.Delete()

 if len(sampleTypes)<2: continue
 elif plotter.filename.find(sampleTypes[1].replace('.root','')) != -1: #alternative shape Herwig
   print "Preparing alternative shapes for sampletype " ,sampleTypes[1]
   print "filename: ", plotter.filename, " preparing alternate shape histo"
   #histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))
 
   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)     
   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))  
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP) 

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshapeUp.Add(histTMP)
    mvv_altshapeUp.Add(histI2)
    
   histI2.Delete()
   histTMP.Delete()
		          	      
 if len(sampleTypes)<3: continue
 elif plotter.filename.find(sampleTypes[2].replace('.root','')) != -1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)
   print "Preparing alternative shapes for sampletype " ,sampleTypes[2]
   print "filename: ", plotter.filename, " preparing alternate shape histo"
   
   #histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
   histI2=plotter.drawTH1Binned('jj_LV_mass',options.cut,"1",array('f',binning))

   dataset=plotterNW.makeDataSet('jj_gen_partialMass,jj_l1_gen_pt,jj_l1_gen_softDrop_mass',options.cut,options.firstEv,options.lastEv)     
   
   histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,array('f',binning))
   if not(options.usegenmass): 
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_pt',scale,res,histTMP)
   else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'jj_l1_gen_softDrop_mass',scale,res,histTMP) 

   if histTMP.Integral()>0:
    histTMP.Scale(histI2.Integral()/histTMP.Integral())
    histogram_altshape2.Add(histTMP)
    mvv_altshape2.Add(histI2)
    
   histI2.Delete()
   histTMP.Delete()


print " ********** ALL DONE, now save in output file ", options.output
f=ROOT.TFile(options.output,"RECREATE")
f.cd()
finalHistograms={}
for hist in histograms:
 # hist.Write(hist.GetName()+"_raw")
 if (options.output).find("VJets")!=-1 and hist.GetName()!="mvv_nominal":
     print "smooth tails of 1D histogram for vjets background"
     if hist.Integral() > 0:
        smoothTail1D(hist)
 hist.Write(hist.GetName())
 finalHistograms[hist.GetName()]=hist

 #################################
c = ROOT.TCanvas("c","C",400,400)
finalHistograms["histo_nominal"].SetLineColor(ROOT.kBlue)
finalHistograms["histo_nominal"].GetYaxis().SetTitle("arbitrary scale")
finalHistograms["histo_nominal"].GetXaxis().SetTitle("dijet mass")
finalHistograms["histo_nominal"].Draw("hist")
data = finalHistograms["mvv_nominal"]
data.Scale(1./data.Integral())
data.SetMarkerColor(ROOT.kBlack)
data.Draw("same")
stack.Draw("same")
c.SetLogy()
c.SaveAs("debug_Vjets_mVV_kernels.pdf")
print "for debugging save   debug_Vjets_mVV_kernels.png "
########################################################

#histogram_altshapeDown=mirror(finalHistograms['histo_altshapeUp'],finalHistograms['histo_nominal'],"histo_altshapeDown")
#histogram_altshapeDown.Write()

alpha=1.5/5000
histogram_pt_down,histogram_pt_up=unequalScale(finalHistograms["histo_nominal"],"histo_nominal_PT",alpha)
if (options.output).find("VJets")!=-1:
     print "smooth tails of 1D histogram for vjets background"
     smoothTail1D(histogram_pt_down)
     smoothTail1D(histogram_pt_up)
histogram_pt_down.Write()
histogram_pt_up.Write()

alpha=1.5*1000
histogram_opt_down,histogram_opt_up=unequalScale(finalHistograms["histo_nominal"],"histo_nominal_OPT",alpha,-1)
if (options.output).find("VJets")!=-1:
     print "smooth tails of 1D histogram for vjets background"
     smoothTail1D(histogram_opt_down)
     smoothTail1D(histogram_opt_up)
histogram_opt_down.Write()
histogram_opt_up.Write()

alpha=5000.*5000.
histogram_pt2_down,histogram_pt2_up=unequalScale(finalHistograms["histo_nominal"],"histo_nominal_PT2",alpha,2)
if (options.output).find("VJets")!=-1:
     print "smooth tails of 1D histogram for vjets background"
     smoothTail1D(histogram_pt2_down)
     smoothTail1D(histogram_pt2_up)
histogram_pt2_down.Write()
histogram_pt2_up.Write()

alpha=1000.*1000.
histogram_opt2_down,histogram_opt2_up=unequalScale(finalHistograms["histo_nominal"],"histo_nominal_OPT2",alpha,-2)
if (options.output).find("VJets")!=-1:
     print "smooth tails of 1D histogram for vjets background"
     smoothTail1D(histogram_opt2_down)
     smoothTail1D(histogram_opt2_up)
histogram_opt2_down.Write()
histogram_opt2_up.Write() 

f.Close()

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

