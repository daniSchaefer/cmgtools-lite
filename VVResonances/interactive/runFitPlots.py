import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import copy

ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
colors = [ROOT.kBlack,ROOT.kRed-2,ROOT.kRed+1,ROOT.kRed-1,ROOT.kRed+2,ROOT.kGreen-1,ROOT.kGreen-2,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kBlue]


getErrorsFromTH3 = True



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


#def groupBinsInMjet1Mjet2Plane(seeds,res):
    #groupsx =[]
    #groupsy =[]
    #i=0
    #if 215*res >= 2.:
        #print "try summing over mjet bins"
        #for seed in seeds:
            #for seed2 in seeds:
                #groupsx.append([])
                #groupsy.append([])
                #for xk, xv in xBins_redux.iteritems():
                    #for yk, yv in yBins_redux.iteritems():
                        #if xBinslowedge[xk] >= seed*(1-res) and xBinslowedge[xk] <= seed*(1+res):
                            #if yBinslowedge[yk] >= seed2*(1-res) and yBinslowedge[yk] <= seed2*(1+res):
                                ##print yBinslowedge[yk]
                                #groupsx[i].append(xv)
                                #groupsy[i].append(yv)
            #i+=1
    #else:
        #i2=0
        #print " use input binning for chi2"
        #for xk, xv in xBins_redux.iteritems():
           #groupsx.append([xv])
           #i2+=1
        #for yk, yv in yBins_redux.iteritems():
           #groupsy.append([yv])
           #i+=1    
    #return [groupsx,groupsy]
            

def smearOverResolution(mj1,mj2,zbin,pdf,data,norm,res,datahist=0):
    d=0
    p=0
    e=0
    #if zbin==1:
        #print "start smearing for zbin "+str(zbin)
        #print mj1 
        #print mj2 
        #print "1-res "+str(mj1*(1-res))
        #print "1+res "+str(mj1*(1+res))
        #print xBinslowedge[5]
        #print "smear over " 
    for xk, xv in xBins_redux.iteritems():
        if xBinslowedge[xk] < mj1*(1-res) or xBinslowedge[xk] > mj1*(1+res):
            continue
        for yk, yv in yBins_redux.iteritems():
            if yBinslowedge[yk] < mj2*(1-res) or yBinslowedge[yk] > mj2*(1+res):
                continue
            MJ1.setVal(xv)
            MJ2.setVal(yv)
            #if zbin==1:
                #print str(xv)+" , " +str(yv)
            d += data.weight(argset)
            binV = zBinsWidth[zbin]*xBinsWidth[xk]*yBinsWidth[yk]
            p += pdf.getVal(argset)*binV*norm
            e += pow(datahist.GetBinError(xk,yk,zbin),1/2.)
    
    return [d,p,ROOT.TMath.Sqrt(e)]

    

#def getChi2(pdf,data,norm,listOf_mj1,listOf_mj2,option="",res=0.1,datahist=0):
    #pr=[]
    #dr=[]
    #error_dr=[]
    #testbins = []
    #for xv in listOf_mj1:
        #for yv in listOf_mj2:
             #for zk,zv in zBins_redux.iteritems():
                 #MJJ.setVal(zv)
                 #l = smearOverResolution(xv,yv,zk,pdf,data,norm,res,datahist)
                 #dr.append(l[0])
                 #pr.append(l[1])
                 #error_dr.append(l[2])
    #ndof = 0
    #nb =0
    #chi2 = 0
    ##print bins
    #for i in range(0,len(pr)):
        #if dr[i] < 0.1e-10:
            ##print i
            #continue
        #if ROOT.TMath.Abs(dr[i] - pr[i])/ROOT.TMath.Sqrt(dr[i]) > 10:
            #print " bin  "+str(getMV(i)) + " data  " +str(dr[i])+ " kernel "+str(pr[i]) + " diff "+ str((dr[i] - pr[i])/ROOT.TMath.Sqrt(dr[i]))
        #ndof+=1
        ##chi2+= pow((dr[i] - pr[i]),2)/pow(error_dr[i],2)
        #if option=="" or option=="BakerCousins":
            #chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))
        #if option=="Neyman":
            #chi2+= pow((dr[i] - pr[i]),2)/pow(error_dr[i],2)
        #if option=="Pearson":
            #chi2+= pow((dr[i] - pr[i]),2)/pr[i]
    #return [chi2,ndof-1]
    
    
    
def getChi2(pdf,data,norm,option="",datahist=0):
    pr=[]
    dr=[]
    error_dr=[]
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 dr.append(data.weight(argset))
                 if datahist!=0:    
                    error_dr.append(datahist.GetBinError(xk,yk,zk))
                 else:
                     error_dr.append(ROOT.TMath.Sqrt(data.weight(argset)))
                 pr.append( pdf.getVal(argset)*binV*norm)
                 if error_dr[-1]==0:
                     continue
                 #if pow(dr[-1] - pr[-1],2)/error_dr[-1] > 10:
                 #   print "mjet1  "+str(xv) + " mjet2 "+ str(yv)+" mjj "+str(zv)+ " data  " +str(dr[-1])+ " kernel "+str(pr[-1]) + " diff "+ str((dr[-1] - pr[-1])) +"      error data "+str(error_dr[-1])  
    ndof = 0
    chi2 = 0
    for i in range(0,len(pr)):
        if dr[i] < 10e-10:
            continue
        ndof+=1
        if option=="" or option=="BakerCousins":
            chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))
        if option=="Neyman":
            if error_dr[i] ==0.0:
                print "error is zero !?"
                continue
            c = pow((dr[i] - pr[i]),2)/pow(error_dr[i],1)
            chi2+= c
        if option=="Pearson":
            chi2+= pow((dr[i] - pr[i]),2)/pr[i]
        if option=="Neyman2":
            chi2+= pow((dr[i] - pr[i]),2)/pow(dr[i],1)
    return [chi2,ndof]


def setHistoErrorsToSQRT(hist):
    for i in range(1,hist.GetNbinsX()+1):
        hist.SetBinError(i,ROOT.TMath.Sqrt(hist.GetBinContent(i)))
    return hist

def doZprojection(pdfs,data,norm,zBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options, proj=0):
    postfit=False
    for p in pdfs:
        if p.GetName().find("postfit")!=-1:
            postfit = True
            break
    # do some z projections
    h=[]
    lv=[]
    test=[]
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
                        if "Jets" in p.GetName() or "Signal" in p.GetName():
                            #print ' "integrate" over analytical function'
                            nn=10
                            for n in range(0,nn):
                                w = zBinsWidth[zk]
                                step = w/float(nn)
                                MJJ.setVal(zv+n*step)
                                if zv+n*step >= zv+w:
                                    continue
                                lv[i][zv]+= p.getVal(argset)*binV/w*step
                        else:
                            lv[i][zv] += p.getVal(argset)*binV
                    i+=1
    #print 'z projection '
    for i in range(0,len(pdfs)):
        for zk,zv in zBins_redux.iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(zv,lv[i][zv])
            else:
                h[i].Fill(zv,lv[i][zv]*norm)
                #if i==0:
                    #print "input in histo " + str(lv[i][zv]*norm) + " zv " +str(zv)
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
    #print 'z projection '
    #print test
    dh.SetLineColor(colors[0])
    dh.SetTitle("Z-Proj. x : "+options.xrange+" y : "+options.yrange)
    dh.GetXaxis().SetTitle("m_{jj}")
    dh.SetMinimum(1e-1)
    dh.GetYaxis().SetTitleOffset(1.3)
    dh.GetYaxis().SetTitle("events")
    #h[0].Scale(n)#/h[0].Integral())
    if postfit:
        dh.GetYaxis().SetTitleOffset(0.6)
        dh.GetYaxis().SetTitle("events")
        dh.GetYaxis().SetTitleSize(0.06)
        dh.GetYaxis().SetLabelSize(0.06)
        dh.GetYaxis().SetNdivisions(5)
    dh.SetBinErrorOption(ROOT.TH1.kPoisson)
    #dh.Sumw2()
    dh.SetMarkerStyle(1)
    dh = setHistoErrorsToSQRT(dh)
    dh.Draw()
    h[0].Draw("histsame")
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
        #ktest0 = h[0].KolmogorovTest(dh,"DX")
        #ktest1 = h[1].KolmogorovTest(dh,"DX")
        #print "chi2 test :" 
        #print ktest0
        #print ktest1
        latex = ROOT.TLatex()
        #latex.DrawLatex(2000,10,"kolmogorov test "+str(ktest0))
        #latex.DrawLatex(2000,1,"kolmogorov test "+str(ktest1))
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


def doXprojection(pdfs,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options,hin=0):
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
                        if "Jets" in p.GetName() or "Signal" in p.GetName():
                            #print ' "integrate" over analytical function'
                            nn=100
                            for n in range(0,nn):
                                w = xBinsWidth[xk]
                                step = w/float(nn)
                                MJ1.setVal(xv+n*step)
                                if xv+n*step >= xv+w:
                                    continue
                                lv[i][xv]+= p.getVal(argset)*(binV/w)*step
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
    proj.SetLineColor(colors[0])
    proj.SetTitle("X-Proj. y : "+options.yrange+" z : "+options.zrange)
    proj.GetXaxis().SetTitle("m_{jet1}")
    proj.GetYaxis().SetTitleOffset(1.3)
    proj.GetYaxis().SetTitle("events")
    if postfit:
        proj.GetYaxis().SetTitleOffset(0.6)
        proj.GetYaxis().SetTitle("events")
        proj.GetYaxis().SetTitleSize(0.06)
        proj.GetYaxis().SetLabelSize(0.06)
        proj.GetYaxis().SetNdivisions(5)
    #print "integral "+str(h[0].Integral())
    #s = h[0].Integral()/h[1].Integral()
    #h[0].Scale(n)#/h[0].Integral())
    #print "integral 1 "+str(h[1].Integral())
    proj.SetMarkerStyle(1)
    proj = setHistoErrorsToSQRT(proj)
    proj.Draw()
    h[0].Draw("histsame")
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
    

def doYprojection(pdfs,data,norm,yBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options):
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
                        if "Jets" in p.GetName() or "Signal" in p.GetName():
                            #print ' "integrate" over analytical function'
                            nn=100
                            for n in range(0,nn):
                                w = yBinsWidth[yk]
                                step = w/float(nn)
                                MJ2.setVal(yv+n*step)
                                if yv+n*step >= yv+w:
                                    continue
                                lv[i][yv]+= p.getVal(argset)*(binV/w)*step
                        else:
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
    proj.SetLineColor(colors[0])
    proj.SetTitle("Y-Proj. x : "+options.xrange+" z : "+options.zrange)
    proj.GetXaxis().SetTitle("m_{jet2}")
    proj.GetYaxis().SetTitleOffset(1.3)
    proj.GetYaxis().SetTitle("events")
    if postfit:
        proj.GetYaxis().SetTitleOffset(0.6)
        proj.GetYaxis().SetTitle("events")
        proj.GetYaxis().SetTitleSize(0.06)
        proj.GetYaxis().SetLabelSize(0.06)
        proj.GetYaxis().SetNdivisions(5)
    #h[0].Scale(n)#/h[0].Integral())
    proj.SetMarkerStyle(1)
    proj = setHistoErrorsToSQRT(proj)
    proj.Draw()
    
    h[0].Draw("histsame")
    leg.AddEntry(proj,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        h[i].SetLineColor(colors[i])
        #h[i].Scale(n)#/h[i].Integral())
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    
    leg.SetLineColor(0)
    leg.Draw("same")
    #proj.Scale(n)#/proj.Integral())
    if postfit:
        ktest0 = h[0].KolmogorovTest(proj,"DX")
        #ktest1 = h[1].KolmogorovTest(proj,"DX")
        latex = ROOT.TLatex()
        latex.DrawLatex(60,proj.GetBinContent(1)*2/3.,"kolmogorov test "+str(ktest0))
        #latex.DrawLatex(60,proj.GetBinContent(1)/3.,"kolmogorov test "+str(ktest1))
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
        #print "value " +str(hdata.GetBinContent(i))
        #print "error post fit " +str( denom_post)
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
     parser.add_option("--hkernel",dest="hkernel",help="MC kernels used to build workspace",default="/home/dschaefer/DiBoson3D/finalKernels/JJ_pythia_HPHP.root")
     parser.add_option("--pdf",dest="pdf",help="name of pdfs lie PTZUp etc",default="nonResNominal_JJ_HPHP_13TeV,nonRes_PTZDown_JJ_HPHP_13TeV,nonRes_OPTZUp_JJ_HPHP_13TeV,nonRes_PTZUp_JJ_HPHP_13TeV,nonRes_OPTZDown_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV")
     
     #pt2Sys
     #nonResNominal_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV,nonRes_OPT2Up_JJ_HPHP_13TeV,nonRes_OPT2Down_JJ_HPHP_13TeV,nonRes_PT2Up_JJ_HPHP_13TeV,nonRes_PT2Down_JJ_HPHP_13TeV
     
     #ptSys 
     
     #nonResNominal_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTZDown_JJ_HPHP_13TeV,nonRes_OPTZUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTZDown_JJ_HPHP_13TeV,nonRes_PTZUp_JJ_HPHP_13TeV
     
     
     
     
     (options,args) = parser.parse_args()
    
    
     #finMC = ROOT.TFile("/home/dschaefer/tmp/JJ_nonRes_COND2D_HPHP_l1_nominal.root","READ")
     #finMC = ROOT.TFile("/home/dschaefer/DiBoson3D/test_kernelSmoothing_pythia/JJ_pythia_HPHP.root","READ");
     #if options.name.find("Binning")!=-1:
     infile_MCTH3 = options.hkernel
     finMC = ROOT.TFile(infile_MCTH3,"READ"); 
     hinMC = finMC.Get("data");
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
     print pdf_shape_postfit
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
  
     
     #make projections onto MJJ axis
     if options.projection =="z":
         pdfs = allpdfs
         doZprojection(pdfs,data,norm,zBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doZprojection(postfit,data,norm,zBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
         
     #make projections onto MJ1 axis
     if options.projection =="x":
         pdfs = allpdfs 
         doXprojection(pdfs,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doXprojection(postfit,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
         
         
     #make projections onto MJ2 axis
     if options.projection =="y":
         pdfs = allpdfs 
         doYprojection(pdfs,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
         
         if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit,pdf_shape_postfit,model]
             doYprojection(postfit,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
      
     listOf_mj1 = []#[55,67,82,100,122,149,182,222]
     listOf_mj2 = listOf_mj1
     
     x=55
     res=0.1
     while(x < 230):
         listOf_mj1.append(x)
         x=x*(1+res)/(1-res)
      
     if options.projection =="xyz":
        pdfs = allpdfs
        #plotDiffMjet1Mjet2(pdfs,data,norm)
        doXprojection(pdfs,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
        doYprojection(pdfs,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
        doZprojection(pdfs,data,norm,zBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
        if options.postfit == True:
             postfit = [pdf,pdf_shape_postfit]
             doXprojection(postfit,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
             doYprojection(postfit,data,norm,xBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
             doZprojection(postfit,data,norm,zBinslowedge,xBins_redux,yBins_redux,zBins_redux,xBinsWidth,yBinsWidth,zBinsWidth,MJ1,MJ2,MJJ,argset,options)
             chi2,ndof = getChi2(pdf_shape_postfit,data,norm,"",hinMC)
             #chi2, ndof = getChi2(pdf_shape_postfit,data,norm,listOf_mj1,listOf_mj1,"",res,hinMC)
             print "chi2 " +str( chi2)
             print "ndof " +str(ndof)
             print "chi2/ndof " +str(chi2/ndof)
             if ndof ==0:
                 sys.exit()
             print "probability "+str(ROOT.TMath.Prob(chi2,ndof))
             print "neyman"
             chi2,ndof = getChi2(pdf_shape_postfit,data,norm,"Neyman",hinMC)
             #chi2, ndof = getChi2(pdf_shape_postfit,data,norm,listOf_mj1,listOf_mj1,"Neyman",res,hinMC)
             print "chi2 " +str( chi2)
             print "ndof " +str(ndof)
             print "chi2/ndof " +str(chi2/ndof)
             print "neyman2"
             #chi2,ndof = getChi2(pdf_shape_postfit,data,norm,"Neyman2",hinMC)
             #print "chi2 " +str( chi2)
             #print "ndof " +str(ndof)
             #print "chi2/ndof " +str(chi2/ndof)
             #print "pearson"
             chi2,ndof = getChi2(pdf_shape_postfit,data,norm,"Pearson",hinMC)
             #chi2, ndof = getChi2(pdf_shape_postfit,data,norm,listOf_mj1,listOf_mj1,"Pearson",res,hinMC)
             print "chi2 " +str( chi2)
             print "ndof " +str(ndof)
             print "chi2/ndof " +str(chi2/ndof)
            
    
