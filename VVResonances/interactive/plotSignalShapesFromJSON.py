#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
inFileName = "JJ_XqZ_MVV.json"
massPoints = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,6000]
# massPoints = [3500,4000,4500,5000,6000]


def main():
    with open(inFileName) as jsonFile:
        j = json.load(jsonFile)
    
    c1 = ROOT.TCanvas("c1", "c1", 800, 600)
    c1.Draw()
    graphs = []
    leg = ROOT.TLegend(0.8, 0.2, 0.95, 0.8)
    mjj = ROOT.RooRealVar("mjj","Dijet invariant mass (GeV)",7000,700,8000)
    frame = mjj.frame()
    for i, MH in enumerate(massPoints):  # mind that MH is evaluated below
        pdfName 	= "signal_%d" % MH
        Jmean 		= eval(j['MEAN'])
        Jsigma		= eval(j['SIGMA'])
        Jscalesigma	= eval(j['SCALESIGMA'])
        Jalpha 		= eval(j['ALPHA'])
        Jn 			= eval(j['N'])
        Jf 			= eval(j['f'])

        mean        = ROOT.RooRealVar("mean","mean"				,Jmean 		)
        sigma       = ROOT.RooRealVar("sigma","sigma"			,Jsigma		)
        scalesigma  = ROOT.RooRealVar("scalesigma","scalesigma"	,Jscalesigma	)
        alpha       = ROOT.RooRealVar("alpha","alpha"			,Jalpha 		)
        sign        = ROOT.RooRealVar("sign","sign"				,Jn 			)
        gsigma      = ROOT.RooFormulaVar("gsigma","@0*@1"		,ROOT.RooArgList(sigma,scalesigma))
        sigfrac     = ROOT.RooRealVar("sigfrac","sigfrac"		,Jf)
        

        scalesigma.setConstant(ROOT.kTRUE)
        sigfrac.setConstant(ROOT.kTRUE)
        alpha.setConstant(ROOT.kTRUE)
        sign.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
        
        
        gauss 	= ROOT.RooGaussian("gauss", "gauss", mjj, mean, gsigma)
        cb    	= ROOT.RooCBShape("cb", "cb",mjj, mean, sigma, alpha, sign)
        function = ROOT.RooAddPdf(pdfName, pdfName,gauss, cb, sigfrac)
        # nsig = ROOT.RooRealVar("NsExp", "Expected signal yield",500, 0, 1000)
        # function = ROOT.RooExtendPdf("mysig","mysig",sig_fit,nsig)
        # nsig.setConstant(ROOT.kTRUE)
        # function = signalResonanceCBGaus(pdfName,mjj,mean,sigma,scalesigma,alpha,sign,gsigma,sigfrac)
       
        function.plotOn(frame, ROOT.RooFit.LineColor(i+840),ROOT.RooFit.Name(str(MH)))#,ROOT.RooFit.Range(MH*0.8,1.2*MH))#ROOT.RooFit.Normalization(1, ROOT.RooAbsReal.RelativeExpected),
        leg.AddEntry(frame.findObject(str(MH)), "%d GeV" % MH, "L")
        # graphs.append(function)
    frame.Draw()
    leg.Draw("same")
    c1.SaveAs("signalShapes_%s.png" % inFileName.rsplit(".", 1)[0])
    sleep(5)


if __name__ == '__main__':
    main()
