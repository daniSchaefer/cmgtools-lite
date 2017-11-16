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
    binsx=[]
    for b in binsxStr:
        binsx.append(float(b))

    binsz=[]
    for b in range(0,51):
        binsz.append(0.7+0.7*b/50.0)

    print "make histos used for detector parametrisation"
    
    superHX=data.drawTH2Binned(variables[0]+'/'+genVariables[0]+':'+genVariables[2],options.cut,"1",binsx,binsz)
    superHY=data.drawTH2Binned(variables[1]+'/'+genVariables[1]+':'+genVariables[2],options.cut,"1",binsx,binsz)    
    print " X "+variables[0]+'/'+genVariables[0]+':'+genVariables[2]
    print " Y "+variables[1]+'/'+genVariables[1]+':'+genVariables[2]
    
    print "============================================================================="
    nameDetectoroutput = options.output+"_2DDetectorParam.root"
    print "making detector parametrisation. Output file is : "+nameDetectoroutput
    f=ROOT.TFile(nameDetectoroutput,"RECREATE")
    
    print "declare output histos "


    scalexHisto=ROOT.TH1F("scalexHisto","scaleHisto",len(binsx)-1,array('d',binsx))
    resxHisto=ROOT.TH1F("resxHisto","resHisto",len(binsx)-1,array('d',binsx))

    scaleyHisto=ROOT.TH1F("scaleyHisto","scaleHisto",len(binsx)-1,array('d',binsx))
    resyHisto=ROOT.TH1F("resyHisto","resHisto",len(binsx)-1,array('d',binsx))
    

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
    histogram1D = ROOT.TH1F("histo1D_nominal","histo1D_nominal",int(options.binsy),options.miny,options.maxy)
    
    for plotter,plotterNW in zip(dataPlotters,dataPlottersNW):
        #Nominal histogram Pythia8
        if plotter.filename.find(sampleTypes[0]) != -1: 
            print "Preparing nominal histogram for sampletype " ,sampleTypes[0]
            print "filename: ", plotter.filename, " preparing central values histo"
            histI2D=plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",options.cut,"1",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
            testhistI2=histI2D.ProjectionY("mjet_tmp")
            print options.cut
        
            histI2=plotter.drawTH1('jj_l1_softDrop_mass',options.cut+"*(jj_LV_mass>1000&&jj_LV_mass<7000)","1",options.binsy,options.miny,options.maxy)
            #c=ROOT.TCanvas("test","test",400,400)
            #histI2.Scale(1/histI2.Integral())
            #testhistI2.Scale(1/testhistI2.Integral())
            #histI2.Draw("Hist")
            #testhistI2.SetLineColor(ROOT.kBlue)
            #testhistI2.SetFillColor(0)
            #testhistI2.Draw("histsame")
            #c.SaveAs("test1DTemplatespeedup.pdf")
            
            mjet_mvv_nominal.Add(histI2D)
            
            print " - Creating dataset - "
            dataset=plotterNW.makeDataSet(varsDataSet,options.cut,maxEvents)
            print varsDataSet

            print " - Creating 2D gaussian template - "
            histTMP=ROOT.TH2F("histoTMP","histoTMP",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
            #histTMP = ROOT.TH2F("histo_nominal","histo_nominal",int(options.binsx),options.minx,options.maxx,options.binsy,options.miny,options.maxy)
            if not(options.usegenmass): 
                datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,"jj_gen_partialMass","jj_l1_gen_softDrop_mass",'jj_l1_gen_pt',scalexHisto,scaleyHisto,resxHisto,resyHisto,histTMP)
            else: datamaker=ROOT.cmg.GaussianSumTemplateMaker(dataset,"jj_gen_partialMass","jj_l1_gen_softDrop_mass",'jj_l1_gen_softDrop_mass',scalexHisto,scaleyHisto,resxHisto,resyHisto,histTMP)
            
            print histTMP
            print histTMP.Integral()
            if histTMP.Integral()>0:
                histTMP.Scale(histI2D.Integral()/histTMP.Integral())
                histogram.Add(histTMP)
                histTMP.Delete()
                print "add hist tmp"
                
                
            print " - Creating dataset 1D - "
            #the cuts of mVV > 1000 GeV are really important since they significally change the shape of the mjet distribution!
            dataset1D=plotterNW.makeDataSet(varsDataSet,options.cut+"*(jj_LV_mass>1000&&jj_LV_mass<7000)",maxEvents)
            print " - Creating 1D gaussian template - "   
            histTMP1D=ROOT.TH1F("histoTMP","histo",int(options.binsy),options.miny,options.maxy) 
            if not(options.usegenmass): 
                datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset1D,'jj_l1_gen_softDrop_mass','jj_l1_gen_pt',scaleyHisto,resyHisto,histTMP1D)
            else: datamaker=ROOT.cmg.GaussianSumTemplateMaker1D(dataset1D,'jj_l1_gen_softDrop_mass','jj_l1_gen_softDrop_mass',scaleyHisto,resyHisto,histTMP1D)     
            if histTMP1D.Integral()>0:
                histTMP1D.Scale(histI2.Integral()/histTMP1D.Integral())
                histogram1D.Add(histTMP1D)
                histTMP1D.Delete()
            histI2D.Delete()   
                
            
    conditional(histogram)
    expanded=expandHisto(histogram,options)
    conditional(expanded)
    mjet_nominal = mjet_mvv_nominal.ProjectionY("mjet_nominal")
    nameKernelFile=options.output+"_kernels.root"
    print "making kernels Output file : "+nameKernelFile
    fkernel = ROOT.TFile(nameKernelFile,"RECREATE")
    mjet_mvv_nominal.Write()
    mjet_nominal.Write()
    histogram.SetName("histo_nominal_test")
    histogram.Write()
    expanded.Write()
    #histogram1D.Scale(1/histogram1D.Integral())
    histogram1D.Write()
    
    
    print "===================================================================="
    nameOutputFile=options.output+"_final.root"
    print "make 2D PDF from convolution "+nameOutputFile
    output=ROOT.TFile(nameOutputFile,"RECREATE")
    
    #test=ROOT.TFile("JJ_nonRes_MJJ_HP.root")
    #testhist = test.Get("histo_nominal")
    makeHisto("histo_nominal",expanded,histogram1D,output)
    
    f.Close()
    fkernel.Close()
    output.Close()
