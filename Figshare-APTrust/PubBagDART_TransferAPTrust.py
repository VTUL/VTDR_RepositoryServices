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


import os
from os.path import exists
from turtle import begin_fill
from ldcoolp.curation import retrieve
from Read_VTDR_Spreadsheet import vtingsheet
from Read_VTDR_Spreadsheet import vtpubsheet
import shutil
from tarfile import TarFile
import job
from job import Job
from cmath import log
import logging
from datetime import datetime
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
import bagit

#Get the parameters from configurations.ini to retrieve information from an article on Figshare

import configparser
config=configparser.ConfigParser()
config.read('configurations.ini')


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
sourcedir1=config['PubBagDartAptrust_PathSettings']['LargeBagsPath']

#Get the publication folder created by PubFolder_Download.py
aptrustBagName=f"VTDR_{pPubAccessionNumber}_{pIngAccessionNumber}_DOI_{pDOIsuffix}_{pCorrespondingAuthorLFI}_v{pVersion}_{pDate}"
aptrustBagName_tar=f"{aptrustBagName}.tar"
#Source folder is where the publication folder is downloaded, this folder will be bagged by DART
PubFolderPath=config['PubFolder_PathSettings']['PubFolderPath']
PubFolder=os.path.join(PubFolderPath,aptrustBagName)
payload=os.listdir(PubFolder)
#************CHANGE THIS TO PICK Demo/Repo for uploading the publication bag created above***************************
#job = Job("Workflow for depositing bag to APTrust-Demo",aptrustBagName)
#job = Job("Workflow for depositing bag to APTrust-Repo and VT library S3 bucket",aptrustBagName)
#job = Job("Workflow for depositing bag to VT library S3 bucket" ,aptrustBagName)
#job = Job("Workflow for depositing bag to APTrust-Repo" ,aptrustBagName)
#workflow=input ("Please enter '1' for APTrust Demo Workflow, '2' for APTrust Production and VT libraries S3 workflow and '3' for VT libraries S3 Workflow:  ")
workflow=input ("Please enter '1' for deposit to APTrust Demo only, '2' for deposit to APTrust-Repo and VT libraries S3 bucket, '3' for deposit to VT libraries S3 bucket only, '4' for deposit to APTrust-Repo only:  ")
if workflow == "1":
    jobname="Workflow for depositing bag to APTrust-Demo"
if workflow =="2":
    jobname="Workflow for depositing bag to APTrust-Repo and VT library S3 bucket"
if workflow =="3":
    jobname="Workflow for depositing bag to VT library S3 bucket"
if workflow =="4":
    jobname="Workflow for depositing bag to APTrust-Repo"    
job=Job(jobname,aptrustBagName)
#Open the publication folder and add all the files to the DART app to bag them
for f in payload:
  job.add_file(aptrustBagName+"\\"+f)
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
if exit_code == 0:
  print("Job completed")
  print("**************************BAG MIGRATED SUCCESSFULLY TO APTRUST/VT S3****************")
else:
  print("Job failed. Check the DART log for details.")
  print("**************************BAG MIGRATION TO APTRUST/VT S3 FAILED****************")

#----------------Copy non disseminated content to a NonDisseminatedContent folder:-------------------------

destn_path=config['PubBagDartAptrust_PathSettings']['NonDisseminatedContentPath']
data_directory=f"NonDisseminatedContent_VTDR_{pPubAccessionNumber}_DOI_{pDOIsuffix}_{pCorrespondingAuthorLFI}_v{pVersion}_{pDate}"
destndir=os.path.join(destn_path,data_directory)
count=0

for root, dirs, files in os.walk(PubFolder):
  print("root is",root)
  print("dir is", dirs)
  print("files are", files)
  random_names=os.listdir(PubFolder)
  inner_dirs = [
  os.path.join(PubFolder, name)
  for name in random_names
  if name[:2] == "Dis" or name[:3] =="Diss" or name[0] =="D" or name[0] == "i" or name[0] == "I"
          ]
          
  inner_dirs=" ".join(inner_dirs)
  print("\n\n")
  print("Inner Dissemination Directory starting with D or Diss or Dis or i or I is ", inner_dirs,"\n")
  if root==inner_dirs: 
      print("*********************SKIPPING COPYING CONTENTS OF THE DISSEMINATED FOLDER******************************** ")
  else:
      for filename in files:
          print("***************************STARTING COPYING CONTENTS FOR FOLLOWING PATHS*************************")
          print("root is",root)
          print("dir is", dirs)
          print("files are", files)
          print("FILENAME is ",filename)
          print("absolute path ",os.path.abspath(root))
          print("destination path ", os.path.join(destndir,filename))
          oldpath=os.path.join(os.path.abspath(root),filename)
          newpath=os.path.join(destndir,filename)
          if not os.path.exists(destndir):
              print("Following directory does not exits for copying contents excluding disseminated folder contents, so creating it: ",destndir, " Now copying file: ", filename)
              os.mkdir(destndir)
              shutil.copy(oldpath,newpath)
          elif not os.path.exists(newpath):
              print("Directory is already created: ", destndir, " But the file: ", filename ," does not exist in this directory so copying it ")
              shutil.copy(oldpath,newpath)
          else:
              print("Directory is already created: ", destndir," file already exists so not copying file: ",filename)
