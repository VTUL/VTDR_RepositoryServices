#!/usr/bin/env python
'''
PubFolder_Download_batch.py
Created on   2024/9/25 14:13:23
@author  :   padma carstens 
'''
"""
Purpose: 
Batch downloads for each article :
  1. Downloads published article from figshare using article ID and token. This was built off of UAL-RE ldcoolp code to download article information which was built off of figshare Python code to retrieve article information 
  2. Reads the published row for the corresponding article in the "Published" sheet from the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Creates publication folder following VTDR ingest folder naming and APTrust bag naming convention for preservation.
  3. Get article details to create a json file for figshare metadata, creates ArchivalPackageREADME rtf file using create_archivalreadme.

"""

import os
from os.path import exists
import sys
#from figshare.figshare import Figshare
import bs4
from bs4 import BeautifulSoup
from figshare import Figshare
import requests
from requests import HTTPError
#from ldcoolp.curation import retrieve
import configparser
sys.path.append("curation")
import AutomatedArchivalPackageREADME
import Read_VTDR_Spreadsheet
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
import bs4
from bs4 import BeautifulSoup
#import BeautifulSoup
from logging import Logger


#Get the parameters from configurations.ini to retrieve information from an article on Figshare

import configparser

def DownloadPub():
  #print('figshare article id is ', ArticleID)
  config=configparser.ConfigParser()
  config.read('configurations-batch.ini')

#Get the ArticleID
  ArticleID=config['FigshareSettings']['FigshareArticleID']
  print('figshare article id is ', ArticleID)
  #quit()
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
  DOIsuffix=vtsheet['DOIsuffix']
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
  fversion=int(PublishedVersionNumber[1])

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

#-------------------------------------------------
  #from AutomatedREADMErtf import create_readme
  readmefile=create_readme(ArticleID,token,PubFolderPayloadPath)
#-----------------------------------------------------------------------------
#Create VTCurationServicesActions folder in order to save provenance log and email correspondence. Provenance log and Email correspondence are created manually and stroed in this folder
                
  VTCurServicesPath=f"VTCurationServicesActions"     
#data_directory_path2=os.path.join(data_directory1,data_directory2,data_directory4)
  payload_path=os.path.join(PubFolderPath,aptrustBagName,VTCurServicesPath)
  if not os.path.exists(payload_path): 
     os.mkdir(payload_path)
     print("Directory '% s' created" % payload_path) 
  else:
     print("Directory ",payload_path," already exists")

#-----------------------------------------------------------------------------

def create_readme(ArticleID,token,PubFolderPayloadPath):
  """
  Purpose:
    Retrieve figshare metadata with token and article id.  Create README.rtf and write the fields retrieved from figshare metadata and Ingest sheet into this file. Create a new README directory to save the README file

  :param Article ID: Figshare article id under "Cite" button for an article in review
  :param token: Figshare token: click circle on data.lib.vt.edu, then click "Applications" then click "Create Personal Token"
  """
  #If creating this AFTER the article is published then change "private" to "False" below, this will create README file using the published metadata
  fs=Figshare(token=token,private=True)
  #There is no versioning for article under review in figshare
  #Retrieve article information from Figshare
  details=fs.get_article_details(ArticleID,version=None)
  #print(details)
  #Get the title of the article
  title=details["title"]
  #Get the author list
  authr=[]
  for i in range(len(details["authors"])):
   authrs=details["authors"][i]['full_name']
   authr.append(authrs)
  s=", "
  author=s.join(authr)

  #Get the categories list
  cat=[]
  for i in range(len(details["categories"])):
   cats=details["categories"][i]['title']
   cat.append(cats)
  Categoriesinfo=s.join(cat)
  
  #Get the list of group ids
  groupidnames=fs.get_groupid_names(version=None)
  groupids=[]
  groupname=[]  
  for i in range(len(groupidnames)):
    groupid=groupidnames[i]['id']
    groupid_name=groupidnames[i]['name']
    groupids.append(groupid)
    groupname.append(groupid_name)
  #Get the funding list
  fundinglist=[]
  for m in range(len(details['funding_list'])):
    fund=details['funding_list'][m]['title']
    fundinglist.append(fund)
  Funding=s.join(fundinglist)
  #Get the group names from group ids
  index=groupids.index(details['group_id'])# this gives the index of the group id displayed on figshare
  Group=groupname[index]#this gives the group name that the displayed group id on figshare corresponds to from the group id list 
  #Get the item type 'dataset' or 'code' etc.
  ItemType=details['defined_type_name']#"Dataset"#change
  #Get the list of keywords
  keywords=s.join(details['tags'])
  #Strip html tags in description
  #In this code we are using BeautifulSoup
  Description=details['description']
  soup=BeautifulSoup(Description,features="html.parser")#,newline='')
  parsedDescription=soup.text
  parsedDescription=parsedDescription.replace("\n","\\line\n")
  
  #Get all the remaining fields 
  License=details["license"]['name']
  Publisher=details['custom_fields'][0]['value']
  Location= details['custom_fields'][1]['value']
  CorresAuthName=details['custom_fields'][2]['value']
  CorresAuthEmail=details['custom_fields'][3]['value']
  FilesFolders=details['custom_fields'][4]['value']
  #Remove html tags in files/folders
  soup1=BeautifulSoup(FilesFolders,features="html.parser")
  parsedFilesFolders=soup1.text
  parsedFilesFolders=parsedFilesFolders.replace("\n","\\line\n")

  #Leave the metadata field empty/default value if the metadata fields are not filled in by the author
  if title is None or title=="":
    title=""
  if author is None or author=="":
    author=""
  if CorresAuthEmail is None or CorresAuthEmail=="":
    CorresAuthEmail=""
  if Categoriesinfo is None or Categoriesinfo=='':
    Categoriesinfo=""
  if Group is None or Group=='':
    Group=""
  if ItemType is None or ItemType=='':
    ItemType=""
  if keywords is None or keywords=='':
    keywords=""
  if Description is None or Description=='':
    Description=""
  if Funding is None or Funding=='':
    Funding=""
  #special character encoding conversion to rtf -------------
  def rtf_encode_char(unichar):
    code = ord(unichar)
    if code < 128:
        return str(unichar)
    return '\\u' + str(code if code <= 32767 else code-65536) + '?'

  def rtf_encode(unistr):
    return ''.join(rtf_encode_char(c) for c in unistr)
  #---------------------------------------------------
  #Get License and related materials:
  if License is None or License=='':
    License="CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
  OtherRef=[]  

  #Get related materials and types idtype: identifiertype, idrelation: identifier relation, idtitle: identifier title, related materials encoded as a hyperlink as orefs to output to readme:
  relatedMaterials=[]
  s1='\n'
  for i in range(len(details["related_materials"])):
     idtype=details['related_materials'][i]['identifier_type']
     idrelation=details['related_materials'][i]['relation']
     idtitle=details['related_materials'][i]['title']
     cleantitle=rtf_encode(idtitle) #rtf encoding for special chars
     orefs=details["references"][i]
     OtherRefs="{\\colortbl ;\\red0\\green0\\blue238;}{\\field{\\*\\fldinst HYPERLINK "+"\""+orefs+"\""+"}{\\fldrslt{\\ul\\cf1 "+str(orefs)+" }}}" #hyperlink in rtf
     if idtitle=='': 
       relatedMaterialStr=idtype+', '+idrelation+', '+OtherRefs
     else:
       relatedMaterialStr=idtype+', '+idrelation+', '+cleantitle+', '+OtherRefs
     relatedMaterials.append(relatedMaterialStr)
  #print(type(relatedMaterials))
  allRelMaterials='\\line\n'.join(relatedMaterials)

  #Get publisher, location, files/folders fill in values    
  if Publisher is None or Publisher=='':
    Publisher="University Libraries, Virginia Tech"
  if Location is None or Location=='':
    Location=""
  if FilesFolders is None or FilesFolders=='':
    FilesFolders=""
  #special character encoding in title funding for outputting to rtf 
  title=rtf_encode(title)
  Funding=rtf_encode(Funding)
  descriptionRtfEncode=rtf_encode(parsedDescription)
  filesFoldersRtfEncode=rtf_encode(parsedFilesFolders)
  #Create README.rtf and write the figshare fields to the file using rtf coding syntax     
  out_file_prefix = f"README.rtf"
  root_directory=os.getcwd()
  readme_path=PubFolderPayloadPath
#  print("The new directory "+readmefolder+" is created")
  out_file_prefix1 = f"{readme_path}/{out_file_prefix}"
  f = open(out_file_prefix1,'w',encoding="utf-8")
  f.write("{\\rtf1\\ansi {\\b Title of Dataset:} "+str(title)+"\\line\n"+
        "{\\b Author(s):} "+str(author)+"\\line\n"+
        "{\\b Categories:} "+Categoriesinfo+"\\line\n"+        
        "{\\b Group:} "+str(Group)+"\\line\n"+
        "{\\b Item Type:} "+str(ItemType)+"\\line\n"+
        "{\\b Keywords:} "+str(keywords)+"\\line\n"+
        "{\\b Description:} "+descriptionRtfEncode+"\\line\n"
        "{\\b Funding:} "+str(Funding)+"\\line\n"+
        "{\\b Related Materials: [Identifier Type, Relationship, Identifier, see DataCite relation types for more information]} \\line\n"+str(allRelMaterials)+"\\line\n"+
        "{\\b License:} "+str(License)+"\\line\n"+
        "{\\b Publisher:} "+str(Publisher)+"\\line\n"+
        "{\\b Location:} "+str(Location)+"\\line\n"+
        "{\\b Corresponding Author Name:} "+str(CorresAuthName)+"\\line\n"+
        "{\\b Corresponding Author E-mail Address:} "+str(CorresAuthEmail)+"\\line\n"+
        "{\\b Files/Folders in Dataset and Description of Files}"+"\\line\n"+
        str(filesFoldersRtfEncode)+ "\\line\n"+
        
        "}")
  f.close()

  return 
