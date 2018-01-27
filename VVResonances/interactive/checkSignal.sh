#!/bin/bash

HP1='(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.57'
HP2='(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.57'
LP1='(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))>0.57&&(jj_l1_tau2/jj_l1_tau1+(0.082*TMath::Log((jj_l1_softDrop_mass*jj_l1_softDrop_mass)/jj_l1_pt)))<0.98'
LP2='(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))>0.57&&(jj_l2_tau2/jj_l2_tau1+(0.082*TMath::Log((jj_l2_softDrop_mass*jj_l2_softDrop_mass)/jj_l2_pt)))<0.98'
HPHP="(${HP1} && ${HP2})"
HPLP="((${LP1} && ${HP2}) || (${LP2} && ${HP1}))"


cuts="((HLT_JJ)*(run>500) + (run<500))*(njj>0&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>700&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)"

acceptanceMJ="(jj_l1_softDrop_mass>55&&jj_l1_softDrop_mass<215&&jj_l2_softDrop_mass>55&&jj_l2_softDrop_mass<215)" 

model="BulkWW"
model2="BulkGWW"

model="Wprime"
model2="WprimeWZ"

#model="BulkGravToZZ"
#model2="BulkGZZ"

model="ZprimeWW"
model2="ZprimeWW"


#python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MVV.json.root"  -c "${cuts}*${acceptanceMJ}*${HPHP}"  -V "jj_LV_mass" -m 1000 -M 5000 -e 0 samples
#python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MVV.json.root"  -c "${cuts}*${acceptanceMJ}*${HPLP}"  -V "jj_LV_mass" -m 1000 -M 5000 -e 0 samples
#python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MVV.json.root"  -c "${cuts}*${acceptanceMJ}"  -V "jj_LV_mass" -m 1000 -M 5000 -e 0 samples



python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MJl1_HPLP.json.root"  -c "${cuts}*${HPLP}"  -V "jj_l1_softDrop_mass" -m 55.0 -M 135.0 -e 0 --minMX 1200.0 --maxMX 7000.0 samples
#python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MJl1_HPHP.json.root"  -c "${cuts}*${HPHP}"  -V "jj_l1_softDrop_mass" -m 55.0 -M 135.0 -e 0 --minMX 1200.0 --maxMX 7000.0 samples

python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MJl1_HPLP.json.root"  -c "${cuts}*${HPLP}"  -V "jj_l2_softDrop_mass" -m 55.0 -M 135.0 -e 0 --minMX 1200.0 --maxMX 7000.0 samples
#python checkSignalFits.py -s ${model} --fitResults "debug_JJ_${model2}_MJl2_HPHP.json.root"  -c "${cuts}*${HPHP}"  -V "jj_l2_softDrop_mass" -m 55.0 -M 135.0 -e 0 --minMX 1200.0 --maxMX 7000.0 samples

