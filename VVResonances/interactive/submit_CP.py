import ROOT
from CMGTools.VVResonances.plotting.RooPlotter import *
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
import os
from array import array
from time import sleep
from datetime import datetime
startTime = datetime.now()
ROOT.gROOT.SetBatch(True)

def getPlotters(indir,samples,isData,period,corr="1"):
    sampleTypes=samples.split(',')
    plotters=[]
    for filename in os.listdir(indir):
        for sampleType in sampleTypes:
            if filename.find(sampleType)!=-1:
                fnameParts=filename.split('.')
                fname=fnameParts[0]
                ext=fnameParts[1]
                if ext.find("root") ==-1:
                    continue
                print 'Adding file',fname
                plotters.append(TreePlotter(indir+'/'+fname+'.root','tree'))
                if not isData:
                  print "IS NOT DATA!!!"
                  plotters[-1].setupFromFile(indir+'/'+fname+'.pck')
                  plotters[-1].addCorrectionFactor('xsec','tree')
                  plotters[-1].addCorrectionFactor('genWeight','tree')
                  plotters[-1].addCorrectionFactor('puWeight','tree')
                  # if period == 2017:
 #                      plotters[-1].addCorrectionFactor('jj_triggerWeight','tree')
 #                  else:
 #                      plotters[-1].addCorrectionFactor('triggerWeight','tree')
                      
                  plotters[-1].addCorrectionFactor(corr,'flat')                  
    return  plotters

def doHist(f,outname,plotter,var,postfix,cut,bins,mini,maxi,title,unit,ytitle,period):
    name =  postfix+"_"+(title.replace("(","").replace(")","").replace("-","_").replace("/","_").replace("#","").replace(" ","_").replace("tau_{21}^{DDT}","DDT").replace("tau_{21}","tau21").replace("{","").replace("}",""))
    h =  plotter.drawTH1(var,cut,"1",bins,mini,maxi,title,unit,"HIST")
    h.SetName(name)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().SetTitle(h.GetXaxis().GetTitle().replace("[]",""))
    return h
    

if __name__ == "__main__":
    
    infile = sys.argv[1]
    outname = sys.argv[2]
    indir  = sys.argv[3]
    if indir.find("16")!=-1: 
        period = 2016
    else:
        period = 2017   
    isData = False
    if infile.find("JetHT")!=-1: 
      isData =True
    print "PERIOD IS " , period
    HCALbinsMVV= [1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808]
    HCALbinsMVV= [838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5058,5253,5455,5663,5877,6099,6328,6564,6808]
    xbins = array('d',HCALbinsMVV)
    cat ={}
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
    
    # cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)'
    # cuts['metfilters'] = "(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)"
    # cuts['common'] = '((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>=838&&abs(jj_l1_eta-jj_l2_eta)<=1.3&&jj_l1_softDrop_mass>=55.&&jj_l2_softDrop_mass>=55.&&jj_l1_pt>=200.&&jj_l2_pt>=200.&&abs(jj_l1_eta)<2.5&&abs(jj_l2_eta)<2.5)' #2017: Flag_CSCTightHaloFilter missing
    cuts['HPHP'] = '('+cat['HP1']+'&&'+cat['HP2']+')'
    cuts['LPLP'] = '('+cat['LP1']+'&&'+cat['LP2']+')'
    cuts['HPLP'] = '(('+cat['HP1']+'&&'+cat['LP2']+')||('+cat['LP1']+'&&'+cat['HP2']+'))'
    cuts['NP'] = '(('+cat['LP1']+'&&'+cat['NP2']+')||('+cat['NP1']+'&&'+cat['LP2']+'))'


    cuts['nonres'] = '1'

    purities=['HPHP','HPLP','LPLP','NP']
    purities=['HPHP']

    minMJ=55.0
    maxMJ=215.0

    minMVV=1126.
    maxMVV=7038.0

    minMX=1000.0
    maxMX=7000.0

    binsMJ=80
    binsMVV=100
    binsMVV=len(HCALbinsMVV)-1

    cuts['acceptance']= "(jj_LV_mass>{minMVV}&&jj_LV_mass<{maxMVV}&&jj_l1_softDrop_mass>={minMJ}&&jj_l1_softDrop_mass<={maxMJ}&&jj_l2_softDrop_mass>={minMJ}&&jj_l2_softDrop_mass<={maxMJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJ=minMJ,maxMJ=maxMJ)
    
    
    plotters = getPlotters(indir,infile,isData,period)
    plotter  = MergedPlotter(plotters)

    hists =[]
    # for p in purities:
    #   print "Plotting variables for category %s" %(p)
    #   cut='*'.join([cuts['common'],cuts['metfilters'],cuts[p],cuts['acceptance']])
    #   postfix = p
      # h1 = doHist(infile,outname,plotter,'jj_l1_softDrop_mass',postfix,cut,32,55.,215.,'Jet 1 softdrop mass',"GeV","Events / 5 GeV")       ; hists.append(h1);
      # h2 = doHist(infile,outname,plotter,'jj_l2_softDrop_mass',postfix,cut,32,55.,215.,'Jet 2 softdrop mass',"GeV","Events / 5 GeV"); hists.append(h2);
      # # h3 = doHist(infile,outname,plotter,'jj_l1_mass',postfix,cut,32,55.,215.,'Jet 1 mass',"GeV","Events / 5 GeV")    ; hists.append(h3);
      # # h4 = doHist(infile,outname,plotter,'jj_l2_mass',postfix,cut,32,55.,215.,'Jet 2 mass',"GeV","Events / 5 GeV")        ; hists.append(h4);
      # h5 = doHist(infile,outname,plotter,'jj_LV_mass',postfix,cut,62,838.,7038.,'Dijet invariant mass',"GeV","Events / 100 GeV")    ; hists.append(h5);
      # # h  = doHist(infile,outname,plotter,'abs(jj_l1_eta-jj_l2_eta)',postfix,cut,15,0.,1.5,'#Delta#eta',"","Events / 0.1")            ; hists.append(h);


    postfix = "looseSel"
    cut='*'.join([cuts['common'],cuts['metfilters'],cuts['acceptance']])
    h = doHist(infile,outname,plotter,'jj_l1_softDrop_mass',postfix,cut,80,55.,215.,'Jet 1 softdrop mass',"GeV","Events / 2 GeV", period) ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_softDrop_mass',postfix,cut,80,55.,215.,'Jet 2 softdrop mass',"GeV","Events / 2 GeV", period) ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_LV_mass',postfix,cut,6000,1126.,7126.,'Dijet invariant mass',"GeV","Events / 1 GeV",period)     ; hists.append(h);
    h = doHist(infile,outname,plotter,'(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))',postfix,cut,24,0.,1.2,'Jet 1 #tau_{21}^{DDT}','',"Events / 0.05", period); hists.append(h);
    h = doHist(infile,outname,plotter,'(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))',postfix,cut,24,0.,1.2,'Jet 2 #tau_{21}^{DDT}','',"Events / 0.05", period); hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_tau2/jj_l1_tau1',postfix,cut,20,0.,1.,'Jet 1 #tau_{21}',"","Events / 0.05", period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_tau2/jj_l2_tau1',postfix,cut,20,0.,1.,'Jet 2 #tau_{21}',"","Events / 0.05", period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_phi',postfix,cut,25,-2.5,2.5,'Jet 1 #phi',"","Events / 0.2", period)   ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_phi',postfix,cut,25,-2.5,2.5,'Jet 2 #phi',"","Events / 0.2", period)   ; hists.append(h);
    h = doHist(infile,outname,plotter,'abs(jj_l1_eta-jj_l2_eta)',postfix,cut,15,0.,1.5,'#Delta#eta',"","Events / 0.1",period)   ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_pt',postfix,cut,36,200.,2000.,'Jet 1 p_{T}',"GeV","Events / 50 GeV",period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_pt',postfix,cut,36,200.,2000.,'Jet 2 p_{T}',"GeV","Events / 50 GeV",period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_eta',postfix,cut,25,-2.5,2.5,'Jet 1 #eta',"","Events / 0.2",period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_eta',postfix,cut,25,-2.5,2.5,'Jet 2 #eta',"","Events / 0.2",period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_tau2',postfix,cut,20,0.,1.,'Jet 1 #tau_{2}',"","Events / 0.05", period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_tau2',postfix,cut,20,0.,1.,'Jet 2 #tau_{2}',"","Events / 0.05", period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l1_tau1',postfix,cut,20,0.,1.,'Jet 1 #tau_{1}',"","Events / 0.05", period)    ; hists.append(h);
    h = doHist(infile,outname,plotter,'jj_l2_tau1',postfix,cut,20,0.,1.,'Jet 2 #tau_{1}',"","Events / 0.05", period)    ; hists.append(h);

    f = ROOT.TFile(outname,"RECREATE")
    f.cd()
    for h in hists:
      h.Write()
    f.Write()
    f.Close()  

    print "Execution time: " ,datetime.now() - startTime

