import ROOT
import os,sys

period = 2017 #2016

submitToBatch = True #Set to true if you want to submit kernels + makeData to batch!
runParallel   = True #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done! TODO! Add waitForBatchJobs also here?
dijetBinning = True
useTriggerWeights = True


HPSF = 0.995
LPSF = 1.005
if period == 2017:
    HPSF = 0.948
    LPSF = 1.057
    

addOption = ""
if useTriggerWeights: 
    addOption = "-t"
    
if dijetBinning:
    if useTriggerWeights: 
        HCALbinsMVV=" --binsMVV 838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5000"
    else:
        HCALbinsMVV=" --binsMVV 1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5000"
        # HCALbinsMVV=" --binsMVV 1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5000"
    HCALbinsMVVSignal=" --binsMVV 1,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808"
    HCALbinsMVVSignal = HCALbinsMVV
else:
    HCALbinsMVV=""
    HCALbinsMVVSignal=""
 	
cat={}
# For standard tau 21, use this
# cat['HP1'] = 'jj_l1_tau2/jj_l1_tau1<0.35'
# cat['HP2'] = 'jj_l2_tau2/jj_l2_tau1<0.35'
# cat['LP1'] = 'jj_l1_tau2/jj_l1_tau1>0.35&&jj_l1_tau2/jj_l1_tau1<0.75'
# cat['LP2'] = 'jj_l2_tau2/jj_l2_tau1>0.35&&jj_l2_tau2/jj_l2_tau1<0.75'
# cat['NP1'] = 'jj_l1_tau2/jj_l1_tau1>0.75'
# cat['NP2'] = 'jj_l2_tau2/jj_l2_tau1>0.75'

# For standard DDT tau 21, use this
# cat['HP1'] = 'jj_l1_tau21_DDT<0.47'
# cat['HP2'] = 'jj_l2_tau21_DDT<0.47'
# cat['LP1'] = 'jj_l1_tau21_DDT>0.47&&jj_l1_tau21_DDT<0.88'
# cat['LP2'] = 'jj_l2_tau21_DDT>0.47&&jj_l2_tau21_DDT<0.88'
# cat['NP1'] = 'jj_l1_tau21_DDT>0.88'
# cat['NP2'] = 'jj_l2_tau21_DDT>0.88'

# For retuned DDT tau 21, use this
cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98'
cat['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.98'
cat['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.98'

cuts={}

if period == 2017:
    lumi = 41367.
    cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'
    cuts['metfilters'] = "(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)"
else:
    lumi = 35900.
    cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'
    cuts['metfilters'] =("Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter")
    
cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
cuts['NP'] = '(('+cat['LP1']+'&&'+cat['NP2']+')||('+cat['NP1']+'&&'+cat['LP2']+')||('+cat['NP1']+'&&'+cat['NP2']+'))'

cuts['nonres'] = '1'
cuts['res'] = '(jj_l1_mergedVTruth==1&&jj_l1_softDrop_mass>60&&jj_l1_softDrop_mass<110)'

purities=['HPHP','HPLP','LPLP','NP']
purities=['HPHP','HPLP']

BulkGravWWTemplate="BulkGravToWW_narrow"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_narrow"
WprimeTemplate= "WprimeToWZ"
ZprimeWWTemplate= "ZprimeWW"
# use arbitrary cross section 0.001 so limits converge better
BRWW=1.*0.001
BRZZ=1.*0.001*0.6991*0.6991
BRWZ=1.*0.001*0.6991*0.676

dataTemplate="JetHT"
nonResTemplate="QCD_Pt_" #high stat
# nonResTemplate="QCD_Pt-" #low stat --> use this for tests
#nonResTemplate="Dijet" #to compare shapes

resTemplate= "JetsToQQ"
    
minMJ=55.0
maxMJ=215.0

binsMJ=80
binsMVV=100

if useTriggerWeights:
    minMVV=838.0
    maxMVV=5000.0
    minMX=1000.0
    maxMX=7000.0
    if dijetBinning:
        binsMVV = 39
        
else:
    minMVV=1000.0
    maxMVV=5000.0
    minMX=1200.0
    maxMX=7000.0
    if dijetBinning:
        binsMVV = 36
    



cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>20&&jj_l2_gen_softDrop_mass>20&&jj_l1_gen_softDrop_mass<300&&jj_l2_gen_softDrop_mass<300&&jj_gen_partialMass>400)'

cuts['acceptanceMJ']= "(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ) 

cuts['looseacceptanceMJ']= "(jj_l1_softDrop_mass>35&&jj_l1_softDrop_mass<300&&jj_l2_softDrop_mass>35&&jj_l2_softDrop_mass<300)"
cuts['acceptanceMVV'] = "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)

def makeSignalShapesMVV(filename,template):
 cut='*'.join([cuts['common'],cuts['metfilters'],cuts['acceptanceMJ']])
 rootFile=filename+"_MVV.root"
 fixPars = "N:129.6"
 if template.find("Wprime")!=-1:
     fixPars = "N:4.13,ALPHA:1.194"
 if template.find("Zprime")!=-1 or template.find("BulkGrav")!=-1:
     fixPars = "N:6.65"
 cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_LV_mass" {BinningMVV} --fix "{fixPars}"   -m {minMVV} -M {maxMVV} --minMX {minMX} --maxMX {maxMX} {addOption} samples '.format(template=template,cut=cut,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV,minMX=minMX,maxMX=maxMX,BinningMVV=HCALbinsMVVSignal,fixPars=fixPars,addOption=addOption)
 os.system(cmd)
 jsonFile=filename+"_MVV.json"
 print 'Making JSON'
 cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol2,ALPHA:pol3,N:pol0,SCALESIGMA:pol2,f:pol3" -m {minMVV} -M {maxMVV}  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV)
 os.system(cmd)

def makeSignalShapesMJ(filename,template,leg):
    #default is for BulkGravToWW samples
 for p in purities:
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p]])
  rootFile=filename+"_MJ"+leg+"_"+p+".root"
  jsonFile=filename+"_MJ"+leg+"_"+p+".json"
  doExp=0
  fixPars="alpha:1.08,n:2,n2:2"
  if p=='HPHP':
      if template.find("Wprime")!=-1:
          fixPars="alpha:1.505,n:2,n2:2"
      if template.find("Zprime")!=-1:
          fixPars="n:2.85,alpha:1.083"    
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "{fixPars}" --minMX {minMX} --maxMX {maxMX} {addOption} samples '.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX,fixPars=fixPars,addOption=addOption)
      cmdjson='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol3,alpha:pol0,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol3" -m 1000 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
  else:
      # doExp=1
      fixPars="alpha:1.125,n:2,n2:2"
      if template.find("Wprime")!=-1:
          fixPars="n:2,n2:2"
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "{fixPars}" --minMX {minMX} --maxMX {maxMX} {addOption} samples '.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX,fixPars=fixPars,addOption=addOption)
      cmdjson='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol0" -m 1000 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
  os.system(cmd)
  os.system(cmdjson)

def makeSignalYields(filename,template,branchingFraction,sfP = {'HPHP':1.0,'HPLP':1.0,'LPLP':1.0}):
 print "using the following scalfactors:" ,sfP
 for p in purities:
  cut = "*".join([cuts[p],cuts['common'],cuts['metfilters'],cuts['acceptance'],str(sfP[p])])
  #Signal yields
  yieldFile=filename+"_"+p+"_yield"
  fnc = "pol2"
  if p == "HPHP": fnc = "pol2"
  if p == "HPLP": fnc = "pol2"
  cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "jj_LV_mass" -m {minMVV} -M {maxMVV} -f {fnc} -b {BR} --minMX {minMX} --maxMX {maxMX} {addOption} samples '.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,fnc=fnc,BR=branchingFraction,minMX=minMX,maxMX=maxMX,addOption=addOption)
  os.system(cmd)

def fitVJets(filename,template):
  for p in purities:
    cut='*'.join([cuts['common'],cuts[p],cuts['acceptance']])
    rootFile=filename+"_"+p+".root"
    cmd='vvMakeVjetsShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -m {minMJ} -M {maxMJ} --store "{filename}_{purity}.py" --minMVV {minMVV} --maxMVV {maxMVV} {addOption} samples '.format(template=template,cut=cut,rootFile=rootFile,minMJ=minMJ,maxMJ=maxMJ,filename=filename,purity=p,minMVV=minMVV,maxMVV=maxMVV,addOption=addOption)
    cmd+=HCALbinsMVV
    os.system(cmd)
    
def makeDetectorResponse(name,filename,template,addCut="1",jobName="DetPar"):
		pwd = os.getcwd()
		samples = pwd +"/samples"
		cut='*'.join([cuts['common'],cuts['metfilters'],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
		resFile=filename+"_"+name+"_detectorResponse.root"		 
		print "Saving detector resolution to file: " ,resFile
		bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"
		if submitToBatch:
			from modules.submitJobs import Make2DDetectorParam,merge2DDetectorParam	
			jobList, files = Make2DDetectorParam(resFile,template,cut,samples,jobName,bins)
			jobList = []
			files = []
			merge2DDetectorParam(jobList,files,bins,jobName)
		else:
			cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b {bins}   samples'.format(rootFile=resFile,samples=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins)
			os.system(cmd)
		
		print "Done with ",resFile
  
def makeBackgroundShapesMJKernel(name,filename,template,leg,addCut="1"):
 
 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  resFile=filename+"_"+name+"_detectorResponse.root"	
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['acceptanceMVV']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+".root"  	      
  cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass" -b {binsMJ}  -x {minMJ} -X {maxMJ} -r {res} samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ)
  os.system(cmd)

def makeBackgroundShapesMJSpline(name,filename,template,leg,addCut="1"):

 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptance']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+"_spline.root"	      
  cmd='vvMake1DTemplateSpline.py  -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_softDrop_mass"  -b {binsMJ}  -x {minMJ} -X {maxMJ} -f 6 samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ)
  os.system(cmd)


def makeBackgroundShapesMVVKernel(name,filename,template,addCut="1",jobName="1DMVV",wait=True):
 pwd = os.getcwd()
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile  = pwd + "/"+ filename+"_"+name+"_detectorResponse.root"	
  rootFile = filename+"_"+name+"_MVV_"+p+".root"
  print "Reading " ,resFile
  print "Saving to ",rootFile
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['acceptanceMJ']])
  samples = pwd +"/samples"

  if submitToBatch:
    if name.find("VJets")== -1: template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make1DMVVTemplateWithKernels,merge1DMVVTemplate
    jobList, files = Make1DMVVTemplateWithKernels(rootFile,template,cut,resFile,binsMVV,minMVV,maxMVV,samples,jobname,wait,HCALbinsMVV,addOption)
    if wait: merge1DMVVTemplate(jobList,files,jobname,p,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
  else:
    cmd='vvMake1DMVVTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_gen_partialMass" -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} {addOption} samples'.format(rootFile=rootFile,samples=template,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,addOption=addOption)
    cmd = cmd+HCALbinsMVV
    os.system(cmd)	  

def makeBackgroundShapesMVVConditional(name,filename,template,leg,addCut="",jobName="2DMVV",wait=True):
 pwd = os.getcwd()	
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile  = pwd + "/"+ filename+"_"+name+"_detectorResponse.root"
  rootFile=filename+"_"+name+"_COND2D_"+p+"_"+leg+".root"		
  print "Reading " ,resFile
  print "Saving to ",rootFile
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
  samples = pwd +"/samples" 
  
  if submitToBatch:
    if name.find("VJets")== -1: template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make2DTemplateWithKernels,merge2DTemplate
    jobList, files = Make2DTemplateWithKernels(rootFile,template,cut,leg,binsMVV,minMVV,maxMVV,resFile,binsMJ,minMJ,maxMJ,samples,jobname,wait,HCALbinsMVV,addOption)
    if wait: merge2DTemplate(jobList,files,jobname,p,leg,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
  else:
      cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{samples}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass,jj_gen_partialMass"  -b {binsMJ} -B {binsMVV} -x {minMJ} -X {maxMJ} -y {minMVV} -Y {maxMVV}  -r {res} {addOption} samples'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ,addOption=addOption)
      cmd=cmd+HCALbinsMVV
      os.system(cmd)

def mergeKernelJobs():
	for p in purities:
		jobList = []
		files   = []
		with open("tmp1D_%s_joblist.txt"%p,'r') as infile:
			for line in infile:
				if line.startswith("job"):
					for job in line.split("[")[1].split("]")[0].split(","):
						jobList.append(job.replace("'","").replace(" ",""))
			if line.startswith("file"):
				for job in line.split("[")[1].split("]")[0].split(","):
					files.append(job.replace("'","").replace(" ",""))	
		from modules.submitJobs import merge1DMVVTemplate
        merge1DMVVTemplate(jobList,files,"1D"+"_"+p,p,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
		
        jobList = []
        files   = []
        with open("tmp2Dl1_%s_joblist.txt"%p,'r') as infile:
            for line in infile:
                if line.startswith("job"):
                    for job in line.split("[")[1].split("]")[0].split(","):
                        jobList.append(job.replace("'","").replace(" ",""))
            if line.startswith("file"):
                for job in line.split("[")[1].split("]")[0].split(","):
                    files.append(job.replace("'","").replace(" ",""))

        from modules.submitJobs import merge2DTemplate
        merge2DTemplate(jobList,files,"2Dl1"+"_"+p,p,"l1",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
        merge2DTemplate(jobList,files,"2Dl2"+"_"+p,p,"l2",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)

def mergeBackgroundShapes(name,filename):

 for p in purities:
  inputx=filename+"_"+name+"_COND2D_"+p+"_l1.root"	
  inputy=filename+"_"+name+"_COND2D_"+p+"_l2.root"	
  inputz=filename+"_"+name+"_MVV_"+p+".root"      
  rootFile=filename+"_"+name+"_3D_"+p+".root"
  print "Reading " ,inputx
  print "Reading " ,inputy
  print "Reading " ,inputz
  print "Saving to ",rootFile 
  cmd='vvMergeHistosToPDF3D.py -i "{inputx}" -I "{inputy}" -z "{inputz}" -o "{rootFile}"'.format(rootFile=rootFile,inputx=inputx,inputy=inputy,inputz=inputz)
  os.system(cmd)
  print "Adding trigger shape uncertainties"
  cmd='vvMakeTriggerShapes.py -i "{rootFile}"'.format(rootFile=rootFile)
  os.system(cmd)

def makeNormalizations(name,filename,template,data=0,addCut='1',jobName="nR",factors="1"):
  pwd = os.getcwd()
  samples = pwd +"/samples/"
  for p in purities:
   jobname = jobName+"_"+p
   rootFile=filename+"_"+name+"_"+p+".root"
   print "Saving to ",rootFile  
   cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptance']])
   if submitToBatch:
   	   if name.find("VJets")== -1: template += ",QCD_Pt-,QCD_HT"
   	   from modules.submitJobs import makeData,mergeData
   	   jobList, files = makeData(template,cut,rootFile,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,factors,name,data,jobname,samples,True,HCALbinsMVV,addOption)
   	   mergeData(jobname,p,rootFile)
   else:
        cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "jj_l1_softDrop_mass,jj_l2_softDrop_mass,jj_LV_mass" -b "{bins},{bins},{BINS}" -m "{mini},{mini},{MINI}" -M "{maxi},{maxi},{MAXI}" -f {factors} -n "{name}" {addOption} samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJ,MINI=minMVV,MAXI=maxMVV,mini=minMJ,maxi=maxMJ,factors=factors,name=name,data=data,addOption=addOption)
        cmd=cmd+HCALbinsMVV
        os.system(cmd)
   
  
  


makeSignalShapesMVV("JJ_WprimeWZ",WprimeTemplate)
makeSignalShapesMJ("JJ_WprimeWZ",WprimeTemplate,'l1')
makeSignalShapesMJ("JJ_WprimeWZ",WprimeTemplate,'l2')
makeSignalYields("JJ_WprimeWZ",WprimeTemplate,BRWZ,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

makeSignalShapesMVV("JJ_BulkGWW",BulkGravWWTemplate)
makeSignalShapesMJ("JJ_BulkGWW",BulkGravWWTemplate,'l1')
makeSignalShapesMJ("JJ_BulkGWW",BulkGravWWTemplate,'l2')
makeSignalYields("JJ_BulkGWW",BulkGravWWTemplate,BRWW,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

makeSignalShapesMVV("JJ_ZprimeWW",ZprimeWWTemplate)
makeSignalShapesMJ("JJ_ZprimeWW",ZprimeWWTemplate,'l1')
makeSignalShapesMJ("JJ_BulkGWW",BulkGravWWTemplate,'l2')
makeSignalYields("JJ_ZprimeWW",ZprimeWWTemplate,BRWW,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

makeSignalShapesMVV("JJ_BulkGZZ",BulkGravZZTemplate)
makeSignalShapesMJ("JJ_BulkGZZ",BulkGravZZTemplate,'l1')
makeSignalShapesMJ("JJ_BulkGZZ",BulkGravZZTemplate,'l2')
makeSignalYields("JJ_BulkGZZ",BulkGravZZTemplate,BRZZ,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

makeDetectorResponse("nonRes","JJ",nonResTemplate,cuts['nonres'])


# ------ do not use these ------
# makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'])
# makeBackgroundShapesMJKernel("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'])
# makeBackgroundShapesMJSpline("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'])
# makeBackgroundShapesMJSpline("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'])
# ------------------------------

#Make nonres kernel
if runParallel and submitToBatch:
  wait = False
  makeBackgroundShapesMVVKernel("nonRes","JJ",nonResTemplate,cuts['nonres'],"1D",wait)
  makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
  makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
  print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
  sys.exit()
  mergeKernelJobs()
else:
  wait = True
  makeBackgroundShapesMVVKernel("nonRes","JJ",nonResTemplate,cuts['nonres'],"1D",wait)
  makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
  makeBackgroundShapesMVVConditional("nonRes","JJ",nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)

if runParallel and submitToBatch: mergeKernelJobs()
mergeBackgroundShapes("nonRes","JJ")

#  Do QCD normalisation
makeNormalizations("nonRes","JJ",nonResTemplate,0,cuts['nonres'],"nR")

# Do Vjets
submitToBatch = False #Do not need batch for the following
if period == 2017:
    makeNormalizations("VJets","JJ",resTemplate,0,cuts['res'],"nRes","ZJetsToQQ:0.3425,WJetsToQQ:0.3425")
else:
    makeNormalizations("VJets","JJ",resTemplate,0,cuts['res'],"nRes","ZJetsToQQ:0.071")
fitVJets("JJ_VJets",resTemplate)
makeBackgroundShapesMVVKernel("VJets","JJ",resTemplate,cuts['nonres'],"1D",0)

# Do data
makeNormalizations("data","JJ",dataTemplate,1,'1',"normD") #run on data. Currently run on pseudodata only (below)
from modules.submitJobs import makePseudoData
for p in purities: makePseudoData("JJ_nonRes_%s.root"%p,"JJ_nonRes_3D_%s.root"%p,"pythia","JJ_PD_%s.root"%p,lumi)


