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

   
   

 
    # signal paramterisation:
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
    
    
    if p=='HPHP':
        ##V+jets background ##############################################################################
        #from JJ_WJets_HPHP_jecv6 import JJ_WJets__MVV, JJ_WJets__Res_l1, JJ_WJets__ratio_l1, JJ_WJets__Res_l2, JJ_WJets__ratio_l2
        #from JJ_ZJets_HPHP_jecv6 import JJ_ZJets__MVV, JJ_ZJets__Res_l1, JJ_ZJets__ratio_l1, JJ_ZJets__Res_l2, JJ_ZJets__ratio_l2
        from JJ_VJets_HPHP_jecv6 import JJ_VJets__MVV, JJ_VJets__Res_l1, JJ_VJets__ratio_l1, JJ_VJets__Res_l2, JJ_VJets__ratio_l2
    if p=='HPLP':
        #V+jets background ##############################################################################
        from JJ_WJets_HPLP_jecv6 import JJ_WJets__MVV, JJ_WJets__Res_l1, JJ_WJets__ratio_l1, JJ_WJets__Res_l2, JJ_WJets__ratio_l2
        from JJ_ZJets_HPLP_jecv6 import JJ_ZJets__MVV, JJ_ZJets__Res_l1, JJ_ZJets__ratio_l1, JJ_ZJets__Res_l2, JJ_ZJets__ratio_l2

    print " start with vjets backgrounds"
     
    #card.addMVVBackgroundShapeQCD("Wjets_mjj","MJJ",True,"",JJ_WJets__MVV)
    #card.addMjetBackgroundShapeVJetsRes("Wjets_mjetRes_l1","MJ1","",JJ_WJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    #card.addMjetBackgroundShapeVJetsRes("Wjets_mjetRes_l2","MJ2","",JJ_WJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    #card.product3D("Wjet","Wjets_mjetRes_l1","Wjets_mjetRes_l2","Wjets_mjj")
    #card.addFixedYieldFromFile("Wjet",1,"JJ_WJets_HPHP_jecv6.root","WJets",JJ_WJets__ratio_l1)
        
        
        
    #card.addMVVBackgroundShapeQCD("Zjets_mjj","MJJ",True,"",JJ_ZJets__MVV)
    #card.addMjetBackgroundShapeVJetsRes("Zjets_mjetRes_l1","MJ1","",JJ_ZJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    #card.addMjetBackgroundShapeVJetsRes("Zjets_mjetRes_l2","MJ2","",JJ_ZJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    #card.product3D("Zjet","Zjets_mjetRes_l1","Zjets_mjetRes_l2","Zjets_mjj")
    #card.addFixedYieldFromFile("Zjet",1,"JJ_ZJets_HPHP_jecv6.root","ZJets",JJ_ZJets__ratio_l1)
        
    ## add systematics for mjj part of resoant vjets contribution
    #card.addSystematic("CMS_VV_JJ_p0_Wjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_WJets__MVV['p0']['val'],JJ_WJets__MVV['p0']['err']*200])
    #card.addSystematic("CMS_VV_JJ_p0_Zjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_ZJets__MVV['p0']['val'],JJ_ZJets__MVV['p0']['err']*200])
    #card.addSystematic("CMS_VV_JJ_p1_Wjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_WJets__MVV['p1']['val'],JJ_WJets__MVV['p1']['err']*100])
    #card.addSystematic("CMS_VV_JJ_p1_Zjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_ZJets__MVV['p1']['val'],JJ_ZJets__MVV['p1']['err']*100])
    #card.addSystematic("CMS_VV_JJ_p2_Wjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_WJets__MVV['p2']['val'],JJ_WJets__MVV['p2']['err']*100])
    #card.addSystematic("CMS_VV_JJ_p2_Zjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_ZJets__MVV['p2']['val'],JJ_ZJets__MVV['p2']['err']*100])
    
    
    card.addMVVBackgroundShapeQCD("Vjets_mjj","MJJ",True,"",JJ_VJets__MVV)
    card.addMjetBackgroundShapeVJetsRes("Vjets_mjetRes_l1","MJ1","",JJ_VJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMjetBackgroundShapeVJetsRes("Vjets_mjetRes_l2","MJ2","",JJ_VJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.product3D("Vjet","Vjets_mjetRes_l1","Vjets_mjetRes_l2","Vjets_mjj")
    card.addFixedYieldFromFile("Vjet",1,"JJ_VJets_HPHP.root","VJets",JJ_VJets__ratio_l1)
        
    # add systematics for mjj part of resoant vjets contribution
    
    card.addSystematic("CMS_VV_JJ_p0_Vjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_VJets__MVV['p0']['val'],1])
    card.addSystematic("CMS_VV_JJ_p1_Vjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_VJets__MVV['p1']['val'],1])
    card.addSystematic("CMS_VV_JJ_p2_Vjets_mjj_JJ_WprimeWZ_"+p+"_13TeV","param",[JJ_VJets__MVV['p2']['val'],1])
        # end V+jets background ####################################################
    
    
    
    #QCD
    rootFile="JJ_nonRes_2D_"+p+".root"

    card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','OPTZ:CMS_VV_JJ_nonRes_OPTZ','PTZ:CMS_VV_JJ_nonRes_PTZ'],False,0)    
    card.addFixedYieldFromFile("nonRes",2,"JJ_"+p+".root","nonRes")

   #DATA
    card.importBinnedData("JJ_"+p+".root","data",["MJ1","MJ2","MJJ"])
 
   #SYSTEMATICS

   #luminosity
    card.addSystematic("CMS_lumi","lnN",{sig:1.026})#,"Vjet":1.026})

   #kPDF uncertainty for the signal
    card.addSystematic("CMS_pdf","lnN",{sig:1.01})#,"Vjet":1.01})

   #W+jets cross section in acceptance-dominated by pruned mass
    card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})
   
    #card.addSystematic("CMS_VV_JJ_Wjets_norm_"+p,"lnN",{'Wjet':1.02})
    #card.addSystematic("CMS_VV_JJ_Zjets_norm_"+p,"lnN",{'Zjet':1.02})
    card.addSystematic("CMS_VV_JJ_Vjets_norm_"+p,"lnN",{'Vjet':1.02})

   #tau21 
    if p=='HPHP':
       card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s':1+0.14})
    if p=='HPLP':
       card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s':1-0.33})
               
    #pruned mass scale    
    card.addSystematic("CMS_scale_j","param",[0.0,0.02])
    card.addSystematic("CMS_res_j","param",[0.0,0.05])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    card.addSystematic("CMS_res_prunedj","param",[-0.2,0.001])
    #card.addSystematic("CMS_res_prunedj","param",[-0.1,0.05])
    #card.addSystematic("CMS_scale_prunedj","param",[0.0,0.0])
    #card.addSystematic("CMS_res_prunedj1","param",[-0.2,0.2])
    #card.addSystematic("CMS_res_prunedj2","param",[-0.2,0.2])
   
   
   
    # #alternative shapes
    card.addSystematic("CMS_VV_JJ_nonRes_PTXY","param",[0.0,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_PTZ","param",[0.0,0.333])
    #card.addSystematic("CMS_VV_JJ_nonRes_PT2","param",[0.0,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTXY","param",[0.0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTZ","param",[0.0,0.333])
    #card.addSystematic("CMS_VV_JJ_nonRes_OPT2","param",[0.0,0.333])
    card.makeCard()

  #make combined cards
  cmd=cmd + ' >> datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt '
  print cmd
