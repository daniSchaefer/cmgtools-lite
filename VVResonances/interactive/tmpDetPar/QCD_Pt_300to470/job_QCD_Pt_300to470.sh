#!/bin/sh
echo
echo
echo 'START---------------'
echo 'WORKDIR ' ${PWD}
source /afs/cern.ch/cms/cmsset_default.sh
cd /usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive
cmsenv
vvMake2DDetectorParam.py  -c "((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)*Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter*1*(jj_l1_gen_softDrop_mass>20&&jj_l2_gen_softDrop_mass>20&&jj_l1_gen_softDrop_mass<300&&jj_l2_gen_softDrop_mass<300&&jj_gen_partialMass>400)*(jj_l1_softDrop_mass>35&&jj_l1_softDrop_mass<300&&jj_l2_softDrop_mass>35&&jj_l2_softDrop_mass<300)"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b 200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000   /usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/samples -o /usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/resDetPar/JJ_nonRes_detectorResponse_QCD_Pt_300to470.root -s QCD_Pt_300to470.root
echo 'STOP---------------'
echo
echo
