#!/usr/bin/env python
'''
downloadFigshareContent_batch.py
Created on   2024/10/01 13:34:59
@author  :   padma carstens 
'''
"""
Purpose:
download content from figshare for the provided article ids and transfer content to aptrust. VTcuration services actions folder path is defined in generate_config_batch.py and stores the emails. Prov log is created and moved to VTCurServActions folder for publication folder. Readme file is created and moved to Disseminated content folder for published content

Input: 
Ing/Pub: Ing for ingest content, provide figshare article ids on line 20 for ingesting and transferring articles in the format on line 16. Pub for publication content, provide figshare article ids on line 20 for published articles in the same format on line 16
aptrust repo/demo: input workflow value of 1 for demo and 4 for repo 
FighsareArticleIDs are provided as an array of article IDs. For Eg:
Enter article ids as follows(Ingest/Pub):
FigshareArticleID=["26860051","26781466","26086258","25267117","24749499","24328498"]

"""
#ENTER ARTICLE IDS 
#Ingest test:
FigshareArticleID=["26860051","24328498"]#6781466","26086258","25267117","24749499","24328498"]
#Publication test:
FigshareArticleID=["23646627","21818604","21538380"]
#------------------------------------
import sys
import configparser
#import generate_config_batch
from generate_config_batch import configurations
#DONT CHANGE THE FOLLOWING CONF GENERATION FOR TEST ARTICLE
#TestGen=configurations("24328498","01")
#config=configparser.ConfigParser()
#------------------------------
#config.read('configurations-batch.ini')
#curPath=config['IngestBag_PathSettings']['IngFolderPath']
#print(curPath)#stop
#sys.path.append(curPath)
#sys.path.append(curPath+'/VTDR_RepositoryServices/Figshare-APTrust')
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

#----------INPUT ING/PUB FROM CURATOR------------------
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
n=len(FigshareArticleID)
PubVerNum=["01" for x in range(n)] 

#------------INPUT FROM USER IF TRANSFER IS TO DEMO OR REPO
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
  print("Fig article ID is",FigshareArticleID[i])
 # quit()
  print(os.getcwd())
  x=configurations(FigshareArticleID[i],PubVerNum[i])

  if DwnldContnt=='Ing': 
    from IngFolder_Download_TransferBagAPTrust_batch import DownloadIngest
    DwnldIngOrPubx=DownloadIngest(workflowVal)
    
  if DwnldContnt=='Pub': 
    print("Fig article ID is",FigshareArticleID[i])
    #quit()
    DwnldIngOrPubx=DownloadPub()
    DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)
   # quit()
  #if DwnldContnt=='PubTransfer': 
  #  DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)

