3#!/bin/env python
import ROOT
import json
import math
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from time import sleep
import optparse, sys
from  CMGTools.VVResonances.plotting.CMS_lumi import *

ROOT.gROOT.SetBatch(True)

def getCanvas(name="c1"):
	
	H_ref = 600
	W_ref = 800
	W = W_ref
	H  = H_ref
	
	T = 0.08*H_ref
	B = 0.12*H_ref 
	L = 0.12*W_ref
	R = 0.04*W_ref
	canvas = ROOT.TCanvas(name,name,50,50,W,H)
	canvas.SetFillColor(0)
	canvas.SetBorderMode(0)
	canvas.SetFrameFillStyle(0)
	canvas.SetFrameBorderMode(0)
	canvas.SetLeftMargin( L/W )
	canvas.SetRightMargin( R/W )
	canvas.SetTopMargin( T/H )
	canvas.SetBottomMargin( B/H )
	canvas.SetTickx(0)
	canvas.SetTicky(0)
	
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
	canvas.cd()
	
	return canvas
	
def getMVVPdf(j,MH):

        var = w.var(options.var)
	
        pdfName 	= "signal_%d" % MH
        Jmean 		= eval(j['MEAN'])
        Jsigma		= eval(j['SIGMA'])
        Jscalesigma	= eval(j['SCALESIGMA'])
        Jalpha 		= eval(j['ALPHA'])
        Jn 		= eval(j['N'])
        Jf 		= eval(j['f'])

        mean        = ROOT.RooRealVar("mean_%d"%MH,"mean_%d"%MH,Jmean)
        sigma       = ROOT.RooRealVar("sigma","sigma_%d"%MH,Jsigma)
        scalesigma  = ROOT.RooRealVar("scalesigma_%d"%MH,"scalesigma_%d"%MH,Jscalesigma)
        alpha       = ROOT.RooRealVar("alpha_%d"%MH,"alpha_%d"%MH,Jalpha)
        sign        = ROOT.RooRealVar("sign_%d"%MH,"sign_%d"%MH,Jn)
        gsigma      = ROOT.RooFormulaVar("gsigma_%d"%MH,"@0*@1",ROOT.RooArgList(sigma,scalesigma))
        sigfrac     = ROOT.RooRealVar("sigfrac_%d"%MH,"sigfrac_%d"%MH,Jf)
        

        scalesigma.setConstant(ROOT.kTRUE)
        sigfrac.setConstant(ROOT.kTRUE)
        alpha.setConstant(ROOT.kTRUE)
        sign.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
        
        
        gauss 	= ROOT.RooGaussian("gauss_%d"%MH, "gauss_%d"%MH, var, mean, gsigma)
        cb    	= ROOT.RooCBShape("cb_%d"%MH, "cb_%d"%MH,var, mean, sigma, alpha, sign)
        function = ROOT.RooAddPdf(pdfName, pdfName,gauss, cb, sigfrac) 
        getattr(w,'import')(function,ROOT.RooFit.Rename(pdfName))

def getMJPdf(j,MH):
 
        var = w.var(options.var)
	
        pdfName 	= "signal_%d" % MH
        Jmean 		= eval(j['mean'])
        Jsigma		= eval(j['sigma'])
        Jalpha 		= eval(j['alpha'])
        Jalpha2 	= eval(j['alpha2'])
        Jn 		= eval(j['n'])
        Jn2 		= eval(j['n2'])

        mean        = ROOT.RooRealVar("mean_%d"%MH,"mean_%d"%MH,Jmean)
        sigma       = ROOT.RooRealVar("sigma_%d"%MH,"sigma_%d"%MH,Jsigma)
        alpha       = ROOT.RooRealVar("alpha_%d"%MH,"alpha_%d"%MH,Jalpha)
        alpha2      = ROOT.RooRealVar("alpha2_%d"%MH,"alpha2_%d"%MH,Jalpha2)
        sign        = ROOT.RooRealVar("sign_%d"%MH,"sign_%d"%MH,Jn)
        sign2        = ROOT.RooRealVar("sign2_%d"%MH,"sign2_%d"%MH,Jn2)        

        alpha.setConstant(ROOT.kTRUE)
        sign.setConstant(ROOT.kTRUE)
        alpha2.setConstant(ROOT.kTRUE)
        sign2.setConstant(ROOT.kTRUE)
        mean.setConstant(ROOT.kTRUE)
        sigma.setConstant(ROOT.kTRUE)
        
	function = ROOT.RooDoubleCB(pdfName, pdfName, var, mean, sigma, alpha, sign,  alpha2, sign2)  
	getattr(w,'import')(function,ROOT.RooFit.Rename(pdfName))
		
parser = optparse.OptionParser()
parser.add_option("-f","--file",dest="file",default='',help="input file")
parser.add_option("-v","--var",dest="var",help="mVV or mJ",default='mVV')
parser.add_option("-l","--leg",dest="leg",help="mVV or mJ",default='l1')
postfix = "Leading jet "
(options,args) = parser.parse_args()
if options.leg == "l2" !=-1: postfix = "Second leading jet "

inFileName = options.file
massPoints = [1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
varName = {'mVV':'Dijet invariant mass (GeV)','mJ':'%sm_{jet} softdrop (GeV)'%postfix}
varBins = {'mVV':'[132,700,6000]','mJ':'[80,55,215]'}
w=ROOT.RooWorkspace("w","w")
w.factory(options.var+varBins[options.var])
w.var(options.var).SetTitle(varName[options.var])
        
def main():
    with open(inFileName) as jsonFile:
      j = json.load(jsonFile)
    
      c1 = getCanvas()
      c1.Draw()
      leg = ROOT.TLegend(0.8, 0.2, 0.95, 0.8)
      frame = w.var(options.var).frame()   
      
      for i, MH in enumerate(massPoints):  # mind that MH is evaluated below
        if options.var == 'mVV': getMVVPdf(j,MH)
        else: getMJPdf(j,MH)
        w.pdf('signal_%d'%MH).plotOn(frame, ROOT.RooFit.LineColor(i+840),ROOT.RooFit.Name(str(MH)))#,ROOT.RooFit.Range(MH*0.8,1.2*MH))#ROOT.RooFit.Normalization(1, ROOT.RooAbsReal.RelativeExpected),
        leg.AddEntry(frame.findObject(str(MH)), "%d GeV" % MH, "L")
      frame.GetYaxis().SetTitle("A.U")
      frame.SetMaximum(0.1)
      if options.var == 'mVV':frame.SetMaximum(0.7)
      frame.Draw()
      leg.Draw("same")
      model = "G_{bulk} #rightarrow WW"
      if options.file.find("ZZ")!=-1:
          model = "G_{bulk} #rightarrow ZZ"
      if options.file.find("WZ")!=-1:
          model = "W' #rightarrow WZ"
      if options.file.find("Zprime")!=-1:
          model = "Z' #rightarrow WW"
      if   options.file.find("HPHP")!=-1: purity = "HPHP"
      elif options.file.find("HPLP")!=-1: purity = "HPLP"
      else:purity = "HPLP+HPHP"
      c1.cd()
      pt =ROOT.TPaveText(0.81,0.82,0.84,0.89,"brNDC")
      pt.SetBorderSize(0)
      pt.SetTextAlign(12)
      pt.SetFillStyle(0)
      pt.SetTextFont(42)
      pt.SetTextSize(0.03)
      pt.AddText(model)
      pt.AddText(purity)

      pt.Draw()
      cmslabel_sim(c1,'2016',11)
      c1.Update()
      
      c1.SaveAs("signalShapes%s_%s.png" %(options.var, inFileName.rsplit(".", 1)[0]))
  
if __name__ == '__main__':
    main()
