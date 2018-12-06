
import ROOT
from CMGTools.VVResonances.plotting.RooPlotter import *
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *
import os
from array import array
from time import sleep
import optparse

ROOT.gROOT.SetBatch(False)

H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref

directory='/eos/user/t/thaarres/www/vvana/control_plots'
lumi_13TeV = "41.4 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=0
iPosX = 11
cuts={}
lumi='41367'

cuts['commonTOT'] = '(njj>0&&jj_LV_mass>1126&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>55.&&jj_l1_softDrop_mass<215.&&jj_l2_softDrop_mass>55.&&jj_l2_softDrop_mass<215.)'
cuts['common'] = '(njj>0&&jj_LV_mass>1126&&abs(jj_l1_eta-jj_l2_eta)<1.3)'

def getCanvas(title):
	T = 0.08*H_ref
	B = 0.12*H_ref 
	L = 0.12*W_ref
	R = 0.04*W_ref
	canvas = ROOT.TCanvas(title,title,50,50,W,H)
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
	canvas.Update()
	ROOT.gStyle.SetOptStat(0)
	ROOT.gStyle.SetOptTitle(0)
	ROOT.gStyle.SetOptFit(0)
	
	legend = ROOT.TLegend(0.42,0.65,0.92,0.9,"","brNDC")
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)
	
	return canvas, legend
	
def getPlotters(samples,isData=False,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    for filename in os.listdir('samples_jer'):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter('samples_jer/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile('samples_jer/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor(corr,'flat')
                    
    return  plotters

def doDDT(p1,cut,outname):
	cut1 ='*'.join([cut,'(jj_l1_pt>300&&jj_l1_pt<400)'])
	cut2 ='*'.join([cut,'(jj_l1_pt>500&&jj_l1_pt<600)'])
	cut3 ='*'.join([cut,'(jj_l1_pt>1000&&jj_l1_pt<1100)'])
	hTOT1=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut ,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h11  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut1,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h12  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut2,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h13  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut3,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	
	hTOT2=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut ,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")                                                                                                                                            
	h21  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut1,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	h22  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut2,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	h23  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut3,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
  
	tuned_hTOT1=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut ,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	tuned_h11  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut1,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	tuned_h12  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut2,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	tuned_h13  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut3,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	tuned_hTOT2=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut ,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")                                                                                                                                            
	tuned_h21  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut1,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	tuned_h22  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut2,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	tuned_h23  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut3,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
  
	gencut1 ='*'.join([cut,'(jj_l1_gen_pt>300&& jj_l1_gen_pt<400)'])
	gencut2 ='*'.join([cut,'(jj_l1_gen_pt>400&& jj_l1_gen_pt<600)'])
	gencut3 ='*'.join([cut,'(jj_l1_gen_pt>1000&&jj_l1_gen_pt<1100)'])
	tuned_genhTOT1=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/jj_l1_gen_pt))",cut    ,"1", 80,   -1. ,8. , 60, 0., 1.5,"Gen #rho'",'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genh11  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/jj_l1_gen_pt))",gencut1,"1", 80,   -1. ,8. , 60, 0., 1.5,"Gen #rho'",'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genh12  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/jj_l1_gen_pt))",gencut2,"1", 80,   -1. ,8. , 60, 0., 1.5,"Gen #rho'",'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genh13  =p1.drawTH2("(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/jj_l1_gen_pt))",gencut3,"1", 80,   -1. ,8. , 60, 0., 1.5,"Gen #rho'",'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genhTOT2=p1.drawTH2("(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/(jj_l1_gen_pt*jj_l1_pt)))"  ,cut    ,"1", 100, -10. ,0. , 60, 0., 1.5,"Gen #rho" ,'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")                                                                                                                                            
	tuned_genh21  =p1.drawTH2("(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/(jj_l1_gen_pt*jj_l1_pt)))"  ,gencut1,"1", 100, -10. ,0. , 60, 0., 1.5,"Gen #rho" ,'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genh22  =p1.drawTH2("(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/(jj_l1_gen_pt*jj_l1_pt)))"  ,gencut2,"1", 100, -10. ,0. , 60, 0., 1.5,"Gen #rho" ,'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
	tuned_genh23  =p1.drawTH2("(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_pt))):(TMath::Log(jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass/(jj_l1_gen_pt*jj_l1_pt)))"  ,gencut3,"1", 100, -10. ,0. , 60, 0., 1.5,"Gen #rho" ,'' ,"Gen #tau_{21}^{DDT}",'',"COLZ")
  
	
	f = ROOT.TFile(outname,"RECREATE")
	h11.Write("rhoHat_b1")
	h12.Write("rhoHat_b2")
	h13.Write("rhoHat_b3")
	h21.Write("rho_b1")
	h22.Write("rho_b2")
	h23.Write("rho_b3")
	hTOT1.Write('tot_rhoHat')
	hTOT2.Write('tot_rho')
	tuned_h11.Write("tuned_rhoHat_b1")
	tuned_h12.Write("tuned_rhoHat_b2")
	tuned_h13.Write("tuned_rhoHat_b3")
	tuned_h21.Write("tuned_rho_b1")
	tuned_h22.Write("tuned_rho_b2")
	tuned_h23.Write("tuned_rho_b3")
	tuned_hTOT1.Write('tuned_tot_rhoHat')
	tuned_hTOT2.Write('tuned_tot_rho')
	tuned_genh11.Write("tuned_genrhoHat_b1")
	tuned_genh12.Write("tuned_genrhoHat_b2")
	tuned_genh13.Write("tuned_genrhoHat_b3")
	tuned_genh21.Write("tuned_genrho_b1")
	tuned_genh22.Write("tuned_genrho_b2")
	tuned_genh23.Write("tuned_genrho_b3")
	tuned_genhTOT1.Write('tuned_gentot_rhoHat')
	tuned_genhTOT2.Write('tuned_gentot_rho')
	f.Write()
	f.Close()

	return f
	 
def doFit(file,fullSel):
	f = ROOT.TFile(file,"READ")
	histos   = []
	profiles = []
	h11 = f.Get("rhoHat_b1")    ; histos.append(h11)
	h12 = f.Get("rhoHat_b2")    ; histos.append(h12)
	h13 = f.Get("rhoHat_b3")    ; histos.append(h13)
	h21 = f.Get("rho_b1")       ; histos.append(h21)
	h22 = f.Get("rho_b2")       ; histos.append(h22)
	h23 = f.Get("rho_b3")       ; histos.append(h23)
	hTOT1 = f.Get('tot_rhoHat') ; histos.append(hTOT1)
	hTOT2 = f.Get('tot_rho')    ; histos.append(hTOT2)
	
	cols = [30,46,38]*2
	canvas1,leg1 = getCanvas("#rho")
	canvas2,leg2 = getCanvas("#rho'")
	for i,h in enumerate(histos):
		hP    = h.ProfileX()
		hP.SetName(h.GetName())
		if i<6 : hP.SetMarkerColor(cols[i])
		else:    hP.SetMarkerColor(1); hP.SetMarkerStyle(4);
		if not fullSel: hP.Rebin(2)
		profiles.append(hP)
	
	if fullSel:
		profiles[0].GetXaxis().SetRangeUser(0.,5.); frRes0 = profiles[0].Fit("pol1", "SR+", "same", 2., 4.)
		profiles[1].GetXaxis().SetRangeUser(0.,5.); frRes1 = profiles[1].Fit("pol1", "SR+", "same", 1.8, 4.0)
		profiles[2].GetXaxis().SetRangeUser(0.,5.); frRes2 = profiles[2].Fit("pol1", "SR+", "same", 1.1, 4.)
		profiles[3].GetXaxis().SetRangeUser(-7.,4.); frRes3 = profiles[3].Fit("pol1", "SR+", "same",-4.,-2.)
		profiles[4].GetXaxis().SetRangeUser(-7.,4.); frRes4 = profiles[4].Fit("pol1", "SR+", "same",-4.6,-2.)
		profiles[5].GetXaxis().SetRangeUser(-7.,4.); frRes5 = profiles[5].Fit("pol1", "SR+", "same",-6.,-3.)
		profiles[6].GetXaxis().SetRangeUser(0.,5.); frRes6 = profiles[6].Fit("pol1", "SR+", "same", 2., 4.0)
		profiles[7].GetXaxis().SetRangeUser(-7.,4.); frRes7 = profiles[7].Fit("pol1", "SR+", "same",-4.2,-2.)
	
	else:
		frRes0 = profiles[0].Fit("pol1", "SR+", "same", 1., 4.)
		frRes1 = profiles[1].Fit("pol1", "SR+", "same", 1., 4.)
		frRes2 = profiles[2].Fit("pol1", "SR+", "same", 1., 4.)
		
		frRes6 = profiles[6].Fit("pol1", "SR+", "same", 1., 4.)
		
		frRes3 = profiles[3].Fit("pol1", "SR+", "same",-5.,-2.)
		frRes4 = profiles[4].Fit("pol1", "SR+", "same",-5.,-2.)
		frRes5 = profiles[5].Fit("pol1", "SR+", "same",-5.,-2.)
		
		frRes7 = profiles[7].Fit("pol1", "SR+", "same",-5.,-2.)
	
	
	canvas2.cd()
	profiles[0].GetYaxis().SetRangeUser(0.,1.5)
	profiles[0].GetYaxis().SetTitle("#tau_{21}")
	profiles[0].GetXaxis().SetTitle("#rho'")
	profiles[0].Draw("")     ; leg2.AddEntry(profiles[0],"300-400 GeV, slope = %.3f #pm %.3f"%(frRes0.Parameter(1),frRes0.ParError(1)),"LEP")
	profiles[1].Draw("same") ; leg2.AddEntry(profiles[1],"400-500 GeV, slope = %.3f #pm %.3f"%(frRes1.Parameter(1),frRes1.ParError(1)),"LEP")
	profiles[2].Draw("same") ; leg2.AddEntry(profiles[2],"1000-1100 GeV, slope = %.3f #pm %.3f"%(frRes2.Parameter(1),frRes2.ParError(1)),"LEP")
	profiles[6].Draw("same") ; leg2.AddEntry(profiles[6],"All jets, slope = %.4f #pm %.4f"%(frRes6.Parameter(1),frRes6.ParError(1)),"LEP")
	leg2.Draw("")
	cmslabel_sim(canvas2,'2017',11)
	canvas2.Update()
	canvas2.SaveAs(file.replace(".root","")+"_rhoPrime.pdf")

	canvas1.cd()
	profiles[3].GetYaxis().SetRangeUser(0.,1.5)
	profiles[3].GetYaxis().SetTitle("#tau_{21}")
	profiles[3].GetXaxis().SetTitle("#rho")
	profiles[3].Draw("")     ; leg1.AddEntry(profiles[3],"300-400 GeV, slope = %.3f #pm %.3f"%(frRes3.Parameter(1),frRes3.ParError(1)),"LEP")
	profiles[4].Draw("same") ; leg1.AddEntry(profiles[4],"400-500 GeV, slope = %.3f #pm %.3f"%(frRes4.Parameter(1),frRes4.ParError(1)),"LEP")
	profiles[5].Draw("same") ; leg1.AddEntry(profiles[5],"1000-1100 GeV, slope = %.3f #pm %.3f"%(frRes5.Parameter(1),frRes5.ParError(1)),"LEP")
	profiles[7].Draw("same") ; leg1.AddEntry(profiles[7],"All jets, slope = %.4f #pm %.4f"%(frRes7.Parameter(1),frRes7.ParError(1)),"LEP")
	leg1.Draw("")
	cmslabel_sim(canvas1,'2017',11)
	canvas1.Update()
	canvas1.SaveAs(file.replace(".root","")+"_rho.pdf")
	sleep(10)

def doClosure(file,fullSel):
	f = ROOT.TFile(file,"READ")
	histos   = []
	profiles = []
	h11   = f.Get("tuned_rhoHat_b1")    ; histos.append(h11)
	h12   = f.Get("tuned_rhoHat_b2")    ; histos.append(h12)
	h13   = f.Get("tuned_rhoHat_b3")    ; histos.append(h13)
	h21   = f.Get("tuned_rho_b1")       ; histos.append(h21)
	h22   = f.Get("tuned_rho_b2")       ; histos.append(h22)
	h23   = f.Get("tuned_rho_b3")       ; histos.append(h23)
	hTOT1 = f.Get('tuned_tot_rhoHat') ; histos.append(hTOT1)
	hTOT2 = f.Get('tuned_tot_rho')    ; histos.append(hTOT2)
	
	cols = [30,46,38]*2
	canvas1,leg1 = getCanvas("#rho")
	canvas2,leg2 = getCanvas("#rho'")
	for i,h in enumerate(histos):
		hP    = h.ProfileX()
		hP.SetName(h.GetName())
		if i<6 : hP.SetMarkerColor(cols[i])
		else:    hP.SetMarkerColor(1); hP.SetMarkerStyle(4);
		if not fullSel: hP.Rebin(2)
		profiles.append(hP)
	
	if fullSel:
		profiles[0].GetXaxis().SetRangeUser(0.,5.); frRes0 = profiles[0].Fit("pol1", "SR+", "same", 2., 4.)
		profiles[1].GetXaxis().SetRangeUser(0.,5.); frRes1 = profiles[1].Fit("pol1", "SR+", "same", 1.8, 4.0)
		profiles[2].GetXaxis().SetRangeUser(0.,5.); frRes2 = profiles[2].Fit("pol1", "SR+", "same", 1.1, 4.)
		profiles[3].GetXaxis().SetRangeUser(-7.,4.); frRes3 = profiles[3].Fit("pol1", "SR+", "same",-4.,-2.)
		profiles[4].GetXaxis().SetRangeUser(-7.,4.); frRes4 = profiles[4].Fit("pol1", "SR+", "same",-4.6,-2.)
		profiles[5].GetXaxis().SetRangeUser(-7.,4.); frRes5 = profiles[5].Fit("pol1", "SR+", "same",-6.,-3.)
		profiles[6].GetXaxis().SetRangeUser(0.,5.); frRes6 = profiles[6].Fit("pol1", "SR+", "same", 2., 4.0)
		profiles[7].GetXaxis().SetRangeUser(-7.,4.); frRes7 = profiles[7].Fit("pol1", "SR+", "same",-4.2,-2.)
	
	else:
		frRes0 = profiles[0].Fit("pol1", "SR+", "same", 1., 4.)
		frRes1 = profiles[1].Fit("pol1", "SR+", "same", 1., 4.)
		frRes2 = profiles[2].Fit("pol1", "SR+", "same", 1., 4.)
		
		frRes6 = profiles[6].Fit("pol1", "SR+", "same", 1., 4.)
		
		frRes3 = profiles[3].Fit("pol1", "SR+", "same",-5.,-2.)
		frRes4 = profiles[4].Fit("pol1", "SR+", "same",-5.,-2.)
		frRes5 = profiles[5].Fit("pol1", "SR+", "same",-5.,-2.)
		
		frRes7 = profiles[7].Fit("pol1", "SR+", "same",-5.,-2.)
	
	
	canvas2.cd()
	profiles[0].GetYaxis().SetRangeUser(0.,1.5)
	profiles[0].GetYaxis().SetTitle("#tau_{21}")
	profiles[0].GetXaxis().SetTitle("#rho'")
	profiles[0].Draw("")     ; leg2.AddEntry(profiles[0],"300-400 GeV, slope = %.3f #pm %.3f"%(frRes0.Parameter(1),frRes0.ParError(1)),"LEP")
	profiles[1].Draw("same") ; leg2.AddEntry(profiles[1],"400-500 GeV, slope = %.3f #pm %.3f"%(frRes1.Parameter(1),frRes1.ParError(1)),"LEP")
	profiles[2].Draw("same") ; leg2.AddEntry(profiles[2],"1000-1100 GeV, slope = %.3f #pm %.3f"%(frRes2.Parameter(1),frRes2.ParError(1)),"LEP")
	profiles[6].Draw("same") ; leg2.AddEntry(profiles[6],"All jets, slope = %.4f #pm %.4f"%(frRes6.Parameter(1),frRes6.ParError(1)),"LEP")
	leg2.Draw("")
	cmslabel_sim(canvas2,'2017',11)
	canvas2.Update()
	canvas2.SaveAs(file.replace(".root","")+"_rhoPrimeClosure.pdf")

	canvas1.cd()
	profiles[3].GetYaxis().SetRangeUser(0.,1.5)
	profiles[3].GetYaxis().SetTitle("#tau_{21}")
	profiles[3].GetXaxis().SetTitle("#rho")
	profiles[3].Draw("")     ; leg1.AddEntry(profiles[3],"300-400 GeV, slope = %.3f #pm %.3f"%(frRes3.Parameter(1),frRes3.ParError(1)),"LEP")
	profiles[4].Draw("same") ; leg1.AddEntry(profiles[4],"400-500 GeV, slope = %.3f #pm %.3f"%(frRes4.Parameter(1),frRes4.ParError(1)),"LEP")
	profiles[5].Draw("same") ; leg1.AddEntry(profiles[5],"1000-1100 GeV, slope = %.3f #pm %.3f"%(frRes5.Parameter(1),frRes5.ParError(1)),"LEP")
	profiles[7].Draw("same") ; leg1.AddEntry(profiles[7],"All jets, slope = %.4f #pm %.4f"%(frRes7.Parameter(1),frRes7.ParError(1)),"LEP")
	leg1.Draw("")
	cmslabel_sim(canvas1,'2017',11)
	canvas1.Update()
	canvas1.SaveAs(file.replace(".root","")+"_rhoClosure.pdf")
	sleep(10)
  
def submitJobs(samples,template,target,jobname="DDT"):
  files = []
  sampleTypes = template.split(',')
  for f in os.listdir(samples):
    for t in sampleTypes:
      if f.find(t) == -1: continue 
      if f.startswith('.'): continue
      if f.find('.root') != -1 and f.find('rawPUMC') == -1: 
        print f
        files.append(f)
  
  NumberOfJobs= len(files)
  cmd = "python fitDDT.py -H "
  queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw

  try: os.system("rm -r tmp"+jobname)
  except: print "No tmp/ directory"
  os.system("mkdir tmp"+jobname)
  try: os.stat(target)
  except: os.mkdir(target)


  ##### Creating and sending jobs #####
  joblist = []
  ###### loop for creating and sending jobs #####
  path = os.getcwd()
  for x in range(1, int(NumberOfJobs)+1):
     os.system("mkdir tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))
     os.chdir("tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))
     #os.system("mkdir tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))
     os.chdir(path+"/tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))

     with open('job_%s.sh'%files[x-1].replace(".root",""), 'w') as fout:
        fout.write("#!/bin/sh\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("echo 'WORKDIR ' ${PWD}\n")
        fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
        fout.write("cd "+str(path)+"\n")
        fout.write("cmsenv\n")
        fout.write(cmd+" -t "+files[x-1]+" -o "+path+"/"+target+"/"+"\n")
        fout.write("echo 'STOP---------------'\n")
        fout.write("echo\n")
        fout.write("echo\n")
     os.system("chmod 755 job_%s.sh"%(files[x-1].replace(".root","")) )

     os.system("bsub -q "+queue+" -o logs job_%s.sh -J %s"%(files[x-1].replace(".root",""),jobname))
     print "job nr " + str(x) + " submitted: " + files[x-1].replace(".root","")
     joblist.append("%s"%(files[x-1].replace(".root","")))
     os.chdir("../..")

  print
  print "your jobs:"
  os.system("bjobs")
  userName=os.environ['USER']
  return joblist, files

if __name__ == '__main__':
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-f', '--folder'  , action='store', type='string', dest='folder', default='samples_jer/')
  parser.add_option('-t', '--template', action='store', type='string', dest='template', default='QCD_Pt_')
  parser.add_option('-H', '--histos', action='store_true', dest='doHistos', default=False)
  parser.add_option('-c', '--closure', action='store_true', dest='doClosure', default=False)
  parser.add_option('-o', '--output', action='store', type='string', dest='target', default='ddt_out/')
  parser.add_option('--doFit', action='store_true', dest='doFit', default=False)
  (options, args) = parser.parse_args()
  
  samples  = options.folder
  template = options.template
  target   = options.target
  
  if options.doFit:
    cmd = "rm ddt_out/rho_pythia*.root"
    os.system(cmd)
    cmd = "hadd -f ddt_out/rho_pythia_FullSel.root ddt_out/*rho_pythia_FullSel.root"
    os.system(cmd)
    cmd = "hadd -f ddt_out/rho_pythia.root ddt_out/*rho_pythia.root"
    os.system(cmd)
    
    doFit(target+"rho_pythia.root",False)
    doFit(target+"rho_pythia_FullSel.root",True)
  
  elif options.doHistos:
    QCDPtPlotters = getPlotters(template,False)
    QCD = MergedPlotter(QCDPtPlotters)
    QCD.setLineProperties(1,434,2)
    QCD.setFillProperties(1001,0)

    file1 = doDDT(QCD,cuts['common']    ,target+template.replace(".root","")+"_rho_pythia.root")
    file2 = doDDT(QCD,cuts['commonTOT'] ,target+template.replace(".root","")+"_rho_pythia_FullSel.root")
  
  elif options.doClosure:
    cmd = "rm ddt_out/rho_pythia*.root"
    os.system(cmd)
    cmd = "hadd -f ddt_out/rho_pythia_FullSel.root ddt_out/*rho_pythia_FullSel.root"
    os.system(cmd)
    cmd = "hadd -f ddt_out/rho_pythia.root ddt_out/*rho_pythia.root"
    os.system(cmd)
    
    doClosure(target+"rho_pythia.root",False)
    doClosure(target+"rho_pythia_FullSel.root",True)
  
  
  else:
    if not os.path.exists(target):
        print 'Target directory', target,'does not exist, creating it...'
        cmd = "mkdir %s" %target
        os.system(cmd)  
    joblist, files = submitJobs(samples,template,target,jobname="DDT")
    sys.exit()
  
  

