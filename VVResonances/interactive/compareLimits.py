#!/usr/bin/env python

import ROOT
import optparse
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from time import sleep
from array import array

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='limit_compare.root',help="Limit plot")

parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1126.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=5500.)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.0001)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=0.14)
parser.add_option("-b","--blind",dest="blind",type=int,help="Not do observed ",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="Log plot",default=1)

parser.add_option("-t","--titleX",dest="titleX",default='M_{X} (GeV)',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default="#sigma x BR(G_{Bulk} #rightarrow WW) (pb)  ",help="title of y axis")

parser.add_option("-p","--period",dest="period",default='2017',help="period")
parser.add_option("-f","--final",dest="final",type=int, default=1,help="Preliminary or not")



#    parser.add_option("-x","--minMVV",dest="minMVV",type=float,help="minimum MVV",default=1000.0)
#    parser.add_option("-X","--maxMVV",dest="maxMVV",type=float,help="maximum MVV",default=13000.0)






(options,args) = parser.parse_args()
#define output dictionary



setTDRStyle()

def getLegend(x1=0.650010112,y1=0.523362,x2=0.90202143,y2=0.8279833):
  legend = ROOT.TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend

titleY = "#sigma x BR(G_{Bulk} #rightarrow WW) (pb)  "
oname= "BulkGWW"  
title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
files = ["LIMITS_DDT_latest/WW/HPLP/Limits_BulkGWW_HPLP_13TeV.root","LIMITS_DDT_latest/WW/HPHP/Limits_BulkGWW_HPHP_13TeV.root","LIMITS_DDT_latest/WW/combined/Limits_BulkGWW_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGWW_13TeV.root"]

# titleY = "#sigma x BR(G_{Bulk} #rightarrow ZZ) (pb)  "
# oname= "BulkGZZ"
# title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/ZZ/HPLP/Limits_BulkGZZ_HPLP_13TeV.root","LIMITS_DDT_latest/ZZ/HPHP/Limits_BulkGZZ_HPHP_13TeV.root","LIMITS_DDT_latest/ZZ/combined/Limits_BulkGZZ_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGZZ_13TeV.root"]

# titleY = "#sigma x BR(W' #rightarrow WZ) (pb)  "
# oname= "WprimeWZ"
# title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/WZ/HPLP/Limits_WprimeWZ_HPLP_13TeV.root","LIMITS_DDT_latest/WZ/HPHP/Limits_WprimeWZ_HPHP_13TeV.root","LIMITS_DDT_latest/WZ/combined/Limits_WprimeWZ_13TeV.root","limits_b2g17001/Limits_b2g17001_WZ_13TeV.root"]
# oname= "BulkGWW"
# title = ["HPHP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/newSigFits/Limits_BulkGWW_HPHP_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGWW_13TeV.root"]

titleY = "#sigma x BR(G_{bulk} #rightarrow WW) (pb)  "
oname= "BulkGWW"  
#title = ["3D HPHP+HPLP 2016","3D HPHP+HPLP 2017","3D '16+17' combined", "test1"]
#files = ["/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/2016limits_BulkGWW.root","/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/2017limits_BulkGWW.root","/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/limits_BulkGWW_13TeV_CMS_jj_combAll2.root","/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/2016limits_NoDijetBinning_BulkGWW_13TeV.root"]
#"/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/2017limits_NoDijetBinning_NOJER_BulkGWW_13TeV.root",




mydir = "/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/"

# 2016 limit comparison 
#title=["2016 No JER","2016 JER","B2G-17-001"]
#files = [mydir+"2016limits_NoDijetBinningForSig_NOJER_BulkGWW.root",mydir+"2016limits_NoDijetBinningForSig_JERSmearing_BulkGWW_2.root",mydir+"b2g-17-001/limits_b2g17-001.root"]
#outname = "compareLimits_"+oname+"_2016"


# 2017 limit comparison 

#title=["2017 signal shapes 2016","2017 No JER","2017 JER"]
#files = [mydir+"2017limits_BulkGWW_test2016SignalShapes.root",mydir+"2017limits_NoDijetBinningForSig_NoJER_BulkGWW.root",mydir+"2017limits_NoDijetBinningForSig_JERSmearing_BulkGWW.root"]
#outname = "compareLimits_"+oname+"_2017"


# compare old 2016 with 3D 2016 
oname="compAll_BulkGWW"
title=["2016 full 3D","2017 full 3D","B2G-18-002","B2G-17-001"]
files = [mydir+"2016limits_NoDijetBinningForSig_JERSmearing_BulkGWW_2.root",mydir+"2017limits_NoDijetBinningForSig_JERSmearing_BulkGWW.root", mydir+"limits_BulkGWW_13TeV_CMS_jj_combAll_newTau21pT.root",mydir+"b2g-17-001/limits_b2g17-001.root"]
outname = "compareLimits_"+oname+"_3D"


#oname="compSys_BulkGWW"
#title=["new tau21 pT ","B2G-18-002"," tau21 pt corr"]
#files = [mydir+"limits_BulkGWW_13TeV_CMS_jj_combAll_newTau21pT.root", mydir+"limits_VjetsNLOrew_BulkGWW_13TeV_CMS_jj_combAll.root",mydir+"limits_BulkGWW_13TeV_CMS_jj_combAll_newTau21pT_corr.root"]
#outname = "compareLimits_"+oname+"_3D"


#titleY = "#sigma x BR(W' #rightarrow WZ) (pb)  "
#oname = "Wprime"
#title = ["B2G-18-001"]
#files = ["/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/limits_WprimeWZ_13TeV_CMS_jj_combAll_newTau21pT.root"]
#outname = "compareLimits_"+oname+"_3D"



#titleY = "#sigma x BR(Z' #rightarrow WW) (pb)  "
#oname = "Zprime"
#title = ["B2G-18-001"]
#files = ["/portal/ekpbms2/home/dschaefer/DiBoson3D/limits/limits_ZprimeWW_13TeV_CMS_jj_combAll_newTau21pT.root"]
#outname = "compareLimits_"+oname+"_3D"


atlas_mps    = [1200,1500,2000,2500,3000,3500,4000,4500,5000]
atlas_BulkZZ = [200, 18, 4.8, 2.2, 1.2, 0.83, 0.60, 0.50, 0.40]; atlas_BulkZZ = [x * 0.001 for x in atlas_BulkZZ]; print "atlas_BulkZZ",atlas_BulkZZ;
atlas_BulkWW = [52 , 13, 4.0, 1.9, 1.2, 0.82, 0.62, 0.52, 0.50]; atlas_BulkWW = [x * 0.001 for x in atlas_BulkWW]; print "atlas_BulkWW",atlas_BulkWW;
atlas_Wprime = [200, 12, 3.0, 1.5, 1.0, 0.79, 0.52, 0.42, 0.38]; atlas_Wprime = [x * 0.001 for x in atlas_Wprime]; print "atlas_Wprime",atlas_Wprime;
atlas_Zprime = [180,  9, 3.1, 1.7, 1.0, 0.71, 0.52, 0.40, 0.37]; atlas_Zprime = [x * 0.001 for x in atlas_Zprime]; print "atlas_Zprime",atlas_Zprime;

x, y = array( 'd' ), array( 'd' )
vatlas_mps   = array("f",atlas_mps   )
 
if   oname.find("BulkGZZ")!=-1: lims  = array("f",atlas_BulkZZ)
elif oname.find("BulkGWW") !=-1: lims = array("f",atlas_BulkWW)
elif oname.find("Zprime") !=-1: lims  = array("f",atlas_Zprime)
elif oname.find("Wprime") !=-1: lims  = array("f",atlas_Wprime) ; print "atlas wprime"
atlas_lim = ROOT.TGraph( 9 , vatlas_mps, lims)


leg = getLegend()
leg.AddEntry(0,"Exp. limits","")
leg.AddEntry(0,"","")
tgraphs = []
for t,fname in zip(title,files):
	f=ROOT.TFile(fname)
	limit=f.Get("limit")
	data={}
	for event in limit:
		if float(event.mh)<options.minX or float(event.mh)>options.maxX:
		    continue
		
		if not (event.mh in data.keys()):
		    data[event.mh]={}
		
		
		lim = event.limit*0.001
		if fname.find("b2g17-001")!=-1: lim = event.limit*0.01
		if fname.find("b2g17-001")!=-1 and oname.find("BulkGZZ")!=-1: lim = event.limit*0.01/(0.6991*0.6991)
		if fname.find("b2g17-001")!=-1 and oname.find("Wprime")!=-1: lim = event.limit*0.01/(0.6991*0.676)
		if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
		    data[event.mh]['exp']=lim
               # if event.quantileExpected>0.52 and event.quantileExpected<0.90:            
		    data[event.mh]['exp']=lim
		
		
		
	line_plus1=ROOT.TGraph()
	line_plus1.SetName(f.GetName().replace(".root",""))



	N=0
	for mass,info in data.iteritems():
            print "for file "+fname
	    print 'Setting mass',mass,info

	    if not ('exp' in info.keys()):
	        print 'Incomplete file'
	        continue
    

	    line_plus1.SetPoint(N,mass,info['exp'])
	    N=N+1
	
	line_plus1.Sort()    
	tgraphs.append(line_plus1)  
	leg.AddEntry(line_plus1,t,"L")



#plotting information
H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref
c=ROOT.TCanvas("c","c",50,50,W,H)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetFrameFillStyle(0)
c.SetFrameBorderMode(0)
c.SetLeftMargin( L/W )
c.SetRightMargin( R/W )
c.SetTopMargin( T/H )
c.SetBottomMargin( B/H )
c.SetTickx(0)
c.SetTicky(0)
c.GetWindowHeight()
c.GetWindowWidth()
c.SetLogy()
c.SetGrid()
c.SetLogy()
	
frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
	
ROOT.gPad.SetTopMargin(0.08)
frame.GetXaxis().SetTitle(options.titleX)
frame.GetXaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetTitleSize(0.05)

frame.GetYaxis().SetTitle(titleY)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)

frame.GetYaxis().SetRangeUser(1e-4,0.5)



c.cd()
frame.Draw()
atlas_lim.SetLineColor(ROOT.kRed)
atlas_lim.SetLineWidth(2)
#leg.AddEntry(atlas_lim,"Atlas (CONF-16-018)","l")
#atlas_lim.Draw("PL")

cols  = [42,46,1,49]*3
tline = [10,9,2,1]*3
for i,g in enumerate(tgraphs):
	g.SetLineStyle(tline[i])
	g.SetLineColor(cols[i])
	g.SetLineWidth(2)
        g.SetMaximum(0.5)
	g.Draw("Lsame")

c.Update()
c.RedrawAxis()
c.SetLogy(options.log)
c.Draw()
leg.Draw("same")
cmslabel_prelim(c,options.period,11)

c.SaveAs(outname+".png")
c.SaveAs(outname+".pdf")
c.SaveAs(outname+".root")
# c.SaveAs(options.output.replace(".root","")+".pdf")
# c.SaveAs(options.output.replace(".root","")+".C")
sleep(100)
f.Close()


