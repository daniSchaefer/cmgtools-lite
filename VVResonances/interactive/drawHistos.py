from ROOT import TFile, TCanvas, TPaveText, TLegend, gDirectory, TH1F,gROOT,gStyle
import sys
import tdrstyle
tdrstyle.setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *

from time import sleep
# gROOT.SetBatch(True)
infile = sys.argv[1]	 


f = TFile(infile,"READ")



def beautify(h1,color,style=1):
	h1.SetLineColor(color)
	h1.SetMarkerColor(color)
	# h1.SetFillColor(color)
	h1.SetLineWidth(3)
	h1.SetLineStyle(style)
	h1.SetMarkerStyle(style)
	
def getLegend():
  legend = TLegend(0.55010112,0.7183362,0.70202143,0.919833)
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
    
def getCanvas():
	 c1 =TCanvas("c","",800,800)
	 return c1

def doMVVFit():
	FqW = TFile("qW_signalfit/debug_JJ_XqW_MVV.json.root","READ")
	FqZ = TFile("qZ_signalfit/debug_JJ_XqZ_MVV.json.root","READ")
	
	vars = ["MEAN","SIGMA","ALPHA","N","SCALESIGMA","f"]
	for var in vars:
		c = getCanvas()
		l = getLegend()
		gStyle.SetOptStat(0)
		gStyle.SetOptTitle(0)
		
		
		gqW = FqW.Get(var)
		gqZ = FqZ.Get(var)
		fqW = FqW.Get(var+"_func")
		fqZ = FqZ.Get(var+"_func")
		
		beautify(gqW ,922)
		beautify(gqZ ,418)
		beautify(fqW ,922)
		beautify(fqZ ,418)
		
		l.AddEntry(fqW,"qW","L")
		l.AddEntry(fqZ,"qZ","L")
		
		gqW.GetXaxis().SetTitle("M_{VV} (GeV)")
		gqW.GetYaxis().SetTitle(var)
		gqW.GetYaxis().SetNdivisions(9,1,0)
		gqW.GetYaxis().SetTitleOffset(1.7)
		gqW.GetXaxis().SetRangeUser(1000., 6000.)
		if var.find("ALPHA")!=-1: gqW.GetYaxis().SetRangeUser(0., 2.)
		elif var.find("SCALESIGMA")!=-1: gqW.GetYaxis().SetRangeUser(0., 4.)
		elif var.find("SIGMA")!=-1: gqW.GetYaxis().SetRangeUser(0., 370.)
		elif var.find("MEAN")!=-1: gqW.GetYaxis().SetRangeUser(700., 7000)
		elif var.find("N")!=-1: gqW.GetYaxis().SetRangeUser(115., 135.)
		elif var.find("f")!=-1: gqW.GetYaxis().SetRangeUser(0., 1.)

		gqW.Draw("AP")
		gqZ.Draw("sameP")
		fqW.Draw("sameL")
		fqZ.Draw("sameL")
		l.Draw("same")
		cmslabel_sim(c,'2016',11)
		c.Update()
		c.SaveAs("/eos/user/t/thaarres/www/vvana/SignalShapesMVV/"+var+"_fit.png")
		


def doResolution():
	fLP = TFile("JJ_nonRes_detectorResponse_LP.root","READ")
	fHP = TFile("JJ_nonRes_detectorResponse_HP.root","READ")
	cols = [922,418]
	hps = []	
	hp_hSx 	=fHP.Get("scalexHisto")
	hp_hSy 	=fHP.Get("scaleyHisto")
	hp_hRx 	=fHP.Get("resxHisto")  
	hp_hRy 	=fHP.Get("resyHisto") 
	hp_hSx.GetYaxis().SetTitle("M_{qV} scale" )
	hp_hSy.GetYaxis().SetTitle("M_{V} scale" )
	hp_hRx.GetYaxis().SetTitle("M_{qV}resolution" )
	hp_hRy.GetYaxis().SetTitle("M_{V} resolution" )
	hp_hSx.GetYaxis().SetRangeUser(0.9,1.3)
	hp_hSy.GetYaxis().SetRangeUser(0.9,1.3)
	hp_hRx.GetYaxis().SetRangeUser(0.,0.2)
	hp_hRy.GetYaxis().SetRangeUser(0.,0.2)
	
	 
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
		h.GetXaxis().SetTitle("Gen p_{T} (GeV)")
		h.GetXaxis().SetNdivisions(9,1,0)
		h.GetYaxis().SetNdivisions(9,1,0)
		h.GetYaxis().SetTitleOffset(1.4)
		# h.GetXaxis().SetRangeUser(200.,5200.)
	
	
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
	
	lg = getLegend()
	lg.AddEntry(hp_hSx,"HP","L")
	lg.AddEntry(lp_hSx,"LP","L")
	
	pt = getPavetext()
	pt.AddText("WP #tau_{21} = 0.60")
	
	
	for hp,lp in zip(hps,lps):
		c = getCanvas()
		hp.Draw("HIST")
		lp.Draw("HISTsame")
		lg.Draw('same')
		pt.Draw("same")
		c.SaveAs("/eos/user/t/thaarres/www/vvana/DetectorResolution/"+hp.GetName()+".png")
	fLP.Close()
	fHP.Close()	

def doScale(f):
	 f.cd()
	 dirList = gDirectory.GetListOfKeys()
	 c = getCanvas()
	 l = getLegend()
	 c.cd()
	 colors= [418,434,802,618,1,7,8,9,40,41,42,43]
	 i = -1
	 for k1 in (dirList):
	 	
	 	i +=1
	 	h1 = k1.ReadObj()
		# if not (h1.GetName().find("altshape2")	!=-1 or h1.GetName().find("mjet") 			!=-1): continue
	 	if   h1.GetName().find("altshape1")	!=-1: h1.SetLineColor(colors[0])
		elif h1.GetName().find("altshape2up")	!=-1: h1.SetLineColor(colors[1])
	 	elif h1.GetName().find("altshape2down")	!=-1: h1.SetLineColor(colors[2])
	 	elif h1.GetName().find("histo")			!=-1: h1.SetLineColor(colors[3])
	 	elif h1.GetName().find("mjet") 			!=-1: h1.SetLineColor(1)
	 	h1.SetLineWidth(2)
		h1.Rebin(2)
	 	h1.Scale(1./h1.Integral())
	 	h1.GetYaxis().SetRangeUser(0., h1.GetMaximum()*1.5)
	 	h1.GetXaxis().SetRangeUser(30., 260)
	 	h1.GetXaxis().SetTitle("Mass (GeV)")
	 	h1.GetYaxis().SetTitle("A.U")
		h1.GetYaxis().SetNdivisions(9,1,0)
		h1.GetYaxis().SetTitleOffset(1.4)
		
		if h1.GetName().find("mjet") 			!=-1: 	h1.Draw("sameM")
	 	else: h1.Draw("samehist")
	 	if   h1.GetName().find("altshape1")!=-1: l.AddEntry(h1,"MadGraph+Pythia8","L")
	 	elif h1.GetName().find("altshape2up")  !=-1: l.AddEntry(h1,"Herwig++ up","L")
		elif h1.GetName().find("altshape2down")!=-1: l.AddEntry(h1,"Herwig++ down","L")
		elif h1.GetName().find("histo")    !=-1: l.AddEntry(h1,"Pythia8 (nominal)","L")
		elif h1.GetName().find("mjet")     !=-1: l.AddEntry(h1,"Simulation (Pythia8)","LEP")
	 	 	
	 l.Draw("same")
	 postfix="HP"
	 if infile.find("LP")!=-1: postfix = "LP"
	 c.SaveAs("/eos/user/t/thaarres/www/vvana/kernel/debug_JJ_nonRes_MJJ_"+postfix+"_withMirroringALL.png")
	 sleep(100)

def doKernel(f):
	c = getCanvas()
	l = getLegend()
	fromKernel = f.Get("histo")
	fromSim    = f.Get("mjet")
	# fLP = TFile("JJ_nonRes_MJJ_LP.root","READ")
	# fromKernelLP = fLP.Get("histo")
	# fromSimLP    = fLP.Get("mjet")
	# fromKernel.Add(fromKernelLP )
	# fromSim   .Add(fromSimLP    )
	fromKernel.Scale(1./fromKernel.Integral())
	fromSim   .Scale(1./fromSim   .Integral())
	beautify(fromKernel,922)
	beautify(fromSim   ,418)
	l.AddEntry(fromKernel,"From Kernel    ","L")
	# l.AddEntry(0,"Mean = %.1f  RMS = %.1f " %(fromKernel.GetMean(),fromKernel.GetRMS()),"")
	l.AddEntry(fromSim   ,"From Simulation","L")
	# l.AddEntry(0,"Mean = %.1f  RMS = %.1f " %(fromSim.GetMean(),fromSim.GetRMS()),"")
	fromSim   .Draw("histL")
	fromKernel.Draw("sameLhist")
	fromKernel.GetXaxis().SetRangeUser(30., 300)
	fromSim.GetXaxis().SetRangeUser(30.   , 300)
	fromSim.GetYaxis().SetRangeUser(0., fromKernel.GetMaximum()*1.1)
	fromSim.GetXaxis().SetTitle("Mass (GeV)")
	fromSim.GetYaxis().SetTitle("A.U")
	fromSim.GetYaxis().SetNdivisions(9,1,0)
	fromSim.GetYaxis().SetTitleOffset(1.5)
	
	l.Draw("same")
	postfix="HP"
	if infile.find("LP")!=-1: postfix = "LP"
	pt = getPavetext()
	pt.AddText(postfix+"-only det. resp.")
	# pt.AddText("HP+LP")
	pt.Draw("same")
	# c.SaveAs("/eos/user/t/thaarres/www/vvana/DetectorResolution/"+postfix+"CORR_kernelVSsim_"+postfix+".png")
	# c.SaveAs("/eos/user/t/thaarres/www/vvana/DetectorResolution/CORR_kernelVSsim_HPandLP.png")

def do2DKernel(f):
	colors= [1,418,434,802,618,1,7,8,9,40,41,42,43]
	
	fromKernel 			= f.Get("histo")
	fromKernelalt1 		= f.Get("histo_altshape1")
	fromKernelalt2up 	= f.Get("histo_altshape2up")
	fromKernelalt2down 	= f.Get("histo_altshape2down")
	fromSim    			= f.Get("mjet_mvv")
	
	 #X==JetMass Y==MVV


	histsAllY = []
	hAllYfromKernel 		= fromKernel    .ProjectionY()
	hAllYfromKernelalt1 	= fromKernelalt1.ProjectionY()
	hAllYfromKernelalt2up 	= fromKernelalt2up.ProjectionY()
	hAllYfromKernelalt2down	= fromKernelalt2down.ProjectionY()
	hAllYfromSim 		    = fromSim       .ProjectionY()
	histsAllY.append(hAllYfromSim 	)
	histsAllY.append(hAllYfromKernel 	)
	histsAllY.append(hAllYfromKernelalt1 )
	histsAllY.append(hAllYfromKernelalt2up )
	histsAllY.append(hAllYfromKernelalt2down )
	c = getCanvas()
	for col,h in enumerate (histsAllY):
		beautify(h,colors[col])
		h.Rebin(2)
		# h.GetXaxis().SetRangeUser(0.,610.)
		h.GetXaxis().SetTitle("Mass (GeV)")
		h.GetYaxis().SetTitle("A.U")
		if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
		else: h.DrawNormalized("HISTsame")
	l = getLegend()
	l.AddEntry(hAllYfromSim       		,"MC events (Pythia8)","LEP")
	l.AddEntry(hAllYfromKernel    		,"Nominal (Pythia8)","L")
	l.AddEntry(hAllYfromKernelalt1		,"Madgraph+Pythia8" ,"L")
	l.AddEntry(hAllYfromKernelalt2up	,"Herwig++ up"		 ,"L")
	l.AddEntry(hAllYfromKernelalt2down	,"Herwig++ down"		 ,"L")
	l.Draw("same")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/projY_mass_allmvvbins.png")

	histsAllX = []
	hAllXfromKernel 		= fromKernel    .ProjectionX()
	hAllXfromKernelalt1 	= fromKernelalt1.ProjectionX()
	hAllXfromKernelalt2up 	= fromKernelalt2up	.ProjectionX()
	hAllXfromKernelalt2down	= fromKernelalt2down.ProjectionX()
	hAllXfromSim 		    = fromSim       	.ProjectionX()
	histsAllX.append(hAllXfromSim 	)
	histsAllX.append(hAllXfromKernel 	)
	histsAllX.append(hAllXfromKernelalt1 )
	histsAllX.append(hAllXfromKernelalt2up )
	histsAllX.append(hAllXfromKernelalt2down )
	c = getCanvas()
	l = getLegend()
	l.AddEntry(hAllXfromSim       ,"MC events (Pythia8)","LEP")
	l.AddEntry(hAllXfromKernel    ,"Nominal (Pythia8)","L")
	l.AddEntry(hAllXfromKernelalt1,"Madgraph+Pythia8" ,"L")
	l.AddEntry(hAllXfromKernelalt2up,"Herwig++ up"		 ,"L")
	l.AddEntry(hAllXfromKernelalt2down,"Herwig++ down"		 ,"L")

	for col,h in enumerate (histsAllX):
		beautify(h,colors[col])
		# h.GetXaxis().SetRangeUser(1000.,7000.)
		h.GetXaxis().SetTitle("M_{jj} (GeV)")
		h.GetYaxis().SetTitle("A.U")
		if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
		else: h.DrawNormalized("HISTsame")
	l.Draw("same")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/projX_mvv_allmassbins.png")

	for bin in range(1,fromKernel.GetNbinsX()):
		hists = []
		hfromKernel 		= fromKernel.ProjectionY("bin%i"%bin,bin,bin)
		hfromKernelalt1 	= fromKernelalt1.ProjectionY("alt1_bin%i"%bin,bin,bin)
		hfromKernelalt2up 	= fromKernelalt2up.ProjectionY("alt2up_bin%i"%bin,bin,bin)
		hfromKernelalt2down = fromKernelalt2down.ProjectionY("alt2down_bin%i"%bin,bin,bin)
		hfromSim 			= fromSim.ProjectionY("sim_bin%i"%bin,bin,bin)
		hists.append(hfromSim 	)
		hists.append(hfromKernel 	)
		hists.append(hfromKernelalt1 )
		hists.append(hfromKernelalt2up )
		hists.append(hfromKernelalt2down )
		c = getCanvas()
		l = getLegend()
		l.AddEntry(hfromSim       ,"MC events (Pythia8)","LEP")
		l.AddEntry(hfromKernel    ,"Nominal (Pythia8)","L")
		l.AddEntry(hfromKernelalt1,"Madgraph+Pythia8" ,"L")
		l.AddEntry(hfromKernelalt2up,"Herwig++ up"		 ,"L")
		l.AddEntry(hfromKernelalt2down,"Herwig++ down"		 ,"L")

		for col,h in enumerate (hists):
			beautify(h,colors[col])
			# h.GetXaxis().SetRangeUser(0.,610.)
			h.GetXaxis().SetTitle("Mass (GeV)")
			h.GetYaxis().SetTitle("A.U")
			if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
			else: h.DrawNormalized("HISTsame")
		l.Draw("same")
		c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/projY_perBin/projY_mass_mvvbin%i.png"%bin)

	for bin in range(2,fromKernel.GetNbinsY()):
		hists = []
		hfromKernel 		= fromKernel.ProjectionX("bin%i"%bin,bin,bin)
		hfromKernelalt1 	= fromKernelalt1.ProjectionX("alt1_bin%i"%bin,bin,bin)
		hfromKernelalt2up 	= fromKernelalt2up.ProjectionX("alt2up_bin%i"%bin,bin,bin)
		hfromKernelalt2down = fromKernelalt2down.ProjectionX("alt2down_bin%i"%bin,bin,bin)
		hfromSim 		= fromSim.ProjectionX("sim_bin%i"%bin,bin,bin)
		hists.append(hfromSim 	)
		hists.append(hfromKernel 	)
		hists.append(hfromKernelalt1 )
		hists.append(hfromKernelalt2up )
		hists.append(hfromKernelalt2down )
		c = getCanvas()
		l = getLegend()
		l.AddEntry(hfromSim       ,"MC events (Pythia8)","LEP")
		l.AddEntry(hfromKernel    ,"Nominal (Pythia8)","L")
		l.AddEntry(hfromKernelalt1,"Madgraph+Pythia8" ,"L")
		l.AddEntry(hfromKernelalt2up,"Herwig++ up"		 ,"L")
		l.AddEntry(hfromKernelalt2down,"Herwig++ down"		 ,"L")
		for col,h in enumerate (hists):
			beautify(h,colors[col])
			# h.GetXaxis().SetRangeUser(1000.,7000.)
			h.GetXaxis().SetTitle("M_{jj}(GeV)")
			h.GetYaxis().SetTitle("A.U")
			if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
			else: h.DrawNormalized("HISTsame")
		l.Draw("same")
		c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/projX_perBin/projX_mvv_massbin%i.png"%bin)


def compare2DKernel(f):
	colors= [1,418,434,802,618,1,7,8,9,40,41,42,43]
	
	fromKernel 			= f.Get("histo")
	fromSim    			= f.Get("mjet_mvv")
	
	c = getCanvas()
	c.cd()
	fromKernel.Draw("COLZ")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/mjetReso/NoAccGen_fromKernel.png")
	c = getCanvas()
	c.cd()
	fromSim.Draw("COLZ")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/mjetReso/NoAccGen_fromSim.png")
	 #X==JetMass Y==MVV


	histsAllY = []
	hAllYfromKernel 		= fromKernel    .ProjectionY()
	hAllYfromSim 		    = fromSim       .ProjectionY()
	histsAllY.append(hAllYfromSim 	)
	histsAllY.append(hAllYfromKernel 	)

	c = getCanvas()
	for col,h in enumerate (histsAllY):
		beautify(h,colors[col])
		h.Rebin(2)
		# h.GetXaxis().SetRangeUser(0.,610.)
		h.GetXaxis().SetTitle("Mass (GeV)")
		h.GetYaxis().SetTitle("A.U")
		if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
		else: h.DrawNormalized("HISTsame")
	l = getLegend()
	l.AddEntry(hAllYfromSim       		,"MC events (Pythia8)","LEP")
	l.AddEntry(hAllYfromKernel    		,"Nominal (Pythia8)","L")

	l.Draw("same")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/mjetReso/NoAccGen_projY_mass_allmvvbins.png")

	histsAllX = []
	hAllXfromKernel 		= fromKernel    .ProjectionX()
	hAllXfromSim 		    = fromSim       .ProjectionX()
	histsAllX.append(hAllXfromSim 	)
	histsAllX.append(hAllXfromKernel 	)

	c = getCanvas()
	l = getLegend()
	l.AddEntry(hAllXfromSim       ,"MC events (Pythia8)","LEP")
	l.AddEntry(hAllXfromKernel    ,"Nominal (Pythia8)","L")
	

	for col,h in enumerate (histsAllX):
		beautify(h,colors[col])
		# h.GetXaxis().SetRangeUser(1000.,7000.)
		h.GetXaxis().SetTitle("M_{jj} (GeV)")
		h.GetYaxis().SetTitle("A.U")
		if h.GetName().find("sim")!=-1: h.DrawNormalized("Esame")
		else: h.DrawNormalized("HISTsame")
	l.Draw("same")
	c.SaveAs("/eos/user/t/thaarres/www/vvana/2Dkernel/mjetReso/NoAccGen_projX_mvv_allmassbins.png")



# doResolution()
# doKernel(f)
# doScale(f)
# do2DKernel(f)
# compare2DKernel(f)
doMVVFit()
f  .Close()

