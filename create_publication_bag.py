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
from spreadsheet import vtgsheet

#Enter published accession number 
PublishedAccessionNumber= "P00156"
#Enter your figshare token
token='1234'
#Enter curator name
curatorname="XYZ"

#Using published accession number to get the details from the spreadsheet:
vtsheet=vtgsheet(PublishedAccessionNumber)
#Get article id 
article_id=vtsheet['gsarticleid']
#create archival readme file using auto_fill_archive.py
reme=create_archivalreadme(pubaccno=PublishedAccessionNumber,cur_name=curatorname)
#get requestor name
Requestor=vtsheet['gsrequestr']
#get corresponding author name
CorrespondingAuthor=vtsheet['gscorsauth']
#get version
Version=vtsheet['gsversnum']
#get published date in YYYYMMDD format 
DatePublished= vtsheet['gsdatepub'] 

#Create Publication folder to store dataset
data_directory1=f"{PublishedAccessionNumber}_v{Version}"
data_directory2=f"{PublishedAccessionNumber}_{Requestor}_{CorrespondingAuthor}_v{Version}_{DatePublished}"
data_directory3=f"DisseminatedContent"
arch_readme_path=os.path.join(data_directory1,data_directory2,"ArchivalPackage.rtf")
data_directory_path=os.path.join(data_directory1, data_directory2, data_directory3)
metadata_directory_path=f"{PublishedAccessionNumber}_DownloadedFileMetadata_v{Version}"
#-----Download dataset for published article using LD-Cool-P and save it as publication meta data in json file format
publicfigshare_url='https://api.figshare.com/v2/articles/'+str(article_id)
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
    if overwrite:
        print("Overwriting!")
        with open(json_out_file1, 'w') as f:
            json.dump(json_response1,f,indent=4)
     
#----------------------create VTCurationServicesActions folder to save provenance log and email correspondence
                
data_directory4=f"VTCurationServicesActions"     
data_directory_path2=os.path.join(data_directory1,data_directory2,data_directory4)
os.mkdir(data_directory_path2)
print("Directory '% s' created" % data_directory4) 
