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

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    

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

def truncate(binning,mmin,mmax):
    res=[]
    for b in binning:
        if b >= mmin and b <= mmax:
            res.append(b)
    return res


## SMEAR WITH JET ENERGY SCALE UNCETAINTY AND RESOLUTION 
#def getJetEnergyScale( jet_LV,matched_genJet_LV ,JEC, JERSF,tag){
  #ptold    = jet_LV.Pt()
  #eta      = jet_LV.Eta()
  #phi      = jet_LV.Phi()
  #e        = jet_LV.E() 
  
    
  #corr     = JEC[0]
  #corrUp   = JEC[1]
  #corrDown = JEC[2]
  
  #jerSF      = JERSF[0]
  #jerSFUp    = JERSF[1]
  #jerSFDown  = JERSF[2]
  #jerSigmaPt = JERSF[3]
  
 
  ## Now do systematics
  #if tag.find("JESup")   != -1 :
    #pt = pt/corr 
    #pt = pt*corrUp
  #if tag.find("JESdown") != -1 :  
    #pt = pt/corr 
    #pt = pt*corrDown
  #if tag.find("JER") != -1 :
    #correction = jerSFDown
    #scaleFactor = jerSF
    #if tag.find("up")!=-1 :
        #correction = jerSFUp
    ##First try scaling:   
    
    #if  jet_LV.DeltaR(matched_genJet_LV) < 0.4 and abs(jet_LV.Pt()-matched_genJet_LV.Pt()) < (3*ptold*jerSigmaPt) :
        #if  correction < 1. : 
            #pt = max(0., matched_genJet_LV.Pt() + ( scaleFactor*(ptold-matched_genJet_LV.Pt()) ) )
        
    
    ##Scaling failed, move to smearing: 
    #else:
      #if  correction < 1.: pt = ptold
      #else:
        #pt = random.Gaus( ptold, ROOT.TMath.Sqrt(correction*correction-1)*(jerSigmaPt*jet_LV.Pt()) )

  #jet = ROOT.TLorentzVector()
  #jet.SetPtEtaPhiE(pt,eta,phi,e)
  #return jet

def fitGauss(htmp,mass):
    gauss  = ROOT.TF1("gauss" ,"gaus",0.85*mass,1.2*mass)  
    htmp.Fit(gauss,"R")
      
    mean = gauss.GetParameter(1)
    sigma = gauss.GetParameter(2)
    
    gauss_refined  = ROOT.TF1("gauss" ,"gaus",mean-2*sigma,mean+2*sigma)  
    htmp.Fit(gauss_refined,"R")
    
    mean = gauss_refined.GetParameter(1)
    sigma = gauss_refined.GetParameter(2)
    return [mean,sigma]


def getMVVJEC(pt,phi,eta,mass,weight):
    jet1 = ROOT.TLorentzVector()
    jet2 = ROOT.TLorentzVector()
    
    corr1 = weight[0]
    corr2 = weight[1]
        
    jet1.SetPtEtaPhiM(pt[0]*corr1,eta[0],phi[0],mass[0])
    jet2.SetPtEtaPhiM(pt[1]*corr2,eta[1],phi[1],mass[1])
        
    X = jet1+jet2
    MJJ = X.M()
    return MJJ


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-l","--located",dest="location",default='',help="storage path of input file")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output Root file",default='')
parser.add_option("-f","--scaleFactors",dest="scaleFactors",help="Additional scale factors separated by comma",default='1')
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary

samples={}

for filename in os.listdir(options.location):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        
    
    mass = float(fname.split('_')[-1])
    if mass < options.minMX or mass > options.maxMX: continue
        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 



scaleFactors=options.scaleFactors.split(',')


#Now we have the samples: Sort the masses and run the fits
N=0
SF=1
Fhists=[]
if options.scaleFactors!='':
    for s in scaleFactors:
        SF=SF*str(s)


logfile = open(options.output.replace(".txt","_JES.txt"),"w")
logfile.write("for signal samples "+str(options.output)+"\n")
logfile.write("mass   :    JES       :     JESUP     :  JESDown      :  difference % \n")

logfileJER = open(options.output.replace(".txt","_JER.txt"),"w")
logfileJER.write("for signal samples "+str(options.output)+"\n")
logfileJER.write("mass   :    JER       :     JERUP     :  JERDown      :  difference % \n")


for mass in sorted(samples.keys()):
    print 'fitting',str(mass)
    binning= truncate(getBinning(options.binsMVV,options.min,options.max,1000),0.75*mass,1.25*mass)
    rfile = ROOT.TFile(options.location+'/'+samples[mass]+'.root',"READ")
    tree = rfile.Get("tree")
    cache =ROOT.TFile("cache.root","RECREATE")
    truncated_tree = tree.CopyTree(options.cut)
    print tree.GetEntries()
    print truncated_tree.GetEntries()
    htmp_Up = ROOT.TH1F("histoUp_"+str(mass),"histoUp_"+str(mass),100,0.75*mass,1.25*mass)
    htmp_Down = ROOT.TH1F("histoDown_"+str(mass),"histoDown_"+str(mass),100,0.75*mass,1.25*mass)
    htmp = ROOT.TH1F("histo_"+str(mass),"histo_"+str(mass),100,0.75*mass,1.25*mass)
    
    JERhtmp_Up =    ROOT.TH1F("JERhistoUp_"+str(mass)  ,"JERhistoUp_"+str(mass),100,0.75*mass,1.25*mass)
    JERhtmp_Down =  ROOT.TH1F("JERhistoDown_"+str(mass),"JERhistoDown_"+str(mass),100,0.75*mass,1.25*mass)
    JERhtmp =       ROOT.TH1F("JERhisto_"+str(mass)    ,"JERhisto_"+str(mass),100,0.75*mass,1.25*mass)
    
    
    for event in truncated_tree:
        jet1 = ROOT.TLorentzVector()
        jet2 = ROOT.TLorentzVector()
        if options.triggerW: SF=SF*even.triggerWeight
        # JEC nominal ############################
        pt =   [event.jj_l1_pt[0]  ,event.jj_l2_pt[0]  ]
        eta =  [event.jj_l1_eta[0] ,event.jj_l2_eta[0] ]
        phi =  [event.jj_l1_phi[0] ,event.jj_l2_phi[0] ]
        lmass = [event.jj_l1_mass[0],event.jj_l2_mass[0]]
        if event.jj_l2_corr[0]==0 or event.jj_l1_corr[0]==0:
            print "corrections are 0"
            continue
        # JEC nominal ############################
        corr =[1,1]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        htmp.Fill(MJJ)#*event.genWeight*event.puWeight)
        # JEC up ############################
        corr = [event.jj_l1_corr_JECUp[0] / event.jj_l1_corr[0], event.jj_l2_corr_JECUp[0] / event.jj_l2_corr[0]]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        htmp_Up.Fill(MJJ)#*event.genWeight*event.puWeight)
        # JEC Down #############################
        corr = [event.jj_l1_corr_JECDown[0] / event.jj_l1_corr[0], event.jj_l2_corr_JECDown[0] / event.jj_l2_corr[0]]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        htmp_Down.Fill(MJJ)#*event.genWeight*event.puWeight)
        
        
        # JER nominal ############################
        if event.jj_l2_corr_JER[0]==0 or event.jj_l1_corr_JER[0]==0:
            print "JER corrections are 0"
            continue
        corr =[1,1]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        JERhtmp.Fill(MJJ)#*event.genWeight*event.puWeight)
        # JER up ############################
        corr = [event.jj_l1_corr_JERUp[0] / event.jj_l1_corr_JER[0], event.jj_l2_corr_JERUp[0] / event.jj_l2_corr_JER[0]]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        JERhtmp_Up.Fill(MJJ)#*event.genWeight*event.puWeight)
        # JER Down #############################
        corr = [event.jj_l1_corr_JERDown[0] / event.jj_l1_corr_JER[0], event.jj_l2_corr_JERDown[0] / event.jj_l2_corr_JER[0]]
        MJJ = getMVVJEC(pt,phi,eta,lmass,corr)
        JERhtmp_Down.Fill(MJJ)#*event.genWeight*event.puWeight)
        
    #Fhists.append([htmp,htmp_Down,htmp_Up]) 
    
    print htmp
    res     = fitGauss(htmp,mass)
    resUp   = fitGauss(htmp_Up,mass)
    resDown = fitGauss(htmp_Down,mass)
    logfile.write("       : mean ; sigma : mean ; sigma  :  mean ; sigma :  mean  ; sigma \n")
    logfile.write(str(mass) +" : "+str(round(res[0],2))+" ; "+ str(round(res[1],2))+" : "+str(round(resUp[0],2))+" ; "+ str(round(resUp[1],2))+" : " +str(round(resDown[0],2))+" ; "+ str(round(resDown[1],2))+" : ")
    if res[0]!=0 and res[1]!=0:
        logfile.write(str(round((1-resUp[0]/res[0])*100,2))+"/"+str(round((1-resDown[0]/res[0])*100,2)) +" ; "+str(round((1-resUp[1]/res[1])*100,2))+"/"+str(round((1-resDown[1]/res[1])*100,2))+"\n")
    else:
        logfile.write("\n")
    c = ROOT.TCanvas("c","c",800,800)
    c.cd(1)    
    htmp.Draw("hist")
    htmp_Up.SetLineColor(ROOT.kBlue)
    htmp_Up.Draw("histsame")
    htmp_Down.SetLineColor(ROOT.kRed)
    htmp_Down.Draw("histsame")
        
    print res    
    c.SaveAs(options.output.replace(".txt","_"+str(mass)+"_JES.pdf"))
    print "save canvas as "+options.output.replace(".txt",".pdf")
   
   
   
    res     = fitGauss(JERhtmp,mass)
    resUp   = fitGauss(JERhtmp_Up,mass)
    resDown = fitGauss(JERhtmp_Down,mass)
    logfileJER.write("       : mean ; sigma : mean ; sigma  :  mean ; sigma :  mean  ; sigma \n")
    logfileJER.write(str(mass) +" : "+str(round(res[0],2))+" ; "+ str(round(res[1],2))+" : "+str(round(resUp[0],2))+" ; "+ str(round(resUp[1],2))+" : " +str(round(resDown[0],2))+" ; "+ str(round(resDown[1],2))+" : ")
    if res[0]!=0 and res[1]!=0:
        logfileJER.write(str(round((1-resUp[0]/res[0])*100,2))+"/"+str(round((1-resDown[0]/res[0])*100,2)) +" ; "+str(round((1-resUp[1]/res[1])*100,2))+"/"+str(round((1-resDown[1]/res[1])*100,2))+"\n")
    else:
        logfileJER.write("\n")
    c2 = ROOT.TCanvas("c","c",800,800)
    c2.cd()
    legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
    JERhtmp.SetLineColor(ROOT.kBlack)
    JERhtmp.Draw("hist")
    JERhtmp_Up.SetLineColor(ROOT.kBlue)
    JERhtmp_Up.Draw("histsame")
    JERhtmp_Down.SetLineColor(ROOT.kRed)
    JERhtmp_Down.Draw("histsame")
    legend.AddEntry(JERhtmp_Down,"JER down","l")
    legend.AddEntry(JERhtmp,"nominal" ,"l")
    legend.AddEntry(JERhtmp_Up, "JER up","l")
    
    text = ROOT.TLatex()
    text.DrawLatex(mass-100,1000,"#color[2]{#mu ="+str(round(resDown[0],2))+" #sigma = "+str(round(resDown[1],2))+" }; #mu ="+str(round(resDown[0],2))+" #sigma = "+str(round(resDown[1],2))+"  ;#color[4]{#mu ="+str(round(resUp[0],2))+" #sigma = "+str(round(resUp[1],2))+" }" )

    c2.SaveAs(options.output.replace(".txt","_"+str(mass)+"_JER.pdf"))
logfile.close() 
logfileJER.close()
    
    



