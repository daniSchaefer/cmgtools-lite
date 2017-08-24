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


def smoothTailOLD(hist):
    #smart smoother ! Find the last hit with data.
    #fIT BEFORE THAT
    #eXTRAPOLATE AFTER THAT

    bin_1200=hist.GetXaxis().FindBin(1200)
    if bin_1200>=hist.GetNbinsX()+1:
        return

    if hist.Integral()==0:
        print "Well we have  0 integrl for the hist ",hist.GetName()
        return
    expo=ROOT.TF1("expo","[0]*((1-x/13000.0)^[1])/(x/13000.0)^[2]",1000,8000)
    expo.SetParameters(1,1,1)
    expo.SetParLimits(0,0,1)
    expo.SetParLimits(1,0.1,100)
    expo.SetParLimits(2,0.1,100)

#    expo=ROOT.TF1("func","expo",0,5000)
    for j in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(j)/hist.Integral()<0.0005:
            hist.SetBinError(j,1.8)

    hist.Fit(expo,"","",1000,8000)
    hist.Fit(expo,"","",1000,8000)
    for j in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(j)
        if x>1000:
            hist.SetBinContent(j,expo.Eval(x))

def smoothTail(hist):

    bin_1200=hist.GetXaxis().FindBin(1200)
    if bin_1200>=hist.GetNbinsX()+1:
        return

    if hist.Integral()==0:
        print "Well we have  0 integrl for the hist ",hist.GetName()
        return
    expo=ROOT.TF1("func","expo",0,5000)
#    expo=ROOT.TF1("expo","[0]*((1-x/13000.0)^[1])/(x/13000.0)^([2]+[3]*log(x))",1000,8000)
#    expo.SetParameters(1,1,1,0)
#    expo.SetParLimits(0,0,1)
#    expo.SetParLimits(1,0.1,100)
#    expo.SetParLimits(2,0.1,100)
#    expo.SetParLimits(3,0.0,20)


    for j in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(j)/hist.Integral()<0.0005:
            hist.SetBinError(j,1.8)

    hist.Fit(expo,"","",2000,8000)
    hist.Fit(expo,"","",2000,8000)
    for j in range(1,hist.GetNbinsX()+1):
        x=hist.GetXaxis().GetBinCenter(j)
        if x>2000:
            hist.SetBinContent(j,expo.Eval(x))



weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)


sampleTypes=options.samples.split(',')
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

scale=fcorr.Get("scale"+options.resHisto+"Histo")
res=fcorr.Get("res"+options.resHisto+"Histo")

ptBins=[0,150,200,250,300,350,400,450,500,550,600,700,800,900,1000,1500,2000,5000]

###Make res up and down
resUp = ROOT.TH1F(res)
resUp.SetName("resUp")
for i in range(1,res.GetNbinsX()+1):
    resUp.SetBinContent(i,res.GetBinContent(i)+0.3)



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





#ptUp = ROOT.TH1F("ptUp","pt",int(5*options.binsx),options.minx*0.7,options.maxx*1.5)
#ptUp.SetName("ptUp")
#ptDown = ROOT.TH1F(ptUp)
#ptDown.SetName("ptDown")

#for i in range(1,ptUp.GetNbinsX()+1):
#    x=ptUp.GetXaxis().GetBinCenter(i)
#    if options.resHisto=='x':
#        ptUp.SetBinContent(i,1+800./x)
#        ptDown.SetBinContent(i,1-400./x)
#    else:
#        ptUp.SetBinContent(i,1+30./x)
#        ptDown.SetBinContent(i,1-20./x)



#distribution of mjet from simulation --> use to validate kernel
mjet=ROOT.TH1F("mjet","mjet",options.binsx,options.minx,options.maxx)
mjet.Sumw2()

histogram=ROOT.TH1F("histo","histo",options.binsx,options.minx,options.maxx)
histogram.Sumw2()

histogram_res_up=ROOT.TH1F("histo_ResUp","histo",options.binsx,options.minx,options.maxx)
histogram_res_up.Sumw2()

histogram_scale_up=ROOT.TH1F("histo_ScaleUp","histo",options.binsx,options.minx,options.maxx)
histogram_scale_up.Sumw2()
histogram_scale_down=ROOT.TH1F("histo_ScaleDown","histo",options.binsx,options.minx,options.maxx)
histogram_scale_down.Sumw2()



histogram_top_up=ROOT.TH1F("histo_TOPUp","histo",options.binsx,options.minx,options.maxx)
histogram_top_up.Sumw2()
histogram_top_down=ROOT.TH1F("histo_TOPDown","histo",options.binsx,options.minx,options.maxx)
histogram_top_down.Sumw2()


#histogram_pt_up=ROOT.TH1F("histo_PTUp","histo",options.binsx,options.minx,options.maxx)
#histogram_pt_up.Sumw2()
#histogram_pt_down=ROOT.TH1F("histo_PTDown","histo",options.binsx,options.minx,options.maxx)
#histogram_pt_down.Sumw2()

histograms=[
    histogram,
    histogram_res_up,
    histogram_scale_up,
    histogram_scale_down,
    histogram_top_up,
    histogram_top_down,
    mjet,
#    histogram_pt_up,
#    histogram_pt_down,
]

#NB: l1 is the highest mass jet for JJ, while it is the lepton for LNUJJ
channel = options.var.split('_')[0] 
l1 = ''
l2 = ''
if channel == 'lnujj':
 l1 = channel+'_l1'
 l2 = channel+'_l2'
elif channel == 'jj':
 l1 = channel+'_l2'
 l2 = channel+'_l1'

#ok lets populate!
for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):

    print "filename: ", plotter.filename, " preparing central values histo"
    
    histI=plotter.drawTH1(options.var,options.cut,"1",1,0,1000000000)
    histI2=plotter.drawTH1(options.var,options.cut,"1",options.binsx,options.minx,options.maxx)

    norm=histI.Integral()
    
    #nominal
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    
    if options.var.find('gen_partialMass') == -1: dataset=plotterNW.makeDataSet('%s_pt,%s_gen_partialMass,%s_partonFlavour,%s_gen_pt,'%(l1,channel,l2,l2)+options.var,options.cut,-1)     
    else: dataset=plotterNW.makeDataSet('%s_pt,%s_partonFlavour,%s_gen_pt,'%(l1,l2,l2)+options.var,options.cut,-1)
        
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'%s_gen_pt'%(l2),scale,res,histTMP);
    
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram.Add(histTMP)
	mjet.Add(histI2)
        if "TT" in plotterNW.filename:
            histogram_top_up.Add(histTMP,2.0)
            histogram_top_down.Add(histTMP,0.5)
        else:
            histogram_top_up.Add(histTMP,1.0)
            histogram_top_down.Add(histTMP,1.0)

    histTMP.Delete()

    print "filename: ", plotter.filename, " preparing res up histo"

    #res Up
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'%s_gen_pt'%(l2),scale,resUp,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_res_up.Add(histTMP)
    histTMP.Delete()


    print "filename: ", plotter.filename, " preparing scale up histo"

    #scale Up
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'%s_gen_pt'%(l2),scaleUp,res,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_up.Add(histTMP)
    histTMP.Delete()

    print "filename: ", plotter.filename, " preparing scale down histo"

    #scale Down
    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'%s_gen_pt'%(l2),scaleDown,res,histTMP);
    if histTMP.Integral()>0:
        histTMP.Scale(histI.Integral()/histTMP.Integral())
        histogram_scale_down.Add(histTMP)
    histTMP.Delete()

    #pt Up
#    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,options.var,ptUp);
#    if histTMP.Integral()>0:
#        histTMP.Scale(histI.Integral()/histTMP.Integral())
#        histogram_pt_up.Add(histTMP)
#    histTMP.Delete()

    #pt Down
#    histTMP=ROOT.TH1F("histoTMP","histo",options.binsx,options.minx,options.maxx)
#    datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset,options.var,'lnujj_l2_gen_pt',scale,res,histTMP,options.var,ptDown);
#    if histTMP.Integral()>0:
#        histTMP.Scale(histI.Integral()/histTMP.Integral())
#        histogram_pt_down.Add(histTMP)
#    histTMP.Delete()

print " ********** ALL DONE, now save in output file ", options.output

f=ROOT.TFile(options.output,"RECREATE")
f.cd()

finalHistograms={}
for hist in histograms:
    hist.Write(hist.GetName()+"_raw")
    smoothTail(hist)
    hist.Write(hist.GetName())
    finalHistograms[hist.GetName()]=hist


if options.resHisto=='x':
    alpha=2.0/5000.
else:
    alpha=2.0/150
histogram_pt_down,histogram_pt_up=unequalScale(finalHistograms['histo'],"histo_PT",alpha)
histogram_pt_down.Write()
histogram_pt_up.Write()

if options.resHisto=='x':
    alpha=1.5*600
else:
    alpha=1.5*20
histogram_opt_down,histogram_opt_up=unequalScale(finalHistograms['histo'],"histo_OPT",alpha,-1)
histogram_opt_down.Write()
histogram_opt_up.Write()



histogram_res_down=mirror(finalHistograms['histo_ResUp'],finalHistograms['histo'],"histo_ResDown")
histogram_res_down.Write()


#scaleUp.Write("scaleUp")
#scaleDown.Write("scaleDown")
#ptUp.Write("weightPTUp")
#ptDown.Write("weightPTDown")
#resUp.Write("resUp")
#resDown.Write("resDown")
#ptUp.Write("ptUp")
#ptDown.Write("ptDown")
#wptUp.Write("wptUp")
#wptDown.Write("wptDown")

#quarkGluonUp.Write("qgUp")
#quarkGluonDown.Write("qgDwn")

f.Close()




