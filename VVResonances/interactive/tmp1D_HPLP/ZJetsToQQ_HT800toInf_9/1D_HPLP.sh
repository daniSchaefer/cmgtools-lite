#!/bin/sh
echo
echo
echo 'START---------------'
echo 'WORKDIR ' ${PWD}
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive
cmsenv
vvMake1DMVVTemplateWithKernels.py -H "x" -c "((HLT_JJ)*(run>500) + (run<500))*(njj>0&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)*(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)*(((jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98)||((jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57))**(jj_l1_softDrop_mass>55&&jj_l1_softDrop_mass<215)&&(jj_l2_softDrop_mass>55&&jj_l2_softDrop_mass<215)*(jj_l1_gen_softDrop_mass>20&&jj_l2_gen_softDrop_mass>20&&jj_l1_gen_softDrop_mass<300&&jj_l2_gen_softDrop_mass<300&&jj_gen_partialMass>400)*(jj_l1_softDrop_mass>55.0&&jj_l1_softDrop_mass<215.0&&jj_l2_softDrop_mass>55.0&&jj_l2_softDrop_mass<215.0)"  -v "jj_gen_partialMass"  --binsMVV 838,890,944,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704,3854,4010,4171,4337,4509,4686,4869,5000 -b 39  -x 838.0 -X 5000.0 -r JJ_nonRes_detectorResponse.root -t /usr/users/dschaefer/CMSSW_7_4_7/src/CMGTools/VVResonances/interactive/samples  -o res1D_HPLP/JJ_VJets_MVV_HPLP_9_ZJetsToQQ_HT800toInf.root -s ZJetsToQQ_HT800toInf.root -e 4000000 -E 499999
echo 'STOP---------------'
echo
echo
