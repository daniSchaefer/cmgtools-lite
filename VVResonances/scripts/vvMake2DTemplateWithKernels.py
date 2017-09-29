#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-r","--res",dest="res",help="res",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for x",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("-u","--usegenmass",dest="usegenmass",action="store_true",help="use gen mass for det resolution",default=False)


def mirror(histo,histoNominal,name):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            up=histo.GetBinContent(i,j)/intUp
            nominal=histoNominal.GetBinContent(i,j)/intNominal
            newHisto.SetBinContent(i,j,histoNominal.GetBinContent(i,j)*nominal/up)
    return newHisto       
	
def expandHisto(histo,options):
    histogram=ROOT.TH2F(histo.GetName(),"histo",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram
        


def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)

def smoothTail(hist):
    hist.Scale(1.0/hist.Integral())
    expo=ROOT.TF1("expo","expo",1000,8000)
#    expo=ROOT.TF1("expo","[0]*(1-pow(x/13000.,[1]))/pow(x/13000.0,[2]+0.0*TMath::Log(x/13000.0))",1000,8000)
#    expo.SetParameters(1,-)
#    expo.SetParLimits(0,0,1)
#    expo.SetParLimits(1,0.1,100)
#    expo.SetParLimits(2,0.1,100)

    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
#        for j in range(1,proj.GetNbinsX()+1):
#            if proj.GetBinContent(j)/proj.Integral()<0.0005:
#                proj.SetBinError(j,1.8)
        proj.Fit(expo,"","",2000,8000)
        proj.Fit(expo,"","",2000,8000)
        for j in range(1,hist.GetNbinsX()+1):
            x=hist.GetXaxis().GetBinCenter(j)
            if x>2500:
                hist.SetBinContent(j,i,expo.Eval(x))



(options,args) = parser.parse_args()

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
scale_x=fcorr.Get("scalexHisto")
scale_y=fcorr.Get("scaleyHisto")
res_x=fcorr.Get("resxHisto")
res_y=fcorr.Get("resyHisto")

variables=options.vars.split(',')

binsx=[]
for i in range(0,options.binsx+1):
    binsx.append(options.minx+i*(options.maxx-options.minx)/options.binsx)

binsy=[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210., 240., 270., 300., 330., 360., 390., 410., 440., 470., 500., 530., 560., 590.,610.]    #28

mjet_mvv_nominal = ROOT.TH2F("mjet_mvv_nominal","mjet_mvv_nominal",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
mjet_mvv_altshapeUp = ROOT.TH2F("mjet_mvv_altshapeUp","mjet_mvv_altshapeUp",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
mjet_mvv_altshape2 = ROOT.TH2F("mjet_mvv_altshape2","mjet_mvv_altshape2",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
histogram = ROOT.TH2F("histo_nominal","histo_nominal",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshapeUp = ROOT.TH2F("histo_altshapeUp","histo_altshapeUp",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
histogram_altshape2 = ROOT.TH2F("histo_altshape2","histo_altshape2",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

#systematics
histograms=[
    histogram,
    histogram_altshapeUp,
    histogram_altshape2
]

# do if only nominal shapes should be calculated
if len(sampleTypes)<2:
    histograms=[histogram]
#ok lets populate!

maxEvents = -1
varsDataSet = 'jj_l1_gen_pt,'+variables[1]+','+variables[0]


for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):

 #if plotter.filename != 'QCD_Pt-15to7000': continue
 
 #Nominal histogram Pythia8
 if plotter.filename.find(sampleTypes[0]) != -1:
  print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
  print "filename: ", plotter.filename, " preparing central values histo"
 
  histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  norm=histI.Integral()
  #y:x
  histI2D=plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

  print " - Creating dataset - "
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)

  print " - Creating gaussian template - "
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_pt',scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_softDrop_mass',scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  # histTMP.Scale(histI.Integral()/histTMP.Integral())
  # histogram.Add(histTMP)
  #if histI2D.Integral()>0: 
  # histI2D.Scale(histI.Integral()/histI2D.Integral())
  # mjet_mvv_nominal.Add(histI2D)

  if histTMP.Integral()>0:
   histTMP.Scale(histI2D.Integral()/histTMP.Integral())
   histogram.Add(histTMP)
   #histI2D.Scale(histI.Integral()/histI2D.Integral())
   mjet_mvv_nominal.Add(histI2D)
   
  #histI.Delete()  
  histI2D.Delete()	  
  histTMP.Delete()

 if len(sampleTypes)<2: continue 
 elif plotter.filename.find(sampleTypes[1]) != -1: #alternative shape Herwig
  print "Preparing alternative shapes for sampletype " ,sampleTypes[1]
  print "filename: ", plotter.filename, " preparing alternate shape histo"

  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()

  histI2D=plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

  print " - Creating dataset - "
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)

  print " - Creating gaussian template - "
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_pt',scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_softDrop_mass',scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  #  histTMP.Scale(histI.Integral()/histTMP.Integral())
  #  histogram_altshapeUp.Add(histTMP)
  #if histI2D.Integral()>0: 
  #  histI2D.Scale(histI.Integral()/histI2D.Integral())
  #  mjet_mvv_altshapeUp.Add(histI2D)

  if histTMP.Integral()>0:
    histTMP.Scale(histI2D.Integral()/histTMP.Integral())
    histogram_altshapeUp.Add(histTMP)
    mjet_mvv_altshapeUp.Add(histI2D)
   
  #histI.Delete()  
  histI2D.Delete()
  histTMP.Delete()

 if len(sampleTypes)<3: continue 
 elif plotter.filename.find(sampleTypes[2]) != -1: #alternative shape Pythia8+Madgraph (not used for syst but only for cross checks)
  print "Preparing alternative shapes for sampletype " ,sampleTypes[2]
  print "filename: ", plotter.filename, " preparing alternate shape histo"

  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()

  histI2D=plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
  histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))

  print " - Creating dataset - "
  dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)

  print " - Creating gaussian template - "
  if not(options.usegenmass): 
   datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_pt',scale_x,scale_y,res_x,res_y,histTMP)
  else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_softDrop_mass',scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
  #  histTMP.Scale(histI.Integral()/histTMP.Integral())
  #  histogram_altshape2.Add(histTMP)
  #if histI2D.Integral()>0:  
  #  histI2D.Scale(histI.Integral()/histI2D.Integral())
  #  mjet_mvv_altshape2.Add(histI2D)

  if histTMP.Integral()>0:
    histTMP.Scale(histI.Integral()/histTMP.Integral())
    histogram_altshape2.Add(histTMP) 
    mjet_mvv_altshape2.Add(histI2D)

    
  #histI.Delete()  
  histI2D.Delete()
  histTMP.Delete()

f=ROOT.TFile(options.output,"RECREATE")
print "Finished producing histograms! Saving to" ,options.output
finalHistograms={}
f.cd()
for hist in histograms:
 print "Working on histogram " ,hist.GetName()
 hist.Write(hist.GetName()+"_coarse")
 #smooth
 #print "Smoothing tail for " ,hist.GetName()
 #smoothTail(hist)
 print "Creating conditional histogram for ",hist.GetName()
 conditional(hist)
 print "Expanding for " ,hist.GetName()
 expanded=expandHisto(hist,options)
 conditional(expanded)
 expanded.Write()
 finalHistograms[hist.GetName()]=expanded

mjet_mvv_nominal.Write()
mjet_mvv_altshapeUp.Write()
mjet_mvv_altshape2.Write()

# ##Mirror Herwig shape
if len(sampleTypes)>2:
    histogram_altshapeDown=mirror(finalHistograms['histo_altshapeUp'],finalHistograms['histo_nominal'],"histo_altshapeDown")
    conditional(histogram_altshapeDown)
    histogram_altshapeDown.Write()
        		
f.Close()




