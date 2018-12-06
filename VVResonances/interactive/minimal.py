import ROOT

ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
colors = [ROOT.kRed,ROOT.kRed-2,ROOT.kRed+1,ROOT.kRed-1,ROOT.kRed+2,ROOT.kGreen-1,ROOT.kGreen-2,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kBlue]

def doXprojection(pdfs,data,norm,outname,hin=0):
    h=[]
    proj = ROOT.TH1F("px","px",len(xBins)-2,xBinslowedge[1],xBinslowedge[len(xBins)-1])
    for p in pdfs:
        h.append( ROOT.TH1F("hx_"+p.GetName(),"hx_"+p.GetName(),len(xBins)-2,xBinslowedge[1],xBinslowedge[len(xBins)-1]))
    for xk, xv in xBins_redux.iteritems():
         MJ1.setVal(xv)
         for yk, yv in yBins_redux.iteritems():
             MJ2.setVal(yv)
             for zk,zv in zBins_redux.iteritems():
                 MJJ.setVal(zv)
                 #print zv
                 i=0
                 binV = 160
                 proj.Fill(xv,data.weight(argset))
                 for p in pdfs:
                     if "postfit" in p.GetName():
                         #h[i].Fill(xv,p.evaluate()*binV)
                         h[i].Fill(xv,p.getVal()*binV)
                         #lv[i][xv] += p.expectedEvents(argset)*binV
                         #print p.expectedEvents(argset)*binV
                         #print "evalueate "+str( lv[i][xv])
                         #print "getVal "+str(p.getVal(argset)*binV)
                     else:
                         h[i].Fill(xv, p.getVal(argset)*binV)
                     i+=1
    leg = ROOT.TLegend(0.88,0.65,0.77,0.89)
    c = ROOT.TCanvas("c","c",800,400)
    # normalize to 1
    h[0].Scale(1/h[0].Integral())#norm)
    for i in range(1,len(h)):
        h[i].Scale(1/h[i].Integral())
    #proj.Scale(norm)
    
    print h[0].GetXaxis().GetBinCenter(80)
    print h[0].GetBinContent(80)
    print h[0].GetXaxis().GetBinCenter(79)
    print h[0].GetBinContent(79)
    
    h[0].SetLineColor(colors[0])
    h[0].GetXaxis().SetTitle("m_{jet1}")
    h[0].GetYaxis().SetTitleOffset(1.3)
    h[0].GetYaxis().SetTitle("events")
    if pdf_shape_postfit in pdfs:
        h[0].GetYaxis().SetTitleOffset(0.6)
        h[0].GetYaxis().SetTitle("events")
        h[0].GetYaxis().SetTitleSize(0.06)
        h[0].GetYaxis().SetLabelSize(0.06)
        h[0].GetYaxis().SetNdivisions(5)
    h[0].Draw("hist")
    leg.AddEntry(proj,"data","lp")
    leg.AddEntry(h[0],"nominal","l")
    for i in range(1,len(h)):
        h[i].SetLineColor(colors[i])
        h[i].Draw("histsame")
        name = h[i].GetName().split("_")
        leg.AddEntry(h[i],name[2],"l")
    if hin!=0:    
        #hin.SetLineColor(ROOT.kGreen)
        #hin.Scale(norm)
        hin.Draw("same")
        leg.AddEntry(hin,"test projection","l")
    proj.SetMarkerStyle(1)
    proj.Scale(1/proj.Integral())
    proj.Draw("same")
    leg.SetLineColor(0)
    leg.Draw("same")
    c.SaveAs(outname)  
    return h[0]


if __name__=="__main__":
     xBins = {0: 54.0, 1: 56.0, 2: 58.0, 3: 60.0, 4: 62.0, 5: 64.0, 6: 66.0, 7: 68.0, 8: 70.0, 9: 72.0, 10: 74.0, 11: 76.0, 12: 78.0, 13: 80.0, 14: 82.0, 15: 84.0, 16: 86.0, 17: 88.0, 18: 90.0, 19: 92.0, 20: 94.0, 21: 96.0, 22: 98.0, 23: 100.0, 24: 102.0, 25: 104.0, 26: 106.0, 27: 108.0, 28: 110.0, 29: 112.0, 30: 114.0, 31: 116.0, 32: 118.0, 33: 120.0, 34: 122.0, 35: 124.0, 36: 126.0, 37: 128.0, 38: 130.0, 39: 132.0, 40: 134.0, 41: 136.0, 42: 138.0, 43: 140.0, 44: 142.0, 45: 144.0, 46: 146.0, 47: 148.0, 48: 150.0, 49: 152.0, 50: 154.0, 51: 156.0, 52: 158.0, 53: 160.0, 54: 162.0, 55: 164.0, 56: 166.0, 57: 168.0, 58: 170.0, 59: 172.0, 60: 174.0, 61: 176.0, 62: 178.0, 63: 180.0, 64: 182.0, 65: 184.0, 66: 186.0, 67: 188.0, 68: 190.0, 69: 192.0, 70: 194.0, 71: 196.0, 72: 198.0, 73: 200.0, 74: 202.0, 75: 204.0, 76: 206.0, 77: 208.0, 78: 210.0, 79: 212.0, 80: 214.0, 81: 216.0}
     xBins_redux=xBins
     yBins_redux ={1: 56.0, 2: 58.0, 3: 60.0, 4: 62.0, 5: 64.0, 6: 66.0, 7: 68.0, 8: 70.0, 9: 72.0, 10: 74.0, 11: 76.0, 12: 78.0, 13: 80.0, 14: 82.0, 15: 84.0, 16: 86.0, 17: 88.0, 18: 90.0, 19: 92.0, 20: 94.0, 21: 96.0, 22: 98.0, 23: 100.0, 24: 102.0, 25: 104.0, 26: 106.0, 27: 108.0, 28: 110.0, 29: 112.0, 30: 114.0, 31: 116.0, 32: 118.0, 33: 120.0, 34: 122.0, 35: 124.0, 36: 126.0, 37: 128.0, 38: 130.0, 39: 132.0, 40: 134.0, 41: 136.0, 42: 138.0, 43: 140.0, 44: 142.0, 45: 144.0, 46: 146.0, 47: 148.0, 48: 150.0, 49: 152.0, 50: 154.0, 51: 156.0, 52: 158.0, 53: 160.0, 54: 162.0, 55: 164.0, 56: 166.0, 57: 168.0, 58: 170.0, 59: 172.0, 60: 174.0, 61: 176.0, 62: 178.0, 63: 180.0, 64: 182.0, 65: 184.0, 66: 186.0, 67: 188.0, 68: 190.0, 69: 192.0, 70: 194.0, 71: 196.0, 72: 198.0, 73: 200.0, 74: 202.0, 75: 204.0, 76: 206.0, 77: 208.0, 78: 210.0, 79: 212.0, 80: 214.0}
     xBinslowedge ={0: 53.0, 1: 55.0, 2: 57.0, 3: 59.0, 4: 61.0, 5: 63.0, 6: 65.0, 7: 67.0, 8: 69.0, 9: 71.0, 10: 73.0, 11: 75.0, 12: 77.0, 13: 79.0, 14: 81.0, 15: 83.0, 16: 85.0, 17: 87.0, 18: 89.0, 19: 91.0, 20: 93.0, 21: 95.0, 22: 97.0, 23: 99.0, 24: 101.0, 25: 103.0, 26: 105.0, 27: 107.0, 28: 109.0, 29: 111.0, 30: 113.0, 31: 115.0, 32: 117.0, 33: 119.0, 34: 121.0, 35: 123.0, 36: 125.0, 37: 127.0, 38: 129.0, 39: 131.0, 40: 133.0, 41: 135.0, 42: 137.0, 43: 139.0, 44: 141.0, 45: 143.0, 46: 145.0, 47: 147.0, 48: 149.0, 49: 151.0, 50: 153.0, 51: 155.0, 52: 157.0, 53: 159.0, 54: 161.0, 55: 163.0, 56: 165.0, 57: 167.0, 58: 169.0, 59: 171.0, 60: 173.0, 61: 175.0, 62: 177.0, 63: 179.0, 64: 181.0, 65: 183.0, 66: 185.0, 67: 187.0, 68: 189.0, 69: 191.0, 70: 193.0, 71: 195.0, 72: 197.0, 73: 199.0, 74: 201.0, 75: 203.0, 76: 205.0, 77: 207.0, 78: 209.0, 79: 211.0, 80: 213.0, 81: 215.0}
     zBins_redux ={ 1: 1020.0, 2: 1060.0, 3: 1100.0, 4: 1140.0, 5: 1180.0, 6: 1220.0, 7: 1260.0, 8: 1300.0, 9: 1340.0, 10: 1380.0, 11: 1420.0, 12: 1460.0, 13: 1500.0, 14: 1540.0, 15: 1580.0, 16: 1620.0, 17: 1660.0, 18: 1700.0, 19: 1740.0, 20: 1780.0, 21: 1820.0, 22: 1860.0, 23: 1900.0, 24: 1940.0, 25: 1980.0, 26: 2020.0, 27: 2060.0, 28: 2100.0, 29: 2140.0, 30: 2180.0, 31: 2220.0, 32: 2260.0, 33: 2300.0, 34: 2340.0, 35: 2380.0, 36: 2420.0, 37: 2460.0, 38: 2500.0, 39: 2540.0, 40: 2580.0, 41: 2620.0, 42: 2660.0, 43: 2700.0, 44: 2740.0, 45: 2780.0, 46: 2820.0, 47: 2860.0, 48: 2900.0, 49: 2940.0, 50: 2980.0, 51: 3020.0, 52: 3060.0, 53: 3100.0, 54: 3140.0, 55: 3180.0, 56: 3220.0, 57: 3260.0, 58: 3300.0, 59: 3340.0, 60: 3380.0, 61: 3420.0, 62: 3460.0, 63: 3500.0, 64: 3540.0, 65: 3580.0, 66: 3620.0, 67: 3660.0, 68: 3700.0, 69: 3740.0, 70: 3780.0, 71: 3820.0, 72: 3860.0, 73: 3900.0, 74: 3940.0, 75: 3980.0, 76: 4020.0, 77: 4060.0, 78: 4100.0, 79: 4140.0, 80: 4180.0, 81: 4220.0, 82: 4260.0, 83: 4300.0, 84: 4340.0, 85: 4380.0, 86: 4420.0, 87: 4460.0, 88: 4500.0, 89: 4540.0, 90: 4580.0, 91: 4620.0, 92: 4660.0, 93: 4700.0, 94: 4740.0, 95: 4780.0, 96: 4820.0, 97: 4860.0, 98: 4900.0, 99: 4940.0, 100: 4980.0}

    
    
     name = "workspace_testBatch_HPHP.root"
     print "open file "+ name
     f = ROOT.TFile(name,"READ")
     workspace = f.Get("w")
     f.Close()
     
     CMS_VV_JJ_nonRes_OPTXY  = workspace.var("CMS_VV_JJ_nonRes_OPTXY")
     CMS_VV_JJ_nonRes_OPTZ   = workspace.var("CMS_VV_JJ_nonRes_OPTZ")
     CMS_VV_JJ_nonRes_PTXY   = workspace.var("CMS_VV_JJ_nonRes_PTXY")
     CMS_VV_JJ_nonRes_PTZ    = workspace.var("CMS_VV_JJ_nonRes_PTZ")
     
    
     print CMS_VV_JJ_nonRes_OPTXY.getVal()
     print CMS_VV_JJ_nonRes_OPTZ .getVal()
     print CMS_VV_JJ_nonRes_PTXY .getVal()
     print CMS_VV_JJ_nonRes_PTZ  .getVal()
    
     
     model = workspace.pdf("model_b")
     data = workspace.data("data_obs")
     args  = model.getComponents()
     pdf_shape_postfit  = args["shapeBkg_nonRes_JJ_HPHP_13TeV"]  # this is the FastVerticlHistPDf3D
     fitresult = pdf_shape_postfit.fitTo(data,ROOT.RooFit.NumCPU(8),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1))
     #workspace.Print()
     pdf_shape_nominal  = args["nonRes_PTXYUp_JJ_HPHP_13TeV"]

     MJ1= workspace.var("MJ1");
     MJ2= workspace.var("MJ2");
     MJJ= workspace.var("MJJ");
     argset = ROOT.RooArgSet();
     argset.add(MJ1);
     argset.add(MJ2);
     argset.add(MJJ);
     set2 = ROOT.RooArgSet();
     set2.add(MJ2)
     set2.add(MJJ)

     set3 = ROOT.RooArgList(MJ1)


     
     print CMS_VV_JJ_nonRes_OPTXY.getVal()
     print CMS_VV_JJ_nonRes_OPTZ .getVal()
     print CMS_VV_JJ_nonRes_PTXY .getVal()
     print CMS_VV_JJ_nonRes_PTZ  .getVal()
     
     #CMS_VV_JJ_nonRes_OPTXY.setVal(   9.14575e-01) 
     #CMS_VV_JJ_nonRes_OPTZ .setVal(  2.87961e-01 ) 
     #CMS_VV_JJ_nonRes_PTXY .setVal(  5.65562e-01 ) 
     #CMS_VV_JJ_nonRes_PTZ  .setVal( 8.57367e-01  ) 

     frame = MJ1.frame()
     
     
     norm = (args["pdf_binJJ_HPHP_13TeV_bonly"].getComponents())["n_exp_binJJ_HPHP_13TeV_proc_nonRes"].getVal()
     # check normalization with from pdf generated data:
     pdfdata_postfit = pdf_shape_postfit.generateBinned(ROOT.RooArgSet(MJ1, MJ2, MJJ), norm,True, True)
     pdfdata_nominal = pdf_shape_nominal.generateBinned(ROOT.RooArgSet(MJ1, MJ2, MJJ), norm, True, True)   
     
     tryProjection = pdf_shape_nominal.createProjection(set2)
     c = ROOT.TCanvas("test","test",800,400)
     tryProjection.plotOn(frame)
     frame.Draw()
     #tryProjection.Draw("AL")
     #c.SaveAs("test.pdf")
     
     tryProjection2 = pdf_shape_postfit.createProjection(set2)
    
     pdf_shape_nominal.Print()
     pdfs = [pdf_shape_nominal,pdf_shape_postfit]
     doXprojection(pdfs,pdfdata_postfit,norm,"pdf_postfit.pdf")
     hist = doXprojection([pdf_shape_nominal],pdfdata_nominal,norm,"pdf_nominal.pdf")
     #datahist = ROOT.RooDataHist("hist","hist",set3,ROOT.RooFit.Import(hist))
     #datahist.plotOn(frame)
     hist.SetLineColor(ROOT.kRed)
     hist.Draw("same")
     c.SaveAs("test.pdf")
     MJ1.setVal(80)

     MJ2.setVal(80)

     MJJ.setVal(2000)

     print pdf_shape_postfit.evaluate()
     
     
