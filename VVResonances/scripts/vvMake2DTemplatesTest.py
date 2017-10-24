#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
import thread
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

(options,args) = parser.parse_args()
########################### speed up ##################################################
weights_ = options.weights.split(',')

random=ROOT.TRandom3(101082)

def Gaussian2D(varx, vary,var,hscalex,hscaley,hresx, hresy, varw, minX,maxX,minY,maxY):
    genw=1
    binw=1
    reweight=1
    #if (weightH!=0):
      #genw=varw
      #binw=weightH.GetXaxis().FindBin(genw);
      #reweight=weightH.GetBinContent(binw);
    
      
    scalex=hscalex.Interpolate(var)*varx;
    scaley=hscaley.Interpolate(var)*vary;
    resx=hresx.Interpolate(var)*varx;
    resy=hresy.Interpolate(var)*vary;
    
    #
    #print str(resx)+'   '+str(resy)
    
    
    gaussian = ROOT.TF2("gauss2D","exp(-0.5*(x-[0])*(x-[0])/([1]*[1])-0.5*(y-[2])*(y-[2])/([3]*[3]))",minX,maxX,minY,maxY)
    gaussian.SetParameter(0,scalex)
    gaussian.SetParameter(1,resx)
    gaussian.SetParameter(2,scaley)
    gaussian.SetParameter(3,resy)
    
    if resx < 1e-6 or resy <1e-6:
        print 'attention for some reason resolution becomes very small!'
        print str(scalex)+'   '+str(scaley)
        print str(resx)+'   '+str(resy)
        
        
    #print 'scale '+str(scalex)+'   '+str(scaley)
    #print 'resolution '+str(resx)+'   '+str(resy)
    #print gaussian.Eval(varx,vary)
    
    #c= ROOT.TCanvas('test','test',400,400)
    #gaussian.Draw()
    #c.SaveAs('test.pdf')
    norm = gaussian.Integral(minX,maxX,minY,maxY)
    mVV=varx
    mjet=vary
    mVVmin= mVV*0.8
    mVVmax= mVV*1.2
    if options.minx < mVVmin:
      mVVmin= options.minx
    if options.maxx > mVVmax:
      mVVmax= options.maxx
      
    mjetmin= mjet*0.8
    mjetmax= mjet*1.2
    if options.miny < mjetmin:
        mjetmin= options.miny
    if options.maxy > mjetmax:
        mjetmax= options.maxy
    norm = gaussian.Integral(mVVmin,mVVmax,mjetmin,mjetmax)
    
    #print 'unnormalised gaussian '+str(norm)
    #print norm
    #print varw
    #print varw/norm
    
    Ngaussian = ROOT.TF2("gauss2Dnormalized","exp(-0.5*(x-[0])*(x-[0])/([1]*[1])-0.5*(y-[2])*(y-[2])/([3]*[3])/(2.5066*[1]*[3]))",minX,maxX,minY,maxY)
    Ngaussian.SetParameter(0,scalex)
    Ngaussian.SetParameter(1,resx)
    Ngaussian.SetParameter(2,scaley)
    Ngaussian.SetParameter(3,resy)
    #Ngaussian.SetParameter(4,1./float(norm))
    #print 'normalised gaussian '+str(Ngaussian.Integral(minX,maxX,minY,maxY))
    #print 'result normalised '+str(Ngaussian.Eval(varx,vary))
    #print 'result unnormalised '+str(gaussian.Eval(varx,vary))
    
    return Ngaussian

def FillSmoothed(hist,gauss,w,mVV,mjet):
  Nx = hist.GetNbinsX()
  Ny = hist.GetNbinsY()
  mVVmin= mVV*0.7
  mVVmax= mVV*1.4
  if options.minx > mVVmin:
      mVVmin= options.minx
  if options.maxx < mVVmax:
      mVVmax= options.maxx
      
  mjetmin= mjet*0.6
  mjetmax= mjet*1.5
  if options.miny > mjetmin:
      mjetmin= options.miny
  if options.maxy < mjetmax:
      mjetmax= options.maxy
  norm = 1 #gauss.Integral(mVVmin,mVVmax,mjetmin,mjetmax)

  for i in range(1,Ny+1):
      for j in range(1,Nx+1):
          varx   = hist.GetXaxis().GetBinCenter(j)
          vary   = hist.GetYaxis().GetBinCenter(i)
          #print 'bin '+str(varx)+' '+str(vary)
          if varx < mVVmin:
              continue
          if vary < mjetmin:
              continue
          if varx> mVVmax:
              continue
          if vary> mjetmax:
              continue
          #print gauss.Eval(varx,vary)
          v = gauss.Eval(varx,vary)/norm
          v=v*w
          if v <= 1e-30:
              continue
          #print 'gauss '+str(v)
          #print v*w
          #print 'number events in bin '+str(w)
          #print 'norm '+str(norm)
          #print 'fill bin '+str(varx)+' '+str(vary)+' with ' +str(v)
          old = hist.GetBinContent(j,i)
          hist.SetBinContent(j,i,v+old)
  return hist

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

#binsy=[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210., 240., 270., 300., 330., 360., 390., 410., 440., 470., 500., 530., 560., 590.,610.]    #28

#scaleUp = ROOT.TH1F(scale_x)
#scaleUp.SetName("scaleUp")
#scaleDown = ROOT.TH1F(scale_x)
#scaleDown.SetName("scaleDown")
#for i in range(1,scale_x.GetNbinsX()+1):
    #scaleUp.SetBinContent(i,scale_x.GetBinContent(i)+0.09)
    #scaleDown.SetBinContent(i,scale_x.GetBinContent(i)-0.09)
    
#mjet_mvv_nominal = ROOT.TH2F("mjet_mvv_nominal","mjet_mvv_nominal",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
histogram = ROOT.TH2F("histo_nominal","histo_nominal",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)

#systematics
histograms=[
    histogram
]
histI2D =dataPlotters[0].drawTH2("jj_l1_gen_softDrop_mass:jj_gen_partialMass",options.cut,"1",options.binsx+2,options.minx-100,options.maxx+100,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):

 #if plotter.filename != 'QCD_Pt-15to7000': continue
 
 #Nominal histogram Pythia8
 if plotter.filename.find(sampleTypes[0]) != -1:
  print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
  print "filename: ", plotter.filename, " preparing central values histo"
 
  #histI=plotter.drawTH1(variables[0],options.cut,"1",1,0,1000000000)
  #norm=histI.Integral()
  #y:x
  histI2D.Add(plotter.drawTH2("jj_l1_gen_softDrop_mass:jj_gen_partialMass",options.cut,"1",options.binsx+2,options.minx-100,options.maxx+100,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" ))

  #print " - Creating dataset - "
  #dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)

print " - Creating 2D gaussian template - "
Nx = histI2D.GetNbinsX()
Ny = histI2D.GetNbinsY()

#Nx=1
#Ny=20
print " minVV "+str(options.minx)+" max MVV "+str(options.maxx)
print " min mjet "+str(options.miny) + " Max mjet "+str(options.maxy) 
for i in range(1,Ny+1):
      for j in range(1,Nx+1):
          w = histI2D.GetBinContent(j,i)
          if w==0:
              continue
          varx   = histI2D.GetXaxis().GetBinCenter(j)
          vary   = histI2D.GetYaxis().GetBinCenter(i)
          gauss  = Gaussian2D(varx, vary,varx,scale_x,scale_y,res_x, res_y, w,options.minx,options.maxx,options.miny,options.maxy)
          #print 'doing bin '+str(varx)+' '+str(vary)
          FillSmoothed(histogram,gauss,w*1000000,varx,vary)
  #histTMP=ROOT.TH2F("histoTMP","histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
  #if not(options.usegenmass): 
   #datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_pt',scale_x,scale_y,res_x,res_y,histTMP)
  #else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,variables[0],variables[1],'jj_l1_gen_softDrop_mass',scale_x,scale_y,res_x,res_y,histTMP)

  #if histTMP.Integral()>0:
   #histTMP.Scale(histI2D.Integral()/histTMP.Integral())
   #histogram.Add(histTMP)
   #mjet_mvv_nominal.Add(histI2D)
   
  ##histI.Delete()  	  
  #histTMP.Delete()
  
f=ROOT.TFile(options.output,"RECREATE")
print "Finished producing histograms! Saving to" ,options.output
histI2D.SetName('genHisto')
histI2D.Write()
print histograms
for hist in histograms:
 print "Working on histogram " ,hist.GetName()
 hist.Write()
