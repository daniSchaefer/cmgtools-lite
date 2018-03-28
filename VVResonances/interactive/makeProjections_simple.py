import ROOT
import os,sys
ROOT.gROOT.SetBatch(True)




def plotTwoHisto(hist1,outname,dolog=False, label="",nominal=0):
    c= ROOT.TCanvas("c","c",400,400)
    hist1.SetLineColor(ROOT.kBlue)
    hist1.SetLineWidth(2)
    if nominal!=0:
        nominal.SetLineWidth(2)
        nominal.SetLineColor(ROOT.kRed)
        hist1.Draw("hist")
        nominal.Draw("histsame")
    else:
        hist1.Draw("hist")
    
    leg = ROOT.TLegend(0.5,0.8,0.7,0.9)
    leg.AddEntry(hist1,"smoothed","l")
    leg.AddEntry(nominal,"nominal","l")
    leg.Draw("same")
    if dolog:
        c.SetLogy()
    text = ROOT.TLatex() 
    if label.find("mjet")!=-1:
        text.DrawLatex(1100,0.003,label)
    else:
        text.DrawLatex(32,0.01,label)
    #nominal.Draw("hist")
    c.SaveAs("2DKernel/"+outname)

def conditional(hist):
    print "make conditional of histo"
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)


if __name__=="__main__":

    fromkernel = "JJ_nonRes_HPHP.root" #'JJ_pythia_tails3D_nonRes_2D_HPHP.root'#'test_HPHP.root' 'JJ_nonRes_2D_HPHP.root' #'JJ_nonRes_COND2D_HPHP_l1.root'#"JJ_nonRes_2D_HP.root"
    f2 = ROOT.TFile(fromkernel,"READ")
    f3 = ROOT.TFile("JJ_WJets_HPHP.root","READ")
    f4 = ROOT.TFile("JJ_ZJets_HPHP.root","READ")
    h1 = f2.Get("nonRes")
    h2 = f3.Get("WJets")
    h3 = f4.Get("ZJets")
    hcombined = h1.Clone("combined")
    hcombined.Add(h2)
    hcombined.Add(h3)
    
    kernelHisto=hcombined
    hn = h1
    #kernelHisto.Scale(dataHisto.Integral()/kernelHisto.Integral())
    #dataHisto.Scale(1)
    ##conditional(dataHisto)
    ##conditional(kernelHisto)
    
    #print dataHisto.Integral()
    #print kernelHisto.Integral()
    
    #c = ROOT.TCanvas("test","test",800,400)
    #c.Divide(2,1)
    #c.cd(1)
    #c.SetRightMargin(0.25)
    #dataHisto.Draw("colz")
    #c.cd(2)
    #c.SetRightMargin(0.25)
    #kernelHisto.Draw("colz")
    #c.SaveAs("testconditional.pdf")
    
    
    ##oneD = ROOT.TFile("/home/dschaefer/tmp/JJ_nonRes_MVV_HPLP.root","READ")
    #oneD = ROOT.TFile("JJ_testGaussianKernel_nonRes_MVV_HPHP.root","READ")
    #oneDdata = oneD.Get("mvv_nominal")
    #oneDhisto = oneD.Get("histo_nominal")
    #plotTwoHisto(oneDhisto,"mVV.pdf",True,"",oneDdata)
    
    
    ## load nominal samples to plot also in the same plot:
    ##fn = ROOT.TFile("JJ_tau21DDT_nonRes_2D_HPHP.root","READ")
    ##hn = fn.Get("histo")
    ############## for 3D histograms 
    
    Nx = kernelHisto.GetNbinsX()
    Ny = kernelHisto.GetNbinsY()
    Nz = kernelHisto.GetNbinsZ()

    for i in range(1,Ny+1):
        pn = hn.ProjectionX("pnx",i,i,0,-1)
        proj = kernelHisto.ProjectionX("projx",i,i,0,-1)
        label = "mjet "+str(round(kernelHisto.GetYaxis().GetBinCenter(i),1))
        plotTwoHisto(proj,"XprojectionYbin"+str(i)+".pdf",False,label,pn)
    for j in range(1,Nx+1):
        pny = hn.ProjectionY("pny",j,j,0,-1)
        projy = kernelHisto.ProjectionY("projy",j,j,0,-1)
        label = "mVV "+str(round(kernelHisto.GetXaxis().GetBinCenter(j),1))
        plotTwoHisto(projy,"YprojectionXbin"+str(j)+".pdf",False,label,pny) 

    xlist = [1,10,20,30,40,50,60,70,80 ]
    ylist = xlist


    for x in range(2,len(xlist)):
        for y in range(2,len(ylist)):
    #for z in range(1,Nx+1):
    #    for z2 in range(z,Ny+1):
            pnz  = hn.ProjectionZ("pnz",xlist[x-1],xlist[x],ylist[y-1],ylist[y])
            projz = kernelHisto.ProjectionZ("projz",xlist[x-1],xlist[x],ylist[y-1],ylist[y])
            plotTwoHisto(projz,"ZprojectionXbin"+str(x)+"Ybin"+str(y)+".pdf",True,"",pnz)
            
    for z in range(1,Nz):
            pnzx = hn.ProjectionX("pnzx",0,-1,z,z)
            pnzy = hn.ProjectionY("pnzy",0,-1,z,z)
        
            projzTox = kernelHisto.ProjectionX("projzTox",0,-1,z,z)
            projzToy = kernelHisto.ProjectionY("projzToy",0,-1,z,z)
            plotTwoHisto(projzTox,"ZtoX_Zbin"+str(z)+"YbinAll.pdf",False,"",pnzx)
            plotTwoHisto(projzToy,"ZtoY_Zbin"+str(z)+"XbinAll.pdf",False,"",pnzy)


    pnx = hn.ProjectionX("pnx")
    px = kernelHisto.ProjectionX("x")
    plotTwoHisto(px,"XprojectionYbinAll.pdf",False,"",pnx)
    
    pny = hn.ProjectionY("pny")
    py = kernelHisto.ProjectionY("y")
    plotTwoHisto(py,"YprojectionXbinAll.pdf",False,"",pny)
    
    pnz = hn.ProjectionZ("pnz")
    pz = kernelHisto.ProjectionZ("z")
    plotTwoHisto(pz,"ZprojectionXYbinAll.pdf",True,"",pnz)
    
    
    #################### for 2D histograms 
    
    #Nx = kernelHisto.GetNbinsX()
    #Ny = kernelHisto.GetNbinsY()
    
    #for i in range(1,Ny+1):
        #proj = kernelHisto.ProjectionX("projx",i,i)
        #hist2 = dataHisto.ProjectionX("projxdata",i,i)
        ##hist2.GetXaxis().SetRangeUser(40,225)
        #label = "mjet "+str(round(kernelHisto.GetYaxis().GetBinCenter(i),1))
        #plotTwoHisto(proj,"XprojectionYbin"+str(i)+".pdf",False,label,hist2)
    #for j in range(1,Nx+1):
        #projy = kernelHisto.ProjectionY("projy",j,j)
        #hist2 = dataHisto.ProjectionY("projydata",j,j)
        #label = "mVV "+str(round(kernelHisto.GetXaxis().GetBinCenter(j),1))
        #plotTwoHisto(projy,"YprojectionXbin"+str(j)+".pdf",True,label,hist2) 


    #px = kernelHisto.ProjectionX("x")
    #hist2 = dataHisto.ProjectionX("projxdata")
    #px.Scale(1/px.Integral())
    #hist2.Scale(1/hist2.Integral())
    #plotTwoHisto(px,"Xprojection.pdf",False,"",hist2)
   
    #hist2 = dataHisto.ProjectionY("projydata")    
    #py = kernelHisto.ProjectionY("y")
    #py.Scale(1/py.Integral())
    #hist2.Scale(1/hist2.Integral())
    #plotTwoHisto(py,"Yprojection.pdf",True,"",hist2)
    
   
