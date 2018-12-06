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


          
def printEvent(event):
    if (event.jj_l1_softDrop_mass[0] <= 70 and event.jj_l1_softDrop_mass[0] >=55) and (event.jj_l2_softDrop_mass[0] <= 70 and event.jj_l2_softDrop_mass[0] >=55) and event.jj_LV_mass[0] > 5500 and event.jj_LV_mass[0]-event.jj_gen_partialMass[0] > 500:
        print str(event.evt)+" : "+str(event.jj_l1_mcFlavour[0])+" "+str(event.jj_l2_mcFlavour[0])
        print "mass "+str(event.jj_LV_mass[0]) +" gen "+str(event.jj_gen_partialMass[0])
        print "jet1 mass "+str(event.jj_l1_softDrop_mass[0])+" sd corr "+str(event.jj_l1_softDrop_massCorr[0])+" sd l1l2 "+str(event.jj_l1_softDrop_massL2L3[0])+" sd bare "+str(event.jj_l1_softDrop_massBare[0])+" sd sub "+str(event.jj_l1_softDrop_nSubJets[0])+" gen "+str(event.jj_l1_gen_softDrop_mass[0])
        print "rho : "+str(ROOT.TMath.Log(event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0]/(event.jj_l1_gen_pt[0]*event.jj_l1_gen_pt[0])))
        
        print "rho : "+str(ROOT.TMath.Log(event.jj_l1_softDrop_mass[0]*event.jj_l1_softDrop_mass[0]/(event.jj_l1_pt[0]*event.jj_l1_pt[0])))
        
        print "jet2 mass "+str(event.jj_l2_softDrop_mass[0])+" sd corr "+str(event.jj_l2_softDrop_massCorr[0])+" sd l1l2 "+str(event.jj_l2_softDrop_massL2L3[0])+" sd bare "+str(event.jj_l2_softDrop_massBare[0])+" sd sub "+str(event.jj_l2_softDrop_nSubJets[0])+" gen "+str(event.jj_l2_gen_softDrop_mass[0])
        print "rho : "+str(ROOT.TMath.Log(event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0]/(event.jj_l2_gen_pt[0]*event.jj_l2_gen_pt[0])))
        
        print "rho : "+str(ROOT.TMath.Log(event.jj_l2_softDrop_mass[0]*event.jj_l2_softDrop_mass[0]/(event.jj_l2_pt[0]*event.jj_l2_pt[0])))

def makeEventlist(event,listevents):
    if (event.jj_l1_softDrop_mass[0] <= 70 and event.jj_l1_softDrop_mass[0] >=55) and (event.jj_l2_softDrop_mass[0] <= 70 and event.jj_l2_softDrop_mass[0] >=55) and ( event.jj_l1_gen_softDrop_mass[0] < 10 or event.jj_l2_gen_softDrop_mass[0] < 10 ):
        listevents.append(event.evt)


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


def passRecoNotGen(genSDmass,recoSDmass):
    if (genSDmass[0] < 55 and recoSDmass[0] >=55) or (genSDmass[1] < 55 and recoSDmass[1] >=55):
        return 1
    return 0


if __name__=="__main__":
    
    h_rho_gen_l1   = ROOT.TH1F("hrho_gen_l1","hrho_gen_l1",50,-20,20)
    h_rho_l1       = ROOT.TH1F("hrho_l1","hrho_l1",50,-50,0)
    
    h_rho_gen_l2   = ROOT.TH1F("hrho_gen_l2","hrho_gen_l2",50,-20,20)
    h_rho_l2       = ROOT.TH1F("hrho_l2","hrho_l2",50,-20,20)
    
    
    listevents = []
    period = 2017
    ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
    from ROOT import rootint
    ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
    from ROOT import rootfloat
    ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
    from ROOT import rootlong
    tree = ROOT.TChain("tree")
    
    
    numberOfEvents={}
    for filename in os.listdir(args[0]):
      if filename.find(options.file)!=-1 and filename.find(options.output)==-1:
        print filename
        if filename.find(".pck")!=-1:
            continue
        tmpfile = ROOT.TFile(args[0]+filename,"READ")
        tmptree = tmpfile.Get("tree")
        tmptree.GetEntry(1)
        numberOfEvents[tmptree.xsec] = (tmptree.GetEntries())
        tmpfile.Close()
        tree.Add(args[0]+filename)
        
        
        #f = ROOT.TFile(args[0]+filename,"READ")
        #tree = f.Get("tree")
        #print "save output under "+options.output+filename
        #copytree = tree.CopyTree("(TMath::Log(( jj_l1_gen_softDrop_mass * jj_l1_gen_softDrop_mass )/( jj_l1_gen_pt * jj_l1_gen_pt ))<-1.5  && TMath::Log(( jj_l2_gen_softDrop_mass * jj_l2_gen_softDrop_mass )/( jj_l2_gen_pt * jj_l2_gen_pt ))<-1.5)")
     
    print numberOfEvents 
    #h_chf = ROOT.TH1F("chf","chf",50,,)
    events =0
    passevents=0
    
    print tree.GetEntries()
    #print copytree.GetEntries()
    for event in tree:
        if event.jj_l1_gen_pt[0] <=0:
            continue
        if event.jj_l2_gen_pt[0] <=0:
            continue
        
        if event.jj_l1_pt[0] <=0:
            continue
        if event.jj_l2_pt[0] <=0:
            continue
        
        
        if event.jj_l1_softDrop_mass[0] < 55 or event.jj_l2_softDrop_mass[0] < 55 :
            continue
        
        if event.jj_l1_softDrop_mass[0] > 215 or event.jj_l2_softDrop_mass[0] > 215:
            continue
        w = event.xsec/float(numberOfEvents[event.xsec])
        #print w
        h_rho_gen_l1  .Fill(ROOT.TMath.Log((event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0])/(event.jj_l1_gen_pt[0])),w)
        h_rho_l1      .Fill(ROOT.TMath.Log((event.jj_l1_softDrop_mass[0]*event.jj_l1_softDrop_mass[0])/(event.jj_l1_pt[0])),w)
        h_rho_gen_l2  .Fill(ROOT.TMath.Log((event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0])/(event.jj_l2_gen_pt[0])),w)
        h_rho_l2      .Fill(ROOT.TMath.Log((event.jj_l2_softDrop_mass[0]*event.jj_l2_softDrop_mass[0])/(event.jj_l2_pt[0])),w)
        
        #print ROOT.TMath.Log((event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0])/(event.jj_l1_gen_pt[0]*event.jj_l1_gen_pt[0]))
        if ROOT.TMath.Log((event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0])/(event.jj_l1_gen_pt[0]*event.jj_l1_gen_pt[0]))>-1.5  and ROOT.TMath.Log((event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0])/(event.jj_l2_gen_pt[0]*event.jj_l2_gen_pt[0]))>-1.5:
            print "======================================"
            print  event.jj_l1_gen_softDrop_mass[0]
            print event.jj_l1_gen_pt[0]
            print ROOT.TMath.Log((event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0])/(event.jj_l1_gen_pt[0]*event.jj_l1_gen_pt[0]))
            
            print event.jj_l2_gen_softDrop_mass[0]
            print event.jj_l2_gen_pt[0]
            print ROOT.TMath.Log((event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0])/(event.jj_l2_gen_pt[0]*event.jj_l2_gen_pt[0]))
            print "======================================"
            continue
        makeEventlist(event,listevents)
        #if splitTrees("gg",event.jj_l1_mcFlavour[0],event.jj_l2_mcFlavour[0]) ==0:
        #        continue
        events+=1
        printEvent(event)
        #if ROOT.TMath.Log((event.jj_l1_gen_softDrop_mass[0]*event.jj_l1_gen_softDrop_mass[0])/(event.jj_l1_gen_pt[0]*event.jj_l1_gen_pt[0]))<-10  and ROOT.TMath.Log((event.jj_l2_gen_softDrop_mass[0]*event.jj_l2_gen_softDrop_mass[0])/(event.jj_l2_gen_pt[0]*event.jj_l2_gen_pt[0]))<-10:
        #    continue
        
        #if passRecoNotGen([event.jj_l1_gen_softDrop_mass[0],event.jj_l2_gen_softDrop_mass[0]],[event.jj_l1_softDrop_mass[0],event.jj_l2_softDrop_mass[0]]):
        passevents+=1
            
    print "number of events in files "+str(events)
    print "number of events passing cuts "+str(passevents)
    print listevents
    
    outfile = ROOT.TFile("test_rho_signal.root","RECREATE")
    h_rho_gen_l1 .Write()
    h_rho_l1     .Write()
    h_rho_gen_l2 .Write()
    h_rho_l2     .Write()
