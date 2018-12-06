import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");
import math, copy

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output folder name",default='postfit_qcd/')
parser.add_option("-n","--name",dest="name",help="Input workspace",default='workspace.root')
parser.add_option("-i","--input",dest="input",help="Input nonRes histo",default='JJ_nonRes_HPHP.root')
parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
parser.add_option("-p","--projection",dest="projection",help="choose which projection should be done",default="xyz")
parser.add_option("-d","--data",dest="data",action="store_true",help="make also postfit plots",default=True)
parser.add_option("--merge",dest="merge",action="store_true",help="Merge all kernels",default=False)
parser.add_option("-l","--label",dest="label",help="add extra label such as pythia or herwig",default="")
parser.add_option("--sample",dest="sample",help="pythia, madgraph or herwig",default="pythia")
parser.add_option("--log",dest="log",help="write fit result to log file",default="fit_results.log")
parser.add_option("--pdfz",dest="pdfz",help="name of pdfs lie PTZUp etc",default="")
parser.add_option("--pdfx",dest="pdfx",help="name of pdfs lie PTXUp etc",default="")
parser.add_option("--pdfy",dest="pdfy",help="name of pdfs lie PTYUp etc",default="")
parser.add_option("--year",dest="year",help="year",default="2017")
(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
colors = [ROOT.kBlack,ROOT.kPink-1,ROOT.kAzure+1,ROOT.kAzure+1,210,210,ROOT.kMagenta,ROOT.kMagenta,ROOT.kOrange,ROOT.kOrange,ROOT.kViolet,ROOT.kViolet]

def merge_all():
 fin_herwig_mjj = ROOT.TFile.Open('save_new_shapes_herwig_%s_1D.root'%purity,'READ') 
 histo_altshapeUp_mjj = fin_herwig_mjj.histo_nominal
 histo_altshapeUp_mjj.SetName('histo_altshapeUp')
 histo_altshapeUp_mjj.SetTitle('histo_altshapeUp')
 
 fin_madgraph_mjj = ROOT.TFile.Open('save_new_shapes_madgraph_%s_1D.root'%purity,'READ')
 histo_altshape2Up_mjj = fin_madgraph_mjj.histo_nominal
 histo_altshape2Up_mjj.SetName('histo_altshape2Up')
 histo_altshape2Up_mjj.SetTitle('histo_altshape2Up')
 
 fin_pythia_mjj = ROOT.TFile.Open('save_new_shapes_pythia_%s_1D.root'%purity,'UPDATE')
 histo_nominal = fin_pythia_mjj.histo_nominal
 histo_altshapeUp_mjj.Write('histo_altshapeUp')
 histo_altshapeDown_mjj = mirror(histo_altshapeUp_mjj,histo_nominal,"histo_altshapeDown")
 histo_altshapeDown_mjj.SetName('histo_altshapeDown')
 histo_altshapeDown_mjj.SetTitle('histo_altshapeDown')
 histo_altshapeDown_mjj.Write('histo_altshapeDown') 
 
 histo_altshape2Up_mjj.Write('histo_altshape2Up')
 histo_altshape2Down_mjj = mirror(histo_altshape2Up_mjj,histo_nominal,"histo_altshape2Down")
 histo_altshape2Down_mjj.SetName('histo_altshape2Down')
 histo_altshape2Down_mjj.SetTitle('histo_altshape2Down')
 histo_altshape2Down_mjj.Write('histo_altshape2Down') 
 
 fin_pythia_mjj.Close()
 fin_madgraph_mjj.Close()
 fin_herwig_mjj.Close()
 
 fin_herwig_l1 = ROOT.TFile.Open('save_new_shapes_herwig_%s_COND2D_l1.root'%purity,'READ') 
 histo_altshapeUp_l1 = fin_herwig_l1.histo_nominal
 histo_altshapeUp_l1.SetName('histo_altshapeUp')
 histo_altshapeUp_l1.SetTitle('histo_altshapeUp')
 
 fin_madgraph_l1 = ROOT.TFile.Open('save_new_shapes_madgraph_%s_COND2D_l1.root'%purity,'READ')
 histo_altshape2Up_l1 = fin_madgraph_l1.histo_nominal
 histo_altshape2Up_l1.SetName('histo_altshape2Up')
 histo_altshape2Up_l1.SetTitle('histo_altshape2Up')
 
 fin_pythia_l1 = ROOT.TFile.Open('save_new_shapes_pythia_%s_COND2D_l1.root'%purity,'UPDATE')
 histo_nominal = fin_pythia_l1.histo_nominal
 histo_altshapeUp_l1.Write('histo_altshapeUp')
 histo_altshapeDown_l1 = mirror(histo_altshapeUp_l1,histo_nominal,"histo_altshapeDown",2)
 conditional(histo_altshapeDown_l1)
 histo_altshapeDown_l1.SetName('histo_altshapeDown')
 histo_altshapeDown_l1.SetTitle('histo_altshapeDown')
 histo_altshapeDown_l1.Write('histo_altshapeDown') 
 
 histo_altshape2Up_l1.Write('histo_altshape2Up')
 histo_altshape2Down_l1 = mirror(histo_altshape2Up_l1,histo_nominal,"histo_altshape2Down",2)
 conditional(histo_altshape2Down_l1)
 histo_altshape2Down_l1.SetName('histo_altshape2Down')
 histo_altshape2Down_l1.SetTitle('histo_altshape2Down')
 histo_altshape2Down_l1.Write('histo_altshape2Down') 
 
 fin_pythia_l1.Close()
 fin_madgraph_l1.Close()
 fin_herwig_l1.Close()
 fin_herwig_l2 = ROOT.TFile.Open('save_new_shapes_herwig_%s_COND2D_l2.root'%purity,'READ') 
 histo_altshapeUp_l2 = fin_herwig_l2.histo_nominal
 histo_altshapeUp_l2.SetName('histo_altshapeUp')
 histo_altshapeUp_l2.SetTitle('histo_altshapeUp')
 
 fin_madgraph_l2 = ROOT.TFile.Open('save_new_shapes_madgraph_%s_COND2D_l2.root'%purity,'READ')
 histo_altshape2Up_l2 = fin_madgraph_l2.histo_nominal
 histo_altshape2Up_l2.SetName('histo_altshape2Up')
 histo_altshape2Up_l2.SetTitle('histo_altshape2Up')
 
 fin_pythia_l2 = ROOT.TFile.Open('save_new_shapes_pythia_%s_COND2D_l2.root'%purity,'UPDATE')
 histo_nominal = fin_pythia_l2.histo_nominal
 histo_altshapeUp_l2.Write('histo_altshapeUp')
 histo_altshapeDown_l2 = mirror(histo_altshapeUp_l2,histo_nominal,"histo_altshapeDown",2)
 conditional(histo_altshapeDown_l2)
 histo_altshapeDown_l2.SetName('histo_altshapeDown')
 histo_altshapeDown_l2.SetTitle('histo_altshapeDown')
 histo_altshapeDown_l2.Write('histo_altshapeDown') 
 
 histo_altshape2Up_l2.Write('histo_altshape2Up')
 histo_altshape2Down_l2 = mirror(histo_altshape2Up_l2,histo_nominal,"histo_altshape2Down",2)
 conditional(histo_altshape2Down_l2)
 histo_altshape2Down_l2.SetName('histo_altshape2Down')
 histo_altshape2Down_l2.SetTitle('histo_altshape2Down')
 histo_altshape2Down_l2.Write('histo_altshape2Down') 
 
 fin_pythia_l2.Close()
 fin_madgraph_l2.Close()
 fin_herwig_l2.Close()
 
def unequalScale(histo,name,alpha,power=1,dim=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    if dim == 2:
	    maxFactor = max(pow(histo.GetXaxis().GetXmax(),power),pow(histo.GetXaxis().GetXmin(),power))
	    for i in range(1,histo.GetNbinsX()+1):
	        x= histo.GetXaxis().GetBinCenter(i)
	        for j in range(1,histo.GetNbinsY()+1):
	            nominal=histo.GetBinContent(i,j)
	            factor = 1+alpha*pow(x,power) 
	            newHistoU.SetBinContent(i,j,nominal*factor)
	            newHistoD.SetBinContent(i,j,nominal/factor)
	    if newHistoU.Integral()>0.0:        
	        newHistoU.Scale(1.0/newHistoU.Integral())        
	    if newHistoD.Integral()>0.0:        
	        newHistoD.Scale(1.0/newHistoD.Integral())        
    else:
	    for i in range(1,histo.GetNbinsX()+1):
	        x= histo.GetXaxis().GetBinCenter(i)
	        nominal=histo.GetBinContent(i) #ROOT.TMath.Log10(histo.GetBinContent(i))
		factor = 1+alpha*pow(x,power)
		#print i,x,power,alpha,factor,nominal,nominal*factor,nominal/factor
	        newHistoU.SetBinContent(i,nominal*factor)
	        if factor != 0: newHistoD.SetBinContent(i,nominal/factor)	
    return newHistoU,newHistoD 
    
def mirror(histo,histoNominal,name,dim=1):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    print intNominal,intUp
    if dim == 2:
		for i in range(1,histo.GetNbinsX()+1):
			for j in range(1,histo.GetNbinsY()+1):
				up=histo.GetBinContent(i,j)/intUp
				nominal=histoNominal.GetBinContent(i,j)/intNominal
				if up != 0: newHisto.SetBinContent(i,j,histoNominal.GetBinContent(i,j)*nominal/up)
    else:
		for i in range(1,histo.GetNbinsX()+1):
			up=histo.GetBinContent(i)/intUp
			nominal=histoNominal.GetBinContent(i)/intNominal
			newHisto.SetBinContent(i,histoNominal.GetBinContent(i)*nominal/up)	
    return newHisto       

def expandHisto(histo,suffix,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ):
    histogram=ROOT.TH2F(histo.GetName()+suffix,"histo",binsMJ,minMJ,maxMJ,binsMVV,minMVV,maxMVV)
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram

def expandHistoBinned(histo,suffix ,binsx,binsy):
    histogram=ROOT.TH2F(histo.GetName()+suffix,"histo",len(binsx)-1,array('f',binsx),len(binsy)-1,array('f',binsy))
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram
        
def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)
            
def save_shape(final_shape,norm_nonres,sample="pythia"):

    histo = ROOT.TH3F('histo','histo',len(xBinslowedge)-1,xBinslowedge,len(yBinslowedge)-1,yBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_xz = ROOT.TH2F('histo_xz','histo_xz',len(xBinslowedge)-1,xBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_yz = ROOT.TH2F('histo_yz','histo_yz',len(yBinslowedge)-1,yBinslowedge,len(zBinslowedge)-1,zBinslowedge)
    histo_z = ROOT.TH1F('histo_z','histo_z',len(zBinslowedge)-1,zBinslowedge)
    print "Done creating out histos"
    lv = {}
    for xk, xv in xBins.iteritems():
        lv[xv] = {}
        for yk, yv in yBins.iteritems():
          lv[xv][yv] = {}
          for zk,zv in zBins.iteritems():
            lv[xv][yv][zv] = 0

    lv_xz = {}
    lv_yz = {}
    for xk, xv in xBins.iteritems():
        lv_xz[xv] = {}
        lv_yz[xv] = {}
        for zk,zv in zBins.iteritems():
          lv_xz[xv][zv] = 0
          lv_yz[xv][zv] = 0

    lv_z = []
    for zk,zv in zBins.iteritems():
      lv_z.append(0)
      print zk
                               
    for xk, xv in xBins.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins.iteritems():
                 MJJ.setVal(zv)
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 lv[xv][yv][zv] = final_shape.getVal(argset)*binV
                 lv_xz[xv][zv] += final_shape.getVal(argset)*binV
                 lv_yz[yv][zv] += final_shape.getVal(argset)*binV
                 lv_z[zk-1] += final_shape.getVal(argset)*binV

    for xk, xv in xBins.iteritems():
     for yk, yv in yBins.iteritems():
      for zk,zv in zBins.iteritems():
       histo.Fill(xv,yv,zv,lv[xv][yv][zv]*norm_nonres[0])

    for xk, xv in xBins.iteritems():
      for zk,zv in zBins.iteritems():
       histo_xz.Fill(xv,zv,lv_xz[xv][zv]*norm_nonres[0])
       histo_yz.Fill(xv,zv,lv_yz[xv][zv]*norm_nonres[0])
    
    for zk,zv in zBins.iteritems(): histo_z.Fill(zv,lv_z[zk-1]*norm_nonres[0])    
       
    fout_z = ROOT.TFile.Open('save_new_shapes_%s_%s_1D.root'%(sample,purity),'RECREATE')
    fout_z.cd()
    histo_z.Scale(1./histo_z.Integral())
    histo_z.SetTitle('histo_nominal')
    histo_z.SetName('histo_nominal')
    histo_z.Write('histo_nominal')

    print "Now PT 1D",zBinslowedge[-1],zBinslowedge[0],xBinslowedge[-1],xBinslowedge[0]
    alpha=1.5/float(zBinslowedge[-1])
    histogram_pt_up,histogram_pt_down=unequalScale(histo_z,"histo_nominal_PT",alpha,1)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 1D"
    alpha=1.5*float(zBinslowedge[0])
    histogram_opt_up,histogram_opt_down=unequalScale(histo_z,"histo_nominal_OPT",alpha,-1)
    histogram_opt_down.SetName('histo_nominal_OPTDown')
    histogram_opt_down.SetTitle('histo_nominal_OPTDown')
    histogram_opt_down.Write('histo_nominal_OPTDown')
    histogram_opt_up.SetName('histo_nominal_OPTUp')
    histogram_opt_up.SetTitle('histo_nominal_OPTUp')
    histogram_opt_up.Write('histo_nominal_OPTUp')
        
    fout_z.Close()
    
    fout_xz = ROOT.TFile.Open('save_new_shapes_%s_%s_COND2D_l1.root'%(sample,purity),'RECREATE')
    fout_xz.cd()  
    conditional(histo_xz)
    histo_xz.SetTitle('histo_nominal')
    histo_xz.SetName('histo_nominal')
    histo_xz.Write('histo_nominal')

    print "Now PT 2D l1"
    alpha=1.5/float(xBinslowedge[-1])
    histogram_pt_up,histogram_pt_down=unequalScale(histo_xz,"histo_nominal_PT",alpha,1,2)
    conditional(histogram_pt_down)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    conditional(histogram_pt_up)
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 2D l1"
    alpha=1.5*float(xBinslowedge[0])
    h1,h2=unequalScale(histo_xz,"histo_nominal_OPT",alpha,-1,2)
    conditional(h1)
    h1.SetName('histo_nominal_OPTUp')
    h1.SetTitle('histo_nominal_OPTUp')
    h1.Write('histo_nominal_OPTUp')
    conditional(h2)
    h2.SetName('histo_nominal_OPTDown')
    h2.SetTitle('histo_nominal_OPTDown')
    h2.Write('histo_nominal_OPTDown')
        
    fout_xz.Close()
    
    fout_yz = ROOT.TFile.Open('save_new_shapes_%s_%s_COND2D_l2.root'%(sample,purity),'RECREATE')
    fout_yz.cd()  
    conditional(histo_yz)
    histo_yz.SetTitle('histo_nominal')
    histo_yz.SetName('histo_nominal')
    histo_yz.Write('histo_nominal')

    print "Now PT 2D l2"
    alpha=1.5/float(xBinslowedge[-1])
    histogram_pt_up,histogram_pt_down=unequalScale(histo_yz,"histo_nominal_PT",alpha,1,2)
    conditional(histogram_pt_down)
    histogram_pt_down.SetName('histo_nominal_PTDown')
    histogram_pt_down.SetTitle('histo_nominal_PTDown')
    histogram_pt_down.Write('histo_nominal_PTDown')
    conditional(histogram_pt_up)
    histogram_pt_up.SetName('histo_nominal_PTUp')
    histogram_pt_up.SetTitle('histo_nominal_PTUp')
    histogram_pt_up.Write('histo_nominal_PTUp')

    print "Now OPT 2D l2"
    alpha=1.5*float(xBinslowedge[0])
    h1,h2=unequalScale(histo_yz,"histo_nominal_OPT",alpha,-1,2)
    conditional(h1)
    h1.SetName('histo_nominal_OPTUp')
    h1.SetTitle('histo_nominal_OPTUp')
    h1.Write('histo_nominal_OPTUp')
    conditional(h2)
    h2.SetName('histo_nominal_OPTDown')
    h2.SetTitle('histo_nominal_OPTDown')
    h2.Write('histo_nominal_OPTDown')
    
    fout_yz.Close()    
    
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
    bins ={}
    for i in range(1,N+1): bins[i] = axis.GetBinCenter(i) 
    
    return bins

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
    for i in range(1,N+2): r.append(axis.GetBinLowEdge(i)) 
    
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

def doZprojection(pdfs,data,norm,proj=0):
    # do some z projections
    h=[]
    lv=[]
    dh = ROOT.TH1F("dh","dh",len(zBinslowedge)-1,zBinslowedge)
    neventsPerBin = [0 for zv in range(len(zBins_redux))]
    errPerBin = [0 for zv in range(len(zBins_redux))]
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
                 #dh.Fill(zv,data.weight(argset))
                 neventsPerBin[zk-1] += data.weight(argset)
                 errPerBin[zk-1] += errdata_lo[xv][yv][zv]*errdata_lo[xv][yv][zv]
                 i=0
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]     
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][zv] += p.weight(argset)#p.evaluate()*binV
                    else:
                            # lv[i][xv] += p.evaluate()*binV 
                            lv[i][zv] += p.getVal(argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for zk,zv in zBins_redux.iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(zv,lv[i][zv])
            else:
                h[i].Fill(zv,lv[i][zv]*norm)
     
    for b,e in enumerate(neventsPerBin):
      dh.SetBinContent(b+1,e)
      dh.SetBinError(b+1,math.sqrt(errPerBin[b]))
      print b+1,e,math.sqrt(errPerBin[b])
           
    dh.SetBinErrorOption(ROOT.TH1.kPoisson)
    MakePlots(h,dh,'z',zBinslowedge)

def MakePlots(histos,hdata,axis,nBins):
   
    extra1 = ''
    extra2 = ''
    htitle = ''
    xtitle = ''
    ymin = 0
    ymax = 0
    xrange = options.xrange
    yrange = options.yrange
    zrange = options.zrange
    if options.xrange == '0,-1': xrange = '55,215'
    if options.yrange == '0,-1': yrange = '55,215'
    if options.zrange == '0,-1': zrange = '1126,5500'
    if axis=='z':
     htitle = "Z-Proj. x : "+options.xrange+" y : "+options.yrange
     xtitle = "m_{jj} [GeV]"
     ymin = 0.002
     ymax = hdata.GetMaximum()*10
     extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
     extra2 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
    elif axis=='x':
     htitle = "X-Proj. y : "+options.yrange+" z : "+options.zrange
     xtitle = "m_{jet1} [GeV]"
     ymin = 0.0
     ymax = hdata.GetMaximum()*1.4
     extra1 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
     extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
    elif axis=='y':
     htitle = "Y-Proj. x : "+options.xrange+" z : "+options.zrange
     xtitle = "m_{jet2} [GeV]"
     ymin = 0.0
     ymax = hdata.GetMaximum()*1.4
     extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
     extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
                   
    leg = ROOT.TLegend(0.88,0.65,0.7,0.88)
    c = ROOT.TCanvas("c","c")
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    if axis == 'z': pad1.SetLogy()
    pad1.SetBottomMargin(0.01)    
    pad1.Draw()
    pad1.cd()  
    histos[0].SetMinimum(ymin)
    histos[0].SetMaximum(ymax) 
    histos[0].SetLineColor(colors[0])
    histos[0].SetLineStyle(2)
    histos[0].SetLineWidth(2)
    histos[0].SetTitle(htitle)
    histos[0].GetXaxis().SetTitle(xtitle)
    histos[0].GetYaxis().SetTitleOffset(1.3)
    histos[0].GetYaxis().SetTitle("events")
    histos[0].GetYaxis().SetTitleOffset(1.3)
    histos[0].GetYaxis().SetTitle("events")
    histos[0].GetYaxis().SetTitleSize(0.06)
    histos[0].GetYaxis().SetLabelSize(0.06)
    histos[0].GetYaxis().SetNdivisions(5)
    histos[0].Draw("hist")
    leg.AddEntry(histos[0],"Pre fit pdf","l")
    
    histos[1].SetLineColor(colors[1])
    histos[1].SetLineWidth(2)
    histos[1].Draw('HISTsame')
    leg.AddEntry(histos[1],"Post fit pdf","l")
    
    for i in range(2,len(histos)):
        histos[i].SetLineColor(colors[i])
        histos[i].Draw("histsame")
        name = histos[i].GetName().split("_")
        leg.AddEntry(histos[i],name[2],"l")

    hdata.SetMarkerStyle(20)
    hdata.SetMarkerColor(ROOT.kBlack)
    hdata.SetLineColor(ROOT.kBlack)
    hdata.SetMarkerSize(0.7)
    hdata.Draw("samePE")
    leg.AddEntry(hdata,"data","lp")
        
    leg.SetLineColor(0)
    leg.Draw("same")
    
    # chi2 = getChi2proj(histos[1],hdata)
#     print "Projection %s: Chi2/ndf = %.2f/%i"%(axis,chi2[0],chi2[1]),"= %.2f"%(chi2[0]/chi2[1])," prob = ",ROOT.TMath.Prob(chi2[0],chi2[1])

    # pt = ROOT.TPaveText(0.18,0.06,0.54,0.17,"NDC")
    # pt.SetTextFont(62)
    # pt.SetTextSize(0.04)
    # pt.SetTextAlign(12)
    # pt.SetFillColor(0)
    # pt.SetBorderSize(0)
    # pt.SetFillStyle(0)
    # pt.AddText("Chi2/ndf = %.2f/%i = %.2f"%(chi2[0],chi2[1],chi2[0]/chi2[1]))
    # pt.AddText("Prob = %.3f"%ROOT.TMath.Prob(chi2[0],chi2[1]))
    # pt.Draw()

    pt2 = ROOT.TPaveText(0.18,0.80,0.53,0.93,"NDC")
    pt2.SetTextFont(62)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)
    pt2.AddText(extra1)
    pt2.AddText(extra2)
    pt2.Draw()
    
    c.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    graphs = addRatioPlot(hdata,histos[0],histos[1],nBins)
    #graphs[0].Draw("AP")
    graphs[1].Draw("AP")
    c.SaveAs(options.output+"PostFit"+options.label+"_"+htitle.replace(' ','_')+purity+"_"+options.sample+".png")
    c.SaveAs(options.output+"PostFit"+options.label+"_"+htitle.replace(' ','_')+purity+"_"+options.sample+".root")
    

def doXprojection(pdfs,data,norm,hin=0):
    h=[]
    lv=[]
    proj = ROOT.TH1F("px","px",len(xBinslowedge)-1,xBinslowedge)
    neventsPerBin = [0 for xv in range(len(xBins_redux))]
    errPerBin = [0 for xv in range(len(xBins_redux))]
    
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
                 i=0
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 #proj.Fill(xv,data.weight(argset))
                 neventsPerBin[xk-1] += data.weight(argset)
                 errPerBin[xk-1] += errdata_lo[xv][yv][zv]*errdata_lo[xv][yv][zv]
                 for p in pdfs:
                     if "postfit" in p.GetName():
                         if "data" in p.GetName():
                            lv[i][xv] += p.weight(argset)#p.evaluate()*binV
                         else:
                             lv[i][xv] += p.evaluate()*binV
                     else:
                        lv[i][xv] += p.getVal(argset)*binV
                     i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)

    for b,e in enumerate(neventsPerBin):
      proj.SetBinContent(b+1,e)
      proj.SetBinError(b+1,math.sqrt(errPerBin[b]))
    # proj.SetBinErrorOption(ROOT.TH1.kPoisson)
    MakePlots(h,proj,'x',xBinslowedge)    

def doYprojection(pdfs,data,norm):
    h=[]
    lv=[]
    proj = ROOT.TH1F("py","py",len(yBinslowedge)-1,yBinslowedge)
    neventsPerBin = [0 for yv in range(len(yBins_redux))]
    errPerBin = [0 for yv in range(len(yBins_redux))]
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
                 #proj.Fill(yv,data.weight(argset))
                 neventsPerBin[yk-1] += data.weight(argset)
                 errPerBin[yk-1] += errdata_lo[xv][yv][zv]*errdata_lo[xv][yv][zv]
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

    for b,e in enumerate(neventsPerBin):
      proj.SetBinContent(b+1,e)
      proj.SetBinError(b+1,math.sqrt(errPerBin[b]))
      
    # proj.SetBinErrorOption(ROOT.TH1.kPoisson)
    MakePlots(h,proj,'y',yBinslowedge)  
 

def addPullPlot(hdata,hprefit,hpostfit,nBins):
    #print "make pull plots: (data-fit)/sigma_data"
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraph(0)
    gpre  = ROOT.TGraph(0)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        if hdata.GetBinContent(i) == 0:
            continue
        ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/hdata.GetBinError(i)
        yprefit  = (hdata.GetBinContent(i) - hprefit.GetBinContent(i))/hdata.GetBinError(i)
        if abs(ypostfit)> 4.: 
                
                print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"prefit",hprefit.GetBinContent(i),"err data",hdata.GetBinError(i),"pull postfit",ypostfit,"pull prefit",yprefit
                print "bin %i x %i data %i post-fit %.2f pre-fit %.2f err data %.2f pull %.2f"%(i,m,hdata.GetBinContent(i),hpostfit.GetBinContent(i),hprefit.GetBinContent(i),hdata.GetBinError(i),ypostfit)
        # print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"prefit",hprefit.GetBinContent(i),"err data",hdata.GetBinError(i),"pull postfit",ypostfit,"pull prefit",yprefit
        # print "bin %i x %i data %i post-fit %.2f pre-fit %.2f err data %.2f pull %.2f"%(i,m,hdata.GetBinContent(i),hpostfit.GetBinContent(i),hprefit.GetBinContent(i),hdata.GetBinError(i),ypostfit)
        
        gpost.SetPoint(i-1,m,ypostfit)
        gpre.SetPoint(i-1,m,yprefit)
    gpost.SetLineColor(colors[1])
    gpre.SetLineColor(colors[0])
    gpost.SetMarkerColor(colors[1])
    gpre.SetMarkerColor(colors[0])
    gpost.SetFillColor(ROOT.kBlue)
    gpost.SetMarkerSize(1)
    gpre.SetMarkerSize(1)
    gpre.SetMarkerStyle(4)
    gpost.SetMarkerStyle(3)
    
    #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
    gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
    gt.SetTitle("")
    gt.SetMinimum(-4.999);
    gt.SetMaximum(4.999);
    gt.SetDirectory(0);
    gt.SetStats(0);
    gt.SetLineStyle(0);
    gt.SetMarkerStyle(20);
    gt.GetXaxis().SetTitle(hprefit.GetXaxis().GetTitle());
    gt.GetXaxis().SetLabelFont(42);
    gt.GetXaxis().SetLabelOffset(0.02);
    gt.GetXaxis().SetLabelSize(0.15);
    gt.GetXaxis().SetTitleSize(0.15);
    gt.GetXaxis().SetTitleOffset(1);
    gt.GetXaxis().SetTitleFont(42);
    gt.GetYaxis().SetTitle("#frac{data-fit}{#sigma}");
    gt.GetYaxis().CenterTitle(True);
    gt.GetYaxis().SetNdivisions(205);
    gt.GetYaxis().SetLabelFont(42);
    gt.GetYaxis().SetLabelOffset(0.007);
    gt.GetYaxis().SetLabelSize(0.15);
    gt.GetYaxis().SetTitleSize(0.15);
    gt.GetYaxis().SetTitleOffset(0.4);
    gt.GetYaxis().SetTitleFont(42);
    gt.GetXaxis().SetNdivisions(505)
    #gpre.SetHistogram(gt);
    gpost.SetHistogram(gt);       
    return [gpre,gpost] 
 
def addRatioPlot(hdata,hprefit,hpostfit,nBins):
    #print "make pull plots: (data-fit)/sigma_data"
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraph(0)
    gpre  = ROOT.TGraph(0)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        if hdata.GetBinContent(i) == 0:
            continue
        ypostfit = (hdata.GetBinContent(i) / hpostfit.GetBinContent(i))
        yprefit  = (hdata.GetBinContent(i) / hprefit.GetBinContent(i))
        gpost.SetPoint(i-1,m,ypostfit)
        gpre.SetPoint(i-1,m,yprefit)
    gpost.SetLineColor(colors[1])
    gpre.SetLineColor(colors[0])
    gpost.SetMarkerColor(colors[1])
    gpre.SetMarkerColor(colors[0])
    gpost.SetFillColor(ROOT.kBlue)
    gpost.SetMarkerSize(1)
    gpre.SetMarkerSize(1)
    gpre.SetMarkerStyle(4)
    gpost.SetMarkerStyle(20)
    
    #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
    gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
    gt.SetTitle("")
    gt.SetMinimum(0.5);
    gt.SetMaximum(1.5);
    gt.SetDirectory(0);
    gt.SetStats(0);
    gt.SetLineStyle(0);
    gt.SetMarkerStyle(20);
    gt.GetXaxis().SetTitle(hprefit.GetXaxis().GetTitle());
    gt.GetXaxis().SetLabelFont(42);
    gt.GetXaxis().SetLabelOffset(0.02);
    gt.GetXaxis().SetLabelSize(0.15);
    gt.GetXaxis().SetTitleSize(0.15);
    gt.GetXaxis().SetTitleOffset(1);
    gt.GetXaxis().SetTitleFont(42);
    gt.GetYaxis().SetTitle("#frac{Data}{Fit}");
    gt.GetYaxis().CenterTitle(True);
    gt.GetYaxis().SetNdivisions(205);
    gt.GetYaxis().SetLabelFont(42);
    gt.GetYaxis().SetLabelOffset(0.007);
    gt.GetYaxis().SetLabelSize(0.15);
    gt.GetYaxis().SetTitleSize(0.15);
    gt.GetYaxis().SetTitleOffset(0.4);
    gt.GetYaxis().SetTitleFont(42);
    gt.GetXaxis().SetNdivisions(505)
    #gpre.SetHistogram(gt);
    gpost.SetHistogram(gt);       
    return [gpre,gpost] 
 
def builtFittedPdf(pdfs,coefficients):
    result = RooAddPdf(pdfs,coefficients)
    return result


def getChi2fullModel(pdf,data,norm):
    pr=[]
    dr=[]
    for xk, xv in xBins.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins.iteritems():
                 MJJ.setVal(zv)
                 dr.append(data.weight(argset))
                 binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                 pr.append( pdf.getVal(argset)*binV*norm)
    ndof = 0
    chi2 = 0
    for i in range(0,len(pr)):
        if dr[i] < 10e-10:
            continue
        ndof+=1
        #chi2+= pow((dr[i] - pr[i]),2)/pr[i]
        chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

    return [chi2,ndof]

def getChi2proj(histo_pdf,histo_data):
    pr=[]
    dr=[]
    for b in range(1,histo_pdf.GetNbinsX()+1):
     dr.append(histo_data.GetBinContent(b))
     pr.append(histo_pdf.GetBinContent(b))
    
    ndof = 0
    chi2 = 0
    for i in range(0,len(pr)):
        if dr[i] < 10e-10:
            continue
        ndof+=1
        #chi2+= pow((dr[i] - pr[i]),2)/pr[i]
  #print i,dr[i],pr[i],(dr[i] - pr[i]),pow((dr[i] - pr[i]),2)/pr[i],(dr[i] - pr[i])/histo_data.GetBinError(i+1)
        chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

    return [chi2,ndof]
    

if __name__=="__main__":
     finMC = ROOT.TFile(options.input,"READ");
     hinMC = finMC.Get("nonRes");
     if options.input.find("HPHP")!=-1: purity = "HPHP"
     elif options.input.find("HPLP")!=-1: purity = "HPLP"
     else: purity = "LPLP"  
     print "Using purity: " ,purity                
     #################################################
     xBins= getListOfBins(hinMC,"x")
     xBinslowedge = getListOfBinsLowEdge(hinMC,'x')
     xBinsWidth   = getListOfBinsWidth(hinMC,"x")
     print "x bins:"
     print xBins
     print "x bins low edge:"
     print xBinslowedge
     print "x bins width:"
     print xBinsWidth
     
     #################################################
     print
     yBins= getListOfBins(hinMC,"y")
     yBinslowedge = getListOfBinsLowEdge(hinMC,'y')     
     yBinsWidth   = getListOfBinsWidth(hinMC,"y")
     print "y bins:"
     print yBins
     print "y bins low edge:"
     print yBinslowedge
     print "y bins width:"
     print yBinsWidth
     
     #################################################
     print 
     zBins= getListOfBins(hinMC,"z")
     zBinslowedge = getListOfBinsLowEdge(hinMC,'z')
     zBinsWidth   = getListOfBinsWidth(hinMC,"z")
     print "z bins:"
     print zBins
     print "z bins low edge:"
     print zBinslowedge
     print "z bins width:"
     print zBinsWidth

            
     #################################################                
     print 
     print "open file " +options.name
     f = ROOT.TFile(options.name,"READ")
     workspace = f.Get("w")
     f.Close()
     workspace.Print()

     model = workspace.pdf("model_b") 
     data = workspace.data("data_obs")
     data.Print()
     
   
     ndata = {}
     errdata_lo = {}
     errdata_hi = {}
     for xk, xv in xBins.iteritems():
       ndata[xv] = {}
       errdata_lo[xv] = {}
       errdata_hi[xv] = {}
       for yk, yv in yBins.iteritems():
         ndata[xv][yv] = {}
         errdata_lo[xv][yv] = {}
         errdata_hi[xv][yv] = {}
         for zk,zv in zBins.iteritems():
            ndata[xv][yv][zv] = 0
            errdata_lo[xv][yv][zv] = 0
            errdata_hi[xv][yv][zv] = 0

     for i in xrange(data.numEntries()):
       entry = data.get(i)
       mj1 = entry.find('MJ1').getVal()
       mj2 = entry.find('MJ2').getVal()
       mjj = entry.find('MJJ').getVal()
       ndata[mj1][mj2][mjj] = data.weight()
       hi = ROOT.Double(0.)
       lo = ROOT.Double(0.)
       data.weightError(lo,hi)
       errdata_lo[mj1][mj2][mjj] = lo
       errdata_hi[mj1][mj2][mjj] = hi
     
     
     
     print
     print "Observed number of events:",data.sumEntries()
     
     args  = model.getComponents()
     pdfName = "pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year

     print "Expected number of QCD events:",(args[pdfName].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
     # print "Expected number of QCD events:",workspace.var((args[pdfName].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year]).getVal()
    
     #################################################
     print "Fitting:"
     fitresult = model.fitTo(data,ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))#,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
     # fitresult = model.fitTo(data,ROOT.RooFit.Save(1),ROOT.RooFit.Verbose(1), ROOT.RooFit.Minos(0),ROOT.RooFit.NumCPU(8))
     # ll = ROOT.RooLinkedList()
   #   fitresult = model.chi2FitTo(data)

     # chi2 = ROOT.RooChi2Var("chi2","chi2",model,data,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
 #     print "done with fit, print chi2"
 #     chi2.Print("v")
 #     print "make minuit"
 #     m = ROOT.RooMinuit(chi2)
 #     print "migrad"
 #     m.migrad()
 #     print "hesse"
 #     m.hesse()
 #     print "save minuit"
 #     fitresult = m.save()
 #     print "print wgt"
 #     fitresult.Print("v")

     
        #
     # fitresult.Print()
     # if options.log!="":
     #    params = fitresult.floatParsFinal()
     #    paramsinit = fitresult.floatParsInit()
     #    paramsfinal = ROOT.RooArgSet(params)
     #    paramsfinal.writeToFile(options.output+options.log)
     #    logfile = open(options.output+options.log,"a::ios::ate")
     #    logfile.write("#################################################\n")
     #    for k in range(0,len(params)):
     #        pf = params.at(k)
     #        print pf.GetName(), pf.getVal(), pf.getError(), "%.2f"%(pf.getVal()/pf.getError())
     #        if not("nonRes" in pf.GetName()):
     #      continue
     #        pi = paramsinit.at(k)
     #        r  = pi.getMax()-1
     #        #logfile.write(pf.GetName()+" & "+str((pf.getVal()-pi.getVal())/r)+"\\\\ \n")
     #    logfile.close()

     #################################################
     print            
     # try to get kernel Components 
     #args  = model.getComponents()
            
     print 
     print "Prefit nonRes pdf:"
     pdf_nonres_shape_prefit = args["nonResNominal_JJ_"+purity+"_13TeV_%s"%options.year]
     pdf_nonres_shape_prefit.Print()
     print
     print "Postfit nonRes pdf:"
     pdf_nonres_shape_postfit  = args["shapeBkg_nonRes_JJ_"+purity+"_13TeV_%s"%options.year]
     pdf_nonres_shape_postfit.Print()
     pdf_nonres_shape_postfit.funcList().Print()
     pdf_nonres_shape_postfit.coefList().Print()
     print
     
     allpdfsz = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsz.append(pdf_nonres_shape_prefit)
     allpdfsz.append(pdf_nonres_shape_postfit)
     for p in options.pdfz.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsz.append(args[p])

     allpdfsx = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsx.append(pdf_nonres_shape_prefit)
     allpdfsx.append(pdf_nonres_shape_postfit)
     for p in options.pdfx.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsx.append(args[p])

     allpdfsy = [] #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsy.append(pdf_nonres_shape_prefit)
     allpdfsy.append(pdf_nonres_shape_postfit)
     for p in options.pdfy.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsy.append(args[p])
      
     print
    
     norm = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
     #norm = (args["pdf_binJJ_"+purity+"_13TeV_bonly"].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_proc_nonRes"].getVal()
     print "norm after fit "+str(norm)
     
     
     #################################################
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
     print "x bins reduced:"
     print xBins_redux
     print "y bins reduced:"
     print yBins_redux
     print "z bins reduced:"
     print zBins_redux
     print 
     print
     print "saving ... "
     print
     (args[pdfName].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].dump()     
     norm_nonres = [0,0]
     norm_nonres[0] = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getVal()
     norm_nonres[1] = (args["pdf_binJJ_"+purity+"_13TeV_%s_bonly"%options.year].getComponents())["n_exp_binJJ_"+purity+"_13TeV_%s_proc_nonRes"%options.year].getPropagatedError(fitresult)
          
     save_shape(pdf_nonres_shape_postfit,norm_nonres,options.sample)
     if options.merge: merge_all()
     #################################################     
     #make projections onto MJJ axis
     if options.projection =="z": doZprojection(allpdfsz,data,norm)
         
     #make projections onto MJ1 axis
     if options.projection =="x": doXprojection(allpdfsx,data,norm)
                  
     #make projections onto MJ2 axis
     if options.projection =="y": doYprojection(allpdfsy,data,norm)
         
     if options.projection =="xyz":
        doZprojection(allpdfsz,data,norm)
        doXprojection(allpdfsx,data,norm)
        doYprojection(allpdfsy,data,norm)
     
     #################################################   
     # #calculate chi2
    #  chi2 = getChi2fullModel(pdf_shape_postfit,data,norm)
    #  print "Chi2/ndof: %.2f/%.2f"%(chi2[0],chi2[1])," = %.2f"%(chi2[0]/chi2[1])," prob = ",ROOT.TMath.Prob(chi2[0], int(chi2[1]))
    #
