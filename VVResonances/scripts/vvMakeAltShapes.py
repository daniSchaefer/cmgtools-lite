#!/usr/bin/env python
import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy
import math


parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output",default='')
#parser.add_option("-n","--nominal",dest="nominal",help="get nominal histogram",default='JJ_nonRes_CONDL1_HPHP.root')
parser.add_option("-a","--altshape",dest="altshape",default='',help="alternative shape")
parser.add_option("--altshape2",dest="altshape2",help="second altenative shape.",default='')

parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins",default=1)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="conditional bins split by comma",default=1)
parser.add_option("-x","--minx",dest="minx",type=float,help="bins",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float,help="conditional bins split by comma",default=1)
parser.add_option("-y","--miny",dest="miny",type=float,help="bins",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float,help="conditional bins split by comma",default=1)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")


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


def varyBins(histo,name):
    newHisto= copy.deepcopy(histo)
    newHisto.SetName(name+"Up")
    newHistoD = copy.deepcopy(histo)
    newHistoD.SetName(name+"Down")
    
    #newHisto.Scale(1e16)
    #newHistoD.Scale(1e16)
    
    
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        for j in range(1,histo.GetNbinsY()+1):
            n = histo.GetBinContent(i,j)*1e16
            if n <= 0:
                continue
            e = n/2#ROOT.TMath.Sqrt(n)*10
            new = n + e 
            newD = n - e
            if( j%2 == 0):
                new = n-e
                newD = n +e
            #print "value "+str(n)+" variation "+str(e)    
            #print "new "+str(new)    
            newHisto.SetBinContent(i,j,new)
            newHistoD.SetBinContent(i,j,newD)
    #conditional(newHisto)
    #conditional(newHistoD)
    print histo.GetNbinsY()
    return newHisto,newHistoD


def unequalScale(histo,name,alpha,power=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    minx = histo.GetXaxis().GetXmin()
    maxx = histo.GetXaxis().GetXmax()
    if minx != 0:
        maxFactor = max(pow(maxx,power),pow(minx,power))
    else:
        maxFactor = max(pow(maxx,power),pow(0.5,power))#pow(maxx,power)
    for i in range(1,histo.GetNbinsX()+1):
        x= histo.GetXaxis().GetBinCenter(i)
        for j in range(1,histo.GetNbinsY()+1):
            nominal=histo.GetBinContent(i,j)
            factor = 1+alpha*pow(x,power) 
            newHistoU.SetBinContent(i,j,nominal*factor)
            newHistoD.SetBinContent(i,j,nominal/factor)
    if newHistoU.Integral()>0.0:        
        newHistoU.Scale(1.0/newHistoU.Integral())        
    if newHistoD.Integral()>0.0:        
        newHistoD.Scale(1.0/newHistoD.Integral())        
    return newHistoU,newHistoD 
    
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
    histogram=ROOT.TH2F(histo.GetName(),"histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
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
        for j in range(1,hist.GetNbinsX()+1):
            if integral==0.0:
                print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
                hist.SetBinContent(j,i,0)
            else:
                hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)


(options,args) = parser.parse_args()

print options.output
f = ROOT.TFile(options.output,"READ")
fout = ROOT.TFile("tmp.root","RECREATE")

histo_nominal = f.Get("histo_nominal")
print histo_nominal
histo_nominal.SetName("histo")
histo_mvv = f.Get("histo_nominal_coarse")
histo_mvv.SetName("histo_nominal_coarse")



fout.cd()
alpha=1.5/5.
histogram_pt_down,histogram_pt_up=unequalScale(histo_nominal,"histo_nominal_PT",alpha)
conditional(histogram_pt_down)
histogram_pt_down.Write()
conditional(histogram_pt_up)
histogram_pt_up.Write()

alpha=1.5*5.
h1,h2=unequalScale(histo_nominal,"histo_nominal_OPT",alpha,-1)
conditional(h1)
h1.Write()
conditional(h2)
h2.Write()

alpha=1.5/5.
h1,h2=unequalScale(histo_nominal,"histo_nominal_OPT2",alpha,2)
conditional(h1)
h1.Write()
conditional(h2)
h2.Write()

print "add alternative shapes"

if options.altshape != "":
    tmp = ROOT.TFile(options.altshape,"READ")
    histo_altshape = tmp.Get("histo_nominal")
    histo_altshape.SetName("histo_altshapeUp")
    fout.cd()
    histo_altshape.Write()
    tmp.Close()
  
print "add alternative shapes 2"  
if options.altshape2 != "":
    tmp = ROOT.TFile(options.altshape2,"READ")
    histo_altshape = tmp.Get("histo_nominal")
    histo_altshape.SetName("histo_altshape2")
    fout.cd()
    histo_altshape.Write()    
    tmp.Close()
 

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin")
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()
histo_mvv.Write()
histo_nominal.SetName("histo_nominal")
histo_nominal.Write()
os.system("mv tmp.root "+options.output)
 
print histo_nominal.Integral()
print varyBinUp.Integral()
 
f.Close()
