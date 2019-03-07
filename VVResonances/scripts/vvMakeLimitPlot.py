#!/usr/bin/env python

import ROOT
import optparse
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='limitPlot',help="Limit plot")
parser.add_option("-s","--signal",dest="sig",type=str,help="Signal sample",default='BulkGWW')
parser.add_option("--sigscale",dest="sigscale",type=float,help="maximum y",default=0.001)
parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1000.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=5000.0)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.00001)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=1)
parser.add_option("-b","--blind",dest="blind",type=int,help="Not do observed ",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="Log plot",default=1)

parser.add_option("-t","--titleX",dest="titleX",default='M_{X} [GeV]',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default='#sigma x BR(X #rightarrow WW) [pb]  ',help="title of y axis")

parser.add_option("-p","--period",dest="period",default='2017',help="period")
parser.add_option("-f","--final",dest="final",type=int, default=1,help="Preliminary or not")

#    parser.add_option("-x","--minMVV",dest="minMVV",type=float,help="minimum MVV",default=1000.0)
#    parser.add_option("-X","--maxMVV",dest="maxMVV",type=float,help="maximum MVV",default=13000.0)

(options,args) = parser.parse_args()
#define output dictionary

setTDRStyle()


f=ROOT.TFile(args[0])
limit=f.Get("limit")
data={}

def rescaleaxis(g,scale=1000.):
    N = g.GetN()
    x = g.GetX()
    for i in range(N):
        x[i] *= scale
    g.GetHistogram().Delete()
    g.SetHistogram(0)
    return
    
for event in limit:
    if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        continue
    if not (event.mh in data.keys()):
        data[event.mh]={}

    lim = event.limit*options.sigscale
    if event.quantileExpected<0:            
        data[event.mh]['obs']=lim
    if event.quantileExpected>0.02 and event.quantileExpected<0.03:            
        data[event.mh]['-2sigma']=lim
    if event.quantileExpected>0.15 and event.quantileExpected<0.17:            
        data[event.mh]['-1sigma']=lim
    if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
        data[event.mh]['exp']=lim
    if event.quantileExpected>0.83 and event.quantileExpected<0.85:            
        data[event.mh]['+1sigma']=lim
    if event.quantileExpected>0.974 and event.quantileExpected<0.976:            
        data[event.mh]['+2sigma']=lim

mean=ROOT.TGraphAsymmErrors()
mean.SetName("mean")

band68=ROOT.TGraphAsymmErrors()
band68.SetName("band68")
band95=ROOT.TGraphAsymmErrors()
band95.SetName("band95")
bandObs=ROOT.TGraph()
bandObs.SetName("bandObs")

line_plus1=ROOT.TGraph()
line_plus1.SetName("line_plus1")

line_plus2=ROOT.TGraph()
line_plus2.SetName("line_plus2")

line_minus1=ROOT.TGraph()
line_minus1.SetName("line_minus1")

line_minus2=ROOT.TGraph()
line_minus2.SetName("line_minus2")



N=0
for mass,info in data.iteritems():
    print 'Setting mass',mass,info

    if not ('exp' in info.keys() and '+1sigma' in info.keys() and '+2sigma' in info.keys() and '-1sigma' in info.keys() and '-2sigma' in info.keys()):
        print 'Incomplete file'
        continue
    if options.blind==0 and not ('obs' in info.keys()):
        print 'Incomplete file'
        continue    
    
    mean.SetPoint(N,mass,info['exp'])    
    band68.SetPoint(N,mass,info['exp'])
    band95.SetPoint(N,mass,info['exp'])
    line_plus1.SetPoint(N,mass,info['+1sigma'])
    line_plus2.SetPoint(N,mass,info['+2sigma'])
    line_minus1.SetPoint(N,mass,info['-1sigma'])
    line_minus2.SetPoint(N,mass,info['-2sigma'])

    if options.blind==0: bandObs.SetPoint(N,mass,info['obs'])
    band68.SetPointError(N,0.0,0.0,info['exp']-info['-1sigma'],info['+1sigma']-info['exp'])
    band95.SetPointError(N,0.0,0.0,info['exp']-info['-2sigma'],info['+2sigma']-info['exp'])
    N=N+1


mean.Sort()
band68.Sort()
band95.Sort()
if options.blind==0: bandObs.Sort()
line_plus1.Sort()    
line_plus2.Sort()    
line_minus1.Sort()    
line_minus2.Sort()    




band68.SetFillColor(ROOT.kGreen+1)
band68.SetLineWidth(3)
band68.SetLineColor(ROOT.kWhite)
band68.SetLineStyle(0)
band68.SetMarkerStyle(0)

band95.SetFillColor(ROOT.kOrange)
band95.SetLineColor(ROOT.kWhite)


bandObs.SetLineWidth(3)
bandObs.SetLineColor(ROOT.kBlack)
bandObs.SetMarkerStyle(20)

mean.SetLineWidth(2)
mean.SetLineColor(ROOT.kBlack)
mean.SetLineStyle(2)

line_plus1.SetLineWidth(1)
line_plus1.SetLineColor(ROOT.kGreen+1)

line_plus2.SetLineWidth(1)
line_plus2.SetLineColor(ROOT.kOrange-2)

line_minus1.SetLineWidth(1)
line_minus1.SetLineColor(ROOT.kGreen+1)

line_minus2.SetLineWidth(1)
line_minus2.SetLineColor(ROOT.kOrange-2)

gtheory = ROOT.TGraphErrors(1)
gtheory.SetLineColor(ROOT.kRed)
gtheory.SetLineWidth(3)
gtheoryUP = ROOT.TGraphErrors(1)
gtheoryUP.SetLineColor(ROOT.kRed-2)
gtheoryUP.SetLineWidth(3)
gtheoryDOWN = ROOT.TGraphErrors(1)
gtheoryDOWN.SetLineColor(ROOT.kRed-2)
gtheoryDOWN.SetLineWidth(3)
gtheorySHADE = ROOT.TGraphErrors(1)
gtheorySHADE.SetLineColor(ROOT.kRed-2)
gtheorySHADE.SetLineWidth(3)


filenameTH = "$CMSSW_BASE/src/CMGTools/VVResonances/scripts/theoryXsec/%s.root"%options.sig
thFile       = ROOT.TFile.Open(filenameTH,'READ')   
print "Opening file " ,thFile.GetName()
gtheory      = thFile.Get("gtheory")
gtheoryUP    = thFile.Get("gtheoryUP")
gtheoryDOWN  = thFile.Get("gtheoryDOWN")
gtheorySHADE = thFile.Get("grshade")
rescaleaxis(gtheory     )
rescaleaxis(gtheoryUP   )
rescaleaxis(gtheoryDOWN )
rescaleaxis(gtheorySHADE)




gtheory     .SetName("%s_gtheory"    %options.sig)
gtheoryUP   .SetName("%s_gtheoryUP"  %options.sig)
gtheoryDOWN .SetName("%s_gtheoryDOWN"%options.sig)
gtheorySHADE.SetName("%s_grshade"    %options.sig)
gtheorySHADE.SetLineColor(0)
gtheoryUP.SetLineColor(ROOT.kRed)
gtheoryDOWN.SetLineColor(ROOT.kRed)
gtheoryUP.SetLineWidth(1)
gtheoryDOWN.SetLineWidth(1)
# thFile.Close()

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
# c.SetGrid()
c.SetLogy()
c.cd()



frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
frame.GetXaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetTitleSize(0.05)
frame.SetMinimum(5e-5)
frame.SetMaximum(0.1)


if "Wprime"  in options.sig: 
  ltheory="#sigma_{TH}#timesBR(W'#rightarrowWZ) HVT_{B}"
  ytitle ="#sigma x BR(W' #rightarrow WZ) [pb]  "
  xtitle = "M_{W'} [GeV]"
  frame.SetMinimum(9e-5)
  frame.SetMaximum(0.5)
if "BulkGWW" in options.sig: 
  ltheory="#sigma_{TH}#timesBR(G_{Bulk}#rightarrowWW) #tilde{k}=0.5"
  ytitle ="#sigma x BR(G_{Bulk} #rightarrow WW) [pb]  "
  xtitle = "M_{G_{Bulk}} [GeV]"
if "BulkGZZ" in options.sig: 
  ltheory="#sigma_{TH}#timesBR(G_{Bulk}#rightarrowZZ) #tilde{k}=0.5"  
  ytitle ="#sigma x BR(G_{Bulk} #rightarrow ZZ) [pb]  "
  xtitle = "M_{G_{Bulk}} [GeV]"
if "Zprime"  in options.sig: 
  ltheory="#sigma_{TH}#timesBR(Z'#rightarrowWW) HVT_{B}"
  ytitle ="#sigma x BR(Z' #rightarrow WW) [pb]  "
  xtitle = "M_{Z'} [GeV]"
  frame.SetMinimum(7e-5)
  frame.SetMaximum(0.5)

frame.GetXaxis().SetTitle(xtitle)
frame.GetYaxis().SetTitle(ytitle)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)

frame.Draw()
band95.Draw("3same")
band68.Draw("3same")
# band68.Draw("XLsame")
line_plus1.Draw("Lsame")
line_plus2.Draw("Lsame")
line_minus1.Draw("Lsame")
line_minus2.Draw("Lsame")
mean.Draw("Lsame")
gtheory.Draw("Lsame")
gtheorySHADE.Draw("Fsame")

c.SetLogy(options.log)
c.Draw()



leg  = ROOT.TLegend(0.498995,0.6602591,0.9446734,0.9011917)
leg2 = ROOT.TLegend(0.498995,0.6602591,0.9446734,0.9011917)
leg.SetTextSize(0.028)
leg.SetLineColor(1)
leg.SetShadowColor(0)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(ROOT.kWhite)
# leg.SetFillStyle(0)
leg.SetMargin(0.35)
leg2.SetTextSize(0.028)
leg2.SetLineColor(1)
leg2.SetShadowColor(0)
leg2.SetLineStyle(1)
leg2.SetLineWidth(1)
leg2.SetFillColor(0)
leg2.SetFillStyle(0)
leg2.SetMargin(0.35)
leg.SetBorderSize(1)

if options.blind==0: leg.AddEntry(bandObs, "Observed", "Lp")
leg.AddEntry(band68, "Expected #pm 1 std. deviation", "f")
leg.AddEntry(band95 , "Expected #pm 2 std. deviation", "f")
leg.AddEntry(gtheory, ltheory, "L")

if not options.blind: leg2.AddEntry(bandObs, " ", "")
leg2.AddEntry(mean, " ", "L")
leg2.AddEntry(mean, " ", "L")
leg2.AddEntry(gtheory, " ", "")      
      




if options.final==1:
    cmslabel_final(c,options.period,11)
else:
    cmslabel_prelim(c,options.period,11)
leg.Draw()
leg2.Draw()
c.Update()
c.RedrawAxis()

if options.blind==0:
    bandObs.Draw("PLsame")
if options.final==1:
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017.png")    
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017.pdf") 
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017.C")
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017.root")
else:
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017_prelim.png")    
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017_prelim.pdf") 
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017_prelim.C")
    c.SaveAs("limits_"+options.sig+"_combo_2016_2017_prelim.root")

fout=ROOT.TFile(options.output+options.sig+".root","RECREATE")
fout.cd()
c.Write()
band68.Write()
band95.Write()
bandObs.Write()
line_plus1.Write()    
line_plus2.Write()    
line_minus1.Write()    
line_minus2.Write()    

fout.Close()
f.Close()

masses = data.keys()
for mass in sorted(masses):
    print mass
