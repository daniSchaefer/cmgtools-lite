import ROOT





if __name__=="__main__":
    purity = "HPLP"
    V = "W"
    #fnew = ROOT.TFile("JJ_"+V+"Jets_MVV_"+purity+".root","READ")
    fnew = ROOT.TFile("JJ_NLOweights_NoEWK_"+V+"Jets_MVV_"+purity+".root","READ")
    
    fold = ROOT.TFile("JJ_NLOweights_"+V+"Jets_MVV_"+purity+".root","READ")
    
    print fold
    
    h_kernel_old = fold.Get("histo_nominal")
    h_kernel_old.SetName("histo_nominal_new")
    h_ptup_old = fold.Get("histo_nominal_PTUp")
    h_ptdown_old = fold.Get("histo_nominal_PTDown")
    h_optup_old = fold.Get("histo_nominal_OPTUp")
    h_optdown_old = fold.Get("histo_nominal_OPTDown")
    
    
    
    
    
    h_kernel_new = fnew.Get("histo_nominal")
    h_data_new  = fold.Get("mvv_nominal")
    h_data_new.SetMarkerStyle(1)
    
    
    h_kernel_old .Scale(1/h_kernel_old .Integral())
    h_ptup_old   .Scale(1/h_ptup_old   .Integral())
    h_ptdown_old .Scale(1/h_ptdown_old .Integral())
    h_optup_old  .Scale(1/h_optup_old  .Integral())
    h_optdown_old.Scale(1/h_optdown_old.Integral())
    
    h_kernel_new .Scale(1/h_kernel_new .Integral())
    h_data_new   .Scale(1/h_data_new   .Integral())
    h_data_new   .Scale(1/h_data_new   .Integral())
    c = ROOT.TCanvas("c","", 600,400)
    
    h_kernel_old .SetLineColor(ROOT.kBlack)
    h_ptup_old   .SetLineColor(ROOT.kBlue)
    h_ptdown_old .SetLineColor(ROOT.kBlue)
    h_optup_old  .SetLineColor(ROOT.kCyan)
    h_optdown_old.SetLineColor(ROOT.kCyan)
    
    h_kernel_new .SetLineColor(ROOT.kRed)
    h_data_new   .SetLineColor(ROOT.kRed)
    h_data_new   .SetMarkerColor(ROOT.kRed)
    
    h_kernel_old.GetXaxis().SetTitle("m_{jj} [GeV]")
    h_kernel_old.GetYaxis().SetTitle("arbitrary scale")
    
    h_kernel_old   .Draw("hist")
    h_ptup_old     .Draw("samehist")
    h_ptdown_old   .Draw("samehist")
    h_optup_old    .Draw("samehist")
    h_optdown_old  .Draw("samehist")
                  
    h_kernel_new   .Draw("samehist")
    #h_data_new     .Draw("same")
   
    legend = ROOT.TLegend(0.5607383,0.8563123,0.85,0.65089701)
    legend.SetLineWidth(2)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.SetTextAlign(12)
    legend.AddEntry(h_kernel_old,"nominal template","l")
    legend.AddEntry(h_ptup_old,"#propto m_{jj}","l")
    legend.AddEntry(h_optup_old,"#propto 1/m_{jj}","l")
    #legend.AddEntry(h_kernel_new,"old kernel","l")
    legend.AddEntry(h_kernel_new,"No EWK weights","l")
    #legend.AddEntry(h_data_new,"NLO weights simulation","p")
    
    legend.Draw("same")
    c.SetLogy()
    c.SaveAs("testNLO_"+V+"_"+purity+".png")
