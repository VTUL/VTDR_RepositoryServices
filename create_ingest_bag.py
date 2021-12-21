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
#For the first run follow the IXXXX->IXXXX_author_requestor_version_dateingested-> to download data, for all the other runs compare with the first run dataset
if ingestrecord_creation_number == 1:
    #Create Ingest folder to store dataset
    data_directory1=f"{IngestAccessionNumber}"
elif ingestrecord_creation_number > 1:
    data_directory1=f"{IngestAccessionNumber}_{date_current}_{time_current}"
data_directory2=f"{IngestAccessionNumber}_{Requestorlfi}_{CorrespondingAuthorlfi}_v{Version}_{DateIngested}"
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
#    if overwrite:
#        print("Overwriting!")
#        with open(json_out_file, 'w') as f:
#            json.dump(json_response,f,indent=4)


if ingestrecord_creation_number == 2:
 rootd=os.getcwd()
 data_directory_check=f"{IngestAccessionNumber}"
 data_directory_path_check=os.path.join(data_directory_check, data_directory2, "data")
 compath=os.path.join(rootd,data_directory_check,data_directory2,"data")
 compath1=os.path.join(rootd,data_directory1,data_directory2)
 list=os.listdir(compath)
 no=len(list)
 print("Number of files in the original bag: ",no)
 list1=os.listdir(compath1)
 no1=len(list1)
 print("Number of files in the current new ingest bag: ",no1)
 dc = filecmp.dircmp(compath, compath1)
 print(f"output \n *** Printing detaile report: \n ")
 print(dc.report())
 print(f"\n")
 print(dc.report_full_closure())

#Call parts of modified UPACK_v2 code written by Luke. I. Menzies(lmenzies@uab.edu) to bag and tar ingest record

myobj=ObjFormatter#()
tarfiledir=data_directory1
ingest_bag=myobj.run_bagit(bagsdir=tarfiledir)
ingest_bag_tar=myobj.run_tar(tarfolder=tarfiledir)

