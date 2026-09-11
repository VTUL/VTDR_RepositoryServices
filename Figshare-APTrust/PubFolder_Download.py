"""
Purpose: 
1. Downloads published article from figshare using article ID and token. This was built off of UAL-RE ldcoolp code to download article information which was built off of figshare Python code to retrieve article information 
2. Reads the published row for the corresponding article in the "Published" sheet from the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Creates publication folder following VTDR ingest folder naming and APTrust bag naming convention for preservation.
3. Get article details to create a json file for figshare metadata, creates ArchivalPackageREADME rtf file using create_archivalreadme.

"""

import os
from os.path import exists
import sys
sys.path.append('figshare')

#from figshare.figshare import Figshare
from figshare import Figshare
import requests
from requests import HTTPError
#from ldcoolp.curation import retrieve
from AutomatedArchivalPackageREADME import create_archivalreadme
from Read_VTDR_Spreadsheet import vtpubsheet
import shutil
import os
import figshareRetrieve
import figshareDownload
import json
from datetime import date
import filecmp
from datetime import datetime
import job
from job import Job
from redata.commons.logger import log_stdout
import hashlib
from logging import Logger
# ============= new import 8.14==========
from workflow_logging import start_logging
from download_validation import check_duplicate_md5

#Get the parameters from configurations.ini to retrieve information from an article on Figshare

import configparser
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

#Get the row information of the published article from the Published sheet using the corresponding ArticleID and Version Number:
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
DOIsuffix=vtsheet['gsdoisuffix']
#FigshareArticleID=vtsheet['psheet_articleid']


#get the row number of published article
PublishedAccessionNumber= vtsheet['gspubnum']
#get the ingest number corresponding to the published accession number
IngestAccessionNumber=vtsheet['gsingestno']
#Get LastnameFirstnameinitial of requestor and corresponding author:
RequestorLFI=vtsheet['gsreqlastfi']
CorrespondingAuthorLFI=vtsheet['gscorrlastfi']



#-----------------------------------------------------
#Create Publication folder and download the figshare published article

#Get current directory:
#directory_path=os.getcwd() 
PubFolderPath=config['PubFolder_PathSettings']['PubFolderPath'] 

aptrustBagName=f"VTDR_{PublishedAccessionNumber}_{IngestAccessionNumber}_DOI_{DOIsuffix}_{CorrespondingAuthorLFI}_v{Version}_{DatePublished}"
payload_directory1=f"DisseminatedContent"
PubFolderPayloadPath=os.path.join(PubFolderPath,aptrustBagName, payload_directory1)
metadata_directory_path=f"{PublishedAccessionNumber}_DownloadedFileMetadata_v{Version}"
PublishedVersionNumber = config['FigshareSettings']['PublishedVersionNumber']
#uncomment the following line and comment out None if recreating a bag for a specific published version and not the latest published version
#fversion=int(PublishedVersionNumber[1])
fversion=None
print(f"***************Figshare published version number (None gets the latest published version): {fversion}")

#==================LOGGING===============================
log_file, original_stdout, original_stderr = start_logging(
    log_base_name=aptrustBagName,
    workflow_name="VTDR PUB WORKFLOW",
    article_id=ArticleID
)

#quit()
fs=Figshare(token=token,private=False,version=fversion)
FileDownload=figshareDownload.download_files(article_id, fversion, fs, data_directory=PubFolderPayloadPath, metadata_directory=metadata_directory_path)

#============ file count check==============
#==========================================
expected_file_count = FileDownload["expected_file_count"]

local_files = []

for root, dirs, files in os.walk(PubFolderPayloadPath):
    for filename in files:
        local_files.append(
            os.path.join(root, filename)
        )

local_file_count = len(local_files)

print("\n")
print("=" * 80)
print("FIGSHARE FILE COUNT CHECK")
print("=" * 80)

print(f"Expected Figshare file count: {expected_file_count}")
print(f"Downloaded local file count:  {local_file_count}")

# # ============ MD5 CHECK ==============

# expected_files = FileDownload["file_list"]

# duplicate_md5_groups = check_duplicate_md5(
#     expected_files
# )



# # ============================================================
# # DUPLICATE FILE NAME VALIDATION
# # ============================================================

# duplicate_filename_groups = FileDownload["duplicate_filename_groups"]

# print("\n")
# print("=" * 80)
# print("DUPLICATE FILE NAME CHECK")
# print("=" * 80)

# if duplicate_filename_groups:

#     print(
#         "Files with duplicated file names were found.\n"
#         "Please review whether their contents are actually duplicated."
#     )

#     for group_number, (filename, files) in enumerate(
#         duplicate_filename_groups.items(),
#         start=1
#     ):

#         print(f"\nDuplicate Filename Group {group_number}")
#         print(f"Filename: {filename}")

#         for file_dict in files:
#             print(f"    Figshare file ID: {file_dict.get('id')}")
#             print(f"    Size: {file_dict.get('size')}")
#             print(f"    URL: {file_dict.get('download_url')}")

#     while True:

#         response = input(
#             "\nWould you like to proceed? (yes/no): "
#         ).strip().lower()

#         print(f"Curator response: {response}")

#         if response == "yes":
#             print("Proceeding with the workflow.")
#             break

#         elif response == "no":
#             print(
#                 "Workflow stopped so the curator can review or revise "
#                 "the possible duplicated files."
#             )
#             sys.exit(0)

#         else:
#             print("Please enter 'yes' or 'no'.")

# else:
#     print("No duplicated file names were detected.")


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

