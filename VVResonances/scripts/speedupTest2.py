#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
ROOT.gSystem.Load("libCMGToolsVVResonances")


parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield in gen sample",default='')
parser.add_option("-v","--vars",dest="vars",help="variable for reco",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("--binarray",dest="binarray",help="binarray",default='')
parser.add_option("-g","--genVars",dest="genVars",help="variable for gen",default='')
parser.add_option("-w","--weights",dest="weights",help="additional weights",default='')
parser.add_option("-u","--usegenmass",dest="usegenmass",action="store_true",help="use gen mass for det resolution",default=False)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)


(options,args) = parser.parse_args()


def makeHisto(name,histox,histoy,fout):
    h=ROOT.TH2F(name,name,histox.GetNbinsX(),histox.GetXaxis().GetXmin(),histox.GetXaxis().GetXmax(),histox.GetNbinsY(),histox.GetYaxis().GetXmin(),histox.GetYaxis().GetXmax())
    print "make histo with " +str(histox.GetNbinsX())+"   "+str(histox.GetXaxis().GetXmin())+" "+str(histox.GetXaxis().GetXmax())
    print "make histo with " +str(histox.GetNbinsY())+"   "+str(histox.GetYaxis().GetXmin())+" "+str(histox.GetYaxis().GetXmax())
    for i in range(1,histoy.GetNbinsX()+1):
        for j in range(1,histox.GetNbinsX()+1):
            h.SetBinContent(j,i,histoy.GetBinContent(i)*histox.GetBinContent(j,i))
    fout.cd()
    h.Write()

def expandHisto(histo,options):
    #histogram=ROOT.TH2F(histo.GetName(),"histo",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    histogram = ROOT.TH2F(histo.GetName(),"histo",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy)
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

def Gaussian2D(varx, vary,var,hscalex,hscaley,hresx, hresy):
    genw=1
    binw=1
    reweight=1
    minX=1000
    maxX=6000
    minY=30
    maxY=600
      
    scalex=hscalex.Interpolate(var)*varx;
    scaley=hscaley.Interpolate(var)*vary;
    resx=hresx.Interpolate(var)*varx;
    resy=hresy.Interpolate(var)*vary;
    
    Ngaussian = ROOT.TF2("gauss2Dnormalized","exp(-0.5*(x-[0])*(x-[0])/([1]*[1])-0.5*(y-[2])*(y-[2])/([3]*[3])/(2.5066*[1]*[3]))",minX,maxX,minY,maxY)
    Ngaussian.SetParameter(0,scalex)
    Ngaussian.SetParameter(1,resx)
    Ngaussian.SetParameter(2,scaley)
    Ngaussian.SetParameter(3,resy)
    
    return Ngaussian



def getXBin(hist, x):
    #print hist.GetNbinsX()
    #print x
    maxB = hist.GetNbinsX()
    for i in range(1,maxB+1):
        xBin = i
        bc = hist.GetXaxis().GetBinCenter(i)
        bw = hist.GetXaxis().GetBinWidth(i)
        xup = bc + bw/2.
        xdown = bc - bw/2.
        if x < xdown:
            continue
        if x < xup:
            #print "return "+str(xBin)
            return xBin
    if x > hist.GetXaxis().GetBinCenter(maxB):
        return maxB+1
    return 0


def getXYBin(hist, histaxis, x):
    maxB = hist.GetNbinsX()
    for i in range(1,maxB+1):
        xBin = i
        bc = histaxis.GetBinCenter(i)
        bw = histaxis.GetBinWidth(i)
        xup = bc + bw/2.
        xdown = bc - bw/2.
        if x < xdown:
            continue
        if x < xup:
            #print "return "+str(xBin)
            return xBin
    if x > histaxis.GetBinCenter(maxB):
        return maxB+1
    return 0


if __name__=="__main__":
    print options.binsy
    maxEvents = -1
    weights_ = options.weights.split(',')
    variables=options.vars.split(',')
    genVariables=options.genVars.split(',')
    print "using variables "
    print variables
    print "using generated variables "
    print genVariables
    varsDataSet = 'jj_l1_gen_pt,'+variables[1]+','+variables[0]+",jj_l1_gen_softDrop_mass,jj_gen_partialMass"
    print "making datasets from samples"
    sampleTypes=options.samples.split(',')
    dataPlotters=[]
    dataPlottersNW=[]

    for filename in os.listdir(args[0]):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                print fname
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

    binsxStr=options.binarray.split(',')
    binsk=[]
    for b in binsxStr:
        binsk.append(float(b))

    binsz=[]
    for b in range(0,51):
        binsz.append(0.7+0.7*b/50.0)

    print "make histos used for detector parametrisation"
    
    superHX=data.drawTH2Binned(variables[0]+'/'+genVariables[0]+':'+genVariables[2],options.cut,"1",binsk,binsz)
    superHY=data.drawTH2Binned(variables[1]+'/'+genVariables[1]+':'+genVariables[2],options.cut,"1",binsk,binsz)    
    print " X "+variables[0]+'/'+genVariables[0]+':'+genVariables[2]
    print " Y "+variables[1]+'/'+genVariables[1]+':'+genVariables[2]
    
    print "============================================================================="
    nameDetectoroutput = options.output+"_2DDetectorParam.root"
    print "making detector parametrisation. Output file is : "+nameDetectoroutput
    f=ROOT.TFile(nameDetectoroutput,"RECREATE")
    
    print "declare output histos "


    scalexHisto=ROOT.TH1F("scalexHisto","scaleHisto",len(binsk)-1,array('d',binsk))
    resxHisto=ROOT.TH1F("resxHisto","resHisto",len(binsk)-1,array('d',binsk))

    scaleyHisto=ROOT.TH1F("scaleyHisto","scaleHisto",len(binsk)-1,array('d',binsk))
    resyHisto=ROOT.TH1F("resyHisto","resHisto",len(binsk)-1,array('d',binsk))
    

    print "fill histos for detector parametrisation"
    for bin in range(1,superHX.GetNbinsX()+1):

        tmp=superHX.ProjectionY("q",bin,bin)
        scalexHisto.SetBinContent(bin,tmp.GetMean())
        scalexHisto.SetBinError(bin,tmp.GetMeanError())
        resxHisto.SetBinContent(bin,tmp.GetRMS())
        resxHisto.SetBinError(bin,tmp.GetRMSError())

        tmp=superHY.ProjectionY("q",bin,bin)
        scaleyHisto.SetBinContent(bin,tmp.GetMean())
        scaleyHisto.SetBinError(bin,tmp.GetMeanError())
        resyHisto.SetBinContent(bin,tmp.GetRMS())
        resyHisto.SetBinError(bin,tmp.GetRMSError())
    
    scalexHisto.Write()
    scaleyHisto.Write()
    resxHisto.Write()
    resyHisto.Write()
    superHX.Write("dataX")
    superHY.Write("dataY")
    #f.Close()
    print "============================================================================="
     
    
    
    
    
    print "make histos used for Kernels"
    binsx=[]
    for i in range(0,int(options.binsx)+1):
        binsx.append(options.minx+i*(options.maxx-options.minx)/int(options.binsx))

    binsy=[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,140.,150.,160.,180.,210., 240., 270., 300., 330., 360., 390., 410., 440., 470., 500., 530., 560., 590.,610.] 
        
    mjet_mvv_nominal = ROOT.TH2F("mjet_mvv_nominal","mjet_mvv_nominal",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    #histogram = ROOT.TH2F("histo_nominal","histo_nominal",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    histogram = ROOT.TH2F("histo_nominal","histo_nominal",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    print "histogram" 
    print "x : "+str(histogram.GetNbinsX())+ " "
    print binsx
    print options.minx
    options.maxx
    print "y : "+str(histogram.GetNbinsY())
    print binsy
    print options.miny
    print options.maxy
    print "_______________________________"
    
    histogram1D = ROOT.TH1F("histo1D_nominal","histo1D_nominal",int(options.binsy),options.miny,options.maxy)
    
    
    testbinsx=[]
    testbinsxmax=300.
    for t in range(0,int(testbinsxmax)):
        testbinsx.append(900+t*5200/testbinsxmax)
    #print testbinsx
    testbinsy=[]
    #testbinsymax=610.
    #for t in range(0,int(testbinsymax)):
    #    testbinsy.append(30+t*580/testbinsymax)
    #print testbinsy
    testbinsy = binsy
    
    hist = ROOT.TH3D("h3D","h3D",len(testbinsx)-1,array('f',testbinsx),len(testbinsy)-1,array('f',testbinsy),len(binsk)-1,array('f',binsk))
    for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
        #Nominal histogram Pythia8
        if plotter.filename.find(sampleTypes[0]) != -1: 
            print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
            print "filename: ", plotter.filename, " preparing central values histo"
            histI2D=plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
            TMPhist=plotter.drawTH3Binned("jj_l1_gen_pt:jj_l1_gen_softDrop_mass:jj_gen_partialMass",options.cut,"1",array('f',testbinsx),array('f',testbinsy),array('f',binsk),"M_{qV} mass","GeV","Softdrop mass","GeV","pt","GeV","COLZ" )
            
            
            hist.Add(TMPhist)
        
            histI2=plotter.drawTH1('jj_l1_softDrop_mass',options.cut+"*(jj_LV_mass>1000&&jj_LV_mass<7000)","1",options.binsy,options.miny,options.maxy)            
            mjet_mvv_nominal.Add(histI2D)
                      
            
    #conditional(histogram)
    #expanded=expandHisto(histogram,options)
    #conditional(expanded)
    mjet_nominal = mjet_mvv_nominal.ProjectionY("mjet_nominal")
    nameKernelFile=options.output+"_kernels.root"
    print "making kernels Output file : "+nameKernelFile
    fkernel = ROOT.TFile(nameKernelFile,"RECREATE")
    mjet_mvv_nominal.Write()
    mjet_nominal.Write()
    #histogram.SetName("histo_nominal_test")
    #histogram.Write()
    expanded.Write()
    histogram1D.Write()
    
    
    #print "===================================================================="
    nameOutputFile=options.output+"_final.root"
    print "make 2D PDF from convolution "+nameOutputFile
    output=ROOT.TFile(nameOutputFile,"RECREATE")
    
    #test=ROOT.TFile("JJ_nonRes_MJJ_HP.root")
    #testhist = test.Get("histo_nominal")
    makeHisto("histo_nominal",expanded,histogram1D,output)
    TMP = ROOT.TH2("tmp","tmp",len(testbinsx)-1,array('f',testbinsx),len(testbinsy)-1,array('f',testbinsy))

    f.Close()
    fkernel.Close()
    output.Close()

