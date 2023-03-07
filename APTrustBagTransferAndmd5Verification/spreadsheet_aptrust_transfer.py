# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:05:20 2021

@author: padma carstens

Purpose:
-Reads the 2021 version 7 VTDR spreadsheet using google cloud API
"""
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

#Following gets data from the spreadsheet version 7 "Ingest" using the ingest number
def aptrust_vtingsheet():
 scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
 creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
 client = gspread.authorize(creds)
 #Open the spreadsheet sheet1: "Ingested"
 ingsheet = client.open("20211214_VTDR_PublishedDatasets_Log_V7").sheet1
 #Get the column values for Ingest Numbers:
 ingestnums=ingsheet.col_values(1)
 #Get the column values for Requestor:
 ingsheet_requestor=ingsheet.col_values(2)
 #Get the column values for Corresponding Author:
 icorres_author=ingsheet.col_values(3)
#Use string split to get lastnamefirstnameinitial for folder creation for requestor and corresponding author:
 ireq_lastfirstini=['Requestor_lastname_firstnameinitial']
 icorr_lastfirstini=['CorrespondingAuthor_lastname_firstnameinitial']
 for x in range(1,len(ingsheet_requestor)):
   requestor1=ingsheet_requestor[x]
   rnamesplit=requestor1.split(" ")
   firstname=rnamesplit[0]
   lastname=rnamesplit[1]
   firstnameinitial=firstname[0].upper()
   req_lastfirstini1=lastname+firstnameinitial
   ireq_lastfirstini.append(req_lastfirstini1)
   corres_author1=icorres_author[x]
   cnamesplit=corres_author1.split(" ")
   corr_firstname=cnamesplit[0]  
   corr_lastname=cnamesplit[1]
   corr_firstnameini=corr_firstname[0].upper()
   corr_lastfirstini1=corr_lastname+corr_firstnameini
   icorr_lastfirstini.append(corr_lastfirstini1)
 #Get the column values for Version:
 ingsheet_version=ingsheet.col_values(4)
#Get the column values for Ingest Date:
 ingsheet_date=ingsheet.col_values(5)
 # Get the column values for Title:
 ingsheet_title=ingsheet.col_values(6)
 #Get the corresponding author email address:
 ingsheet_cemail=ingsheet.col_values(7)
 #Get the column values for comment:
 ingsheet_comment=ingsheet.col_values(8)
 #Get the column values for article ID
 ingsheet_article=ingsheet.col_values(9)
#Get the doi suffixes if article is published
 ingsheet_doi=ingsheet.col_values(10)
 dictingsheet=dict({'iRequestor': ingsheet_requestor,'iCorAuth':icorres_author,'iVersion':ingsheet_version,'iDate':ingsheet_date,'iTitle':ingsheet_title,'iCAemail':ingsheet_cemail,'iComment':ingsheet_comment,'iArticleid': ingsheet_article,'iIngestnum':ingestnums,'iReqLnameFini':ireq_lastfirstini,'iCorLnameFini': icorr_lastfirstini,'iDOIsuffix' : ingsheet_doi})

 
 return dictingsheet


#Following gets information from the spreadsheet version 7 "Published" sheet using the article id and version
def aptrust_vtpubsheet():
# use creds to create a client to interact with the Google Drive API
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  client = gspread.authorize(creds)
  #Open the spreadsheet sheet1: "Published"
  pubsheet = client.open("20211214_VTDR_PublishedDatasets_Log_V7").worksheet('Published')
  #Get the column values for Ingest Number:
  ingest_num=pubsheet.col_values(1)
  #Get the column values for Published Accession number:
  pubacc_num=pubsheet.col_values(2)
  #Get the column values for Requestor:
  requestor=pubsheet.col_values(3)
  #Get the column values for Corresponding Author:
  corres_author=pubsheet.col_values(4)
  #Use string split to get lastnamefirstnameinitial for folder creation for requestor and corresponding author:
  req_lastfirstini=['Requestor_lastname_firstnameinitial']
  corr_lastfirstini=['CorrespondingAuthor_lastname_firstnameinitial']
  for x in range(1,len(requestor)):
    requestor1=requestor[x]
    rnamesplit=requestor1.split(" ")
    firstname=rnamesplit[0]
    lastname=rnamesplit[1]
    firstnameinitial=firstname[0].upper()
    req_lastfirstini1=lastname+firstnameinitial
    req_lastfirstini.append(req_lastfirstini1)
    corres_author1=corres_author[x]
    cnamesplit=corres_author1.split(" ")
    corr_firstname=cnamesplit[0]  
    corr_lastname=cnamesplit[1]
    corr_firstnameini=corr_firstname[0].upper()
    corr_lastfirstini1=corr_lastname+corr_firstnameini
    corr_lastfirstini.append(corr_lastfirstini1)
    
  #Get the column values for Version number:
  version=pubsheet.col_values(5)
  #Get the column values for published date:
  date_pub=pubsheet.col_values(6)
  #Get the column values for DOI:
  doi=pubsheet.col_values(7)
  #split article id from doi:
  doisuffix=['DOI']
  for l in range(1,len(doi)):
    d=doi[l]
    v= d.split('/')[1]
    doisuffix.append(v)
  #Get the column values for title:
  title=pubsheet.col_values(8)
  #Get the column values for corresponding author email id:
  corres_authemail=pubsheet.col_values(9)
  #Get the column values for College:
  college=pubsheet.col_values(10)
  #Get the column values for department:
  dept=pubsheet.col_values(11)
  #Get the column values for date of most recent comment:
  date_most_recent_comment=pubsheet.col_values(12)
  #Get the column values for most recent commen
  most_recent_comment=pubsheet.col_values(13)


  dictpubsheet=dict({'pDOIsuffix':doisuffix,'pIngestnum':ingest_num,'pPubnum':pubacc_num,'pRequestor':requestor,'pCorAuth':corres_author,'pVersion':version,'pDate':date_pub,'pDoi':doi,'pTitle':title,'pCAemail':corres_authemail,'pCollege':college,'pDept':dept,'pDateComnt':date_most_recent_comment,'pComment':most_recent_comment,'pReqLnameFini': req_lastfirstini,'pCorLnameFini':corr_lastfirstini})
  return dictpubsheet


#Fill article id information from figshare batch download for articles published before migration to figshare 
def aptrust_vtFigDownld():
# use creds to create a client to interact with the Google Drive API
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  client = gspread.authorize(creds)
  #Open the spreadsheet sheet1: "Published"
  Figsheet = client.open("20211214_VTDR_PublishedDatasets_Log_V7").worksheet('FigshareBatchDownload')
  #Get the column values for Ingest Number:
  fArticleID=Figsheet.col_values(1)
  
  #Get the column values for DOI:
  fdoi=Figsheet.col_values(14)
  #split article id from doi:
  fdoisuffix=['DOI']
  for l in range(1,len(fdoi)):
    d=fdoi[l]
    v= d.split('/')[1]
    fdoisuffix.append(v)
  #Get the column values for title:
  ftitle=Figsheet.col_values(5)
  #Get the column values for corresponding author email id:
  fpubdate=Figsheet.col_values(29)

#aptrust_vtFigDownld():
  dictfigsheet=dict({'fArticleID': fArticleID,'fDOIsuffix':fdoisuffix,'fPubDate':fpubdate,'fDoisuffix':fdoisuffix,'ftitle':ftitle})
  return dictfigsheet

