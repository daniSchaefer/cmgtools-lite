import ROOT
import os,sys

cuts={}


cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.)'

cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
cuts['LP'] = '(jj_l1_tau2/jj_l1_tau1>0.35&&jj_l1_tau2/jj_l1_tau1<0.75)'

cuts['nonres'] = '1'

purities=['HP','LP']
purities=['HP']

qWTemplate="QstarQW"
qZTemplate="QstarQZ"

VJetTemplate="JetsToQQ"
BRqW=1.

dataTemplate="JetHT"
nonResTemplate="QCD_Pt_1000to1400"
nonResTemplate="QCD_random"




minMJJ=30.0
maxMJJ=610.0

minMVV=1000.0
maxMVV=6000.0

binsMJJ=290
binsMVV=160

cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)                
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'
cuts['acceptanceMJJ']= "(jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ) 
cuts['acceptanceGENMJJ']= '(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)'


def makeAllNonRes(name,filename,template,addCut=""):
    for p in purities:
        print "=========== PURITY: ", p
        cut='*'.join([cuts['common'],cuts[p],'(jj_l1_gen_softDrop_mass>0&&jj_gen_partialMass>0)',addCut])
        resFile=filename+"_"+name+"_"+p		 
        cmd='speedupMake2DNonResTemplates.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  --binarray "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000" -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ}  samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ,maxMJJ=maxMJJ,minMJJ=minMJJ,tag=name)
        os.system(cmd)


def makeBackgroundShapesMVVConditional(name,filename,template,addCut=""):
	
 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  resFile=filename+"_"+name+"_detectorResponse_"+p+".root"	
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGEN']])
  rootFile=filename+"_"+name+"_test2D_"+p+".root"		 
  cmd='vvMake2DTemplatesTest.py -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_gen_partialMass,jj_l1_gen_softDrop_mass"  -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ}  -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
  os.system(cmd)
  
  
  
  
  
#makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,cuts['nonres'])
makeAllNonRes("nonRes","JJ",nonResTemplate,cuts['nonres'])






