import sys, os
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

period = 2017 #2016


#signals = ["BulkGZZ","BulkGWW","WprimeWZ"]
#signals = ["BulkGWW"]

for sig in signals:
  for p in purities:
    cat='_'.join(['JJ',sig,p,'13TeV'])
    print cat
    if period == 2016:
        card=DataCardMaker('',p,'13TeV',35900,'JJ',cat)
    else:
        card=DataCardMaker('',p,'13TeV',41367,'JJ',cat)
    cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '
    print "COMMAND = ",cmd
    #SIGNAL

    card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ","JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addParametricYieldWithUncertainty("%s"%sig,0,"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence','log(MH/600)',0.041)
    card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)
    
    #Vjets
    #execfile(indir+"JJ_VJets_HPHP.py")
    if p=='HPHP': from JJ_VJets_HPHP import JJ_VJets__Res_l1, JJ_VJets__Res_l2,JJ_VJets__nonRes_l1, JJ_VJets__nonRes_l2
    if p=='HPLP': from JJ_VJets_HPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2,JJ_VJets__nonRes_l1, JJ_VJets__nonRes_l2
    if p=='LPLP': from JJ_VJets_LPLP import JJ_VJets__Res_l1, JJ_VJets__Res_l2


    rootFile = 'JJ_VJets_MVV_'+p+'.root'
    card.addHistoShapeFromFile("Vjets_mjj",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Vjets_PTZ_'+p,'OPT:CMS_VV_JJ_Vjets_OPTZ_'+p],False,0)
    card.addMJJSignalShapeNOEXP("Vjets_mjetRes_l1","MJ1","",JJ_VJets__Res_l1,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.addMJJSignalShapeNOEXP("Vjets_mjetRes_l2","MJ2","",JJ_VJets__Res_l2,{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})
    card.product3D("Vjet","Vjets_mjetRes_l1","Vjets_mjetRes_l2","Vjets_mjj")
    card.addFixedYieldFromFile("Vjet",1,"JJ_VJets_%s.root"%p,"VJets",1.0)

    #QCD
    rootFile="JJ_nonRes_3D_"+p+".root"
    # card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY_'+p,'OPTXY:CMS_VV_JJ_nonRes_OPTXY_'+p,'PTZ:CMS_VV_JJ_nonRes_PTZ_'+p,'OPTZ:CMS_VV_JJ_nonRes_OPTZ_'+p,'TRIG:CMS_VV_JJ_nonRes_TRIG_'+p,'altshapeZ:CMS_VV_JJ_nonRes_altshapeZ_'+p,'altshape2Z:CMS_VV_JJ_nonRes_altshape2Z_'+p],False,0)
    card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PTXY:CMS_VV_JJ_nonRes_PTXY_'+p,'OPTXY:CMS_VV_JJ_nonRes_OPTXY_'+p,'PTZ:CMS_VV_JJ_nonRes_PTZ_'+p,'OPTZ:CMS_VV_JJ_nonRes_OPTZ_'+p],False,0) 
    card.addFixedYieldFromFile("nonRes",2,"JJ_nonRes_"+p+".root","nonRes")
    
    #DATA
    card.importBinnedData("JJ_data_"+p+".root","data",["MJ1","MJ2","MJJ"])
    
    #SYSTEMATICS
    #luminosity
    card.addSystematic("CMS_lumi","lnN",{'%s'%sig:1.026,"Vjet":1.026})
    
    #PDF uncertainty for the signal
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

    #systematics for dijet part of V+jets background
    card.addSystematic("CMS_VV_JJ_Vjets_PTZ_"+p,"param",[0,0.333])
    card.addSystematic("CMS_VV_JJ_Vjets_OPTZ_"+p,"param",[0,0.333])
    
    #alternative shapes for QCD background
    card.addSystematic("CMS_VV_JJ_nonRes_PTXY_"+p,"param",[0.0,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_PTZ_"+p,"param",[0.0,1.0])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTXY_"+p,"param",[0.0,0.333])
    card.addSystematic("CMS_VV_JJ_nonRes_OPTZ_"+p,"param",[0.0,1.0])
    # card.addSystematic("CMS_VV_JJ_nonRes_altshapeZ_"+p,"param",[0.0,1.0])
    # card.addSystematic("CMS_VV_JJ_nonRes_altshape2Z_"+p,"param",[0.0,1.0])
    #card.addSystematic("CMS_VV_JJ_nonRes_altshape3Z","param",[0.0,0.333]) 
    # card.addSystematic("CMS_VV_JJ_nonRes_TRIG_"+p,"param",[0.0,1.0])

    card.makeCard()
    cm='text2workspace.py %s -o %s'%('datacard_'+cat+'.txt','workspace_'+cat+'.root')
    print cm
    os.system(cm)


  #make combined cards
  combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","")+'.txt'
  os.system('rm %s'%combo_card)
  cmd+=' >> %s'%combo_card
  print cmd

  
  
  ################################################## madgraph HPHP QCD only fit ''''''''''''''''''''
    #CMS_VV_JJ_nonRes_OPTXY  -1.77253e-01   
    # CMS_VV_JJ_nonRes_OPTZ   6.82755e-02   
   # CMS_VV_JJ_nonRes_PTXY  -5.77556e-01   
   #  CMS_VV_JJ_nonRes_PTZ   1.60077e-01  
   #  CMS_VV_JJ_nonRes_TRIG   7.49123e-03   
   #  CMS_VV_JJ_nonRes_altshape   7.64363e-01  
   #  CMS_VV_JJ_nonRes_altshape2  -3.39454e-01   
   #  CMS_VV_JJ_nonRes_norm_HPHP  -5.41249e-06   
################################################## herwig HPHP QCD only fit ''''''''''''''''''''
#  CMS_VV_JJ_nonRes_OPTXY  -4.80407e-01  
#CMS_VV_JJ_nonRes_OPTZ   1.21991e-01   
   #  CMS_VV_JJ_nonRes_PTXY  -7.02057e-01  
   #  CMS_VV_JJ_nonRes_PTZ   3.41028e-02   
   #  CMS_VV_JJ_nonRes_TRIG  -1.21811e-01  
   #  CMS_VV_JJ_nonRes_altshape  -1.44828e-01   
   #  CMS_VV_JJ_nonRes_altshape2   7.56597e-01  
   #  CMS_VV_JJ_nonRes_norm_HPHP  -5.38621e-06  


################################################## NLO HPHP QCD only fit ''''''''''''''''''''
 #  CMS_VV_JJ_nonRes_OPTXY   4.93136e-02 
   #  CMS_VV_JJ_nonRes_OPTZ  -4.51575e-01  
   #  CMS_VV_JJ_nonRes_PTXY  -3.81257e-01  
   #  CMS_VV_JJ_nonRes_PTZ   1.25810e-01  
   #  CMS_VV_JJ_nonRes_TRIG  -2.07896e-01 
   #  CMS_VV_JJ_nonRes_altshape   4.54100e-01 
   #  CMS_VV_JJ_nonRes_altshape2  -4.61090e-01 
   #  CMS_VV_JJ_nonRes_norm_HPHP  -5.40528e-06  
  os.system(cmd)

  #make workspace
  workspace = combo_card.replace('datacard','workspace').replace('.txt','.root')
  cmd2='text2workspace.py %s -o %s'%(combo_card,workspace)
  print cmd2
  os.system(cmd2)

