import sys,os
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '


datasets=['2016','2017']

addTT = False

lumi = {'2016':35900,'2017':41367}
lumi_unc = {'2016':1.025,'2017':1.023}

scales = {"2017" :[0.983,1.08], "2016":[1.014,1.086]}
#scales = {"2017" :[1.,1.], "2016":[1.,1.]}
  
vtag_unc = {'HPHP':{},'HPLP':{},'LPLP':{}}
#old
#vtag_unc['HPHP'] = {'2016':'1.078/0.922','2017':'1.066/0.934'}
#vtag_unc['HPLP'] = {'2016':'0.926/1.074','2017':'0.933/1.067'}
#new
vtag_unc['HPHP'] = {'2016':'1.094/0.910','2017':'1.082/0.922'}
vtag_unc['HPLP'] = {'2016':'0.939/1.063','2017':'0.957/1.043'}    
vtag_unc['LPLP'] = {'2016':'1.063','2017':'1.043'}

vtag_pt_dependence = {'HPHP':'0.085*log(MH/400)*0.085*log(MH/400)','HPLP':'0.085*log(MH/400)*0.039*log(MH/400)','LPLP':'0.039*log(MH/400)*0.039*log(MH/400)'}
  
purities= ['HPHP','HPLP']
signals = ["BulkGWW"]


for sig in signals:
  cmd ="combineCards.py"
  for dataset in datasets:
    cmd_combo="combineCards.py"
    for p in purities:

      ncontrib = 1
      
      cat='_'.join(['JJ',sig,p,'13TeV_'+dataset])
      card=DataCardMaker('',p,'13TeV_'+dataset,lumi[dataset],'JJ',cat)
      cmd=cmd+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cmd_combo=cmd_combo+" "+cat.replace('_%s'%sig,'')+'=datacard_'+cat+'.txt '
      cardName='datacard_'+cat+'.txt'
      workspaceName='workspace_'+cat+'.root'

      
      #SIGNAL
      card.addMVVSignalParametricShape("%s_MVV"%sig,"MJJ",dataset+"/JJ_%s_MVV.json"%sig,{'CMS_scale_j':1},{'CMS_res_j':1.0})
      card.addMJJSignalParametricShapeNOEXP("Wqq1","MJ1" ,dataset+"/JJ_%s_MJl1_"%sig+p+".json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addMJJSignalParametricShapeNOEXP("Wqq2","MJ2" ,dataset+"/JJ_%s_MJl2_"%sig+p+".json",{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addParametricYieldWithUncertainty("%s"%sig,0  ,dataset+"/JJ_%s_"%sig+p+"_yield.json",1,'CMS_tau21_PtDependence',vtag_pt_dependence[p],0.019)
      card.product3D("%s"%sig,"Wqq1","Wqq2","%s_MVV"%sig)

      #---------------------------------------------------------------------------------
      #Vjets
      sys.path.append(dataset)
      
      from JJ_WJets_HPLP import Wjets_TTbar_nonRes_l1, Wjets_TTbar_Res_l1, Wjets_TTbar_nonRes_l2, Wjets_TTbar_Res_l2, ratio_Res_nonRes_l1, ratio_Res_nonRes_l2
      from JJ_WJets_HPLP import Zjets_Res_l1, Zjets_Res_l2, Zjets_nonRes_l1, Zjets_nonRes_l2
         
         
      
      rootFile = '2017/JJ_WJets_MVV_'+p+'.root' #jen
      card.addHistoShapeFromFile("Wjets_mjj",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+p,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l1","MJ1","",Wjets_TTbar_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l2","MJ2","",Wjets_TTbar_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset]) 
      
      card.addGaussianShape("Wjets_mjetNonRes_l1","MJ1",Wjets_TTbar_nonRes_l1)
      card.addGaussianShape("Wjets_mjetNonRes_l2","MJ2",Wjets_TTbar_nonRes_l2)
      
      print  "ratio "+str(ratio_Res_nonRes_l2["ratio"] ) 
      
      print "Wjets  l1 "
      card.sumPdf("Wjets_mjet_l1","Wjets_mjetRes_l1","Wjets_mjetNonRes_l1","CMS_ratio_Wjets_"+p,"("+ratio_Res_nonRes_l1["ratio"]+")")
      print "Wjets  l2 "
      card.sumPdf("Wjets_mjet_l2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l2","CMS_ratio_Wjets_"+p,"("+ratio_Res_nonRes_l2["ratio"]+")")
      
      card.product3D("Wjet","Wjets_mjet_l1","Wjets_mjet_l2","Wjets_mjj")
      card.addYieldWithRateParameterFromFile('Wjet',ncontrib,'Wjet_%s_%s'%(p,dataset),"2017/JJ_WJets_%s.root"%p,"WJets")
      ncontrib+=1
            
      rootFile = '2017/JJ_ZJets_MVV_'+p+'.root' #jen
      card.addHistoShapeFromFile("Zjets_mjj",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+p,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l1","MJ1","",Zjets_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l2","MJ2","",Zjets_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      card.addGaussianShape("Zjets_mjetNonRes_l1","MJ1",Zjets_nonRes_l1)
      card.addGaussianShape("Zjets_mjetNonRes_l2","MJ2",Zjets_nonRes_l2)
      
      print "Zjets pdf l1 "
      card.sumPdf("Zjets_mjet_l1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l1","CMS_ratio_Zjets_"+p,"("+ratio_Res_nonRes_l1["ratio_Z"]+")")
      print "Zjets MJ2"
      card.sumPdf("Zjets_mjet_l2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l2","CMS_ratio_Zjets_"+p,"("+ratio_Res_nonRes_l2["ratio_Z"]+")")
     
      card.product3D("Zjet","Zjets_mjet_l1","Zjets_mjet_l2","Zjets_mjj")
      ##card.addFixedYieldFromFile("Zjet",ncontrib,"2017/JJ_ZJets_%s.root"%p,"ZJets",1.0)
      card.addYieldWithRateParameter('Zjet',ncontrib,'Zjet_%s_%s'%(p,dataset),"@0*@1",['Wjet_%s_%s'%(p,dataset),"CMS_VV_JJ_Vjets_ratio"])
      #ncontrib+=1
      
      
      
      #QCD
      if dataset.find("2016")!=-1:
        rootFile=dataset+"/save_new_shapes_pythia_"+p+"_3D.root"
      else:
        rootFile=dataset+"/SaveNewShapes_nonRes_3D_"+p+".root"
      card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+p,'OPT:CMS_VV_JJ_nonRes_OPT_'+p,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+p,'altshape:CMS_VV_JJ_nonRes_altshape_'+p,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+p],False,0)
      
      # card.addFixedYieldFromFile("nonRes",2,"/afs/cern.ch/user/j/jngadiub/public/"+dataset+"/JJ_nonRes_"+p+".root","nonRes",1.0)
      card.addFixedYieldFromFile("nonRes",ncontrib,dataset+"/JJ_nonRes_"+p+".root","nonRes",0.8)

      #DATA
      #card.importBinnedData(dataset+"/JJ_"+p+".root","data",["MJ1","MJ2","MJJ"]) JJ_herwig_HPLP_2016.root
      pseudodata = "herwig"
      card.importBinnedData("JJ_"+pseudodata+"_"+p+"_"+dataset+".root","data_obs",["MJ1","MJ2","MJJ"])
      #SYSTEMATICS
      #luminosity
      card.addSystematic("CMS_lumi","lnN",{'%s'%sig:lumi_unc[dataset],"Wjet":lumi_unc[dataset],"Zjet":lumi_unc[dataset]})

      #PDF uncertainty for the signal
      card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})
    

      #background normalization
      card.addSystematic("CMS_VV_JJ_nonRes_norm","lnN",{'nonRes':1.2})
      card.addSystematic("CMS_VV_JJ_Wjets_norm","lnN",{'Wjet':1.2})
      card.addSystematic("CMS_VV_JJ_Vjets_ratio","param",[0.5,0.01])
      
      card.addSystematic("CMS_ratio_Wjets_"+p,"param",[0.5,0.1])
      card.addSystematic("CMS_ratio_Zjets_"+p,"param",[0.5,0.1])
     # card.addSystematic("CMS_VV_JJ_Zjets_norm","lnN",{'Zjet':1.5})
        
      #tau21 
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:vtag_unc[p][dataset],"Wjet":vtag_unc[p][dataset],"Zjet":vtag_unc[p][dataset]})
             
      #pruned mass scale  
      card.addSystematic("CMS_scale_prunedj","param",[0.0,0.02])
      card.addSystematic("CMS_res_prunedj","param",[0.0,0.08])
      card.addSystematic("CMS_scale_j","param",[0.0,0.012])
      card.addSystematic("CMS_res_j","param",[0.0,0.08])
    
      #systematics for dijet part of V+jets background
      card.addSystematic("CMS_VV_JJ_Wjets_PTZ_"+p,"param",[0,0.666]) #0.333
      card.addSystematic("CMS_VV_JJ_Wjets_OPTZ_"+p,"param",[0,0.666]) #0.333
      card.addSystematic("CMS_VV_JJ_Zjets_PTZ_"+p,"param",[0,0.333]) #0.333
      card.addSystematic("CMS_VV_JJ_Zjets_OPTZ_"+p,"param",[0,0.333]) #0.333
      
    
      #alternative shapes for QCD background
      card.addSystematic("CMS_VV_JJ_nonRes_PT_"+p,"param",[0.0,0.333])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT_"+p,"param",[0.0,0.333])
      card.addSystematic('CMS_VV_JJ_nonRes_altshape_'+p,"param",[0.0,0.333])  
      card.addSystematic('CMS_VV_JJ_nonRes_altshape2_'+p,"param",[0.0,0.333])
      card.addSystematic("CMS_VV_JJ_nonRes_OPT3_"+p,"param",[1.0,0.333])
        
      card.makeCard()
      
      t2wcmd = "text2workspace.py %s -o %s"%(cardName,workspaceName)
      print t2wcmd
      os.system(t2wcmd)
    del card
    #make combined HPHP+HPLP card   
    combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")+'.txt'
    combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","")+'.root'
    os.system('rm %s'%combo_card)
    cmd_combo+=' >> %s'%combo_card
    print cmd_combo
    os.system(cmd_combo)
    t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
    print t2wcmd
    os.system(t2wcmd)
  
  #make combine 2016+2017 card
  combo_card = 'datacard_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.txt'
  combo_workspace = 'workspace_'+cat.replace("_HPHP","").replace("_HPLP","").replace("_LPLP","").replace('_2016','').replace('_2017','')+'.root'
  os.system('rm %s'%combo_card)
  cmd+=' >> %s'%combo_card
  print cmd

  
  #cmd = 'combineCards.py  JJ_HPHP_13TeV_2016=datacard_JJ_BulkGWW_HPHP_13TeV_2016.txt JJ_HPLP_13TeV_2016=datacard_JJ_BulkGWW_HPLP_13TeV_2016.txt JJ_HPHP_13TeV_2017=datacard_JJ_BulkGWW_HPHP_13TeV_2017.txt  JJ_HPLP_13TeV_2017=datacard_JJ_BulkGWW_HPLP_13TeV_2017.txt  >> datacard_JJ_BulkGWW_13TeV.txt   && text2workspace.py datacard_JJ_BulkGWW_13TeV.txt -o workspace_combo_BulkGWW.root'
  #os.system(cmd)
  
  os.system(cmd)
  t2wcmd = "text2workspace.py %s -o %s"%(combo_card,combo_workspace)
  print t2wcmd
  os.system(t2wcmd)
  
  
  
  
  
  
  
  
  
  
  

