import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import copy

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output folder name",default='')
parser.add_option("-n","--name",dest="name",help="Input ROOT File name",default='/home/dschaefer/DiBoson3D/test_kernelSmoothing_pythia/workspace_pythia_nominal.root')
parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
parser.add_option("-p","--projection",dest="projection",help="choose which projection should be done",default="z")
parser.add_option("-f","--postfit",dest="postfit",action="store_true",help="make also postfit plots",default=False)
parser.add_option("-l","--label",dest="label",help="add extra label such as pythia or herwig",default="")
parser.add_option("--log",dest="log",help="write fit result to log file",default="")
parser.add_option("--pdf",dest="pdf",help="name of pdfs lie PTZUp etc",default="nonResNominal_JJ_HPHP_13TeV,nonRes_PTZDown_JJ_HPHP_13TeV,nonRes_OPTZUp_JJ_HPHP_13TeV,nonRes_PTZUp_JJ_HPHP_13TeV,nonRes_OPTZDown_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV")

#pt2Sys
#nonResNominal_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV,nonRes_OPT2Up_JJ_HPHP_13TeV,nonRes_OPT2Down_JJ_HPHP_13TeV,nonRes_PT2Up_JJ_HPHP_13TeV,nonRes_PT2Down_JJ_HPHP_13TeV

#ptSys 

#nonResNominal_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTZDown_JJ_HPHP_13TeV,nonRes_OPTZUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTZDown_JJ_HPHP_13TeV,nonRes_PTZUp_JJ_HPHP_13TeV




(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
colors = [ROOT.kBlack,ROOT.kRed-2,ROOT.kRed+1,ROOT.kRed-1,ROOT.kRed+2,ROOT.kGreen-1,ROOT.kGreen-2,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kBlue]

def getListFromRange(xyzrange):
    r=[]
    a,b = xyzrange.split(",")
    r.append(float(a))
    r.append(float(b))
    return r


def getListOfBins(hist,dim):
    axis =0
    N = 0
    if dim =="x":
        axis= hist.GetXaxis()
        N = hist.GetNbinsX()
    if dim =="y":
        axis = hist.GetYaxis()
        N = hist.GetNbinsY()
    if dim =="z":
        axis = hist.GetZaxis()
        N = hist.GetNbinsZ()
    if axis==0:
        return {}
    
    mmin = axis.GetXmin()
    mmax = axis.GetXmax()
    r ={}
    for i in range(1,N+1):
        #v = mmin + i * (mmax-mmin)/float(N)
        r[i] = axis.GetBinCenter(i) 
    return r   


def getListOfBinsLowEdge(hist,dim):
    axis =0
    N = 0
    if dim =="x":
        axis= hist.GetXaxis()
        N = hist.GetNbinsX()
    if dim =="y":
        axis = hist.GetYaxis()
        N = hist.GetNbinsY()
    if dim =="z":
        axis = hist.GetZaxis()
        N = hist.GetNbinsZ()
    if axis==0:
        return {}
    
    mmin = axis.GetXmin()
    mmax = axis.GetXmax()
    r=[]
    for i in range(1,N+2):
        #v = mmin + i * (mmax-mmin)/float(N)
        r.append(axis.GetBinLowEdge(i)) 
    return array("d",r)


def getListOfBinsWidth(hist,dim):
    axis =0
    N = 0
    if dim =="x":
        axis= hist.GetXaxis()
        N = hist.GetNbinsX()
    if dim =="y":
        axis = hist.GetYaxis()
        N = hist.GetNbinsY()
    if dim =="z":
        axis = hist.GetZaxis()
        N = hist.GetNbinsZ()
    if axis==0:
        return {}
    
    mmin = axis.GetXmin()
    mmax = axis.GetXmax()
    r ={}
    for i in range(0,N+2):
        #v = mmin + i * (mmax-mmin)/float(N)
        r[i] = axis.GetBinWidth(i) 
    return r 

    
def reduceBinsToRange(Bins,r):
    if r[0]==0 and r[1]==-1:
        return Bins
    result ={}
    for key, value in Bins.iteritems():
        if value >= r[0] and value <=r[1]:
            result[key]=value
    return result


def getMV(binnumber):
    i=0
    for xk, xv in xBins_redux.iteritems():
         for yk, yv in yBins_redux.iteritems():
             for zk,zv in zBins_redux.iteritems():
                 if i==binnumber:
                     return [xv,yv,zv]
                 i+=1
    

def getChi2(pdf,data,norm):
    pr=[]
    dr=[]
    error_dr=[]
    testbins = []
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 dr.append(data.weight(argset))
                 error_dr.append(ROOT.TMath.Sqrt(data.weight(argset)))
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 pr.append( pdf.getVal(argset)*binV*norm)
                 #print zv
    ndof = 0
    chi2 = 0
    #print bins
    for i in range(0,len(pr)):
        if dr[i] < 0.1e-10:
            #print i
            continue
        #if ROOT.TMath.Abs(dr[i] - pr[i]) > 100:
            #print " I " +str(i) + " " + str(dr[i] - pr[i])+" bins  "
            #print "data  "+str(dr[i])
            #print "pdf  "+str(pr[i])
            #print "bins " +str(getMV(i))
        ndof+=1
        chi2+= pow((dr[i] - pr[i]),2)/pow(error_dr[i],2)
    return [chi2,ndof]




def doZprojection(pdfs,data,norm,proj=0):
    postfit=False
    for p in pdfs:
        if p.GetName().find("postfit")!=-1:
            postfit = True
            break
    # do some z projections
    h=[]
    lv=[]
    dh = ROOT.TH1F("dh","dh",len(zBinslowedge)-1,zBinslowedge)
    for p in pdfs:
        h.append( ROOT.TH1F("h_"+p.GetName(),"h_"+p.GetName(),len(zBinslowedge)-1,zBinslowedge))
        lv.append({})
    for i in range(0,len(pdfs)):
        for zk,zv in zBins_redux.iteritems():
            lv[i][zv]=0    
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 dh.Fill(zv,data.weight(argset))
                 i=0
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][zv] += p.weight(argset)#p.evaluate()*binV
                    else:
                            lv[i][zv] += p.getVal(argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for zk,zv in zBins_redux.iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(zv,lv[i][zv])
            else:
                h[i].Fill(zv,lv[i][zv]*norm)
            #h[i].Fill(zv,lv[i][zv])
    leg = ROOT.TLegend(0.88,0.65,0.7,0.88)
    c = ROOT.TCanvas("c","c",800,400)
    if postfit:
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()    
    c.SetLogy()
    h[0].SetLineColor(colors[0])
    h[0].SetTitle("Z-Proj. x : "+options.xrange+" y : "+options.yrange)
    h[0].GetXaxis().SetTitle("m_{jj}")
    #h[0].SetMaximum(1e6)
    h[0].GetYaxis().SetTitleOffset(1.3)
    h[0].GetYaxis().SetTitle("events")
    #h[0].Scale(n)#/h[0].Integral())
    if postfit:
        h[0].GetYaxis().SetTitleOffset(0.6)
        h[0].GetYaxis().SetTitle("events")
        h[0].GetYaxis().SetTitleSize(0.06)
        h[0].GetYaxis().SetLabelSize(0.06)
        h[0].GetYaxis().SetNdivisions(5)
    h[0].Draw("hist")
    dh.SetBinErrorOption(ROOT.TH1.kPoisson)
    dh.SetMarkerStyle(1)
    dh.Draw("same")
    leg.AddEntry(dh,"data","lp")
    if proj!=0:    
        #proj.Scale(n/proj.Integral())
        proj.SetMarkerStyle(1)
        proj.Draw("same")
        leg.AddEntry(proj,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        #h[i].Scale(n)#/h[i].Integral())
        h[i].SetLineColor(colors[i])
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    
    leg.SetLineColor(0)
    leg.Draw("same")
    if postfit:
        ktest0 = h[0].KolmogorovTest(dh,"DX")
        ktest1 = h[1].KolmogorovTest(dh,"DX")
        print "chi2 test :" 
        print ktest0
        print ktest1
        latex = ROOT.TLatex()
        latex.DrawLatex(2000,100,"kolmogorov test "+str(ktest0))
        latex.DrawLatex(2000,10,"kolmogorov test "+str(ktest1))
        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
        pad2.SetTopMargin(0.1)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        graphs = addPullPlot(dh,h[0],h[1])
        graphs[0].Draw("AP")
        graphs[1].Draw("P")
        line1 = ROOT.TLine()
        line1.SetLineStyle(3)
        x = dh.GetXaxis().GetBinLowEdge(1)
        X = dh.GetXaxis().GetBinUpEdge(dh.GetNbinsX())
        line1.DrawLine(x,2,X,2)
        line1.DrawLine(x,-2,X,-2)
        c.SaveAs(options.output+"PostFit"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+".png")
        c.SaveAs(options.output+"PostFit"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+".pdf")
    else:    
        c.SaveAs(options.output+"Zproj"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+".png")
        c.SaveAs(options.output+"Zproj"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+".pdf")


def doXprojection(pdfs,data,norm,hin=0):
    postfit=False
    for p in pdfs:
        if p.GetName().find("postfit")!=-1:
            postfit = True
            break
    print zBins_redux
    print yBins_redux
    h=[]
    lv=[]
    proj = ROOT.TH1F("px","px",len(xBinslowedge)-1,xBinslowedge)
    for p in pdfs:
        h.append( ROOT.TH1F("hx_"+p.GetName(),"hx_"+p.GetName(),len(xBinslowedge)-1,xBinslowedge))
        lv.append({})
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for i in range(0,len(pdfs)):
            lv[i][xv]=0
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 #print zv
                 i=0
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 proj.Fill(xv,data.weight(argset))
                 for p in pdfs:
                     if "postfit" in p.GetName():
                         #test = p.createProjection(argset).getVal(argset)
                         #lv[i][xv] += test*binV
                         #print test
                         if "data" in p.GetName():
                            lv[i][xv] += p.weight(argset)#p.evaluate()*binV
                         else:
                             lv[i][xv] += p.evaluate()*binV
                         #lv[i][xv] += p.expectedEvents(argset)*binV
                         #print p.expectedEvents(argset)*binV
                         #print "evalueate "+str( lv[i][xv])
                         #print "getVal "+str(p.getVal(argset)*binV)
                     else:
                        lv[i][xv] += p.getVal(argset)*binV
                     i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)
    leg = ROOT.TLegend(0.88,0.65,0.77,0.89)
    c = ROOT.TCanvas("c","c",800,400)
    if postfit:
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
        pad1.SetBottomMargin(0.01)
        pad1.Draw()
        pad1.cd()    
    h[0].SetLineColor(colors[0])
    h[0].SetTitle("X-Proj. y : "+options.yrange+" z : "+options.zrange)
    h[0].GetXaxis().SetTitle("m_{jet1}")
    h[0].GetYaxis().SetTitleOffset(1.3)
    h[0].GetYaxis().SetTitle("events")
    if postfit:
        h[0].GetYaxis().SetTitleOffset(0.6)
        h[0].GetYaxis().SetTitle("events")
        h[0].GetYaxis().SetTitleSize(0.06)
        h[0].GetYaxis().SetLabelSize(0.06)
        h[0].GetYaxis().SetNdivisions(5)
    #print "integral "+str(h[0].Integral())
    #s = h[0].Integral()/h[1].Integral()
    #h[0].Scale(n)#/h[0].Integral())
    #print "integral 1 "+str(h[1].Integral())
    h[0].Draw("hist")
    leg.AddEntry(proj,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        h[i].SetLineColor(colors[i])
        #h[i].Scale(n)
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    if hin!=0:    
        #hin.Scale(n/hin.Integral())
        hin.SetMarkerStyle(1)
        hin.Draw("same")
    proj.SetMarkerStyle(1)
    proj.Draw("same")
    leg.SetLineColor(0)
    leg.Draw("same")
    if postfit:
        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
        pad2.SetTopMargin(0.1)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        graphs = addPullPlot(proj,h[0],h[1])
        graphs[0].Draw("AP")
        graphs[1].Draw("P")
        line1 = ROOT.TLine()
        line1.SetLineStyle(3)
        x = proj.GetXaxis().GetBinLowEdge(1)
        X = proj.GetXaxis().GetBinUpEdge(proj.GetNbinsX())
        line1.DrawLine(x,2,X,2)
        line1.DrawLine(x,-2,X,-2)
        c.SaveAs(options.output+"PostFit"+options.label+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".png") 
        c.SaveAs(options.output+"PostFit"+options.label+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".pdf") 
    else:    
        c.SaveAs(options.output+"Xproj"+options.label+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".png")   
        c.SaveAs(options.output+"Xproj"+options.label+"_y"+(options.yrange.split(","))[0]+"To"+(options.yrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".pdf")   
    

def doYprojection(pdfs,data,norm):
    postfit=False
    for p in pdfs:
        if p.GetName().find("postfit")!=-1:
            postfit = True
            break
    h=[]
    lv=[]
    proj = ROOT.TH1F("py","py",len(yBinslowedge)-1,yBinslowedge)
    for p in pdfs:
        h.append( ROOT.TH1F("hy_"+p.GetName(),"hy_"+p.GetName(),len(yBinslowedge)-1,yBinslowedge))
        lv.append({})
    for yk, yv in yBins_redux.iteritems():
         MJ2.setVal(yv)
         for i in range(0,len(pdfs)):
            lv[i][yv]=0
         for xk, xv in xBins_redux.iteritems():
             MJ1.setVal(xv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 i=0
                 proj.Fill(yv,data.weight(argset))
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][yv] += p.weight(argset)#p.evaluate()*binV
                    else:
                            #lv[i][xv] += p.evaluate()*binV 
                            lv[i][yv] += p.getVal(argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)
            #h[i].Fill(key,value)
    leg = ROOT.TLegend(0.88,0.65,0.77,0.89)
    c = ROOT.TCanvas("c","c",800,400)
    if postfit:
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
        pad1.SetBottomMargin(0.01)
        pad1.Draw()
        pad1.cd()               
    h[0].SetLineColor(colors[0])
    h[0].SetTitle("Y-Proj. x : "+options.xrange+" z : "+options.zrange)
    h[0].GetXaxis().SetTitle("m_{jet2}")
    h[0].GetYaxis().SetTitleOffset(1.3)
    h[0].GetYaxis().SetTitle("events")
    if postfit:
        h[0].GetYaxis().SetTitleOffset(0.6)
        h[0].GetYaxis().SetTitle("events")
        h[0].GetYaxis().SetTitleSize(0.06)
        h[0].GetYaxis().SetLabelSize(0.06)
        h[0].GetYaxis().SetNdivisions(5)
    #h[0].Scale(n)#/h[0].Integral())
    h[0].Draw("hist")
    leg.AddEntry(proj,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        h[i].SetLineColor(colors[i])
        #h[i].Scale(n)#/h[i].Integral())
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    proj.SetMarkerStyle(1)
    leg.SetLineColor(0)
    leg.Draw("same")
    #proj.Scale(n)#/proj.Integral())
    proj.Draw("same")
    if postfit:
        ktest0 = h[0].KolmogorovTest(proj,"DX")
        ktest1 = h[1].KolmogorovTest(proj,"DX")
        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
        pad2.SetTopMargin(0.1)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        graphs = addPullPlot(proj,h[0],h[1])
        graphs[0].Draw("AP")
        graphs[1].Draw("P")
        line1 = ROOT.TLine()
        line1.SetLineStyle(3)
        x = proj.GetXaxis().GetBinLowEdge(1)
        X = proj.GetXaxis().GetBinUpEdge(proj.GetNbinsX())
        line1.DrawLine(x,2,X,2)
        line1.DrawLine(x,-2,X,-2)
        c.SaveAs(options.output+"PostFit"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".png")
        c.SaveAs(options.output+"PostFit"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".pdf")
    else:
        c.SaveAs(options.output+"Yproj"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".png")  
        c.SaveAs(options.output+"Yproj"+options.label+"_x"+(options.xrange.split(","))[0]+"To"+(options.xrange.split(","))[1]+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".pdf") 
 

def addPullPlot(hdata,hprefit,hpostfit):
    print "make pull plots: (data-fit)/sigma_data"
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraphAsymmErrors(0)
    gpre  = ROOT.TGraphAsymmErrors(0)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        if hdata.GetBinContent(i) == 0:
            continue
        denom_pre = hdata.GetBinError(i)
        denom_post = hdata.GetBinError(i)
        #denom_pre = ROOT.TMath.Sqrt(hdata.GetBinContent(i))
        #denom_post = ROOT.TMath.Sqrt(hdata.GetBinContent(i))
        ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/denom_post
        yprefit  = (hdata.GetBinContent(i) - hprefit.GetBinContent(i))/denom_pre
        gpost.SetPoint(i-1,m,ypostfit)
        gpre.SetPoint(i-1,m,yprefit)
    #gpost.Divide(hdata,hpostfit,"pois")
    #gpre.Divide(hdata,hprefit,"pois")
    gpost.SetLineColor(colors[1])
    gpre.SetLineColor(colors[0])
    gpost.SetMarkerColor(colors[1])
    gpre.SetMarkerColor(colors[0])
    gpost.SetMarkerSize(1)
    gpre.SetMarkerSize(1)
    gpre.SetTitle("")
    gpre.SetMarkerStyle(4)
    gpost.SetMarkerStyle(3)
    gpre.GetXaxis().SetTitle(hprefit.GetXaxis().GetTitle())
    gpre.GetYaxis().SetTitle("#frac{data-fit}{#sigma}")
    gpre.GetYaxis().SetTitleSize(0.15)
    gpre.GetYaxis().SetTitleOffset(0.2)
    gpre.GetXaxis().SetTitleSize(0.15)
    gpre.GetXaxis().SetTitleOffset(0.7)
    gpre.GetXaxis().SetLabelSize(0.15)
    gpre.GetYaxis().SetLabelSize(0.15)
    gpre.GetXaxis().SetNdivisions(6)
    gpre.GetYaxis().SetNdivisions(4)
    gpre.SetMaximum(6)
    gpre.SetMinimum(-6)
    x = hprefit.GetXaxis().GetBinLowEdge(1)
    X = hprefit.GetXaxis().GetBinUpEdge(N)
    gpre.GetXaxis().SetLimits(x,X)
    gpost.GetXaxis().SetLimits(x,X)
    print "set fit range " +str(x) + " "+str(X)
    return [gpre,gpost] 
 

def builtFittedPdf(pdfs,coefficients):
    result = RooAddPdf(pdfs,coefficients)
    return result

def plotDiffMjet1Mjet2(pdfs,data,norm):
    # do some z projections
    h=[]
    lv=[]
    dh = ROOT.TH1F("delta","delta",50,0,215)
    for p in pdfs:
        h.append( ROOT.TH1F("h_"+p.GetName(),"h_"+p.GetName(),50,0,215))
        lv.append({})
    for i in range(0,len(pdfs)):
        for zk,zv in zBins_redux.iteritems():
            lv[i][zv]=0    
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 dh.Fill(ROOT.TMath.Abs(xv-yv),data.weight(argset))
                 i=0
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]*norm
                 for p in pdfs:
                    h[i].Fill(ROOT.TMath.Abs(xv-yv),p.getVal(argset)*binV)
                    i+=1
    leg = ROOT.TLegend(0.88,0.65,0.7,0.88)
    c = ROOT.TCanvas("c","c",800,400)
    h[0].SetLineColor(colors[0])
    h[0].SetTitle("Mjet1 - Mjet2")
    h[0].GetXaxis().SetTitle("m_{jj}")
    h[0].GetYaxis().SetTitleOffset(1.3)
    h[0].GetYaxis().SetTitle("events")
    h[0].SetMinimum(0)
    h[0].Draw("hist")
    
    dh.SetMarkerStyle(1)
    dh.Draw("same")
    leg.AddEntry(dh,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        #h[i].Scale(n)#/h[i].Integral())
        h[i].SetLineColor(colors[i])
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    
    leg.SetLineColor(0)
    leg.Draw("same")
    c.SaveAs(options.output+"testDeltaMjet_"+options.label+"_z"+(options.zrange.split(","))[0]+"To"+(options.zrange.split(","))[1]+".pdf")



if __name__=="__main__":
     #finMC = ROOT.TFile("/home/dschaefer/tmp/JJ_nonRes_COND2D_HPHP_l1_nominal.root","READ")
     #finMC = ROOT.TFile("/home/dschaefer/DiBoson3D/test_kernelSmoothing_pythia/JJ_pythia_HPHP.root","READ");
     #if options.name.find("Binning")!=-1:
     finMC = ROOT.TFile("/home/dschaefer/DiBoson3D/finalKernels/JJ_HPHP.root","READ"); 
     hinMC = finMC.Get("nonRes");
     #hinMC = finMC.Get("histo_nominal");
     sig = "WprimeWZ"
     
     xBins= getListOfBins(hinMC,"x")
     xBinslowedge = getListOfBinsLowEdge(hinMC,'x')
     yBins= getListOfBins(hinMC,"y")
     yBinslowedge = getListOfBinsLowEdge(hinMC,'y')
     zBins= getListOfBins(hinMC,"z")
     #finMC.Close()
    
     xBinslowedge = getListOfBinsLowEdge(hinMC,'x')
     xBinsWidth   = getListOfBinsWidth(hinMC,"x")
     
     yBinsWidth   = getListOfBinsWidth(hinMC,"y")
     
     zBinslowedge = getListOfBinsLowEdge(hinMC,'z')
     zBinsWidth   = getListOfBinsWidth(hinMC,"z")
     print "open file " +options.name
     f = ROOT.TFile(options.name,"READ")
     workspace = f.Get("w")
     f.Close()
     #workspace.Print()
     model = workspace.pdf("model_b")
    
     data = workspace.data("data_obs")
     norm = data.sumEntries()
     print "sum entries norm "+str(norm)

     if options.postfit:
        fitresult = model.fitTo(data,ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1) ,ROOT.RooFit.NumCPU(8))
        if options.log!="":
            params = fitresult.floatParsFinal()
            paramsinit = fitresult.floatParsInit()
            paramsfinal = ROOT.RooArgSet(params)
            paramsfinal.writeToFile(options.output+options.log)
            logfile = open(options.output+options.log,"a::ios::ate")
            logfile.write("#################################################\n")
            for k in range(0,len(params)):
                pf = params.at(k)
                if not("nonRes" in pf.GetName()):
                    continue
                pi = paramsinit.at(k)
                r  = pi.getMax()-1
                logfile.write(pf.GetName()+" & "+str((pf.getVal()-pi.getVal())/r)+"\\\\ \n")
            logfile.close()
            
     # try to get kernel Components 
     args  = model.getComponents()
     #coeff = model.get
     allpdfs = []
     purity="HPHP"
     if options.pdf.find("HPLP")!=-1:
         print "make plots for HPLP region "
         purity="HPLP"
     for p in options.pdf.split(","):
         allpdfs.append(args[p])
     pdf = args["nonResNominal_JJ_"+sig+"_"+purity+"_13TeV"]
     pdf_shape_postfit  = args["shapeBkg_nonRes_JJ_"+sig+"_"+purity+"_13TeV"]
     #pdf_shape_postfit.funcList().Print()
     #pdf_shape_postfit.coefList().Print()
     pdf_shape_postfit.SetName("pdf_postfit_shape")       
     # get data from workspace 
     norm = (args["pdf_binJJ_"+sig+"_"+purity+"_13TeV_bonly"].getComponents())["n_exp_binJJ_"+sig+"_"+purity+"_13TeV_proc_nonRes"].getVal()
     # check normalization with from pdf generated data:
     #pdf_shape_postfit.syncTotal()
     #################################################
     print "norm after fit "+str(norm)
     data.Print()
     pdf_shape_postfit.Print()
     pdf.Print()
     # get variables from workspace 
     MJ1= workspace.var("MJ1");
     MJ2= workspace.var("MJ2");
     MJJ= workspace.var("MJJ");
     del workspace
    
     argset = ROOT.RooArgSet();
     argset.add(MJJ);
     argset.add(MJ2);
     argset.add(MJ1);
     
     x = getListFromRange(options.xrange)
     y = getListFromRange(options.yrange)
     z = getListFromRange(options.zrange)
     
     
     xBins_redux = reduceBinsToRange(xBins,x)
     yBins_redux = reduceBinsToRange(yBins,y)
     zBins_redux = reduceBinsToRange(zBins,z)
     #print xBins_redux
     #print yBins_redux
     #print zBins_redux
     
     #make projections onto MJJ axis
     if options.projection =="z":
         pdfs = allpdfs#[pdf,pdf_PTZDown,pdf_OPTZUp,pdf_OPTZDown,pdf_PTZUp]
         #keys = xBins_redux.keys()
         #keys.sort()
         #zkeys = yBins_redux.keys()
         #zkeys.sort()
         #if y[0]==0 and y[1]==-1 and x[0]==0 and x[1]==-1:
             #print "project all " 
             #proj= hinMC.ProjectionZ("projz",0,-1,0,-1)
         #else:    
             #proj= hinMC.ProjectionZ("projz",keys[0],keys[-1],zkeys[0],zkeys[-1])
         doZprojection(pdfs,data,norm)
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doZprojection(postfit,data,norm)
         
     #make projections onto MJ1 axis
     if options.projection =="x":
         pdfs = allpdfs #[pdf,pdf_PTXYDown,pdf_OPTXYDown,pdf_OPTXYUp,pdf_PTXYUp]
         #if y[0]==0 and y[1]==-1 and z[0]==0 and z[1]==-1:
             #print "project all " 
             #proj= hinMC.ProjectionX("projx",0,-1,0,-1)
         #else:
            #keys = yBins_redux.keys()
            #keys.sort()
            #zkeys = zBins_redux.keys()
            #zkeys.sort()
         
            #proj= hinMC.ProjectionX("projx",keys[0],keys[-1],zkeys[0],zkeys[-1])
         doXprojection(pdfs,data,norm)
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doXprojection(postfit,data,norm)
         
         
     #make projections onto MJ2 axis
     if options.projection =="y":
         pdfs = allpdfs #[pdf,pdf_PTXYDown,pdf_OPTXYDown,pdf_OPTXYUp,pdf_PTXYUp]
         #if x[0]==0 and x[1]==-1 and z[0]==0 and z[1]==-1:
             #print "project all " 
             #proj= hinMC.ProjectionY("projy",0,-1,0,-1)
         #else:
            #keys = xBins_redux.keys()
            #keys.sort()
            #zkeys = zBins_redux.keys()
            #zkeys.sort()
            #proj= hinMC.ProjectionY("projy",keys[0],keys[-1],zkeys[0],zkeys[-1])
         doYprojection(pdfs,data,norm)
         
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doYprojection(postfit,data,norm)
         
     if options.projection =="xyz":
        pdfs = allpdfs
        #plotDiffMjet1Mjet2(pdfs,data,norm)
        doXprojection(pdfs,data,norm)
        doYprojection(pdfs,data,norm)
        doZprojection(pdfs,data,norm)
        if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit]
             doXprojection(postfit,data,norm)
             doYprojection(postfit,data,norm)
             doZprojection(postfit,data,norm)
             chi2,ndof = getChi2(pdf_shape_postfit,data,norm)
             print "chi2 " +str( chi2)
             print "ndof " +str(ndof)
             print "chi2/ndof " +str(chi2/ndof)
     #print "xbins = "+str(xBins)
     #print "yBins_redux ="+str(yBins_redux)
     #print "xBinslowedge "+str(xBinslowedge)
     #print "zBins_redux ="+str(zBins_redux)

