#!/bin/bash
# 
# echo "run some plots to make post/prefit figure"
# w="workspace_pythia_nominal_dataherwig.root"
# l="dataherwig"
# o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/dataherwig/"
# 
# #w="/home/dschaefer/DiBoson3D/test_kernelSmoothing_pythia/workspace_pythia_nominal.root"
# #l="datapythia"
# #o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/datapythia/"
# 
# #w="workspace_datamadgraph.root"
# #l="datamadgraph"
# #o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/datamadgraph/"
# 
# #w="/home/dschaefer/DiBoson3D/workspaces/JJ_BulkGWW_HPHP_13TeV_workspace_pt2Syst_fitNominal.root"
# #l="pt2Syst_fitNominal"
# #o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/datapythia/"
# #echo "use workspace ${w}"
# 
# #echo "python runFitPlots.py -p z -f -n ${w} -l ${l} -o ${o} --log ${l}.log" 
# 
# 
# 
# # for the pt^2 systematics ######################################################################
# aw=("/home/dschaefer/DiBoson3D/workspaces/JJ_BulkGWW_HPHP_13TeV_workspace_pt2Syst_fitHerwig.root")
# #"/home/dschaefer/DiBoson3D/workspaces/JJ_BulkGWW_HPHP_13TeV_workspace_pt2Syst_fitNominal.root" "/home/dschaefer/DiBoson3D/workspaces/JJ_BulkGWW_HPHP_13TeV_workspace_pt2Syst_fitMadgraph.root")
# 
# al=("pt2Syst_fitHerwig")
# #"pt2Syst_fitNominal" "pt2Syst_fitMadgraph")       
# o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/"
# pdfs="nonResNominal_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV,nonRes_OPT2Up_JJ_HPHP_13TeV,nonRes_OPT2Down_JJ_HPHP_13TeV,nonRes_PT2Up_JJ_HPHP_13TeV,nonRes_PT2Down_JJ_HPHP_13TeV"
# ##################################################################################################

# for the default systematics ####################################################################
aw=("/home/dschaefer/DiBoson3D/finalKernels/workspace_testSyst.root" "/home/dschaefer/DiBoson3D/finalKernels/JJ_WprimeWZ_madgraph_HPHP.root" "/home/dschaefer/DiBoson3D/finalKernels/workspace_WprimeWZ_herwig.root" "workspace_testBatch_HPHP.root" "/home/dschaefer/DiBoson3D/workspaces/workspace_pythia_nominal_dataherwig.root" "/home/dschaefer/DiBoson3D/workspaces/workspace_datamadgraph.root")
al=("testSyst_HPHP" "datamadgraph_HPHP" "dataherwig_HPHP" "datapythia_testbatch" "dataherwig_HPHP" "datamadgraph_HPHP")
o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/"

pdfs="nonResNominal_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTZDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTZUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTZUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTZDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTXYUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTXYDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTXYUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTXYDown_JJ_WprimeWZ_HPHP_13TeV"
#pdfs="nonResNominal_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTZDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTZUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTZUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTZDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTXYUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTXYDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTXYUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTXYDown_JJ_WprimeWZ_HPLP_13TeV"
##################################################################################################


for i in `seq 0 2`;
do
echo ${aw[i]}
# python runFitPlots.py -p z -f -n ${aw[i]}  -l ${al[i]} -o ${o} --log ${al[i]}.log --pdf ${pdfs} 
# python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs}
   python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} 
# #   python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1350,1400
# #    python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1400,1450
#      python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} 
#   python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 205,207 -y 91,93
#      python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 150,215 -y 150,215
#      python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 150,215 -y 55,80
#      python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 80,150 -y 150,215
#     
#     
#     python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 55,65 -y 55,65
#     python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 65,85 -y 65,85
#     python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 85,105 -y 85,105
#     python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 105,125 -y 105,125
#     python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 125,145 -y 125,145
#    python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 65,105 
# 
done
echo "############ end of script #################"
