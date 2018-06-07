
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

cuts['commonTOT'] = '(njj>0&&jj_LV_mass>838&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>55.&&jj_l1_softDrop_mass<215.&&jj_l2_softDrop_mass>55.&&jj_l2_softDrop_mass<215.)'
cuts['common'] = '(njj>0&&jj_LV_mass>838&&abs(jj_l1_eta-jj_l2_eta)<1.3)'

cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
cuts['LP'] = '(jj_l1_tau2/jj_l1_tau1>0.35&&jj_l1_tau2/jj_l1_tau1<0.75)'

cuts['nonres'] = '1'

purities=['HP', 'LP']

qWTemplate="QstarToQW"
qZTemplate="QstarToQZ"
BRqW=1.
BRqZ=1.

dataTemplate="JetHT"
nonResTemplate="QCD_Pt-"

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
    for filename in os.listdir('samples'):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter('samples/'+fname+'.root','tree'))
                if not isData:
                    plotters[-1].setupFromFile('samples/'+fname+'.pck')
                    plotters[-1].addCorrectionFactor('xsec','tree')
                    plotters[-1].addCorrectionFactor('genWeight','tree')
                    plotters[-1].addCorrectionFactor('puWeight','tree')
                    plotters[-1].addCorrectionFactor(corr,'flat')
                    
    return  plotters

def doDDT(p1,cut,outname):
	cut1 ='*'.join([cut,'(jj_l1_pt>300&&jj_l1_pt<400)'])
	cut2 ='*'.join([cut,'(jj_l1_pt>500&&jj_l1_pt<600)'])
	cut3 ='*'.join([cut,'(jj_l1_pt>1000&&jj_l1_pt<1100)'])
	hTOT1=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"         ,cut ,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h11=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut1,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h12=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut2,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	h13=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/jj_l1_pt))"           ,cut3,"1", 80,   -1. ,8. , 60, 0., 1.5,"#rho'",'' ,"#tau_{21}",'',"COLZ")
	
	hTOT2=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))",cut ,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")                                                                                                                                            
	h21=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut1,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	h22=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut2,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	h23=p1.drawTH2("(jj_l1_tau2/jj_l1_tau1):(TMath::Log(jj_l1_softDrop_mass*jj_l1_softDrop_mass/(jj_l1_pt*jj_l1_pt)))"  ,cut3,"1", 100, -10. ,0. , 60, 0., 1.5,"#rho" ,'' ,"#tau_{21}",'',"COLZ")
	
	f = ROOT.TFile(outname,"RECREATE")
	h11.Write("rhoHat_b1")
	h12.Write("rhoHat_b2")
	h13.Write("rhoHat_b3")
	h21.Write("rho_b1")
	h22.Write("rho_b2")
	h23.Write("rho_b3")
	hTOT1.Write('tot_rhoHat')
	hTOT2.Write('tot_rho')
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
	canvas2.SaveAs("rhoPrime_"+file.replace(".root",".pdf"))

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
	canvas1.SaveAs("rho_"+file.replace(".root",".pdf"))
	sleep(10)

QCDPtPlotters = getPlotters("QCD_Pt_",False)
QCD = MergedPlotter(QCDPtPlotters)
# QCDherwigPlotters = getPlotters('QCD_Pt-',False)
# QCDherwig = MergedPlotter(QCDherwigPlotters)

QCD.setLineProperties(1,434,2)
QCD.setFillProperties(1001,0)

file1 = doDDT(QCD,cuts['common'],"rho_pythia.root")
file2 = doDDT(QCD,cuts['commonTOT'] ,"rho_pythia_FullSel.root")
doFit("rho_pythia.root",False)
doFit("rho_pythia_FullSel.root",True)
