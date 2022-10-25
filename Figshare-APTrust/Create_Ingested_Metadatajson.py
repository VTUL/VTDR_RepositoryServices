
import os
from os.path import exists
import sys

from figshare.figshare import Figshare
from ldcoolp.curation import retrieve
import json
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import filecmp
from datetime import datetime
import job
from job import Job
import configparser
from Read_VTDR_Spreadsheet import vtpubsheet
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



#Get the row information of the article in review/ingested article from the Ingest sheet using the corresponding ArticleID and Version Number:
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
#get version number
pVersion=Pvtsheet['gsversnum']
#get date published
pDate=Pvtsheet['gsdatepub']
#Create Ingest folder using VTDR folder convention for ingest preservation
IngFolderPath=config["IngestBag_PathSettings"]['IngFolderPath']
IngFolderName=f"VTDR_{IngestAccessionNumber}_{Requestorlfi}_{CorrespondingAuthorlfi}_v{PublishedVersionNumber}_{pDate}_IngestedMetadata"
data_directory_path=os.path.join(IngFolderPath,IngFolderName)
metadata_jsonpath=config["IngestBag_PathSettings"]['metadatajsonpath']
metadata_filename=f"{IngestAccessionNumber}_DownloadedFileMetadata"
metadata_directory_path=os.path.join(metadata_jsonpath,metadata_filename)

fversion=2

fs=Figshare(token=token,private=False,version=fversion)
#fversion=None#no version for ingest
privatefigshare_url='https://api.figshare.com/v'+str(PublishedVersionNumber[1])+'/account/articles/'+str(article_id)
json_out_file=f"{data_directory_path}/{IngestAccessionNumber}_IngestedMetadata.json"
json_response=fs.get_article_details(ArticleID,version=None)

if not os.path.exists(json_out_file):
    with open(json_out_file, 'w') as f:
        json.dump(json_response,f,indent=4)
else:
    print(f"File exists: {json_out_file}")