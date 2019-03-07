import ROOT
import os,sys


period = 2017 #2016

samples= "samples/"# "/ceph/dschaefer/VV3D2017/2017_JECV6_PURew_NoJER_LOWeights_CHSrescale_CHSJER/"#"/ceph/dschaefer/VV3D2017/NoJERSmearing/"#"samples/"
if period==2016:
    samples= "samples2016/" # "/ceph/dschaefer/VV3D2016/SignalSamples2016_JERsmearing/" #"samples2016/"

submitToBatch = False #Set to true if you want to submit kernels + makeData to batch!
runParallel   = False #Set to true if you want to run all kernels in parallel! This will exit this script and you will have to run mergeKernelJobs when your jobs are done! TODO! Add waitForBatchJobs also here?
dijetBinning = True
useTriggerWeights = False


HPSF = 0.937
LPSF = 1.006
if period == 2017:
    HPSF = 0.955#0.948
    LPSF = 1.003#1.057
    
addOption = ""
if useTriggerWeights: 
    addOption = "-t"
    
if dijetBinning:
    HCALbinsMVVSignal=" --binsMVV 1,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5500,5663,5877,6099,6328,6564,6808"
    dijetbins = [1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5500] # ,7060,7320,7589]
    # dijetbins = [1126,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808,7060,7320,7589]
    HCALbinsMVV  =" --binsMVV "
    HCALbinsMVV += ','.join(str(e) for e in dijetbins)
else:
    HCALbinsMVV=""
    HCALbinsMVVSignal=""
    
cat={}

# For retuned DDT tau 21, use this

cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.43'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.43'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.43&&(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.79'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.43&&(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.79'
cat['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.080*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.79'
cat['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.080*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.79'
cat['genHP1'] = '(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt)))<0.43'
cat['genHP2'] = '(jj_l2_gen_tau2/jj_l2_gen_tau1+(0.080*TMath::Log((jj_l2_gen_softDrop_mass*jj_l2_gen_softDrop_mass)/jj_l2_gen_pt)))<0.43'
cat['genLP1'] = '(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt)))>0.43&&(jj_l1_gen_tau2/jj_l1_gen_tau1+(0.080*TMath::Log((jj_l1_gen_softDrop_mass*jj_l1_gen_softDrop_mass)/jj_l1_gen_pt)))<0.79'
cat['genLP2'] = '(jj_l2_gen_tau2/jj_l2_gen_tau1+(0.080*TMath::Log((jj_l2_gen_softDrop_mass*jj_l2_gen_softDrop_mass)/jj_l2_gen_pt)))>0.43&&(jj_l2_gen_tau2/jj_l2_gen_tau1+(0.080*TMath::Log((jj_l2_gen_softDrop_mass*jj_l2_gen_softDrop_mass)/jj_l2_gen_pt)))<0.79'




cuts={}

cuts['genHPHP'] = '('+cat['genHP1']+'&&'+cat['genHP2']+')'
cuts['genLPLP'] = '('+cat['genLP1']+'&&'+cat['genLP2']+')'
cuts['genHPLP'] = '(('+cat['genHP1']+'&&'+cat['genLP2']+')||('+cat['genLP1']+'&&'+cat['genHP2']+'))'

if period == 2017:
    lumi = 41367.
    
    cuts['metfilters'] = "(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)"
else:
    lumi = 35900.
    cuts['metfilters'] =("Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter")

cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.&&TMath::Log(jj_l1_softDrop_mass**2/jj_l1_pt**2)<-1.8&&TMath::Log(jj_l2_softDrop_mass**2/jj_l2_pt**2)<-1.8)' #with rho


cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
cuts['NP'] = '(('+cat['LP1']+'&&'+cat['NP2']+')||('+cat['NP1']+'&&'+cat['LP2']+')||('+cat['NP1']+'&&'+cat['NP2']+'))'

cuts['nonres'] = '1'
cuts['res'] = '(jj_l1_mergedVTruth==1&&jj_l1_softDrop_mass>60&&jj_l1_softDrop_mass<120)'
cuts['resTT'] = '(jj_l1_mergedVTruth==1&&jj_l1_softDrop_mass>140&&jj_l1_softDrop_mass<200)'

purities=['HPHP','HPLP','LPLP','NP']
purities=['HPHP','HPLP','LPLP']
purities=['HPHP',"HPLP"]

BulkGravWWTemplate="BulkGravToWW_narrow_"
#BulkGravWWTemplate="BulkWW"
BulkGravZZTemplate="BulkGravToZZToZhadZhad"
WprimeTemplate= "WprimeToWZToWhadZhad"
ZprimeWWTemplate= "ZprimeToWW"
# use arbitrary cross section 0.001 so limits converge better
BRWW=1.*0.001
BRZZ=1.*0.001*0.6991*0.6991
BRWZ=1.*0.001*0.6991*0.676

dataTemplate="JetHT"
nonResTemplate="QCD_Pt_" #high stat

# nonResTemplate="QCD_Pt-" #low stat --> use this for tests
#nonResTemplate="Dijet" #to compare shapes
WTemplate= "WJetsToQQ_HT800toInf_new"
TTemplate= "TTHad"

WresTemplate= "WJetsToQQ_HT800toInf_new,TTHad_pow"
ZresTemplate= "ZJetsToQQ_HT800toInf_new"
resTemplate= "ZJetsToQQ_HT800toInf_new,WJetsToQQ_HT800toInf_new,TTHad_pow"
directory = "samplesVjets/"
# if period == 2016:
#    resTemplate= "WJetsToQQ_HT600toInf_new,ZJetsToQQ_HT600toInf_new" 
#    WresTemplate= "WJetsToQQ_HT600,TTHad_pow"
#    ZresTemplate= "ZJetsToQQ_HT600"
#    directory = "samplesVjets2016/"
    
minMJ=55.0
maxMJ=215.0


binsMJ=80

minMVV=838.0
maxMVV=6000.
binsMVV=100

if dijetBinning:
    minMVV = float(dijetbins[0])
    maxMVV = float(dijetbins[-1])
    binsMVV= len(dijetbins)-1
    
    
    
if useTriggerWeights:
    minMVV=838.0
    maxMVV=5500.0
    minMX=1000.0
    maxMX=7000.0
    if dijetBinning:
        binsMVV = 39
        
else:
    minMVV=1126.0
    maxMVV=5500.0
    minMX=1000.0
    maxMX=6000.0
    if dijetBinning:
        binsMVV = 36
    



cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceMJ']= "(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceMVV'] = "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV})".format(minMVV=minMVV,maxMVV=maxMVV)
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>20.&&jj_l2_gen_softDrop_mass>20.&jj_l1_gen_softDrop_mass<300.&&jj_l2_gen_softDrop_mass<300.&&jj_gen_partialMass>800.&&jj_gen_partialMass<6000.&&TMath::Log(jj_l1_gen_softDrop_mass**2/jj_l1_gen_pt**2)<-1.5&&TMath::Log(jj_l2_gen_softDrop_mass**2/jj_l2_gen_pt**2)<-1.5)'
cuts['looseacceptanceMJ']= "(jj_l1_softDrop_mass>35&&jj_l1_softDrop_mass<300&&jj_l2_softDrop_mass>35&&jj_l2_softDrop_mass<300)"

def makeSignalShapesMVV(filename,template):
 cut='*'.join([cuts['common'],cuts['metfilters'],cuts['acceptanceMJ']])
 rootFile=filename+"_MVV.root"
 fixPars = "N1:1.61364,N2:4.6012"
 cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_LV_mass" {BinningMVV} --fix "{fixPars}"   -m {minMVV} -M {maxMVV} --minMX {minMX} --maxMX {maxMX} {addOption} {samples} '.format(template=template,cut=cut,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV,minMX=minMX,maxMX=maxMX,BinningMVV=HCALbinsMVVSignal,fixPars=fixPars,addOption=addOption,samples=samples)
 os.system(cmd)
 jsonFile=filename+"_MVV.json"
 print 'Making JSON'
 cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol6,ALPHA1:pol5,N1:pol0,ALPHA2:pol4,N2:pol0" -m {minMX} -M {maxMX} {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile,minMX=minMX,maxMX=maxMX)
 os.system(cmd)

def makeSignalShapesMJ(filename,template,leg):
    #default is for BulkGravToWW samples
 for p in purities:
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p]])
  rootFile=filename+"_MJ"+leg+"_"+p+".root"
  jsonFile=filename+"_MJ"+leg+"_"+p+".json"
  doExp=0
  fixPars="alpha:1.08,n:6,n2:2"
  if p=='HPHP':
      if template.find("Wprime")!=-1:
          fixPars="alpha:1.505,n:2,n2:2"
      if template.find("Zprime")!=-1:
          fixPars="n:2.85,alpha:1.083,n2:2"
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "{fixPars}" --minMX {minMX} --maxMX {maxMX} {addOption} {samples} '.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX,fixPars=fixPars,addOption=addOption,samples=samples)
      cmdjson='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol5,sigma:pol3,alpha:pol0,n:pol0,alpha2:pol3,n2:pol0,slope:pol0,f:pol3" -m {minMX} -M {maxMX} {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile,minMX=minMX,maxMX=maxMX)

  else:
      # doExp=1
      fixPars="alpha:1.125,n:2,n2:2"
      if template.find("Wprime")!=-1:
          fixPars="n:2,n2:2"
      cmd='vvMakeSignalMJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_{leg}_softDrop_mass" -m {minMJ} -M {maxMJ} -e {doExp} -f "{fixPars}" --minMX {minMX} --maxMX {maxMX} {addOption} {samples} '.format(template=template,cut=cut,rootFile=rootFile,leg=leg,minMJ=minMJ,maxMJ=maxMJ,doExp=doExp,minMX=minMX,maxMX=maxMX,fixPars=fixPars,addOption=addOption,samples=samples)
      cmdjson='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol5,sigma:pol3,alpha:pol3,n:pol0,alpha2:pol4,n2:pol0,slope:pol0,f:pol0" -m {minMX} -M {maxMX} {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile,minMX=minMX,maxMX=maxMX)
  os.system(cmd)
  #os.system(cmdjson)


def makeSignalYields(filename,template,branchingFraction,sfP = {'HPHP':1.0,'HPLP':1.0,'LPLP':1.0}):
 print "using the following scalfactors:" ,sfP
 for p in purities:
  cut = "*".join([cuts[p],cuts['common'],cuts['metfilters'],cuts['acceptance'],str(sfP[p])])
  #Signal yields
  yieldFile=filename+"_"+p+"_yield"
  fnc = "pol7"
  cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "jj_LV_mass" -m {minMVV} -M {maxMVV} -f {fnc} -b {BR} --minMX {minMX} --maxMX {maxMX} {addOption} {samples} '.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,fnc=fnc,BR=branchingFraction,minMX=minMX,maxMX=maxMX,addOption=addOption,samples=samples)
  os.system(cmd)

def fitVJets(filename,template,Wxsec=1,Zxsec=1):
  for p in purities:
    cut='*'.join([cuts['common'],cuts[p],cuts['acceptance']])
    rootFile=filename+"_"+p+".root"

    print cuts["acceptance"]
    fixPars="1" #"n:0.8,alpha:1.9"
    cmd='vvMakeVjetsShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -m {minMJ} -M {maxMJ} --store "{filename}_{purity}.py" --minMVV {minMVV} --maxMVV {maxMVV} {addOption} --corrFactorW {Wxsec} --corrFactorZ {Zxsec} {samples} '.format(template=template,cut=cut,rootFile=rootFile,minMJ=minMJ,maxMJ=maxMJ,filename=filename,purity=p,minMVV=minMVV,maxMVV=maxMVV,addOption=addOption,Wxsec=Wxsec,Zxsec=Zxsec,samples=directory)
    cmd+=HCALbinsMVV
    os.system(cmd)
    
def makeDetectorResponse(name,filename,template,addCut="1",jobName="DetPar"):
        pwd = os.getcwd()
        #samples = pwd +"/samples_jer/"
        cut='*'.join([cuts['common'],cuts['metfilters'],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
        resFile=filename+"_"+name+"_detectorResponse.root"       
        print "Saving detector resolution to file: " ,resFile
        bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1200,1500,1800,2200,2600,3000,3400,3800,5000"#4200,4600,5000,7000"#TODO: The last three bins are empty, remove next iteration!
        # bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,2700,3500,5000"
        # bins = "200,300,400,500,600,700,800,900,1000,1500,2000,2700,5000"
        if submitToBatch:
            from modules.submitJobs import Make2DDetectorParam,merge2DDetectorParam 
            jobList, files = Make2DDetectorParam(resFile,template,cut,samples,jobName,bins)
            jobList = []
            files = []
            merge2DDetectorParam(resFile,bins,jobName)
        else:
            cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b {bins}   {samples}'.format(rootFile=resFile,template=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins,samples=samples)
            os.system(cmd)
        
        print "Done with ",resFile

def makeDetectorResponsePerCat(name,filename,template,addCut="1",jobName="DetPar",wait=True):
        wait = False
        pwd = os.getcwd()
        samples = pwd +"/samples"
        for p in purities:
            cut='*'.join([cuts['common'],cuts['metfilters'],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ'],cuts[p]])
            resFile=filename+"_"+name+"_detectorResponse_%s.root"%p       
            print "Saving detector resolution to file: " ,resFile
            # bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1200,1500,1800,2200,2600,3000,3400,3800,4200,4600,5000,7000"
            bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,2700,3500,5000"
            bins = "200,300,400,500,600,700,800,900,1000,1500,2000,2700,5000"
            if submitToBatch:
                from modules.submitJobs import Make2DDetectorParam,merge2DDetectorParam 
                # jobList, files = Make2DDetectorParam(resFile,template,cut,samples,jobName,bins,wait)
                jobList = []
                files = []
                merge2DDetectorParam(resFile,bins,jobName)
            else:
                cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b {bins}   {samples}'.format(rootFile=resFile,template=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins,samples=samples)
                os.system(cmd)
            
            print "Done with ",resFile

def makeDetectorResponsePerLeg(name,filename,template,addCut="1",jobName="DetPar",leg="l1"):
        pwd = os.getcwd()
        samples = pwd +"/samples_jer/"
        cut='*'.join([cuts['common'],cuts['metfilters'],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
        cut='*'.join([cuts['common'],cuts['metfilters'],addCut,cuts['acceptance']])
        resFile=filename+"_"+name+"_detectorResponse_%s_accepCuts.root"%(leg)       
        print "Saving detector resolution to file: " ,resFile
        bins = "200,250,300,350,400,450,500,600,700,800,900,1000,1200,1500,1800,2200,2600,3000,3400,3800,5000"
        if submitToBatch:
            from modules.submitJobs import Make2DDetectorParam,merge2DDetectorParam 
            jobList, files = Make2DDetectorParam(resFile,template,cut,samples,jobName,bins,True,leg)
            jobList = []
            files = []
            merge2DDetectorParam(resFile,bins,jobName)
        else:
            if leg == "l1": cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b {bins}   {samples}'.format(rootFile=resFile,template=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins,samples=samples)
            if leg == "l2": cmd='vvMake2DDetectorParam.py  -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_LV_mass,jj_l2_softDrop_mass"  -g "jj_gen_partialMass,jj_l2_gen_softDrop_mass,jj_l2_gen_pt"  -b {bins}   {samples}'.format(rootFile=resFile,template=template,cut=cut,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,tag=name,bins=bins,samples=samples)
            os.system(cmd)
        
        print "Done with ",resFile
        
          
def makeBackgroundShapesMJKernel(name,filename,template,leg,addCut="1"):
 
 template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  resFile=filename+"_"+name+"_detectorResponse.root"    
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['acceptanceMVV']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+".root"          
  cmd='vvMake1DTemplateWithKernels.py -H "y" -o "{rootFile}" -s "{tmplate}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass" -b {binsMJ}  -x {minMJ} -X {maxMJ} -r {res} {sdir}'.format(rootFile=rootFile,tmplate=template,cut=cut,leg=leg,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ,sdir=samples)
  os.system(cmd)

def makeBackgroundShapesMJSpline(name,filename,template,leg,addCut="1"):

 #template += ",QCD_Pt-,QCD_HT"
 for p in purities:
  print "=========== PURITY: ", p
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptance']])
  rootFile=filename+"_"+name+"_MJ"+leg+"_"+p+"_spline.root"       
  cmd='vvMake1DTemplateSpline.py  -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_{leg}_softDrop_mass"  -b {binsMJ}  -x {minMJ} -X {maxMJ} -f 6 {samples}'.format(rootFile=rootFile,template=template,cut=cut,leg=leg,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ,samples=samples)
  os.system(cmd)


def makeBackgroundShapesMVVKernel(name,filename,template,addCut="1",jobName="1DMVV",wait=True,corrFactorW=1,corrFactorZ=1):
 pwd = os.getcwd()
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile  = pwd + "/"+ filename+"_"+name+"_detectorResponse.root"
  if name.find("Jets")!=-1:
      resFile="JJ_nonRes_detectorResponse.root"

  rootFile = filename+"_"+name+"_MVV_"+p+".root"
  print "Reading " ,resFile
  print "Saving to ",rootFile
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
  smp = pwd +"/"+samples
  if name.find("Jets")!= -1: smp = pwd +"/samplesVjets/"

  if submitToBatch:
    if name.find("Jets")== -1: template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make1DMVVTemplateWithKernels,merge1DMVVTemplate
    jobList, files = Make1DMVVTemplateWithKernels(rootFile,template,cut,resFile,binsMVV,minMVV,maxMVV,smp,jobname,wait,HCALbinsMVV,addOption)
    if wait: merge1DMVVTemplate(jobList,files,jobname,p,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
  else:
    if name.find("Jets")== -1: template += ",QCD_Pt-,QCD_HT"  
    cmd='vvMake1DMVVTemplateWithKernels.py -H "x" -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_gen_partialMass" -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} {addOption} {directory} --corrFactorW {corrFactorW} --corrFactorZ {corrFactorZ} '.format(rootFile=rootFile,template=template,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,addOption=addOption,corrFactorW=corrFactorW,corrFactorZ=corrFactorZ,directory=smp)
    cmd = cmd+HCALbinsMVV
    os.system(cmd)    

def makeBackgroundShapesMVVConditional(name,filename,template,leg,addCut="",jobName="2DMVV",wait=True):
 pwd = os.getcwd()  
 for p in purities:
  jobname = jobName+"_"+p
  print " Working on purity: ", p
  resFile=filename+"_"+name+"_detectorResponse.root"
  # resFile=filename+"_"+name+"_detectorResponse_%s_accepCuts.root"%leg
  rootFile=filename+"_"+name+"_COND2D_"+p+"_"+leg+".root"       
  print "Reading " ,resFile
  print "Saving to ",rootFile
  cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],addCut])#,cuts['acceptanceGEN'],cuts['looseacceptanceMJ']])
  smp = pwd +"/"+samples 
  
  if submitToBatch:
    if name.find("VJets")== -1: template += ",QCD_Pt-,QCD_HT"
    from modules.submitJobs import Make2DTemplateWithKernels,merge2DTemplate
    jobList, files = Make2DTemplateWithKernels(rootFile,template,cut,leg,binsMVV,minMVV,maxMVV,resFile,binsMJ,minMJ,maxMJ,smp,jobname,wait,HCALbinsMVV,addOption)
    if wait: merge2DTemplate(jobList,files,jobname,p,leg,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,HCALbinsMVV)
  else:
      if name.find("VJets")== -1: template += ",QCD_Pt-,QCD_HT"
      cmd='vvMake2DTemplateWithKernels.py -o "{rootFile}" -s "{template}" -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass,jj_gen_partialMass"  -b {binsMJ} -B {binsMVV} -x {minMJ} -X {maxMJ} -y {minMVV} -Y {maxMVV}  -r {res} {addOption} {samples}'.format(rootFile=rootFile,template=template,cut=cut,leg=leg,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ,addOption=addOption,samples=smp)
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

  #inputz="save_new_shapes_pythia_"+p+"_1D.root"
  #inputx="save_new_shapes_pythia_"+p+"_COND2D_l1.root"
  #inputy="save_new_shapes_pythia_"+p+"_COND2D_l2.root"
 #  #
  # inputz="save_new_shapes_looseDDT_"+p+"_1D.root"
  # inputx="save_new_shapes_looseDDT_"+p+"_COND2D_l1.root"
  # inputy="save_new_shapes_looseDDT_"+p+"_COND2D_l2.root"
     
  # rootFile=filename+"_"+name+"_3D_"+p+".root"
  rootFile="SaveNewShapes_"+name+"_3D_"+p+".root"
  print "Reading " ,inputx
  print "Reading " ,inputy
  print "Reading " ,inputz
  print "Saving to ",rootFile 
  cmd='vvMergeHistosToPDF3D.py -i "{inputx}" -I "{inputy}" -z "{inputz}" -o "{rootFile}"'.format(rootFile=rootFile,inputx=inputx,inputy=inputy,inputz=inputz)
  os.system(cmd)
  print "Adding trigger shape uncertainties"
  if useTriggerWeights: 
      cmd='vvMakeTriggerShapes.py -i "{rootFile}"'.format(rootFile=rootFile)
      os.system(cmd)

def makeNormalizations(name,filename,template,data=0,addCut='1',jobName="nR",factors="1",wait=True):
  pwd = os.getcwd()
  sam = pwd +"/"+samples
  if name.find("Jets")!= -1 or name.find("tt")!=-1: sam = pwd +"/samplesVjets/"
  print "using files in" , sam
  # if name.find("data")!= -1: samples = "/eos/user/t/thaarres/reduced/"
  for p in purities:
   if name.find("Jets")!=-1:
        if p == "HPLP":
            factors=factors+",sf:"+str(LPSF)
        else:
            factors=factors+",sf:"+str(HPSF)
      
   jobname = jobName+"_"+p
   rootFile=filename+"_"+name+"_"+p+".root"
   print "Saving to ",rootFile  
   cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptance']])

   if submitToBatch:
       if name.find("nonRes")!= -1: template += ",QCD_Pt-,QCD_HT"
       from modules.submitJobs import makeData,mergeData
       jobList, files = makeData(template,cut,rootFile,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,factors,name,data,jobname,sam,wait,HCALbinsMVV,addOption)
       wait = True
       mergeData(jobname,p,rootFile)
   else:
        print "using cut: " ,cut
        cmd='vvMakeData.py -s "{template}" -d {data} -c "{cut}"  -o "{rootFile}" -v "jj_l1_softDrop_mass,jj_l2_softDrop_mass,jj_LV_mass" -b "{bins},{bins},{BINS}" -m "{mini},{mini},{MINI}" -M "{maxi},{maxi},{MAXI}" -f {factors} -n "{name}" {addOption} {samples}'.format(template=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJ,MINI=minMVV,MAXI=maxMVV,mini=minMJ,maxi=maxMJ,factors=factors,name=name,data=data,addOption=addOption,samples=sam)
        cmd=cmd+HCALbinsMVV
        print cmd
        os.system(cmd)
   
  
  

#makeSignalShapesMVV("JJ_WprimeWZ_"+str(period),WprimeTemplate)
#makeSignalShapesMJ("JJ_WprimeWZ_"+str(period),WprimeTemplate,'l1')
#makeSignalShapesMJ("JJ_WprimeWZ_"+str(period),WprimeTemplate,'l2')
#makeSignalYields("JJ_WprimeWZ_"+str(period),WprimeTemplate,BRWZ,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

#makeSignalShapesMVV("JJ_BulkGWW_"+str(period),BulkGravWWTemplate)
#makeSignalShapesMJ("JJ_BulkGWW_"+str(period),BulkGravWWTemplate,'l1')
#makeSignalShapesMJ("JJ_BulkGWW_"+str(period),BulkGravWWTemplate,'l2')
#makeSignalYields("JJ_BulkGWW_"+str(period),BulkGravWWTemplate,BRWW,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

#makeSignalShapesMVV("JJ_ZprimeWW_"+str(period),ZprimeWWTemplate)
#makeSignalShapesMJ("JJ_ZprimeWW_"+str(period),ZprimeWWTemplate,'l1')
#makeSignalShapesMJ("JJ_ZprimeWW_"+str(period),ZprimeWWTemplate,'l2')
#makeSignalYields("JJ_ZprimeWW_"+str(period),ZprimeWWTemplate,BRWW,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

#makeSignalShapesMVV("JJ_BulkGZZ_"+str(period),BulkGravZZTemplate)
#makeSignalShapesMJ("JJ_BulkGZZ_"+str(period),BulkGravZZTemplate,'l1')
#makeSignalShapesMJ("JJ_BulkGZZ_"+str(period),BulkGravZZTemplate,'l2')
#makeSignalYields("JJ_BulkGZZ_"+str(period),BulkGravZZTemplate,BRZZ,{'HPHP':HPSF*HPSF,'HPLP':HPSF*LPSF,'LPLP':LPSF*LPSF})

#makeDetectorResponse("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'])

#### # Make nonres kernel
#if runParallel and submitToBatch:
  #wait = False
  #makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'],"1D",wait)
  #makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
  #makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)
  #print "Exiting system! When all jobs are finished, please run mergeKernelJobs below"
  #sys.exit()
  #mergeKernelJobs()
#else:
  #wait = True
  ##makeBackgroundShapesMVVKernel("nonRes","JJ_"+str(period),nonResTemplate,cuts['nonres'],"1D",wait)
  #makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l1',cuts['nonres'],"2Dl1",wait)
  #makeBackgroundShapesMVVConditional("nonRes","JJ_"+str(period),nonResTemplate,'l2',cuts['nonres'],"2Dl2",wait)


#mergeBackgroundShapes("nonRes","JJ_"+str(period))
# Do Vjets
submitToBatch = False #Do not need batch for the following
#makeNormalizations("WJets","JJ",WresTemplate,0,cuts['nonres'],"nRes","WJetsToQQ_HT800toInf:0.205066345")
#makeNormalizations("ZJets","JJ",ZresTemplate,0,cuts['nonres'],"nRes","ZJetsToQQ_HT800toInf:0.09811023622")

#makeNormalizations("VJets","JJ",resTemplate,0,cuts['nonres'],"nRes","WJetsToQQ_HT800toInf:1,ZJetsToQQ_HT800toInf:1")

makeNormalizations("WJets","JJ_NLOweights",WresTemplate,0,cuts['nonres'],"nRes","WJetsToQQ_HT800toInf:0.205066345")
makeNormalizations("ZJets","JJ_NLOweights",ZresTemplate,0,cuts['nonres'],"nRes","ZJetsToQQ_HT800toInf:0.09811023622")
makeNormalizations("TTJets","JJ",TTemplate,0,cuts['nonres'],"nRes","")



fitVJets("JJ_WJets",resTemplate,0.205066345,0.09811023622)#0.3425,0.3425)
makeBackgroundShapesMVVKernel("WJets","JJ_NLOweights",WresTemplate,cuts['nonres'],"1D",0,0.205066345,0.09811023622)
makeBackgroundShapesMVVKernel("ZJets","JJ_NLOweights",ZresTemplate,cuts['nonres'],"1D",0,0.205066345,0.09811023622)



## Do data
#makeNormalizations("data","JJ",dataTemplate,1,'1',"normD") #run on data. Currently run on pseudodata only (below)
#from modules.submitJobs import makePseudoData
#for p in purities: makePseudoData("JJ_nonRes_%s.root"%p,"JJ_nonRes_3D_%s.root"%p,"pythia","JJ_PDnoVjets_%s.root"%p,lumi)
#from modules.submitJobs import makePseudoDataVjets
#for p in purities: makePseudoDataVjets("/afs/cern.ch/user/t/thaarres/public/forJen/looseDDT/JJ_nonRes_%s.root"%p,"/afs/cern.ch/user/t/thaarres/public/forJen/looseDDT/JJ_nonRes_3D_%s.root"%p,"pythia","/afs/cern.ch/user/t/thaarres/public/forJen/looseDDT/JJ_PD_%s.root"%p,lumi,"/afs/cern.ch/user/t/thaarres/public/forJen/looseDDT/workspace_JJ_13TeV_2017.root",2017,p)
