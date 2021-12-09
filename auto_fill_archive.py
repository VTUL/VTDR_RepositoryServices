# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma carstens
"""
#Following code creates archival readme rtf file using information from the spreadsheet

#from create_publication_bag import PublicationDate
from spreadsheet import vtpubsheet
from spreadsheet import vtingsheet
from datetime import date
import re
import os
from PyRTF import *
def create_archivalreadme(ArticleID,PublishedVersionNumber,IngestVersionNumber,CuratorName, archival_directory: str = '',):
  today = date.today()

# dd/mm/YY
  currentday = today.strftime("%Y%m%d")
  curator=CuratorName
  out_file_prefix = f"ArchivalPackageREADME.rtf"
  root_directory=os.getcwd()
  archival_path=os.path.join(root_directory, archival_directory)
  out_file_prefix1 = f"{archival_path}/{out_file_prefix}"
  vtsheet=vtpubsheet(ArticleID,PublishedVersionNumber)
  PublishedAccessionNumber= vtsheet['gspubnum']
  IngestAccessionNumber= vtsheet['gsingestno']
  vtisheet=vtingsheet(ArticleID,IngestVersionNumber)
  DateIngested=vtisheet['ingestdate']
  Requestor=vtsheet['gsrequestr']
  CorrespondingAuthor=vtsheet['gscorsauth']
  DatePublished= vtsheet['gsdatepub']  
  DOI=vtsheet['gsdoi']
  Title=vtsheet['gstitle']
  authoremail=vtsheet['gscorauthemail']
  college=vtsheet['gscollg']
  dept=vtsheet['gsdept']
  comment=vtsheet['gscomnt']
  datecomment=vtsheet['gsdatecomnt']
  IngestVerNum=IngestVersionNumber
  m = re.search(r'(?<=/)\w+', DOI)
  doilink= "https://doi.org/10.7294/"+m.group(0)
  f = open(out_file_prefix1,"w")
  f.write("{\\rtf1\\ansi This Archival Information Package created by "+curator+ "on "+currentday+"\\line"+
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
        "Bag Containing Original Content: "+IngestAccessionNumber+"_"+Requestor+"_"+CorrespondingAuthor+"_"+"v"+IngestVerNum+"_"+DateIngested+".tar"+"\\line\n"
        "*****************************"+"\\line\n"+
        "DisseminationContent (directory) contains"+"\\line\n"+
        "	-content and metadata made accessible through the Virginia Tech Data Repository; more information about this repository can be found at http://doi.org/10.17616/R3JF54 "+"\\line\n"+
        "VTCurationServicesActions (directory) contains"+"\\line\n"+
        "	-e-mail correspondence, provenance log(s), a form for capturing metadata from the Virginia Tech research, and any other files associated with actions conducted by Virginia Tech "+"\\line\n"+
        "Curation Services to augment the original files and metadata transferred to Virginia Tech Curation Services by a Virginia Tech researcher for their publication as a dataset}")
  f.close()

  return 
