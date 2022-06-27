# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:39:04 2021

@author: padma carstens
"""

import os
from os.path import exists
from figshare.figshare import Figshare
from UPack_v2 import ObjFormatter
from ldcoolp.curation import retrieve
import json
from spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime
import job
from job import Job
#from fill_readme import create_readme

filename="secrets.txt"
fileObj=open(filename)
params={}
for line in fileObj:
    line=line.strip()
    key_value=line.split('=')
    if len(key_value)==2:
        params[key_value[0].strip()]=key_value[1].strip()


#Get ArticleID from secrets.txt:
ArticleID=params["ArticleID"]
#Get the Published Version number from secrets.txt
PublishedVersionNumber=params["PublishedVersionNumber"]
#Get the Ingest Version number from secrets.txt
IngestVersionNumber=params["IngestVersionNumber"]
#Get your figshare token from secrets.txt
token=params["token"]
#Get curator name from secrets.txt
#readme_auto=create_readme(ArticleID,token)
CuratorName=params["CuratorName"]
#Enter the ingest record creation number: (Is this the first time creating ingest record or nth time to check against the originial bag?)
ingestrecord_creation_number=int(params["ingestrecord_creation_number"])
#Get information from the spreadsheet for the corresponding ArticleID and Version Number:
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)
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

data_directory_path=f"VTDR_{IngestAccessionNumber}_{Requestorlfi}_{CorrespondingAuthorlfi}_v{Version}_{DateIngested}"

metadata_directory_path=f"{IngestAccessionNumber}_DownloadedFileMetadata"

#-----Download dataset for private article under review using LD-Cool-P and save it as Ingest metadata in json file format
fs=Figshare(token=token,private=True)
FileDownload=retrieve.download_files(article_id, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
#privatefigshare_url='https://api.figshare.com/v2/account/articles/'+str(article_id)
privatefigshare_url='https://api.figshare.com/v'+str(Version[1])+'/account/articles/'+str(article_id)
#-----Get article details for private article under review using LD-Cool-P and save it as Ingest metadata in json file format
json_out_file=f"{data_directory_path}/{IngestAccessionNumber}_IngestedMetadata.json"
json_response=fs.get_article_details(article_id,version=None)

if not os.path.exists(json_out_file):
    with open(json_out_file, 'w') as f:
        json.dump(json_response,f,indent=4)
else:
    print(f"File exists: {json_out_file}")


#bagging with DART using tar format

payload=os.listdir(data_directory_path)
aptrustBagName=data_directory_path
#job = Job("APTrust Demo Workflow for Virginia Tech",aptrustBagName)
#
job = Job("APTrust Production Workflow for Virginia Tech",aptrustBagName)
for f in payload:
    job.add_file(data_directory_path+"\\"+f)
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
    print("**************************BAG MIGRATED SUCCESSFULLY TO APTRUST****************")

else:
    print("Job failed. Check the DART log for details.")
    print("**************************BAG MIGRATION TO APTRUST FAILED****************")

     