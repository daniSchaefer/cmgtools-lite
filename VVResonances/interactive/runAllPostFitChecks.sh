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
aw=("workspace_test.root" "/home/dschaefer/DiBoson3D/finalKernels/workspace_pythia.root" "/home/dschaefer/DiBoson3D/finalKernels/JJ_WprimeWZ_madgraph_HPHP.root" "/home/dschaefer/DiBoson3D/finalKernels/workspace_herwig.root" )
al=("test_HPHP" "datapythia_HPHP" "datamadgraph_HPHP" "dataherwig_HPHP" )
o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/"
histos=("/home/dschaefer/DiBoson3D/finalKernels/JJ_pythia_HPHP.root" "/home/dschaefer/DiBoson3D/finalKernels/JJ_pythia_HPHP.root" "/home/dschaefer/DiBoson3D/finalKernels/JJ_madgraph_HPHP.root" "/home/dschaefer/DiBoson3D/finalKernels/JJ_herwig_HPHP.root")


pdfs="nonResNominal_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTZDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTZUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTZUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTZDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTXYUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_PTXYDown_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTXYUp_JJ_WprimeWZ_HPHP_13TeV,nonRes_OPTXYDown_JJ_WprimeWZ_HPHP_13TeV"
#pdfs="nonResNominal_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTZDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTZUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTZUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTZDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTXYUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_PTXYDown_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTXYUp_JJ_WprimeWZ_HPLP_13TeV,nonRes_OPTXYDown_JJ_WprimeWZ_HPLP_13TeV"
##################################################################################################


for i in `seq 0 0`;
do
echo ${aw[i]}
      python runFitPlots.py -p xyz  -n ${aw[i]} -l ${al[i]} -o ${o}  
done
echo "############ end of script #################"
