# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:39:04 2021

@author: padma carstens
"""

"""
Purpose: 
-Opens the publication folder created by PubFolder_Download.py. 
-Opens the DART app, adds publication folder items and tag values to DART.
-Runs DART, creates a publication bag at .dart folder
-Uploads the publication bag to the storage services picked in the DART workflow to repo/demo/VT S3 
-Copies non disseminted content to the non disseminated content folder under BAGS folder on google drive
Notes:
Part of this script is built off of "Scripting with DART" code available on APTrust github page. In the scripting with DART code a new job called job.py is created and executed based on a pre-defined DART workflow. 
The publicaiton bag created by DART can also be uploaded to APTrust using APTrust partner tools without using DART app. Documentation for this is also availabla on APTrust github page
"""


#Get the parameters from configurations.ini to retrieve information from an article on Figshare
import configparser
import sys
config=configparser.ConfigParser()
config.read('configurations-bulk.ini')
curPath=config['IngestBag_PathSettings']['IngFolderPath']
sys.path.append(curPath)
sys.path.append(curPath+'/VTDR_RepositoryServices/Figshare-APTrust')
from Read_VTDR_Spreadsheet import vtpubsheet
from Read_VTDR_Spreadsheet import vtingsheet
from turtle import begin_fill
import shutil
from tarfile import TarFile
import job
from job import Job
from cmath import log
import logging
from datetime import datetime
import bagit
import aptCmd
from aptCmd import registryCheck
#Get the parameters from configurations.ini to retrieve information from an article on Figshare

def DownloadPubTrnsfr(workflowVal):
  config=configparser.ConfigParser()
  config.read('configurations-bulk.ini')


# get the ArticleID from configurations 
  ArticleID=config['FigshareSettings']['FigshareArticleID']
# get Published Version number from configurations
  PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
#Get the row information from VTDR spreadsheet for the given article id and version number: 
  Pvtsheet=vtpubsheet(ArticleID=ArticleID,PublishedVersionNumber=PublishedVersionNumber)
#get published accession number
  pPubAccessionNumber= Pvtsheet['gspubnum']
#get ingest accession number
  pIngAccessionNumber=Pvtsheet['gsingestno']
#get the requestor and corresponding author last name first name initial
  pRequestorLFI=Pvtsheet['gsreqlastfi']
  pCorrespondingAuthorLFI=Pvtsheet['gscorrlastfi']
#get version number
  pVersion=Pvtsheet['gsversnum']
#get date published
  pDate=Pvtsheet['gsdatepub']
#get DOI suffix
  pDOIsuffix=Pvtsheet['DOIsuffix']
#get the bag path for large bags
 # sourcedir1=config['PubBagDartAptrust_PathSettings']['LargeBagsPath']

#Get the publication folder created by PubFolder_Download.py
  aptrustBagName=f"VTDR_{pPubAccessionNumber}_{pIngAccessionNumber}_DOI_{pDOIsuffix}_{pCorrespondingAuthorLFI}_v{pVersion}_{pDate}"
  aptrustBagName_tar=f"{aptrustBagName}.tar"
#Source folder is where the publication folder is downloaded, this folder will be bagged by DART
  PubFolderPath=config['PubFolder_PathSettings']['PubFolderPath']
  import os
  import glob
  PubFolder=os.path.join(PubFolderPath,aptrustBagName)
  print("Pub Folder Path ",PubFolder)
  #-------------------------------------------------------------------------
  #Add emails and provenance logs to all the publication folders:
  #Get the publication folder created by PubFolder_Download.py
  #Get the VTCurationServices folder path and copy its contents to the Publication folder:
  # path to source directory
  SRC_DIR =config['VTCurationServicesActionsFolder']['VTCurationServicesActionsFolderPath']
  # path to destination directory
  TARG_DIR = PubFolder+"/VTCurationServicesActions"
#  files = os.listdir(src_dir)
#  shutil.copytree(src_dir, dest_dir)
  GLOB_PARMS = "*" #maybe "*.pdf" ?

  for file in glob.glob(os.path.join(SRC_DIR, GLOB_PARMS)):
    if file not in glob.glob(os.path.join(TARG_DIR, GLOB_PARMS)):
        shutil.copy(file,TARG_DIR)
    else:
        print("{} exists in {}".format(
            file,os.path.join(os.path.split(TARG_DIR)[-2:])))
        # This is just a print command that outputs to console that the
        # file was already in directory
  #--------------------------------------------------------------------------

  
  payload=os.listdir(PubFolder)
  destn_path_sandisk=config['PubFolder_PathSettings']['SanDiskDirPath']
  local_dir_path=config["PubFolder_PathSettings"]["LocalPathBag"]

  workflow=workflowVal
  if workflow == "1":
    jobname="Workflow for depositing bag to APTrust-Demo"
  if workflow == "2":
    jobname="Workflow for depositing bag to APTrust-Repo and VT library S3 bucket"
  if workflow =="3":
    jobname="Workflow for depositing bag to VT library S3 bucket"
  if workflow =="4":
    jobname="Workflow for depositing bag to APTrust-Repo" 
#---------------------------------------   

  if workflow =='2' or workflow =='4':
     checkReg=registryCheck(aptrustBagName)#check aptrust registry return 1 for upload , 0 for terminate upload
  if workflow =='3': 
     checkReg=1
  if (workflow == "1") or (checkReg == 1):
    job=Job(jobname,aptrustBagName)
  #Open the publication folder and add all the files to the DART app to bag them
    for f in payload:
      payloadfilepath=os.path.join(aptrustBagName,f)
      job.add_file(payloadfilepath)
      print("Added following file to bag in DART: ",f)
      logging.info("Added following file to bag in DART: %s " % f)
  
    bag_group_identifier=f"VTDR_{pPubAccessionNumber}"
    job.add_tag("bag-info.txt", "Bag-Group-Identifier", bag_group_identifier)
    job.add_tag("bag-info.txt","Source-Organization","Virginia Tech")
    job.add_tag("aptrust-info.txt", "Access", "Institution")
    job.add_tag("aptrust-info.txt", "Storage-Option", "Standard")
    aptrust_title=aptrustBagName
    job.add_tag("aptrust-info.txt","Title",aptrust_title)
    job.add_tag("bagit.txt","BagIt-Version","0.97")
    job.add_tag("bagit.txt","Tag-File-Character-Encoding","UTF-8")

    exit_code = job.run()
    print("EXIT CODE IS ",exit_code)
    if exit_code == 0:
      print("JOB COMPLETED")
      print("**************************BAG MIGRATED SUCCESSFULLY TO APTRUST/VT S3****************")
    else:
      print("JOB FAILED. Check the DART log for details.")
      print("**************************BAG MIGRATION TO APTRUST/VT S3 FAILED****************")
      quit()

#----------------Copy non disseminated content to a NonDisseminatedContent folder only if it doesnt exist already:-------------------------

    destn_path=config['PubBagDartAptrust_PathSettings']['NonDisseminatedContentPath']
    data_directory=f"NonDisseminatedContent_VTDR_{pPubAccessionNumber}_DOI_{pDOIsuffix}_{pCorrespondingAuthorLFI}_v{pVersion}_{pDate}"
    destndir=os.path.join(destn_path,data_directory)
    count=0

    for root, dirs, files in os.walk(PubFolder):
      print("Root folder is: ",root)
      print("Directories in the root folder are: ", dirs)
      print("\n \n")
      print("Non-Disseminated files in the root folder are", files)
      random_names=os.listdir(PubFolder)
      inner_dirs = [
      os.path.join(PubFolder, name)
      for name in random_names
      if name[:2] == "Dis" or name[:3] =="Diss" or name[0] =="D" or name[0] == "i" or name[0] == "I"
          ]
          
      inner_dirs=" ".join(inner_dirs)
   # print("\n\n")
   # print("Inner Dissemination Directory starting with D or Diss or Dis or i or I is ", inner_dirs,"\n")
      if root==inner_dirs: 
          print("*********************SKIPPING COPYING CONTENTS OF THE DISSEMINATED FOLDER******************************** ")
      else:
          for filename in files:
              print("***************************STARTING COPYING CONTENTS FOR FOLLOWING PATHS*************************")
              print("Current root folder is: ",root)
              print("Directories in this root are: ", dirs)
            #print("files are", files)
              print("COPYING FILE: ",filename)
              print("absolute path of the file is: ",os.path.abspath(root))
              print("copied file to the destination path: ", os.path.join(destndir,filename))
              oldpath=os.path.join(os.path.abspath(root),filename)
              newpath=os.path.join(destndir,filename)
              if not os.path.exists(destndir):
                  print("\n \n")
                  print("Non Disseminated Content folder does not exist on GoogleDrive. So creating it and copying non-disseminated content to the folder: ",destndir)
                  os.mkdir(destndir)
                  shutil.copy(oldpath,newpath)
              if os.path.exists(destndir):
                  print("\n \n")
                  print("Non Disseminated Content folder already exists, so not copying any files from the current non disseminated content publication folder into the already existing non disseminated content folder on googleDrive")                  
            
#----------------Copy Publication bag to SanDisk path defined in generate_config.py:-------------------------
    destn_path_bag=os.path.join(destn_path_sandisk,aptrustBagName_tar)
    localPath=os.path.join(local_dir_path,aptrustBagName_tar)
    if not os.path.exists(destn_path_sandisk):
       print("*************SAN DISK PATH IS NOT FOUND, SO BAG CREATED IS NOT COPIED TO SANDISK*************")
    if os.path.exists(destn_path_sandisk):
      if not os.path.exists(destn_path_bag):
        shutil.copy(localPath,destn_path_sandisk)#shutil.copy(source,destn)
        print("*************COPIED BAG: ",aptrustBagName_tar, " FROM SOURCE: ",localPath," TO: ",destn_path_sandisk,"***************")
      else:
        print("*************BAG IN TAR FORMAT: ",aptrustBagName_tar, "ALREADY EXISTS IN: ",destn_path_sandisk," SO NOT OVERWRITING IT*************")
          
