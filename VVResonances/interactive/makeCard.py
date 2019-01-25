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
      
      from JJ_WJets_HPLP import Wjets_TTbar_nonRes_l1, Wjets_TTbar_Res_l1, Wjets_TTbar_nonRes_l2, Wjets_TTbar_Res_l2
      from JJ_WJets_HPLP import Zjets_Res_l1, Zjets_Res_l2, Zjets_nonRes_l1, Zjets_nonRes_l2
         
         
      # begin W+jets background :
      
      # W+jets 
      rootFile = '2017/JJ_WJets_MVV_'+p+'.root' #jen
      card.addHistoShapeFromFile("Wjets_mjj_c1",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+p,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l1","MJ1","",Wjets_TTbar_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      
      card.addGaussianShape("Wjets_mjetNonRes_l2","MJ2",Wjets_TTbar_nonRes_l2)
      
      card.product3D("Wjets_c1","Wjets_mjetRes_l1","Wjets_mjetNonRes_l2","Wjets_mjj_c1")
      
      #card.addYieldWithRateParameterFromFile('Wjets_c1',ncontrib,'Wjets_c1_%s_%s'%(p,dataset),"2017/JJ_WJets_%s.root"%p,"WJets",[],0.5)
      #ncontrib+=1
      
      # jets + W
      rootFile = '2017/JJ_WJets_MVV_'+p+'.root' #jen
      card.addHistoShapeFromFile("Wjets_mjj_c2",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Wjets_PTZ_'+p,'OPT:CMS_VV_JJ_Wjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Wjets_mjetRes_l2","MJ2","",Wjets_TTbar_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      
      card.addGaussianShape("Wjets_mjetNonRes_l1","MJ1",Wjets_TTbar_nonRes_l1)
      
      card.product3D("Wjets_c2","Wjets_mjetRes_l2","Wjets_mjetNonRes_l1","Wjets_mjj_c2")
      
      card.sumPdf('Wjets',"Wjets_c1","Wjets_c2","CMS_ratio_Wjets_"+p+"_"+dataset)

      card.addYieldWithRateParameterFromFile('Wjets',ncontrib,'Wjets_%s_%s'%(p,dataset),"2017/JJ_WJets_%s.root"%p,"WJets")
     
      ncontrib+=1
            
      # begin Z+jets background :
      
      # Z+jets 
      rootFile = '2017/JJ_ZJets_MVV_'+p+'.root' #jen
      card.addHistoShapeFromFile("Zjets_mjj_c1",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+p,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+p],False,0)
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l1","MJ1","",Zjets_Res_l1,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      
      card.addGaussianShape("Zjets_mjetNonRes_l2","MJ2",Zjets_nonRes_l2)
      
      card.product3D("Zjets_c1","Zjets_mjetRes_l1","Zjets_mjetNonRes_l2","Zjets_mjj_c1")
      
      
      # jets + Z
      rootFile = '2017/JJ_ZJets_MVV_'+p+'.root' #jen
      print "add mjj "
      card.addHistoShapeFromFile("Zjets_mjj_c2",["MJJ"],rootFile,"histo_nominal",['PT:CMS_VV_JJ_Zjets_PTZ_'+p,'OPT:CMS_VV_JJ_Zjets_OPTZ_'+p],False,0)
      print "add res shape "
      card.addMJJSignalShapeNOEXP("Zjets_mjetRes_l2","MJ2","",Zjets_Res_l2,{'CMS_scale_prunedj':1.},{'CMS_res_prunedj':1.},scales[dataset])
      print "add non res shape"
      card.addGaussianShape("Zjets_mjetNonRes_l1","MJ1",Zjets_nonRes_l1)
      print "make 3d product "
      card.product3D("Zjets_c2","Zjets_mjetRes_l2","Zjets_mjetNonRes_l1","Zjets_mjj_c2")
      print " sum pdf "
      card.sumPdf('Zjets',"Zjets_c1","Zjets_c2","CMS_ratio_Zjets_"+p+"_"+dataset)
      print " zjets ready"
      #card.addYieldWithRateParameterFromFile('Zjet',ncontrib,'Zjets_%s_%s'%(p,dataset),"2017/JJ_ZJets_%s.root"%p,"ZJets")
      card.addYieldWithRateParameter('Zjets',ncontrib,'Zjets_%s_%s'%(p,dataset),"@0*@1",['Wjets_%s_%s'%(p,dataset),"CMS_VV_JJ_Vjets_ratio"])
      ncontrib+=1
      
      
      
      #QCD
      
      rootFile=dataset+"/save_new_shapes_pythia_"+p+"_3D.root"
    
      card.addHistoShapeFromFile("nonRes",["MJ1","MJ2","MJJ"],rootFile,"histo",['PT:CMS_VV_JJ_nonRes_PT_'+p,'OPT:CMS_VV_JJ_nonRes_OPT_'+p,'OPT3:CMS_VV_JJ_nonRes_OPT3_'+p,'altshape:CMS_VV_JJ_nonRes_altshape_'+p,'altshape2:CMS_VV_JJ_nonRes_altshape2_'+p],False,0)
      
      # card.addFixedYieldFromFile("nonRes",2,"/afs/cern.ch/user/j/jngadiub/public/"+dataset+"/JJ_nonRes_"+p+".root","nonRes",1.0)
      card.addFixedYieldFromFile("nonRes",ncontrib,dataset+"/JJ_nonRes_"+p+".root","nonRes",0.8)

      #DATA
      card.importBinnedData(dataset+"/JJ_"+p+".root","data",["MJ1","MJ2","MJJ"])
      #pseudodata = "herwig"
      #card.importBinnedData("JJ_"+pseudodata+"_"+p+"_"+dataset+".root","data_obs",["MJ1","MJ2","MJJ"])
      #SYSTEMATICS
      #luminosity
      card.addSystematic("CMS_lumi","lnN",{'%s'%sig:lumi_unc[dataset],"Wjets":lumi_unc[dataset],"Zjets":lumi_unc[dataset]})

      #PDF uncertainty for the signal
      card.addSystematic("CMS_pdf","lnN",{'%s'%sig:1.01})
    

      #background normalization
      card.addSystematic("CMS_VV_JJ_nonRes_norm","lnN",{'nonRes':1.2})
      #card.addSystematic("CMS_VV_JJ_Wjets_c1_norm","lnN",{'Wjets_c1':1.2})
      #card.addSystematic("CMS_VV_JJ_Wjets_c2_norm","lnN",{'Wjets_c2':1.2})
      card.addSystematic("CMS_VV_JJ_Wjets_norm","lnN",{'Wjets':1.2})#,'Wjets_c2':1.2})
      
      card.addSystematic("CMS_VV_JJ_Vjets_ratio","param",[0.4,0.1])#0.01
      
      card.addSystematic("CMS_ratio_Wjets_"+p+"_"+dataset,"param",[0.5,0.11])
      card.addSystematic("CMS_ratio_Zjets_"+p+"_"+dataset,"param",[0.5,0.11])
      
     ##card.addSystematic("CMS_VV_JJ_Zjets_norm","lnN",{'Zjet':1.5})
        
      #tau21 
      card.addSystematic("CMS_VV_JJ_tau21_eff","lnN",{'%s'%sig:vtag_unc[p][dataset],"Wjets":vtag_unc[p][dataset],"Zjets":vtag_unc[p][dataset]})#,"Zjet":vtag_unc[p][dataset]})
             
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
  
  
  
  
  #CMS_VV_JJ_Vjets_ratio    4.9916e-01 +/-  9.89e-03
  #CMS_VV_JJ_Wjets_OPTZ_HPHP   -3.6366e-03 +/-  9.89e-02
  #CMS_VV_JJ_Wjets_OPTZ_HPLP    1.0268e-01 +/-  9.65e-02
  #CMS_VV_JJ_Wjets_PTZ_HPHP    3.2513e-03 +/-  9.90e-02
  #CMS_VV_JJ_Wjets_PTZ_HPLP   -8.9659e-02 +/-  9.69e-02
  #CMS_VV_JJ_Wjets_norm    7.4850e-01 +/-  8.39e-01
  #CMS_VV_JJ_Zjets_OPTZ_HPHP   -2.8293e-03 +/-  9.90e-02
  #CMS_VV_JJ_Zjets_OPTZ_HPLP    4.2117e-02 +/-  9.83e-02
  #CMS_VV_JJ_Zjets_PTZ_HPHP    2.2163e-03 +/-  9.90e-02
  #CMS_VV_JJ_Zjets_PTZ_HPLP   -3.6144e-02 +/-  9.83e-02
  #CMS_VV_JJ_nonRes_OPT3_HPHP    1.0330e+00 +/-  3.27e-01
  #CMS_VV_JJ_nonRes_OPT3_HPLP    1.1032e+00 +/-  1.71e-01
  #CMS_VV_JJ_nonRes_OPT_HPHP    3.9789e-02 +/-  2.35e-01
  #CMS_VV_JJ_nonRes_OPT_HPLP    1.2059e-01 +/-  1.06e-01
  #CMS_VV_JJ_nonRes_PT_HPHP   -5.0705e-01 +/-  2.54e-01
  #CMS_VV_JJ_nonRes_PT_HPLP    1.0153e-01 +/-  1.10e-01
  #CMS_VV_JJ_nonRes_altshape2_HPHP    2.1300e-02 +/-  2.11e-01
  #CMS_VV_JJ_nonRes_altshape2_HPLP    3.1251e-01 +/-  6.04e-02
  #CMS_VV_JJ_nonRes_altshape_HPHP    3.6052e-03 +/-  2.01e-01
  #CMS_VV_JJ_nonRes_altshape_HPLP    3.2049e-01 +/-  7.09e-02
  #CMS_VV_JJ_nonRes_norm   -3.2183e-01 +/-  4.70e-02
   #CMS_VV_JJ_tau21_eff   -4.6653e-02 +/-  9.98e-01
              #CMS_lumi   -4.2646e-03 +/-  9.97e-01
               #CMS_pdf   -7.2035e-05 +/-  9.97e-01
  #CMS_ratio_Wjets_HPHP    4.8704e-01 +/-  8.55e-02
  #CMS_ratio_Wjets_HPLP    5.6800e-01 +/-  3.62e-02
  #CMS_ratio_Zjets_HPHP    4.9990e-01 +/-  9.86e-02
  #CMS_ratio_Zjets_HPLP    5.7611e-01 +/-  8.31e-02
             #CMS_res_j   -2.0002e-03 +/-  7.93e-02
       #CMS_res_prunedj   -9.1631e-02 +/-  5.48e-02
           #CMS_scale_j   -5.2695e-04 +/-  1.17e-02
     #CMS_scale_prunedj   -3.0111e-02 +/-  7.88e-03
  #CMS_tau21_PtDependence    1.4623e-06 +/-  1.88e-02
        #Wjets_HPHP_2016    2.5470e+01 +/-  9.96e+00
        #Wjets_HPHP_2017    7.1363e+01 +/-  1.56e+01
        #Wjets_HPLP_2016    1.3465e+03 +/-  2.15e+02
        #Wjets_HPLP_2017    2.6115e+03 +/-  3.55e+02
                     #r    1.2720e-01 +/-  2.96e-01

  
# combined 2016: 
   #-- Profile Likelihood -- 
#Limit: r < 1.49125 @ 95% CL
  
# HPLP 2016  
 #-- Profile Likelihood -- 
#Limit: r < 1.28459 @ 95% CL  
  
  
# HPHP 2016
 #-- Profile Likelihood -- 
#Limit: r < 4.0461 @ 95% CL





