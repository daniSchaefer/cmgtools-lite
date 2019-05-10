# with this script: for test = 2016 fit 2017 CHS data with 2016 files
# for test = 2017 fit 2017 CHS data with 2016 files

import sys,os
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '


dataset='2017'#,'2017'
test = '2017'
if test=="2016":
    outlabel = "_17data16bkg"
else:
    outlabel = "_17data17bkg"

addTT = False

lumi = {'2016':35900,'2017':41367}
lumi_unc = {'2016':1.025,'2017':1.023}

scales = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}


vtag_unc = {'HPHP':{},'HPLP':{},'LPLP':{}}
vtag_unc['HPHP'] = {'2016':'1.232/0.792','2017':'1.269/0.763'}
vtag_unc['HPLP'] = {'2016':'0.882/1.12','2017':'0.866/1.136'}    
vtag_unc['LPLP'] = {'2016':'1.063','2017':'1.043'}

vtag_pt_dependence = {'HPHP':'((1+0.06*log(MH/2/300))*(1+0.06*log(MH/2/300)))','HPLP':'((1+0.06*log(MH/2/300))*(1+0.07*log(MH/2/300)))'}
  
purities= ['HPHP','HPLP']
signals = ["BulkGWW"]#,"BulkGZZ","ZprimeWW","WprimeWZ"]


for sig in signals:
  cmd ="combineCards.py"
  cmd_combo ="combineCards.py"
  for p in purities:

      ncontrib = 1
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      cardName='datacard_'+cat+outlabel+'.txt'
      workspaceName='workspace_'+cat+outlabel+'.root'
      
      
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat+outlabel)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'='+cardName
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'='+cardName
      

     
      card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",dataset+"/JJ_%s_CHS_MVV.json"%(sig),{'CMS_scale_j':1},{'CMS_res_j':1.0})
      card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1" ,dataset+"/JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2" ,dataset+"/JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addParametricYieldWithUncertainty("%s"%sig,0  ,dataset+"/JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence',vtag_pt_dependence[p],1.0)
      card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)

      #---------------------------------------------------------------------------------
      #Vjets
      sys.path.append(dataset)
      from JJ_WJets_HPLP_gauss import Wjets_TTbar_nonRes_l1, Wjets_TTbar_Res_l1, Wjets_TTbar_nonRes_l2, Wjets_TTbar_Res_l2
      from JJ_WJets_HPLP_gauss import Zjets_Res_l1, Zjets_Res_l2, Zjets_nonRes_l1, Zjets_nonRes_l2  
         
      # begin W+jets background :
      
      # W+jets 
      #rootFile = '2017/JJ_WJets_MVV_'+p+'.root' #jen
      rootFile = '2017/JJ_WJets_MVV_%s_new.root'%p
      card.addHistoShapeFromFile("Wjets_mjj_c1",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+p,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l1","MJ1","",Wjets_TTbar_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addGaussianShape("Wjets_mjetNonRes_l2","MJ2",Wjets_TTbar_nonRes_l2)
      card.product3D("Wjets_c1","Wjets_mjetRes_l1","Wjets_mjetNonRes_l2","Wjets_mjj_c1")
      
      # jets + W
      #rootFile = '2017/JJ_WJets_MVV_'+p+'.root' #jen
      rootFile = '2017/JJ_WJets_MVV_%s_new.root'%p
      card.addHistoShapeFromFile("Wjets_mjj_c2",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+p,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l2","MJ2","",Wjets_TTbar_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addGaussianShape("Wjets_mjetNonRes_l1","MJ1",Wjets_TTbar_nonRes_l1)
      card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj_c2")
      card.sumPdf('Wjets',"Wjets_c1","Wjets_c2","CMS_ratio_Wjets_"+p)
      card.addFixedYieldFromFile('Wjets',ncontrib,"2017/JJ_WJets_%s.root"%p,"WJets")
     
      ncontrib+=1
            
      # begin Z+jets background :
      
      # Z+jets 
      rootFile = '2017/JJ_ZJets_MVV_%s_new.root'%p
      card.addHistoShapeFromFile("Zjets_mjj_c1",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+p,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l1","MJ1","",Zjets_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addGaussianShape("Zjets_mjetNonRes_l2","MJ2",Zjets_nonRes_l2)
      card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj_c1")
      
      
      # jets + Z
      rootFile = '2017/JJ_ZJets_MVV_%s_new.root'%p
      card.addHistoShapeFromFile("Zjets_mjj_c2",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+p,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l2","MJ2","",Zjets_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addGaussianShape("Zjets_mjetNonRes_l1","MJ1",Zjets_nonRes_l1)
      card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj_c2")
      card.sumPdf('Zjets',"Zjets_c1","Zjets_c2","CMS_ratio_Zjets_"+p)
      
      card.addFixedYieldFromFile('Zjets',ncontrib,"2017/JJ_ZJets_%s.root"%p,"ZJets")
     

      ncontrib+=1
      
      
      
      #QCD
      if test == "2016":
        rootFile="2016/save_new_shapes_pythia_"+p+"_3D_new.root"
      else:
        rootFile="2017/save_new_shapes_pythia_"+p+"_3D_new.root"  
    
      card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+p,'OPT:CMS_VV_JJ_nonRes_OPT_'+p,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+p,'altshape:CMS_VV_JJ_nonRes_altshape_'+p,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+p],False,0) ,
     
      card.addFixedYieldFromFile("nonRes",ncontrib,dataset+"/JJ_nonRes_"+p+".root","nonRes",0.8)

      #DATA
      card.importBinnedData("2017/JJ_CHS_"+p+".root","data",["MJ1","MJ2","MJJ"]) 
            
      #SYSTEMATICS
      #luminosity
      card.addSystematic("CMS_lumi","lnN",{'%s'%sig:lumi_unc[dataset],"Wjets":lumi_unc[dataset],"Zjets":lumi_unc[dataset]})

      #PDF uncertainty for the signal
      card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})
    

      #background normalization
      card.addSystematic("CMS_VV_JJ_nonRes_norm","lnN",{'nonRes':1.5})
      card.addSystematic("CMS_VV_JJ_Wjets_norm","lnN",{'Wjets':1.2})
      card.addSystematic("CMS_VV_JJ_Zjets_norm","lnN",{'Zjets':1.2})
      
        
      #tau21 
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:vtag_unc[p][dataset],"Wjets":vtag_unc[p][dataset],"Zjets":vtag_unc[p][dataset]})
             
      #pruned mass scale  
      card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
      card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
      card.addSystematic("CMS_scale_j","param",[0.0,0.012])
      card.addSystematic("CMS_res_j","param",[0.0,0.08])
    
      #systematics for dijet part of V+jets background
      card.addSystematic("CMS_VV_JJ_Wjets_PTZ_"+p,"param",[0,0.1]) #0.333
      card.addSystematic("CMS_VV_JJ_Wjets_OPTZ_"+p,"param",[0,0.1]) #0.333
      card.addSystematic("CMS_VV_JJ_Zjets_PTZ_"+p,"param",[0,0.1]) #0.333
      card.addSystematic("CMS_VV_JJ_Zjets_OPTZ_"+p,"param",[0,0.1]) #0.333
      
    
      #alternative shapes for QCD background
      card.addSystematic("CMS_VV_JJ_nonRes_PT_"+p,"param",[0.0,0.333])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT_"+p,"param",[0.0,0.333])
      card.addSystematic('CMS_VV_JJ_nonRes_altshape2_'+p,"param",[0.0,0.333])  
      card.addSystematic('CMS_VV_JJ_nonRes_altshape_'+p,"param",[0.0,0.333])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+p,"param",[1.0,0.333])
        
      card.makeCard()
      
      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
  del card
  #make combined HPHP+HPLP card   
  combo_card =  cardName.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")
  combo_workspace =  workspaceName.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")
  os.system('rm %s'%combo_card)
  cmd_combo+=' >> %s'%combo_card
  print cmd_combo
  os.system(cmd_combo)
  t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
  print t2wcmd
  os.system(t2wcmd)
  
  
  
  




