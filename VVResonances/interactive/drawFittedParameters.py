from ROOT import TFile, TCanvas, TPaveText, TLegend, gDirectory, TH1F,gROOT,gStyle, TLatex
import sys,copy
import tdrstyle
tdrstyle.setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *

from time import sleep
gROOT.SetBatch(True)
# infile = sys.argv[1]
# f = TFile(infile,"READ")

path = "/eos/user/t/thaarres/www/vvana/3D_latest/signalFits/"
cols = [46,30]
colors = ["#4292c6","#41ab5d","#ef3b2c","#ffd300","#fdae61","#abd9e9","#2c7bb6"]
mstyle = [8,4]

def beautify(h1,color,linestyle=1,markerstyle=8):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    # h1.SetFillColor(color)
    h1.SetLineWidth(3)
    h1.SetLineStyle(linestyle)
    h1.SetMarkerStyle(markerstyle)
    
def getLegend(x1=0.70010112,y1=0.123362,x2=0.90202143,y2=0.279833):
  legend = TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend

def getPavetext():
  addInfo = TPaveText(0.3010112,0.2066292,0.4202143,0.3523546,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  return addInfo
    
def getCanvas(w=800,h=600):
    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H = H_ref
    
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    c=TCanvas("c","c",50,50,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( 1.2*B/H )
    c.SetTickx(0)
    c.SetTicky(0)
    c.GetWindowHeight()
    c.GetWindowWidth()
    # c.SetLogy()
    # c.SetGrid()
    return c
    

def doSignalEff():
    gStyle.SetOptFit(0)
    signals = ["ZprimeWW","BulkGWW","WprimeWZ","BulkGZZ"]
    titles =  ["Z' #rightarrow WW","G_{B}#rightarrow WW","W' #rightarrow WZ","G_{B}#rightarrow ZZ"]
    fitsHP=[]
    fitsLP=[]
    datasHP=[]
    datasLP=[]
    
    
    c = getCanvas()
    l = getLegend(0.7788945,0.723362,0.9974874,0.879833)
    l2 = getLegend(0.7788945,0.1783217,0.9974874,0.2482517)
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    
    filesHP=[]
    filesLP=[]

    for i,s in enumerate(signals):
        filesLP.append(TFile("JJ_"+s+"_HPLP_yield_eff.root","READ"))
        filesHP.append(TFile("JJ_"+s+"_HPHP_yield_eff.root","READ"))
    
    for i,(fHP,fLP) in enumerate(zip(filesHP,filesLP)):
        print fLP.GetName()
        gHPLP = fLP.Get("yield")
        gHPHP = fHP.Get("yield")
        fHPLP = gHPLP.GetFunction("func")
        fHPHP = gHPHP.GetFunction("func")
        gHPLP.GetFunction("func").SetBit(rt.TF1.kNotDraw)
        gHPHP.GetFunction("func").SetBit(rt.TF1.kNotDraw)
        # gHPLP.SetMarkerColor(rt.TColor.GetColor(colors[i]))
        # gHPHP.SetMarkerColor(rt.TColor.GetColor(colors[i]))
        beautify(fHPLP ,rt.TColor.GetColor(colors[i]),9,24)
        beautify(fHPHP ,rt.TColor.GetColor(colors[i]),1,8)
        beautify(gHPLP ,rt.TColor.GetColor(colors[i]),9,24)
        beautify(gHPHP ,rt.TColor.GetColor(colors[i]),1,8)
        datasHP.append(gHPHP)
        datasLP.append(gHPLP)
        fitsHP.append(fHPHP)
        fitsLP.append(fHPLP)
        l.AddEntry(fHPHP,titles[i],"L")
    l2.AddEntry(fitsHP[0],"HPHP","LP")    
    l2.AddEntry(fitsLP[0],"HPLP","LP")    
    fitsHP[0].GetXaxis().SetTitle("M_{X} (GeV)")
    fitsHP[0].GetYaxis().SetTitle("Signal efficiency")
    fitsHP[0].GetYaxis().SetNdivisions(4,5,0)
    fitsHP[0].GetXaxis().SetNdivisions(9,2,0)
    fitsHP[0].GetYaxis().SetTitleOffset(0.97)
    fitsHP[0].GetXaxis().SetTitleOffset(0.94)
    fitsHP[0].GetXaxis().SetRangeUser(1126, 5500.)
    fitsHP[0].GetYaxis().SetRangeUser(0.0, 0.25)
    fitsHP[0].Draw("C")
    for i,(gHP,gLP) in enumerate(zip(datasHP,datasLP)): 
        gLP.Draw("Psame")
        gHP.Draw("Psame")
        fitsHP[i].Draw("Csame")
        fitsLP[i].Draw("Csame")
    c.Update()
    l.Draw("same")
    l2.Draw("same")
    cmslabel_sim_prelim(c,'sim',11)
    c.Update()
    c.SaveAs(path+"signalEff.png")
    c.SaveAs(path+"signalEff.pdf")
    c.SaveAs(path+"signalEff.C")
    
def doJetMass(leg="l1"):
    gStyle.SetOptFit(0)
    signals = ["ZprimeWW","BulkGWW","WprimeWZ","BulkGZZ"]
    titles =  ["Z' #rightarrow WW","G_{B}#rightarrow WW","W' #rightarrow WZ","G_{B}#rightarrow ZZ"]
    # signals = ["BulkGWW","WprimeWZ","BulkGZZ"]
    # titles =  ["G_{B}#rightarrow WW","W' #rightarrow WZ","G_{B}#rightarrow ZZ"]
    filesHP=[]
    filesLP=[]

    for i,s in enumerate(signals):
        filesLP.append(TFile("debug_JJ_"+s+"_MJ%s_HPLP.json.root"%leg,"READ"))
        filesHP.append(TFile("debug_JJ_"+s+"_MJ%s_HPHP.json.root"%leg,"READ"))
    
    vars = ["mean","sigma"]
    vars = ["mean","sigma","alpha","n","alpha2","n2"]
    for var in vars:
        fitsHP=[]
        fitsLP=[]
        datasHP=[]
        datasLP=[]
        
        c = getCanvas()
        l = getLegend(0.7788945,0.723362,0.9974874,0.879833)
        l2 = getLegend(0.7788945,0.1783217,0.9974874,0.2482517)
        l3 = getLegend(0.7788945,0.1783217,0.9974874,0.2482517)
        gStyle.SetOptStat(0)
        gStyle.SetOptTitle(0)
        
        for i,(fHP,fLP) in enumerate(zip(filesHP,filesLP)):
            gHPLP = fLP.Get(var)
            gHPHP = fHP.Get(var)
            fHPLP = fLP.Get(var+"_func")
            fHPHP = fHP.Get(var+"_func")
            gHPLP.GetFunction(var+"_func").SetBit(rt.TF1.kNotDraw)
            gHPHP.GetFunction(var+"_func").SetBit(rt.TF1.kNotDraw)

            beautify(fHPLP ,rt.TColor.GetColor(colors[i]),9,24)
            beautify(fHPHP ,rt.TColor.GetColor(colors[i]),1,8)
            beautify(gHPLP ,rt.TColor.GetColor(colors[i]),9,24)
            beautify(gHPHP ,rt.TColor.GetColor(colors[i]),1,8)
            datasHP.append(gHPHP)
            datasLP.append(gHPLP)
            fitsHP.append(fHPHP)
            fitsLP.append(fHPLP)
            l.AddEntry(fHPHP,titles[i],"L")
        l2.AddEntry(datasHP[0],"HPHP","LP")    
        l2.AddEntry(datasLP[0],"HPLP","LP")    
        datasHP[0].GetXaxis().SetTitle("M_{X} (GeV)")
        datasHP[0].GetYaxis().SetTitle(var+" (GeV)")
        datasHP[0].GetYaxis().SetNdivisions(4,5,0)
        datasHP[0].GetXaxis().SetNdivisions(9,2,0)
        datasHP[0].GetYaxis().SetTitleOffset(0.97)
        datasHP[0].GetXaxis().SetTitleOffset(0.94)
        datasHP[0].GetXaxis().SetRangeUser(1126, 5500.)
        if var == "mean": datasHP[0].GetYaxis().SetRangeUser(70,110)
        if var == "sigma": datasHP[0].GetYaxis().SetRangeUser(0,20)
        if var == "alpha": datasHP[0].GetYaxis().SetRangeUser(0,5)
        if var == "n": datasHP[0].GetYaxis().SetRangeUser(0,4)
        if var == "alpha2": datasHP[0].GetYaxis().SetRangeUser(0,5)
        if var == "n2": datasHP[0].GetYaxis().SetRangeUser(0,4)
        datasHP[0].Draw("AP")
        for i,(gHP,gLP) in enumerate(zip(datasHP,datasLP)): 
            gLP.Draw("Psame")
            gHP.Draw("Psame")
            fitsHP[i].Draw("Csame")
            fitsLP[i].Draw("Csame")
        datasHP[0].GetXaxis().SetRangeUser(1126, 5500.)
        l.Draw("same")
        l2.Draw("same")
        cmslabel_sim_prelim(c,'sim',11)
        pt = getPavetext()
        c.Update()
        c.SaveAs(path+"Signal_mjet%s_"%leg+var+".png")
        c.SaveAs(path+"Signal_mjet%s_"%leg+var+".pdf")
        c.SaveAs(path+"Signal_mjet%s_"%leg+var+".C")
    
def doYield():
    FHPLP = TFile("JJ_"+sys.argv[1]+"_HPLP_yield.root","READ")
    FHPHP = TFile("JJ_"+sys.argv[1]+"_HPHP_yield.root","READ")
    
    vars = ["yield"]
    for var in vars:
        c = getCanvas()
        l = getLegend()
        gStyle.SetOptStat(0)
        gStyle.SetOptTitle(0)
        
        
        gHPLP = FHPLP.Get(var)
        gHPHP = FHPHP.Get(var)
        fHPLP = gHPLP.GetFunction("func")
        fHPHP = gHPHP.GetFunction("func")
        
        beautify(gHPLP ,1,1,8)
        beautify(gHPHP ,1,1,4)
        beautify(fHPLP ,46,1,8)
        beautify(fHPHP ,30,1,4)
        
        l.AddEntry(fHPLP,"HPLP","LP")
        l.AddEntry(fHPHP,"HPHP","LP")
        
        gHPLP.GetXaxis().SetTitle("M_{X} (GeV)")
        gHPLP.GetYaxis().SetTitle(var)
        gHPLP.GetYaxis().SetNdivisions(9,1,0)
        gHPLP.GetYaxis().SetTitleOffset(1.7)
        gHPLP.GetXaxis().SetRangeUser(1126., 5500.)
        gHPLP.GetYaxis().SetRangeUser(0.0, 0.00025)
            
        gHPLP.Draw("APE")
        gHPHP.Draw("samePE")
        # fHPLP.Draw("sameL")
    #   fHPHP.Draw("sameL")
        model = "G_{bulk} #rightarrow WW"
        if sys.argv[1].find("ZZ")!=-1:
            model = "G_{bulk} #rightarrow ZZ"
        if sys.argv[1].find("WZ")!=-1:
            model = "W' #rightarrow WZ"
        if sys.argv[1].find("Zprime")!=-1:
            model = "Z' #rightarrow WW"
        text = TLatex()
        text.DrawLatex(3500,0.00020,model)
        l.Draw("same")
        cmslabel_sim(c,'2016',11)
        c.Update()
        #sleep(112600)
        c.SaveAs(path+"signalFit/"+sys.argv[1]+"_Yield_"+var+"_fit.png")
        
def doMVV():

    vars = ["MEAN","SIGMA","ALPHA1","ALPHA2","N1","N2"]
    # vars = ["ALPHA2"]
    
    gStyle.SetOptFit(0)
    signals = ["ZprimeWW","BulkGWW","WprimeWZ","BulkGZZ"]
    titles =  ["Z' #rightarrow WW","G_{B}#rightarrow WW","W' #rightarrow WZ","G_{B}#rightarrow ZZ"]
    
    filesHP=[]
    # filesLP=[]
    
    for i,s in enumerate(signals):
        # filesLP.append(TFile("debug_JJ_"+s+"_MVV_jer.json.root","READ"))
        filesHP.append(TFile("debug_JJ_"+s+"_MVV.json.root","READ"))
    
    for var in vars:
        fitsHP=[]
        fitsLP=[]
        datasHP=[]
        datasLP=[]
        
        c = getCanvas()
        l = getLegend(0.7788945,0.723362,0.9974874,0.879833)
        l2 = getLegend(0.7788945,0.1783217,0.9974874,0.2482517)
        gStyle.SetOptStat(0)
        gStyle.SetOptTitle(0)
        
        for i,fHP in enumerate(filesHP):
                
                # gHPLP = fLP.Get(var)
                gHPHP = fHP.Get(var)
                # fHPLP = fLP.Get(var+"_func")
                fHPHP = fHP.Get(var+"_func")
                # gHPLP.GetFunction(var+"_func").SetBit(rt.TF1.kNotDraw)
                gHPHP.GetFunction(var+"_func").SetBit(rt.TF1.kNotDraw)
                
                # beautify(fHPLP ,rt.TColor.GetColor(colors[i]),9,1)
                beautify(fHPHP ,rt.TColor.GetColor(colors[i]),1,8)
                # beautify(gHPLP ,rt.TColor.GetColor(colors[i]),9,1)
                beautify(gHPHP ,rt.TColor.GetColor(colors[i]),1,8)
                datasHP.append(gHPHP)
                # datasLP.append(gHPLP)
                fitsHP.append(fHPHP)
                # fitsLP.append(fHPLP)
                l.AddEntry(fHPHP,titles[i],"L")
        # l2.AddEntry(datasHP[0],"No JER","L")
 #        l2.AddEntry(datasLP[0],"JER","L")
        fitsHP[0].GetXaxis().SetTitle("M_{X} (GeV)")
        fitsHP[0].GetYaxis().SetTitle(var+" (GeV)")
        fitsHP[0].GetYaxis().SetNdivisions(4,5,0)
        fitsHP[0].GetXaxis().SetNdivisions(9,2,0)
        fitsHP[0].GetYaxis().SetTitleOffset(0.97)
        fitsHP[0].GetXaxis().SetTitleOffset(0.94)
        fitsHP[0].GetXaxis().SetRangeUser(1126, 5500.)
        fitsHP[0].GetYaxis().SetRangeUser(-2., 3.)
        if var.find("ALPHA1")!=-1: fitsHP[0].GetYaxis().SetRangeUser(0., 4.)
        if var.find("ALPHA2")!=-1: fitsHP[0].GetYaxis().SetRangeUser(0., 6.)
        if var.find("SIGMA")!=-1:  fitsHP[0].GetYaxis().SetRangeUser(0., 400.)
        if var.find("MEAN")!=-1:   fitsHP[0].GetYaxis().SetRangeUser(700., 7000)
        if var.find("N1")!=-1:     fitsHP[0].GetYaxis().SetRangeUser(0., 10.)
        if var.find("N2")!=-1:     fitsHP[0].GetYaxis().SetRangeUser(0., 10.)
        fitsHP[0].Draw("C")
        if var.find("ALPHA1")!=-1: fitsHP[0].GetYaxis().SetRangeUser(0., 4.)
        if var.find("ALPHA2")!=-1: fitsHP[0].GetYaxis().SetRangeUser(0., 6.)
        c.Update()
        for i,gHP in enumerate(datasHP): 
            if var.find("ALPHA1")!=-1: fitsHP[i].GetYaxis().SetRangeUser(0., 4.)
            if var.find("ALPHA2")!=-1: fitsHP[i].GetYaxis().SetRangeUser(0., 6.)
            # gLP.Draw("Psame")
            gHP.Draw("Psame")
            fitsHP[i].Draw("Csame")
            # fitsLP[i].Draw("Csame")
        l.Draw("same")
        # l2.Draw("same")
        cmslabel_sim_prelim(c,'sim',11)
        pt = getPavetext()
        c.Update()
        c.SaveAs(path+"Signal_mVV_"+var+".png")
        c.SaveAs(path+"Signal_mVV_"+var+".pdf")
        c.SaveAs(path+"Signal_mVV_"+var+".C")
        
def doMJFit():
    FHPLP = TFile("debug_JJ_"+sys.argv[1]+"_MJl1_HPHP.json.root","READ")
    FHPHP = TFile("debug_JJ_"+sys.argv[1]+"_MJl1_HPHP.json.root","READ")
    
    vars = ["mean","sigma"]#,"alpha","n","f","alpha2","n2","slope"]
    #if sys.argv[1].find("Wprime")!=-1:
            #vars = ["meanW","sigmaW","alphaW","f","alphaW2","meanZ","sigmaZ","alphaZ","alphaZ2"]
    for var in vars:
        print "Plotting variable: " ,var
        c = getCanvas()
        l = getLegend()
        gStyle.SetOptStat(0)
        gStyle.SetOptTitle(0)
        
        
        gHPLP = FHPLP.Get(var)
        gHPHP = FHPHP.Get(var)
        fHPLP = FHPLP.Get(var+"_func")
        fHPHP = FHPHP.Get(var+"_func")
        
        beautify(gHPLP ,1,1,8)
        beautify(gHPHP ,1,1,4)
        beautify(fHPLP ,46,1,8)
        beautify(fHPHP ,30,1,4)
        
        l.AddEntry(fHPHP,"HPHP","LP")
        l.AddEntry(fHPLP,"HPLP","LP")
        
        
        gHPLP.GetXaxis().SetTitle("M_{X} (GeV)")
        gHPLP.GetYaxis().SetTitle(var)
        gHPLP.GetYaxis().SetNdivisions(9,1,0)
        gHPLP.GetYaxis().SetTitleOffset(1.7)
        gHPLP.GetXaxis().SetRangeUser(1126., 5500.)
        
                
<<<<<<< HEAD
                if var.find("n2")!=-1: gHPLP.GetYaxis().SetRangeUser(0., 5.)
		if var.find("n")!=-1: gHPLP.GetYaxis().SetRangeUser(1., 5.)
		if var.find("alpha2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.1)
		if var.find("alpha")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.5)
		if var.find("alphaZ2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
		if var.find("alphaZ")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
		if var.find("slope")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 1.)
		if var.find("sigma")!=-1: gHPLP.GetYaxis().SetRangeUser(3.,25.)
		if var.find("mean")!=-1: gHPLP.GetYaxis().SetRangeUser(70., 95.)
		if var.find("meanZ")!=-1: gHPLP.GetYaxis().SetRangeUser(80., 95.)
		if var.find("f")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 2.)
		gHPLP.Draw("APE")
		gHPHP.Draw("samePE")
		fHPLP.Draw("sameL")
		fHPHP.Draw("sameL")
		l.Draw("same")
		cmslabel_sim(c,'2016',11)
		c.Update()
		c.SaveAs(path+"signalFit/"+sys.argv[1]+"_MJ_"+var+"_fit.png")
		#sleep(10)
		
=======
        if var.find("n2")!=-1: gHPLP.GetYaxis().SetRangeUser(1., 3.)
        if var.find("n")!=-1: gHPLP.GetYaxis().SetRangeUser(1., 3.)
        if var.find("alpha2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.1)
        if var.find("alpha")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 5.5)
        if var.find("alphaZ2")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
        if var.find("alphaZ")!=-1: gHPLP.GetYaxis().SetRangeUser(0.1, 10)
        if var.find("slope")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 1.)
        if var.find("sigma")!=-1: gHPLP.GetYaxis().SetRangeUser(3.,25.)
        if var.find("mean")!=-1: gHPLP.GetYaxis().SetRangeUser(70., 95.)
        if var.find("meanZ")!=-1: gHPLP.GetYaxis().SetRangeUser(80., 95.)
        if var.find("f")!=-1: gHPLP.GetYaxis().SetRangeUser(-1., 2.)
        gHPLP.Draw("APE")
        gHPHP.Draw("samePE")
        fHPLP.Draw("sameL")
        fHPHP.Draw("sameL")
        l.Draw("same")
        cmslabel_sim(c,'2016',11)
        c.Update()
        c.SaveAs(path+"signalFit/"+sys.argv[1]+"_MJ_"+var+"_fit.png")
        #sleep(10)
        
>>>>>>> cfda05bb720c9d2593c89935499f994a8a94fbf2
def doResolution():
    fLP = TFile("JJ_nonRes_detectorResponse_2016.root","READ")
    fHP = TFile("JJ_nonRes_detectorResponse.root","READ")
    hps = []    
    hp_hSx  =fHP.Get("scalexHisto")
    hp_hSy  =fHP.Get("scaleyHisto")
    hp_hRx  =fHP.Get("resxHisto")  
    hp_hRy  =fHP.Get("resyHisto") 
    hp_hSx.GetYaxis().SetTitle("M_{VV} scale" )
    hp_hSy.GetYaxis().SetTitle("M_{jet} scale" )
    hp_hRx.GetYaxis().SetTitle("M_{VV} resolution" )
    hp_hRy.GetYaxis().SetTitle("M_{jet} resolution" )
    hp_hSx.GetYaxis().SetRangeUser(0.9,1.1)
    hp_hSy.GetYaxis().SetRangeUser(0.9,1.1)
    hp_hRx.GetYaxis().SetRangeUser(0.,0.15)
    hp_hRy.GetYaxis().SetRangeUser(0.,0.15)
    
     
    # hp_h2D_x =f.Get("dataX")    
    # hp_h2D_y =f.Get("dataY")    
    hps.append(hp_hSx)
    hps.append(hp_hSy)
    hps.append(hp_hRx)
    hps.append(hp_hRy)
    for h in hps: 
        h.SetLineColor(rt.TColor.GetColor(colors[0]))
        h.SetLineWidth(3)
        h.GetXaxis().SetTitle("Gen p_{T} (GeV)")
        h.GetXaxis().SetNdivisions(9,1,0)
        h.GetYaxis().SetNdivisions(9,1,0)
        h.GetYaxis().SetTitleOffset(1.4)
    
    
    lps =[]
    lp_hSx   =fLP.Get("scalexHisto")
    lp_hSy   =fLP.Get("scaleyHisto")
    lp_hRx   =fLP.Get("resxHisto")
    lp_hRy   =fLP.Get("resyHisto")
    # lp_h2D_x =fLP.Get("dataX")
    # lp_h2D_y =fLP.Get("dataY")
    lps.append(lp_hSx)
    lps.append(lp_hSy)
    lps.append(lp_hRx)
    lps.append(lp_hRy)
    for h in lps:
      h.SetLineColor(rt.TColor.GetColor(colors[1]))
      h.SetLineWidth(3)
      h.GetXaxis().SetTitle("Gen p_{T} (GeV)")
    
    lg = getLegend(0.7788945,0.723362,0.9974874,0.879833)
  # lg.AddEntry(hp_hSx,"m_{VV} scale","L")
  # lg.AddEntry(lp_hSx,"HPLP","L")
    lg.AddEntry(hp_hSx,"2017","L")
    lg.AddEntry(lp_hSx,"2016","L")
    
    pt = getPavetext()
    # pt.AddText("WP #tau_{21}^{DDT} = 0.57")
    
    
    for hp,lp in zip(hps,lps):
        c = getCanvas()
        hp.GetXaxis().SetRangeUser(200.,2600.)
        hp.Draw("HIST")
        lp.Draw("HISTsame")
        lg.Draw('same')
        pt.Draw("same")
        c.Update()
        c.SaveAs(path+"detectorresolution_"+hp.GetName()+".png")
        
    dataY_lp = fLP.Get('dataY')
    dataY_lp.SetName('dataY_lp')
    plotY_lp = TH1F('plotYlp','mJJ projection',dataY_lp.GetNbinsY(),dataY_lp.GetYaxis().GetXmin(),dataY_lp.GetYaxis().GetXmax())
    
    dataY_hp = fHP.Get('dataY')
    dataY_hp.SetName('dataY_hp')
    plotY_hp = TH1F('plotYhp','mJJ projection',dataY_hp.GetNbinsY(),dataY_hp.GetYaxis().GetXmin(),dataY_hp.GetYaxis().GetXmax())
    
    for bx in range(dataY_hp.GetNbinsX()):
      for by in range(dataY_hp.GetNbinsY()):
        plotY_hp.Fill(dataY_hp.GetYaxis().GetBinCenter(by),dataY_hp.GetBinContent(bx,by))
        plotY_lp.Fill(dataY_lp.GetYaxis().GetBinCenter(by),dataY_lp.GetBinContent(bx,by))
    plotY_hp.SetLineColor(rt.TColor.GetColor(colors[0])) 
    plotY_lp.SetLineColor(rt.TColor.GetColor(colors[1]))
    plotY_hp.SetLineWidth(3)
    plotY_lp.SetLineWidth(3)
    c = getCanvas()
    
    plotY_hp.GetXaxis().SetTitle("M_{jet}^{reco}/M_{jet}^{gen}")
    plotY_hp.GetYaxis().SetTitle("A.U")
    plotY_hp.GetXaxis().SetNdivisions(9,1,0)
    plotY_hp.GetYaxis().SetNdivisions(9,1,0)
    plotY_hp.GetYaxis().SetTitleOffset(0.94)
    plotY_hp.GetXaxis().SetTitleOffset(0.97)
    plotY_hp.GetYaxis().SetRangeUser(0.,plotY_hp.GetMaximum()*1.8)
    plotY_hp.DrawNormalized('HIST')
    plotY_lp.DrawNormalized('HISTSAME')
    lg.Draw("same")
    cmslabel_sim(c,'2016',11)
    c.Update()
    c.SaveAs(path+"detectorresolution_mjet.png")
    
    dataX_lp = fLP.Get('dataX')
    dataX_lp.SetName('dataX_lp')
    plotX_lp = TH1F('plotXlp','mJJ projection',dataX_lp.GetNbinsY(),dataX_lp.GetYaxis().GetXmin(),dataX_lp.GetYaxis().GetXmax())
    
    dataX_hp = fHP.Get('dataX')
    dataX_hp.SetName('dataX_hp')
    plotX_hp = TH1F('plotXhp','mVV projection',dataX_hp.GetNbinsY(),dataX_hp.GetYaxis().GetXmin(),dataX_hp.GetYaxis().GetXmax())
    
    for bx in range(dataX_hp.GetNbinsX()):
     for by in range(dataX_hp.GetNbinsY()):
      plotX_hp.Fill(dataX_hp.GetYaxis().GetBinCenter(by),dataX_hp.GetBinContent(bx,by))
      plotX_lp.Fill(dataX_lp.GetYaxis().GetBinCenter(by),dataX_lp.GetBinContent(bx,by))
    
    plotX_hp.SetLineColor(rt.TColor.GetColor(colors[0])) 
    plotX_lp.SetLineColor(rt.TColor.GetColor(colors[1]))
    plotX_hp.SetLineWidth(3)
    plotX_lp.SetLineWidth(3)
    c = getCanvas()
    
    plotX_hp.GetXaxis().SetTitle("M_{VV}^{reco}/M_{VV}^{gen}")
    plotX_hp.GetYaxis().SetTitle("A.U")
    plotX_hp.GetXaxis().SetNdivisions(4,5,0)
    plotX_hp.GetYaxis().SetNdivisions(4,5,0)
    plotX_hp.GetYaxis().SetTitleOffset(0.94)
    plotX_hp.GetXaxis().SetTitleOffset(0.97)
    plotX_hp.GetYaxis().SetRangeUser(0.,plotX_lp.GetMaximum()*1.8)
    plotX_hp.DrawNormalized('HIST')
    plotX_lp.DrawNormalized('HISTSAME')
    lg.Draw("same")
    cmslabel_sim(c,'2016',11)
    c.Update()
    c.SaveAs(path+"detectorresolution_mvv.png")
    
    fLP.Close()
    fHP.Close() 
    
def doKernelMVV():
    files = []
    fLP = TFile("JJ_nonRes_MVV_HPHP.root","READ")
    fHP = TFile("JJ_nonRes_MVV_HPHP.root","READ")
    files.append(fLP)
    files.append(fHP)
    cols = [46,30]
    mstyle = [8,4]
    c = getCanvas()
    c.SetLogy()
    l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
    hists = []
    for i,f in enumerate(files):
        hsts = []
        fromKernel = f.Get("histo_nominal")
        fromSim    = f.Get("mvv_nominal")
        beautify(fromKernel,cols[i],1,mstyle[i])
        beautify(fromSim   ,cols[i],1,mstyle[i])
        l.AddEntry(fromKernel,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
        l.AddEntry(fromSim   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
        
        hsts.append(fromSim)
        hsts.append(fromKernel)
        hists.append(hsts)
    hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
    hists[0][0].GetYaxis().SetTitle("A.U")
    hists[0][0].GetYaxis().SetNdivisions(9,1,0)
    hists[0][0].GetYaxis().SetTitleOffset(1.5)  
    hists[0][0].GetXaxis().SetRangeUser(1126   , 6808)
    hists[0][0].DrawNormalized("histPE")
    for h in hists:
        h[0].DrawNormalized("samehistPE")
        h[1].DrawNormalized("sameLhist")
        
    l.Draw("same")
    c.SaveAs(path+"1Dkernel.png")

def compKernelMVV():
    purities=['HPHP','HPLP']
    
    for p in purities:
        hists = []
        files = []
        fNominal = TFile("JJ_nonRes_MVV_"+p+".root","READ")
        fCombined = TFile("JJ_nonRes_MVV_"+p+"_NP.root","READ")
        files.append(fNominal)
        files.append(fCombined)
        
        
        hists = []
        l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
        cols = [46,30]
        for i,f in enumerate(files):
            hsts = []
    
            fromKernel = f.Get("histo_nominal")
            fromSim    = f.Get("mvv_nominal")

            beautify(fromKernel,cols[i])
            beautify(fromSim   ,cols[i])
            if i == 1:
                l.AddEntry(fromKernel,"Combined, Kernel    ","L")
                l.AddEntry(fromSim   ,"Combined, Simulation","PE")
            elif i == 0:
                l.AddEntry(fromKernel,"%s res., Kernel    "%p,"L")
                l.AddEntry(fromSim   ,"%s res., Simulation"%p,"PE")
                    
            hsts.append(fromSim)
            hsts.append(fromKernel)
            hists.append(hsts)
        c = getCanvas()
        c.SetLogy()
        
        hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
        hists[0][0].GetYaxis().SetTitle("A.U")
        hists[0][0].GetYaxis().SetNdivisions(9,1,0)
        hists[0][0].GetYaxis().SetTitleOffset(1.5)  
        hists[0][0].GetXaxis().SetRangeUser(1126.   , 4900)
        hists[0][0].Draw("histPE")
        for h in hists:
            h[0].Draw("samehistPE")
            h[1].Draw("sameLhist")
        
        l.Draw("same")
        c.SaveAs(path+"compare_1Dkernel"+p+".png")

def doKernel2D():
    files = []
    fLP = TFile("JJ_nonRes_COND2D_HPHP_l1.root","READ")
    fHP = TFile("JJ_nonRes_COND2D_HPHP_l2.root","READ")
    histnames = ["mjet_mvv_nominal","histo_nominal"]
    files.append(fLP)
    files.append(fHP)
    cols = [46,30]
    c = getCanvas()
    c.SetLogy()
    l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
    hists = []
    for i,f in enumerate(files):
        hsts = []
    
        fromKernel  = f.Get(histnames[i])
        fromSim     = f.Get(histnames[i])
        fromKernelY = fromKernel.ProjectionX()
        fromSimY    = fromSim.ProjectionX()
        fromKernelY .SetName("kernel"+f.GetName().replace(".root","").split("_")[3])
        fromSimY    .SetName("sim"+f.GetName().replace(".root","").split("_")[3])

        beautify(fromKernelY,cols[i])
        beautify(fromSimY   ,cols[i])
        l.AddEntry(fromKernelY,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
        l.AddEntry(fromSimY   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
        
        hsts.append(fromSimY)
        hsts.append(fromKernelY)
        hists.append(hsts)

    hists[0][0].GetXaxis().SetTitle("M_{jet} (GeV)")
    hists[0][0].GetYaxis().SetTitle("A.U")
    hists[0][0].GetYaxis().SetNdivisions(9,1,0)
    hists[0][0].GetYaxis().SetTitleOffset(1.5)  
    # hists[0][0].GetXaxis().SetRangeUser(1126.   , 5200)
    hists[0][0].DrawNormalized("histPE")
    for h in hists:
        h[0].DrawNormalized("samehistPE")
        h[1].DrawNormalized("sameLhist")
    
    l.Draw("same")
    c.SaveAs(path+"2Dkernel_Mjet.png")      
    
    c = getCanvas()
    c.SetLogy()
    l = getLegend(0.60010112,0.723362,0.90202143,0.879833)
    hists = []
    for i,f in enumerate(files):
        hsts = []
    
        fromKernel  = f.Get("histo_nominal")
        fromSim     = f.Get("mjet_mvv_nominal")
        fromKernelY = fromKernel.ProjectionY()
        fromSimY    = fromSim.ProjectionY()
        fromKernelY .SetName("kernel"+f.GetName().replace(".root","").split("_")[3])
        fromSimY    .SetName("sim"+f.GetName().replace(".root","").split("_")[3])

        beautify(fromKernelY,cols[i])
        beautify(fromSimY   ,cols[i])
        l.AddEntry(fromKernelY,"%s,From Kernel    "%(f.GetName().replace(".root","").split("_")[3]),"L")
        l.AddEntry(fromSimY   ,"%s,From Simulation"%(f.GetName().replace(".root","").split("_")[3]),"PE")
        
        hsts.append(fromSimY)
        hsts.append(fromKernelY)
        hists.append(hsts)
    hists[0][0].GetXaxis().SetTitle("M_{jj} (GeV)")
    hists[0][0].GetYaxis().SetTitle("A.U")
    hists[0][0].GetYaxis().SetNdivisions(9,1,0)
    hists[0][0].GetYaxis().SetTitleOffset(1.5)  
    # hists[0][0].GetXaxis().SetRangeUser(1126.   , 5200)
    hists[0][0].DrawNormalized("histPE")

    for h in hists:
        # h[0].DrawNormalized("samehistPE")
        h[1].DrawNormalized("sameLhist")
    
    # l.Draw("same")
    c.SaveAs(path+"2Dkernel_Mjj.png")

def compSignalMVV():
<<<<<<< HEAD
	
	masses = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
	
	
	files = []
	fHP  = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV_HPHP.root","READ")
	fLP = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV_HPLP.root","READ")
	files.append(fHP)
	files.append(fLP)
	
	
	histsHP = []
	histsLP = []
	l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
	cols = [46,30]
	for m in masses:
		hHP = fHP.Get("%i"%m)
		hLP = fLP.Get("%i"%m)
		hHP.SetName(hHP.GetName()+"HP")
		hLP.SetName(hLP.GetName()+"LP")
		hHP.SetLineColor(cols[0])
		hLP.SetLineColor(cols[1])
		hHP.SetFillColor(0)
		hLP.SetFillColor(0)
		hHP.Rebin(10)
		hLP.Rebin(10)
		if m == masses[0]:
			l.AddEntry(hHP   ,"HPHP","L")
			l.AddEntry(hLP   ,"HPLP","L")
				
		histsHP.append(hHP)
		histsLP.append(hLP)
		
	c = getCanvas()
	
	histsHP[0].GetXaxis().SetTitle("M_{jj} (GeV)")
	
	histsHP[0].GetYaxis().SetTitle("A.U")
	histsHP[0].GetYaxis().SetNdivisions(9,1,0)
	histsHP[0].GetYaxis().SetTitleOffset(1.5)
	histsHP[0].GetXaxis().SetRangeUser(1000,5200)
	histsHP[0].DrawNormalized("hist")
	for hp,lp in zip(histsHP,histsLP):
		hp.DrawNormalized("hist same")
		lp.DrawNormalized("hist same")
	
	l.Draw("same")
	c.SaveAs(path+"comparePurities_MVV.png")
	
	
	
	# histsHP[0].GetXaxis().SetRangeUser(1000,5200)
	c = getCanvas(1600,600)
	c.Divide(2,5)
	legs = []
	for i,(m,hp,lp) in enumerate(zip(masses,histsHP,histsLP)):
		hp.Scale(1./hp.Integral())
		lp.Scale(1./lp.Integral())
		hp.Divide(lp)
		hp.SetMarkerColor(1)
		hp.GetXaxis().SetRangeUser(m*0.80,m*1.2)
		hp.GetYaxis().SetRangeUser(0,2)
		hp.GetYaxis().SetNdivisions(3,0,0)
		hp.GetXaxis().SetTitle("M = %i GeV"%m)
		hp.GetYaxis().SetTitle("HP/LP")
		hp.GetYaxis().SetTitleSize(0.7)
		hp.GetYaxis().SetLabelSize(0.16)
		 
		hp.GetXaxis().SetTitleSize(0.7)
		c.cd(i+1)
		hp.Draw("M")
		l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
		l.SetName("l%i"%m)
		l.SetTextSize(0.2)
		l.AddEntry(hp   ,"%i"%m,"LEP")
		l.Draw("same")
		legs.append(l)

	c.SaveAs(path+"comparePurities_MVVratio.png")
		
if __name__ == '__main__':

=======
    
    masses = [1200,1400,1600,1800,2000,2500,3000,3500,4000,4500]
    
    
    files = []
    fHP  = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV.root","READ")
    fLP = TFile("massHISTOS_JJ_"+sys.argv[1]+"_MVV_jer.root","READ")
    files.append(fHP)
    files.append(fLP)
    
    
    histsHP = []
    histsLP = []
    l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
    cols = [46,30]
    for m in masses:
        print "Working on masspoint " ,m
        hHP = fHP.Get("%i"%m)
        hLP = fLP.Get("%i"%m)
        hHP.SetName(hHP.GetName()+"HP")
        hLP.SetName(hLP.GetName()+"LP")
        hHP.SetLineColor(cols[0])
        hLP.SetLineColor(cols[1])
        hHP.SetLineWidth(2)
        hLP.SetLineWidth(2)
        hHP.SetFillColor(0)
        hLP.SetFillColor(0)
        if m == masses[0]:
            l.AddEntry(hHP   ,"No JER","L")
            l.AddEntry(hLP   ,"JER","L")
                
        histsHP.append(hHP)
        histsLP.append(hLP)
    
    print " ", len(histsHP) 
    print " ", len(histsLP)
    c = getCanvas()
    
    histsHP[0].GetXaxis().SetTitle("M_{jj} (GeV)")
    histsHP[0].GetYaxis().SetTitle("A.U")
    histsHP[0].GetYaxis().SetNdivisions(9,1,0)
    histsHP[0].GetYaxis().SetTitleOffset(1.5)
    histsHP[0].GetXaxis().SetRangeUser(1126,5500)
    histsHP[0].GetXaxis().SetLimits(1126,5500);
    # histsHP[0].GetYaxis().SetRangeUser(0,0.4)
    # histsHP[0].GetYaxis().SetLimits(0.,0.4);
    histsHP[0].Draw("hist")
    for hp,lp in zip(histsHP,histsLP):
        hp.Draw("hist same")
        lp.Draw("hist same")
    l.Draw("same")
    c.Update()
    c.SaveAs(path+"compareJER_MVV.png")
    
    
    
    # # histsHP[0].GetXaxis().SetRangeUser(1126,5200)
#     c = getCanvas(1600,600)
#     c.Divide(2,5)
#     legs = []
#     for i,(m,hp,lp) in enumerate(zip(masses,histsHP,histsLP)):
#         hp.Scale(1./hp.Integral())
#         lp.Scale(1./lp.Integral())
#         hp.Divide(lp)
#         hp.SetMarkerColor(1)
#         hp.GetXaxis().SetRangeUser(m*0.80,m*1.2)
#         hp.GetYaxis().SetRangeUser(0,2)
#         hp.GetYaxis().SetNdivisions(3,0,0)
#         hp.GetXaxis().SetTitle("M = %i GeV"%m)
#         hp.GetYaxis().SetTitle("HP/LP")
#         hp.GetYaxis().SetTitleSize(0.7)
#         hp.GetYaxis().SetLabelSize(0.16)
#
#         hp.GetXaxis().SetTitleSize(0.7)
#         c.cd(i+1)
#         hp.Draw("M")
#         l = getLegend(0.80010112,0.723362,0.90202143,0.879833)
#         l.SetName("l%i"%m)
#         l.SetTextSize(0.2)
#         l.AddEntry(hp   ,"%i"%m,"LEP")
#         l.Draw("same")
#         legs.append(l)
#
#     c.SaveAs(path+"compareJER_MVVratio.png")
        
if __name__ == '__main__':
  
  # doSignalEff()
  # doJetMass("l1")
  # doJetMass("l2")
>>>>>>> cfda05bb720c9d2593c89935499f994a8a94fbf2
  # doMJFit()
  doMVV()
  # doYield()
  # doResolution()
  # doKernelMVV()
    #compKernelMVV()
    # doKernel2D()
    # compSignalMVV()
