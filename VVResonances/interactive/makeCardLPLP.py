import sys,os

import ROOT

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker

cmd='combineCards.py '



dataset='2016'



lumi = {'2016':35900,'2017':41367}

lumi_unc = {'2016':1.025,'2017':1.023}



vtag_unc = {'HPHP':{},'HPLP':{},'LPLP':{}}

vtag_unc['HPHP'] = {'2016':1.078,'2017':1.066}

vtag_unc['HPLP'] = {'2016':1.074,'2017':1.067}

vtag_unc['LPLP'] = {'2016':1.071,'2017':1.067}



vtag_pt_dependence = {'HPHP':'0.085*log(MH/400)*0.085*log(MH/400)','HPLP':'0.085*log(MH/400)*0.039*log(MH/400)','LPLP':'0.039*log(MH/400)*0.039*log(MH/400)'}



purities=['HPHP','HPLP']

purities=['LPLP']

signals = ["BulkGWW"]



for sig in signals:

  for p in purities:



    cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])

    card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)

    cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '



    #SIGNAL

    card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ","JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})

    card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1","JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})

    card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2","JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1},{'CMS_res_prunedj':1.0})

    card.addParametricYieldWithUncertainty("%s"%sig,0,"JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence',vtag_pt_dependence[p],0.019)

    card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)





    #QCD

    rootFile="save_new_shapes_pythia_LPLP_3D.root"

    card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['altshapeZ:CMS_VV_JJ_nonRes_altshapeZ_'+p,'PT:CMS_VV_JJ_nonRes_PT_'+p,'OPT:CMS_VV_JJ_nonRes_OPT_'+p,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+p],False,0)   # ,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+p,'PT:CMS_VV_JJ_nonRes_PT_'+p ,



    card.addFixedYieldFromFile("nonRes",1,"JJ_nonRes_LPLP.root","nonRes",1.0)



    #DATA

    card.importBinnedData("JJ_LPLP.root","data",["MJ1","MJ2","MJJ"])

    #SYSTEMATICS

    #luminosity

    card.addSystematic("CMS_lumi","lnN",{'%s'%sig:lumi_unc[dataset]})



    #PDF uncertainty for the signal

    card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})

    



    #background normalization

    card.addSystematic("CMS_VV_JJ_nonRes_norm_"+p,"lnN",{'nonRes':1.5})



    #tau21 

    card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:vtag_unc[p][dataset]})



    #pruned mass scale    

    card.addSystematic("CMS_scale_j","param",[0.0,0.02])

    card.addSystematic("CMS_res_j","param",[0.0,0.05])#0.05

    card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])

    card.addSystematic("CMS_res_prunedj","param",[0.0,0.03])#0.2



    #systematics for dijet part of V+jets background

    card.addSystematic("CMS_VV_JJ_nonRes_PT_"+p,"param",[0.0,0.333])

    card.addSystematic("CMS_VV_JJ_nonRes_OPT_"+p,"param",[0.0,0.333])

    card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+p,"param",[0.0,0.333])

    #card.addSystematic('CMS_VV_JJ_nonRes_altshape_'+p,"param",[0.0,0.333])  

    card.addSystematic('CMS_VV_JJ_nonRes_altshapeZ_'+p,"param",[0.0,0.333]) 

            

    card.makeCard()

    

  #make combined cards    

  combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")+'.txt'

  os.system('rm %s'%combo_card)

  cmd+=' >> %s'%combo_card 

  print cmd

  #os.system(cmd)

  

  #make workspace

  workspace = combo_card.replace('datacard','workspace').replace('.txt','.root')

  cmd2='text2workspace.py %s -o %s'%(combo_card,workspace)

  print cmd2
  os.system(cmd2)
