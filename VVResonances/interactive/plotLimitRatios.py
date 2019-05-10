import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output ROOT File",default='')
parser.add_option("-f","--firstfile",dest="firstfile",help="Input ROOT File",default='')
parser.add_option("-s","--secondfile",dest="secondfile",help="Input ROOT File",default='')
parser.add_option("-t","--title",dest="title",help="set title of y axis",default='')


(options,args) = parser.parse_args()


def getLimit(filename):
    f=ROOT.TFile(filename)
    limit=f.Get("limit")
    data={}
    for event in limit:
        #if float(event.mh)<options.minX or float(event.mh)>options.maxX:
        #    continue
        
        #if not (event.mh in data.keys()):
            #data[event.mh]={}


        #if event.quantileExpected<0:            
        #    data[event.mh]['obs']=event.limit
        #if event.quantileExpected>0.02 and event.quantileExpected<0.03:            
        #    data[event.mh]['-2sigma']=event.limit
        #if event.quantileExpected>0.15 and event.quantileExpected<0.17:            
        #    data[event.mh]['-1sigma']=event.limit
        if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
            data[event.mh]=event.limit*0.001
        #if event.quantileExpected>0.83 and event.quantileExpected<0.85:            
        #    data[event.mh]['+1sigma']=event.limit
        #if event.quantileExpected>0.974 and event.quantileExpected<0.976:            
        #    data[event.mh]['+2sigma']=event.limit
    return data

def getCanvas(cname):
 ROOT.gStyle.SetOptStat(0)

 H_ref = 600 
 W_ref = 600 
 W = W_ref
 H  = H_ref
 iPeriod = 0
 # references for T, B, L, R
 T = 0.08*H_ref
 B = 0.15*H_ref 
 L = 0.15*W_ref
 R = 0.04*W_ref
 canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
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
 return canvas
    

if __name__=="__main__":
    
    lim1 = getLimit(options.firstfile)
    lim2 = getLimit(options.secondfile)
    
    c= getCanvas("ratio")
    g= ROOT.TGraph(1)
    i=0
    for m in lim1.keys():
        for m2 in lim2.keys():
            if m!=m2:
                continue
            g.SetPoint(i,m,lim1[m]/lim2[m])
            print "mass "+str(m)+"lim 1 "+str(lim1[m])+" lim 2 "+str(lim2[m])
            #print str(m)+" "+str(1-lim1[m]/lim2[m])
            i+=1
    g.SetMarkerStyle(20)
    g.GetXaxis().SetTitle("M_{VV}")
    g.GetYaxis().SetTitleOffset(1.8)
    g.GetYaxis().SetTitle(options.firstfile.replace(".root","")+"/"+options.secondfile.replace(".root",""))
    if options.title!="":
        g.GetYaxis().SetTitle(options.title)
    #g.SetMarkerSize(2)
    g.Draw("AP")
    c.SaveAs("limit_ratio.pdf")
    c.SaveAs("limit_ratio.png")
