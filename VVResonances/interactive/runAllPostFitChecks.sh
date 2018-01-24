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
aw=("workspace_thea.root" "/home/dschaefer/DiBoson3D/workspaces/JJ_BulkGWW_HPHP_13TeV_workspace_ptSyst_fitNominal.root" "workspace_testBinning.root" "workspace_testBatch_HPHP.root" "/home/dschaefer/DiBoson3D/workspaces/workspace_pythia_nominal_dataherwig.root" "/home/dschaefer/DiBoson3D/workspaces/workspace_datamadgraph.root")
al=("thea" "datapythia_HPHP" "testBinning" "datapythia_testbatch" "dataherwig_HPHP" "datamadgraph_HPHP")
o="/home/dschaefer/DiBoson3D/GoodnessOfFitTests/"
pdfs="nonResNominal_JJ_HPHP_13TeV,nonRes_PTZDown_JJ_HPHP_13TeV,nonRes_OPTZUp_JJ_HPHP_13TeV,nonRes_PTZUp_JJ_HPHP_13TeV,nonRes_OPTZDown_JJ_HPHP_13TeV,nonRes_PTXYUp_JJ_HPHP_13TeV,nonRes_PTXYDown_JJ_HPHP_13TeV,nonRes_OPTXYUp_JJ_HPHP_13TeV,nonRes_OPTXYDown_JJ_HPHP_13TeV"
#pdfs="nonResNominal_JJ_HPLP_13TeV,nonRes_PTZDown_JJ_HPLP_13TeV,nonRes_OPTZUp_JJ_HPLP_13TeV,nonRes_PTZUp_JJ_HPLP_13TeV,nonRes_OPTZDown_JJ_HPLP_13TeV,nonRes_PTXYUp_JJ_HPLP_13TeV,nonRes_PTXYDown_JJ_HPLP_13TeV,nonRes_OPTXYUp_JJ_HPLP_13TeV,nonRes_OPTXYDown_JJ_HPLP_13TeV"
##################################################################################################


for i in `seq 0 0`;
do
echo ${aw[i]}
# python runFitPlots.py -p z -f -n ${aw[i]}  -l ${al[i]} -o ${o} --log ${al[i]}.log --pdf ${pdfs} 
# python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs}
  python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} 
#   python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1350,1400
#    python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1400,1450
#    python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 55,150 -y 55,150
#    python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -x 150,215 -y 150,215
    

#  python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1000,1300
#  python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 1300,2000
#  python runFitPlots.py -p xyz  -f -n ${aw[i]} -l ${al[i]} -o ${o} --pdf ${pdfs} -z 2000,5000
#  python runFitPlots.py -p z -f -n ${aw[i]} -l ${al[i]} -x 150,215 -y 150,215 -o ${o} --pdf ${pdfs}
# # python runFitPlots.py -p z -f -n ${aw[i]} -l ${al[i]} -x 150,215 -y 55,150 -o ${o} --pdf ${pdfs}
# #  
#  python runFitPlots.py -p x -f -n ${aw[i]} -l ${al[i]} -z 1000,1300 -o ${o} --pdf ${pdfs}
#  python runFitPlots.py -p x -f -n ${aw[i]} -l ${al[i]} -z 1300,2000 -o ${o} --pdf ${pdfs}
#  python runFitPlots.py -p x -f -n ${aw[i]} -l ${al[i]} -z 2000,5000 -o ${o} --pdf ${pdfs}
# # 
# # python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -z 1000,1300 -o ${o} --pdf ${pdfs}
# # python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -z 1300,2000 -o ${o} --pdf ${pdfs}
# # python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -z 2000,5000 -o ${o} --pdf ${pdfs}
# # 
# # python runFitPlots.py -p x -f -n ${aw[i]} -l ${al[i]} -y 150,215 -o ${o} --pdf ${pdfs}
# # python runFitPlots.py -p x -f -n ${aw[i]} -l ${al[i]} -y 55,150 -o ${o} --pdf ${pdfs}
# # 
#  python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -x 150,215 -o ${o} --pdf ${pdfs}
#  python runFitPlots.py -p y -f -n ${aw[i]} -l ${al[i]} -x 55,150 -o ${o} --pdf ${pdfs}
# 
done
echo "############ end of script #################"
