#!/usr/bin/env python

import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json


def getBinning(histo):
    b = []
    for i in range(1,histo.GetNbinsX()+2):
        b.append(histo.GetBinLowEdge(i))
    return array('d',b)

def makeHisto(name,fx,nhistox,fy,nhistoy,fz,nhistoz,fout):
    histox=fx.Get(nhistox)
    histoy=fy.Get(nhistoy)
    histoz=fz.Get(nhistoz)
    try:
        if histox == None: 
            raise TypeError
        if histoy == None: 
            raise TypeError
        if histoz == None: 
            raise TypeError
    except TypeError: return -1
    hxx = histox.ProjectionX("projX")
    hxy = histox.ProjectionY("projY")
    binningx= getBinning(hxx)
    binningz= getBinning(hxy)
    binningz2= getBinning(histoz)
    binningz3= getBinning(histoy.ProjectionY("projY2"))
    #print binningx
    #print binningz
    #print binningz2
    #print binningz3
   
    #print len(binningz)-1
    #print histoz.GetNbinsX() 
    h=ROOT.TH3F(name,name,len(binningx)-1,binningx,len(binningx)-1,binningx,len(binningz)-1,binningz)
    for k in range(1,histoz.GetNbinsX()+2):
     for j in range(1,histoy.GetNbinsX()+2):
        for i in range(1,histox.GetNbinsX()+2):
            c = histoz.GetBinContent(k)*histox.GetBinContent(i,k)*histoy.GetBinContent(j,k)
            #if c == 0:
            #    print histoz.GetBinCenter(k)
            h.SetBinContent(i,j,k,c)
    fout.cd()
    h.Write()


parser = optparse.OptionParser()
parser.add_option("-s","--systX",dest="systX",default='',help="Comma   separated and semicolon separated systs for p0 ")
parser.add_option("-S","--systY",dest="systY",default='',help="Comma   separated and semicolon separated systs for p1 ")
parser.add_option("-C","--systCommon",dest="systCommon",default='',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-i","--inputX",dest="inputX",default='erfexp',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-I","--inputY",dest="inputY",default='erfexp',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-z","--inputZ",dest="inputZ",default='erfexp',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-o","--output",dest="output",help="Output ROOT File",default='')


(options,args) = parser.parse_args()
#define output dictionary

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

inputx=ROOT.TFile(options.inputX)
inputy=ROOT.TFile(options.inputY)
inputz=ROOT.TFile(options.inputZ)
output=ROOT.TFile(options.output,"RECREATE")

print options.inputX
print options.inputY
print options.inputZ
print options.output

print "Merge nominal"
makeHisto("histo",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal",output)
print "   - pt x up/down"
makeHisto("histo_PTXUp",inputx,"histo_nominal_PTUp",inputy,"histo_nominal",inputz,"histo_nominal",output)
makeHisto("histo_PTXDown",inputx,"histo_nominal_PTDown",inputy,"histo_nominal",inputz,"histo_nominal",output)
print "   - pt y up/down"
makeHisto("histo_PTYUp",inputx,"histo_nominal",inputy,"histo_nominal_PTUp",inputz,"histo_nominal",output)
makeHisto("histo_PTYDown",inputx,"histo_nominal",inputy,"histo_nominal_PTDown",inputz,"histo_nominal",output)
print "   - pt z up/down"
makeHisto("histo_PTZUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_PTUp",output)
makeHisto("histo_PTZDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_PTDown",output)
print "   - pt x,y,z up/down"
makeHisto("histo_PTUp",inputx,"histo_nominal_PTUp",inputy,"histo_nominal_PTUp",inputz,"histo_nominal_PTUp",output)
makeHisto("histo_PTDown",inputx,"histo_nominal_PTDown",inputy,"histo_nominal_PTDown",inputz,"histo_nominal_PTDown",output)
print "   - pt (x,y) up/down"
makeHisto("histo_PTXYUp",inputx,"histo_nominal_PTUp",inputy,"histo_nominal_PTUp",inputz,"histo_nominal",output)
makeHisto("histo_PTXYDown",inputx,"histo_nominal_PTDown",inputy,"histo_nominal_PTDown",inputz,"histo_nominal",output)
print "   - pt2 (x,y) up/down"
makeHisto("histo_PT2XYUp",inputx,"histo_nominal_PT2Up",inputy,"histo_nominal_PT2Up",inputz,"histo_nominal",output)
makeHisto("histo_PT2XYDown",inputx,"histo_nominal_PT2Down",inputy,"histo_nominal_PT2Down",inputz,"histo_nominal",output)
print "   - pt2 z up/down"
makeHisto("histo_PTZ2Up",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_PT2Up",output)
makeHisto("histo_PTZ2Down",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_PT2Down",output)
print "   - pt (x,z) up/down"
makeHisto("histo_PTXZUp",inputx,"histo_nominal_PTUp",inputy,"histo_nominal",inputz,"histo_nominal_PTUp",output)
makeHisto("histo_PTXZDown",inputx,"histo_nominal_PTDown",inputy,"histo_nominal",inputz,"histo_nominal_PTUp",output)
print "   - pt (y,z) up/down"
makeHisto("histo_PTYZUp",inputx,"histo_nominal",inputy,"histo_nominal_PTUp",inputz,"histo_nominal_PTUp",output)
makeHisto("histo_PTYZDown",inputx,"histo_nominal",inputy,"histo_nominal_PTDown",inputz,"histo_nominal_PTUp",output)
print "   - pt2 x,y,z up/down"
makeHisto("histo_PT2Up",inputx,"histo_nominal_PT2Up",inputy,"histo_nominal_PT2Up",inputz,"histo_nominal_PT2Up",output)
makeHisto("histo_PT2Down",inputx,"histo_nominal_PT2Down",inputy,"histo_nominal_PT2Down",inputz,"histo_nominal_PT2Down",output)

print "   - Opt x up/down"
makeHisto("histo_OPTXUp",inputx,"histo_nominal_OPTUp",inputy,"histo_nominal",inputz,"histo_nominal",output)
makeHisto("histo_OPTXDown",inputx,"histo_nominal_OPTDown",inputy,"histo_nominal",inputz,"histo_nominal",output)
print "   - Opt y up/down"
makeHisto("histo_OPTYUp",inputx,"histo_nominal",inputy,"histo_nominal_OPTUp",inputz,"histo_nominal",output)
makeHisto("histo_OPTYDown",inputx,"histo_nominal",inputy,"histo_nominal_OPTDown",inputz,"histo_nominal",output)
print "   - Opt z up/down"
makeHisto("histo_OPTZUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_OPTUp",output)
makeHisto("histo_OPTZDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_OPTDown",output)
print "   - Opt x,y,z up/down"
makeHisto("histo_OPTUp",inputx,"histo_nominal_OPTUp",inputy,"histo_nominal_OPTUp",inputz,"histo_nominal_OPTUp",output)
makeHisto("histo_OPTDown",inputx,"histo_nominal_OPTDown",inputy,"histo_nominal_OPTDown",inputz,"histo_nominal_OPTDown",output)
print "   - Opt (x,y) up/down"
makeHisto("histo_OPTXYUp",inputx,"histo_nominal_OPTUp",inputy,"histo_nominal_OPTUp",inputz,"histo_nominal",output)
makeHisto("histo_OPTXYDown",inputx,"histo_nominal_OPTDown",inputy,"histo_nominal_OPTDown",inputz,"histo_nominal",output)
print "   - Opt2 (x,y) up/down"
makeHisto("histo_OPT2XYUp",inputx,"histo_nominal_OPT2Up",inputy,"histo_nominal_OPT2Up",inputz,"histo_nominal",output)
makeHisto("histo_OPT2XYDown",inputx,"histo_nominal_OPT2Down",inputy,"histo_nominal_OPT2Down",inputz,"histo_nominal",output)
print "   - Opt2 z up/down"
makeHisto("histo_OPTZ2Up",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_OPT2Up",output)
makeHisto("histo_OPTZ2Down",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_OPT2Down",output)
print "   - logpt z up/down"
makeHisto("histo_LOGPTUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_LOGPTUp",output)
makeHisto("histo_LOGPTDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_LOGPTDown",output)
print "   - logpt z up/down"
makeHisto("histo_LOGPTOPTUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_LOGPTOPTUp",output)
makeHisto("histo_LOGPTOPTDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_nominal_LOGPTOPTDown",output)
print "   - opt (x,z) up/down"
makeHisto("histo_OPTXZUp",inputx,"histo_nominal_OPTUp",inputy,"histo_nominal",inputz,"histo_nominal_OPTUp",output)
makeHisto("histo_OPTXZDown",inputx,"histo_nominal_OPTDown",inputy,"histo_nominal",inputz,"histo_nominal_OPTUp",output)
print "   - opt (y,z) up/down"
makeHisto("histo_OPTYZUp",inputx,"histo_nominal",inputy,"histo_nominal_OPTUp",inputz,"histo_nominal_OPTUp",output)
makeHisto("histo_OPTYZDown",inputx,"histo_nominal",inputy,"histo_nominal_OPTDown",inputz,"histo_nominal_OPTUp",output)
print "   - opt2 x,y,z up/down"
makeHisto("histo_OPT2Up",inputx,"histo_nominal_OPT2Up",inputy,"histo_nominal_OPT2Up",inputz,"histo_nominal_OPT2Up",output)
makeHisto("histo_OPT2Down",inputx,"histo_nominal_OPT2Down",inputy,"histo_nominal_OPT2Down",inputz,"histo_nominal_OPT2Down",output)

print "  - herwig x"
makeHisto("histo_altshapeXUp",inputx,"histo_altshapeUp",inputy,"histo_nominal",inputz,"histo_nominal",output)
makeHisto("histo_altshapeXDown",inputx,"histo_altshapeDown",inputy,"histo_nominal",inputz,"histo_nominal",output)
print "  - herwig y"
makeHisto("histo_altshapeYUp",inputx,"histo_nominal",inputy,"histo_altshapeUp",inputz,"histo_nominal",output)
makeHisto("histo_altshapeYDown",inputx,"histo_nominal",inputy,"histo_altshapeDown",inputz,"histo_nominal",output)
print "  - herwig z"
makeHisto("histo_altshapeZUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_altshapeUp",output)
makeHisto("histo_altshapeZDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_altshapeDown",output)
print "  - herwig (x,y)"
makeHisto("histo_altshapeXYUp",inputx,"histo_altshapeUp",inputy,"histo_altshapeUp",inputz,"histo_nominal",output)
makeHisto("histo_altshapeXYDown",inputx,"histo_altshapeDown",inputy,"histo_altshapeDown",inputz,"histo_nominal",output)

print "  - madgraph x"
makeHisto("histo_altshape2XUp",inputx,"histo_altshape2Up",inputy,"histo_nominal",inputz,"histo_nominal",output)
makeHisto("histo_altshape2XDown",inputx,"histo_altshape2Down",inputy,"histo_nominal",inputz,"histo_nominal",output)
print "  - madgraph y"
makeHisto("histo_altshape2YUp",inputx,"histo_nominal",inputy,"histo_altshape2Up",inputz,"histo_nominal",output)
makeHisto("histo_altshape2YDown",inputx,"histo_nominal",inputy,"histo_altshape2Down",inputz,"histo_nominal",output)
print "  - madgraph z"
makeHisto("histo_altshape2ZUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_altshape2Up",output)
makeHisto("histo_altshape2ZDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_altshape2Down",output)
print "  - madgraph (x,y)"
makeHisto("histo_altshape2XYUp",inputx,"histo_altshape2Up",inputy,"histo_altshape2Up",inputz,"histo_nominal",output)
makeHisto("histo_altshape2XYDown",inputx,"histo_altshape2Down",inputy,"histo_altshape2Down",inputz,"histo_nominal",output)

print "  - powheg z"
makeHisto("histo_altshape3ZUp",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_NLO",output)
makeHisto("histo_altshape3ZDown",inputx,"histo_nominal",inputy,"histo_nominal",inputz,"histo_NLODown",output)

print "Merge herwig"
makeHisto("histo_altshapeUp",inputx,"histo_altshapeUp",inputy,"histo_altshapeUp",inputz,"histo_altshapeUp",output)
makeHisto("histo_altshapeDown",inputx,"histo_altshapeDown",inputy,"histo_altshapeDown",inputz,"histo_altshapeDown",output)
print "Merge madgraph"
makeHisto("histo_altshape2Up",inputx,"histo_altshape2Up",inputy,"histo_altshape2Up",inputz,"histo_altshape2Up",output)
makeHisto("histo_altshape2Down",inputx,"histo_altshape2Up",inputy,"histo_altshape2Up",inputz,"histo_altshape2Up",output)
print "Merge NLO"
makeHisto("histo_NLO",inputx,"histo_NLO",inputy,"histo_NLO",inputz,"histo_NLO",output)

print "Write file "+options.output

inputx.Close()
inputy.Close()
inputz.Close()
output.Close()



