# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""

import os
from os.path import exists
import json
from ldcoolp.curation import retrieve

#Enter article id for published articles:this is the also last number in the "cite" on data.lib.vt.edu 
article_id=1234
#Enter your token below
token='1234'
#Enter published accession number from the spreadsheet
PublishedAccessionNumber= "P123"
#Enter requestor name
Requestor="XYZ"
#Enter corresponding author name
CorrespondingAuthor="XYZ"
#Enter version
Version="01"
#Enter published date in YYYYMMDD format 
DatePublished= "20211025"  

#Create Publication folder to store dataset
data_directory1=f"{PublishedAccessionNumber}_v{Version}"
data_directory2=f"{PublishedAccessionNumber}_{Requestor}_{CorrespondingAuthor}_v{Version}_{DatePublished}"
data_directory3=f"DisseminatedContent"
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
