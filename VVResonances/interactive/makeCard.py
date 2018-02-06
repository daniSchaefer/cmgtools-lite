import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '

purities=['HPHP','HPLP','LPLP']
purities=['HPHP']

signals = ["WprimeWZ"]
for sig in signals:
  for p in purities:

   card=DataCardMaker('',p,'13TeV',35900,'JJ_%s'%sig)
   cat='_'.join(['JJ',sig,p,'13TeV'])
   cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

   #SIGNAL
   card.addMVVSignalParametricShape2("%s_MVV"%sig,"MJJ","JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})

   if p=='HPLP':
       #card.addMJJSignalParametricShape("Wqq","MJ","JJ_%s_MJl1_"+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
       #card.addParametricYieldWithUncertainty("XqW",0,"JJ_%s_MJl1_"+p+".json",1,'CMS_tau21_PtDependence','((0.054/0.041)*(-log(MH/600)))',0.041)
       card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#
       card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2","JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#
       card.addParametricYieldWithUncertainty("%s"%sig,0,"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
   else:
       card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#
       card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})#

       card.addParametricYieldWithUncertainty("%s"%sig,0,"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
    
   card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)
   
   #QCD
   rootFile="test_JJ_nonRes_2D_"+p+".root"

   card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','OPTZ:CMS_VV_JJ_nonRes_OPTZ','PTZ:CMS_VV_JJ_nonRes_PTZ'],False,0)    
   card.addFixedYieldFromFile("nonRes",1,"JJ_"+p+".root","nonRes")

   #DATA
   card.importBinnedData("JJ_herwig_"+p+".root","data",["MJ1","MJ2","MJJ"])
 
   #SYSTEMATICS

   #luminosity
   card.addSystematic("CMS_lumi","lnN",{'%s':1.026})

   #kPDF uncertainty for the signal
   card.addSystematic("CMS_pdf","lnN",{'%s':1.01})

   #W+jets cross section in acceptance-dominated by pruned mass
   card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})

   #tau21 
   if p=='HPHP':
       card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s':1+0.14})
   if p=='HPLP':
       card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s':1-0.33})
               
   #pruned mass scale    
   card.addSystematic("CMS_scale_j","param",[0.0,0.02])
   card.addSystematic("CMS_res_j","param",[0.0,0.05])
   card.addSystematic("CMS_scale_prunedj","param",[0.0,0.0094])
   card.addSystematic("CMS_res_prunedj","param",[0.0,0.2])

   # #alternative shapes
   card.addSystematic("CMS_VV_JJ_nonRes_PTXY","param",[0.0,0.333])
   card.addSystematic("CMS_VV_JJ_nonRes_PTZ","param",[0.0,0.333])
   #card.addSystematic("CMS_VV_JJ_nonRes_PT2","param",[0.0,0.333])
   card.addSystematic("CMS_VV_JJ_nonRes_OPTXY","param",[0.0,0.333])
   card.addSystematic("CMS_VV_JJ_nonRes_OPTZ","param",[0.0,0.333])
   #card.addSystematic("CMS_VV_JJ_nonRes_OPT2","param",[0.0,0.333])
   card.makeCard()

  #make combined cards
  cmd=cmd + ' >> datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt '
  print cmd
