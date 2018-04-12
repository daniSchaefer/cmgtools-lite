import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '



purities=['HPHP']#,'HPLP']
signals = ["BulkGWW"]

for sig in signals:
  for p in purities:

    cat='_'.join(['JJ',sig,p,'13TeV'])
    card=DataCardMaker('',p,'13TeV',35900,'JJ',cat)
    cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

    #SIGNAL
    card.addMVVSignalParametricShape2("%s_MVV"%sig,"MJJ","JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addParametricYieldWithUncertainty("%s"%sig,0,"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
    card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)

    #Vjets
    if p=='HPHP': from JJ_VJets_HPHP import JJ_VJets__MVV, JJ_VJets__Res_l1, JJ_VJets__ratio_l1, JJ_VJets__Res_l2, JJ_VJets__ratio_l2
    if p=='HPLP': from JJ_VJets_HPLP import JJ_VJets__MVV, JJ_VJets__Res_l1, JJ_VJets__ratio_l1, JJ_VJets__Res_l2, JJ_VJets__ratio_l2
    if p=='LPLP': from JJ_VJets_LPLP import JJ_VJets__MVV, JJ_VJets__Res_l1, JJ_VJets__ratio_l1, JJ_VJets__Res_l2, JJ_VJets__ratio_l2

    card.addMVVBackgroundShapeQCD("Vjets_mjj","MJJ",True,"",JJ_VJets__MVV)
    card.addMjetBackgroundShapeVJetsGaus("Vjets_mjetRes_l1","MJ1","",JJ_VJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMjetBackgroundShapeVJetsGaus("Vjets_mjetRes_l2","MJ2","",JJ_VJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.product3D("Vjet","Vjets_mjetRes_l1","Vjets_mjetRes_l2","Vjets_mjj")
    card.addFixedYieldFromFile("Vjet",1,"JJ_VJets_%s.root"%p,"VJets",1.0)

    #QCD
    qcd_dir = "/home/dschaefer/DiBoson3D/forBiasTests/"
    rootFile=qcd_dir+"JJ_nonRes_3D_"+p+".root"
    card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','PTZ:CMS_VV_JJ_nonRes_PTZ','OPTZ:CMS_VV_JJ_nonRes_OPTZ'],False,0)    
    card.addFixedYieldFromFile("nonRes",2,qcd_dir+"JJ_pythia_"+p+".root","nonRes")

    #DATA
    card.importBinnedData(qcd_dir+"pseudodata_"+p+".root","data",["MJ1","MJ2","MJJ"])

    #SYSTEMATICS

    #luminosity
    card.addSystematic("CMS_lumi","lnN",{'%s'%sig:1.026,"Vjet":1.026})

    #kPDF uncertainty for the signal
    card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01,"Vjet":1.01})

    #background normalization
    card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})
    card.addSystematic("CMS_VV_JJ_Vjets_norm_"+p,"lnN",{'Vjet':1.02})

    #tau21 
    if p=='HPHP': card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'BulkGWW':1+0.14})
    else: card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'BulkGWW':1-0.33})

    #pruned mass scale    
    card.addSystematic("CMS_scale_j","param",[0.0,0.02])
    card.addSystematic("CMS_res_j","param",[0.0,0.05])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
    #card.addSystematic("CMS_res_prunedj","param",[-0.2,0.001])
    card.addSystematic("CMS_res_prunedj","param",[-0.0,0.2])

    #dijet function parameters for V+jets
    card.addSystematic("CMS_VV_JJ_p0_Vjets_mjj_JJ_"+p+"_13TeV","param",[JJ_VJets__MVV['CMS_p0']['val'],1.0])
    card.addSystematic("CMS_VV_JJ_p1_Vjets_mjj_JJ_"+p+"_13TeV","param",[JJ_VJets__MVV['CMS_p1']['val'],1.0])
    card.addSystematic("CMS_VV_JJ_p2_Vjets_mjj_JJ_"+p+"_13TeV","param",[JJ_VJets__MVV['CMS_p2']['val'],1.0])
    
    #alternative shapes for QCD background
    card.addSystematic("CMS_VV_JJ_nonRes_PTXY","param",[3.34103e-03,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_PTZ","param",[1.19886e-01,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTXY","param",[6.46206e-03,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTZ","param",[7.08497e-02,0.333])

    card.makeCard()

    #make combined cards
    cmd=cmd + ' >> datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt '
    print cmd
