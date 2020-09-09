import ROOT
import os,sys
import numpy
import cuts


 
ctx  = cuts.cuts("init_VV_VH.json","2017","random_dijetbins",False) 

HPSF = ctx.HPSF_vtag*ctx.HPSF_vtag
LPSF = ctx.HPSF_ctag*ctx.LPSF_vtag

HCALbinsMVV=" --binsMVV "+ctx.HCALbinsMVV
    

cuts={}


cuts['common'] = ctx.cuts['common']
 

cuts['HPHP'] = ctx.cuts['VV_HPHP']
cuts['HPLP'] = ctx.cuts['VV_HPLP']
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


  
minMJ=ctx.minMJ
maxMJ=ctx.maxMJ
minMVV =ctx.minMVV
maxMVV=ctx.minMVV

binsMJ=ctx.binsMJ
binsMVV = ctx.binsMVV
    

cuts['acceptance']= ctx.cuts['acceptance']
cuts['acceptanceGEN']=ctx.cuts['acceptanceGEN']

cuts['acceptanceMJ']= ctx.cuts['acceptanceMJ']


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
    makeJECShapesMVV("JECUncertainty_BulkZZ",BulkGravZZTemplate)
    makeJECShapesMVV("JECUncertainty_ZprimeWW",ZprimeWWTemplate)
    makeJECShapesMVV("JECUncertainty_WprimeWZ",WprimeTemplate)
    log = open("JECUncertainties.log","w")
    filelist = ["JECUncertainty_BulkWW_HPHP_MVV_JER.txt","JECUncertainty_BulkZZ_HPHP_MVV_JER.txt","JECUncertainty_WprimeWZ_HPHP_MVV_JER.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JER.txt"]
    makeOutputFile(filelist,"JER uncertainties for HPHP category",log)
    
    
    filelist = ["JECUncertainty_BulkWW_HPHP_MVV_JES.txt","JECUncertainty_BulkZZ_HPHP_MVV_JES.txt","JECUncertainty_WprimeWZ_HPHP_MVV_JES.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JES.txt"]
    makeOutputFile(filelist,"JES uncertainties for HPHP category",log)
    
    filelist = ["JECUncertainty_BulkWW_HPLP_MVV_JER.txt","JECUncertainty_BulkZZ_HPLP_MVV_JER.txt","JECUncertainty_WprimeWZ_HPLP_MVV_JER.txt","JECUncertainty_ZprimeWW_HPLP_MVV_JER.txt"]
    makeOutputFile(filelist,"JER uncertainties for HPLP category",log)
    
    
    filelist = ["JECUncertainty_BulkWW_HPLP_MVV_JES.txt","JECUncertainty_BulkZZ_HPLP_MVV_JES.txt","JECUncertainty_WprimeWZ_HPLP_MVV_JES.txt","JECUncertainty_ZprimeWW_HPHP_MVV_JES.txt"]
    makeOutputFile(filelist,"JES uncertainties for HPLP category",log)
    
    
    log.close()
    
    
    
    
    
    
    
    
