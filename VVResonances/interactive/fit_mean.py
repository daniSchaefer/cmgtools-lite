import ROOT




if __name__=="__main__":
    
    f = ROOT.TFile("test.root","READ")
    graph = f.Get("")
    
    print graph
    
    #func = ROOT.TF1("pol2","[0]+[1]*x+[3]*(5000-x)*(5000-x)+[2]*x*x*x",1000,5000)
    #func = ROOT.TF1("exp","[0]*exp([1]*x)",1000,5000)
    #func = ROOT.TF1("pol1","[0]+[1]*(5000-x)+[2]*(5000-x)*(5000-x)+[3]*(5000-x)*(5000-x)*(5000-x)",1000,5000)
    func = ROOT.TF1("pol1","[0]+[2]*(5000-x)*(5000-x)+[3]*(5000-x)*(5000-x)*(5000-x)",1000,5000)
    func.SetLineColor(ROOT.kRed)
    graph.Fit(func)


    
    c = ROOT.TCanvas("c","c",400,400)
    #c.SetLogy()
    func.Draw("l")
    graph.Draw("lpsame")
    
    c.SaveAs("mean.pdf")
