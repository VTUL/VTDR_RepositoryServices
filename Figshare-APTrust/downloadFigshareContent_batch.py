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
#FigshareArticleID=["24328498"]#,"26860051"],"26086258","25267117","24749499","24328498"] 
#Publication test:
FigshareArticleID=["23646627","21818604","21538380"]

#------------------------Assign PubVerNum's
#Get the number of article ids to be bagged:
n=len(FigshareArticleID)
#Assign version '01' to all the publication ids
PubVerNum=["01" for x in range(n)] 
#Comment out above and uncomment below if PubVerNum is not "01" for that particular Figshare Article ID. Number of elements in figshare article ids must match the number of elements in PubVerNums, and the elements correspond to each other, for eg for ID 54545 if version number is 2, it should look like this: FigshareArticleID=["34343","54545"], PubVerNum=["01","02"]

#PubVerNum=["01","02","01","03"]

#---------------------
import sys
import configparser
#import generate_config_batch
from generate_config_batch import configurations
#generate config batch with a random test id:
x=configurations("24328498","01")
sys.path.append('curation')
import aptCmd
from aptCmd import registryCheck
import Read_VTDR_Spreadsheet
from Read_VTDR_Spreadsheet import vtingsheet
import os
from redata.commons.logger import log_stdout
from PubFolder_Download_batch import DownloadPub
from PubBagDART_TransferAPTrust_batch import DownloadPubTrnsfr
import AutomatedREADMErtf_batch
from AutomatedREADMErtf_batch import create_readme_batch
import hashlib
import json
from figshareUploadFile import upload_part,initiate_new_upload,complete_upload,upload_parts

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
#Testing:
#DwnldContnt='Ing' #Pub Input 
#DwnldContnt='Pub' #Pub Input 
#DwnldContnt='PubTransfer' #Pub Input 
#----------------------------------------------


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
#testing:
#workflowVal='1'

for i in range(n) :
 # print("STARTING CONFIGURATIONS")
  print("Working on the Figshare article ID: ",FigshareArticleID[i])
 # quit()
  print(os.getcwd())
  #Declare the configurations for the current figshare ID
  x=configurations(FigshareArticleID[i],PubVerNum[i])
  #Bagging Ingest/in review content:
  if DwnldContnt=='Ing': 
    #########Download and transfer Ingest/Before-review bag to aptrust
    from IngFolder_Download_TransferBagAPTrust_batch import DownloadIngest
    DwnldIngOrPubx=DownloadIngest(workflowVal)

    ##########Create the README file for the article in review:
    config=configparser.ConfigParser()
    config.read('configurations-batch.ini')
    #Get your figshare token 
    token=config['FigshareSettings']['token']
    READMEPath=config['AutomatedREADMEPathSettings']['README_Dir']
    readmefile=create_readme_batch(FigshareArticleID[i],token,READMEPath)
    ##########

    ##########Upload README file to figshare article in review:
    FILE_PATH=readmefile
    file_info=initiate_new_upload(FigshareArticleID[i],FILE_PATH)
    # use the figshare upload service API to upload file:
    upload_parts(file_info,FILE_PATH)
    # use figshare api to complete process:
    complete_upload(FigshareArticleID[i], file_info['id'])
    ######################

  #Bagging published content:
  if DwnldContnt=='Pub': 
    print("Working on the Figshare article ID: ",FigshareArticleID[i])
    #quit()
    # Download Published article content from figshare:
    DwnldIngOrPubx=DownloadPub()
    # Transfer Downloaded content to aptrust, after adding non disseminated content:
    DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)


