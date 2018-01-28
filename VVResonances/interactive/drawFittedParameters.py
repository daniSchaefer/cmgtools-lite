from ROOT import TFile, TCanvas, TPaveText, TLegend, gDirectory, TH1F,gROOT,gStyle, TLatex
import sys
import tdrstyle
tdrstyle.setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *

from time import sleep
# gROOT.SetBatch(True)
# infile = sys.argv[1]
# f = TFile(infile,"READ")

path = ""

def beautify(h1,color,linestyle=1,markerstyle=8):
	h1.SetLineColor(color)
	h1.SetMarkerColor(color)
	# h1.SetFillColor(color)
	h1.SetLineWidth(3)
	h1.SetLineStyle(linestyle)
	h1.SetMarkerStyle(markerstyle)
	
def getLegend(x1=0.80010112,y1=0.123362,x2=0.90202143,y2=0.279833):
  legend = TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend

def getPavetext():
  addInfo = TPaveText(0.3010112,0.2066292,0.4202143,0.3523546,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  return addInfo
    
def getCanvas(w=800,h=600):
	 c1 =TCanvas("c","",w,h)
	 return c1

def doYield():
	FHPLP = TFile("JJ_"+sys.argv[1]+"_HPLP_yield.root","READ")
	FHPHP = TFile("JJ_"+sys.argv[1]+"_HPHP_yield.root","READ")
	
	vars = ["yield"]
	for var in vars:
		c = getCanvas()
		l = getLegend()
		gStyle.SetOptStat(0)
		gStyle.SetOptTitle(0)
		
		
		gHPLP = FHPLP.Get(var)
		gHPHP = FHPHP.Get(var)
		fHPLP = gHPLP.GetFunction("func")
		fHPHP = gHPHP.GetFunction("func")
		
		beautify(gHPLP ,1,1,8)
		beautify(gHPHP ,1,1,4)
		beautify(fHPLP ,414,1,8)
		beautify(fHPHP ,611,1,4)
		
		l.AddEntry(fHPLP,"HPLP","LP")
		l.AddEntry(fHPHP,"HPHP","LP")
		
		gHPLP.GetXaxis().SetTitle("M_{VV} (GeV)")
		gHPLP.GetYaxis().SetTitle(var)
		gHPLP.GetYaxis().SetNdivisions(9,1,0)
		gHPLP.GetYaxis().SetTitleOffset(1.7)
		gHPLP.GetXaxis().SetRangeUser(1000., 5000.)
		gHPLP.GetYaxis().SetRangeUser(0.0, 0.0002)
            
		gHPLP.Draw("APE")
		gHPHP.Draw("samePE")
		# fHPLP.Draw("sameL")
	# 	fHPHP.Draw("sameL")
                model = "G_{bulk} #rightarrow WW"
                if sys.argv[1].find("ZZ")!=-1:
                    model = "G_{bulk} #rightarrow ZZ"
                if sys.argv[1].find("WZ")!=-1:
                    model = "W' #rightarrow WZ"
                if sys.argv[1].find("Zprime")!=-1:
                    model = "Z' #rightarrow WW"
                text = TLatex()
                text.DrawLatex(3500,0.00017,model)
		l.Draw("same")
		cmslabel_sim(c,'2016',11)
		c.Update()
		#sleep(100000)
		c.SaveAs(path+"signalFit/"+sys.argv[1]+"_Yield_"+var+"_fit.png")
		
def doMVVFit():
	# FHPLP = TFile("debug_JJ_"+sys.argv[1]+"_MVV_HPLP.json.root","READ")
# 	FHPHP = TFile("debug_JJ_"+sys.argv[1]+"_MVV_HPHP.json.root","READ")
	FHPLP = TFile("debug_JJ_"+sys.argv[1]+"_MVV.json.root","READ")
	FHPHP = TFile("debug_JJ_"+sys.argv[1]+"_MVV.json.root","READ")
	
	vars = ["MEAN","SIGMA","ALPHA","N","SCALESIGMA","f"]
	for var in vars:
		c = getCanvas()
		l = getLegend()
		gStyle.SetOptStat(0)
		gStyle.SetOptTitle(0)
		
		
		gHPLP = FHPLP.Get(var)
		gHPHP = FHPHP.Get(var)
		fHPLP = FHPLP.Get(var+"_func")
		fHPHP = FHPHP.Get(var+"_func")
		
		beautify(gHPLP ,1,1,8)
		beautify(gHPHP ,1,1,4)
		beautify(fHPLP ,414,1,8)
		beautify(fHPHP ,611,1,4)
		
		# l.AddEntry(fHPLP,"HPLP","L")
		# l.AddEntry(fHPHP,"HPHP","L")
		l.AddEntry(fHPHP,var,"L")
		
		gHPLP.GetXaxis().SetTitle("M_{VV} (GeV)")
		gHPLP.GetYaxis().SetTitle(var)
		gHPLP.GetYaxis().SetNdivisions(9,1,0)
		gHPLP.GetYaxis().SetTitleOffset(1.7)
		gHPLP.GetXaxis().SetRangeUser(1000., 5000.)
		if var.find("ALPHA")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 2.)
		elif var.find("SCALESIGMA")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 4.)
		elif var.find("SIGMA")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 150.)
		elif var.find("MEAN")!=-1: gHPLP.GetYaxis().SetRangeUser(700., 7000)
		elif var.find("N")!=-1: gHPLP.GetYaxis().SetRangeUser(115., 135.)
		elif var.find("f")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 1.)

		gHPLP.Draw("APE")
		gHPHP.Draw("samePE")
		fHPLP.Draw("sameL")
		fHPHP.Draw("sameL")
		l.Draw("same")
		cmslabel_sim(c,'2016',11)
		c.Update()
		c.SaveAs(path+"signalFit/"+sys.argv[1]+"_MVV_combined_"+var+"_fit.png")
		
def doMJFit():
	FHPLP = TFile("debug_JJ_"+sys.argv[1]+"_MJl1_HPLP.json.root","READ")
	FHPHP = TFile("debug_JJ_"+sys.argv[1]+"_MJl1_HPHP.json.root","READ")
	
	vars = ["mean","sigma","alpha","n","f","alpha2","n2","slope"]
	#if sys.argv[1].find("Wprime")!=-1:
            #vars = ["meanW","sigmaW","alphaW","f","alphaW2","meanZ","sigmaZ","alphaZ","alphaZ2"]
	for var in vars:
		print "Plotting variable: " ,var
		c = getCanvas()
		l = getLegend()
		gStyle.SetOptStat(0)
		gStyle.SetOptTitle(0)
		
		
		gHPLP = FHPLP.Get(var)
		gHPHP = FHPHP.Get(var)
		fHPLP = FHPLP.Get(var+"_func")
		fHPHP = FHPHP.Get(var+"_func")
		
		beautify(gHPLP ,1,1,8)
		beautify(gHPHP ,1,1,4)
		beautify(fHPLP ,414,1,8)
		beautify(fHPHP ,611,1,4)
		
		l.AddEntry(fHPHP,"HPHP","LP")
		l.AddEntry(fHPLP,"HPLP","LP")
		
		
		gHPLP.GetXaxis().SetTitle("M_{VV} (GeV)")
		gHPLP.GetYaxis().SetTitle(var)
		gHPLP.GetYaxis().SetNdivisions(9,1,0)
		gHPLP.GetYaxis().SetTitleOffset(1.7)
		gHPLP.GetXaxis().SetRangeUser(1000., 5000.)
		
                
                if var.find("n2")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 5.)
		if var.find("n")!=-1: gHPLP.GetYaxis().SetRangeUser(1., 5.)
		if var.find("alpha2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.1)
		if var.find("alpha")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.5)
		if var.find("alphaZ2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
		if var.find("alphaZ")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
		if var.find("slope")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 1.)
		if var.find("sigma")!=-1: gHPLP.GetYaxis().SetRangeUser(3.,25.)
		if var.find("mean")!=-1: gHPLP.GetYaxis().SetRangeUser(70., 95.)
		if var.find("meanZ")!=-1: gHPLP.GetYaxis().SetRangeUser(80., 95.)
		if var.find("f")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 2.)
		gHPLP.Draw("APE")
		gHPHP.Draw("samePE")
		fHPLP.Draw("sameL")
		fHPHP.Draw("sameL")
		l.Draw("same")
		cmslabel_sim(c,'2016',11)
		c.Update()
		c.SaveAs(path+"signalFit/"+sys.argv[1]+"_MJ_"+var+"_fit.png")
		#sleep(10)
		
def doResolution():
	fLP = TFile("JJ_nonRes_detectorResponse_HPLP.root","READ")
	fHP = TFile("JJ_nonRes_detectorResponse_HPHP.root","READ")
	cols = [611,414]
	hps = []	
	hp_hSx 	=fHP.Get("scalexHisto")
	hp_hSy 	=fHP.Get("scaleyHisto")
	hp_hRx 	=fHP.Get("resxHisto")  
	hp_hRy 	=fHP.Get("resyHisto") 
	hp_hSx.GetYaxis().SetTitle("M_{VV} scale" )
	hp_hSy.GetYaxis().SetTitle("M_{jet} scale" )
	hp_hRx.GetYaxis().SetTitle("M_{VV} resolution" )
	hp_hRy.GetYaxis().SetTitle("M_{jet} resolution" )
	hp_hSx.GetYaxis().SetRangeUser(0.9,1.1)
	hp_hSy.GetYaxis().SetRangeUser(0.9,1.1)
	hp_hRx.GetYaxis().SetRangeUser(0.,0.15)
	hp_hRy.GetYaxis().SetRangeUser(0.,0.15)
	
	 
	# hp_h2D_x =f.Get("dataX")    
	# hp_h2D_y =f.Get("dataY")    
	hps.append(hp_hSx)
	hps.append(hp_hSy)
	hps.append(hp_hRx)
	hps.append(hp_hRy)
	for h in hps: 
		h.SetLineColor(cols[0])
		h.SetLineWidth(3)
		h.GetXaxis().SetTitle("Gen p_{T} (GeV)")
		h.GetXaxis().SetNdivisions(9,1,0)
		h.GetYaxis().SetNdivisions(9,1,0)
		h.GetYaxis().SetTitleOffset(1.4)
	
	
	lps =[]
	lp_hSx 	=fLP.Get("scalexHisto")
	lp_hSy 	=fLP.Get("scaleyHisto")
	lp_hRx 	=fLP.Get("resxHisto")  
	lp_hRy 	=fLP.Get("resyHisto")  
	# lp_h2D_x =fLP.Get("dataX")    
	# lp_h2D_y =fLP.Get("dataY")    
	lps.append(lp_hSx)
	lps.append(lp_hSy)
	lps.append(lp_hRx)
	lps.append(lp_hRy)
	for h in lps: 
		h.SetLineColor(cols[1])
		h.SetLineWidth(3)
		h.GetXaxis().SetTitle("Gen p_{T} (GeV)")
	
	lg = getLegend()
	lg.AddEntry(hp_hSx,"HPHP","L")
	lg.AddEntry(lp_hSx,"HPLP","L")
	
	pt = getPavetext()
	pt.AddText("WP #tau_{21} = 0.35")
	
	
	for hp,lp in zip(hps,lps):
		c = getCanvas()
		hp.GetXaxis().SetRangeUser(200.,2600.)
		hp.Draw("HIST")
		lp.Draw("HISTsame")
		lg.Draw('same')
		pt.Draw("same")
		c.Update()
		c.SaveAs(path+"detectorresolution_"+hp.GetName()+".png")
		
	dataX_lp = fLP.Get('dataY')
	dataX_lp.SetName('dataY_lp')
	plotX_lp = TH1F('plotYlp','mJJ projection',dataX_lp.GetNbinsY(),dataX_lp.GetYaxis().GetXmin(),dataX_lp.GetYaxis().GetXmax())
	
	dataX_hp = fHP.Get('dataY')
	dataX_lp.SetName('dataY_hp')
	plotX_hp = TH1F('plotYhp','mJJ projection',dataX_hp.GetNbinsY(),dataX_hp.GetYaxis().GetXmin(),dataX_hp.GetYaxis().GetXmax())

	for bx in range(dataX_hp.GetNbinsX()):
	 for by in range(dataX_hp.GetNbinsY()):
	  plotX_hp.Fill(dataX_hp.GetYaxis().GetBinCenter(by),dataX_hp.GetBinContent(bx,by))
	  plotX_lp.Fill(dataX_lp.GetYaxis().GetBinCenter(by),dataX_lp.GetBinContent(bx,by))
  
  	plotX_hp.SetLineColor(cols[0]) 
	plotX_lp.SetLineColor(cols[1])  
	plotX_hp.SetLineWidth(3)
	plotX_lp.SetLineWidth(3) 
	c = getCanvas()
	
	plotX_hp.GetXaxis().SetTitle("M_{jet}^{reco}/M_{jet}^{gen}")
	plotX_hp.GetYaxis().SetTitle("A.U")
	plotX_hp.GetXaxis().SetNdivisions(9,1,0)
	plotX_hp.GetYaxis().SetNdivisions(9,1,0)
	plotX_hp.GetYaxis().SetTitleOffset(1.4)
	plotX_hp.DrawNormalized('HIST')
	plotX_lp.DrawNormalized('HISTSAME')
	lg.Draw("same")
	c.SaveAs(path+"detectorresolution_mvv.png")
	
	dataX_lp = fLP.Get('dataX')
	dataX_lp.SetName('dataY_lp')
	plotX_lp = TH1F('plotYlp','mJJ projection',dataX_lp.GetNbinsY(),dataX_lp.GetYaxis().GetXmin(),dataX_lp.GetYaxis().GetXmax())
	
	dataX_hp = fHP.Get('dataX')
	dataX_lp.SetName('dataY_hp')
	plotX_hp = TH1F('plotYhp','mJJ projection',dataX_hp.GetNbinsY(),dataX_hp.GetYaxis().GetXmin(),dataX_hp.GetYaxis().GetXmax())

	for bx in range(dataX_hp.GetNbinsX()):
	 for by in range(dataX_hp.GetNbinsY()):
	  plotX_hp.Fill(dataX_hp.GetYaxis().GetBinCenter(by),dataX_hp.GetBinContent(bx,by))
	  plotX_lp.Fill(dataX_lp.GetYaxis().GetBinCenter(by),dataX_lp.GetBinContent(bx,by))
  
  	plotX_hp.SetLineColor(cols[0]) 
	plotX_lp.SetLineColor(cols[1])  
	plotX_hp.SetLineWidth(3)
	plotX_lp.SetLineWidth(3) 
	c = getCanvas()
	
	plotX_hp.GetXaxis().SetTitle("M_{jj}^{reco}/M_{jj}^{gen}")
	plotX_hp.GetYaxis().SetTitle("A.U")
	plotX_hp.GetXaxis().SetNdivisions(9,1,0)
	plotX_hp.GetYaxis().SetNdivisions(9,1,0)
	plotX_hp.GetYaxis().SetTitleOffset(1.4)
	plotX_hp.DrawNormalized('HIST')
	plotX_lp.DrawNormalized('HISTSAME')
	lg.Draw("same")
	c.SaveAs(path+"detectorresolution_mj.png")
	
	fLP.Close()
	fHP.Close()	

def doKernelMVV():
	files = []
	fLP = TFile("JJ_nonRes_MVV_HPLP.root","READ")
	fHP = TFile("JJ_nonRes_MVV_HPHP.root","READ")
	files.append(fLP)
	files.append(fHP)
	cols = [611,414]
	c = getCanvas()
	c.SetLogy()
	l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
	hists = []
	for i,f in enumerate(files):
		hsts = []
	
		fromKernel = f.Get("histo_nominal")
		fromSim    = f.Get("mvv_nominal")

		beautify(fromKernel,cols[i])
		beautify(fromSim   ,cols[i])
		l.AddEntry(fromKernel,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
		l.AddEntry(fromSim   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
		
		hsts.append(fromSim)
		hsts.append(fromKernel)
		hists.append(hsts)
	hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
	hists[0][0].GetYaxis().SetTitle("A.U")
	hists[0][0].GetYaxis().SetNdivisions(9,1,0)
	hists[0][0].GetYaxis().SetTitleOffset(1.5)	
	hists[0][0].GetXaxis().SetRangeUser(1000.   , 5200)
	hists[0][0].DrawNormalized("histPE")
	for h in hists:
		h[0].DrawNormalized("samehistPE")
		h[1].DrawNormalized("sameLhist")
		
	l.Draw("same")
	c.SaveAs(path+"1Dkernel.png")

def compKernelMVV():
	purities=['HPHP','HPLP']
	
	
	for p in purities:
		hists = []
		files = []
		fNominal = TFile("JJ_nonRes_MVV_"+p+".root","READ")
		fCombined = TFile("JJ_nonRes_MVV_"+p+"_NP.root","READ")
		files.append(fNominal)
		files.append(fCombined)
		
		
		hists = []
		l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
		cols = [608,614]
		for i,f in enumerate(files):
			hsts = []
	
			fromKernel = f.Get("histo_nominal")
			fromSim    = f.Get("mvv_nominal")

			beautify(fromKernel,cols[i])
			beautify(fromSim   ,cols[i])
			if i == 1:
				l.AddEntry(fromKernel,"Combined, Kernel    ","L")
				l.AddEntry(fromSim   ,"Combined, Simulation","PE")
			elif i == 0:
				l.AddEntry(fromKernel,"%s res., Kernel    "%p,"L")
				l.AddEntry(fromSim   ,"%s res., Simulation"%p,"PE")
					
			hsts.append(fromSim)
			hsts.append(fromKernel)
			hists.append(hsts)
		c = getCanvas()
		c.SetLogy()
		
		hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
		hists[0][0].GetYaxis().SetTitle("A.U")
		hists[0][0].GetYaxis().SetNdivisions(9,1,0)
		hists[0][0].GetYaxis().SetTitleOffset(1.5)	
		hists[0][0].GetXaxis().SetRangeUser(1000.   , 4900)
		hists[0][0].Draw("histPE")
		for h in hists:
			h[0].Draw("samehistPE")
			h[1].Draw("sameLhist")
		
		l.Draw("same")
		sleep(100)
		c.SaveAs(path+"compare_1Dkernel"+p+".png")

def doKernel2D():
	files = []
	fLP = TFile("JJ_nonRes_COND2D_HPLP_l1.root","READ")
	fHP = TFile("JJ_nonRes_COND2D_HPHP_l1.root","READ")
	files.append(fLP)
	files.append(fHP)
	cols = [611,414]
	c = getCanvas()
	c.SetLogy()
	l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
	hists = []
	for i,f in enumerate(files):
		hsts = []
	
		fromKernel  = f.Get("histo_nominal")
		fromSim     = f.Get("mjet_mvv_nominal")
		fromKernelY = fromKernel.ProjectionX()
		fromSimY 	= fromSim.ProjectionX()
		fromKernelY .SetName("kernel"+f.GetName().replace(".root","").split("_")[3])
		fromSimY 	.SetName("sim"+f.GetName().replace(".root","").split("_")[3])

		beautify(fromKernelY,cols[i])
		beautify(fromSimY   ,cols[i])
		l.AddEntry(fromKernelY,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
		l.AddEntry(fromSimY   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
		
		hsts.append(fromSimY)
		hsts.append(fromKernelY)
		hists.append(hsts)
	hists[0][0].GetXaxis().SetTitle("M_{jet} (GeV)")
	hists[0][0].GetYaxis().SetTitle("A.U")
	hists[0][0].GetYaxis().SetNdivisions(9,1,0)
	hists[0][0].GetYaxis().SetTitleOffset(1.5)	
	# hists[0][0].GetXaxis().SetRangeUser(1000.   , 5200)
	hists[0][0].DrawNormalized("histPE")
	for h in hists:
		h[0].DrawNormalized("samehistPE")
		h[1].DrawNormalized("sameLhist")
	
	l.Draw("same")
	c.SaveAs(path+"2Dkernel_Mjet.png")		
	
	c = getCanvas()
	c.SetLogy()
	l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
	hists = []
	for i,f in enumerate(files):
		hsts = []
	
		fromKernel  = f.Get("histo_nominal")
		fromSim     = f.Get("mjet_mvv_nominal")
		fromKernelY = fromKernel.ProjectionY()
		fromSimY 	= fromSim.ProjectionY()
		fromKernelY .SetName("kernel"+f.GetName().replace(".root","").split("_")[3])
		fromSimY 	.SetName("sim"+f.GetName().replace(".root","").split("_")[3])

		beautify(fromKernelY,cols[i])
		beautify(fromSimY   ,cols[i])
		l.AddEntry(fromKernelY,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
		l.AddEntry(fromSimY   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
		
		hsts.append(fromSimY)
		hsts.append(fromKernelY)
		hists.append(hsts)
	hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
	hists[0][0].GetYaxis().SetTitle("A.U")
	hists[0][0].GetYaxis().SetNdivisions(9,1,0)
	hists[0][0].GetYaxis().SetTitleOffset(1.5)	
	# hists[0][0].GetXaxis().SetRangeUser(1000.   , 5200)
	hists[0][0].DrawNormalized("histPE")
	for h in hists:
		h[0].DrawNormalized("samehistPE")
		h[1].DrawNormalized("sameLhist")
	
	l.Draw("same")
	c.SaveAs(path+"2Dkernel_Mjj.png")

def compSignalMVV():
	
	masses = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
	
	
	files = []
	fHP  = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV_HPHP.root","READ")
	fLP = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV_HPLP.root","READ")
	files.append(fHP)
	files.append(fLP)
	
	
	histsHP = []
	histsLP = []
	l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
	cols = [611,414]
	for m in masses:
		hHP = fHP.Get("%i"%m)
		hLP = fLP.Get("%i"%m)
		hHP.SetName(hHP.GetName()+"HP")
		hLP.SetName(hLP.GetName()+"LP")
		hHP.SetLineColor(cols[0])
		hLP.SetLineColor(cols[1])
		hHP.SetFillColor(0)
		hLP.SetFillColor(0)
		hHP.Rebin(10)
		hLP.Rebin(10)
		if m == masses[0]:
			l.AddEntry(hHP   ,"HPHP","L")
			l.AddEntry(hLP   ,"HPLP","L")
				
		histsHP.append(hHP)
		histsLP.append(hLP)
		
	c = getCanvas()
	
	histsHP[0].GetXaxis().SetTitle("M_{jj} (GeV)")
	
	histsHP[0].GetYaxis().SetTitle("A.U")
	histsHP[0].GetYaxis().SetNdivisions(9,1,0)
	histsHP[0].GetYaxis().SetTitleOffset(1.5)
	histsHP[0].GetXaxis().SetRangeUser(1000,5200)
	histsHP[0].DrawNormalized("hist")
	for hp,lp in zip(histsHP,histsLP):
		hp.DrawNormalized("hist same")
		lp.DrawNormalized("hist same")
	
	l.Draw("same")
	c.SaveAs(path+"comparePurities_MVV.png")
	
	
	
	# histsHP[0].GetXaxis().SetRangeUser(1000,5200)
	c = getCanvas(1600,600)
	c.Divide(2,5)
	legs = []
	for i,(m,hp,lp) in enumerate(zip(masses,histsHP,histsLP)):
		hp.Scale(1./hp.Integral())
		lp.Scale(1./lp.Integral())
		hp.Divide(lp)
		hp.SetMarkerColor(1)
		hp.GetXaxis().SetRangeUser(m*0.80,m*1.2)
		hp.GetYaxis().SetRangeUser(0,2)
		hp.GetYaxis().SetNdivisions(3,0,0)
		hp.GetXaxis().SetTitle("M = %i GeV"%m)
		hp.GetYaxis().SetTitle("HP/LP")
		hp.GetYaxis().SetTitleSize(0.7)
		hp.GetYaxis().SetLabelSize(0.16)
		 
		hp.GetXaxis().SetTitleSize(0.7)
		c.cd(i+1)
		hp.Draw("M")
		l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
		l.SetName("l%i"%m)
		l.SetTextSize(0.2)
		l.AddEntry(hp   ,"%i"%m,"LEP")
		l.Draw("same")
		legs.append(l)
	c.SaveAs(path+"comparePurities_MVVratio.png")
		
if __name__ == '__main__':
	doMJFit()
	#doMVVFit()
	#doYield()
	# doResolution()
	# doKernelMVV()
	# compKernelMVV()
	# doKernel2D()
	# compSignalMVV()
