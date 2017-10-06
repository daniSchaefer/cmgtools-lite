import ROOT
import os,sys
sys.path.append(os.path.abspath("/usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/python/plotting/"))
from PlotterBase import *
from TreePlotter import *
from MergedPlotter import *
ROOT.gROOT.SetBatch(True)


def plotTwoHistos(hist1,hist2,outname,dolog=False ,hist3=0,label=""):
    c= ROOT.TCanvas("c","c",400,400)
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetLineWidth(2)
    hist2.SetLineColor(ROOT.kRed)
    hist2.SetLineWidth(2)
    hist1.Draw("hist")
    if hist3!=0:
        hist3.SetLineColor(ROOT.kGreen)
        hist3.SetLineWidth(2)
        hist3.Draw("histsame")
    hist2.Draw("histsame")
    
    leg = ROOT.TLegend(0.2,0.8,0.7,0.9)
    leg.AddEntry(hist1,"nominal","l")
    leg.AddEntry(hist2,'kernel',"l")
    if hist3!=0:
        leg.AddEntry(hist3,'smoothed kernel',"l")
    leg.Draw("same")
    if dolog:
        c.SetLogy()
    text = ROOT.TLatex() 
    if label.find("mjet")!=-1:
        text.DrawLatex(1100,0.003,label)
    else:
        text.DrawLatex(32,0.01,label)
    c.SaveAs("2DKernel/"+outname)
    
    

    

#Q: why does the kernel only go up to 5000 GeV in MVV?

#x-Axis : MVV spectrum   => projection X gives the projection of m_jet along the MVV axis
#y-Axis : mjet spectrum  => projection Y gives the projection of MVV along the m_jet dimension   



if __name__=="__main__":
    cuts={}
    fromkernel = "JJ_nonRes_2D_HP_withoutTailSmoothing.root"
    fromsample = "samples/QCD_Pt-15to7000"
    f = ROOT.TFile(fromkernel,"READ")
    fromkernel = "JJ_nonRes_2D_HP.root"
    f2 = ROOT.TFile(fromkernel,"READ")
    
    cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.)'

    cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
    minMJJ=30.0
    maxMJJ=610.0

    minMVV=1000.0
    maxMVV=7000.0

    binsMJJ=290
    binsMVV=160

    cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
    cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'
    cuts['nonres'] = '1'
    cut='*'.join([cuts['common'],cuts['nonres'], '(jj_l1_softDrop_mass>30&&jj_l1_softDrop_mass<610)','(jj_LV_mass>1000&&jj_LV_mass<7000)',cuts['HP'],'(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'])
    
    dataPlotters=[]
    dataPlottersNW=[]
    dataPlotters.append(TreePlotter(fromsample+'.root','tree'))
    dataPlotters[-1].setupFromFile(fromsample+'.pck')
    dataPlotters[-1].addCorrectionFactor('xsec','tree')
    dataPlotters[-1].addCorrectionFactor('genWeight','tree')
    dataPlotters[-1].addCorrectionFactor('puWeight','tree')
    data=MergedPlotter(dataPlotters)
    sampleHisto=dataPlotters[0].drawTH2("jj_l1_gen_softDrop_mass:jj_LV_mass",cut,"1",binsMVV,minMVV,maxMVV,binsMJJ,minMJJ,maxMJJ,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
    
    sampleHisto1Dmjet=dataPlotters[0].drawTH1('jj_l1_softDrop_mass',cut,"1",binsMJJ,minMJJ,maxMJJ)
    sampleHisto1Dmjet.Scale(1/sampleHisto1Dmjet.Integral())
    print sampleHisto
     
     
     
     
     
    
    # get sample histo from somewhere else:
    
    #fromsample = "JJ_nonRes_COND2D_HP.root"
    #fnew = ROOT.TFile(fromsample,"READ")
    #sampleHisto= fnew.Get("mjet_mvv_nominal")
    
    
    
    
     
    kernelHisto = f.Get("histo_nominal")
    kernelHisto.SetName("histo_nominal_old")
    kernelHisto2 = f2.Get("histo_nominal")
    
    
    print kernelHisto
    print kernelHisto2
    print f
    Nx = kernelHisto.GetNbinsX()
    Ny = kernelHisto.GetNbinsY()
    kernelHisto.GetXaxis().SetTitle("MVV (GeV)")
    kernelHisto.GetYaxis().SetTitle("m_{jet} (GeV)")
    print Nx
    print Ny
    for i in range(1,Ny+1):
        proj = kernelHisto.ProjectionX("projx",i,i)
        proj3 = kernelHisto2.ProjectionX("projx3",i,i)
        proj2 = sampleHisto.ProjectionX("projx2",i,i)
        proj2.Scale(1/proj2.Integral())
        proj3.Scale(1/proj3.Integral())
        proj.Scale(1/proj.Integral())
        #proj2.SetAxisRange(0.,1,"Y")
        proj2.SetMinimum(0.00000001)
        label = "mjet "+str(round(kernelHisto.GetYaxis().GetBinCenter(i),1))
        plotTwoHistos(proj2,proj,"ProjInMjetBin"+str(i)+"overMVV.pdf",True,proj3,label)
    for i in range(1,Nx+1):
        proj = kernelHisto.ProjectionY("projy",i,i)
        proj3 = kernelHisto2.ProjectionY("projy3",i,i)
        proj2 = sampleHisto.ProjectionY("projy2",i,i)
        label = "mVV "+str(round(kernelHisto.GetXaxis().GetBinCenter(i),1))
        if proj.Integral()!=0 and proj2.Integral()!=0:
            proj2.Scale(1/proj2.Integral())
            proj.Scale(1/proj.Integral())
            proj3.Scale(1/proj3.Integral())
            plotTwoHistos(proj2,proj,"ProjInMVVBin"+str(i)+"overMjet.pdf",False,proj3,label)
        
        
    proj = kernelHisto.ProjectionX("projx")
    proj3 = kernelHisto2.ProjectionX("projx3")
    proj2 = sampleHisto.ProjectionX("projx2")
    proj2.Scale(1/proj2.Integral())
    proj.Scale(1/proj.Integral())
    proj3.Scale(1/proj3.Integral())
    plotTwoHistos(proj2,proj,"ProjInMjetoverMVV.pdf",True,proj3)
    
    proj = kernelHisto.ProjectionY("projy")
    proj2 = sampleHisto.ProjectionY("projy2")
    print proj2.Integral()
    print proj.Integral()
    proj2.Scale(1/proj2.Integral())
    proj.Scale(1/proj.Integral())
    plotTwoHistos(proj2,proj,"ProjInMVVoverMjet.pdf")
        
        
        
        
        
        
        
        
        
        
