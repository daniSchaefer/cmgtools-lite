import ROOT
import numpy
from array import array
import os, sys
import optparse
import numpy
from  CMS_lumi import *
from array import array
from forCorr_JJ_WJets_HPHP import JJ_WJets_HPHP_Res_l1_0, JJ_WJets_HPHP_Res_l1_1, JJ_WJets_HPHP_Res_l1_2, JJ_WJets_HPHP_Res_l1_3,JJ_WJets_HPHP_Res_l1_4,JJ_WJets_HPHP_Res_l1_5,JJ_WJets_HPHP_Res_l2_0, JJ_WJets_HPHP_Res_l2_1, JJ_WJets_HPHP_Res_l2_2, JJ_WJets_HPHP_Res_l2_3,JJ_WJets_HPHP_Res_l2_4,JJ_WJets_HPHP_Res_l2_5

from forCorr_JJ_WJets_HPLP import JJ_WJets_HPLP_Res_l1_0, JJ_WJets_HPLP_Res_l1_1, JJ_WJets_HPLP_Res_l1_2, JJ_WJets_HPLP_Res_l1_3,JJ_WJets_HPLP_Res_l1_4,JJ_WJets_HPLP_Res_l1_5,JJ_WJets_HPLP_Res_l2_0, JJ_WJets_HPLP_Res_l2_1, JJ_WJets_HPLP_Res_l2_2, JJ_WJets_HPLP_Res_l2_3,JJ_WJets_HPLP_Res_l2_4,JJ_WJets_HPLP_Res_l2_5

from forCorr_JJ_ZJets_HPHP import JJ_ZJets_HPHP_Res_l1_0, JJ_ZJets_HPHP_Res_l1_1, JJ_ZJets_HPHP_Res_l1_2, JJ_ZJets_HPHP_Res_l1_3,JJ_ZJets_HPHP_Res_l1_4,JJ_ZJets_HPHP_Res_l1_5,JJ_ZJets_HPHP_Res_l2_0, JJ_ZJets_HPHP_Res_l2_1, JJ_ZJets_HPHP_Res_l2_2, JJ_ZJets_HPHP_Res_l2_3,JJ_ZJets_HPHP_Res_l2_4,JJ_ZJets_HPHP_Res_l2_5


#arser = optparse.OptionParser()
#parser.add_option("-v","--variable",dest="variable",help="variable name to be used for example tau21, softdopmass",default='')
#(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)



def setMjetFunc(param, label):
    mean = ROOT.RooRealVar("mean_"+label,"mean_"+label,param['mean']["val"])
    sigma = ROOT.RooRealVar("sigma_"+label,"sigma_"+label,param['sigma']["val"])
    alpha = ROOT.RooRealVar("alpha_"+label,"alpha_"+label,param['alpha']["val"])
    n = ROOT.RooRealVar("n_"+label,"n_"+label,param['n']["val"])
    alpha2 = ROOT.RooRealVar("alpha2_"+label,"alpha2_"+label,param['alpha2']["val"])
    n2 = ROOT.RooRealVar("n2_"+label,"n2_"+label,param['n2']["val"])
    return [mean,sigma,alpha,n,alpha2,n2]


def setMjetFuncUp(param,label=""):
    m=5
    up_mean    = ROOT.RooRealVar("mean_"+label,"mean_"+label,param['mean']["val"]       + param['mean']["err"]  *m)
    up_sigma   = ROOT.RooRealVar("sigma_"+label,"sigma_"+label,param['sigma']["val"]    + param['sigma']["err"] *m)
    up_alpha   = ROOT.RooRealVar("alpha_"+label,"alpha_"+label,param['alpha']["val"]    + param['alpha']["err"] *m)
    up_n       = ROOT.RooRealVar("n_"+label,"n_"+label,param['n']["val"]                + param['n']["err"]     *m)
    up_alpha2  = ROOT.RooRealVar("alpha2_"+label,"alpha2_"+label,param['alpha2']["val"] + param['alpha2']["err"]*m)
    up_n2      = ROOT.RooRealVar("n2_"+label,"n2_"+label,param['n2']["val"]             + param["n2"]["err"]    *m)
    return [up_mean,up_sigma,up_alpha,up_n,up_alpha2,up_n2]

def setMjetFuncDown(param,label=""):
    m=5
    down_mean    = ROOT.RooRealVar("mean_"+label,"mean_"+label,param['mean']["val"]       - param['mean']["err"]  *m)
    down_sigma   = ROOT.RooRealVar("sigma_"+label,"sigma_"+label,param['sigma']["val"]    - param['sigma']["err"] *m)
    down_alpha   = ROOT.RooRealVar("alpha_"+label,"alpha_"+label,param['alpha']["val"]    - param['alpha']["err"] *m)
    down_n       = ROOT.RooRealVar("n_"+label,"n_"+label,param['n']["val"]                - param['n']["err"]     *m)
    down_alpha2  = ROOT.RooRealVar("alpha2_"+label,"alpha2_"+label,param['alpha2']["val"] - param['alpha2']["err"]*m)
    down_n2      = ROOT.RooRealVar("n2_"+label,"n2_"+label,param['n2']["val"]             - param["n2"]["err"]    *m)
    return [down_mean,down_sigma,down_alpha,down_n,down_alpha2,down_n2]

def findErrorRegion(param,mjet,label=""):
    nominal = setMjetFunc(param,"nominal")
    mean   = nominal[0]
    sigma  = nominal[1]
    alpha  = nominal[2]
    n      = nominal[3]
    alpha2 = nominal[4]
    n2     = nominal[5]
    
    up = setMjetFuncUp(param,"up")
    up_mean    = up[0]
    up_sigma   = up[1]
    up_alpha   = up[2]
    up_n       = up[3]
    up_alpha2  = up[4]
    up_n2      = up[5]
    
    down = setMjetFuncDown(param,"down")
    down_mean    = down[0]
    down_sigma   = down[1]
    down_alpha   = down[2]
    down_n       = down[3]
    down_alpha2  = down[4]
    down_n2      = down[5]


    arg = ROOT.RooArgSet(mjet)
    
    variables = [[mean,up_mean,down_mean],[sigma,up_sigma,down_sigma],[alpha,up_alpha,down_alpha],[n,up_n,down_n],[alpha2,up_alpha2,down_alpha2],[n2,up_n2,down_n2]]
    period=[0,1,2]
    max=[]
    min=[]
    x = []
    for i in range(0,1000):
        m = mjet.getMin()+i*(mjet.getMax()-mjet.getMin())/1000.
        w = (mjet.getMax()-mjet.getMin())/1000.
        mjet.setVal(m)
        mmin = 10000000
        mmax = -11111111111
        for j in period:
            for j1 in period:
                for j2 in period:
                    for j3 in period:
                        for j4 in period:
                            for j5 in period:
                                func = ROOT.RooDoubleCB("nominal",'model',mjet,variables[0][j],variables[1][j1],variables[2][j2],variables[3][j3],variables[4][j4],variables[5][j5])
                                v = func.getVal(arg)
                                if v <= mmin:
                                    mmin =v
                                if v>= mmax:
                                    mmax =v
        
        max.append(mmax*w)
        min.append(mmin*w)
        x.append(m)
    return [max,min,x]

if __name__=="__main__":
    # l1 
    x = ROOT.RooRealVar("mjet","mjet",55,215)
    frame = x.frame()
    test_frame = x.frame()
    
    param = setMjetFunc(JJ_WJets_HPHP_Res_l1_0,"nominal") 
    func = ROOT.RooDoubleCB("nominal",'model',x,param[0],param[1],param[2],param[3],param[4],param[5])
    
    param_alt1 = setMjetFunc(JJ_WJets_HPHP_Res_l1_1,"alt1")
    func_alt1 = ROOT.RooDoubleCB("nominal",'model',x,param_alt1[0],param_alt1[1],param_alt1[2],param_alt1[3],param_alt1[4],param_alt1[5])
    
    param_alt2 = setMjetFunc(JJ_WJets_HPHP_Res_l1_2,"alt2")
    func_alt2 = ROOT.RooDoubleCB("nominal",'model',x,param_alt2[0],param_alt2[1],param_alt2[2],param_alt2[3],param_alt2[4],param_alt2[5])
    
    param_alt3 = setMjetFunc(JJ_WJets_HPHP_Res_l1_3,"alt3")
    func_alt3 = ROOT.RooDoubleCB("nominal",'model',x,param_alt3[0],param_alt3[1],param_alt3[2],param_alt3[3],param_alt3[4],param_alt3[5])
    
    param_alt4 = setMjetFunc(JJ_WJets_HPHP_Res_l1_4,"alt4")
    func_alt4 = ROOT.RooDoubleCB("nominal",'model',x,param_alt4[0],param_alt4[1],param_alt4[2],param_alt4[3],param_alt4[4],param_alt4[5])
    
    param_alt5 = setMjetFunc(JJ_WJets_HPHP_Res_l1_5,"alt5")
    func_alt5 = ROOT.RooDoubleCB("nominal",'model',x,param_alt5[0],param_alt5[1],param_alt5[2],param_alt5[3],param_alt5[4],param_alt5[5])
    
    #func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    #func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue))
    
    up_param =setMjetFuncUp(JJ_WJets_HPHP_Res_l1_0)
    down_param = setMjetFuncDown(JJ_WJets_HPHP_Res_l1_0)
    
    #func_up = ROOT.RooDoubleCB("up",'model',x,up_param[0],up_param[1],up_param[2],up_param[3],up_param[4],up_param[5])
    #func_down = ROOT.RooDoubleCB("down",'model',x,down_param[0],down_param[1],down_param[2],down_param[3],down_param[4],down_param[5])
    
    #func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    #func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    #mjet_nominal = setMjetFunc("nominal",x,JJ_WJets_HPHP_Res_l1_0)
    #print mjet_nominal
    #mjet_nominal.plotOn(frame)
    
    max, min , mjet = findErrorRegion(JJ_WJets_HPHP_Res_l1_0,x)
    hmin = ROOT.TH1F("min","min",len(mjet),mjet[0],mjet[-1])
    hmax = ROOT.TH1F("max","max",len(mjet),mjet[0],mjet[-1])
    i=0
    for m in mjet:
        hmin.Fill(m,min[i])
        hmax.Fill(m,max[i])
        i+=1
    
    arg = ROOT.RooArgSet(x)
    arglist = ROOT.RooArgList(arg)   
    func_up_h = ROOT.RooDataHist("up","up",arglist,ROOT.RooFit.Import(hmax))
    func_up =ROOT.RooHistPdf("up","hp",arglist,arglist,func_up_h)
    func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    
    func_down_h = ROOT.RooDataHist("down","down",arglist,ROOT.RooFit.Import(hmin))
    func_down =ROOT.RooHistPdf("down","down",arglist,arglist,func_down_h)
    func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    
    
    #g = ROOT.TGraph()
    #for i in range(0,len(mjet)):
        #g.SetPoint(i,mjet[i],max[i])
    #for i in range(len(mjet),2*len(mjet)):
        #g.SetPoint(i,mjet[i-len(mjet)],min[i-len(mjet)])
    
    #g.plotOn(frame)
    
    #func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt2.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt3.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt4.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt5.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    c = ROOT.TCanvas("c","c",400,400)
    frame.Draw()
    #test_frame.Draw()
    c.SaveAs("testCorrelations_Wjets.png")
    c.SaveAs("testCorrelations_Wjets.pdf")
    
    # l2 
    x = ROOT.RooRealVar("mjet","mjet",55,215)
    frame = x.frame()
    
    param = setMjetFunc(JJ_WJets_HPHP_Res_l2_0,"nominal") 
    func = ROOT.RooDoubleCB("nominal",'model',x,param[0],param[1],param[2],param[3],param[4],param[5])
    
    param_alt1 = setMjetFunc(JJ_WJets_HPHP_Res_l2_1,"alt1")
    func_alt1 = ROOT.RooDoubleCB("nominal",'model',x,param_alt1[0],param_alt1[1],param_alt1[2],param_alt1[3],param_alt1[4],param_alt1[5])
    
    param_alt2 = setMjetFunc(JJ_WJets_HPHP_Res_l2_2,"alt2")
    func_alt2 = ROOT.RooDoubleCB("nominal",'model',x,param_alt2[0],param_alt2[1],param_alt2[2],param_alt2[3],param_alt2[4],param_alt2[5])
    
    param_alt3 = setMjetFunc(JJ_WJets_HPHP_Res_l2_3,"alt3")
    func_alt3 = ROOT.RooDoubleCB("nominal",'model',x,param_alt3[0],param_alt3[1],param_alt3[2],param_alt3[3],param_alt3[4],param_alt3[5])
    
    param_alt4 = setMjetFunc(JJ_WJets_HPHP_Res_l2_4,"alt4")
    func_alt4 = ROOT.RooDoubleCB("nominal",'model',x,param_alt4[0],param_alt4[1],param_alt4[2],param_alt4[3],param_alt4[4],param_alt4[5])
    
    param_alt5 = setMjetFunc(JJ_WJets_HPHP_Res_l2_5,"alt5")
    func_alt5 = ROOT.RooDoubleCB("nominal",'model',x,param_alt5[0],param_alt5[1],param_alt5[2],param_alt5[3],param_alt5[4],param_alt5[5])
    
    
    max, min , mjet = findErrorRegion(JJ_WJets_HPHP_Res_l2_0,x)
    hmin = ROOT.TH1F("min","min",len(mjet),mjet[0],mjet[-1])
    hmax = ROOT.TH1F("max","max",len(mjet),mjet[0],mjet[-1])
    i=0
    for m in mjet:
        hmin.Fill(m,min[i])
        hmax.Fill(m,max[i])
        i+=1
    
    arg = ROOT.RooArgSet(x)
    arglist = ROOT.RooArgList(arg)   
    func_up_h = ROOT.RooDataHist("up","up",arglist,ROOT.RooFit.Import(hmax))
    func_up =ROOT.RooHistPdf("up","hp",arglist,arglist,func_up_h)
    func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    
    func_down_h = ROOT.RooDataHist("down","down",arglist,ROOT.RooFit.Import(hmin))
    func_down =ROOT.RooHistPdf("down","down",arglist,arglist,func_down_h)
    func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    

    func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt2.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt3.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt4.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt5.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    c = ROOT.TCanvas("c","c",400,400)
    frame.Draw()
    #test_frame.Draw()
    c.SaveAs("testCorrelations_Wjets_l2.png")
    c.SaveAs("testCorrelations_Wjets_l2.pdf")
    
    # l2 
    x = ROOT.RooRealVar("mjet","mjet",55,215)
    frame = x.frame()
    
    param = setMjetFunc(JJ_ZJets_HPHP_Res_l2_0,"nominal") 
    func = ROOT.RooDoubleCB("nominal",'model',x,param[0],param[1],param[2],param[3],param[4],param[5])
    
    param_alt1 = setMjetFunc(JJ_ZJets_HPHP_Res_l2_1,"alt1")
    func_alt1 = ROOT.RooDoubleCB("nominal",'model',x,param_alt1[0],param_alt1[1],param_alt1[2],param_alt1[3],param_alt1[4],param_alt1[5])
    
    param_alt2 = setMjetFunc(JJ_ZJets_HPHP_Res_l2_2,"alt2")
    func_alt2 = ROOT.RooDoubleCB("nominal",'model',x,param_alt2[0],param_alt2[1],param_alt2[2],param_alt2[3],param_alt2[4],param_alt2[5])
    
    param_alt3 = setMjetFunc(JJ_ZJets_HPHP_Res_l2_3,"alt3")
    func_alt3 = ROOT.RooDoubleCB("nominal",'model',x,param_alt3[0],param_alt3[1],param_alt3[2],param_alt3[3],param_alt3[4],param_alt3[5])
    
    param_alt4 = setMjetFunc(JJ_ZJets_HPHP_Res_l2_4,"alt4")
    func_alt4 = ROOT.RooDoubleCB("nominal",'model',x,param_alt4[0],param_alt4[1],param_alt4[2],param_alt4[3],param_alt4[4],param_alt4[5])
    
    param_alt5 = setMjetFunc(JJ_ZJets_HPHP_Res_l2_5,"alt5")
    func_alt5 = ROOT.RooDoubleCB("nominal",'model',x,param_alt5[0],param_alt5[1],param_alt5[2],param_alt5[3],param_alt5[4],param_alt5[5])
    
    
    max, min , mjet = findErrorRegion(JJ_ZJets_HPHP_Res_l2_0,x)
    hmin = ROOT.TH1F("min","min",len(mjet),mjet[0],mjet[-1])
    hmax = ROOT.TH1F("max","max",len(mjet),mjet[0],mjet[-1])
    i=0
    for m in mjet:
        hmin.Fill(m,min[i])
        hmax.Fill(m,max[i])
        i+=1
    
    arg = ROOT.RooArgSet(x)
    arglist = ROOT.RooArgList(arg)   
    func_up_h = ROOT.RooDataHist("up","up",arglist,ROOT.RooFit.Import(hmax))
    func_up =ROOT.RooHistPdf("up","hp",arglist,arglist,func_up_h)
    func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    
    func_down_h = ROOT.RooDataHist("down","down",arglist,ROOT.RooFit.Import(hmin))
    func_down =ROOT.RooHistPdf("down","down",arglist,arglist,func_down_h)
    func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    

    func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt2.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt3.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt4.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt5.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    c = ROOT.TCanvas("c","c",400,400)
    frame.Draw()
    #test_frame.Draw()
    c.SaveAs("testCorrelations_Zjets_l2.png")
    c.SaveAs("testCorrelations_Zjets_l2.pdf")
    
    
    # l1 
    x = ROOT.RooRealVar("mjet","mjet",55,215)
    frame = x.frame()
    
    param = setMjetFunc(JJ_ZJets_HPHP_Res_l1_0,"nominal") 
    func = ROOT.RooDoubleCB("nominal",'model',x,param[0],param[1],param[2],param[3],param[4],param[5])
    
    param_alt1 = setMjetFunc(JJ_ZJets_HPHP_Res_l1_1,"alt1")
    func_alt1 = ROOT.RooDoubleCB("nominal",'model',x,param_alt1[0],param_alt1[1],param_alt1[2],param_alt1[3],param_alt1[4],param_alt1[5])
    
    param_alt2 = setMjetFunc(JJ_ZJets_HPHP_Res_l1_2,"alt2")
    func_alt2 = ROOT.RooDoubleCB("nominal",'model',x,param_alt2[0],param_alt2[1],param_alt2[2],param_alt2[3],param_alt2[4],param_alt2[5])
    
    param_alt3 = setMjetFunc(JJ_ZJets_HPHP_Res_l1_3,"alt3")
    func_alt3 = ROOT.RooDoubleCB("nominal",'model',x,param_alt3[0],param_alt3[1],param_alt3[2],param_alt3[3],param_alt3[4],param_alt3[5])
    
    param_alt4 = setMjetFunc(JJ_ZJets_HPHP_Res_l1_4,"alt4")
    func_alt4 = ROOT.RooDoubleCB("nominal",'model',x,param_alt4[0],param_alt4[1],param_alt4[2],param_alt4[3],param_alt4[4],param_alt4[5])
    
    param_alt5 = setMjetFunc(JJ_ZJets_HPHP_Res_l1_5,"alt5")
    func_alt5 = ROOT.RooDoubleCB("nominal",'model',x,param_alt5[0],param_alt5[1],param_alt5[2],param_alt5[3],param_alt5[4],param_alt5[5])
    
    
    max, min , mjet = findErrorRegion(JJ_ZJets_HPHP_Res_l1_0,x)
    hmin = ROOT.TH1F("min","min",len(mjet),mjet[0],mjet[-1])
    hmax = ROOT.TH1F("max","max",len(mjet),mjet[0],mjet[-1])
    i=0
    for m in mjet:
        hmin.Fill(m,min[i])
        hmax.Fill(m,max[i])
        i+=1
    
    arg = ROOT.RooArgSet(x)
    arglist = ROOT.RooArgList(arg)   
    func_up_h = ROOT.RooDataHist("up","up",arglist,ROOT.RooFit.Import(hmax))
    func_up =ROOT.RooHistPdf("up","hp",arglist,arglist,func_up_h)
    func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    
    func_down_h = ROOT.RooDataHist("down","down",arglist,ROOT.RooFit.Import(hmin))
    func_down =ROOT.RooHistPdf("down","down",arglist,arglist,func_down_h)
    func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    

    func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt2.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt3.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt4.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt5.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    c = ROOT.TCanvas("c","c",400,400)
    frame.Draw()
    #test_frame.Draw()
    c.SaveAs("testCorrelations_Zjets.png")
    c.SaveAs("testCorrelations_Zjets.pdf")
    
    
    ####################### Wjet HPLP ####################################################################
    # l1 
    x = ROOT.RooRealVar("mjet","mjet",55,215)
    frame = x.frame()
    test_frame = x.frame()
    
    param = setMjetFunc(JJ_WJets_HPLP_Res_l1_0,"nominal") 
    func = ROOT.RooDoubleCB("nominal",'model',x,param[0],param[1],param[2],param[3],param[4],param[5])
    
    param_alt1 = setMjetFunc(JJ_WJets_HPLP_Res_l1_1,"alt1")
    func_alt1 = ROOT.RooDoubleCB("nominal",'model',x,param_alt1[0],param_alt1[1],param_alt1[2],param_alt1[3],param_alt1[4],param_alt1[5])
    
    param_alt2 = setMjetFunc(JJ_WJets_HPLP_Res_l1_2,"alt2")
    func_alt2 = ROOT.RooDoubleCB("nominal",'model',x,param_alt2[0],param_alt2[1],param_alt2[2],param_alt2[3],param_alt2[4],param_alt2[5])
    
    param_alt3 = setMjetFunc(JJ_WJets_HPLP_Res_l1_3,"alt3")
    func_alt3 = ROOT.RooDoubleCB("nominal",'model',x,param_alt3[0],param_alt3[1],param_alt3[2],param_alt3[3],param_alt3[4],param_alt3[5])
    
    param_alt4 = setMjetFunc(JJ_WJets_HPLP_Res_l1_4,"alt4")
    func_alt4 = ROOT.RooDoubleCB("nominal",'model',x,param_alt4[0],param_alt4[1],param_alt4[2],param_alt4[3],param_alt4[4],param_alt4[5])
    
    param_alt5 = setMjetFunc(JJ_WJets_HPLP_Res_l1_5,"alt5")
    func_alt5 = ROOT.RooDoubleCB("nominal",'model',x,param_alt5[0],param_alt5[1],param_alt5[2],param_alt5[3],param_alt5[4],param_alt5[5])
    
    #func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    #func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue))
    
    up_param =setMjetFuncUp(JJ_WJets_HPLP_Res_l1_0)
    down_param = setMjetFuncDown(JJ_WJets_HPLP_Res_l1_0)
    
    #func_up = ROOT.RooDoubleCB("up",'model',x,up_param[0],up_param[1],up_param[2],up_param[3],up_param[4],up_param[5])
    #func_down = ROOT.RooDoubleCB("down",'model',x,down_param[0],down_param[1],down_param[2],down_param[3],down_param[4],down_param[5])
    
    #func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    #func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    #mjet_nominal = setMjetFunc("nominal",x,JJ_WJets_HPLP_Res_l1_0)
    #print mjet_nominal
    #mjet_nominal.plotOn(frame)
    
    max, min , mjet = findErrorRegion(JJ_WJets_HPLP_Res_l1_0,x)
    hmin = ROOT.TH1F("min","min",len(mjet),mjet[0],mjet[-1])
    hmax = ROOT.TH1F("max","max",len(mjet),mjet[0],mjet[-1])
    i=0
    for m in mjet:
        hmin.Fill(m,min[i])
        hmax.Fill(m,max[i])
        i+=1
    
    arg = ROOT.RooArgSet(x)
    arglist = ROOT.RooArgList(arg)   
    func_up_h = ROOT.RooDataHist("up","up",arglist,ROOT.RooFit.Import(hmax))
    func_up =ROOT.RooHistPdf("up","hp",arglist,arglist,func_up_h)
    func_up.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kBlue),ROOT.RooFit.DrawOption("F"))
    
    func_down_h = ROOT.RooDataHist("down","down",arglist,ROOT.RooFit.Import(hmin))
    func_down =ROOT.RooHistPdf("down","down",arglist,arglist,func_down_h)
    func_down.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kWhite),ROOT.RooFit.DrawOption("F"))
    
    
    #g = ROOT.TGraph()
    #for i in range(0,len(mjet)):
        #g.SetPoint(i,mjet[i],max[i])
    #for i in range(len(mjet),2*len(mjet)):
        #g.SetPoint(i,mjet[i-len(mjet)],min[i-len(mjet)])
    
    #g.plotOn(frame)
    
    #func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    func_alt1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt2.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt3.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt4.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func_alt5.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineWidth(1))
    func.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlack))
    c = ROOT.TCanvas("c","c",400,400)
    frame.Draw()
    #test_frame.Draw()
    c.SaveAs("testCorrelations_Wjets.png")
    c.SaveAs("testCorrelations_Wjets.pdf")
    
    