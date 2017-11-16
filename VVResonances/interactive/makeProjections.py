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
    
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
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
    fromkernel = "JJ_nonRes_2D_HP_allShapesJen.root"
    fromsample = "QCD_Pt_"
    
    sampleTypes = [fromsample]
    #fromsample = "samples/QCD_pythia"
    f = ROOT.TFile(fromkernel,"READ")
    fromkernel =  'JJ_nonRes_2D_HP_valerieSpeedup1.root'#"JJ_nonRes_2D_HP.root"
    f2 = ROOT.TFile(fromkernel,"READ")
  
    
    cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.)'

    cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
    minMJJ=30.0
    maxMJJ=610.0

    minMVV=1000.0
    maxMVV=6000.0

    binsMJJ=290
    binsMVV=160

    cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
    cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'
    cuts['nonres'] = '1'
    cut='*'.join([cuts['common'],cuts['nonres'], '(jj_l1_softDrop_mass>30&&jj_l1_softDrop_mass<610)','(jj_LV_mass>1000&&jj_LV_mass<7000)',cuts['HP'],'(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'])
    
    dataPlotters=[]
    dataPlottersNW=[]
    
    for filename in os.listdir("samples/"):
     for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            print fname
            dataPlotters.append(TreePlotter("samples/"+fname+'.root','tree'))
            dataPlotters[-1].setupFromFile("samples/"+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')
    data=MergedPlotter(dataPlotters)
        
    print dataPlotters    
    sampleHisto=dataPlotters[0].drawTH2("jj_l1_softDrop_mass:jj_LV_mass",cut,"1",binsMVV,minMVV,maxMVV,binsMJJ,minMJJ,maxMJJ,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" )
    for plotter in dataPlotters:
        print "add histos " 
        sampleHisto.Add(plotter.drawTH2("jj_l1_softDrop_mass:jj_LV_mass",cut,"1",binsMVV,minMVV,maxMVV,binsMJJ,minMJJ,maxMJJ,"M_{qV} mass","GeV","Softdrop mass","GeV","COLZ" ))
    
    sampleHisto.SetFillColor(0)
    
    sampleHisto1Dmjet=dataPlotters[0].drawTH1('jj_LV_mass',cut,"1",binsMVV,minMVV,maxMVV)
    sampleHisto1Dmjet.Scale(1/sampleHisto1Dmjet.Integral())
    sampleHistogen1Dmjet=dataPlotters[0].drawTH1('jj_gen_partialMass',cut,"1",binsMVV,minMVV,maxMVV)
    sampleHistogen1Dmjet.Scale(1/sampleHistogen1Dmjet.Integral())
    
    kernelHisto = f.Get("histo_nominal")
    kernelHisto.SetName("histo_nominal_old")
    kernelHisto2 = f2.Get("histo_nominal")
    
    proj = kernelHisto.ProjectionX("projx")
    proj3 = kernelHisto2.ProjectionX("projx3")
    proj.Scale(1/proj.Integral())
    proj3.Scale(1/proj3.Integral())
    
    
    v = ROOT.TCanvas("c","c",800,400)
    p0 = kernelHisto2.ProjectionY("p0",1,5)
    p0s= sampleHisto.ProjectionY("p0s",1,5)
    p1 = kernelHisto2.ProjectionY("p1",5,100)
    p1s= sampleHisto.ProjectionY("p1s",5,100)
    p2 = kernelHisto2.ProjectionY("p2",100,200)
    p2s= sampleHisto.ProjectionY("p2s",100,200)
    
    
    test = ROOT.TFile("JJ_nonRes_HP_kernels.root")
    p0 =  test.Get("histo1D_nominal")
    test2 = ROOT.TFile("JJ_nonRes_MJJ_HP.root")
    p0s = test2.Get("histo_nominal")
    p1 = sampleHisto.ProjectionY("p0s",1,5)
    
    
    p0 .SetLineColor(ROOT.kBlack) 
    p0s.SetLineColor(ROOT.kBlack) 
    p1 .SetLineColor(ROOT.kRed) 
    p1s.SetLineColor(ROOT.kRed) 
    p2 .SetLineColor(ROOT.kBlue) 
    p2s.SetLineColor(ROOT.kBlue) 
    
    p0 .Scale(1/p0 .Integral())
    p0s.Scale(1/p0s.Integral())
    p1 .Scale(1/p1 .Integral())
    p1s.Scale(1/p1s.Integral())
    p2 .Scale(1/p2 .Integral())
    p2s.Scale(1/p2s.Integral())

    
    
    p0 .Draw("hist")
    p0s.Draw("histsame")
    p1 .Draw("histsame")
    p1s.Draw("histsame")
    p2 .Draw("histsame")
    p2s.Draw("histsame")
    
    lb0 = "mVV "+str(round(kernelHisto2.GetXaxis().GetBinCenter(1),1))+" "+str(round(kernelHisto2.GetXaxis().GetBinCenter(5),1))
    lb1 = "mVV "+str(round(kernelHisto2.GetXaxis().GetBinCenter(5),1))+" "+str(round(kernelHisto2.GetXaxis().GetBinCenter(100),1))
    lb2 = "mVV "+str(round(kernelHisto2.GetXaxis().GetBinCenter(100),1))+" "+str(round(kernelHisto2.GetXaxis().GetBinCenter(200),1))
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
    leg.AddEntry(p0,lb0,"l")
    leg.AddEntry(p1,lb1,"l")
    leg.AddEntry(p2,lb2,"l")
    leg.Draw("same")
    v.SaveAs("mjet_histosFromDataset.pdf")
     
    
   
     
     
    
    ## get sample histo from somewhere else:
    
    ##fromsample = "JJ_nonRes_COND2D_HP.root"
    ##fnew = ROOT.TFile(fromsample,"READ")
    ##sampleHisto= fnew.Get("mjet_mvv_nominal")
    
    
    
    
     
    
    
    print kernelHisto
    print kernelHisto2
    print f
    Nx = kernelHisto.GetNbinsX()
    Ny = kernelHisto.GetNbinsY()
    kernelHisto.GetXaxis().SetTitle("MVV (GeV)")
    kernelHisto.GetYaxis().SetTitle("m_{jet} (GeV)")
    kernelHisto.Scale(1/kernelHisto.Integral())
    kernelHisto2.Scale(1/kernelHisto2.Integral())
    sampleHisto.Scale(1/sampleHisto.Integral())
    print Nx
    print Ny
    for i in range(1,Ny+1):
        proj = kernelHisto.ProjectionX("projx",i,i)
        proj3 = kernelHisto2.ProjectionX("projx3",i,i)
        proj2 = sampleHisto.ProjectionX("projx2",i,i)
        if proj3.Integral()==0:
           continue
        proj2.Scale(1/proj2.Integral())
        proj3.Scale(1/proj3.Integral())
        proj.Scale(1/proj.Integral())
        proj2.SetAxisRange(0.,1,"Y")
        proj2.SetMinimum(0.00000001)
        label = "mjet "+str(round(kernelHisto.GetYaxis().GetBinCenter(i),1))
        plotTwoHistos(proj2,proj,"ProjInMjetBin"+str(i)+"overMVV.pdf",True,proj3,label)
    for i in range(1,Nx+1):
        proj = kernelHisto.ProjectionY("projy",i,i)
        proj3 = kernelHisto2.ProjectionY("projy3",i,i)
        proj2 = sampleHisto.ProjectionY("projy2",i,i)
        label = "mVV "+str(round(kernelHisto.GetXaxis().GetBinCenter(i),1))
        if proj.Integral()!=0 and proj2.Integral()!=0 and proj3.Integral()!=0:
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
    proj3 = kernelHisto2.ProjectionY("projx3")
    print proj2.Integral()
    print proj.Integral()
    proj2.Scale(1/proj2.Integral())
    proj.Scale(1/proj.Integral())
    proj3.Scale(1/proj3.Integral())
    plotTwoHistos(proj2,proj,"ProjInMVVoverMjet.pdf",False,proj3)
        
        
        
        
        
        
        
        
        
        
