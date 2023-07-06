

from cmath import log
import os
from os.path import exists
import json
from turtle import begin_fill
import sys
import shutil #Used for copying files
import logging
from datetime import datetime
import re
import hashlib
import xlwt
#from xlrd import open_workbook
from xlwt import Workbook
#from xlutils.copy import copy
from test_md5 import md5sum
from retrying import retry
from datetime import datetime
sys.path.append('C:/Users/padma/anaconda3/envs/curation/VTDR_RepositoryServices/Figshare-APTrust')

from Read_VTDR_Spreadsheet import vtingsheet
from Read_VTDR_Spreadsheet import vtpubsheet

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/SandiskVsSpreadsheetBagItems_'+'%Y%m%d_%H%M_.xls')
#------------------------------------
wb=Workbook(sheetname)
#sheet = wb.add_sheet("MD5VerificationPubBags_"+bagstartID+"_"+bagendID)
sheet = wb.add_sheet("BagsOnSandiskVs2021Sheet")
sheet.write(0, 0, 'BagName on Sandisk')
sheet.write(0,1,'IngestNumber on Sandisk')
sheet.write(0, 2, 'BagName on 2021Sheet')
sheet.write(0, 3, 'Matching')
sheet.write(0,4,'BagSizeOnSandisk')
#----------------------------------------------
#Fetch information from Ingest sheet
ivtsheet=vtingsheet(ArticleID=None,IngestVersionNumber=None)
pvtsheet=vtpubsheet(ArticleID=None,PublishedVersionNumber=None)
#Create Ingest folder to store dataset
iIngAccessionNumber= ivtsheet['iIngestnum']
pPubAccessionNumber=pvtsheet['pPubnum']
i3=1
#print(iIngAccessionNumber)
for i in iIngAccessionNumber:
   sheet.write(i3,2,i)
   i3=i3+1
for k in pPubAccessionNumber:
   sheet.write(i3,2,k)
   i3=i3+1
#---------------------------
sourcedir1="E:"
sourcedir2="C:/Users/padma/anaconda3/envs/curation/MissedGoogleDriveBags"
ext=".tar"
bagCount=0
bagNames=[]
iAccNum=[]
for root1, dirs1, bags1 in os.walk(sourcedir1):
  for bagname1 in bags1:
    if bagname1.endswith(ext) :
      bagCount=bagCount+1
      sheet.write(bagCount,0,bagname1)
      path1=os.path.join( os.path.abspath(root1), bagname1 )
      bag_size=os.path.getsize(path1)
      bag_size_gb=bag_size/(10**9)
      sheet.write(bagCount,4,bag_size_gb)
      if bagname1[0:4]== 'VTDR':
         iNumber=bagname1[5:11]
         iAccNum.append(iNumber)
         sheet.write(bagCount,1,iNumber)
      bagNames.append(bagname1)

#print(iAccNum)
#---------------------
from numpy import *
import numpy as np
a=iAccNum
b=iIngAccessionNumber
#c=a==b
#print("Result of a==b ",c)
#indices = np.where(np.in1d(b,a))[0]
#sheet.write()
#print(indices)
#matchedNums=a[indices]
#-------------col3
#i4=1
#print(iIngAccessionNumber)
#for y in indices:
#   sheet.write(i4,3,b[y])
#   i4=i4+1
#----------------------------
import numpy as np
x = np.array(b)
y = np.array(a)

index = np.argsort(x)
sorted_x = x[index]
sorted_index = np.searchsorted(sorted_x, y)

yindex = np.take(index, sorted_index, mode="clip")
mask = x[yindex] != y

result = np.ma.array(yindex, mask=mask)
print(result)
print(type(result))
#sheet.write(1:len(result),3,result)
#i4=1
#for y in range(0,len(result)-1):
#   print(result[y])
#   sheet.write(i4,3,result(y))
#   i4=i4+1
#sheet.write(i4,3,b[y])

sheet.col(1).width = 15000
sheet.col(2).width = 15000
sheet.col(3).width = 15000
sheet.col(4).width = 15000
sheet.col(5).width = 15000
wb.save(sheetname)

