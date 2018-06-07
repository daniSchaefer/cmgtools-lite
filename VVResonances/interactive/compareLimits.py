#!/usr/bin/env python

import ROOT
import optparse
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from time import sleep
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='limit_compare.root',help="Limit plot")

parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=838.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=5200.)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.0001)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=1.4)
parser.add_option("-b","--blind",dest="blind",type=int,help="Not do observed ",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="Log plot",default=1)

parser.add_option("-t","--titleX",dest="titleX",default='M_{X} (GeV)',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default="#sigma x BR(W' #rightarrow WZ) (pb)  ",help="title of y axis")

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
  
title = ["3D HPLP","3D HPLP DDT","3D HPHP","3D HPHP+HPLP","B2G-17-001"]
files = ["Limits_BulkGWW_HPLP_13TeV.root","Limits_BulkGWW_HPLP_13TeV_ddt.root","Limits_BulkGWW_HPHP_13TeV.root","Limits_BulkGWW_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGWW_13TeV.root"]

title = ["3D HPHP","3D HPHP DDT"]
files = ["Limits_BulkGWW_HPHP_13TeV.root","Limits_BulkGWW_HPHP_13TeV_ddt.root"]

title = ["Expected 2017","B2G-17-001"]
files = ["HPLP_noOPTPT2/Limits2.root","limits_b2g17001/Limits_b2g17001_WZ_13TeV.root"]

# title = ["Nominal","p_{T}/m_{VV}>0.4"]
# files = ["LIMITS_NOM/Limits_BulkGWW_HPHP_13TeV.root","LIMITS_VCUT/Limits_BulkGWW_HPHP_13TeV.root"]

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
		if fname.find("b2g17001")!=-1:lim = event.limit*0.01/(0.6991*0.6760)
		if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
		    data[event.mh]['exp']=lim
		
		
		
	line_plus1=ROOT.TGraph()
	line_plus1.SetName(f.GetName().replace(".root",""))



	N=0
	for mass,info in data.iteritems():
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

frame.GetYaxis().SetTitle(options.titleY)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)





c.cd()
frame.Draw()
cols  = [42,46,49,1]*3
tline = [10,9,1,2]*3
for i,g in enumerate(tgraphs):
	g.SetLineStyle(tline[i])
	g.SetLineColor(cols[i])
	g.SetLineWidth(2)
	g.Draw("Lsame")

c.SetLogy(options.log)
c.Draw()
leg.Draw("same")
cmslabel_prelim(c,options.period,11)

c.Update()
c.RedrawAxis()

c.SaveAs("Limits_HPHPHPHL_trigW.png")
# c.SaveAs(options.output.replace(".root","")+".pdf")
# c.SaveAs(options.output.replace(".root","")+".C")
sleep(100)
f.Close()


