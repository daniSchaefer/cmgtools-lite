
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


ROOT.gROOT.SetBatch(True)

H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref

directory='/eos/user/t/thaarres/www/vvana/control_plots'
lumi_13TeV = "35.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=0
iPosX = 11
cuts={}
lumi='35900'
cuts['common'] = '(njj>0&&jj_LV_mass>1000&&abs(jj_l1_eta-jj_l2_eta)<1.3)'

cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
cuts['LP'] = '(jj_l1_tau2/jj_l1_tau1>0.35&&jj_l1_tau2/jj_l1_tau1<0.75)'

cuts['nonres'] = '1'

purities=['HP', 'LP']

qWTemplate="QstarToQW"
qZTemplate="QstarToQZ"
BRqW=1.
BRqZ=1.

dataTemplate="JetHT"
nonResTemplate="QCD_Pt_"

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

def compare(p1,p2,var,postfix,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2,logY=0):
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    name = "%s_%s" %(postfix, var.replace("(","").replace(")","").replace("-","_"))
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
    legend = ROOT.TLegend(0.62,0.7,0.92,0.9,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    
    h1=p1.drawTH1(var,cut1,lumi,bins,mini,maxi,title,unit,"HIST")
    h2=p2.drawTH1(var,cut2,lumi,bins,mini,maxi,title,unit,"HIST")
    
    h2.Scale(0.5*(h1.Integral()/h2.Integral()))
    h1.Draw("HISTC")
    h2.Draw("HISTSAME")
    maxY = h1.GetMaximum()*1.5
    if h1.GetMaximum() < h2.GetMaximum(): 
		 maxY = h2.GetMaximum()*1.5
    if logY: 
		 canvas.SetLogy()
		 maxY = maxY*200
    h1.GetYaxis().SetRangeUser(0.001,maxY)
    # h1.DrawNormalized("HISTC")
    # h2.DrawNormalized("SAMEHIST")
    # h1=p1.drawTH1Binned(var,cut1,lumi,bins,title,unit, "HISTC")
    # h2=p2.drawTH1Binned(var,cut2,lumi,bins,title,unit, "SAMEHIST")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"LF")
    legend.Draw()
    
    
    # pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    # pt.SetBorderSize(0)
    # pt.SetTextAlign(12)
    # pt.SetFillStyle(0)
    # pt.SetTextFont(42)
    # pt.SetTextSize(0.03)
    #
    # pt.Draw()
    cmslabel_prelim(canvas,'2016',11)
    # CMS_lumi(canvas,  iPeriod,  iPosX )
    
    
    return canvas,h1,h2,legend #,pt
	 
def compareQCD(p1,p2,p3,var,postfix,cut,bins,mini,maxi,title,unit,leg1,leg2,leg3,logY=0):
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    name = "qcdCompare_%s_%s" %(postfix, var.replace("(","").replace(")","").replace("-","_"))
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
    legend = ROOT.TLegend(0.62,0.7,0.92,0.9,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    
    h1=p1.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST")
    h2=p2.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST")
    h3=p3.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST")
		
    SFpythia   = h1.Integral()/h3.Integral()
    SFmadgraph = h2.Integral()/h3.Integral()
    print "Herwig scalefactor (derived from Pythia   ) = " , SFpythia
    print "Herwig scalefactor (derived from Madgraph ) = " , SFmadgraph
    h3.Draw("HIST")
    h2.Draw("HISTSAME")
    h1.Draw("MSAME")
    minY = 0.
    maxY = h1.GetMaximum()*1.5
    if h1.GetMaximum() < h2.GetMaximum():
     maxY = h2.GetMaximum()*1.5
    if h2.GetMaximum() < h3.GetMaximum():
     maxY = h3.GetMaximum()*1.5
    if logY:
     canvas.SetLogy()
     minY = 0.1
     maxY = maxY*200
    h1.GetYaxis().SetRangeUser(minY,maxY)
    # h1.DrawNormalized("HISTC")
    # h2.DrawNormalized("SAMEHIST")
    # h1=p1.drawTH1Binned(var,cut1,lumi,bins,title,unit, "HISTC")
    # h2=p2.drawTH1Binned(var,cut2,lumi,bins,title,unit, "SAMEHIST")
    legend.AddEntry(h1,leg1,"LEP")
    legend.AddEntry(h2,leg2,"LF")
    legend.AddEntry(h3,leg3,"LF")
    legend.Draw("same")
    
    cmslabel_prelim(canvas,'2016',11)
    canvas.Update()

    return canvas,h1,h2,h3,legend #,pt



QCDPtPlotters = getPlotters(nonResTemplate,False)
QCDhtPlotters = getPlotters('QCD_HT',False)
QCDherwigPlotters = getPlotters('QCD_Pt-',False)
QCD = MergedPlotter(QCDPtPlotters)
QCDht = MergedPlotter(QCDhtPlotters)
QCDherwig = MergedPlotter(QCDherwigPlotters)

#
# # DATAPlotters = getPlotters('SingleJet',True)
# # data=MergedPlotter(DATAPlotters)
#
# SigPlotters = getPlotters('QstarToQW_2000',False)
# sig = MergedPlotter(SigPlotters)
#
#
QCD.setFillProperties(1001,921)

QCDht.setLineProperties(1,633,2)
QCDht.setFillProperties(1001,0)
#
QCDherwig.setLineProperties(1,434,2)
QCDherwig.setFillProperties(1001,0)
#
# sig.setFillProperties(3001,ROOT.kGreen+2)


#Stack
# jjStack = StackPlotter()
# jjStack.addPlotter(QCD,"QCD","QCD multijet","background")
# jjStack.addPlotter(data,"data_obs","Data","data")

for p in purities:
	canvs = []
	print "Plotting variables for category %s" %(p)
	cut='*'.join([cuts['common'],cuts[p]])
	postfix = p
	# c1 = compare(QCD,sig,'jj_l1_tau21',postfix,cut,cut,20,0.,1.,'V candidate #tau_{21}',"","QCD","q*(2 TeV)#rightarrowqW")
	# c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
	# c2 = compare(QCD,sig,'jj_l2_tau21',postfix,cut,cut,20,0.,1.,'q candidate #tau_{21}',"","QCD","q*(2 TeV)#rightarrowqW")
	# c2[0].SaveAs(directory+"/"+c2[0].GetName()+".png")
	# c3 = compare(QCD,sig,'jj_l1_softDrop_mass',postfix,cut,cut,60,0.,300.,'V candidate mass',"GeV","QCD","q*(2 TeV)#rightarrowqW")
	# c3[0].SaveAs(directory+"/"+c3[0].GetName()+".png")
	# c4 = compare(QCD,sig,'jj_l2_softDrop_mass',postfix,cut,cut,60,0.,300.,'q candidate mass',"GeV","QCD","q*(2 TeV)#rightarrowqW")
	# c4[0].SaveAs(directory+"/"+c4[0].GetName()+".png")
	# c5 = compare(QCD,sig,'jj_LV_mass',postfix,cut,cut,80,1000.,8000.,'M_{qV}',"GeV","QCD","q*(2 TeV)#rightarrowqW",1)
	# c5[0].SaveAs(directory+"/"+c5[0].GetName()+".png")
	# c6 = compare(QCD,sig,'abs(jj_l1_eta-jj_l2_eta)',postfix,cut,cut,13,0.,1.3,'#Delta#eta(q,V)',"","QCD","q*(2 TeV)#rightarrowqW")
	# c6[0].SaveAs(directory+"/"+c6[0].GetName()+".png")
	# c7 = compare(QCD,sig,'jj_l1_pt',postfix,cut,cut,50,200.,5000.,'V candidate p_{T}',"GeV","QCD","q*(2 TeV)#rightarrowqW",1)
	# c7[0].SaveAs(directory+"/"+c7[0].GetName()+".png")
	# c8 = compare(QCD,sig,'jj_l2_pt',postfix,cut,cut,50,200.,5000.,'q candidate p_{T}',"GeV","QCD","q*(2 TeV)#rightarrowqW",1)
	# c8[0].SaveAs(directory+"/"+c8[0].GetName()+".png")
	#
	
	
	d8 = compareQCD(QCD,QCDht,QCDherwig,'jj_l1_softDrop_mass',postfix,cut,50,0.,300.,'V candidate mass',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",0)
	d8[0].SaveAs(directory+"/"+d8[0].GetName()+".png")
	d9 = compareQCD(QCD,QCDht,QCDherwig,'jj_LV_mass',postfix,cut,80,1000.,8000.,'M_{qV}',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",1)
	d9[0].SaveAs(directory+"/"+d9[0].GetName()+".png")
	d10 = compareQCD(QCD,QCDht,QCDherwig,'jj_l2_softDrop_mass',postfix,cut,50,0.,300.,'q candidate mass',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",0)
	d10[0].SaveAs(directory+"/"+d10[0].GetName()+".png")
	d11 = compareQCD(QCD,QCDht,QCDherwig,'jj_l1_tau21',postfix,cut,20,0.,1.,'V candidate #tau_{21}','',"Pythia8","Madgraph+Pythia8","Herwig++",0)
	d11[0].SaveAs(directory+"/"+d11[0].GetName()+".png")
	d12 = compareQCD(QCD,QCDht,QCDherwig,'jj_l2_tau21',postfix,cut,20,0.,1.,'q candidate #tau_{21}','',"Pythia8","Madgraph+Pythia8","Herwig++",0)
	d12[0].SaveAs(directory+"/"+d12[0].GetName()+".png")


