
#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=1)
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("--fitResults",dest="fitResults",default="debug_JJ_BulkGWW_MJl1_HPLP.json.root",help="name of root file containing the fitted curves for each parameter")

(options,args) = parser.parse_args()
#define output dictionary

samples={}

title = "M_{JJ}"







def getVal(mass,param,File):
    f = File.Get(param+"_func")
    val = f.Eval(mass)
    return val


def getValues(mass,params,File):
    val = {}
    for p in params:
        val[p] = getVal(mass,p,File)
    return val

def setPDF(vals,variabletype, sampletype, doExp, Fitter):
    if variabletype.find("l1")!=-1 or variabletype.find("l2")!=-1:
        print "make mjet plots "
        #fitter=Fitter(['x'])
        if doExp==1:
            #if sampletype.find("Wprime")!=-1:
            #    Fitter.jetDoublePeakZ('model','x')
            #else:
                Fitter.jetResonance('model','x')
        else:
            #if sampletype.find("Wprime")!=-1:
            #    print "fit double peak "
            #   Fitter.jetDoublePeakZ('model','x')
            #else:
                Fitter.jetResonanceNOEXP('model','x')
    else:
        print "make mVV plots "
        Fitter.signalResonanceCBGaus('model','MVV',mass)
        Fitter.w.var("MH").setVal(mass)
    for v in vals.keys():
            print "set vars " +v +" to "+str(vals[v])
            Fitter.w.var(v).setVal(vals[v])
            Fitter.w.var(v).setConstant(1)
        

def beautifyPull(gpre,title):
    gpre.SetTitle("")
    if title.find("jet")!=-1:
        gpre.GetXaxis().SetRangeUser(55,215)
    gpre.GetXaxis().SetTitle(title)
    gpre.GetYaxis().SetTitle("pull")
    gpre.GetYaxis().SetTitleSize(0.15)
    gpre.GetYaxis().SetTitleOffset(0.2)
    gpre.GetXaxis().SetTitleSize(0.15)
    gpre.GetXaxis().SetTitleOffset(0.7)
    gpre.GetXaxis().SetLabelSize(0.15)
    gpre.GetYaxis().SetLabelSize(0.15)
    gpre.GetXaxis().SetNdivisions(6)
    gpre.GetYaxis().SetNdivisions(4)
    gpre.SetMaximum(5)
    gpre.SetMinimum(-5)
    return gpre


def printHistContent(histo,pullDist):
    for b in range(1,histo.GetNbinsX()):
        i = histo.GetBinCenter(b)
        #fitters[N].w.var("x").setVal(i)
        print str(i)+" "+str(round(histo.GetBinContent(b),4))+ "  "+str(round(pullDist.Eval(i),4))


def truncate(binning,mmin,mmax):
    res=[]
    for b in binning:
        if b >= mmin and b <= mmax:
            res.append(b)
            print b
    return res
    

if __name__=="__main__":
    x=1100
    y=1000
    if options.mvv.find("l1")!=-1 or options.mvv.find("l2")!=-1:
        title="m_{jet}"
        x= options.mini + 50
    shapes = ["mean","sigma","alpha","n","f","slope","alpha2","n2"]
    xvar = 'x'
    #if options.sample.find("Wprime")!=-1:
    #    shapes = ['meanW','sigmaW','alphaW','n','f','alphaW2','meanZ','sigmaZ','alphaZ','alphaZ2']
        
    if options.mvv.find("LV_mass")!=-1:
        shapes = ["MEAN","SIGMA","ALPHA","N","SCALESIGMA","f"]
        xvar ="MVV"

    for filename in os.listdir(args[0]):
        if not (filename.find(options.sample)!=-1):
            continue

    #found sample. get the mass
        fnameParts=filename.split('.')
        fname=fnameParts[0]
        ext=fnameParts[1]
        if ext.find("root") ==-1:
            continue

        mass = float(fname.split('_')[-1])
        if mass < options.minMX or mass > options.maxMX: continue	

            

        samples[mass] = fname

        print 'found',filename,'mass',str(mass) 

    leg = options.mvv.split('_')[1]

    #Now we have the samples: Sort the masses and make histograms
    c = ROOT.TCanvas("c","c",2000,1600)
    c.Divide(4,3)
    h={}
    fitters=[]
    frames=[]
    N=0
    File = ROOT.TFile(options.fitResults,"READ")
    for mass in sorted(samples.keys()):
        if options.mvv.find("LV_mass")!=-1:
            x = mass*1.1
        values =  getValues(mass,shapes,File)
        print 'make histos ',str(mass) 
        plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
        plotter.addCorrectionFactor('genWeight','tree')
        plotter.addCorrectionFactor('puWeight','tree')
        if options.mvv.find("LV_mass")!=-1:
            binning=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337,4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808]
            truncatedbinning = truncate(binning,mass*0.75,mass*1.25)
            #truncatedbinning = binning
            histo = plotter.drawTH1Binned(options.mvv,options.cut+"*(jj_LV_mass>%f&&jj_LV_mass<%f)"%(0.75*mass,1.25*mass),"1",array("d",truncatedbinning))
            #histo = plotter.drawTH1(options.mvv,options.cut,"1",60,mass*0.75,mass*1.25)
            #histo = plotter.drawTH1Binned(options.mvv,options.cut,"1",array("d",binning))
        else:
            histo = plotter.drawTH1(options.mvv,options.cut,"1",40,options.mini,options.maxi)
        #for b in range(1,histo.GetNbinsX()):
           #if histo.GetBinContent(b) < 1:
               #histo.SetBinContent(b,0)
        c.cd(N+1)
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0.01)
        pad1.Draw()                                                                                       
        pad1.cd()
        #print "draw mass "+str(mass)
        #histo.SetTitle(str(mass))
        #histo.Draw()
        #histo2.Draw("same")
        fitters.append(Fitter([xvar])) 
        if options.mvv.find("LV_mass")!=-1:
            frames.append(fitters[N].w.var(xvar).frame(mass*0.75,mass*1.25))
        else:
            frames.append(fitters[N].w.var(xvar).frame(55,215))
        setPDF(values,options.mvv, options.sample, options.doExp, fitters[N])
        fitters[N].importBinnedData(histo,[xvar],'data')
        res =  fitters[N].getFrame("model","data",xvar,title,mass)
        #res[0].SetAxisRange(150,200,"X")
        res[0].Draw()
        chi2 = ROOT.TLatex()
        y = histo.GetBinContent(histo.GetMaximumBin())*2/3.
        chi2.DrawLatex(x,y,"#chi^{2} = "+str(round(res[3],2)))
        c.cd(N+1)
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0.1)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.SetGridx()
        pad2.Draw()
        pad2.cd()
        if options.mvv.find("LV_mass")!=-1:
            res[2].GetXaxis().SetRangeUser(mass*0.75,mass*1.25)
        beautifyPull(res[2],title).Draw()
        #if mass!=4500:
        #    printHistContent(histo,res[2])
        N+=1
    fname = options.fitResults.replace(".root",".pdf")
    if options.mvv.find("l2")!=-1 and fname.find("l1")!=-1:
        fname = fname.replace("l1","l2")
    c.SaveAs(fname)
