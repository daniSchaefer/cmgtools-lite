import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import copy
sys.path.append("/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/")
from runFitPlots import getListOfBinsLowEdge, doZprojection, getListOfBins, getListOfBinsWidth,reduceBinsToRange, doXprojection,getListFromRange, doYprojection


ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
colors = [ROOT.kBlack,ROOT.kRed-2,ROOT.kRed+1,ROOT.kRed-1,ROOT.kRed+2,ROOT.kGreen-1,ROOT.kGreen-2,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kBlue]



def getNominalData(histo,nEvents_bkg,resbkg,resbkg_events,binsxy,binsz,args,category):
    histo.Scale(nEvents_bkg/histo.Integral())
    i=0
    for vjets in resbkg:
        print resbkg_events[i]
        vjets.Scale(resbkg_events[i]/vjets.Integral())
        histo.Add(vjets)
        i+=1
    arglist = ROOT.RooArgList(args)
 
    data = ROOT.RooDataHist("data","data",arglist,ROOT.RooFit.Index(category),ROOT.RooFit.Import(category.getLabel(),histo)) 
    return data    




if __name__=="__main__":
    Parser = optparse.OptionParser()
    Parser.add_option("-o","--output",dest="output",help="Output folder name",default='')
    Parser.add_option("-n","--name",dest="name",help="Input ROOT File name",default='/home/dschaefer/DiBoson3D/forBiasTests/workspace_wjets2.root')
    Parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
    Parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
    Parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
    Parser.add_option("-l","--label",dest="label",help="add extra label such as pythia or herwig",default="")
    Parser.add_option("-s","--signal",dest="signal",help="signal model in workspace",default="WprimeWZ")
    (options,args) = Parser.parse_args()
    sig = options.signal
    lumi = 35900.
    purity="HPHP"
    pdflist = "nonRes_PTZDown_JJ_"+sig+"_"+purity+"_13TeV,nonRes_OPTZUp_JJ_"+sig+"_"+purity+"_13TeV,nonRes_PTZUp_JJ_"+sig+"_"+purity+"_13TeV,nonRes_OPTZDown_JJ_"+sig+"_"+purity+"_13TeV,nonRes_PTXYUp_JJ_"+sig+"_"+purity+"_13TeV,nonRes_PTXYDown_JJ_"+sig+"_"+purity+"_13TeV,nonRes_OPTXYUp_JJ_"+sig+"_"+purity+"_13TeV,nonRes_OPTXYDown_JJ_"+sig+"_"+purity+"_13TeV"
    infiles = ["/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/JJ_WJets_resl1_HPHP.root","/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/JJ_ZJets_resl1_HPHP.root"]#,"/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/JJ_ttbar_HPHP.root"]
    infiles = ["/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/JJ_ZJets_resl1_HPHP.root"]
    
    # get "data" of Vjets events
    f =(ROOT.TFile(infiles[0],"READ"))
    V_jets_histo  =  f.Get("WJets")
    if V_jets_histo==None:
        V_jets_histo  =  f.Get("ZJets")
    if V_jets_histo==None:
        V_jets_histo  =  f.Get("ttbar")
    V_jets_histo.Scale(lumi)
    nEvents= V_jets_histo.Integral()
    for i in range(1,len(infiles)):
        print "open file "+infiles[i]
        tmp =(ROOT.TFile(infiles[i],"READ"))
        tmp_histo = tmp.Get("WJets")
        if tmp_histo==None:
            tmp_histo = tmp.Get("ZJets")
        if tmp_histo==None:
            tmp_histo = tmp.Get("ttbar")
        tmp_histo.Scale(lumi)
        nEvents += tmp_histo.Integral()
        V_jets_histo.Add(tmp_histo)
   
    # get binning (necessary to make plots)
    binsxy = getListOfBinsLowEdge(V_jets_histo,"x")
    binsz  = getListOfBinsLowEdge(V_jets_histo,"z")
    xBins  = getListOfBins(V_jets_histo,"x")
    zBins  = getListOfBins(V_jets_histo,"z")
    xBins_redux = reduceBinsToRange(xBins,getListFromRange(options.xrange))
    yBins_redux = reduceBinsToRange(xBins,getListFromRange(options.yrange))
    zBins_redux = reduceBinsToRange(zBins,getListFromRange(options.zrange))
    xBinsWidth   = getListOfBinsWidth(V_jets_histo,"x")
    zBinsWidth   = getListOfBinsWidth(V_jets_histo,"z")
     
    # get QCD background estimation from workspace 
     
    print "open file " +options.name
    fw = (ROOT.TFile(options.name,"READ"))
    workspace = fw.Get("w")
    ############################# extract TH3 histos to generate toys from #############
     
    forToys = ROOT.TFile("/home/dschaefer/DiBoson3D/finalKernels/JJ_HPHP.root","READ")
    bkg_histo = forToys.Get("nonRes")
    nEvents_qcd = bkg_histo.Integral()*lumi
    print nEvents_qcd
    
    model_b = workspace.pdf("model_b")
    components  = model_b.getComponents()
    pdf_sig = workspace.pdf("shapeSig_"+sig+"_JJ"+sig+"_HPHP_13TeV")
    pdf_shape  = components["shapeBkg_nonRes_JJ_"+sig+"_"+purity+"_13TeV"]
    pdf_shape.SetName("qcd_postfit")
    allpdfs = []
    allpdfs.append(components["nonResNominal_JJ_"+sig+"_"+purity+"_13TeV"])
    for p in pdflist.split(","):
        allpdfs.append(components[p])
    
    category = workspace.obj("CMS_channel")
    
    ## get variables from workspace 
    MJ1= workspace.var("MJ1");
    MJ2= workspace.var("MJ2");
    MJJ= workspace.var("MJJ");
    args = ROOT.RooArgSet(MJ1,MJ2,MJJ)
    arglist = ROOT.RooArgList(args)
     
    # get pdf for Wjets component from workspace:
    wjets_shape = workspace.pdf("shapeBkg_Wjet_JJ_WprimeWZ_HPHP_13TeV")
    wjets_shape.SetName("WJets_postfit")
    zjets_shape = workspace.pdf("shapeBkg_Zjet_JJ_WprimeWZ_HPHP_13TeV")
    ratio_wz = ROOT.RooRealVar("ratio","ratio",1.)
    #vjets_shape = ROOT.RooAddPdf("vjets_postfit","vjets_postfit",wjets_shape,zjets_shape,ratio_wz)
    vjets_shape = zjets_shape
    vjets_shape.SetName("v_jets_postfit")
     
    # make plots with QCD components and alternative shapes:
     
    vjets = ROOT.RooDataHist("data","data",arglist,ROOT.RooFit.Index(category),ROOT.RooFit.Import(category.getLabel(),V_jets_histo))
    # compare to QCD
    #doZprojection(allpdfs,vjets,nEvents,binsz,xBins_redux,xBins_redux,zBins,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
    #doXprojection(allpdfs,vjets,nEvents,binsxy,xBins,xBins,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
    #doYprojection(allpdfs,vjets,nEvents,binsxy,xBins_redux,xBins,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
     
    if vjets_shape!=None:
        #vjets_shape.fitTo(vjets)
        doZprojection([vjets_shape,pdf_shape],vjets,nEvents,binsz,xBins_redux,yBins_redux,zBins,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
        doXprojection([vjets_shape,pdf_shape],vjets,nEvents,binsxy,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
        doYprojection([vjets_shape,pdf_shape],vjets,nEvents,binsxy,yBins_redux,xBins_redux,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
        
        
        
    #data = getNominalData(bkg_histo,nEvents_qcd,[V_jets_histo],[nEvents],binsxy,binsz,args,category)
    #model_b.fitTo(data)
    #doZprojection([model_b,pdf_shape],data,nEvents+nEvents_qcd,binsz,xBins_redux,yBins_redux,zBins,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
    #doXprojection([model_b,pdf_shape],data,nEvents+nEvents_qcd,binsxy,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
    #doYprojection([model_b,pdf_shape],data,nEvents+nEvents_qcd,binsxy,yBins_redux,xBins_redux,zBins_redux,xBinsWidth,xBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,args,options)
    
    #print "set number of background events to " +str(nEvents_qcd)
    #print "number of wjets events "+str(nEvents)
    #print "normalise pdfs to "+str(nEvents+nEvents_qcd)
    