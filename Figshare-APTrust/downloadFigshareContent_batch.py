#!/usr/bin/env python
'''
downloadFigshareContent_batch.py
Created on   2024/10/01 13:34:59
@author  :   padma carstens 
@co-author: jonathan petters
'''
"""
Purpose:
downloadFigshareContent_batch.py calls functions defined in the scripts: generate_config_batch.py, IngFolder_Download_TransferBagAPTrust_batch.py, PubBagDART_TransferAPTrust_batch.py and AutomatedProvenanceLog_batch.py
The following actions are performed by running this script:
-download content from figshare for the provided "FigsareArticleID"s at the start of the script and transfer content to aptrust. 
-VTcuration services actions folder path is defined in generate_config_batch.py and stores the emails. 
-Prov log is created and moved to VTCurServActions folder for publication folder. 
-Readme file is created and moved to Disseminated content folder for published content
Note: The only place ARTICLE IDs need to be entered is under FigshareArticleID at the beginning of the script

Input from user: 
-FighsareArticleIDs are provided as an array of article IDs. For Eg:
Enter article ids as follows(Ingest/Pub):
FigshareArticleID=["26860051","26781466","26086258","25267117","24749499","24328498"]
When the script is run, it will ask to input 'Ing' for ingest bagging or 'Pub' for publication bagging.
When the script is run, it will ask to input '1' for transferring bag to aptrust demo and 4 for transferring bag to aptrust repo 


"""
#ENTER ARTICLE IDS that need to be ingested/published article ids that need to be bagged:
#Ingest test:
FigshareArticleID=["26860051","24328498"]#6781466","26086258","25267117","24749499","24328498"]
#Publication test:
#FigshareArticleID=["23646627","21818604","21538380"]
#------------------------------------
import sys
import configparser
#import generate_config_batch
from generate_config_batch import configurations
sys.path.append('curation')
import aptCmd
from aptCmd import registryCheck
import Read_VTDR_Spreadsheet
from Read_VTDR_Spreadsheet import vtingsheet
import os
import platform 
import shutil
import requests
import job
import figshareRetrieve
import figshareDownload
import json
import filecmp
import shutil
import os
from figshare import Figshare
from requests import HTTPError
from datetime import date
from datetime import datetime
from job import Job
from redata.commons.logger import log_stdout
from PubFolder_Download_batch import DownloadPub
from PubBagDART_TransferAPTrust_batch import DownloadPubTrnsfr

#----------INPUT 'Ing'/'Pub' FROM CURATOR------------------
while True:
  #try:
    IngOrPub=input("Please enter '1' for Ing transfer to APTrust or '2' for Pub transfer to APTrust: ")
    try:
        IngOrPub=int(IngOrPub)
      #break
    except ValueError:
        print("Oops! That was not a valid number. Try again")
        continue
    if 1 <= IngOrPub <= 2:
        break
    else:
        print("Please pick number 1 or 2")
IngOrPub=str(IngOrPub)
if IngOrPub=="1":
  DwnldContnt="Ing"
if IngOrPub=="2":
  DwnldContnt="Pub"
print('You selected to download ',DwnldContnt," content")
#----------------------------------------
#DwnldContnt='Ing' #Pub Input 
#DwnldContnt='Pub' #Pub Input 
#DwnldContnt='PubTransfer' #Pub Input 
#----------------------------------------------
#Get the number of article ids to be bagged:
n=len(FigshareArticleID)
#Assign version '01' to all the publication 
PubVerNum=["01" for x in range(n)] 

#------------INPUT '1' for aptrust demo or '4' for aptrust repo and other values
def workflowValue():
    while True:
  #try:
      workflow=input("Please enter '1' for deposit to APTrust Demo only, '2' for deposit to APTrust-Repo and VT libraries S3 bucket, '3' for deposit to VT libraries S3 bucket only, '4' for deposit to APTrust-Repo only:  ")
      try:
          workflow=int(workflow)
      #break
      except ValueError:
          print("Oops! That was not a valid number. Try again")
          continue
      if 1 <= workflow <= 4:
          break
      else:
          print("Please pick a workflow number between 1 and 4")
    workflowStr=str(workflow)
    return workflowStr
workflowVal=workflowValue()
if workflowVal=='1': 
  print("You picked to transfer content to AptrustDemo")
if workflowVal=='4': 
  print("You picked to transfer to AptrustRepo")
#quit()
#-------------------------------------
#workflowVal='4'

for i in range(n) :
 # print("STARTING CONFIGURATIONS")
  print("Working on the Figshare article ID: ",FigshareArticleID[i])
 # quit()
  print(os.getcwd())
  x=configurations(FigshareArticleID[i],PubVerNum[i])
  #Bagging Ingest/in review content:
  if DwnldContnt=='Ing': 
    from IngFolder_Download_TransferBagAPTrust_batch import DownloadIngest
    DwnldIngOrPubx=DownloadIngest(workflowVal)
  #Bagging published content:
  if DwnldContnt=='Pub': 
    print("Working on the Figshare article ID: ",FigshareArticleID[i])
    #quit()
    DwnldIngOrPubx=DownloadPub()
    DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)
   # quit()
  #if DwnldContnt=='PubTransfer': 
  #  DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)

