# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:05:20 2021

@author: padma carstens
""""
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

#Following gets data from the spreadsheet version 7 "Ingest" using the ingest number
def vtingsheet(ArticleID,IngestVersionNumber):
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
 #Get the column values for comment:
 ingsheet_comment=ingsheet.col_values(8)
 #Get the column values for article ID
 ingsheet_article=ingsheet.col_values(9)
#Find the row/rows in the spreadsheet that correspond to the given articleid 
 row_aidmatch=[i for i, e in enumerate(ingsheet_article) if e == ArticleID]
 #Find the row/rows in the spreadsheet that correspond to the given version
 row_vermatch=[i for i, e in enumerate(ingsheet_version) if e == IngestVersionNumber]
 #Find the row in the spreadsheet that corresponds to the given article ID and version number
 rownum=np.intersect1d(row_aidmatch,row_vermatch)
 #the row number on the spreadsheet is rownum+1 due to array indexing from 0
 #convert numpy array to integer
 rownum=int(rownum)
 print("Ingest sheet rownumber: ",rownum+1)

#Get the Requestion, Version, IngestDate, Title, Comment, ArticleID, IngestNumber that correspond the rownumber found above   
 ing_requestor=ingsheet_requestor[rownum]
 ing_version=ingsheet_version[rownum]
 ing_date=ingsheet_date[rownum]
 ing_title=ingsheet_title[rownum]
 ing_comment=ingsheet_comment[rownum]
 ing_articleid=ingsheet_article[rownum] 
 ingest_no=ingestnums[rownum]
 ing_reqlastfi=ireq_lastfirstini[rownum]
 ing_corlastfi=icorr_lastfirstini[rownum]
 isheetinfo=[rownum+1,ing_requestor,ing_version,ing_date,ing_title,ing_comment,ing_articleid]
 print("Information from the Ingest sheet: ",isheetinfo)
 dictingsheet=dict({'ingrownum': rownum+1,'ingestno':ingest_no,'ingrequestr':ing_requestor,'ingversion':ing_version,'ingestdate':ing_date,'ingtitle':ingsheet_title,'ingcomment':ing_comment,'ingarticleid': ing_articleid,'ingreqlastfirsti':ing_reqlastfi,'ingcorlastfirsti':ing_corlastfi})
 return dictingsheet


#Following gets information from the spreadsheet version 7 "Published" sheet using the article id and version
def vtpubsheet(articleid,vernum):
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
  artid=['DOI']
  for l in range(1,len(doi)):
    d=doi[l]
    v= d.split('/')[1]
    artid.append(v)
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
  #find the row in the spreadsheet that corresponds to the given articleid:
  row_aidmatch=[i for i, e in enumerate(artid) if e == articleid]
  #find the row in the spreadsheet that corresponds to the given version number:
  row_vermatch=[i for i, e in enumerate(version) if e == vernum]
  #find the row in the spreadsheet that corresponds to the given articleid and version number
  rownum=np.intersect1d(row_aidmatch,row_vermatch)
  #the row number on the spreadsheet is rownum+1 due to array indexing from 0
  #convert numpy array to integer
  rownum=int(rownum)
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
  psheet_articleid=artid[rownum]
  psheet_reqlastfi=req_lastfirstini[rownum]
  psheet_corlastfi=corr_lastfirstini[rownum]
  psheetinfo=[rownum,psheet_articleid,psheet_ingestno,psheet_pubno,psheet_reques,psheet_corrsaut,psheet_vers,psheet_datepub,psheet_doipub,psheet_titlepub,psheet_corremail,psheet_coll,psheet_departmnt,psheet_datecomm,psheet_mostreccomm] 
  print("Information form the Published Sheet:",psheetinfo)
  dictgsvt=dict({'gsrownum':rownum+1,'gsarticleid':psheet_articleid,'gsingestno':psheet_ingestno,'gspubnum':psheet_pubno,'gsrequestr':psheet_reques,'gscorsauth':psheet_corrsaut,'gsversnum':psheet_vers,'gsdatepub':psheet_datepub,'gsdoi':psheet_doipub,'gstitle':psheet_titlepub,'gscorauthemail':psheet_corremail,'gscollg':psheet_coll,'gsdept':psheet_departmnt,'gsdatecomnt':psheet_datecomm,'gscomnt':psheet_mostreccomm,'gsreqlastfi':psheet_reqlastfi,'gscorrlastfi':psheet_corlastfi})
  return dictgsvt
