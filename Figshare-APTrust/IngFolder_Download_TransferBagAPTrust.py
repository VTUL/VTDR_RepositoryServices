# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:39:04 2021

@author: padma carstens
"""

"""
Purpose: 
1. Downloads article in review from figshare using article ID and token. This was built off of UAL-RE ldcoolp code to download article information which was built off of figshare Python code to retrieve article information 
2. Read the ingest row information for the corresponding article in review from "Ingest" sheet in the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Creates ingest dataset folder following VTDR ingest folder naming and APTrust bag naming convention for preservation.
3. Calls and passes tags and ingest folder to DART app through STDIN using a predefined VT workflow. The workflow is created within the DART app. DART creates the ingest bag from the ingest folder in the .dart folder in the local computer. DART also transfers this Ingest bag to APTrust Repo and VT S3 storage, credentials for upload are stored in the DART app. The ingest bag created by DART can also be uploaded to APTrust using APTrust partner tools without using DART app.
"""
import os
from os.path import exists
import sys
#sys.path.insert(0,'C:/Users/padma/anaconda3/envs/curation/figshare/figshare')
#sys.path.insert(0,'C:/Users/padma/anaconda3/envs/curation/figshare')
#sys.path.insert(0,'C:/Users/padma/anaconda3/envs/curation')
#sys.path.insert(0,'C:/Users/padma/anaconda3/envs/curation/figshare/figshare')
#import figshare
from figshare.figshare import Figshare
from ldcoolp.curation import retrieve
import json
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime
import job
from job import Job

#Get the parameters from configurations.ini to retrieve information from an article on Figshare

import configparser
#config=configload.read_config()
config=configparser.ConfigParser()
config.read('configurations.ini')


#Get the ArticleID
ArticleID=config['FigshareSettings']['FigshareArticleID']
#Get the Published Version number 
PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
#Get the Ingest Version number 
IngestVersionNumber=config['FigshareSettings']['IngestVersionNumber']
#Get your figshare token 
token=config['FigshareSettings']['token']
#Get curator name 
CuratorName=config['FigshareSettings']['CuratorName']


#Get the row information of the article in review/ingested article from the Ingest sheet using the corresponding ArticleID and Version Number:
#try:
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)
    #break
#except TypeError:
#    print("Oops! No row with the given article id and ingest version number was found in the Ingest sheet")
#    raise TypeError
#finally:
#    print("Goodbye, see you later aligator")
    #break
    #raise
    #pass
    #break
    #raise TypeError("Oops! No row with the given article id and ingest version number was found in the Ingest sheet")
#Get article id
article_id=ingsheet['ingarticleid']
# get Ingest Accession Number 
IngestAccessionNumber=ingsheet['ingestno'] 
#get Requestor name
Requestor=ingsheet['ingrequestr']
#get corresponding author name
CorrespondingAuthor=ingsheet['ingrequestr']
#Get LastnameFirstnameinitial of requestor and corresponding author:
Requestorlfi=ingsheet['ingreqlastfirsti']
CorrespondingAuthorlfi=ingsheet['ingcorlastfirsti']

#get version number
Version=ingsheet['ingversion']
#get date ingested in YYYYMMDD format
DateIngested= ingsheet['ingestdate']  
#get current date
today=date.today()
date_current=today.strftime("%Y%m%d")
#get current time
now=datetime.now()
time_current=now.strftime("%H_%M_%S")

#Download large datasets to SanDisk:
#directory1=config['IngestBag_Download_TransferAPTrustPathSettings']['SanDiskDirPath']
#directory2=f"VTDR_{IngestAccessionNumber}_{Requestorlfi}_{CorrespondingAuthorlfi}_v{Version}_{DateIngested}"
#data_directory_path=os.path.join(directory1,directory2)

#------------------STEP 1------------------------------------------------------------------------
#Create Ingest folder using VTDR folder convention for ingest preservation
IngFolderPath=config["IngestBag_PathSettings"]['IngFolderPath']
IngFolderName=f"VTDR_{IngestAccessionNumber}_{Requestorlfi}_{CorrespondingAuthorlfi}_v{Version}_{DateIngested}"
data_directory_path=os.path.join(IngFolderPath,IngFolderName)
metadata_jsonpath=config["IngestBag_PathSettings"]['metadatajsonpath']
metadata_filename=f"{IngestAccessionNumber}_DownloadedFileMetadata"
metadata_directory_path=os.path.join(metadata_jsonpath,metadata_filename)


#-------------------------------------------------------------------------------------------------

#------------------STEP 2-------------------------------------------------------------------------
# Download private article under review to the ingest folder created in step 1, save Ingest metadata in json file format, there is no versioning in ingest so set version to None
fversion=None
fs=Figshare(token=token,private=True,version=fversion)

FileDownload=retrieve.download_files(article_id,fversion, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
privatefigshare_url='https://api.figshare.com/v'+str(Version[1])+'/account/articles/'+str(article_id)
json_out_file=f"{data_directory_path}/{IngestAccessionNumber}_IngestedMetadata.json"
json_response=fs.get_article_details(article_id,version=None)

if not os.path.exists(json_out_file):
    with open(json_out_file, 'w') as f:
        json.dump(json_response,f,indent=4)
else:
    print(f"File exists: {json_out_file}")

#-----------------STEP 3---------------------------------------------------------------------------
#Bag the ingest folder with DART using tar format, transfer the Ingest bag to VT S3/ APTrust demo/ APTrust repo

payload=os.listdir(data_directory_path)
aptrustBagName=IngFolderName
#Create APTrust Demo/Production workflow in the DART app before running this script, this workflow created should also includes the credentials for the preferred storage i.e. aptrust repo/demo or VT s3
#job = Job("Workflow for depositing bag to APTrust-Demo",aptrustBagName)
#job = Job("Workflow for depositing bag to APTrust-Repo and VT library S3 bucket",aptrustBagName)
#job = Job("Workflow for depositing bag to VT library S3 bucket" ,aptrustBagName)
#job = Job("Workflow for depositing bag to APTrust-Repo" ,aptrustBagName)

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
workflow=str(workflow)
if workflow == "1":
    jobname="Workflow for depositing bag to APTrust-Demo"
if workflow =="2":
    jobname="Workflow for depositing bag to APTrust-Repo and VT library S3 bucket"
if workflow =="3":
    jobname="Workflow for depositing bag to VT library S3 bucket"
if workflow =="4":
    jobname="Workflow for depositing bag to APTrust-Repo"    

job=Job(jobname,aptrustBagName)
for f in payload:
    datapath=os.path.join(data_directory_path,f)
    job.add_file(datapath)
    #job.add_file(data_directory_path+"\\"+f)
    print("Added following file to bag in DART: ",f)
    bag_group_identifier=f"VTDR_{IngestAccessionNumber}"
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

     