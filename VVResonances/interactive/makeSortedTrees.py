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


def sortTau21DDT(tau21_l1,mass_l1,pt_l1,tau21_l2,mass_l2,pt_l2):
    tau21_l1_ddt = tau21_l1 +(0.082*ROOT.TMath.Log((mass_l1*mass_l1)/pt_l1))
    tau21_l2_ddt = tau21_l2 +(0.082*ROOT.TMath.Log((mass_l2*mass_l2)/pt_l2))                
    if tau21_l1_ddt > tau21_l2_ddt:
        return 1
    return 0




def   splitTrees(ID,l1_mcFlavour,l2_mcFlavour):
      if ID == "gg":
          if ROOT.TMath.Abs(l1_mcFlavour)==21 and ROOT.TMath.Abs(l2_mcFlavour)==21:
             return 1
          else:
             return 0
      if ID=="qg":
          if (ROOT.TMath.Abs(l1_mcFlavour)==21 and ROOT.TMath.Abs(l2_mcFlavour) <=6) or (ROOT.TMath.Abs(l2_mcFlavour)==21 and ROOT.TMath.Abs(l1_mcFlavour) <=6):
              return 1
          else:
              return 0

      if ID =="qq":
          if (ROOT.TMath.Abs(l1_mcFlavour)<=6 and ROOT.TMath.Abs(l2_mcFlavour) <=6):
              return 1
          else:
              return 0
          
          
          
          
def printEvent(event):
    if (event.jj_l1_softDrop_mass <= 70 and event.jj_l1_softDrop_mass >=55) or (event.jj_l2_softDrop_mass <= 70 and event.jj_l2_softDrop_mass >=55):
        print str(event.evt)+" :"
        print "mass "+str(event.jj_LV_mass) +" gen "+str(event.jj_gen_partialMass)
        print "jet1 mass "+str(event.jj_l1_softDrop_mass)+" gen "+str(event.jj_l1_gen_softDrop_mass)
        print "jet2 mass "+str(event.jj_l2_softDrop_mass)+" gen "+str(event.jj_l1_gen_softDrop_mass)


if __name__=="__main__":
    period = 2017
    ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
    from ROOT import rootint
    ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
    from ROOT import rootfloat
    ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
    from ROOT import rootlong
    #tree = ROOT.TChain("tree")
    for filename in os.listdir(args[0]):
      if filename.find(options.file)!=-1 and filename.find(options.output)==-1:
        if filename.find("tau21")!=-1: continue
        #tree.Add(args[0]+filename)
        f = ROOT.TFile(args[0]+filename,"READ")
        tree = f.Get("tree")
        print "save output under "+options.output+filename
        fout = ROOT.TFile(options.outdir+options.output+filename,"RECREATE")
        sortedTree = ROOT.TTree("tree","tree")
        run = rootint()
        lumi = rootint()
        puWeight  = rootfloat()
        genWeight = rootfloat()
        xsec      = rootfloat()
        evt       = rootlong()
        
        
        HLT_JJ                       = rootint()
        Flag_HBHENoiseFilter         = rootint()
        Flag_HBHENoiseIsoFilter      = rootint()
        Flag_CSCTightHaloFilter      = rootint()
        Flag_goodVertices            = rootint()
        Flag_eeBadScFilter           = rootint()
        njj                          = rootint()
        jj_l2_mergedVTruth           = array("i",[0])
        jj_l1_mergedVTruth           = array("i",[0])
        jj_nJets                     = array("i",[0])
        jj_nOtherLeptons             = array("i",[0])
        
        
        jj_l1_rho                  = array("f",[0])
        jj_l2_rho                  = array("f",[0])
        jj_l1_gen_rho              = array("f",[0])
        jj_l2_gen_rho              = array("f",[0])
        
        jj_l2_softDrop_mass        = array("f",[0])
        jj_l2_pt                   = array("f",[0])
        jj_l2_eta                  = array("f",[0])
        jj_l2_phi                  = array("f",[0])
        jj_l2_tau1                 = array("f",[0])
        jj_l2_tau2                 = array("f",[0])
        jj_l2_tau21_DDT            = array("f",[0])
        jj_l2_gen_tau1             = array("f",[0])
        jj_l2_gen_tau2             = array("f",[0])
        jj_l2_gen_pt               = array("f",[0])
        jj_l2_gen_eta              = array("f",[0])
        jj_l2_gen_phi              = array("f",[0])
        jj_l2_gen_mass             = array("f",[0])
        jj_l2_gen_softDrop_mass    = array("f",[0])
        jj_l1_softDrop_mass        = array("f",[0])
        jj_l1_pt                   = array("f",[0])
        jj_l1_eta                  = array("f",[0])
        jj_l1_phi                  = array("f",[0])
        jj_l1_tau1                 = array("f",[0])
        jj_l1_tau2                 = array("f",[0])
        jj_l1_tau21_DDT            = array("f",[0])
        jj_l1_gen_tau1             = array("f",[0])
        jj_l1_gen_tau2             = array("f",[0])
        jj_l1_gen_pt               = array("f",[0])
        jj_l1_gen_eta              = array("f",[0])
        jj_l1_gen_phi              = array("f",[0])
        jj_l1_gen_mass             = array("f",[0])
        jj_l1_gen_softDrop_mass    = array("f",[0])
        jj_LV_pt                   = array("f",[0])
        jj_LV_eta                  = array("f",[0])
        jj_LV_phi                  = array("f",[0])
        jj_LV_mass                 = array("f",[0])
        jj_gen_partialMass         = array("f",[0])
        
        
        # define branches ################
        sortedTree.Branch("run",run,"run/i")
        sortedTree.Branch("HLT_JJ",(HLT_JJ),"HLT_JJ/I")
        sortedTree.Branch("lumi",lumi,"lumi/i")
        sortedTree.Branch("evt",evt,"evt/l")
        sortedTree.Branch("xsec",(xsec),"xsec/F")        
        sortedTree.Branch("puWeight",(puWeight),"puWeight/F")                 
        sortedTree.Branch("genWeight",(genWeight),"genWeight/F")
        sortedTree.Branch("Flag_HBHENoiseIsoFilter", (Flag_HBHENoiseIsoFilter),"Flag_HBHENoiseIsoFilter/I") 
        sortedTree.Branch("Flag_CSCTightHaloFilter", (Flag_CSCTightHaloFilter),"Flag_CSCTightHaloFilter/I") 
        sortedTree.Branch("Flag_HBHENoiseFilter", (Flag_HBHENoiseFilter),"Flag_HBHENoiseFilter/I")
        sortedTree.Branch("Flag_goodVertices", (Flag_goodVertices),"Flag_goodVertices/I")
        sortedTree.Branch("Flag_eeBadScFilter", (Flag_eeBadScFilter),"Flag_eeBadScFilter/I")
        sortedTree.Branch("njj", (njj),"njj/I   ")
         
       
       
        sortedTree.Branch("jj_nJets", (jj_nJets),"jj_nJets/I")
        sortedTree.Branch("jj_nOtherLeptons", (jj_nOtherLeptons),"jj_nOtherLeptons/I")
        sortedTree.Branch("jj_LV_pt", (jj_LV_pt),"jj_LV_pt/F")
        sortedTree.Branch("jj_LV_eta", (jj_LV_eta),"jj_LV_eta/F")
        sortedTree.Branch("jj_LV_phi", (jj_LV_phi),"jj_LV_phi/F")
        sortedTree.Branch("jj_LV_mass", (jj_LV_mass),"jj_LV_mass/F")
        sortedTree.Branch("jj_gen_partialMass", (jj_gen_partialMass),"jj_gen_partialMass/F")
        sortedTree.Branch("jj_l1_softDrop_mass", (jj_l1_softDrop_mass),"jj_l1_softDrop_mass/F")
        sortedTree.Branch("jj_l1_pt", (jj_l1_pt),"jj_l1_pt/F")
        sortedTree.Branch("jj_l1_eta", (jj_l1_eta),"jj_l1_eta/F")
        sortedTree.Branch("jj_l1_phi", (jj_l1_phi),"jj_l1_phi/F")
        sortedTree.Branch("jj_l1_tau1", (jj_l1_tau1),"jj_l1_tau1/F")
        sortedTree.Branch("jj_l1_tau2", (jj_l1_tau2),"jj_l1_tau2/F")
        sortedTree.Branch("jj_l1_tau21_DDT", (jj_l1_tau21_DDT),"jj_l1_tau21_DDT/F")
        sortedTree.Branch("jj_l1_mergedVTruth", (jj_l1_mergedVTruth),"jj_l1_mergedVTruth/I")
        sortedTree.Branch("jj_l1_gen_tau1", (jj_l1_gen_tau1),"jj_l1_gen_tau1/F")
        sortedTree.Branch("jj_l1_gen_tau2", (jj_l1_gen_tau2),"jj_l1_gen_tau2/F")
        sortedTree.Branch("jj_l1_gen_pt", (jj_l1_gen_pt),"jj_l1_gen_pt/F")
        sortedTree.Branch("jj_l1_gen_eta", (jj_l1_gen_eta),"jj_l1_gen_eta/F")
        sortedTree.Branch("jj_l1_gen_phi", (jj_l1_gen_phi),"jj_l1_gen_phi/F")
        sortedTree.Branch("jj_l1_gen_mass", (jj_l1_gen_mass),"jj_l1_gen_mass/F")
        sortedTree.Branch("jj_l1_gen_softDrop_mass", (jj_l1_gen_softDrop_mass),"jj_l1_gen_softDrop_mass/F")
        sortedTree.Branch("jj_l1_rho", (jj_l1_rho),"jj_l1_rho/F")
        sortedTree.Branch("jj_l1_gen_rho", (jj_l1_gen_rho),"jj_l1_gen_rho/F")
        
        sortedTree.Branch("jj_l2_gen_rho", (jj_l2_gen_rho),"jj_l2_gen_rho/F")
        sortedTree.Branch("jj_l2_rho", (jj_l2_rho),"jj_l2_rho/F")
        sortedTree.Branch("jj_l2_softDrop_mass",jj_l2_softDrop_mass,"jj_l2_softDrop_mass/F")
        sortedTree.Branch("jj_l2_pt", (jj_l2_pt),"jj_l2_pt/F")
        sortedTree.Branch("jj_l2_eta", (jj_l2_eta),"jj_l2_eta/F")
        sortedTree.Branch("jj_l2_phi", (jj_l2_phi),"jj_l2_phi/F")
        sortedTree.Branch("jj_l2_tau1", (jj_l2_tau1),"jj_l2_tau1/F")
        sortedTree.Branch("jj_l2_tau2", (jj_l2_tau2),"jj_l2_tau2/F")
        sortedTree.Branch("jj_l2_tau21_DDT", (jj_l2_tau21_DDT),"jj_l2_tau21_DDT/F")
        sortedTree.Branch("jj_l2_mergedVTruth", (jj_l2_mergedVTruth),"jj_l2_mergedVTruth/I")
        sortedTree.Branch("jj_l2_gen_tau1", (jj_l2_gen_tau1),"jj_l2_gen_tau1/F")
        sortedTree.Branch("jj_l2_gen_tau2", (jj_l2_gen_tau2),"jj_l2_gen_tau2/F")
        sortedTree.Branch("jj_l2_gen_pt", (jj_l2_gen_pt),"jj_l2_gen_pt/F")
        sortedTree.Branch("jj_l2_gen_eta", (jj_l2_gen_eta),"jj_l2_gen_eta/F")
        sortedTree.Branch("jj_l2_gen_phi", (jj_l2_gen_phi),"jj_l2_gen_phi/F")
        sortedTree.Branch("jj_l2_gen_mass", (jj_l2_gen_mass),"jj_l2_gen_mass/F")
        sortedTree.Branch("jj_l2_gen_softDrop_mass", (jj_l2_gen_softDrop_mass),"jj_l2_gen_softDrop_mass/F")
        
        
        
            
            
        for event in tree:
            #print event.jj_l1_mcFlavour[0]
            #print event.jj_l2_mcFlavour[0]
            printEvent(event)
            #if splitTrees(options.pdf,event.jj_l1_mcFlavour[0],event.jj_l2_mcFlavour[0]) ==0:
            #    continue
            
            if event.jj_l1_pt[0] ==0 or event.jj_l2_pt[0] ==0 or event.jj_l1_gen_pt[0] ==0 or event.jj_l2_gen_pt[0] == 0:
                continue
            run.ri = event.run          
            HLT_JJ.ri                  = event.HLT_JJ                 
            Flag_HBHENoiseFilter   .ri = event.Flag_HBHENoiseFilter     
            Flag_HBHENoiseIsoFilter.ri = event.Flag_HBHENoiseIsoFilter
            if period == 2017:
                 Flag_CSCTightHaloFilter.ri = event.Flag_globalTightHalo2016Filter
            else:
                Flag_CSCTightHaloFilter.ri = event.Flag_CSCTightHaloFilter  
            Flag_goodVertices      .ri = event.Flag_goodVertices        
            Flag_eeBadScFilter     .ri = event.Flag_eeBadScFilter       
            njj .ri                    = event.njj                     
            jj_l2_mergedVTruth      [0] = event.jj_l2_mergedVTruth       [0]
            jj_l1_mergedVTruth      [0] = event.jj_l1_mergedVTruth       [0]
            jj_nJets                [0] = event.jj_nJets                 [0]
            jj_nOtherLeptons        [0] = event.jj_nOtherLeptons         [0]
            
            puWeight.rf       = event.puWeight 
            genWeight.rf      = event.genWeight
            xsec.rf           = event.xsec     
            evt.rl            = event.evt                  
            lumi.ri           = event.lumi
            
            #print event.xsec

            #if sortTau21DDT( event.jj_l1_tau2[0]/event.jj_l1_tau1[0],event.jj_l1_softDrop_mass[0],event.jj_l1_pt[0], event.jj_l2_tau2[0]/event.jj_l2_tau1[0],event.jj_l2_softDrop_mass[0],event.jj_l2_pt[0])==1:
            jj_l2_softDrop_mass     [0] =    event.jj_l2_softDrop_mass      [0]    
            jj_l2_pt                [0] =    event.jj_l2_pt                 [0]
            jj_l2_eta               [0] =    event.jj_l2_eta                [0]
            jj_l2_phi               [0] =    event.jj_l2_phi                [0]
            jj_l2_tau1              [0] =    event.jj_l2_tau1               [0]
            jj_l2_tau2              [0] =    event.jj_l2_tau2               [0]
            jj_l2_tau21_DDT         [0] =    event.jj_l2_tau21_DDT          [0]
            jj_l2_gen_tau1          [0] =    event.jj_l2_gen_tau1           [0]
            jj_l2_gen_tau2          [0] =    event.jj_l2_gen_tau2           [0]
            jj_l2_gen_pt            [0] =    event.jj_l2_gen_pt             [0]
            jj_l2_gen_eta           [0] =    event.jj_l2_gen_eta            [0]
            jj_l2_gen_phi           [0] =    event.jj_l2_gen_phi            [0]
            jj_l2_gen_mass          [0] =    event.jj_l2_gen_mass           [0]
            jj_l2_gen_softDrop_mass [0] =    event.jj_l2_gen_softDrop_mass  [0]
            
            jj_l1_softDrop_mass     [0] =    event.jj_l1_softDrop_mass      [0]
            jj_l1_pt                [0] =    event.jj_l1_pt                 [0]
            jj_l1_eta               [0] =    event.jj_l1_eta                [0]
            jj_l1_phi               [0] =    event.jj_l1_phi                [0]
            jj_l1_tau1              [0] =    event.jj_l1_tau1               [0]
            jj_l1_tau2              [0] =    event.jj_l1_tau2               [0]
            jj_l1_tau21_DDT         [0] =    event.jj_l1_tau21_DDT          [0]
            jj_l1_gen_tau1          [0] =    event.jj_l1_gen_tau1           [0]
            jj_l1_gen_tau2          [0] =    event.jj_l1_gen_tau2           [0]
            jj_l1_gen_pt            [0] =    event.jj_l1_gen_pt             [0]
            jj_l1_gen_eta           [0] =    event.jj_l1_gen_eta            [0]
            jj_l1_gen_phi           [0] =    event.jj_l1_gen_phi            [0]
            jj_l1_gen_mass          [0] =    event.jj_l1_gen_mass           [0]
            jj_l1_gen_softDrop_mass [0] =    event.jj_l1_gen_softDrop_mass  [0]
            #else:
                #jj_l2_softDrop_mass     [0] =    event.jj_l1_softDrop_mass      [0]    
                #jj_l2_pt                [0] =    event.jj_l1_pt                 [0]
                #jj_l2_eta               [0] =    event.jj_l1_eta                [0]
                #jj_l2_phi               [0] =    event.jj_l1_phi                [0]
                #jj_l2_tau1              [0] =    event.jj_l1_tau1               [0]
                #jj_l2_tau2              [0] =    event.jj_l1_tau2               [0]
                #jj_l2_tau21_DDT         [0] =    event.jj_l1_tau21_DDT          [0]
                #jj_l2_gen_tau1          [0] =    event.jj_l1_gen_tau1           [0]
                #jj_l2_gen_tau2          [0] =    event.jj_l1_gen_tau2           [0]
                #jj_l2_gen_pt            [0] =    event.jj_l1_gen_pt             [0]
                #jj_l2_gen_eta           [0] =    event.jj_l1_gen_eta            [0]
                #jj_l2_gen_phi           [0] =    event.jj_l1_gen_phi            [0]
                #jj_l2_gen_mass          [0] =    event.jj_l1_gen_mass           [0]
                #jj_l2_gen_softDrop_mass [0] =    event.jj_l1_gen_softDrop_mass  [0]
                
                #jj_l1_softDrop_mass     [0] =    event.jj_l2_softDrop_mass      [0]
                #jj_l1_pt                [0] =    event.jj_l2_pt                 [0]
                #jj_l1_eta               [0] =    event.jj_l2_eta                [0]
                #jj_l1_phi               [0] =    event.jj_l2_phi                [0]
                #jj_l1_tau1              [0] =    event.jj_l2_tau1               [0]
                #jj_l1_tau2              [0] =    event.jj_l2_tau2               [0]
                #jj_l1_tau21_DDT         [0] =    event.jj_l2_tau21_DDT          [0]
                #jj_l1_gen_tau1          [0] =    event.jj_l2_gen_tau1           [0]
                #jj_l1_gen_tau2          [0] =    event.jj_l2_gen_tau2           [0]
                #jj_l1_gen_pt            [0] =    event.jj_l2_gen_pt             [0]
                #jj_l1_gen_eta           [0] =    event.jj_l2_gen_eta            [0]
                #jj_l1_gen_phi           [0] =    event.jj_l2_gen_phi            [0]
                #jj_l1_gen_mass          [0] =    event.jj_l2_gen_mass           [0]
                #jj_l1_gen_softDrop_mass [0] =    event.jj_l2_gen_softDrop_mass  [0]
                
            
            
            jj_l1_rho                [0] = ROOT.TMath.Log(event.jj_l1_softDrop_mass[0]*event.jj_l1_softDrop_mass[0]/event.jj_l1_pt[0])
            jj_l2_rho                [0] = ROOT.TMath.Log(event.jj_l2_softDrop_mass[0]*event.jj_l2_softDrop_mass[0]/event.jj_l2_pt[0])
            
            
            jj_l1_gen_rho  [0] = ROOT.TMath.Log(event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0]/event.jj_l1_gen_pt[0])
            jj_l2_gen_rho  [0] = ROOT.TMath.Log(event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0]/event.jj_l2_gen_pt[0])
            
            
            jj_LV_pt                [0] =    event.jj_LV_pt                 [0]
            jj_LV_eta               [0] =    event.jj_LV_eta                [0]
            jj_LV_phi               [0] =    event.jj_LV_phi                [0]
            jj_LV_mass              [0] =    event.jj_LV_mass               [0] 
            jj_gen_partialMass      [0] =    event.jj_gen_partialMass       [0] 
            
            sortedTree.Fill()
        
        f.Close()
        sortedTree.Write()
        fout.Close()
