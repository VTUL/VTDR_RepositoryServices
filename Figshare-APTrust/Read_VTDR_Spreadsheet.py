# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:05:20 2021

@author: padma carstens
@co-author: jonathan petters 
Purpose:

Read VTDR 2022 spreadsheet

"""
#from boto import Version
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import sys
from sys import exit

#Following gets data from the spreadsheet version 7 "Ingest" using the ingest number
def vtingsheet(ArticleID,IngestVersionNumber):

 """
Purpose: 
Access Ingest sheet from VTDR spreadsheet using VTDR curation services account and OAuth2 credentials from the Google API Console using credentails from the JSON file

Parameters: 
ArticleID: Figshare article ID of the article that needs to be read from the spreadsheet
IngestVersionNumber: Ingest number of the article in review whose row information needs to be read
 """
 #Get the parameters from configurations.ini to retrieve information on spreadsheet

 import configparser
 config=configparser.ConfigParser()
 config.read('configurations.ini')
 spreadSheet=config['SpreadsheetSettings']['SpreadsheetName']

 scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
 creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
 client = gspread.authorize(creds)
 #Open the spreadsheet sheet1: "Ingested"
 #ingsheet = client.open("20211214_VTDR_PublishedDatasets_Log_V7").sheet1
 print(spreadSheet)
 ingsheet = client.open(spreadSheet).sheet1
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
 #IF article ID is provided, do following
 if ArticleID is not None:
#Find the row/rows in the spreadsheet that correspond to the given articleid 
   row_aidmatch=[i for i, e in enumerate(ingsheet_article) if e == ArticleID]
 #Find the row/rows in the spreadsheet that correspond to the given version
   row_vermatch=[i for i, e in enumerate(ingsheet_version) if e == IngestVersionNumber]
 #Find the row in the spreadsheet that corresponds to the given article ID and version number
   rownum=np.intersect1d(row_aidmatch,row_vermatch)
 #the row number on the spreadsheet is rownum+1 due to array indexing from 0
 #convert numpy array to integer
   print("Ingest sheet rownumber: ",rownum+1)
   try:
     rownum=int(rownum)
   except TypeError:
    print("ROW INFORMATION FOR THE PROVIDED ARTICLE ID AND VERSION NUMBER WAS NOT FOUND IN THE INGEST SHEET")
    print("Please enter the ingest record information in the ingest sheet and try running again")
    sys.exit()
   
   #print("GOODBYE")
   #print("Ingest sheet rownumber: ",rownum+1)
   

#Get the Requestor namen, Version, IngestDate, Title, Comment, ArticleID, IngestNumber that correspond the rownumber found above   
   #try:
   ing_requestor=ingsheet_requestor[rownum]
   #except TypeError:
   # print("Cannot find this row number")
   ing_version=ingsheet_version[rownum]
   ing_date=ingsheet_date[rownum]
   ing_title=ingsheet_title[rownum]
   ing_cemail=ingsheet_cemail[rownum]
   ing_comment=ingsheet_comment[rownum]
   ing_articleid=ingsheet_article[rownum] 
   ingest_no=ingestnums[rownum]
   ing_reqlastfi=ireq_lastfirstini[rownum]
   ing_corlastfi=icorr_lastfirstini[rownum]
   isheetinfo=[rownum+1,ing_requestor,ing_version,ing_date,ing_title,ing_comment,ing_articleid,ing_reqlastfi]
   print("Information from the Ingest sheet: ",isheetinfo)
 #Create a dictionary of all the fields read from the ingest sheet:
   dictingsheet=dict({'ingrownum': rownum+1,'ingestno':ingest_no,'ingrequestr':ing_requestor,'ingversion':ing_version,'ingestdate':ing_date,'ingtitle':ingsheet_title,'ingcemail':ing_cemail,'ingcomment':ing_comment,'ingarticleid': ing_articleid,'ingreqlastfirsti':ing_reqlastfi,'ingcorlastfirsti':ing_corlastfi})
   return dictingsheet
 else:
   dictingsheetAll=dict({'iRequestor': ingsheet_requestor,'iCorAuth':icorres_author,'iVersion':ingsheet_version,'iDate':ingsheet_date,'iTitle':ingsheet_title,'iCAemail':ingsheet_cemail,'iComment':ingsheet_comment,'iArticleid': ingsheet_article,'iIngestnum':ingestnums,'iReqLnameFini':ireq_lastfirstini,'iCorLnameFini': icorr_lastfirstini,'iDOIsuffix' : ingsheet_doi})
   return dictingsheetAll


#Following gets information from the spreadsheet version 7 "Published" sheet using the article id and version
def vtpubsheet(ArticleID,PublishedVersionNumber):

  """
  Purpose: 
  Access Published sheet from VTDR spreadsheet using VTDR curation services account and OAuth2 credentials from the Google API Console using credentails from the JSON file

  Parameters: 
  ArticleID: Figshare article ID of the article that needs to be read from the spreadsheet
  PublishedVersionNumber: Publication number of the published article whose row information needs to be read
   """
 #Get the parameters from configurations.ini to retrieve information on spreadsheet

  import configparser
  config=configparser.ConfigParser()
  config.read('configurations.ini')
  spreadSheet=config['SpreadsheetSettings']['SpreadsheetName']

  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  client = gspread.authorize(creds)
  
# use creds to create a client to interact with the Google Drive API
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  client = gspread.authorize(creds)
  #Open the spreadsheet sheet1: "Published"
  pubsheet = client.open(spreadSheet).worksheet('Published')
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
  #artid=['DOI']
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

  if ArticleID is not None:
  #find the row in the spreadsheet that corresponds to the given articleid:
   row_aidmatch=[i for i, e in enumerate(doisuffix) if e == ArticleID]
  #find the row in the spreadsheet that corresponds to the given version number:
   row_vermatch=[i for i, e in enumerate(version) if e == PublishedVersionNumber]
  #find the row in the spreadsheet that corresponds to the given articleid and version number
   rownum=np.intersect1d(row_aidmatch,row_vermatch)
   if (len(rownum)>1):
    print("two or more rows with the same publication for the same version")
  #the row number on the spreadsheet is rownum+1 due to array indexing from 0
  #convert numpy array to integer
   try:
     rownum=int(rownum)
   except TypeError:
    print("ROW INFORMATION FOR THE PROVIDED ARTICLE ID AND VERSION NUMBER WAS NOT FOUND IN THE PUBLISHED SHEET")
    print("Please enter the publication record information in the published sheet and try running again")
    sys.exit()
#   rownum=int(rownum)
   print("Published sheet rownumber: ",rownum)
  #get the Ingest number, Published Accession number, Requestion, Corresponding author, version number, date published, title, corresponding author email, college, department, date of most recent comment, most recent comment, article id from row that the article id and version correspond to from the spreadsheet
   psheet_ingestno=ingest_num[rownum]
   psheet_pubno=pubacc_num[rownum]
   psheet_reques=requestor[rownum]
   psheet_corrsaut=corres_author[rownum]
   psheet_vers=version[rownum]
   psheet_datepub=date_pub[rownum]
   psheet_doipub=doi[rownum]
   psheet_titlepub=title[rownum]
   psheet_corremail=corres_authemail[rownum]
   psheet_coll=college[rownum]
   psheet_departmnt=dept[rownum]
   psheet_datecomm=date_most_recent_comment[rownum]
   psheet_mostreccomm=most_recent_comment[rownum]
   psheet_articleid=doisuffix[rownum]
   psheet_reqlastfi=req_lastfirstini[rownum]
   psheet_corlastfi=corr_lastfirstini[rownum]
   psheetinfo=[rownum,psheet_articleid,psheet_ingestno, psheet_pubno,psheet_reques,psheet_corrsaut,psheet_vers,psheet_datepub,psheet_doipub,psheet_titlepub,psheet_corremail,psheet_coll,psheet_departmnt,psheet_datecomm,psheet_mostreccomm] 
   print("Information form the Published Sheet:",psheetinfo)
   #Create a dictionary of all the fields read from the Published sheet:
   dictgsvt=dict({'gsrownum':rownum+1,'gsarticleid':psheet_articleid,'gsingestno':psheet_ingestno,'gspubnum':psheet_pubno,'gsrequestr':psheet_reques,'gscorsauth':psheet_corrsaut,'gsversnum':psheet_vers,'gsdatepub':psheet_datepub,'gsdoi':psheet_doipub,'gstitle':psheet_titlepub,'gscorauthemail':psheet_corremail,'gscollg':psheet_coll,'gsdept':psheet_departmnt,'gsdatecomnt':psheet_datecomm,'gscomnt':psheet_mostreccomm,'gsreqlastfi':psheet_reqlastfi,'gscorrlastfi':psheet_corlastfi,'DOIsuffix':psheet_articleid})
   return dictgsvt
  else: 
   dictpubsheet=dict({'pDOIsuffix':doisuffix,'pIngestnum':ingest_num,'pPubnum':pubacc_num,'pRequestor':requestor,'pCorAuth':corres_author,'pVersion':version,'pDate':date_pub,'pDoi':doi,'pTitle':title,'pCAemail':corres_authemail,'pCollege':college,'pDept':dept,'pDateComnt':date_most_recent_comment,'pComment':most_recent_comment,'pReqLnameFini': req_lastfirstini,'pCorLnameFini':corr_lastfirstini})
   return dictpubsheet
