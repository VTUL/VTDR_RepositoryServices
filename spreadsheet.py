# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 14:05:20 2021

@author: padma
"""

#from VTechDataServices.auto_fill_archive import DateIngested
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


#Following gets data from the spreadsheet "Ingest" using the ingest number
def vtingsheet(ing):
 ingestno=ing
 scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
 creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
 client = gspread.authorize(creds)
 ingsheet = client.open("20180628_VTechData_PublishedDatasets_LogAndStatus_V6").sheet1
 ingestnums=ingsheet.col_values(1)
 ingsheet_requestor=ingsheet.col_values(2)
 ingsheet_version=ingsheet.col_values(3)
 ingsheet_date=ingsheet.col_values(4)
 ingsheet_title=ingsheet.col_values(5)
 ingsheet_comment=ingsheet.col_values(7)
 ingsheet_article=ingsheet.col_values(8)
 find_ing= ingsheet.find(ingestno)
 y=str(find_ing)
 ingrowcol=re.findall('\d+',y)
 ingrownum=int(ingrowcol[0])
 ingcolnum=int(ingrowcol[1])
 ing_requestor=ingsheet_requestor[ingrownum-1]
 ing_version=ingsheet_version[ingrownum-1]
 ing_date=ingsheet_date[ingrownum-1]
 ing_title=ingsheet_title[ingrownum-1]
 ing_comment=ingsheet_comment[ingrownum-1]
 ing_articleid=ingsheet_article[ingrownum-1] 
 ingest_no=ingestnums[ingrownum-1]
 isheetinfo=[ingrownum,ingcolnum,ing_requestor,ing_version,ing_date,ing_title,ing_comment,ing_articleid]
 print(isheetinfo)
 dictingsheet=dict({'ingrownum':ingrownum,'ingcolnum':ingcolnum,'ingestno':ingest_no,'ingrequestr':ing_requestor,'ingversion':ing_version,'ingestdate':ing_date,'ingtitle':ingsheet_title,'ingcomment':ing_comment,'ingarticleid': ing_articleid})
 return dictingsheet


#Following gets information from the spreadsheet "Published" using the publication number
def vtpubsheet(pub,vernum):
# use creds to create a client to interact with the Google Drive API
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  client = gspread.authorize(creds)

# Find a workbook by name and open the published sheet
  pubsheet = client.open("20180628_VTechData_PublishedDatasets_LogAndStatus_V6").worksheet('Published')
  published_acc_no=pub
  ingest_num=pubsheet.col_values(1)
  pubacc_num=pubsheet.col_values(2)
  requestor=pubsheet.col_values(3)
  corres_author=pubsheet.col_values(4)
  version=pubsheet.col_values(5)
  date_pub=pubsheet.col_values(6)
  doi=pubsheet.col_values(7)
  title=pubsheet.col_values(8)
  corres_authemail=pubsheet.col_values(9)
  college=pubsheet.col_values(10)
  dept=pubsheet.col_values(11)
  date_most_recent_comment=pubsheet.col_values(12)
  most_recent_comment=pubsheet.col_values(13)
  #Find the row number of the publication from the spreadsheet:
  find_pubno = pubsheet.findall(published_acc_no)#findsall
  find_ver=pubsheet.findall(vernum)
  pubstring=str(find_pubno)#convert the row/col number of the corres. publication no. into a string
  verstring=str(find_ver)#convert the row/col number of the corres. publication no. into a string
  #Extract the row /col number from the above lists, for example for P00119 above strings look like [<Cell R97C5 '03'>, <Cell R148C5 '03'>, <Cell R171C5 '03'>] and [<Cell R97C5 '03'>, <Cell R148C5 '03'>, <Cell R171C5 '03'>]
  pubrowcol=re.findall('\d+',pubstring)#this gives ['97', '5', '03', '148', '5', '03', '171', '5', '03'] 
  verrowcol=re.findall('\d+',verstring)#this gives ['129', '2', '00119', '130', '2', '00119', '171', '2', '00119']
  #Get the rows:
  x=np.array(pubrowcol)
  y=np.array(verrowcol)
  #find which row corresponds to the giver publication number and version number
  z=np.where(x==y)#in our example above this is index 6 of the arrays
  rownum=int(x[z])#in our example this is row 171 ,int[171] returns the integer 171, which corresponds to P00119 and version 3
  psheet_ingestno=ingest_num[rownum-1]
  psheet_pubno=pubacc_num[rownum-1]
  psheet_reques=requestor[rownum-1]
  psheet_corrsaut=corres_author[rownum-1]
  psheet_vers=version[rownum-1]
  psheet_datepub=date_pub[rownum-1]
  psheet_doipub=doi[rownum-1]
  psheet_titlepub=title[rownum-1]
  psheet_corremail=corres_authemail[rownum-1]
  psheet_coll=college[rownum-1]
  psheet_departmnt=dept[rownum-1]
  psheet_datecomm=date_most_recent_comment[rownum-1]
  psheet_mostreccomm=most_recent_comment[rownum-1]
  #split doi to get the article id:
  pubdoi=psheet_doipub
  splitdoi=pubdoi.split("/")
  psheet_articleid=splitdoi[1]
  psheetinfo=[rownum,psheet_articleid,psheet_ingestno,psheet_pubno,psheet_reques,psheet_corrsaut,psheet_vers,psheet_datepub,psheet_doipub,psheet_titlepub,psheet_corremail,psheet_coll,psheet_departmnt,psheet_datecomm,psheet_mostreccomm] 
  print(psheetinfo)
  dictgsvt=dict({'gsrownum':rownum,'gsarticleid':psheet_articleid,'gsingestno':psheet_ingestno,'gspubnum':psheet_pubno,'gsrequestr':psheet_reques,'gscorsauth':psheet_corrsaut,'gsversnum':psheet_vers,'gsdatepub':psheet_datepub,'gsdoi':psheet_doipub,'gstitle':psheet_titlepub,'gscorauthemail':psheet_corremail,'gscollg':psheet_coll,'gsdept':psheet_departmnt,'gsdatecomnt':psheet_datecomm,'gscomnt':psheet_mostreccomm})
  return dictgsvt
