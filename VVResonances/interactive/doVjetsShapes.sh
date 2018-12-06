#bin/bash!

python cPVJets.py --xrange 55,65
python cPVJets.py --xrange 65,85
python cPVJets.py --xrange 85,105
python cPVJets.py --yrange 85,105 --xrange 55,65
python cPVJets.py --yrange 85,105 --xrange 85,105
python cPVJets.py --xrange 85,105 --yrange 105,215
python cPVJets.py --xrange 85,105 --yrange 55,65
python cPVJets.py --xrange 85,105 --yrange 85,105
python cPVJets.py --xrange 105,215 --yrange 105,215
python cPVJets.py --zrange 1000,1300
python cPVJets.py --zrange 1300,2000
python cPVJets.py --zrange 2000,5000
