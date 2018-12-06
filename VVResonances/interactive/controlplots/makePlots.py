import ROOT
import os,sys,optparse
from array import array


ROOT.gStyle.SetOptStat(0)

parser = optparse.OptionParser()
parser.add_option("-i","--infile",dest="infile",help="use this as infile",default='histos_jetProperties.root')
parser.add_option("--histogram",dest="hist",help="name of the histo",default='che')
(options,args) = parser.parse_args()


def getCanvas(w=800,h=800):
    c1 = ROOT.TCanvas("c","",w,h)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.08)
    c1.SetRightMargin(0.08)
    return c1

def getLegend(name,hist,hist2):
    l = ROOT.TLegend(0.55,0.9,0.9,0.7)
    #l.SetTextFont(82)
    l.AddEntry(hist," "+name,"l")
    l.AddEntry(hist2,"weird events "+name,"l")
    return l




if __name__=="__main__":
    infile = ROOT.TFile(options.infile,"READ")
    
    h1 = infile.Get("h"+options.hist)
    h2 = infile.Get("testh"+options.hist)
    
    
    c = getCanvas()
    h1.SetLineColor(ROOT.kBlue)
    h2.SetLineColor(ROOT.kRed)
    h1.Scale(1/h1.Integral())
    h2.Scale(1/h2.Integral())
    h1.SetLineWidth(2)
    h2.SetLineWidth(2)
    h1.Draw("hist")
    h2.Draw("histsame")
    
    l = getLegend(options.hist,h1,h2)
    l.Draw("same")
    c.SaveAs("histo_"+options.hist+".pdf")
