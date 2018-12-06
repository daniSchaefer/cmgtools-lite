#!/usr/bin/env python
import ROOT
from array import array
from math import log,exp,sqrt
import os, sys, re, optparse,pickle,shutil,json
import json
import copy


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


def varyBins(histo,name,vary_bin):
    print "integral 2 : "+str(histo.Integral())
    newHisto= copy.deepcopy(histo)
    newHisto.SetName(name+"Up")
    newHistoD = copy.deepcopy(histo)
    newHistoD.SetName(name+"Down")
    
    print "integral newHisto "+str(newHisto.Integral())
    
    print "integral newHistoD "+str(newHistoD.Integral())
    newHisto.Scale(1e8)
    newHistoD.Scale(1e8)
    
    
    #newHisto.SetBinContent(vary_bin,1.1*histo.GetXaxis().GetBinCenter(vary_bin) )
    #newHistoD.SetBinContent(vary_bin,0.9*histo.GetXaxis().GetBinCenter(vary_bin) )
    n = newHisto.GetBinContent(vary_bin)
    print "n "+str(n)+" error "+str(ROOT.TMath.Sqrt(n))+" new "+str(n+ROOT.TMath.Sqrt(n))
    print "before "+str(newHisto.GetBinContent(vary_bin))
    newHisto.SetBinContent(vary_bin,n+ROOT.TMath.Sqrt(n))
    newHistoD.SetBinContent(vary_bin,n- ROOT.TMath.Sqrt(n))
    print "after "+str(newHisto.GetBinContent(vary_bin))
    
    print "histo "+str(histo.GetBinContent(vary_bin))
    
    return newHisto,newHistoD


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
histo_mvv = f.Get("mvv_nominal")
histo_mvv.SetName("mvv_nominal")



fout.cd()

alpha=1.5/800
histogram_pt_down,histogram_pt_up=unequalScale(histo_nominal,"histo_nominal_PT",alpha)
histogram_pt_down.Write()
histogram_pt_up.Write()

alpha=1.5*800.
histogram_opt_down,histogram_opt_up=unequalScale(histo_nominal,"histo_nominal_OPT",alpha,-1)
histogram_opt_down.Write()
histogram_opt_up.Write()

alpha=5000.*5000.
histogram_pt2_down,histogram_pt2_up=unequalScale(histo_nominal,"histo_nominal_PT2",alpha,2)
histogram_pt2_down.Write()
histogram_pt2_up.Write()

alpha=800.*800.
histogram_opt2_down,histogram_opt2_up=unequalScale(histo_nominal,"histo_nominal_OPT2",alpha,-2)
histogram_opt2_down.Write()
histogram_opt2_up.Write() 

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
 
print "integral "+str(histo_nominal.Integral())
varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin1",1)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())

fout.cd()
varyBinUp.Write()
varyBinDown.Write()

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin2",2)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())

fout.cd()
varyBinUp.Write()
varyBinDown.Write()

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin3",3)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())

fout.cd()
varyBinUp.Write()
varyBinDown.Write()

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin4",4)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())

fout.cd()
varyBinUp.Write()
varyBinDown.Write()

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin5",5)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()

varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin6",6)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()


varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin7",7)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()


varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin8",8)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()


varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin9",9)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()


varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin10",10)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()


varyBinUp,varyBinDown = varyBins(histo_nominal,"histo_bin11",11)
varyBinUp.Scale(histo_nominal.Integral()/varyBinUp.Integral())
varyBinDown.Scale(histo_nominal.Integral()/varyBinDown.Integral())
 
fout.cd()
varyBinUp.Write()
varyBinDown.Write()









histo_mvv.Write()
histo_nominal.SetName("histo_nominal")
histo_nominal.Write()
print "create output file "+options.output
os.system("mv tmp.root "+options.output)

c = ROOT.TCanvas("c","c",400,400)
histo_nominal.Draw("hist")
varyBinUp.SetLineColor(ROOT.kRed)
varyBinUp.Draw("histsame")
c.SetLogy()
c.SaveAs("test.pdf")
 
 
print histo_nominal.Integral()
print varyBinUp.Integral()
 
f.Close()
