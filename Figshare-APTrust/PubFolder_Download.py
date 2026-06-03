"""
Purpose: 
1. Downloads published article from figshare using article ID and token. This was built off of UAL-RE ldcoolp code to download article information which was built off of figshare Python code to retrieve article information 
2. Reads the published row for the corresponding article in the "Published" sheet from the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Creates publication folder following VTDR ingest folder naming and APTrust bag naming convention for preservation.
3. Get article details to create a json file for figshare metadata, creates ArchivalPackageREADME rtf file using create_archivalreadme.

"""

import os
from os.path import exists
import sys
from pathlib import Path
sys.path.append('figshare')

#from figshare.figshare import Figshare
from figshare import Figshare
import requests
from requests import HTTPError
#from ldcoolp.curation import retrieve
from AutomatedArchivalPackageREADME import create_archivalreadme
from Read_VTDR_Spreadsheet import vtpubsheet
from Read_VTDR_Spreadsheet import vtingsheet
import shutil
import os
import figshareRetrieve
import figshareDownload
import json
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime
import job
from job import Job
from redata.commons.logger import log_stdout
import hashlib
from logging import Logger

import configparser
config=configparser.ConfigParser()
config.read('configurations.ini')

ArticleID=config['FigshareSettings']['FigshareArticleID'] 
PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
IngestVersionNumber=config['FigshareSettings']['IngestVersionNumber']
token=config['FigshareSettings']['token']
CuratorName=config['FigshareSettings']['CuratorName']

print("Figshare Article ID:", ArticleID, "Version number: ", PublishedVersionNumber)
vtsheet=vtpubsheet(ArticleID,PublishedVersionNumber)

article_id=vtsheet['gsarticleid']
Requestor=vtsheet['gsrequestr']
CorrespondingAuthor=vtsheet['gscorsauth']
Version=vtsheet['gsversnum']
DatePublished= vtsheet['gsdatepub'] 
DOIsuffix=vtsheet['gsdoisuffix']



PublishedAccessionNumber= vtsheet['gspubnum']
IngestAccessionNumber=vtsheet['gsingestno']
RequestorLFI=vtsheet['gsreqlastfi']
CorrespondingAuthorLFI=vtsheet['gscorrlastfi']

#=============copy function===================
def copy_arc_folder_as_payload(source_dir, destination_dir, overwrite=True):
    source_path = Path(source_dir)
    # destination_path = Path(destination_dir)
    destination_path = os.path.join(
        PubFolderPayloadPath,
        os.path.basename(ARCSourcePath)
    )

    if not source_path.exists():
        raise FileNotFoundError(f"ARC source directory does not exist: {source_path}")

    if not source_path.is_dir():
        raise NotADirectoryError(f"ARC source path is not a directory: {source_path}")

    # if destination_path.exists():
    #     if overwrite:
    #         shutil.rmtree(destination_path)
    #         print(f"Removed existing DisseminatedContent: {destination_path}")
    #     else:
    #         raise FileExistsError(f"{destination_path} already exists and overwrite=False")

    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

    print(f"Copied ARC folder as full payload:")
    print(f"  FROM: {source_path}")
    print(f"  TO:   {destination_path}")
    
#-----------------------------------------------------
#Create Publication folder and download the figshare published article

#Get current directory:
#directory_path=os.getcwd() 
PubFolderPath=config['PubFolder_PathSettings']['PubFolderPath'] 

# article_id = ArticleID
# PublishedAccessionNumber = "TESTPUB"
# IngestAccessionNumber = "TESTINGEST"
# DOIsuffix = "TESTDOI"
# CorrespondingAuthorLFI = "TESTAUTHOR"
# Version = "1"
# DatePublished = "20260312"


aptrustBagName=f"VTDR_{PublishedAccessionNumber}_{IngestAccessionNumber}_DOI_{DOIsuffix}_{CorrespondingAuthorLFI}_v{Version}_{DatePublished}"
payload_directory1=f"DisseminatedContent"
PubFolderPayloadPath=os.path.join(PubFolderPath,aptrustBagName, payload_directory1)
metadata_directory_path=f"{PublishedAccessionNumber}_DownloadedFileMetadata_v{Version}"
PublishedVersionNumber = config['FigshareSettings']['PublishedVersionNumber']
fversion=None
print(f"***************Figshare published version number (None gets the latest published version): {fversion}")
#quit()
fs=Figshare(token=token,private=False,version=fversion)
FileDownload=figshareDownload.download_files(article_id, fversion, fs, data_directory=PubFolderPayloadPath, metadata_directory=metadata_directory_path)

#----------------Download figshare metadata for the published article and write it into a json file

json_out_file1=f"{PubFolderPayloadPath}/{PublishedAccessionNumber}_DisseminatedMetadata.json"

json_response1=fs.get_article_details(article_id,version=fversion)


if not os.path.exists(json_out_file1):
    with open(json_out_file1, 'w') as f:
        json.dump(json_response1,f,indent=4)
else:
    print(f"File exists: {json_out_file1}")

#-----------------------------------------------------------------------------

#Create ArchivalPackageREADME rtf file
archival_directory=os.path.join(PubFolderPath,aptrustBagName)
#create archival readme file using auto_fill_archive.py

reme=create_archivalreadme(ArticleID,PublishedVersionNumber,IngestVersionNumber,CuratorName,archival_directory) 

#-----------------------------------------------------------------------------
#Create VTCurationServicesActions folder in order to save provenance log and email correspondence. Provenance log and Email correspondence are created manually and stroed in this folder
                
VTCurServicesPath=f"VTCurationServicesActions"     
#data_directory_path2=os.path.join(data_directory1,data_directory2,data_directory4)
payload_path=os.path.join(PubFolderPath,aptrustBagName,VTCurServicesPath)
if not os.path.exists(payload_path):
    os.mkdir(payload_path)
    print("Directory '%s' created" % payload_path)
else:
    print("Directory '%s' already exists, skipping creation." % payload_path)




arc_template = config['ARC_PathSettings'].get('ARCResourceTemplate', '').strip()
arc_resource_path = config['ARC_PathSettings'].get('ARCResourcePath', '').strip()

if arc_template:
    ARCSourcePath = arc_template.format(
        ArticleID=ArticleID,
        PublishedAccessionNumber=PublishedAccessionNumber,
        IngestAccessionNumber=IngestAccessionNumber,
        Version=Version
    )
elif arc_resource_path:
    ARCSourcePath = arc_resource_path
else:
    raise ValueError(
        "No ARC source path configured. Please set ARCResourcePath or ARCResourceTemplate "
        "under [ARC_PathSettings] in configurations.ini"
    )

print(f"ARC source directory: {ARCSourcePath}")
print(f"Copying ARC content into DisseminatedContent: {PubFolderPayloadPath}")

copy_arc_folder_as_payload(
    ARCSourcePath,
    PubFolderPayloadPath,
    overwrite=False
)