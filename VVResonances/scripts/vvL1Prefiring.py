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



def getEfficiency(SF,effmap,jet1,jet2):
    if jet2.Pt() > 500.:
        b2 = effmap.FindFixBin(jet2.Eta(),488.)
    else: 
        b2 = effmap.FindFixBin(jet2.Eta(),jet2.Pt())
    if jet1.Pt() > 500.:
        b = effmap.FindFixBin(jet1.Eta(),488.)    
    else: 
        b  = effmap.FindFixBin(jet1.Eta(),jet1.Pt())
    
    
    eff1 = effmap.GetBinContent(b)
    eff2 = effmap.GetBinContent(b2)
    
    if ROOT.TMath.Abs(jet1.Eta()) > 1.75 or ROOT.TMath.Abs(jet1.Eta()) > 1.75:
        print "jet 1 "+str(jet1.Eta()) + "  "+str(jet1.Pt())
        print "jet 2 "+str(jet2.Eta()) + "  "+str(jet2.Pt())
        
        print "jet 1 "+str(jet1.Eta()) + "  "+str(jet1.Pt())+" eff1 "+str(eff1)
        print "jet 2 "+str(jet2.Eta()) + "  "+str(jet2.Pt())+" eff2 "+str(eff2)
    
    
    finalSF = float(SF)*(1-eff1)*(1-eff2)
    return finalSF





parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-l","--located",dest="location",default='',help="storage path of input file")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output Root file",default='')
parser.add_option("--map",dest="effmap",help="efficiency map Root file",default='')
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
        
    print fname.split('_')[-1]
    mass = float(fname.split('_')[-1])
    if mass < options.minMX or mass > options.maxMX: continue
        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 
    
#Now we have the samples: Sort the masses and run the fits

scaleFactors=options.scaleFactors.split(',')
N=0
SF=1
if options.scaleFactors!='':
    for s in scaleFactors:
        SF=SF*str(s)


logfile = open(options.output.replace(".txt","_L1prefiring.txt"),"w")
logfile.write("for signal samples "+str(options.output)+"\n")
logfile.write("mass   :    nominal       :     L1 SF applied     :  difference % \n")


print "open efficiency map for L1 prefiring issue : "
file_effmap = ROOT.TFile(options.effmap,"READ")
effmap = file_effmap.Get("L1prefiring_jet_2017BtoF")
result = {}

for mass in sorted(samples.keys()):
    print 'using mass point ',str(mass)
    #binning= truncate(getBinning(options.binsMVV,options.min,options.max,1000),0.75*mass,1.25*mass)
    rfile = ROOT.TFile(options.location+'/'+samples[mass]+'.root',"READ")
    tree = rfile.Get("tree")
    cache =ROOT.TFile("cache.root","RECREATE")
    print options.cut
    truncated_tree = tree.CopyTree(options.cut)
    print tree.GetEntries()
    print truncated_tree.GetEntries()
    result[mass]={"nominal":1, "L1":1}
    
    for event in truncated_tree:
        jet1 = ROOT.TLorentzVector()
        jet2 = ROOT.TLorentzVector()
        if options.triggerW: SF=SF*event.triggerWeight
        
        jet1.SetPtEtaPhiM(event.jj_l1_pt[0],event.jj_l1_eta[0],event.jj_l1_phi[0],event.jj_l1_mass[0])
        jet2.SetPtEtaPhiM(event.jj_l2_pt[0],event.jj_l2_eta[0],event.jj_l2_phi[0],event.jj_l2_mass[0])
        
        #print SF
        result[mass]["nominal"] +=float(SF)
        result[mass]["L1"]+=getEfficiency(SF,effmap,jet1,jet2)

    logfile.write(str(mass)+"  :  "+str(result[mass]["nominal"])+"  :  "+str(result[mass]["L1"])+"  :  "+str(1-result[mass]["L1"]/result[mass]["nominal"])+" \n")

print result
       
    
