import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import copy

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output ROOT File",default='')
parser.add_option("-i","--infile",dest="infile",help="Input ROOT File",default='')
parser.add_option("--oneD",dest="OneD",help="do 1D smoothing",default='1')
parser.add_option("--threeD",dest="ThreeD",help="do 3D smoothing",default=0)


(options,args) = parser.parse_args()


def smoothTail(proj,hist3D,xbin,ybin):#,xmin,xmax,ymin,ymax):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral() 
    proj.Scale(1.0/scale)
    
    beginFit = proj.GetBinLowEdge( proj.GetMaximumBin() )
    beginFitX = beginFit + 1500. * 1/(beginFit/1000.)
    #beginFitX = beginFit + 800. * 1/(beginFit/1000.)
    print beginFit
    print beginFitX
    #beginFitX=beginFit
   #expo=ROOT.TF1("expo","expo",beginFitX,8000)
    expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000) 
    expo.SetParameters(0,16.,2.)
    expo.SetParLimits(2,1.,20.)
    proj.Fit(expo,"LLMR","",beginFitX,8000)
    #c = ROOT.TCanvas("c","c",400,400)
    #c.SetLogy()
    #proj.Draw("hist")
    #proj.Draw("funcsame")
    #c.SaveAs(proj.GetName()+"_binX"+str(xbin)+"binY"+str(ybin)+".pdf")
    beginsmooth = False
    print proj.GetNbinsX()+1
    for j in range(1,proj.GetNbinsX()+1):
        x=proj.GetXaxis().GetBinCenter(j)
        if x>beginFitX:
            if beginsmooth==False:
               if x<3000: 
                   if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00009:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                    #print beginFitX
                    #print "begin smoothing at " +str(x)
                    beginsmooth = True 
               if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                   #print beginFitX
                   #print "begin smoothing at " +str(x)
                   beginsmooth = True 
            if beginsmooth:
                hist3D.SetBinContent(xbin,ybin,j,expo.Eval(x)*scale)
    return 1


def smoothTail1D(proj):
    if proj.Integral() == 0:
        print "histogram has zero integral "+proj.GetName()
        return 0
    scale = proj.Integral() 
    proj.Scale(1.0/scale)
    
    
    beginFitX = 2100
    expo=ROOT.TF1("expo","[0]*(1-x/13000.)^[1]/(x/13000)^[2]",2000,8000) 
    expo.SetParameters(0,16.,2.)
    expo.SetParLimits(2,1.,20.)
    proj.Fit(expo,"LLMR","",beginFitX,8000)
    c = ROOT.TCanvas("c","c",400,400)
    c.SetLogy()
    proj.Draw("hist")
    proj.Draw("funcsame")
    c.SaveAs(proj.GetName()+".pdf")
    beginsmooth = False
    print proj.GetNbinsX()+1
    for j in range(1,proj.GetNbinsX()+1):
        x=proj.GetXaxis().GetBinCenter(j)
        if x>beginFitX:
            if beginsmooth==False:
               if x<3000: 
                   if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00009:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                    print beginFitX
                    print "begin smoothing at " +str(x)
                    beginsmooth = True 
               if abs(proj.GetBinContent(j) - expo.Eval(x)) < 0.00001:# and abs(expo.Derivative(x)- (hist.GetBinContent(j):
                   print beginFitX
                   print "begin smoothing at " +str(x)
                   beginsmooth = True 
            if beginsmooth:
                proj.SetBinContent(j,expo.Eval(x))
    return 1




def getXbin( xmin,xmax):
    bins = []
    for i in range(xmin,xmax):
        bins.append(xmin + i)
    return bins
    
   
def unequalScale(histo,name,alpha,power=1,dim=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    for i in range(1,histo.GetNbinsX()+1):
	x= histo.GetXaxis().GetBinCenter(i)
	nominal=histo.GetBinContent(i) #ROOT.TMath.Log10(histo.GetBinContent(i))
	factor = 1+alpha*pow(x,power)
	if power == 0: factor = alpha*math.log(x)
	if power == -100: factor = alpha/x + math.log(alpha*10./x)
	print i,x,power,alpha,factor,nominal,nominal*factor,nominal/factor
	newHistoU.SetBinContent(i,nominal*factor)
	if factor != 0: newHistoD.SetBinContent(i,nominal/factor)	
    return newHistoU,newHistoD
   

def addSystematics(infile):
    #alpha=1.5/5000
    #hup,hdown = unequalScale(hist,"histo_PT",alpha)
    #alpha=1.5*1000
    #hup2,hdown2 = unequalScale(hist,"histo_OPT",alpha)
    hup = infile.Get("histo_nominal_PTUp")
    smoothTail1D(hup)
    hdown = infile.Get("histo_nominal_PTDown")
    smoothTail1D(hdown)
    hup2 = infile.Get("histo_nominal_OPTUp")
    smoothTail1D(hup2)
    hdown2 = infile.Get("histo_nominal_OPTDown")
    smoothTail1D(hdown2)
    #infile.Close()
    return [hup,hup2,hdown,hdown2]
    

if __name__=='__main__':
    print options.ThreeD
    
    # try smoothing 3D histogram in each bin ######################################
    if options.ThreeD ==str(1):
        fromkernel =  options.infile
        f2 = ROOT.TFile(fromkernel,"READ")
        
        names = ["histo","histo_PTXYUp","histo_PTXYDown","histo_PTZUp","histo_PTZDown","histo_OPTXYUp","histo_OPTXYDown","histo_OPTZUp", "histo_nominal_OPTDown"]
        histograms = []
        for n in names:
            histograms.append(f2.Get(n))  
    
        nameOutputFile=options.output
        print "make output root file "+nameOutputFile
        output=ROOT.TFile(nameOutputFile,"RECREATE")
    
        for kernelHisto in histograms:
            smoothTail1D(kernelHisto)
            ctest = ROOT.TCanvas("ctest","ctest",400,400)
            ctest.SetLogy()
            kernelHisto.Draw("Ahist")
            ctest.SaveAs("bla.pdf")
            kernelHisto.Scale(1/kernelHisto.Integral())
            kernelHisto.Write()
        output.Close()
    if options.OneD == str(1):
        fromkernel = options.infile
        kernel = ROOT.TFile(fromkernel,"READ")
        histo = kernel.Get("histo_nominal")
        smoothTail1D(histo)
        nameOutputFile=options.output
        print "make output root file "+nameOutputFile
        output=ROOT.TFile(nameOutputFile,"RECREATE")
        histo.Scale(1/histo.Integral())
        histo.Write()
        data = kernel.Get("mvv_nominal")
        data.Scale(1/data.Integral())
        data.Write()
        
        lhist = addSystematics(kernel)
        for lh in lhist:
            lh.Scale(1/lh.Integral())
            lh.Write()
            
        c = ROOT.TCanvas("c","C",400,400)
        histo.Draw("hist")
        data.SetMarkerColor(ROOT.kBlack)
        data.Draw("same")
        for lh in lhist:
            lh.SetLineColor(ROOT.kPink)
            lh.Draw("histsame")
        c.SetLogy()
        c.SaveAs("debug_Vjets_mVV_kernels.png")
        
        
        
