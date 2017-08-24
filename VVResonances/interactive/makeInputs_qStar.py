import ROOT
import os,sys

cuts={}

<<<<<<< HEAD
cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0)'
#cuts['common'] = '((HLT_JJ)*(run>500) + (run<500)*(njj>0&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0))'
=======
cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter)'
>>>>>>> 681ab9cbf493726898c8ae04a52f21a8505ef435

cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.35)'
cuts['LP'] = '(jj_l1_tau2/jj_l1_tau1>0.35 && jj_l1_tau2/jj_l1_tau1<0.75)'

cuts['nonres'] = '1'

purities=['HP','LP']

qWTemplate="QstarQW"
qZTemplate="QstarQZ"
BRqW=1.

dataTemplate="JetHT"
nonResTemplate="QCD_HT"

minMJJ=30.0
maxMJJ=210.0

minMVV=1000.0
maxMVV=5000.0

binsMJJ=90
binsMVV=160

cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
cuts['acceptanceGEN']= "(jj_l1_gen_softDrop_mass>{minMJJ}&&jj_l1_gen_softDrop_mass<{maxMJJ}&&jj_gen_partialMass>{minMVV}&&jj_gen_partialMass<{maxMVV})".format(minMJJ=25,maxMJJ=300,minMVV=700,maxMVV=10000)                

cuts['acceptanceMJJ']= "(jj_l1_softDrop_mass>{minMJJ}&&jj_l1_softDrop_mass<{maxMJJ}) ".format(minMJJ=minMJJ,maxMJJ=maxMJJ) 
cuts['acceptanceGENMJJ']= "(jj_l1_gen_softDrop_mass>{minMJJ}&&jj_l1_gen_softDrop_mass<{maxMJJ}&&jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV})".format(minMJJ=minMJJ-5,maxMJJ=maxMJJ+5,minMVV=minMVV,maxMVV=maxMVV)

cuts['acceptanceGENMVV']= "(jj_gen_partialMass>{minMVV}&&jj_gen_partialMass<{maxMVV})".format(minMVV=700,maxMVV=5000)




def makeSignalShapesMVV(filename,template):

 cut='*'.join([cuts['common'],cuts['acceptanceMJJ']])
 #cut=cuts['acceptanceMJJ']
 rootFile=filename+"_MVV.root"
 cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_LV_mass"  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
 os.system(cmd)
 jsonFile=filename+"_MVV.json"
 print 'Making JSON'
 cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol1,ALPHA:pol2,N:pol2,SCALESIGMA:pol2,f:pol2" -m 1000 -M 6000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
 os.system(cmd)


def makeSignalShapesMJJ(filename,template):

 for p in purities:
  cut='*'.join([cuts['common'],cuts[p]])
  rootFile=filename+"_MJJ_"+p+".root"
  doExp=1
  if p=='HP' or p=='NP':
      doExp=0
  cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_l1_softDrop_mass" -m {minMJJ} -M {maxMJJ} -e {doExp} -f "alpha:1.347" samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ,doExp=doExp)
  os.system(cmd)
  jsonFile=filename+"_MJJ_"+p+".json"

  if p=='HP' or p=='NP':
      cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
  else:
      cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol3,sigma:pol1,alpha:pol0,n:pol0,slope:pol1,f:laur4,alpha2:pol0,n2:pol0" -m 601 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)

  os.system(cmd)

def makeSignalYields(filename,template,branchingFraction,sfP = {'HP':1.0,'LP':1.0}):
 	 
 for p in purities:
  cut = "*".join([cuts[p],cuts['common'],cuts['acceptance'],str(sfP[p])])
  #Signal yields
  yieldFile=filename+"_"+p+"_yield"
  cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "jj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol5" -b {BR} -x 950 samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
  os.system(cmd)

def makeDetectorResponse(name,filename,template,addCut="1"):

 #first parameterize detector response
 cut='*'.join([cuts['common'],'jj_l1_gen_softDrop_mass>10&&jj_gen_partialMass>0',addCut])
 resFile=filename+"_"+name+"_detectorResponse.root"	       
 cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b "150,200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name)
 os.system(cmd)
 
def makeBackgroundShapesMJJ(name,filename,template,addCut="1"):
 
 resFile=filename+"_"+name+"_detectorResponse.root"
 
 for p in purities:

  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGENMJJ']])
  rootFile=filename+"_"+name+"_MJJ_"+p+".root"  	      
  cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_l1_gen_softDrop_mass" -b {binsMJJ}  -x {minMJJ} -X {maxMJJ} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
  os.system(cmd)

def makeBackgroundShapesMVVConditional(name,filename,template,addCut=""):

 resFile=filename+"_"+name+"_detectorResponse.root"
 
 for p in purities:

  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptanceGEN']])
  rootFile=filename+"_"+name+"_COND2D_"+p+".root"		 
  cmd='vvMake2DTemplateWithKernels.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_gen_partialMass,jj_l1_gen_softDrop_mass"  -b {binsMVV} -B {binsMJJ} -x {minMVV} -X {maxMVV} -y {minMJJ} -Y {maxMJJ}  -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ)
  os.system(cmd)



									
makeSignalShapesMVV("JJ_XqW",qWTemplate)
#makeSignalShapesMJJ("JJ_XqW",qWTemplate)
#makeSignalYields("JJ_XqW",qWTemplate,BRqW,{'HP':1.03,'LP':0.95})

#makeSignalShapesMVV("JJ_XqZ",qZTemplate)
#makeSignalShapesMJJ("JJ_XqZ",qZTemplate)
#makeSignalYields("JJ_XqZ",qZTemplate,BRqW,{'HP':1.03,'LP':0.95})

#makeDetectorResponse("nonRes","JJ",nonResTemplate,cuts['nonres'])
#makeBackgroundShapesMJJ("nonRes","JJ",nonResTemplate,cuts['nonres'])
#makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,cuts['nonres'])
