#i=219
import os
from os.path import exists
import json
from turtle import begin_fill
#from typing import _KT_co
from ldcoolp.curation import retrieve
import spreadsheet_aptrust_transfer
#from auto_fill_archive import create_archivalreadme
from spreadsheet_aptrust_transfer import aptrust_vtingsheet
from spreadsheet_aptrust_transfer import aptrust_vtpubsheet
import shutil
import tarfile
from tarfile import TarFile
import job
from job import Job
from cmath import log
import logging
from datetime import datetime
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
import filecomparetestmod
from filecomparetestmod import comparemd5txt
#from test_md5 import md5sum

#from bagvalid import s3bagvalid
import bagit

ivtsheet=aptrust_vtingsheet()
#Get article id 
iArticleid=ivtsheet['iArticleid']
iDOIsuffix=ivtsheet['iDOIsuffix']
#get requestor name
iRequestor=ivtsheet['iRequestor']
#get corresponding author name
iCorrespondingAuthor=ivtsheet['iCorAuth']
#get version
iVersion=ivtsheet['iVersion']
#get ingested date in YYYYMMDD format 
iDate= ivtsheet['iDate'] 

#Create Ingest folder to store dataset
iIngAccessionNumber= ivtsheet['iIngestnum']
iRequestorLFI=ivtsheet['iReqLnameFini']
iCorrespondingAuthorLFI=ivtsheet['iCorLnameFini']

Pvtsheet=aptrust_vtpubsheet()
pPubAccessionNumber= Pvtsheet['pPubnum']
pIngAccessionNumber=Pvtsheet['pIngestnum']
pRequestorLFI=Pvtsheet['pReqLnameFini']
pCorrespondingAuthorLFI=Pvtsheet['pCorLnameFini']
#get version
pVersion=Pvtsheet['pVersion']
pDate=Pvtsheet['pDate']
pDOIsuffix=Pvtsheet['pDOIsuffix']
sourcedir1="F:/VTechbags"
count=0
IngOrPub ='P'
###Example of range for the for loop below: i=42 gets the row 43 which is the bag P00041, i=42,53 runs until i=52 and terminates when i=53, so last bag corresponds to i=52,row 53 which is P00050
for i in range(220,221):
  if IngOrPub=='P':
    aptrustBagName=f"VTDR_{pPubAccessionNumber[i]}_{pIngAccessionNumber[i]}_DOI_{pDOIsuffix[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}"
    aptrustBagName_tar=f"{aptrustBagName}.tar"

  if IngOrPub=='I':
    aptrustBagName=f"VTDR_{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}"
  
  #Source folder is where the publication bag is at, the bag made that needs to be tarred by DART
  PubFolderPath='C:/Users/padma/anaconda3/envs/curation'
  PubFolder=os.path.join(PubFolderPath,aptrustBagName)
  payload=os.listdir(PubFolder)
#************CHANGE THIS TO PICK Demo/Repo***************************
  #job = Job("APTrust Demo Workflow for Virginia Tech",aptrustBagName)
  job = Job("APTrust Production Workflow for Virginia Tech",aptrustBagName)
  for f in payload:
    job.add_file(aptrustBagName+"\\"+f)
    print("Added following file to bag in DART: ",f)
    logging.info("Added following file to bag in DART: %s " % f)
       
  if IngOrPub=='I':
    bag_group_identifier=f"VTDR_{iIngAccessionNumber[i]}"
    job.add_tag("bag-info.txt", "Bag-Group-Identifier", bag_group_identifier)
  if IngOrPub=='P':
    bag_group_identifier=f"VTDR_{pPubAccessionNumber[i]}"
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
    print("**************************BAG MIGRATED SUCCESSFULLY TO APTRUST****************")
  else:
    print("Job failed. Check the DART log for details.")
    print("**************************BAG MIGRATION TO APTRUST FAILED****************")

#----------------Copy non disseminated content to a different location:-------------------------
  
  if IngOrPub=='P':    
    destn_path="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/NonDisseminatedContent"
    data_directory=f"NonDisseminatedContent_VTDR_{pPubAccessionNumber[i]}_DOI_{pDOIsuffix[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}"
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
            else:
                print("Directory is already created: ", destndir," file already exists so not copying file: ",filename)
