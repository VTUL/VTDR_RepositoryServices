# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:39:04 2021

@author: padma carstens
"""

import os
from os.path import exists
from figshare.figshare import Figshare
from ldcoolp.curation.UPack_v2 import ObjFormatter
from ldcoolp.curation import retrieve
import json
from spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime

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
#Get the Version number from secrets.txt:
VersionNumber=params["VersionNumber"]
#Get figshare token from secrets.txt:
token=params["token"]

# Get the ingest record creation number from secrets.txt:(Is this the first time creating ingest record or nth time to check against the originial bag?)
ingestrecord_creation_number=int(params["ingestrecord_creation_number"])

#Get information from the spreadsheet for the corresponding ArticleID and Version Number:
ingsheet=vtingsheet(ArticleID,VersionNumber)
#Get article id
article_id=ingsheet['ingarticleid']
# get Ingest Accession Number 
IngestAccessionNumber=ingsheet['ingestno'] 
#get Requestor name
Requestor=ingsheet['ingrequestr']
#get corresponding author name
CorrespondingAuthor=ingsheet['ingrequestr']
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
#For the first run follow the IXXXX->IXXXX_author_requestor_version_dateingested-> to download data, for all the other runs compare with the first run dataset
if ingestrecord_creation_number == 1:
    #Create Ingest folder to store dataset
    data_directory1=f"{IngestAccessionNumber}"
elif ingestrecord_creation_number > 1:
    data_directory1=f"{IngestAccessionNumber}_{date_current}_{time_current}"
data_directory2=f"{IngestAccessionNumber}_{Requestor}_{CorrespondingAuthor}_v{Version}_{DateIngested}"
data_directory_path=os.path.join(data_directory1, data_directory2)
metadata_directory_path=f"{IngestAccessionNumber}_DownloadedFileMetadata"


#-----Download dataset for private article under review using LD-Cool-P and save it as Ingest metadata in json file format
fs=Figshare(token=token,private=True)
FileDownload=retrieve.download_files(article_id, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
privatefigshare_url='https://api.figshare.com/v2/account/articles/'+str(article_id)
#-----Get article details for private article under review using LD-Cool-P and save it as Ingest metadata in json file format
json_out_file=f"{data_directory_path}/{IngestAccessionNumber}_IngestedMetadata.json"
json_response=fs.get_article_details(article_id,version=None)

if not os.path.exists(json_out_file):
    with open(json_out_file, 'w') as f:
        json.dump(json_response,f,indent=4)
else:
    print(f"File exists: {json_out_file}")
    if overwrite:
        print("Overwriting!")
        with open(json_out_file, 'w') as f:
            json.dump(json_response,f,indent=4)


if ingestrecord_creation_number == 2:
 data_directory_check=f"{IngestAccessionNumber}"
 data_directory_path_check=os.path.join(data_directory_check, data_directory2, "data")
 
 #for IngestAcessionNumber_IngestedMetadata.json in os.listdir(data_directory_path_check):
 file1_path = os.path.join(data_directory_path_check, f"{IngestAccessionNumber}_IngestedMetadata.json")
 file2_path = os.path.join(data_directory_path, f"{IngestAccessionNumber}_IngestedMetadata.json")
 result=filecmp.cmp(file1_path,file2_path)
 #Print true or false if the files match/dont match
 print("Do the files match: ",result)

#Call parts of modified UPACK_v2 code written by Luke. I. Menzies(lmenzies@uab.edu) to bag and tar ingest record

myobj=ObjFormatter#()
tarfiledir=data_directory1
ingest_bag=myobj.run_bagit(bagsdir=tarfiledir)
ingest_bag_tar=myobj.run_tar(tarfolder=tarfiledir)

