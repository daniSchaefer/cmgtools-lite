# VV statistical analysis in 74X

Prepare your working dir with Higgs combine tools (74X)

```
mkdir VVAnalysisWith2DFit
mkdir CMGToolsForStat74X
cd CMGToolsForStat74X
cmsrel CMSSW_7_4_7
cd CMSSW_7_4_7/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v6.3.1
scram b clean; scram b -j 8
```

Fork cmgtools from https://github.com/Diboson3D/cmgtools-lite and checkout the VV statistical tools

```
cd ../..
export GITUSER=`git config user.github`
git clone https://github.com/${GITUSER}/cmgtools-lite CMGTools
cd CMGTools
git remote add Diboson3D https://github.com/Diboson3D/cmgtools-lite
git fetch Diboson3D
git checkout -b 3DVVstat Diboson3D/3DVVstat
scram b -j 8
cd VVResonances/interactive
ln -s samples_location sample
```

Current sample location with random sorting of jet1 and jet2

```
/eos/cms/store/cmst3/group/exovv/VVtuple/VV3Dproduction/
```

Make the 3D templates
 
```
python makeInputs.py
```

Run closure test of signal fits:

```
python plotSignalShapesFromJSON.py -f JJ_BulkGWW_MJl1_HPLP.json -v mJ
python plotSignalShapesFromJSON.py -f JJ_BulkGWW_MJl2_HPLP.json -v mJ
python plotSignalShapesFromJSON.py -f JJ_BulkGWW_MVV.json -v mVV
```

Run closure test of 3D templates versus simulation with Projections3DHisto.C script:

```
root -l
.x  Projections3DHisto.C("JJ_nonRes_HPHP_nominal.root","nonRes","JJ_nonRes_2D_HPHP.root","histo","control-plots")
```

Create datacard and workspace and run post fit

```
python makeCard.py
text2workspace.py datacard_JJ_HPHP_13TeV.txt -o JJ_BulkGWW_HPHP_13TeV_workspace.root
python runPostFit.py
```

Run the limits with combine and make final plot

```
vvSubmitLimits.py JJ_BulkGWW_HPHP_13TeV_workspace.root -s 100 -q 1nd -m 1200 -M 4200
find higgsCombineTest.Asymptotic.* -size +1500c | xargs hadd Limits_BulkGWW_HPHP_13TeV.root
vvMakeLimitPlot.py Limits_BulkGWW_HPHP_13TeV.root -x 1200 -X 4200 (expected limits)
vvMakeLimitPlot.py Limits_BulkGWW_HPHP_13TeV.root -x 1200 -X 4200 -b 0 (expected+observed limits)
```

Further instructions on how to run the code can be found at:
https://www.evernote.com/shard/s531/sh/cead4d9f-6b68-465f-8583-388f7527e7fc/f59cc13785c6e236454d2f69d5ce970c
