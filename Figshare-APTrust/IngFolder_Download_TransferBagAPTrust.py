"""
Purpose: 
1. Downloads article in review from figshare using article ID and token. This was built off of UAL-RE ldcoolp code to download article information which was built off of figshare Python code to retrieve article information 
2. Read the ingest row information for the corresponding article in review from "Ingest" sheet in the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Creates ingest dataset folder following VTDR ingest folder naming and APTrust bag naming convention for preservation.
3. Calls and passes tags and ingest folder to DART app through STDIN using a predefined VT workflow. The workflow is created within the DART app. DART creates the ingest bag from the ingest folder in the .dart folder in the local computer. DART also transfers this Ingest bag to APTrust Repo and VT S3 storage, credentials for upload are stored in the DART app. The ingest bag created by DART can also be uploaded to APTrust using APTrust partner tools without using DART app.
"""
import os
import platform 
from os.path import exists
import sys
sys.path.append('figshare')
sys.path.append('curation')
import shutil
from figshare import Figshare
import requests
from requests import HTTPError
import figshareRetrieve
import figshareDownload
import json
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime
from redata.commons.logger import log_stdout
import aptCmd
from aptCmd import registryCheck
import subprocess 

import configparser
config=configparser.ConfigParser()
config.read('configurations.ini')


ArticleID=config['FigshareSettings']['FigshareArticleID']
#Get the Published Version number 
PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
#Get the Ingest Version number 
IngestVersionNumber=config['FigshareSettings']['IngestVersionNumber']
#Get your figshare token 
token=config['FigshareSettings']['token']
#Get curator name 
CuratorName=config['FigshareSettings']['CuratorName']

print("DEBUG ArticleID:", ArticleID, PublishedVersionNumber, IngestVersionNumber)

#Get the row information of the article in review/ingested article from the Ingest sheet using the corresponding ArticleID and Version Number:
#try:
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)


#Get article id
article_id=ingsheet['ingarticleid']

IngestAccessionNumber=ingsheet['ingestno'] 
#get Requestor name
Requestor=ingsheet['ingrequestr']
#get corresponding author name
CorrespondingAuthor=ingsheet['ingrequestr']
#Get LastnameFirstnameinitial of requestor and corresponding auth
Requestorlfi=ingsheet['ingreqlastfirsti']
CorrespondingAuthorlfi=ingsheet['ingcorlastfirsti']

#get version number and time
Version=ingsheet['ingversion']
DateIngested= ingsheet['ingestdate']  
today=date.today()
date_current=today.strftime("%Y%m%d")
now=datetime.now()
time_current=now.strftime("%H_%M_%S")


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
#-----------------------------------------------------------------------------
FileDownload=figshareDownload.download_files(article_id,fversion, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
#privatefigshare_url='https://api.figshare.com/v'+str(Version[1])+'/account/articles/'+str(article_id)
#data_directory=data_directory_path
#metadata_directory=metadata_directory_path
#metadata_only=False
#root_directory=None
#log = None
#-----------------------------------------------------------------------------------------------
#FileDownload=retrieve.download_files(article_id,fversion, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
privatefigshare_url='https://api.figshare.com/v'+str(Version[1])+'/account/articles/'+str(article_id)
json_out_file=f"{data_directory_path}/{IngestAccessionNumber}_IngestedMetadata.json"
json_response=fs.get_article_details(article_id,version=None)

if not os.path.exists(json_out_file):
    with open(json_out_file, 'w') as f:
        json.dump(json_response,f,indent=4)
else:
    print(f"Ingest metadata file already exists as: {json_out_file}")

# ====================================AEC dart-runner Bagit=================================================

aptrustBagName = IngFolderName
aptrustBagName_tar = f"{aptrustBagName}.tar"

dart_runner = config["dart_PathSettings"]["dart_runner_path"]
workflow_json = config["dart_PathSettings"]["workflow_package_only"]

scratch_out = config["IngestBag_PathSettings"]["RunnerOutputDir"]  
final_out = config["IngestBag_PathSettings"]["FinalOutputDir"]   

os.makedirs(scratch_out, exist_ok=True)
os.makedirs(final_out, exist_ok=True)

job_params = {
    "packageName": aptrustBagName_tar,
    "files": [data_directory_path], 
    "tags": [
        {"tagFile": "bag-info.txt", "tagName": "Bag-Group-Identifier", "value": f"VTDR_{IngestAccessionNumber}"},
        {"tagFile": "bag-info.txt", "tagName": "Source-Organization", "value": "Virginia Tech"},
        {"tagFile": "aptrust-info.txt", "tagName": "Access", "value": "Institution"},
        {"tagFile": "aptrust-info.txt", "tagName": "Storage-Option", "value": "Standard"},
        {"tagFile": "aptrust-info.txt", "tagName": "Title", "value": aptrustBagName},
        {"tagFile": "bagit.txt", "tagName": "BagIt-Version", "value": "0.97"},
        {"tagFile": "bagit.txt", "tagName": "Tag-File-Character-Encoding", "value": "UTF-8"},
    ]
}

print("Running dart-runner (package-only workflow, no upload)...")
p = subprocess.run(
    [dart_runner, f"--workflow={workflow_json}", f"--output-dir={scratch_out}", "--delete=false"],
    input=json.dumps(job_params),
    text=True,
    capture_output=True
)

print("dart-runner stdout:\n", p.stdout)
if p.stderr.strip():
    print("dart-runner stderr:\n", p.stderr, file=sys.stderr)

if p.returncode != 0:
    raise RuntimeError(f"dart-runner failed with exit code {p.returncode}")

# ✅ Copy tar from scratch to final project location
scratch_tar_path = os.path.join(scratch_out, aptrustBagName_tar)
final_tar_path = os.path.join(final_out, aptrustBagName_tar)

if not os.path.exists(scratch_tar_path):
    raise FileNotFoundError(f"Expected tar not found: {scratch_tar_path}")

# Avoid overwrite
if os.path.exists(final_tar_path):
    # add a timestamp suffix to avoid collision
    final_tar_path = os.path.join(final_out, f"{aptrustBagName}_{date_current}_{time_current}.tar")

shutil.copy2(scratch_tar_path, final_tar_path)
print(f"✅ Bag copied to: {final_tar_path}")