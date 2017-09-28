#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
inFileName = "JJ_XqZ_MJJ_HP.json"
massPoints = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,6000]
# massPoints = [3500,4000,4500,5000,6000]

def main():
    with open(inFileName) as jsonFile:
        j = json.load(jsonFile)
    
    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    c1.Draw()
    graphs = []
    leg = ROOT.TLegend(0.8, 0.2, 0.95, 0.8)
    mjj = ROOT.RooRealVar("mjet","m_{jet} softdrop (GeV)",2900,30,610)
    frame = mjj.frame()
    for i, MH in enumerate(massPoints):  # mind that MH is evaluated below
        pdfName 	= "signal_%d" % MH
        Jmean 		= eval(j['mean'])
        Jsigma		= eval(j['sigma'])
        Jalpha 		= eval(j['alpha'])
        Jalpha2 	= eval(j['alpha2'])
        Jn 		= eval(j['n'])
        Jn2 		= eval(j['n2'])

        mean        = ROOT.RooRealVar("mean","mean",Jmean)
        sigma       = ROOT.RooRealVar("sigma","sigma",Jsigma)
        alpha       = ROOT.RooRealVar("alpha","alpha",Jalpha)
        alpha2      = ROOT.RooRealVar("alpha2","alpha2",Jalpha2)
        sign        = ROOT.RooRealVar("sign","sign",Jn)
        sign2        = ROOT.RooRealVar("sign2","sign2",Jn2)        

        alpha.setConstant(ROOT.kTRUE)
        sign.setConstant(ROOT.kTRUE)
        alpha2.setConstant(ROOT.kTRUE)
        sign2.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
        
	function = ROOT.RooDoubleCB(pdfName, pdfName, mjj, mean, sigma, alpha, sign,  alpha2, sign2)        
       
        function.plotOn(frame, ROOT.RooFit.LineColor(i+840),ROOT.RooFit.Name(str(MH)))#,ROOT.RooFit.Range(MH*0.8,1.2*MH))#ROOT.RooFit.Normalization(1, ROOT.RooAbsReal.RelativeExpected),
        leg.AddEntry(frame.findObject(str(MH)), "%d GeV" % MH, "L")
        # graphs.append(function)
    frame.Draw()
    leg.Draw("same")
    c1.SaveAs("signalShapes_%s.png" % inFileName.rsplit(".", 1)[0])
    sleep(1000)


if __name__ == '__main__':
    main()
