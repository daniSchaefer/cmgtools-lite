import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

purities=['HP','LP']

for p in purities:

 card=DataCardMaker('',p,'13TeV',35900,'JJ')
 cat='_'.join(['JJ',p,'13TeV'])
 cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

 #SIGNAL
 card.addMVVSignalParametricShape2("XqW_MVV","MJJ","JJ_XqW_MVV.json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
 card.addMVVSignalParametricShape2("XqZ_MVV","MJJ","JJ_XqZ_MVV.json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})

 if p=='LP':
     card.addMJJSignalParametricShape("Wqq","MJ","JJ_XqW_MJJ_"+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
     card.addMJJSignalParametricShape("Zqq","MJ","JJ_XqZ_MJJ_"+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})

     card.addParametricYieldWithUncertainty("XqW",0,"JJ_XqW_"+p+"_yield.json",1,'CMS_tau21_PtDependence','((0.054/0.041)*(-log(MH/600)))',0.041)
     card.addParametricYieldWithUncertainty("XqZ",0,"JJ_XqZ_"+p+"_yield.json",1,'CMS_tau21_PtDependence','((0.054/0.041)*(-log(MH/600)))',0.041)
 else:
     card.addMJJSignalParametricShapeNOEXP("Wqq","MJ","JJ_XqW_MJJ_"+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#
     card.addMJJSignalParametricShapeNOEXP("Zqq","MJ","JJ_XqZ_MJJ_"+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#

     card.addParametricYieldWithUncertainty("XqW",0,"JJ_XqW_"+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
     card.addParametricYieldWithUncertainty("XqZ",0,"JJ_XqZ_"+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
     
 card.product("XqW","Wqq","XqW_MVV")
 card.product("XqZ","Zqq","XqZ_MVV")

 #QCD
 rootFile="JJ_nonRes_2D_"+p+".root"
 qcdTag ="_".join([p])
 card.addHistoShapeFromFile("nonRes",["MJJ","MJ"],rootFile,"histo",['PTX:CMS_VV_JJ_nonRes_PTX_'+qcdTag,'OPTX:CMS_VV_JJ_nonRes_OPTX_'+qcdTag,'OPTY:CMS_VV_JJ_nonRes_OPTY_'+qcdTag,'PTY:CMS_VV_JJ_nonRes_PTY_'+qcdTag],False,0)                    
 card.addFixedYieldFromFile("nonRes",1,"JJ_"+p+".root","nonRes")

 #DATA
 card.importBinnedData("JJ_"+p+".root","data",["MJJ","MJ"])
 
 #SYSTEMATICS

 #luminosity
 card.addSystematic("CMS_lumi","lnN",{'XWW':1.026,'XWZ':1.026})

 #kPDF uncertainty for the signal
 card.addSystematic("CMS_pdf","lnN",{'XWW':1.01,'XWZ':1.01})

 #W+jets cross section in acceptance-dominated by pruned mass
 card.addSystematic("CMS_VV_JJ_nonRes_norm_"+lepton+"_"+purity+"_"+category,"lnN",{'nonRes':1.5})
 #card.addSystematic("CMS_VV_LNuJ_resW_norm_"+lepton+"_"+purity+"_"+category,"lnN",{'resW':1.20})

 #tau21 
 if p=='HP':
     card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'XqW':1+0.14,'XqZ':1+0.14})
 if p=='LP':
     card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'XqW':1-0.33,'XqZ':1-0.33})
               
 #pruned mass scale    
 card.addSystematic("CMS_scale_j","param",[0.0,0.02])
 card.addSystematic("CMS_res_j","param",[0.0,0.05])
 card.addSystematic("CMS_scale_prunedj","param",[0.0,0.0094])
 card.addSystematic("CMS_res_prunedj","param",[0.0,0.2])
 #card.addSystematic('CMS_VV_topPt_0_'+lepton+"_"+purity+"_"+category,"param",[0.0,0.2])
 #card.addSystematic('CMS_VV_topPt_1_'+lepton+"_"+purity+"_"+category,"param",[0.0,25000.0])

 card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
 card.addSystematic("CMS_res_MET","param",[0.0,0.01])
 card.addSystematic("CMS_VV_JJ_nonRes_PTX_"+qcdTag,"param",[0.0,0.333])
 card.addSystematic("CMS_VV_JJ_nonRes_OPTX_"+qcdTag,"param",[0.0,0.333])
 card.addSystematic("CMS_VV_JJ_nonRes_PTY_"+qcdTag,"param",[0.0,333])
 card.addSystematic("CMS_VV_JJ_nonRes_OPTY_"+qcdTag,"param",[0.0,0.6])

 card.makeCard()

#make combined cards
print cmd
