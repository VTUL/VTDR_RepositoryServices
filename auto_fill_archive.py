# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 10:55:10 2021

@author: padma
"""
#Following code creates archival readme rtf file using information from the spreadsheet

#from create_publication_bag import PublicationDate
from spreadsheet import vtpubsheet
from spreadsheet import vtingsheet
from datetime import date
import re
import os
#def create_archivalreadme(pubaccno,cur_name,ver,pdate):
def create_archivalreadme(ArticleID,VersionNumber,CuratorName, archival_directory: str = '',):
  today = date.today()

# dd/mm/YY
  currentday = today.strftime("%Y%m%d")
  curator=CuratorName
  out_file_prefix = f"ArchivalPackage.rtf"
  #VersionNumber=ver
  root_directory=os.getcwd()
  archival_path=os.path.join(root_directory, archival_directory)
  out_file_prefix1 = f"{archival_path}/{out_file_prefix}"
  vtsheet=vtpubsheet(ArticleID,VersionNumber)
 # DatePublished=vtsheet['gspubdate']
  #vtisheet=vtingsheet(IngestAccessionNumber)
  PublishedAccessionNumber= vtsheet['gspubnum']
  IngestAccessionNumber= vtsheet['gsingestno']
  ingnum=IngestAccessionNumber
  vtisheet=vtingsheet(ArticleID,VersionNumber)
  DateIngested=vtisheet['ingestdate']
  Requestor=vtsheet['gsrequestr']
  CorrespondingAuthor=vtsheet['gscorsauth']
  #Version=vtsheet['gsversnum']
  DatePublished= vtsheet['gsdatepub']  
  DOI=vtsheet['gsdoi']
  Title=vtsheet['gstitle']
  authoremail=vtsheet['gscorauthemail']
  college=vtsheet['gscollg']
  dept=vtsheet['gsdept']
  comment=vtsheet['gscomnt']
  datecomment=vtsheet['gsdatecomnt']
  IngestVerNum="01"#Ingest records are always version 01
  m = re.search(r'(?<=/)\w+', DOI)
  #f = open('ArchivalPackage.rtf',"w")
  f = open(out_file_prefix1,"w")
  f.write(" "+"\n"+
        "This Archival Information Package created by "+curator+" on "+currentday+"\n"+
        "Virginia Tech Curation Services\n"+
        "*****************************\n"+
        "Accession# for Ingest: "+ IngestAccessionNumber+"\n"+
        "Accession# for Publication: "+PublishedAccessionNumber+"\n"+
        "Requestor: "+Requestor+"\n"+
        "Corresponding Author: "+CorrespondingAuthor+"\n"+
        "Version#: "+VersionNumber+"\n"+
        "Date Published: "+DatePublished+"\n"+
        "DOI: 10.7294/"+m.group(0)+"\n"+
        "Dataset Title: "+Title+"\n"+
        "Corresponding Author Email: "+authoremail+"\n"+
        "College: "+college+"\n"+
        "Department: "+dept+"\n"+
        "Date of Most Recent Comment: "+datecomment+"\n"+
        "Most Recent Comment: "+comment+"\n"+
        "Bag Containing Original Content: "+IngestAccessionNumber+"_"+Requestor+"_"+CorrespondingAuthor+"_"+"v"+IngestVerNum+"_"+DateIngested+".tar"+"\n"
        "*****************************"+"\n"+
        "DisseminationContent (directory) contains"+"\n"+
        "	-content and metadata made accessible through the Virginia Tech Data Repository; more information about this repository can be found at http://doi.org/10.17616/R3JF54 "+"\n"+
        "VTCurationServicesActions (directory) contains"+"\n"+
        "	-e-mail correspondence, provenance log(s), a form for capturing metadata from the Virginia Tech research, and any other files associated with actions conducted by Virginia Tech "+"\n"+
        "Curation Services to augment the original files and metadata transferred to Virginia Tech Curation Services by a Virginia Tech researcher for their publication as a dataset")
  f.close()

  return 
