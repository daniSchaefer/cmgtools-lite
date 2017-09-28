#!/usr/bin/env python

import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json


def makeHisto(name,fx,nhistox,fy,nhistoy,fout):
    histox=fx.Get(nhistox)
    histoy=fy.Get(nhistoy)
    h=ROOT.TH2F(name,name,histox.GetNbinsX(),histox.GetXaxis().GetXmin(),histox.GetXaxis().GetXmax(),histox.GetNbinsY(),histox.GetYaxis().GetXmin(),histox.GetYaxis().GetXmax())
    for i in range(1,histoy.GetNbinsX()+1):
        for j in range(1,histox.GetNbinsX()+1):
            h.SetBinContent(j,i,histoy.GetBinContent(i)*histox.GetBinContent(j,i))
    fout.cd()
    h.Write()


parser = optparse.OptionParser()
parser.add_option("-s","--systX",dest="systX",default='',help="Comma   separated and semicolon separated systs for p0 ")
parser.add_option("-S","--systY",dest="systY",default='',help="Comma   separated and semicolon separated systs for p1 ")
parser.add_option("-C","--systCommon",dest="systCommon",default='',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-i","--inputX",dest="inputX",default='erfexp',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-I","--inputY",dest="inputY",default='erfexp',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-o","--output",dest="output",help="Output ROOT File",default='')


(options,args) = parser.parse_args()
#define output dictionary

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

'''
systX={}
tmp=options.systX.split(',')
for s in tmp:
    tmp2=s.split(':')
    systX[tmp2[0]]=tmp2[1]

systY={}
tmp=options.systY.split(',')
for s in tmp:
    tmp2=s.split(':')
    systY[tmp2[0]]=tmp2[1]

systC={}
tmp=options.systCommon.split(',')
for s in tmp:
    tmp2=s.split(':')
    systC[tmp2[0]]=tmp2[1]
'''

inputx=ROOT.TFile(options.inputX)
inputy=ROOT.TFile(options.inputY)
output=ROOT.TFile(options.output,"RECREATE")


makeHisto("histo_nominal",inputx,"histo_nominal",inputy,"histo_nominal",output)
makeHisto("histo_altshapeUp",inputx,"histo_altshapeUp",inputy,"histo_altshapeUp",output)
makeHisto("histo_altshapeDown",inputx,"histo_altshapeDown",inputy,"histo_altshapeDown",output)

'''
for systName,systNewName in systC.iteritems():
    makeHisto("histo_"+systNewName+"Up",inputx,"histo_"+systName+"Up",inputy,"histo_"+systName+"Up",output)
    makeHisto("histo_"+systNewName+"Down",inputx,"histo_"+systName+"Down",inputy,"histo_"+systName+"Down",output)

for systName,systNewName in systX.iteritems():
    makeHisto("histo_"+systNewName+"Up",inputx,"histo_"+systName+"Up",inputy,"histo",output)
    makeHisto("histo_"+systNewName+"Down",inputx,"histo_"+systName+"Down",inputy,"histo",output)

for systName,systNewName in systY.iteritems():
    makeHisto("histo_"+systNewName+"Up",inputx,"histo",inputy,"histo_"+systName+"Up",output)
    makeHisto("histo_"+systNewName+"Down",inputx,"histo",inputy,"histo_"+systName+"Down",output)
'''

inputx.Close()
inputy.Close()
output.Close()



