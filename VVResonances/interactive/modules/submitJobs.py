#!/usr/bin/env python
import os, re, copy
import commands
import math, time
import sys
import ROOT
from ROOT import *
import subprocess, thread

timeCheck = "30"
userName=os.environ['USER']

def waitForBatchJobs( jobname, remainingjobs, listOfJobs, userName, timeCheck="30"):
	if listOfJobs-remainingjobs < listOfJobs:
	    time.sleep(float(timeCheck))
	    # nprocess = "bjobs -u %s | awk {'print $9'} | grep %s | wc -l" %(userName,jobname)
	    nprocess = "bjobs -u %s | grep %s | wc -l" %(userName,jobname)
	    result = subprocess.Popen(nprocess, stdout=subprocess.PIPE, shell=True)
	    runningJobs =  int(result.stdout.read())
	    print "waiting for %d job(s) in the queue (out of total %d)" %(runningJobs,listOfJobs)
	    waitForBatchJobs( jobname, runningJobs, listOfJobs, userName, timeCheck)  
	else:
	    print "Jobs finished! Allow some time for files to be saved to your home directory"
	    time.sleep(5)
	    noutcmd = "ls res"+jobname+"/ | wc -l"
	    result = subprocess.Popen(noutcmd, stdout=subprocess.PIPE, shell=True)
	    nout =  int(result.stdout.read())
	    if listOfJobs-nout > 0: 
			print "Uooh! Missing %i jobs. Resubmit when merging. Now return to main script" %int(listOfJobs-nout)
	    else:
			print "Done! Have %i out of %i files in res%s directory. Return to main script"%(nout,listOfJobs,jobname)
	    return
        
def submitJobs(minEv,maxEv,cmd,OutputFileNames,queue,jobname,path):
	joblist = []
	for k,v in minEv.iteritems():

	  for j in range(len(v)):
	   os.system("mkdir tmp"+jobname+"/"+str(k).replace(".root","")+"_"+str(j+1))
	   os.chdir("tmp"+jobname+"/"+str(k).replace(".root","")+"_"+str(j+1))
	  
	   with open('job_%s_%i.sh'%(k.replace(".root",""),j+1), 'w') as fout:
	      fout.write("#!/bin/sh\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	      fout.write("echo 'START---------------'\n")
	      fout.write("echo 'WORKDIR ' ${PWD}\n")
	      fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
	      fout.write("cd "+str(path)+"\n")
	      fout.write("cmsenv\n")
	      fout.write(cmd+" -o res"+jobname+"/"+OutputFileNames+"_"+str(j+1)+"_"+k+" -s "+k+" -e "+str(minEv[k][j])+" -E "+str(maxEv[k][j])+"\n")
	      fout.write("echo 'STOP---------------'\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	   os.system("chmod 755 job_%s_%i.sh"%(k.replace(".root",""),j+1) )
	   os.system("bsub -q "+queue+" -o logs job_%s_%i.sh -J %s"%(k.replace(".root",""),j+1,jobname))
	   print "job nr " + str(j+1) + " file " + k + " being submitted"
	   joblist.append("%s_%i"%(k.replace(".root",""),j+1))
	   os.chdir("../..")
	return joblist 	   

def getEvents(template,samples):
	files = []
	sampleTypes = template.split(',')
	for f in os.listdir(samples):
		for t in sampleTypes:
			if f.find('.root') != -1 and f.find(t) != -1: files.append(f)

	minEv = {}
	maxEv = {}

	for f in files:
	 inf = ROOT.TFile('./samples/'+f,'READ')
	 minEv[f] = []
	 maxEv[f] = []
	 intree = inf.Get('tree')
	 nentries = intree.GetEntries()
	 print f,nentries,nentries/500000
	 if nentries/500000 == 0:
	  minEv[f].append(0)
	  maxEv[f].append(500000)
	 else:
	  for i in range(nentries/500000):
	   minEv[f].append(i*500000)
	   maxEv[f].append(499999)


	NumberOfJobs = 0
	for k in maxEv.keys():
	 NumberOfJobs += len(maxEv[k])

	return minEv, maxEv, NumberOfJobs, files
	
def Make2DDetectorParam(rootFile,template,cut,samples,jobName="DetPar"): # TODO! Buggy, fix
   
	print 
	print 'START: Make2DDetectorParam with parameters:'
	print
	print "rootFile = %s" %rootFile  
	print "template = %s" %template  
	print "cut      = %s" %cut       
	print "samples  = %s" %samples   
	print "jobName  = %s" %jobName 
	

	cmd='vvMake2DDetectorParam.py  -c "{cut}"  -v "jj_LV_mass,jj_l1_softDrop_mass"  -g "jj_gen_partialMass,jj_l1_gen_softDrop_mass,jj_l1_gen_pt"  -b "200,250,300,350,400,450,500,600,700,800,900,1000,1500,2000,5000"   {infolder}'.format(rootFile=rootFile,samples=template,cut=cut,infolder=samples)
	
	OutputFileNames = rootFile.replace(".root","") # base of the output file name, they will be saved in res directory
	queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
	
	files = []
	sampleTypes = template.split(',')
	for f in os.listdir(samples):
		for t in sampleTypes:
			if f.find('.root') != -1 and f.find(t) != -1: files.append(f)
 
	NumberOfJobs= len(files) 
	print
	print "Submitting %i number of jobs "  ,NumberOfJobs
	print
	
	path = os.getcwd()
	try: os.system("rm -r tmp"+jobName)
	except: print "No tmp/ directory"
	os.system("mkdir tmp"+jobName)
	try: os.stat("res"+jobName) 
	except: os.mkdir("res"+jobName)
	print

	#### Creating and sending jobs #####
	joblist = []
	##### loop for creating and sending jobs #####
	for x in range(1, int(NumberOfJobs)+1):
	 
	   os.system("mkdir tmp"+jobName+"/"+str(files[x-1]).replace(".root",""))
	   os.chdir("tmp"+jobName+"/"+str(files[x-1]).replace(".root",""))
	 
	   with open('job_%s.sh'%files[x-1].replace(".root",""), 'w') as fout:
	      fout.write("#!/bin/sh\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	      fout.write("echo 'START---------------'\n")
	      fout.write("echo 'WORKDIR ' ${PWD}\n")
	      fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
	      fout.write("cd "+str(path)+"\n")
	      fout.write("cmsenv\n")
	      fout.write(cmd+" -o "+path+"/res"+jobName+"/"+OutputFileNames+"_"+files[x-1]+" -s "+files[x-1]+"\n")
	      fout.write("echo 'STOP---------------'\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	   os.system("chmod 755 job_%s.sh"%(files[x-1].replace(".root","")) )
   
	   os.system("bsub -q "+queue+" -o logs job_%s.sh -J %s"%(files[x-1].replace(".root",""),jobName))
	   print "job nr " + str(x) + " submitted"
	   joblist.append("%s"%(files[x-1].replace(".root","")))
	   os.chdir("../..")
   
	print
	print "your jobs:"
	os.system("bjobs")
	userName=os.environ['USER']
	waitForBatchJobs(jobName,NumberOfJobs,NumberOfJobs, userName, timeCheck)
	
	print
	print 'END: Make2DDetectorParam'
	print
	return joblist, files	
	
def Make1DMVVTemplateWithKernels(rootFile,template,cut,resFile,binsMVV,minMVV,maxMVV,samples,jobName="1DMVV"):
	
	print 
	print 'START: Make1DMVVTemplateWithKernels with parameters:'
	print
	print "rootFile = %s" %rootFile  
	print "template = %s" %template  
	print "cut      = %s" %cut       
	print "resFile  = %s" %resFile   
	print "binsMVV  = %i" %binsMVV   
	print "minMVV   = %i" %minMVV    
	print "maxMVV   = %i" %maxMVV    
	print "samples  = %s" %samples   
	print "jobName  = %s" %jobName 
	print

	minEv, maxEv, NumberOfJobs, files = getEvents(template,samples) 
	print "Submitting %i number of jobs "  ,NumberOfJobs
	print

	cmd='vvMake1DMVVTemplateWithKernels.py -H "x" -c "{cut}"  -v "jj_gen_partialMass" -b {binsMVV}  -x {minMVV} -X {maxMVV} -r {res} {infolder} '.format(rootFile=rootFile,cut=cut,res=resFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,infolder=samples)
	OutputFileNames = rootFile.replace(".root","") # base of the output file name, they will be saved in res directory
	queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
	
	path = os.getcwd()
	try: os.system("rm -r tmp"+jobName)
	except: print "No tmp/ directory"
	os.system("mkdir tmp"+jobName)
	try: os.stat("res"+jobName) 
	except: os.mkdir("res"+jobName)
	print

	#### Creating and sending jobs #####
	joblist = submitJobs(minEv,maxEv,cmd,OutputFileNames,queue,jobName,path)
	with open('tmp'+jobName+'_joblist.txt','w') as outfile:
		outfile.write("jobList: %s\n" % joblist)
		outfile.write("files: %s\n" % files)
	outfile.close()
	print
	print "your jobs:"
	os.system("bjobs")
	waitForBatchJobs(jobName,NumberOfJobs,NumberOfJobs, userName, timeCheck)
	
	
	
	print
	print 'END: Make1DMVVTemplateWithKernels'
	print
	return joblist, files 

def Make2DTemplateWithKernels(rootFile,template,cut,leg,binsMVV,minMVV,maxMVV,resFile,binsMJ,minMJ,maxMJ,samples,jobName="2DMVV"):
	
	print 
	print 'START: Make2DTemplateWithKernels'
	print
	print "rootFile  = %s" %rootFile   
	print "template  = %s" %template   
	print "cut  	 = %s" %cut  	  
	print "leg  	 = %s" %leg  	  
	print "binsMVV   = %i" %binsMVV    
	print "minMVV    = %i" %minMVV     
	print "maxMVV    = %i" %maxMVV     
	print "resFile   = %s" %resFile    
	print "binsMJ    = %s" %binsMJ    
	print "minMJ     = %s" %minMJ 
	print "maxMJ     = %s" %maxMJ 
	print "samples   = %s" %samples   
	print "jobName   = %s" %jobName   
	print

	minEv, maxEv, NumberOfJobs, files = getEvents(template,samples) 
	print "Submitting %i number of jobs "  ,NumberOfJobs
	print

	cmd='vvMake2DTemplateWithKernels.py -c "{cut}"  -v "jj_{leg}_gen_softDrop_mass,jj_gen_partialMass"  -b {binsMJ} -B {binsMVV} -x {minMJ} -X {maxMJ} -y {minMVV} -Y {maxMVV}  -r {res}  {infolder}'.format(rootFile=rootFile,samples=template,cut=cut,leg=leg,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,res=resFile,binsMJ=binsMJ,minMJ=minMJ,maxMJ=maxMJ,infolder=samples)
	OutputFileNames = rootFile.replace(".root","") # base of the output file name, they will be saved in res directory
	queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
	
	path = os.getcwd()
	try: os.system("rm -r tmp"+jobName)
	except: print "No tmp/ directory"
	os.system("mkdir tmp"+jobName)
	try: os.stat("res"+jobName) 
	except: os.mkdir("res"+jobName)
	print

	#### Creating and sending jobs #####
	joblist = submitJobs(minEv,maxEv,cmd,OutputFileNames,queue,jobName,path)
	with open('tmp'+jobName+'_joblist.txt','w') as outfile:
		outfile.write("jobList: %s\n" % joblist)
		outfile.write("files: %s\n" % files)
	outfile.close()
	print
	print "your jobs:"
	os.system("bjobs")
	userName=os.environ['USER']
	waitForBatchJobs(jobName,NumberOfJobs,NumberOfJobs, userName, timeCheck)
	
	
	  
	print
	print 'END: Make2DTemplateWithKernels'
	print
	return joblist, files

def unequalScale(histo,name,alpha,power=1,dim=1):
    newHistoU =copy.deepcopy(histo) 
    newHistoU.SetName(name+"Up")
    newHistoD =copy.deepcopy(histo) 
    newHistoD.SetName(name+"Down")
    if dim == 2:
	    maxFactor = max(pow(histo.GetXaxis().GetXmax(),power),pow(histo.GetXaxis().GetXmin(),power))
	    for i in range(1,histo.GetNbinsX()+1):
	        x= histo.GetXaxis().GetBinCenter(i)
	        for j in range(1,histo.GetNbinsY()+1):
	            nominal=histo.GetBinContent(i,j)
	            factor = 1+alpha*pow(x,power) 
	            newHistoU.SetBinContent(i,j,nominal*factor)
	            newHistoD.SetBinContent(i,j,nominal/factor)
	    if newHistoU.Integral()>0.0:        
	        newHistoU.Scale(1.0/newHistoU.Integral())        
	    if newHistoD.Integral()>0.0:        
	        newHistoD.Scale(1.0/newHistoD.Integral())        
    else:
	    for i in range(1,histo.GetNbinsX()+1):
	        x= histo.GetXaxis().GetBinCenter(i)
	        nominal=histo.GetBinContent(i)
	        factor = 1+alpha*pow(x,power) 
	        newHistoU.SetBinContent(i,nominal*factor)
	        newHistoD.SetBinContent(i,nominal/factor)	
    return newHistoU,newHistoD 
    
def mirror(histo,histoNominal,name,dim=1):
    newHisto =copy.deepcopy(histoNominal) 
    newHisto.SetName(name)
    intNominal=histoNominal.Integral()
    intUp = histo.Integral()
    if dim == 2:
		for i in range(1,histo.GetNbinsX()+1):
			for j in range(1,histo.GetNbinsY()+1):
				up=histo.GetBinContent(i,j)/intUp
				nominal=histoNominal.GetBinContent(i,j)/intNominal
				newHisto.SetBinContent(i,j,histoNominal.GetBinContent(i,j)*nominal/up)
    else:
		for i in range(1,histo.GetNbinsX()+1):
			up=histo.GetBinContent(i)/intUp
			nominal=histoNominal.GetBinContent(i)/intNominal
			newHisto.SetBinContent(i,histoNominal.GetBinContent(i)*nominal/up)	
    return newHisto       

def expandHisto(histo,suffix,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ):
    histogram=ROOT.TH2F(histo.GetName()+suffix,"histo",binsMJ,minMJ,maxMJ,binsMVV,minMVV,maxMVV)
    for i in range(1,histo.GetNbinsX()+1):
        proje = histo.ProjectionY("q",i,i)
        graph=ROOT.TGraph(proje)
        for j in range(1,histogram.GetNbinsY()+1):
            x=histogram.GetYaxis().GetBinCenter(j)
            bin=histogram.GetBin(i,j)
            histogram.SetBinContent(bin,graph.Eval(x,0,"S"))
    return histogram
        
def conditional(hist):
    for i in range(1,hist.GetNbinsY()+1):
        proj=hist.ProjectionX("q",i,i)
        integral=proj.Integral()
        if integral==0.0:
            print 'SLICE WITH NO EVENTS!!!!!!!!',hist.GetName()
            continue
        for j in range(1,hist.GetNbinsX()+1):
            hist.SetBinContent(j,i,hist.GetBinContent(j,i)/integral)

def getJobs(files,jobList,outdir):
	resubmit = []
	jobsPerSample = {}
	exit_flag = False

	for s in files:
	 s = s.replace('.root','')
	 filelist = []
	 for t in jobList:
	  if t.find(s) == -1: continue
	  jobid = t.split("_")[-1]
	  found = False
	  for o in os.listdir(outdir):
	   if o.find(s) != -1 and o.find('_'+jobid+'_') != -1:
	    found = True
	    filelist.append(outdir+"/"+o)
	    break
	  if not found:
	   print "SAMPLE ",s," JOBID ",jobid," NOT FOUND"
	   exit_flag = True
	   resubmit.append(s+"_"+jobid)
	 if len(filelist) > 0: jobsPerSample[s] = filelist
	return resubmit, jobsPerSample,exit_flag	 
	
def reSubmit(jobdir,resubmit,jobname):
 jobs = []
 for o in os.listdir(jobdir):
	 for jobs in resubmit:
		 if o.find(jobs) != -1: 
			 jobfolder = jobdir+"/"+jobs+"/"
			 os.chdir(jobfolder)
			 script = "job_"+jobs+".sh"
			 cmd = "bsub -q 8nh -o logs %s -J %s"%(script,jobname)
			 print cmd
			 jobs += cmd
			 os.system("chmod 755 %s"%script)
			 os.system(cmd)
			 os.chdir("../..")
 return jobs

def merge2DDetectorParam(jobList,files,jobname): # TODO! Buggy, fix
	
	print "Merging 2D detector parametrization"
	print
	print "Jobs to merge :   " ,jobList
	print "Files ran over:   " ,files
	
	outdir = 'res'+jobname
	jobdir = 'tmp'+jobname
	
	resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
	
	if exit_flag:
	 submit = raw_input("The following files are missing: %s. Do you  want to resubmit the jobs to the batch system before merging? [y/n] "%resubmit)
	 if submit == 'y' or submit=='Y':
		 print "Resubmitting jobs:"
		 jobs = reSubmit(jobdir,resubmit,jobname)
		 waitForBatchJobs(jobname,len(resubmit),len(resubmit), userName, timeCheck)
		 resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
		 if exit_flag: 
			 print "Job crashed again! Please resubmit manually before attempting to merge again"
			 for j in jobs: print j 
			 sys.exit()
	else:
		 submit = raw_input("Some files are missing. [y] == Exit without merging, [n] == continue ? ")
		 if submit == 'y' or submit=='Y':
			 print "Exit without merging!"
			 sys.exit()
		 else:
			 print "Continuing merge!"
 
	try: 
		os.stat(outdir+'_out') 
		os.system('rm -r '+outdir+'_out')
		os.mkdir(outdir+'_out')
	except: os.mkdir(outdir+'_out')

	filelist = os.listdir('./res'+jobname+'/')

	pythia_files = []

	for f in filelist:
	 if f.find('QCD_Pt_') != -1: pythia_files.append('./res'+jobname+'/'+f)
	

	#now hadd them

	if len(pythia_files) > 0:
		cmd = 'hadd -f JJ_nonRes_detectorResponse.root'
		for f in pythia_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
		 	
def merge1DMVVTemplate(jobList,files,jobname,purity,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ):
	
	print "Merging 1D templates"
	print
	print "Jobs to merge :   " ,jobList
	print "Files ran over:   " ,files
	
	outdir = 'res'+jobname
	jobdir = 'tmp'+jobname
	
	resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
	
	if exit_flag:
	 submit = raw_input("The following files are missing: %s. Do you  want to resubmit the jobs to the batch system before merging? [y/n] "%resubmit)
	 if submit == 'y' or submit=='Y':
		 print "Resubmitting jobs:"
		 jobs = reSubmit(jobdir,resubmit,jobname)
		 waitForBatchJobs(jobname,len(resubmit),len(resubmit), userName, timeCheck)
		 resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
		 if exit_flag: 
			 print "Job crashed again! Please resubmit manually before attempting to merge again"
			 for j in jobs: print j 
			 sys.exit()
	 else:
		 submit = raw_input("Some files are missing. [y] == Exit without merging, [n] == continue ? ")
		 if submit == 'y' or submit=='Y':
			 print "Exit without merging!"
			 sys.exit()
		 else:
			 print "Continuing merge!"
 
	try: 
		os.stat(outdir+'_out') 
		os.system('rm -r '+outdir+'_out')
		os.mkdir(outdir+'_out')
	except: os.mkdir(outdir+'_out')

	for s in jobsPerSample.keys():

	 factor = 1./float(len(jobsPerSample[s]))
	 print "sample: ", s,"number of files:",len(jobsPerSample[s]),"adding histo with scale factor:",factor
 
	 outf = ROOT.TFile.Open(outdir+'_out/JJ_nonRes_MVV_%s_%s.root'%(s,purity),'RECREATE')
  
	 finalHistos = {}
	 finalHistos['histo_nominal'] = ROOT.TH1F("histo_nominal_out","histo_nominal_out",binsMVV,minMVV,maxMVV)
	 finalHistos['mvv_nominal'] = ROOT.TH1F("mvv_nominal_out","mvv_nominal_out",binsMVV,minMVV,maxMVV)
    
	 for f in jobsPerSample[s]:
    
	  inf = ROOT.TFile.Open(f,'READ')
    
	  for h in inf.GetListOfKeys():
  
	   if (h.GetName() == 'histo_nominal' and h.GetTitle() == 'histo_nominal') or (h.GetName() == 'mvv_nominal' and h.GetTitle() == 'mvv_nominal'):

	    histo = ROOT.TH1F()
	    histo = inf.Get(h.GetName())

	    finalHistos[h.GetName()].Add(histo,factor)
      
   
	 print "Write file: ",outdir+'_out/JJ_nonRes_MVV_%s_%s.root'%(s,purity)
   
	 outf.cd()  
	 finalHistos['histo_nominal'].Write('histo_nominal')
	 finalHistos['mvv_nominal'].Write('mvv_nominal')
   
	 outf.Close()
	 outf.Delete()


	# read out files
	filelist = os.listdir('./'+outdir+'_out'+'/')

	mg_files = []
	pythia_files = []
	herwig_files = []

	for f in filelist:
	 if f.find('QCD_HT') != -1: mg_files.append('./'+outdir+'_out'+'/'+f)
	 elif f.find('QCD_Pt_') != -1: pythia_files.append('./'+outdir+'_out'+'/'+f)
	 else: herwig_files.append('./'+outdir+'_out'+'/'+f)
	 
	 
	doMadGraph = False
	doHerwig   = False
	doPythia   = False
	
	#now hadd them
	if len(mg_files) > 0:
		cmd = 'hadd -f JJ_nonRes_MVV_%s_altshape2.root '%purity
		for f in mg_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
		
		fhadd_madgraph = ROOT.TFile.Open('JJ_nonRes_MVV_%s_altshape2.root'%purity,'READ')
		mvv_altshape2 = fhadd_madgraph.Get('mvv_nominal')
		mvv_altshape2.SetName('mvv_altshape2')
		mvv_altshape2.SetTitle('mvv_altshape2')
		histo_altshape2 = fhadd_madgraph.Get('histo_nominal')
		histo_altshape2.SetName('histo_altshape2')
		histo_altshape2.SetTitle('histo_altshape2')
		
		doMadGraph = True
		

	if len(herwig_files) > 0:
		cmd = 'hadd -f JJ_nonRes_MVV_%s_altshapeUp.root '%purity
		for f in herwig_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
		
		fhadd_herwig = ROOT.TFile.Open('JJ_nonRes_MVV_%s_altshapeUp.root'%purity,'READ')
		mvv_altshapeUp = fhadd_herwig.Get('mvv_nominal')
		mvv_altshapeUp.SetName('mvv_altshapeUp')
		mvv_altshapeUp.SetTitle('mvv_altshapeUp')
		histo_altshapeUp = fhadd_herwig.Get('histo_nominal')
		histo_altshapeUp.SetName('histo_altshapeUp')
		histo_altshapeUp.SetTitle('histo_altshapeUp')
		
		doHerwig = True
 	
	if len(pythia_files) > 0:
		cmd = 'hadd -f JJ_nonRes_MVV_%s_nominal.root '%purity
		for f in pythia_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
		
		fhadd_pythia = ROOT.TFile.Open('JJ_nonRes_MVV_%s_nominal.root'%(purity),'READ')
		mvv_nominal = fhadd_pythia.Get('mvv_nominal')
		mvv_nominal.SetName('mvv_nominal')
		mvv_nominal.SetTitle('mvv_nominal')
		histo_nominal = fhadd_pythia.Get('histo_nominal')
		histo_nominal.SetName('histo_nominal')
		histo_nominal.SetTitle('histo_nominal')
		
		doPythia = True

	outf = ROOT.TFile.Open('JJ_nonRes_MVV_%s.root'%purity,'RECREATE') 
    
	if doPythia:
		mvv_nominal.Write('mvv_nominal')
		histo_nominal.Write('histo_nominal')
		#histo_nominal_ScaleUp.Write('histo_nominal_ScaleUp')
		#histo_nominal_ScaleDown.Write('histo_nominal_ScaleDown')
		alpha=1.5/5000
		histogram_pt_down,histogram_pt_up=unequalScale(histo_nominal,"histo_nominal_PT",alpha)
		histogram_pt_down.SetName('histo_nominal_PTDown')
		histogram_pt_down.SetTitle('histo_nominal_PTDown')
		histogram_pt_down.Write('histo_nominal_PTDown')
		histogram_pt_up.SetName('histo_nominal_PTUp')
		histogram_pt_up.SetTitle('histo_nominal_PTUp')
		histogram_pt_up.Write('histo_nominal_PTUp')

		alpha=1.5*1000
		histogram_opt_down,histogram_opt_up=unequalScale(histo_nominal,"histo_nominal_OPT",alpha,-1)
		histogram_opt_down.SetName('histo_nominal_OPTDown')
		histogram_opt_down.SetTitle('histo_nominal_OPTDown')
		histogram_opt_down.Write('histo_nominal_OPTDown')
		histogram_opt_up.SetName('histo_nominal_OPTUp')
		histogram_opt_up.SetTitle('histo_nominal_OPTUp')
		histogram_opt_up.Write('histo_nominal_OPTUp')
		
		alpha=5000.*5000.
		histogram_pt2_down,histogram_pt2_up=unequalScale(histo_nominal,"histo_nominal_PT2",alpha,2)
		histogram_pt2_down.SetName('histo_nominal_PT2Down')
		histogram_pt2_down.SetTitle('histo_nominal_PT2Down')
		histogram_pt2_down.Write('histo_nominal_PT2Down')
		histogram_pt2_down.Write()
		
		histogram_pt2_up.SetName('histo_nominal_PT2Up')
		histogram_pt2_up.SetTitle('histo_nominal_PT2Up')
		histogram_pt2_up.Write('histo_nominal_PT2Up')
		histogram_pt2_up.Write()
		
		alpha=1000.*1000.
		histogram_opt2_down,histogram_opt2_up=unequalScale(histo_nominal,"histo_nominal_OPT2",alpha,-2)
		
		histogram_opt2_up.SetName('histo_nominal_OPT2Up')
		histogram_opt2_up.SetTitle('histo_nominal_OPT2Up')
		histogram_opt2_up.Write()
		
		histogram_opt2_down.SetName('histo_nominal_OPT2Up')
		histogram_opt2_down.SetTitle('histo_nominal_OPT2Up')
		histogram_opt2_down.Write()
		
		
		
	if doHerwig:
		mvv_altshapeUp.Write('mvv_altshapeUp')
		histo_altshapeUp.Write('histo_altshapeUp')
		#histo_altshape_ScaleUp.Write('histo_altshape_ScaleUp')
		#histo_altshape_ScaleDown.Write('histo_altshape_ScaleDown')
		if doPythia:
			histogram_altshapeDown=mirror(histo_altshapeUp,histo_nominal,"histo_altshapeDown")
			histogram_altshapeDown.SetName('histo_altshapeDown')
			histogram_altshapeDown.SetTitle('histo_altshapeDown')
			histogram_altshapeDown.Write('histo_altshapeDown')
		
	if doMadGraph:
		mvv_altshape2.Write('mvv_altshape2')
		histo_altshape2.Write('histo_altshape2')
		
	os.system('rm -rf '+outdir+'_out/')
	# os.system('rm -rf '+outdir+'/')

def merge2DTemplate(jobList,files,jobname,purity,leg,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ):  
	
	print "Merging 2D templates"
	print
	print "Jobs to merge :   " ,jobList
	print "Files ran over:   " ,files
	
	outdir = 'res'+jobname
	jobdir = 'tmp'+jobname
	
	resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
	
	if exit_flag:
	 submit = raw_input("The following files are missing: %s. Do you  want to resubmit the jobs to the batch system before merging? [y/n] "%resubmit)
	 if submit == 'y' or submit=='Y':
		 print "Resubmitting jobs:"
		 jobs = reSubmit(jobdir,resubmit,jobname)
		 waitForBatchJobs(jobname,len(resubmit),len(resubmit), userName, timeCheck)
		 resubmit, jobsPerSample,exit_flag = getJobs(files,jobList,outdir)
		 if exit_flag: 
			 print "Job crashed again! Please resubmit manually before attempting to merge again"
			 for j in jobs: print j 
			 sys.exit()
	 else:
		 submit = raw_input("Some files are missing. [y] == Exit without merging, [n] == continue ? ")
		 if submit == 'y' or submit=='Y':
			 print "Exit without merging!"
			 sys.exit()
		 else:
			 print "Continuing merge!"
	
 
	try: 
		os.stat(outdir+'_out') 
		os.system('rm -r '+outdir+'_out')
		os.mkdir(outdir+'_out')
	except: os.mkdir(outdir+'_out')

	for s in jobsPerSample.keys():

	 factor = 1./float(len(jobsPerSample[s]))
	 print "sample: ", s,"number of files:",len(jobsPerSample[s]),"adding histo with scale factor:",factor
 
	 outf = ROOT.TFile.Open(outdir+'_out/JJ_nonRes_COND2D_%s_%s_%s.root'%(s,leg,purity),'RECREATE')
  
	 finalHistos = {}
	 finalHistos['histo_nominal_coarse'] = ROOT.TH2F("histo_nominal_coarse","histo_nominal_coarse_out",binsMJ,minMJ,maxMJ,40,minMVV,maxMVV)
	 finalHistos['mjet_mvv_nominal'] = ROOT.TH2F("mjet_mvv_nominal_out","mjet_mvv_nominal_out",binsMJ,minMJ,maxMJ,binsMVV,minMVV,maxMVV)
	 finalHistos['mjet_mvv_nominal_3D'] = ROOT.TH3F("mjet_mvv_nominal_3D_out","mjet_mvv_nominal_3D_out",binsMJ,minMJ,maxMJ,binsMJ,minMJ,maxMJ,binsMVV,minMVV,maxMVV)
    
	 for f in jobsPerSample[s]:

	  inf = ROOT.TFile.Open(f,'READ')
    
	  for h in inf.GetListOfKeys():
  
	   for k in finalHistos.keys():
	    if h.GetName() == k:

	     histo = ROOT.TH1F()
	     histo = inf.Get(h.GetName())

	     finalHistos[h.GetName()].Add(histo,factor)
   
	 print "Write file: ",outdir+'_out/JJ_nonRes_COND2D_%s_%s_%s.root'%(s,leg,purity)
   
	 outf.cd()  
 
	 for k in finalHistos.keys():
	  finalHistos[k].SetTitle(k)
	  finalHistos[k].Write(k)
   
	 outf.Close()
	 outf.Delete()


	# read out files
	filelist = os.listdir('./'+outdir+'_out'+'/')

	mg_files = []
	pythia_files = []
	herwig_files = []

	for f in filelist:
	 if f.find('COND2D') == -1: continue
	 if f.find('QCD_HT') != -1: mg_files.append('./'+outdir+'_out'+'/'+f)
	 elif f.find('QCD_Pt_') != -1: pythia_files.append('./'+outdir+'_out'+'/'+f)
	 else: herwig_files.append('./'+outdir+'_out'+'/'+f)
	 
	 
	doMadGraph = False
	doHerwig   = False
	doPythia   = False
	
	#now hadd them
	if len(mg_files) > 0:
		cmd = 'hadd -f JJ_nonRes_COND2D_%s_%s_altshape2.root '%(purity,leg)
		for f in mg_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)


		fhadd_madgraph = ROOT.TFile.Open('JJ_nonRes_COND2D_%s_%s_altshape2.root'%(purity,leg),'READ')
		mjet_mvv_altshape2_3D = fhadd_madgraph.Get('mjet_mvv_nominal_3D') 
		mjet_mvv_altshape2_3D.SetName('mjet_mvv_altshape2_3D')
		mjet_mvv_altshape2_3D.SetTitle('mjet_mvv_altshape2_3D')
		mjet_mvv_altshape2 = fhadd_madgraph.Get('mjet_mvv_nominal')
		mjet_mvv_altshape2.SetName('mjet_mvv_altshape2')
		mjet_mvv_altshape2.SetTitle('mjet_mvv_altshape2')
		histo_altshape2 = fhadd_madgraph.Get('histo_nominal_coarse')
		histo_altshape2.SetName('histo_altshape2_coarse')
		histo_altshape2.SetTitle('histo_altshape2_coarse')
		#histo_altshape2 = fhadd_madgraph.Get('histo_nominal')
		#histo_altshape2.SetName('histo_altshape2')
		#histo_altshape2.SetTitle('histo_altshape2')

		doMadGraph = True


	if len(herwig_files) > 0:
		cmd = 'hadd -f JJ_nonRes_COND2D_%s_%s_altshapeUp.root '%(purity,leg)
		for f in herwig_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)

		fhadd_herwig = ROOT.TFile.Open('JJ_nonRes_COND2D_%s_%s_altshapeUp.root'%(purity,leg),'READ')
		mjet_mvv_altshapeUp_3D = fhadd_herwig.Get('mjet_mvv_nominal_3D') 
		mjet_mvv_altshapeUp_3D.SetName('mjet_mvv_altshapeUp_3D')
		mjet_mvv_altshapeUp_3D.SetTitle('mjet_mvv_altshapeUp_3D')
		mjet_mvv_altshapeUp = fhadd_herwig.Get('mjet_mvv_nominal')
		mjet_mvv_altshapeUp.SetName('mjet_mvv_altshapeUp')
		mjet_mvv_altshapeUp.SetTitle('mjet_mvv_altshapeUp')
		histo_altshapeUp = fhadd_herwig.Get('histo_nominal_coarse')
		histo_altshapeUp.SetName('histo_altshapeUp_coarse')
		histo_altshapeUp.SetTitle('histo_altshapeUp_coarse')
		#histo_altshapeUp = fhadd_herwig.Get('histo_nominal')
		#histo_altshapeUp.SetName('histo_altshapeUp')
		#histo_altshapeUp.SetTitle('histo_altshapeUp')
		doHerwig = True

	if len(pythia_files) > 0:
		cmd = 'hadd -f JJ_nonRes_COND2D_%s_%s_nominal.root '%(purity,leg)
		for f in pythia_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
		
		fhadd_pythia = ROOT.TFile.Open('JJ_nonRes_COND2D_%s_%s_nominal.root'%(purity,leg),'READ')
		mjet_mvv_nominal_3D = fhadd_pythia.Get('mjet_mvv_nominal_3D') 
		mjet_mvv_nominal_3D.SetName('mjet_mvv_nominal_3D')
		mjet_mvv_nominal_3D.SetTitle('mjet_mvv_nominal_3D')
		mjet_mvv_nominal = fhadd_pythia.Get('mjet_mvv_nominal')
		mjet_mvv_nominal.SetName('mjet_mvv_nominal')
		mjet_mvv_nominal.SetTitle('mjet_mvv_nominal')
		histo_nominal = fhadd_pythia.Get('histo_nominal_coarse')
		histo_nominal.SetName('histo_nominal_coarse')
		histo_nominal.SetTitle('histo_nominal_coarse')
		#histo_nominal = fhadd_pythia.Get('histo_nominal')
		#histo_nominal.SetName('histo_nominal')
		#histo_nominal.SetTitle('histo_nominal')
		
		doPythia = True

	outf = ROOT.TFile.Open('JJ_nonRes_COND2D_%s_%s.root'%(purity,leg),'RECREATE') 
	finalHistograms = {}
	
	if doPythia:
		mjet_mvv_nominal.Write('mjet_mvv_nominal')
		mjet_mvv_nominal_3D.Write('mjet_mvv_nominal_3D')

		histo_nominal.Write('histo_nominal_coarse')
		conditional(histo_nominal)

		expanded=expandHisto(histo_nominal,"",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
		conditional(expanded)
		expanded.SetName('histo_nominal')
		expanded.SetTitle('histo_nominal')
		expanded.Write('histo_nominal')
		finalHistograms['histo_nominal'] = histo_nominal
		
		#histo_nominal_ScaleUp.Write('histo_nominal_ScaleUp')
		#conditional(histo_nominal_ScaleUp)
		#expanded=expandHisto(histo_nominal_ScaleUp,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
		#conditional(expanded)
		#expanded.Write('histo_nominal_ScaleUp')

		#histo_nominal_ScaleDown.Write('histo_nominal_ScaleDown')
		#conditional(histo_nominal_ScaleDown)
		#expanded=expandHisto(histo_nominal_ScaleDown,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
		#conditional(expanded)
		#expanded.Write('histo_nominal_ScaleDown')
		
		alpha=1.5/float(maxMJ)
		histogram_pt_down,histogram_pt_up=unequalScale(finalHistograms['histo_nominal'],"histo_nominal_PT",alpha,1,2)
		conditional(histogram_pt_down)
		histogram_pt_down.SetName('histo_nominal_PTDown')
		histogram_pt_down.SetTitle('histo_nominal_PTDown')
		histogram_pt_down.Write('histo_nominal_PTDown')
		conditional(histogram_pt_up)
		histogram_pt_up.SetName('histo_nominal_PTUp')
		histogram_pt_up.SetTitle('histo_nominal_PTUp')
		histogram_pt_up.Write('histo_nominal_PTUp')

		alpha=1.5*float(minMJ)
		h1,h2=unequalScale(finalHistograms['histo_nominal'],"histo_nominal_OPT",alpha,-1,2)
		conditional(h1)
		h1.SetName('histo_nominal_OPTDown')
		h1.SetTitle('histo_nominal_OPTDown')
		h1.Write('histo_nominal_OPTDown')
		conditional(h2)
		h2.SetName('histo_nominal_OPTUp')
		h2.SetTitle('histo_nominal_OPTUp')
		h2.Write('histo_nominal_OPTUp')

	if doHerwig:
		histo_altshapeUp.Write('histo_altshapeUp_coarse')
		conditional(histo_altshapeUp)
		expanded=expandHisto(histo_altshapeUp,"herwig",binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ)
		conditional(expanded)
		expanded.SetName('histo_altshapeUp')
		expanded.SetTitle('histo_altshapeUp')
		expanded.Write('histo_altshapeUp')
		finalHistograms['histo_altshapeUp'] = expanded
		#histo_altshapeUp.Write('histo_altshapeUp')
		#finalHistograms['histo_altshapeUp'] = histo_altshapeUp
		finalHistograms['histo_altshapeUp'] = histo_altshapeUp
		if doPythia:
			histogram_altshapeDown=mirror(finalHistograms['histo_altshapeUp'],finalHistograms['histo_nominal'],"histo_altshapeDown")
			conditional(histogram_altshapeDown)
			histogram_altshapeDown.SetName('histo_altshapeDown')
			histogram_altshapeDown.SetTitle('histo_altshapeDown')
			histogram_altshapeDown.Write()

	if doMadGraph:
		histo_altshape2.Write('histo_altshape2_coarse')
		conditional(histo_altshape2)
		expanded=expandHisto(histo_altshape2,"madgraph")
		conditional(expanded)
		expanded.SetName('histo_altshape2')
		expanded.SetTitle('histo_altshape2')
		expanded.Write('histo_altshape2')
		#histo_altshape2.Write('histo_altshape2')

	os.system('rm -r '+outdir+'_out')
	# os.system('rm -r '+outdir)
	
def makeData(template,cut,rootFile,binsMVV,binsMJ,minMVV,maxMVV,minMJ,maxMJ,factor,name,data,jobname,samples):
	print 
	print 'START: makeData'
	print "template = ",template
	print "cut      = ",cut
	print "rootFile = ",rootFile
	print "binsMVV  = ",binsMVV
	print "binsMJ   = ",binsMJ
	print "minMVV   = ",minMVV
	print "maxMVV   = ",maxMVV
	print "minMJ    = ",minMJ
	print "maxMJ    = ",maxMJ
	print "factor   = ",factor
	print "name     = ",name
	print "data     = ",data
	print "jobname  = ",jobname
	print "samples  = ",samples
	print 

	files = []
	sampleTypes = template.split(',')
	for f in os.listdir(samples):
		for t in sampleTypes:
			if f.find('.root') != -1 and f.find(t) != -1: files.append(f)
 
	NumberOfJobs= len(files) 
	OutputFileNames = rootFile.replace(".root","")
	cmd='vvMakeData.py -d {data} -c "{cut}"  -v "jj_l1_softDrop_mass,jj_l2_softDrop_mass,jj_LV_mass" -b "{bins},{bins},{BINS}" -m "{mini},{mini},{MINI}" -M "{maxi},{maxi},{MAXI}" -f {factor} -n "{name}" {infolder} '.format(cut=cut,BINS=binsMVV,bins=binsMJ,MINI=minMVV,MAXI=maxMVV,mini=minMJ,maxi=maxMJ,factor=factor,name=name,data=data,infolder=samples)	
	queue = "1nd" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
	

	path = os.getcwd()
	try: os.system("rm -r tmp"+jobname)
	except: print "No tmp/ directory"
	os.system("mkdir tmp"+jobname)
	try: os.stat("res"+jobname) 
	except: os.mkdir("res"+jobname)
	print

	#### Creating and sending jobs #####
	joblist = []
	##### loop for creating and sending jobs #####
	for x in range(1, int(NumberOfJobs)+1):
	 
	   os.system("mkdir tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))
	   os.chdir("tmp"+jobname+"/"+str(files[x-1]).replace(".root",""))
	 
	   with open('job_%s.sh'%files[x-1].replace(".root",""), 'w') as fout:
	      fout.write("#!/bin/sh\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	      fout.write("echo 'START---------------'\n")
	      fout.write("echo 'WORKDIR ' ${PWD}\n")
	      fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
	      fout.write("cd "+str(path)+"\n")
	      fout.write("cmsenv\n")
	      fout.write(cmd+" -o "+path+"/res"+jobname+"/"+OutputFileNames+"_"+files[x-1]+" -s "+files[x-1]+"\n")
	      fout.write("echo 'STOP---------------'\n")
	      fout.write("echo\n")
	      fout.write("echo\n")
	   os.system("chmod 755 job_%s.sh"%(files[x-1].replace(".root","")) )
   
	   os.system("bsub -q "+queue+" -o logs job_%s.sh -J %s"%(files[x-1].replace(".root",""),jobname))
	   print "job nr " + str(x) + " submitted"
	   joblist.append("%s"%(files[x-1].replace(".root","")))
	   os.chdir("../..")
   
	print
	print "your jobs:"
	os.system("bjobs")
	userName=os.environ['USER']
	waitForBatchJobs(jobname,NumberOfJobs,NumberOfJobs, userName, timeCheck)
	
	print
	print 'END: makeData'
	print
	return joblist, files

def mergeData(jobname,purity,rootFile):
	
	print "Merging data from job " ,jobname
	print "Purity is " ,purity
	# read out files
	filelist = os.listdir('./res'+jobname+'/')

	mg_files     = []
	pythia_files = []
	herwig_files = []
	data_files   = []

	for f in filelist:
	 #if f.find('COND2D') == -1: continue
	 if f.find('QCD_HT')    != -1: mg_files.append('./res'+jobname+'/'+f)
	 elif f.find('QCD_Pt_') != -1: pythia_files.append('./res'+jobname+'/'+f)
	 elif f.find('JetHT')   != -1: data_files.append('./res'+jobname+'/'+f)
	 else: herwig_files.append('./res'+jobname+'/'+f)

	#now hadd them
	if len(mg_files) > 0:
		cmd = 'hadd -f JJ_nonRes_%s_altshape2.root '%purity
		for f in mg_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)

	if len(herwig_files) > 0:
		cmd = 'hadd -f JJ_nonRes_%s_altshapeUp.root '%purity
		for f in herwig_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)

	if len(pythia_files) > 0:
		cmd = 'hadd -f %s '%rootFile
		for f in pythia_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
	
	if len(data_files) > 0:
		cmd = 'hadd -f JJ_%s.root '%purity
		for f in data_files:
		 cmd += f
		 cmd += ' '
		print cmd
		os.system(cmd)
	print "Done merging data!"
	
def makePseudodata(infile,purity):
	print "Making pseudodata from infile " ,infile
	fin = ROOT.TFile.Open(infile,'READ')
	hmcin = fin.Get('nonRes')
	
	fout = ROOT.TFile.Open('JJ_%s.root'%purity,'RECREATE')
	hout = ROOT.TH3F('data','data',hmcin.GetNbinsX(),hmcin.GetXaxis().GetXmin(),hmcin.GetXaxis().GetXmax(),hmcin.GetNbinsY(),hmcin.GetYaxis().GetXmin(),hmcin.GetYaxis().GetXmax(),hmcin.GetNbinsZ(),hmcin.GetZaxis().GetXmin(),hmcin.GetZaxis().GetXmax())
	hmcout = ROOT.TH3F('nonRes','nonRes',hmcin.GetNbinsX(),hmcin.GetXaxis().GetXmin(),hmcin.GetXaxis().GetXmax(),hmcin.GetNbinsY(),hmcin.GetYaxis().GetXmin(),hmcin.GetYaxis().GetXmax(),hmcin.GetNbinsZ(),hmcin.GetZaxis().GetXmin(),hmcin.GetZaxis().GetXmax())
	hmcout.Add(hmcin)
	
	for k in range(1,hmcin.GetNbinsZ()+1):
	 for j in range(1,hmcin.GetNbinsY()+1):
	  for i in range(1,hmcin.GetNbinsX()+1):
	   evs = hmcin.GetBinContent(i,j,k)*35900.
	   #if evs >= 1:
	   err = math.sqrt(evs)
	   hout.SetBinContent(i,j,k,evs)
	   hout.SetBinError(i,j,k,err)
	
	hout.Write()
	hmcout.Write()
	
	fin.Close()
	fout.Close()