import ROOT
import os,sys
import numpy

HPSF = 0.948
LPSF = 1.057
    

HCALbinsMVV=" --binsMVV 1,3,6,10,16,23,31,40,50,61,74,88,103,119,137,156,176,197,220,244,270,296,325,354,386,419,453,489,526,565,606,649,693,740,788,838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808"
    

 	
cat={}

# For retuned DDT tau 21, use this
cat['HP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57'
cat['HP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57'
cat['LP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98'
cat['LP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98'
cat['NP1'] = '(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.98'
cat['NP2'] = '(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.98'

cuts={}


cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'
cuts['metfilters'] = "(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)"
 

cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
cuts['NP'] = '1'



purities=['HPHP']


BulkGravWWTemplate="BulkGravToWW_narrow_M_4500"
BulkGravZZTemplate="BulkGravToZZToZhadZhad_narrow"
WprimeTemplate= "Wprime"
ZprimeWWTemplate= "ZprimeToWW"

# use arbitrary cross section 0.001 so limits converge better
BRWW=1.*0.001
BRZZ=1.*0.001*0.6991*0.6991
BRWZ=1.*0.001*0.6991*0.676


  
minMJ=55.0
maxMJ=215.0
minMVV =1000
maxMVV=5500

binsMJ=80
binsMVV=100
binsMVV = 36
    

cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
cuts['acceptanceGEN']='(jj_l1_gen_softDrop_mass>20&&jj_l2_gen_softDrop_mass>20&&jj_l1_gen_softDrop_mass<300&&jj_l2_gen_softDrop_mass<300&&jj_gen_partialMass>400)'

cuts['acceptanceMJ']= "(jj_l1_softDrop_mass>{minMJ}&&jj_l1_softDrop_mass<{maxMJ}&&jj_l2_softDrop_mass>{minMJ}&&jj_l2_softDrop_mass<{maxMJ})".format(minMJ=minMJ,maxMJ=maxMJ) 



def makeJECShapesMVV(filename,template):
 for p in purities:   
    cut='*'.join([cuts['common'],cuts['metfilters'],cuts['acceptanceMJ'],cuts[p]])
    rootFile=filename+"_"+p+"_MVV.txt"
    cmd='vvMakeJECShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" {BinningMVV}   -m {minMVV} -M {maxMVV}  -l /eos/cms/store/cmst3/group/exovv/VVtuple/VV3Dproduction/2017_JECV6_PURew_JER/ '.format(template=template,cut=cut,rootFile=rootFile,minMVV=minMVV,maxMVV=maxMVV,BinningMVV=HCALbinsMVV)
    os.system(cmd)
 

def getResults(filelist):
    mean    = []
    sigma   = []
        
    for f in filelist:
        lines = [line.rstrip('\n') for line in open(f,"r")]
        for line in lines:
            if line.find("s")!=-1:
                continue
            tmp1 = line.split(":")[4]
            print tmp1
            t2 = tmp1.split(";")
            print t2
            mu,md = t2[0].split("/")
            su,sd = t2[1].split("/")
            mean.append(abs(float(mu)))
            mean.append(abs(float(md)))
            
            sigma.append(abs(float(su)))
            sigma.append(abs(float(sd)))

    s=0
    for w in sigma:
        s += w**2
    s = numpy.sqrt(s/(len(sigma)-1))

    m=0
    for w in mean:
        m += w**2
    m = numpy.sqrt(m/(len(mean)-1))

    
    
    nsigma = numpy.array(sigma)
    nmean  = numpy.array(mean)
    return [nmean.max(), nsigma.max(),m , s, nmean.mean(), nsigma.mean()]
 
def  makeOutputFile(filelist,label,log):
    log.write(label+" \n")
    log.write("mean: \n")
    log.write("           : max     :    mean   :  std    \n")
    
    
    for f in filelist:
        sample = "BulkGravToWW"
        if f.find("Wprime")!=-1:
            sample ="Wprime"
        if f.find("Zprime")!=-1:
            sample = "Zprime"
        if f.find("Bulk")!=-1 and f.find("Z")!=-1:
            sample = "BulkGravToZZ"
        res = getResults([f])
        log.write(sample+"   "+str(res[0])+"    :   "+str(res[4])+"    :    "+str(res[2])+"\n")
        
    log.write(label+" \n")
    log.write("sigma: \n")
    log.write("           : max     :    mean   :  std    \n")    
        
    for f in filelist:
        sample = "BulkGravToWW"
        if f.find("Wprime")!=-1:
            sample ="WprimeToWZ"
        if f.find("Zprime")!=-1:
            sample = "ZprimeToWW"
        if f.find("Bulk")!=-1 and f.find("Z")!=-1:
            sample = "BulkGravToZZ"
        res = getResults([f])    
        log.write(sample+"   "+str(res[1])+"    :   "+str(res[5])+"    :    "+str(res[3])+"\n")
    
 

if __name__=="__main__":
    makeJECShapesMVV("JECUncertainty_BulkWW",BulkGravWWTemplate)
    #makeJECShapesMVV("JECUncertainty_BulkZZ",BulkGravZZTemplate)
    #makeJECShapesMVV("JECUncertainty_ZprimeWW",ZprimeWWTemplate)
    #makeJECShapesMVV("JECUncertainty_WprimeWZ",WprimeTemplate)
    #log = open("JECUncertainties.log","w")
    #filelist = ["JECUncertainty_BulkWW_HPHP_MVV_JER.txt","JECUncertainty_BulkZZ_HPHP_MVV_JER.txt","JECUncertainty_WprimeWZ_HPHP_MVV_JER.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JER.txt"]
    #makeOutputFile(filelist,"JER uncertainties for HPHP category",log)
    
    
    #filelist = ["JECUncertainty_BulkWW_HPHP_MVV_JES.txt","JECUncertainty_BulkZZ_HPHP_MVV_JES.txt","JECUncertainty_WprimeWZ_HPHP_MVV_JES.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JES.txt"]
    #makeOutputFile(filelist,"JES uncertainties for HPHP category",log)
    
    #filelist = ["JECUncertainty_BulkWW_HPLP_MVV_JER.txt","JECUncertainty_BulkZZ_HPLP_MVV_JER.txt","JECUncertainty_WprimeWZ_HPLP_MVV_JER.txt","JECUncertainty_ZprimeWW_HPLP_MVV_JER.txt"]
    #makeOutputFile(filelist,"JER uncertainties for HPLP category",log)
    
    
    #filelist = ["JECUncertainty_BulkWW_HPLP_MVV_JES.txt","JECUncertainty_BulkZZ_HPLP_MVV_JES.txt","JECUncertainty_WprimeWZ_HPLP_MVV_JES.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JES.txt"]
    #makeOutputFile(filelist,"JES uncertainties for HPLP category",log)
    
    
    #log.close()
    
    
    
    
    
    
    
    
