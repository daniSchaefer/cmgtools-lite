import sys
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '


indir = sys.argv[1] #"/home/dschaefer/DiBoson3D/forBiasTests/"
sys.path.append(indir)

purities=['HPHP']#,'HPLP']
if sys.argv[2]!="":
    purities=[sys.argv[2]]
signals = ["BulkGWW"]

period = 2016 #2016


for sig in signals:
  for p in purities:

    cat='_'.join(['JJ',sig,p,'13TeV'])
    if period == 2016:
        card=DataCardMaker('',p,'13TeV',35900,'JJ',cat)
    else:
        card=DataCardMaker('',p,'13TeV',41367,'JJ',cat)
    cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '

    ######################### SIGNAL #########################
    card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",indir+"JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1",indir+"JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2",indir+"JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addParametricYieldWithUncertainty("%s"%sig,0,indir+"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
    card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)

    ################# Vjets ##################################
    sys.path.append(indir) 
    if p=='HPHP': from JJ_VJets_HPHP import JJ_VJets__Res_l1, JJ_VJets__Res_l2
    if p=='HPLP': from JJ_VJets_HPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2
    if p=='LPLP': from JJ_VJets_LPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2

    print JJ_VJets__Res_l1['mean']

    card.addHistoShapeFromFile("Vjets_mjj",["MJJ"],indir+"JJ_VJets_MVV_"+p+".root","histo_nominal",['PT:CMS_VV_JJ_Vjets_PT','OPT:CMS_VV_JJ_Vjets_OPT'],False,0)#
    card.addMjetBackgroundShapeVJets2("Vjets_l1","MJ1","",JJ_VJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMjetBackgroundShapeVJets2("Vjets_l2","MJ2","",JJ_VJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    
    card.conditionalDoubleProduct("Wjet","Vjets_l1","Vjets_l2","MJJ","Vjets_mjj")
    
    card.addMjetBackgroundShapeTopPeak("Top_l1","MJ1","",JJ_VJets__Res_l1)
    card.addMjetBackgroundShapeTopPeak("Top_l2","MJ2","",JJ_VJets__Res_l2)
    
    card.conditionalDoubleProduct("Top","Top_l1","Top_l2","MJJ","Vjets_mjj")
    
    card.sum("Vjet","Wjet","Top",JJ_VJets__Res_l1["f"]["val"])
    
    

    card.addFixedYieldFromFile("Vjet",1,indir+"JJ_VJets_%s.root"%p,"VJets",1.0)

    ################# QCD #####################
 
    rootFile=indir+"JJ_nonRes_3D_"+p+".root"
    card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY','OPTXY:CMS_VV_JJ_nonRes_OPTXY','OPTY:CMS_VV_JJ_nonRes_OPTY','OPTX:CMS_VV_JJ_nonRes_OPTX','PTZ:CMS_VV_JJ_nonRes_PTZ','OPTZ:CMS_VV_JJ_nonRes_OPTZ'],False,0) #'altshapeZ:CMS_VV_JJ_nonRes_altshapeZ','altshape2Z:CMS_VV_JJ_nonRes_altshape2Z' 
    #'varBin1Z:CMS_VV_JJ_nonRes_varBin1Z','varBin2Z:CMS_VV_JJ_nonRes_varBin2Z','varBin3Z:CMS_VV_JJ_nonRes_varBin3Z','varBin4Z:CMS_VV_JJ_nonRes_varBin4Z','varBin5Z:CMS_VV_JJ_nonRes_varBin5Z','varBin6Z:CMS_VV_JJ_nonRes_varBin6Z','varBin7Z:CMS_VV_JJ_nonRes_varBin7Z','varBin8Z:CMS_VV_JJ_nonRes_varBin8Z','varBin9Z:CMS_VV_JJ_nonRes_varBin9Z','varBin10Z:CMS_VV_JJ_nonRes_varBin10Z','varBin11Z:CMS_VV_JJ_nonRes_varBin11Z'
    card.addFixedYieldFromFile("nonRes",2,indir+"JJ_nonRes_"+p+".root","nonRes",1.0)

    ################# DATA #####################
    card.importBinnedData(indir+"JJ_nonRes_"+p+".root","nonRes",["MJ1","MJ2","MJJ"])
    


    #############################  SYSTEMATICS ##############################
    #luminosity
    card.addSystematic("CMS_lumi","lnN",{'%s'%sig:1.026,"Vjet":1.026})


    #kPDF uncertainty for the signal
    card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})

    #background normalization
    card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})
    card.addSystematic("CMS_VV_JJ_Vjets_norm_"+p,"lnN",{'Vjet':1.02})

    #tau21 

    if p=='HPHP': 
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1+0.14,"Vjet":1+0.14})
    else: 
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:1-0.33,"Vjet":1-0.33})

    #softdrop mass scale/resolution    
    card.addSystematic("CMS_scale_j","param",[0.0,0.02])
    card.addSystematic("CMS_res_j","param",[0.0,0.05])
    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.009])
    card.addSystematic("CMS_res_prunedj","param",[0.0,0.2])
    #card.addSystematic("CMS_res_prunedj","param",[0.0,0.05])

    #dijet mass uncertainty for V+jets
    card.addSystematic("CMS_VV_JJ_Vjets_PT","param",[0,0.1])
    card.addSystematic("CMS_VV_JJ_Vjets_OPT","param",[0,0.1])
    
 
    #alternative shapes for QCD background

    card.addSystematic("CMS_VV_JJ_nonRes_PTXY","param",[0 ,0.33])
    card.addSystematic("CMS_VV_JJ_nonRes_PTZ","param",[0.0,0.33])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTXY","param",[0,0.33])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTY","param",[0,0.33])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTX","param",[0,0.33])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTZ","param",[0.0,0.33])
    #card.addSystematic("CMS_VV_JJ_nonRes_OPT2XY","param",[0.0,0.33])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin1Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin2Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin3Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin4Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin5Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin6Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin7Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin8Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin9Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin10Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_varBin11Z","param",[0.0,1])
    #card.addSystematic("CMS_VV_JJ_nonRes_altshape","param",[0.0,0.33])
    #card.addSystematic("CMS_VV_JJ_nonRes_altshape2","param",[0.0,0.33])

    card.makeCard()
  del card
    #make combined cards
  cmd=cmd + ' >> datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt '
  print "Combine cards: "
  print cmd
  cmd='text2workspace.py '+'datacard_'+cat+'.txt '+' -o workspace.root'
  print "Text to workspace: "
  print cmd
  
  
  
