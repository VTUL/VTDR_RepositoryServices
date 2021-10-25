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


#Enter article id: this is the last number in the "cite" on data.lib.vt.edu
article_id="XYZ"
# Enter Ingest Accession Number from the spreadsheet:
IngestAccessionNumber= "1234" 
#Enter Requestor name
Requestor="XYZ"
#Enter corresponding author name
CorrespondingAuthor="XYZ"
#Enter version number
Version="01"
#Enter date ingested in YYYYMMDD format
DateIngested= "20211018"   #in YYYYMMDD format
#Enter your token
token='1234'

#Create Ingest folder to store dataset
data_directory1=f"{IngestAccessionNumber}"
data_directory2=f"{IngestAccessionNumber}_{Requestor}_{CorrespondingAuthor}_v{Version}_{DateIngested}"
data_directory_path=os.path.join(data_directory1, data_directory2)
metadata_directory_path=f"{IngestAccessionNumber}_DownloadedFileMetadata"
#-----Download dataset for private files using LD-Cool-P and save it as Ingest data json file
fs=Figshare(token=token,private=True)
FileDownload=retrieve.download_files(article_id, fs, data_directory=data_directory_path, metadata_directory=metadata_directory_path)
 
privatefigshare_url='https://api.figshare.com/v2/account/articles/'+str(article_id)

#-----get article details for private files using LD-Cool-P and save it as Ingest data json file

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

#Call parts of modified UPACK_v2 code written by Luke. I. Menzies(lmenzies@uab.edu) to bag and tar files

myobj=ObjFormatter#()
tarfiledir=data_directory1
ingest_bag=myobj.run_bagit(bagsdir=tarfiledir)
ingest_bag_tar=myobj.run_tar(tarfolder=tarfiledir)

