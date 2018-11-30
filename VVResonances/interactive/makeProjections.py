import ROOT
import os,sys
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetLegendBorderSize(0)

def plotStack(backgrounds,xrange,yrange,zrange,projection,purity):
    c = getCanvas()
    leg = ROOT.TLegend(0.1,0.92,0.3,0.7)
    if projection == "z":
        leg = ROOT.TLegend(0.6,0.92,0.9,0.7)
    leg.SetTextFont(42)
    
    p_bkg =[]
    labels  =[]
    stack = ROOT.THStack("stackplot","stackplot")
    for bkg in backgrounds:
        print " make projection of histogram "+str(bkg.GetName())
        if projection == "x":
            print "zrange "+str(zrange[0][1]) + " to "+str(zrange[0][2])
            p = makeProjections(bkg,yrange[0],zrange[0],projection,bkg.GetName().replace("_all",""))
        if projection == "y":
            p = makeProjections(bkg,xrange[0],zrange[0],projection,bkg.GetName().replace("_all",""))
        if projection == "z":
            p = makeProjections(bkg,xrange[0],yrange[0],projection,bkg.GetName().replace("_all",""))
        p_bkg.append(p) 
        if bkg.GetName().find("W")!=-1:
            p.SetFillColor(ROOT.kRed)
            labels.append("W+jets")
        if bkg.GetName().find("Z")!=-1:
            p.SetFillColor(ROOT.kGreen)
            labels.append("Z+jets")
        if bkg.GetName().find("tt")!=-1:
            p.SetFillColor(ROOT.kBlue)
            labels.append("t#bar{t}+jets")
        if bkg.GetName().find("nonRes")!=-1:
            p.SetFillColor(ROOT.kGray)
            labels.append("qcd multijet")
        stack.Add(p)
        leg.AddEntry(p,labels[-1],"f")
    
    addText = ROOT.TLatex()
    addText.SetTextFont(42)
    label_proj_2 = str(yrange[0][1])+" < #rho_{jet2} < "+str(yrange[0][2])
    label_proj_1 = str(xrange[0][1])+" < #rho_{jet1} < "+str(xrange[0][2])
    label_proj_3 = str(zrange[0][1])+" < m_{jj} < "    +str(zrange[0][2])+" GeV"

    
    stack.Draw("hist")
    stack.GetXaxis().SetTitle("#rho_{jet1}")
    stack.GetYaxis().SetTitle("# events")
    stack.GetYaxis().SetTitleOffset(1.5)
    leg.Draw("same")
    if projection=="z":
        c.SetLogy()
        addText.DrawLatexNDC(0.6,0.65,"#scale[0.8]{"+label_proj_1+"}")
        addText.DrawLatexNDC(0.6,0.6,"#scale[0.8]{"+label_proj_2+"}")
        
    else:
        addText.DrawLatexNDC(0.12,0.65,"#scale[0.8]{"+label_proj_2+"}")
        addText.DrawLatexNDC(0.12,0.6,"#scale[0.8]{"+label_proj_3+"}")
    c.SaveAs("CP_background_p"+projection+"_xrange"+str(xrange[0][1])+"-"+str(xrange[0][2])+"_yrange"+str(yrange[0][1])+"-"+str(yrange[0][2])+"zrange"+str(zrange[0][1])+"-"+str(zrange[0][2])+"_"+purity+".pdf")





def plotHistos(hists,outname,label,dolog=False,data=None,scales=None):
    colors=[ROOT.kBlack,ROOT.kBlue,ROOT.kRed,ROOT.kGreen,ROOT.kPink,ROOT.kOrange,ROOT.kGreen+2,ROOT.kGray]
    
    if scales!=None:
        for s in range(0,len(scales)):
            hists[s].Scale(scales[s])
            data[s].Scale(scales[s])
    
    c= getCanvas()
    leg = ROOT.TLegend(0.1,0.92,0.4,0.6)
    if dolog == True:
        leg = ROOT.TLegend(0.6,0.92,0.9,0.6)
    leg.SetTextFont(42)
    i=0
    for h in hists:
        h.SetMaximum(0.07)
        if outname.find("HPLP")!=-1:
            h.SetMaximum(1.0)
        if dolog == True:
            h.SetMaximum(10)
        h.SetLineColor(colors[i])
        h.SetLineWidth(2)
        leg.AddEntry(h,label[i],"l")
        h.Draw("histsame")
        i+=1
    leg.Draw("same")
    if dolog:
        c.SetLogy()
       
       
    if data!=None:
        i=0
        for d in data:
            d.SetLineColor(colors[i])
            d.SetMarkerColor(colors[i])
            d.SetMarkerStyle(1)
            d.Draw("PEsame")
            i+=1
            

    #text = ROOT.TLatex() 
    #if label.find("mjet")!=-1:
    #    text.DrawLatex(1100,0.003,label)
    #else:
    #    text.DrawLatex(32,0.01,label)
    c.SaveAs(outname)
    
  
def getCanvas(w=800,h=600):
    c1 = ROOT.TCanvas("c","",w,h)
    c1.SetBottomMargin(0.15)
    c1.SetTopMargin(0.08)
    c1.SetRightMargin(0.08)
    return c1

  
  
  
  
  
def findBins(histo,axis,r):
    if r == 0:
        return 0
    if r == -1:
        return -1
    if axis=="x":
        p = histo.ProjectionX("tmp")
        N = histo.GetNbinsX()
    if axis=="y":
        p = histo.ProjectionY("tmp")
        N = histo.GetNbinsY()
    if axis=="z":
        p = histo.ProjectionZ("tmp")
        N = histo.GetNbinsZ()
        
        
    for i in range(0,N+1):
        if ( r >= p.GetBinLowEdge(N-i)):
           return N-i


def makeProjections(histo,range1,range2,axis,label):
    if axis=="x":
        print findBins(histo,"z",range2[2])
        p = histo.ProjectionX(label,findBins(histo,"y",range1[1]),findBins(histo,"y",range1[2]),findBins(histo,"z",range2[1]),findBins(histo,"z",range2[2]))
        p.GetXaxis().SetTitle("#rho_{jet1}")
        p.GetYaxis().SetTitleOffset(1.5)
        p.GetYaxis().SetTitle("# events")
        return p
    if axis=="y":
        p = histo.ProjectionY(label,findBins(histo,"x",range1[1]),findBins(histo,"x",range1[2]),findBins(histo,"z",range2[1]),findBins(histo,"z",range2[2]))
        p.GetXaxis().SetTitle("#rho_{jet2}")
        p.GetYaxis().SetTitleOffset(1.5)
        p.GetYaxis().SetTitle("# events")
        return p
    if axis== "z":
        print "z projection "
        p = histo.ProjectionZ(label,findBins(histo,"x",range1[1]),findBins(histo,"x",range1[2]),findBins(histo,"y",range2[1]),findBins(histo,"y",range2[2]))
        p.GetXaxis().SetTitle("m_{jj}")
        p.GetYaxis().SetTitleOffset(1.5)
        p.GetYaxis().SetTitle("# events")
        return p
    
    


#z-Axis : MVV spectrum   => projection X gives the projection of m_jet along the MVV axis
#y-Axis : mjet spectrum  => projection Y gives the projection of MVV along the m_jet dimension 
#x-Axis : mjet spectrum  => projection Y gives the projection of MVV along the m_jet dimension 



if __name__=="__main__":
    f_kernel = ROOT.TFile(sys.argv[1],"READ")
    f_sample = ROOT.TFile(sys.argv[2],"READ")
    
    purity = "HPHP"
    if sys.argv[1].find("HPLP")!=-1:
        purity = "HPLP"
    if sys.argv[1].find("LPLP")!=-1:
        purity = "LPLP"
  
    kernel = f_kernel.Get("histo")
    sample = f_sample.Get("nonRes")
    print sample.Integral()
    print kernel.Integral()
    kernel.Scale(sample.Integral()/kernel.Integral())
    
    sample.SetFillColor(0)
    
    xrange = [["px0",0,-1],["px1",0,2],["px2",2,3],["px3",3,5]]
    yrange = [["py0",0,-1],["py1",0,2],["py2",2,3],["py3",3,5]]
    zrange = [["pz0",0,-1],["pz1",1000,1300],["pz2",1300,2000],["pz3",2000,5000]]
    
    projections_x =[]
    data_x =[]
    labels_x =[]
    for z in zrange:
        p = makeProjections(kernel,["py",0,-1],z,"x",z[0])
        projections_x.append(p)
        labels_x.append(str(z[1])+" < m_{jj} < "+str(z[2]))
    
        d = makeProjections(sample,["py",0,-1],z,"x",z[0]+"_d")
        data_x.append(d)
    
    scales = [1,1,1.5,10]
    plotHistos(projections_x,"x_projection"+"_"+purity+".pdf",labels_x,False,data_x,scales)
    
    
    
    projections_y =[]
    data_y =[]
    labels_y =[]
    for z in zrange:
        p = makeProjections(kernel,["px",0,-1],z,"y",z[0])
        projections_y.append(p)
        labels_y.append(str(z[1])+" < m_{jj} < "+str(z[2]))
    
        d = makeProjections(sample,["px",0,-1],z,"y",z[0]+"_d")
        data_y.append(d)
    
    scales = [1,1,1.5,10]
    plotHistos(projections_y,"y_projection"+"_"+purity+".pdf",labels_y,False,data_y,scales)
    
    
    projections_z =[]
    data_z =[]
    labels_z =[]
    for j in range(0,len(xrange)):
        p = makeProjections(kernel,xrange[j],yrange[j],"z",zrange[j][0])
        projections_z.append(p)
        labels_z.append(str(xrange[j][1])+" < #rho_{jet1/2} < "+str(xrange[j][2]))
    
        d = makeProjections(sample,xrange[j],yrange[j],"z",zrange[j][0]+"_d")
        data_z.append(d)
    print projections_z
    scales = [1,1,1,1]
    plotHistos(projections_z,"z_projection"+"_"+purity+".pdf",labels_z,True,data_z,scales)
    
        
        
   ############### make controlplots of QCD alternative shapes ####################
    kernel_OPTXYup = f_kernel.Get("histo_OPT2XYUp")
    kernel = f_kernel.Get("histo")
    kernel_OPTXYdown = f_kernel.Get("histo_OPT2XYDown")
    
    kernel_PTup = f_kernel.Get("histo_OPTXYUp")
    kernel_PTdown = f_kernel.Get("histo_OPTXYDown")
    
    kernel_PTZup   = f_kernel.Get("histo_PTZUp")
    kernel_PTZdown = f_kernel.Get("histo_PTZDown")
    
    kernel_OPTZup   = f_kernel.Get("histo_OPTZUp")
    kernel_OPTZdown = f_kernel.Get("histo_OPTZDown")
    
    kernel_varBinUp   = f_kernel.Get("histo_varBin1ZUp")
    
    kernel_varBinDown   = f_kernel.Get("histo_varBin1ZDown")
    
    xrange = [["px0",0,-1]]
    yrange = [["py0",0,-1]]
    zrange = [["pz0",0,-1]]
    
    p_XY=[]
    XY =[kernel,kernel_OPTXYup,kernel_OPTXYdown,kernel_PTup,kernel_PTdown,kernel_varBinUp,kernel_varBinDown]
    labels_XY =[]    
    for hist in XY:
        print " make projection of histogram "+str(hist.GetName())
        p = makeProjections(hist,yrange[0],zrange[0],"x",hist.GetName())    
        p_XY.append(p)    
        labels_XY.append(hist.GetName().replace("histo_",""))

    plotHistos(p_XY,"qcd_altenate_shapes_X"+"_"+purity+".pdf",labels_XY,False)
    p_XY=[]
    labels_XY =[]   
    for hist in XY:
        print " make projection of histogram "+str(hist.GetName())
        p = makeProjections(hist,xrange[0],zrange[0],"y",hist.GetName())    
        p_XY.append(p)    
        labels_XY.append(hist.GetName().replace("histo_",""))

    plotHistos(p_XY,"qcd_altenate_shapes_Y"+"_"+purity+".pdf",labels_XY,False)
    
    
    
    p_Z=[]
    labels_Z =[] 
    Z =[kernel,kernel_OPTZup,kernel_OPTZdown,kernel_PTZup,kernel_PTZdown,kernel_varBinUp,kernel_varBinDown]
    for hist in Z:
        hist.Scale(1/hist.Integral())
        print " make projection of histogram "+str(hist.GetName())
        p = makeProjections(hist,xrange[0],yrange[0],"z",hist.GetName())    
        p_Z.append(p)    
        labels_Z.append(hist.GetName().replace("histo_",""))

    plotHistos(p_Z,"qcd_altenate_shapes_Z"+"_"+purity+".pdf",labels_Z,True)   
    
    print kernel_varBinUp.Integral()
    ############## make stackplots of all backgrounds ####################
    
    #f_Wjets  = ROOT.TFile("JJ_WJets_all_"+purity+".root","READ")
    #f_Zjets  = ROOT.TFile("JJ_ZJets_all_"+purity+".root","READ")
    #f_ttjets = ROOT.TFile("JJ_ttJets_all_"+purity+".root","READ")
    
    #qcd = f_sample.Get("nonRes")
    #Wjets = f_Wjets.Get("WJets_all")
    #Zjets = f_Zjets.Get("ZJets_all")
    #ttbar = f_ttjets.Get("ttJets_all")
    #qcd  .SetName("nonRes")
    #Wjets.SetName("WJets_all")
    #Zjets.SetName("ZJets_all")
    #ttbar.SetName("ttJets_all")
    
    #lumi = 35900.
    #qcd  .Scale(lumi)
    #Wjets.Scale(lumi)
    #Zjets.Scale(lumi)
    #ttbar.Scale(lumi)
    
    #print qcd
    #print Wjets
    #print Zjets
    #print ttbar
    
    #xrange = [["px0",0,5]]
    #yrange = [["py0",0,5]]
    #zrange = [["pz0",1000,5000]]
    
    #backgrounds = [Wjets,Zjets,ttbar,qcd]
    
    #plotStack(backgrounds,xrange,yrange,zrange,"x",purity)
    #plotStack(backgrounds,xrange,yrange,zrange,"y",purity)
    #plotStack(backgrounds,xrange,yrange,zrange,"z",purity)

    
    
    
    
    
    
    
