import ROOT
import os,sys,optparse
from array import array




parser = optparse.OptionParser()
parser.add_option("-s","--sorting",dest="sorting",default='tau21DDT',help="sort after variable")
parser.add_option("-f","--file",dest="file",help="file to sort",default='')
parser.add_option("-o","--output",dest="output",help="label to add to output tree name",default='tau21DDT_')
parser.add_option("-d","--dir",dest="outdir",help="write output tree in directory outdir",default='/storage/b/psi_data/samples3DFit/')
parser.add_option("-p","--pdf",dest="pdf",help="split trees after starting partons ",default="")


(options,args) = parser.parse_args()




def selectJets(puppi_pt,puppi_eta,puppi_tightID,puppi_N):
    if puppi_N < 2:
        return [0]
    if puppi_tightID[0]==0:
        return [0]
    jets = []
    for i in range(0,puppi_N):
        if puppi_pt[i] <= 200: continue
        if abs(puppi_eta[i]) >= 2.5: continue
        if puppi_tightID[i] == 0: continue
        jets.append(i)
    if len(jets)<2:
        return [0]
    if abs(puppi_eta[jets[0]]-puppi_eta[jets[1]]) > 1.3: 
        return [0]
    return [jets[0],jets[1]]


def makeLV(pt,eta,phi,e,j1,j2):
    W1 = ROOT.TLorentzVector()
    W1.SetPtEtaPhiE(pt[j1],eta[j1],phi[j1],e[j1])
    W2 = ROOT.TLorentzVector()
    W2.SetPtEtaPhiE(pt[j2],eta[j2],phi[j2],e[j2])
    return [W1+W2,W1,W2]

def massCut(X,sdmass1,sdmass2):
    if X.M() < 1000:
        return 0
    if sdmass1 > 215:
        return 0
    if sdmass1 < 55:
        return 0
    if sdmass2 > 215:
        return 0
    if sdmass2 < 55:
        return 0
    return 1



def ApplyPuppiSoftdropMassCorrections(puppiJet,m_puppisd_corr,sdmass):
 genCorr = m_puppisd_corr[0].Eval(puppiJet.Pt());
 recoCorr = 1;
 if abs(puppiJet.Eta()) <= 1.3: recoCorr = m_puppisd_corr[1].Eval(puppiJet.Pt())
 else: recoCorr = m_puppisd_corr[2].Eval(puppiJet.Pt())
 return sdmass*genCorr*recoCorr



def matchPuppiJet(W1,W2,puppi):
  nPUPPIjets = len(puppi.jetAK8_puppi_pt)
  puppiMatch =[]
  if (nPUPPIjets < 2): return [-1,-1]
  for W in [W1,W2]:
    for i in range(0,nPUPPIjets):
        if len(puppiMatch) == 2: return puppiMatch
    # Match to puppi jet
        dRmin = 99.
    
        mypuppijet  = ROOT.TLorentzVector()
        mypuppijet.SetPtEtaPhiE(puppi.jetAK8_puppi_pt[i],puppi.jetAK8_puppi_eta[i],puppi.jetAK8_puppi_phi[i],puppi.jetAK8_puppi_e[i])
     
        dR = W.DeltaR(mypuppijet);
        if ( dR > dRmin ): continue
        samePuppiJet =0

        for m in range(len(puppiMatch)):
           if (i == puppiMatch[m]): samePuppiJet=1
      

        if (samePuppiJet ==1): continue
        puppiMatch.append(i)
        dRmin = dR
    return puppiMatch



def findGenJets(goodFatJets,genjets):
  #Match to gen jet
  puppiMatch =[]
  for i in range(0,len(goodFatJets)):
      dRmin = 99.
      jetIdx = 99;
      for j in range(0,len(genjets.genJetAK8_pt)):
        gen = ROOT.TLorentzVector()
        gen.SetPtEtaPhiE(genjets.genJetAK8_pt[j],genjets.genJetAK8_eta[j],genjets.genJetAK8_phi[j],genjets.genJetAK8_e[j])
        if ( genjets.genJetAK8_pt[j] < 50. ): continue
        dR = gen.DeltaR(goodFatJets[i]);
        if ( dR > dRmin ): continue;
        dRmin = dR
        jetIdx = j
        samePuppiJet =0;

        for m in range(len(puppiMatch)):
          if (j == puppiMatch[m]): samePuppiJet=1
        if samePuppiJet==1: continue
        puppiMatch.append(jetIdx)
       
  return puppiMatch
  

  
  
  






if __name__=="__main__":
    # define histos 
    
    h_muf       = ROOT.TH1F("hmuf","hmuf",50,0,0.06)
    h_phf       = ROOT.TH1F("hphf","hphf",50,0,1)
    h_emf       = ROOT.TH1F("hemf","hemf",50,0,0.06)
    h_chf       = ROOT.TH1F("hchf","hchf",50,0,1)
    h_nhf       = ROOT.TH1F("hnhf","hnhf",50,0,0.06)
    h_area      =ROOT.TH1F("harea","harea",50,0.5,3.5)
    h_cm        =   ROOT.TH1F("hcm","hcm",50,0,200)
    h_nm        = ROOT.TH1F("hmn" ,"hnm" ,50,0,200)
    h_che       = ROOT.TH1F("hche","hche",50,0,3500)
    h_ne        = ROOT.TH1F("hne","hne",50,0,4100)
    h_hof       = ROOT.TH1F("hhof","hhof",50,0,0.4)
    h_chm       = ROOT.TH1F("hchm","hchm",50,0,200)
    h_neHadMult = ROOT.TH1F("hneHadMult","hneHadMult",50,0,25)
    h_nemf      = ROOT.TH1F("hnemf","hnemf",50,0,1)
    h_cemf      = ROOT.TH1F("hcemf","hcemf",50,0,0.06)
    h_phoMult   = ROOT.TH1F("hphoMult","hphoMult",50,0,100)
    
    
    
    test_h_muf = ROOT.TH1F("testhmuf" ,"testhmuf",50,0,0.06)
    test_h_phf = ROOT.TH1F("testhphf" ,"testhphf",50,0,1)
    test_h_emf = ROOT.TH1F("testhemf" ,"testhemf",50,0,0.06)
    test_h_chf = ROOT.TH1F("testhchf" ,"testhchf",50,0,1)
    test_h_nhf = ROOT.TH1F("testhnhf" ,"testhnhf",50,0,0.06)
    test_h_area= ROOT.TH1F("testharea","testharea",50,0.5,3.5)
    test_h_cm  = ROOT.TH1F("testhcm"  ,"testhcm",50,0,200)
    test_h_nm  = ROOT.TH1F("testhmn"  ,"testhnm" ,50,0,200)
    test_h_che = ROOT.TH1F("testhche" ,"testhche",50,0,3500)
    test_h_ne =  ROOT.TH1F("testhne"  ,"testhne",50,0,4100)
    test_h_hof = ROOT.TH1F("testhhof" ,"testhhof",50,0,0.4)
    test_h_chm = ROOT.TH1F("testhchm", "testhchm",50,0,200)
    test_h_neHadMult = ROOT.TH1F("testhneHadMult","testhneHadMult",50,0,25)
    test_h_nemf = ROOT.TH1F("testhnemf","testhnemf",50,0,1)
    test_h_cemf = ROOT.TH1F("testhcemf","testhcemf",50,0,0.06)
    test_h_phoMult = ROOT.TH1F("testhphoMult","testhphoMult",50,0,100)
        
    
    nEvents =0
    # end define histos
    
    sd_mass_weights_file = ROOT.TFile("puppiCorr.root","READ")
    w0 = sd_mass_weights_file.Get("puppiJECcorr_gen")
    w1 = sd_mass_weights_file.Get("puppiJECcorr_reco_0eta1v3")
    w2 = sd_mass_weights_file.Get("puppiJECcorr_reco_1v3eta2v5")
    sd_mass_weights = [w0,w1,w2]

    tree = ROOT.TChain("ntuplizer/tree")
    for level1 in os.listdir(args[0]):
      if level1.find(options.file)!=-1 and level1.find(options.output)==-1:
        for level2 in os.listdir(args[0]+level1):
            for level3 in os.listdir(args[0]+level1+"/"+level2):
                for level4 in os.listdir(args[0]+level1+"/"+level2+"/"+level3):
                    for filename in os.listdir(args[0]+level1+"/"+level2+"/"+level3+"/"+level4):
                        print filename
        
                        tree.Add(args[0]+level1+"/"+level2+"/"+level3+"/"+level4+"/"+filename)
    
    #h_chf = ROOT.TH1F("chf","chf",50,,)
    events =0
    passevents=0
    for event in tree:
         nEvents+=1
         jets = selectJets(event.jetAK8_pt,event.jetAK8_eta,event.jetAK8_IDTight,event.jetAK8_N)
         if len(jets) < 2:
                #print len(jets)
            continue
         [X,W1,W2] = makeLV(event.jetAK8_pt,event.jetAK8_eta,event.jetAK8_phi,event.jetAK8_e,jets[0],jets[1])
         if ROOT.TMath.Abs( (W1.Eta() - W2.Eta() )  > 1.3 ):
             continue
         puppijets = matchPuppiJet(W1,W2,event)
         if len(puppijets)<2: continue
         [puppi_X,puppi_W1,puppi_W2] = makeLV(event.jetAK8_puppi_pt,event.jetAK8_puppi_eta,event.jetAK8_puppi_phi,event.jetAK8_puppi_e,puppijets[0],puppijets[1])
     
         sdmassCorr1 = ApplyPuppiSoftdropMassCorrections(puppi_W1,sd_mass_weights,event.jetAK8_puppi_softdrop_mass[puppijets[0]])
         sdmassCorr2 = ApplyPuppiSoftdropMassCorrections(puppi_W2,sd_mass_weights,event.jetAK8_puppi_softdrop_mass[puppijets[1]])
         if massCut(X,sdmassCorr1,sdmassCorr2)==0:
                continue
    
    
         #print "jets :"
         #print jets
         #print W1.Pt()
         #print W1.Eta()
         #print event.jetAK8_IDTight[jets[0]].Print()
         #print "------------------------"
         #print W2.Pt()
         #print W2.Eta()
         #print event.jetAK8_IDTight[jets[1]]
         
         #print "puppi"
         #print puppijets
         #print puppi_W1.Pt()
         genjets = findGenJets([W1,W2],event)
         #print "genjets"
         #print genjets
         
        
         if sdmassCorr1 > 55 and sdmassCorr2 > 55 and event.genJetAK8_softdropmass[genjets[0]] > 10 and event.genJetAK8_softdropmass[genjets[1]] > 10 :
              h_muf       .Fill(event.jetAK8_muf      [jets[0]])
              h_phf       .Fill(event.jetAK8_phf      [jets[0]])
              h_emf       .Fill(event.jetAK8_emf      [jets[0]])
              h_chf       .Fill(event.jetAK8_chf      [jets[0]])
              h_nhf       .Fill(event.jetAK8_nhf      [jets[0]])
              h_area      .Fill(event.jetAK8_area     [jets[0]])
              h_cm        .Fill(event.jetAK8_cm       [jets[0]])
              h_nm        .Fill(event.jetAK8_nm       [jets[0]])
              h_che       .Fill(event.jetAK8_muf      [jets[0]])
              h_ne        .Fill(event.jetAK8_ne       [jets[0]])
              h_hof       .Fill(event.jetAK8_hof      [jets[0]])
              h_chm       .Fill(event.jetAK8_chm      [jets[0]])
              h_neHadMult .Fill(event.jetAK8_neHadMult[jets[0]])
              h_nemf      .Fill(event.jetAK8_nemf     [jets[0]])
              h_cemf      .Fill(event.jetAK8_cemf     [jets[0]])
              h_phoMult   .Fill(event.jetAK8_phoMult  [jets[0]])
              
         else:
            if event.genJetAK8_softdropmass[genjets[0]] < 10 and   sdmassCorr1 > 55:
                test_h_muf       .Fill(event.jetAK8_muf      [jets[0]])
                test_h_phf       .Fill(event.jetAK8_phf      [jets[0]])
                test_h_emf       .Fill(event.jetAK8_emf      [jets[0]])
                test_h_chf       .Fill(event.jetAK8_chf      [jets[0]])
                test_h_nhf       .Fill(event.jetAK8_nhf      [jets[0]])
                test_h_area      .Fill(event.jetAK8_area     [jets[0]])
                test_h_cm        .Fill(event.jetAK8_cm       [jets[0]])
                test_h_nm        .Fill(event.jetAK8_nm       [jets[0]])
                test_h_che       .Fill(event.jetAK8_muf      [jets[0]])
                test_h_ne        .Fill(event.jetAK8_ne       [jets[0]])
                test_h_hof       .Fill(event.jetAK8_hof      [jets[0]])
                test_h_chm       .Fill(event.jetAK8_chm      [jets[0]])
                test_h_neHadMult .Fill(event.jetAK8_neHadMult[jets[0]])
                test_h_nemf      .Fill(event.jetAK8_nemf     [jets[0]])
                test_h_cemf      .Fill(event.jetAK8_cemf     [jets[0]])
                test_h_phoMult   .Fill(event.jetAK8_phoMult  [jets[0]])
            if event.genJetAK8_softdropmass[genjets[1]] < 10 and   sdmassCorr2 > 55:    
                test_h_muf       .Fill(event.jetAK8_muf      [jets[1]])
                test_h_phf       .Fill(event.jetAK8_phf      [jets[1]])
                test_h_emf       .Fill(event.jetAK8_emf      [jets[1]])
                test_h_chf       .Fill(event.jetAK8_chf      [jets[1]])
                test_h_nhf       .Fill(event.jetAK8_nhf      [jets[1]])
                test_h_area      .Fill(event.jetAK8_area     [jets[1]])
                test_h_cm        .Fill(event.jetAK8_cm       [jets[1]])
                test_h_nm        .Fill(event.jetAK8_nm       [jets[1]])
                test_h_che       .Fill(event.jetAK8_muf      [jets[1]])
                test_h_ne        .Fill(event.jetAK8_ne       [jets[1]])
                test_h_hof       .Fill(event.jetAK8_hof      [jets[1]])
                test_h_chm       .Fill(event.jetAK8_chm      [jets[1]])
                test_h_neHadMult .Fill(event.jetAK8_neHadMult[jets[1]])
                test_h_nemf      .Fill(event.jetAK8_nemf     [jets[1]])
                test_h_cemf      .Fill(event.jetAK8_cemf     [jets[1]])
                test_h_phoMult   .Fill(event.jetAK8_phoMult  [jets[1]])
        
         #if nEvents >= 10000: break
        
                
    outfile = ROOT.TFile("histos_jetProperties.root","RECREATE")
    h_muf       .Write()
    h_phf       .Write()
    h_emf       .Write()
    h_chf       .Write()
    h_nhf       .Write()
    h_area      .Write()
    h_cm        .Write()
    h_nm        .Write()
    h_che       .Write()
    h_ne        .Write()
    h_hof       .Write()
    h_chm       .Write()
    h_neHadMult .Write()
    h_nemf      .Write()
    h_cemf      .Write()
    h_phoMult   .Write()
    
    test_h_muf       .Write()
    test_h_phf       .Write()
    test_h_emf       .Write()
    test_h_chf       .Write()
    test_h_nhf       .Write()
    test_h_area      .Write()
    test_h_cm        .Write()
    test_h_nm        .Write()
    test_h_che       .Write()
    test_h_ne        .Write()
    test_h_hof       .Write()
    test_h_chm       .Write()
    test_h_neHadMult .Write()
    test_h_nemf      .Write()
    test_h_cemf      .Write()
    test_h_phoMult   .Write()
