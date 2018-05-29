import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '


indir = sys.argv[1] #"/home/dschaefer/DiBoson3D/forBiasTests/"

purities=['HPHP']#,'HPLP']
if sys.argv[2]!="":
    purities=[sys.argv[2]]
signals = ["BulkGWW"]
print indir
print purities

for sig in signals:
  for p in purities:

    cat='_'.join(['JJ',sig,p,'13TeV'])
    card=DataCardMaker('',p,'13TeV',35900,'JJ',cat)
    cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

    #SIGNAL
    card.addMVVSignalParametricShape2("%s_MVV"%sig,"MJJ",indir+"JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1",indir+"JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2",indir+"JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addParametricYieldWithUncertainty("%s"%sig,0,indir+"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
    card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)

    #Vjets
    if p=='HPHP': from JJ_VJets_HPHP import JJ_VJets__Res_l1, JJ_VJets__Res_l2
    if p=='HPLP': from JJ_VJets_HPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2
    if p=='LPLP': from JJ_VJets_LPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2


    #card.addMVVBackgroundShapeQCD("Vjets_mjj","MJJ",True,"",JJ_VJets__MVV)
    card.addHistoShapeFromFile("Vjets_mjj",["MJJ"],indir+"JJ_VJets_MVV_"+p+".root","histo_nominal",['PT:CMS_VV_JJ_Vjets_PT','OPT:CMS_VV_JJ_Vjets_OPT'],False,0)
    card.addMjetBackgroundShapeVJetsRes("Vjets_mjetRes_l1","MJ1","",JJ_VJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMjetBackgroundShapeVJetsRes("Vjets_mjetRes_l2","MJ2","",JJ_VJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})

    card.product3D("Vjet","Vjets_mjetRes_l1","Vjets_mjetRes_l2","Vjets_mjj")
    card.addFixedYieldFromFile("Vjet",1,indir+"JJ_VJets_%s.root"%p,"VJets",1.0)

    #QCD
    rootFile0=indir+"JJ_nonRes_3D_"+p+".root"
    rootFile=indir+"JJ_nonRes_3D_HPLP.root"
    card.addShapes("nonRes",["MJ1","MJ2","MJJ"],rootFile0,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','PTZ:CMS_VV_JJ_nonRes_PTZ','OPTZ:CMS_VV_JJ_nonRes_OPTZ'],False,0,"",rootFile,['altshape2Z:CMS_VV_JJ_nonRes_Alt2','altshapeZ:CMS_VV_JJ_nonRes_Alt']) 
    #card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['altshape:CMS_VV_JJ_nonRes_altshape','altshape2:CMS_VV_JJ_nonRes_altshape2','PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','PTZ:CMS_VV_JJ_nonRes_PTZ','OPTZ:CMS_VV_JJ_nonRes_OPTZ','TRIG:CMS_VV_JJ_nonRes_TRIG'],False,0)
    card.addFixedYieldFromFile("nonRes",2,indir+"JJ_"+p+".root","nonRes")

    #DATA
    #card.importBinnedData(indir+"jen-data-obs.root","data",["MJ1","MJ2","MJJ"])
    #card.importBinnedData(indir+"JJ_data_"+p+".root","data",["MJ1","MJ2","MJJ"])
    card.importBinnedData(indir+"pseudodata_"+p+".root","data",["MJ1","MJ2","MJJ"])

    #SYSTEMATICS
    #luminosity
    card.addSystematic("CMS_lumi","lnN",{'%s'%sig:1.026,"Vjet":1.026})

    #card.addSystematic("CMS_lumi","lnN",{'%s'%sig:1.026})

    #kPDF uncertainty for the signal
    card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})

    #background normalization
    card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})
    card.addSystematic("CMS_VV_JJ_Vjets_norm_"+p,"lnN",{'Vjet':1.02})

    #tau21 

    if p=='HPHP': #card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1+0.14})
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1+0.14,"Vjet":1+0.14})
    else: #card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1-0.33})
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1-0.33,"Vjet":1-0.33})

    #pruned mass scale    
    card.addSystematic("CMS_scale_j","param",[0.0,0.02])
    card.addSystematic("CMS_res_j","param",[0.0,0.05])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.009])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.2])

    #dijet function parameters for V+jets
    card.addSystematic("CMS_VV_JJ_Vjets_PT","param",[0,0.1])
    card.addSystematic("CMS_VV_JJ_Vjets_OPT","param",[0,0.1])
 
    #alternative shapes for QCD background
    card.addSystematic("CMS_VV_JJ_nonRes_OPTXY","param",[0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTZ","param", [0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_PTXY","param", [0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_PTZ","param",  [0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_Alt2","param",  [0,0.888])
    card.addSystematic("CMS_VV_JJ_nonRes_Alt","param",  [0,0.888])
    #card.addSystematic("CMS_VV_JJ_nonRes_Alt2_hp","param",  [0,0.888])
    #card.addSystematic("CMS_VV_JJ_nonRes_Alt_hp","param",  [0,0.888])
    #card.addSystematic("CMS_VV_JJ_nonRes_Alt2XY","param",  [0,0.888])
    #card.addSystematic("CMS_VV_JJ_nonRes_AltXY","param",  [0,0.888])

    card.makeCard()

    #make combined cards
    cmd=cmd + ' >> datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt '
    print cmd
