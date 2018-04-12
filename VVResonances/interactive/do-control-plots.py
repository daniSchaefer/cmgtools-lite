
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

from datetime import datetime
startTime = datetime.now()

ROOT.gROOT.SetBatch(True)


dijetBinning = True

if dijetBinning:
    HCALbinsMVV=" --binsMVV 1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5000"
    HCALbinsMVVSignal=" --binsMVV 1,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808"
    print "set binsMVV to 36"
else:
    HCALbinsMVV=""
    HCALbinsMVVSignal=""
	
H_ref = 600
W_ref = 800
W = W_ref
H  = H_ref

directory='control_plots/'
try: os.stat(directory)
except: os.mkdir(directory)
	
lumi_13TeV = "35.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=0
iPosX = 11
cuts={}
lumi='35900'

cat ={}
# For retuned DDT tau 21, use this
cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98'
cat['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.98'
cat['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.98'

cuts={}

cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'

cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
cuts['NP'] = '(('+cat['LP1']+'&&'+cat['NP2']+')||('+cat['NP1']+'&&'+cat['LP2']+'))'

cuts['nonres'] = '1'

purities=['HPHP','HPLP','LPLP','NP']
purities=['HPHP']


# use arbitrary cross section 0.001 so limits converge better
BRWW=1.*0.001
BRZZ=1.*0.001*0.6991*0.6991
BRWZ=1.*0.001*0.6991*0.676

#nonResTemplate="Dijet" #to compare shapes

minMJ=55.0
maxMJ=215.0

minMVV=1000.0
maxMVV=5000.0

minMX=1200.0
maxMX=7000.0

binsMJ=80
binsMVV=100
if dijetBinning:
    binsMVV = 36

cuts['nonres'] = '1'

def getCanvas(name="c1"):
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
    legend = ROOT.TLegend(0.62,0.7,0.92,0.9,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    
    return canvas,legend

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

def compareSigQCD(p1,p2,var,postfix,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2,logY=0):
   
    name = "%s_%s" %(postfix, var.replace("(","").replace(")","").replace("-","_"))
    canvas,legend = getCanvas(name)
    canvas.cd()
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
    name = "qcdCompare_%s_%s" %(postfix, var.replace("(","").replace(")","").replace("-","_"))
    canvas,legend = getCanvas(name)
    canvas.cd()

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

def dataMC(mc,data,sig1,sig2,sig3,var,postfix,cut,bins,mini,maxi,title,unit,ytitle,legMC,legDat,legSig1,legSig2,legSig3,logY=0):
    name = "%s_%s" %(postfix, var.replace("(","").replace(")","").replace("-","_"))
    canvas, legend = getCanvas(name)

    hData = data.drawTH1(var,cut,"1.",bins,mini,maxi,title,unit,"HIST")
    hMC   = mc  .drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST")
    hSig1 = sig1.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST"); hSig1.Scale(0.1*(hData.Integral()/hSig1.Integral()))
    hSig2 = sig2.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST"); hSig2.Scale(0.1*(hData.Integral()/hSig2.Integral()))
    hSig3 = sig3.drawTH1(var,cut,lumi,bins,mini,maxi,title,unit,"HIST"); hSig3.Scale(0.1*(hData.Integral()/hSig3.Integral()))
    
    hData.GetYaxis().SetTitle(ytitle)
    hData.GetXaxis().SetTitle(hData.GetXaxis().GetTitle().replace("[]",""))
    hData.Draw("EP")
    hMC.Draw("HISTCSAME")
    hSig1.Draw("HISTCSAME")
    hSig2.Draw("HISTCSAME")
    hSig3.Draw("HISTCSAME")
    maxY = hData.GetMaximum()*1.5
    # if hData.GetMaximum() < hMC.GetMaximum(): maxY = hMC.GetMaximum()*1.5
 #    if logY: canvas.SetLogy(); maxY = maxY*200
    hData.GetYaxis().SetRangeUser(0.001,maxY)
    # hData.DrawNormalized("HISTC")
    # hMC.DrawNormalized("SAMEHIST")
    # hData=data.drawTH1Binned(var,cut1,lumi,bins,title,unit, "HISTC")
    # hMC=mc.drawTH1Binned(var,cut2,lumi,bins,title,unit, "SAMEHIST")
    legend.AddEntry(hData,legDat,"LEP")
    legend.AddEntry(hMC  ,legMC,"F")
    legend.AddEntry(hSig1 ,legSig1,"L")
    legend.AddEntry(hSig2 ,legSig2,"L")
    legend.AddEntry(hSig3 ,legSig3,"L")
    legend.Draw()
    
    
    
    # pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    # pt.SetBorderSize(0)
    # pt.SetTextAlign(12)
    # pt.SetFillStyle(0)
    # pt.SetTextFont(42)
    # pt.SetTextSize(0.03)
    #
    # pt.Draw()
    canvas.Update()
    cmslabel_prelim(canvas,'2016',11)
    canvas.Update()
    return canvas,hData,hSig1,hSig2,hSig3,legend #,pt
    




# QCDhtPlotters = getPlotters('QCD_HT',False)
# QCDht = MergedPlotter(QCDhtPlotters)
# QCDht.setLineProperties(1,633,2)
# QCDht.setFillProperties(1001,0)

BulkGravWWTemplate="BulkGravToWW_narrow_1800"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_narrow_1800"
WprimeTemplate= "WprimeToWZToWhadZhad_narrow_1800"
dataTemplate="JetHT"
nonResTemplate="QCD_Pt_" #high stat
nonResTemplateH="QCD_Pt-" #low stat --> use this for tests

# QCDPtPlotters = getPlotters(nonResTemplate,False)
# QCD = MergedPlotter(QCDPtPlotters)
# QCD.setLineProperties(1,1,1)
# QCD.setFillProperties(3001,36)

QCDherwigPlotters = getPlotters(nonResTemplate,False)
QCDherwig = MergedPlotter(QCDherwigPlotters)
QCDherwig.setLineProperties(1,1,1)
QCDherwig.setFillProperties(3001,36)

DATAPlotters = getPlotters(dataTemplate,True)
data=MergedPlotter(DATAPlotters)
data.setLineProperties(1,1,1)
data.setFillProperties(0,0)

SigPlottersWZ = getPlotters(WprimeTemplate,False)
sigWZ = MergedPlotter(SigPlottersWZ)
sigWZ.setLineProperties(1,ROOT.kMagenta+2,3)
sigWZ.setFillProperties(0,0)

SigPlottersWW = getPlotters(BulkGravWWTemplate,False)
sigWW = MergedPlotter(SigPlottersWW)
sigWW.setLineProperties(2,ROOT.kOrange+7,3)
sigWW.setFillProperties(0,0)

SigPlottersZZ = getPlotters(BulkGravZZTemplate,False)
sigZZ = MergedPlotter(SigPlottersZZ)
sigZZ.setLineProperties(9,ROOT.kGreen+2,3)
sigZZ.setFillProperties(0,0)

#Stack
# jjStack = StackPlotter()
# jjStack.addPlotter(QCD,"QCD Pythia8","QCD multijet","background")
# jjStack.addPlotter(data,"data_obs","Data","data")

for p in purities:
	canvs = []
	print "Plotting variables for category %s" %(p)
	cut='*'.join([cuts['common'],cuts[p]])
	postfix = p
	c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_l1_softDrop_mass',postfix,cut,32,55.,215.,'V candidate softdrop mass',"GeV","Events / 5 GeV","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
	c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
	c1[0].SaveAs(directory+"/"+c1[0].GetName()+".root")
	c2 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_l1_mass',postfix,cut,32,55.,215.,'V candidate bare mass',"GeV","Events / 5 GeV","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
	c2[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
	c2[0].SaveAs(directory+"/"+c1[0].GetName()+".root")
# 	canv,leg= getCanvas("mass")
# 	canv.cd()
# 	c2[1].GetXaxis().SetTitle("V candidate mass [GeV]")
# 	# c2[2].SetLineStyle(2)
# # 	c2[3].SetLineStyle(2)
# # 	c2[1].SetMarkerStyle(4)
# 	c2[1].Draw("EP")
# 	c2[2].Draw("CSAME")
# 	c2[3].Draw("CSAME")
# 	c1[1].Draw("EPSAME")
# 	c1[2].Draw("HISTCSAME")
# 	c1[3].Draw("HISTCSAME")
# 	leg.AddEntry(c1[1],"Data","LEP")
# 	leg.AddEntry(c1[2],"QCD Pythia8","F")
# 	leg.AddEntry(c1[3],"W'(2 TeV)#rightarrowWZ","L")
# 	leg.Draw()
# 	canv.SaveAs(directory+"/mass_compare.png")
# 	canv.SaveAs(directory+"/mass_compare.root")
postfix = "looseSel"
cut='*'.join([cuts['common']])
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_l1_pt',postfix,cut,48,200.,5000.,'V candidate p_{T}',"GeV","Events / 100 GeV","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".root")
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_l1_eta',postfix,cut,25,-2.5,2.5,'V candidate #eta',"","Events / 0.2","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".root")
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_LV_mass',postfix,cut,40,1000.,5000.,'Dijet invariant mass',"GeV","Events / 100 GeV","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ",1)
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".root")
cut='*'.join([cuts['common'],"(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ)])	
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'jj_l1_tau2/jj_l1_tau1',postfix,cut,20,0.,1.,'V candidate #tau_{21}',"","Events / 0.05","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".png")
c1[0].SaveAs(directory+"/"+c1[0].GetName()+".root")	
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))',postfix,cut,24,0.,1.2,'V candidate #tau_{21}^{DDT}','',"Events / 0.05","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
c1[0].SaveAs(directory+"/ddt_l1.png")
c1[0].SaveAs(directory+"/ddt_l1.root")	
c1 = dataMC(QCDherwig,data,sigWZ,sigWW,sigZZ,'(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))',postfix,cut,24,0.,1.2,'V candidate #tau_{21}^{DDT}','',"Events / 0.05","QCD Pythia8","Data","W'(2 TeV)#rightarrowWZ","G_{Bulk}(2 TeV)#rightarrowWW","G_{Bulk}(2 TeV)#rightarrowZZ")
c1[0].SaveAs(directory+"/ddt_l2.png")
c1[0].SaveAs(directory+"/ddt_l2.root")	
	
	
	
	
	# c2 = compareSigQCD(QCD,sig,'jj_l2_tau21',postfix,cut,cut,20,0.,1.,'q candidate #tau_{21}',"","QCD Pythia8","q*(2 TeV)#rightarrowqW")
	# c2[0].SaveAs(directory+"/"+c2[0].GetName()+".png")
	# c3 = compareSigQCD(QCD,sig,'jj_l1_softDrop_mass',postfix,cut,cut,60,0.,300.,'V candidate mass',"GeV","QCD Pythia8","q*(2 TeV)#rightarrowqW")
	# c3[0].SaveAs(directory+"/"+c3[0].GetName()+".png")
	# c4 = compareSigQCD(QCD,sig,'jj_l2_softDrop_mass',postfix,cut,cut,60,0.,300.,'q candidate mass',"GeV","QCD Pythia8","q*(2 TeV)#rightarrowqW")
	# c4[0].SaveAs(directory+"/"+c4[0].GetName()+".png")
	# c5 = compareSigQCD(QCD,sig,'jj_LV_mass',postfix,cut,cut,80,1000.,8000.,'M_{qV}',"GeV","QCD Pythia8","q*(2 TeV)#rightarrowqW",1)
	# c5[0].SaveAs(directory+"/"+c5[0].GetName()+".png")
	# c6 = compareSigQCD(QCD,sig,'abs(jj_l1_eta-jj_l2_eta)',postfix,cut,cut,13,0.,1.3,'#Delta#eta(q,V)',"","QCD Pythia8","q*(2 TeV)#rightarrowqW")
	# c6[0].SaveAs(directory+"/"+c6[0].GetName()+".png")
	# c7 = compareSigQCD(QCD,sig,'jj_l1_pt',postfix,cut,cut,50,200.,5000.,'V candidate p_{T}',"GeV","QCD Pythia8","q*(2 TeV)#rightarrowqW",1)
	# c7[0].SaveAs(directory+"/"+c7[0].GetName()+".png")
	# c8 = compareSigQCD(QCD,sig,'jj_l2_pt',postfix,cut,cut,50,200.,5000.,'q candidate p_{T}',"GeV","QCD Pythia8","q*(2 TeV)#rightarrowqW",1)
	# c8[0].SaveAs(directory+"/"+c8[0].GetName()+".png")
	#
	
	
	# d8 = compareQCD(QCD,QCDht,QCDherwig,'jj_l1_softDrop_mass',postfix,cut,50,0.,300.,'V candidate mass',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",0)
# 	d8[0].SaveAs(directory+"/"+d8[0].GetName()+".png")
	# d9 = compareQCD(QCD,QCDht,QCDherwig,'jj_LV_mass',postfix,cut,80,1000.,8000.,'M_{qV}',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",1)
	# d9[0].SaveAs(directory+"/"+d9[0].GetName()+".png")
	# d10 = compareQCD(QCD,QCDht,QCDherwig,'jj_l2_softDrop_mass',postfix,cut,50,0.,300.,'q candidate mass',"GeV","Pythia8","Madgraph+Pythia8","Herwig++",0)
	# d10[0].SaveAs(directory+"/"+d10[0].GetName()+".png")
	# d11 = compareQCD(QCD,QCDht,QCDherwig,'jj_l1_tau21',postfix,cut,20,0.,1.,'V candidate #tau_{21}','',"Pythia8","Madgraph+Pythia8","Herwig++",0)
	# d11[0].SaveAs(directory+"/"+d11[0].GetName()+".png")
	# d12 = compareQCD(QCD,QCDht,QCDherwig,'jj_l2_tau21',postfix,cut,20,0.,1.,'q candidate #tau_{21}','',"Pythia8","Madgraph+Pythia8","Herwig++",0)
	# d12[0].SaveAs(directory+"/"+d12[0].GetName()+".png")
	
print "Execution time: " ,datetime.now() - startTime

