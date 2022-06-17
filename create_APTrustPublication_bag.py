# -*- coding: utf-8 -*-

"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""

import os
from os.path import exists
import json
from ldcoolp.curation import retrieve
from auto_fill_archive import create_archivalreadme
from spreadsheet import vtpubsheet
from spreadsheet import vtingsheet
import shutil
import os
#Get the parameters from secrets.txt created in the curation folder
filename="secrets.txt"
fileObj=open(filename)

params={}
for line in fileObj:
    line=line.strip()
    key_value=line.split('=')
    if len(key_value)==2:
        params[key_value[0].strip()]=key_value[1].strip()

#Get the article id from secrets.txt 
ArticleID=params["ArticleID"]
#Get the Published Version number from secrets.txt
PublishedVersionNumber=params["PublishedVersionNumber"]
#Get the Ingest Version number from secrets.txt
IngestVersionNumber=params["IngestVersionNumber"]
#Get your figshare token from secrets.txt
token=params["token"]
#Get curator name from secrets.txt
CuratorName=params["CuratorName"]
#Get figshare version for published articles
FigVersion=params["FigVersion"]

#get the details from the spreadsheet:
vtsheet=vtpubsheet(ArticleID,PublishedVersionNumber)
#Get article id 
article_id=vtsheet['gsarticleid']
#get requestor name
Requestor=vtsheet['gsrequestr']
#get corresponding author name
CorrespondingAuthor=vtsheet['gscorsauth']
#get version
Version=vtsheet['gsversnum']
#get published date in YYYYMMDD format 
DatePublished= vtsheet['gsdatepub'] 
#get DOI suffix
DOIsuffix=vtsheet['DOIsuffix']


#Create Publication folder to store dataset
PublishedAccessionNumber= vtsheet['gspubnum']
RequestorLFI=vtsheet['gsreqlastfi']
CorrespondingAuthorLFI=vtsheet['gscorrlastfi']


#************INGEST SHEET INFO
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)
IngestAccessionNumber=ingsheet['ingestno'] 

#********************************
#Get current directory:
directory_path=os.getcwd()  

aptrustBagName=f"VTDR_{PublishedAccessionNumber}_{IngestAccessionNumber}_DOI_{DOIsuffix}_{CorrespondingAuthorLFI}_v{Version}_{DatePublished}"
payload_directory1=f"DisseminatedContent"
data_directory_path=os.path.join(aptrustBagName, payload_directory1)
metadata_directory_path=f"{PublishedAccessionNumber}_DownloadedFileMetadata_v{Version}"

#-----Download dataset for published article using LD-Cool-P UAL and save it as publication meta data in json file format
publicfigshare_url='https://api.figshare.com/'+str(FigVersion[1])+'/articles/'+str(article_id)
from figshare.figshare import Figshare
fs=Figshare(token=token,private=False)
FileDownload=retrieve.download_files(article_id, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)

#-----get article details for published article using LD-Cool-P and save it as published metadata in json file format
json_out_file1=f"{data_directory_path}/{PublishedAccessionNumber}_DisseminatedMetadata.json"
json_response1=fs.get_article_details(article_id,version=None)


if not os.path.exists(json_out_file1):
    with open(json_out_file1, 'w') as f:
        json.dump(json_response1,f,indent=4)
else:
    print(f"File exists: {json_out_file1}")

archival_directory=os.path.join(aptrustBagName)
#create archival readme file using auto_fill_archive.py

reme=create_archivalreadme(ArticleID,PublishedVersionNumber,IngestVersionNumber,CuratorName,archival_directory) 
#----------------------create VTCurationServicesActions folder to save provenance log and email correspondence
                
payload_directory2=f"VTCurationServicesActions"     
#data_directory_path2=os.path.join(data_directory1,data_directory2,data_directory4)
payload_path=os.path.join(aptrustBagName,payload_directory2)
os.mkdir(payload_path)
print("Directory '% s' created" % payload_path) 

