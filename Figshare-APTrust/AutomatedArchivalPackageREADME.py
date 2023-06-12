# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma carstens
"""
from Read_VTDR_Spreadsheet import vtpubsheet
from Read_VTDR_Spreadsheet import vtingsheet
from datetime import date
import re
import os
#import PyRTF
#from PyRTF import *
import configparser
config=configparser.ConfigParser()
config.read('configurations.ini')

def create_archivalreadme(ArticleID,PublishedVersionNumber,IngestVersionNumber,CuratorName, archival_directory: str = '',):
  """
Purpose: Create ArchivalPackageREADME file in rtf format. Read the row information from Ingest and Published sheet from the google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7.xls. Write to rtf using rtf coding syntax. This function is called in 
PubFolder_Download.py to create ArchivalPackageREADME.rtf in the Publication folder 

Parameters: 
Following parameters are provided as a string:
ArticleID: Figshare Article ID of the published article
PublishedVersionNumber: Version number of the published article on figshare
IngestVersionNumber: Version number of the ingested figshare article in review provided by the curator in the spreadsheet. 
CuratorName: Curator's FirstName LastName 
archival_directory: Directory where ArchivalPackageREADME.rtf is created

Example: create_archivalreadme("20161580","01","01","Padma Carstens",'C:/Users/padma/anaconda3/envs/curation/')
"""
#Get the current day
  today = date.today()
  currentday = today.strftime("%Y%m%d")
  curator=CuratorName
  out_file_prefix = f"ArchivalPackageREADME.rtf"
  #Get the archival package README parent folder from configurations.ini
  root_directory=config['ArchivalREADMEPathSettings']['ArchivalREADME_RootDir']
  archival_path=os.path.join(root_directory, archival_directory)
  out_file_prefix1 = f"{archival_path}/{out_file_prefix}"
  #Get row information from Published sheet:
  vtsheet=vtpubsheet(ArticleID,PublishedVersionNumber)
  PublishedAccessionNumber= vtsheet['gspubnum']
  IngestAccessionNumber= vtsheet['gsingestno']
   #Get row information from Ingest sheet:
  vtisheet=vtingsheet(ArticleID,IngestVersionNumber)
  DateIngested=vtisheet['ingestdate']
  Requestor=vtsheet['gsrequestr']
  CorrespondingAuthor=vtsheet['gscorsauth']
  RequestorLFI=vtisheet['ingreqlastfirsti']
  CorrespondingAuthorLFI=vtisheet['ingcorlastfirsti']
  DatePublished= vtsheet['gsdatepub']  
  DOI=vtsheet['gsdoi']
  Title=vtsheet['gstitle']
  authoremail=vtsheet['gscorauthemail']
  college=vtsheet['gscollg']
  dept=vtsheet['gsdept']
  comment=vtsheet['gscomnt']
  datecomment=vtsheet['gsdatecomnt']
  IngestVerNum=IngestVersionNumber
  #Open the rtf file and write to it using rtf coding syntax
  m = re.search(r'(?<=/)\w+', DOI)
  doilink= "https://doi.org/10.7294/"+m.group(0)
  f = open(out_file_prefix1,"w")
  f.write("{\\rtf1\\ansi This Archival Information Package created by "+curator+ " on "+currentday+"\\line"+
        " Virginia Tech Curation Services \\line"+"\n"+
        "***************************** \\line"+"\n"+
        "Accession# for Ingest: "+ IngestAccessionNumber+"\\line\n"+
        "Accession# for Publication: "+PublishedAccessionNumber+"\\line\n"+
        "Requestor: "+Requestor+"\\line\n"+
        "Corresponding Author: "+CorrespondingAuthor+"\\line\n"+
        "Version#: "+PublishedVersionNumber+"\\line\n"+
        "Date Published: "+DatePublished+"\\line\n"+
        "DOI: "+"{\\colortbl ;\\red0\\green0\\blue238;}{\\field{\\*\\fldinst HYPERLINK "+"\""+doilink+"\""+"}{\\fldrslt{\\ul\\cf1 "+doilink+"}}}"+"\\line\n"+
        "Dataset Title: "+Title+"\\line\n"+
        "Corresponding Author Email: "+authoremail+"\\line\n"+
        "College: "+college+"\\line\n"+
        "Department: "+dept+"\\line\n"+
        "Date of Most Recent Comment: "+datecomment+"\\line\n"+
        "Most Recent Comment: "+comment+"\\line\n"+
        "Bag Containing Original Content: "+"VTDR_"+IngestAccessionNumber+"_"+RequestorLFI+"_"+CorrespondingAuthorLFI+"_"+"v"+IngestVerNum+"_"+DateIngested+".tar"+"\\line\n"
        "*****************************"+"\\line\n"+
        "DisseminationContent (directory) contains"+"\\line\n"+
        "	-content and metadata made accessible through the Virginia Tech Data Repository; more information about this repository can be found at http://doi.org/10.17616/R3JF54 "+"\\line\n"+
        "VTCurationServicesActions (directory) contains"+"\\line\n"+
        "	-e-mail correspondence, provenance log(s), a form for capturing metadata from the Virginia Tech research, and any other files associated with actions conducted by Virginia Tech "+"\\line\n"+
        "Curation Services to augment the original files and metadata transferred to Virginia Tech Curation Services by a Virginia Tech researcher for their publication as a dataset}")
  f.close()

  return 

