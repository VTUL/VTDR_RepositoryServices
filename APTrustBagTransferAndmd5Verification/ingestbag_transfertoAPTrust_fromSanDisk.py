"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""
"""
Purpose: 
-searches for bags in the sandisk copied from s3, for the range of the row numbers provided from the spreadsheet,search for the ingest bag is performed using the ingest number match with the bag name in tar format sitting in san disk
-Extracts the old bags made with UPACK and the newer bags made by DART
- Performs bag validation on the bag made by UPACK, creates DART bag using APTrust tag values, deposits the new DART bag to APTrust, compares the md5 checksums of the bags made by UPACK and DART software in tar format for bags entered on the spreadsheet starting for the row numbers provided in rowstrt and rowend. Bags were transferred 10 at a time to APTrust and transfer was checked and log sheets were verified, tracking was updated by  Padma and Jon in MOVING_CONTENT_PROCESS_TRACKING_2022 sheet in 'MovingContentToAPTrust' folder in CurationServicesGoogleDriveArchive
- Creates a sheet in the path provided under 'sheetname' with filenames and md5 checksum list of the associated files and the comparison results, also creates log file with the name and path provided with more details. Log files and sheets were created in 'MovingContentToAPTrust' folder in curation services google drive archive.

Parameters: 
rowstart: row number of the 2021 vtdr spreadsheet where transfer starts
rownd: row number of the 2021 vtdr spreadsheet where transfer ends
sheetname: creates the provided sheetname at the specified path containing md5 checksum verification results of the 2 bags that are compared
sizeul: the upper limit of the size of the bag on which md5 verification is to be performed.
sheet: add the sheet with the provided name
dartpath: path to the folder where bags created using aptrust tag values and DART app are created
LOG_FILENAME: path to where the log file is created in text format, containing md5 checksum verification results of the 2 bags that are compared
filename_s3: filename of the bag in s3 in tar format
path1: path of the bag on s3
filename_gd: filename of the bag in google drive in tar format
path: path of the bag on google drive
"""
import os
from os.path import exists
import json
from turtle import begin_fill
#from typing import _KT_co
from ldcoolp.curation import retrieve
import spreadsheet_aptrust_transfer
import sys
sys.path.insert(0,'C:/Users/padma/anaconda3/envs/curation/VTechDataRepo/Figshare-APTrust')

from Read_VTDR_Spreadsheet import vtingsheet
from Read_VTDR_Spreadsheet import vtpubsheet

import shutil
import tarfile
from tarfile import TarFile
import job
from job import Job
from cmath import log
import logging
from datetime import datetime
from xlrd import open_workbook
from xlwt import Workbook
#from xlutils.copy import copy
import filecomparetestmod
from filecomparetestmod import comparemd5txt
import bagit


#Fetch information from Ingest sheet

#ivtsheet=aptrust_vtingsheet()
ivtsheet=vtingsheet(ArticleID=None,IngestVersionNumber=None)
#Get article id 
iArticleid=ivtsheet['iArticleid']
iDOIsuffix=ivtsheet['iDOIsuffix']
#get requestor name
iRequestor=ivtsheet['iRequestor']
#get corresponding author name
iCorrespondingAuthor=ivtsheet['iCorAuth']
#get version
iVersion=ivtsheet['iVersion']
#get ingested date in YYYYMMDD format 
iDate= ivtsheet['iDate'] 

#Create Ingest folder to store dataset
iIngAccessionNumber= ivtsheet['iIngestnum']
iRequestorLFI=ivtsheet['iReqLnameFini']
iCorrespondingAuthorLFI=ivtsheet['iCorLnameFini']

#************CHANGE rowstart and rownd FOR EVERY 10 BAG RUN***************************
rowstart=121
rownd=122
#rownd=121
rowstrt=rowstart-1
rowend=rownd-1
transferbagnames=iIngAccessionNumber[rowstrt]+"_"+iIngAccessionNumber[rowend]
#Create a log sheet

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/'+transferbagnames+'_'+'%Y%m%d_%H%M.xls')
wb=Workbook(sheetname)

sheet1=wb.add_sheet(transferbagnames)#this name has a character limit

sheet1.write(0, 0, 'Bagname made by UPACK')
sheet1.write(0, 1, 'Bagname made by DART')
sheet1.write(0, 2, 'ValidationTest of bag made by UPACK')
sheet1.write(0, 3, 'Size of bag in tar format made with UPACK(in GB)')
sheet1.write(0, 4, 'Size of bag in tar format made with DART(in GB)')
sheet1.write(0, 5, 'DART Job Completed/Failed')
sheet1.write(0,6,'Filenames associated with the checksums in bag made by UPACK')
sheet1.write(0,7,'Filenames associated with the checksums in bag made by DART')
sheet1.write(0,8,'MD5 checksum of payload files in bag made by UPACK')
sheet1.write(0,9,'MD5 checksum of payload files in bag made by DART')
sheet1.write(0,10,'Additional Files in bag made by UPACK(not found in bag made by DART')
sheet1.write(0,11,'md5 checksum of additional file in bag made by UPACK')
sheet1.write(0,12,'Additional Files in bag made by DART(not found in bag made by UPACK')
sheet1.write(0,13,'md5 checksum of additional file in bag made by DART')
sheet1.write(0,14,'md5 checksum of additional file in bag made by DART')
#sheet1.write(0,15,'Exceptions with the bag made by UPACK')
sheet1.write(0,15,'Comments')
#Create a log file

LOG_FILENAME=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration\MovingContentToAPTrust/APTrustTransferLogfile_'+transferbagnames+'_'+'%Y%m%d_%H%M.log')
ext=".tar"
i1=1

#Fetch information from published sheet

Pvtsheet=vtpubsheet(ArticleID=None,PublishedVersionNumber=None)
pPubAccessionNumber= Pvtsheet['pPubnum']
pIngAccessionNumber=Pvtsheet['pIngestnum']
pRequestorLFI=Pvtsheet['pReqLnameFini']
pCorrespondingAuthorLFI=Pvtsheet['pCorLnameFini']
#get version
pVersion=Pvtsheet['pVersion']
pDate=Pvtsheet['pDate']
pDOIsuffix=Pvtsheet['pDOIsuffix']
sourcedir1="F:/VTechbags"
count=0

"""
#************10 loop bag runs***************************
#Example1 of indexing: for P23-P30: i=22 gets the row 23 which is the bag P00021, i=22,32 runs until i=31 and terminates when i=32, so last bag corresponds to i=31,row 32 which is P00030
#Example 2 indexing: for P41-P50: i=42 gets the row 43 which is the bag P00041, i=42,53 runs until i=52 and terminates when i=53, so last bag corresponds to i=52,row 53 which is P00050
"""
  
for i in range(rowstrt,rowend):      
  wb.save(sheetname)
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
  #IngOrPub='P' #0 for ingest 1 for pub
  IngOrPub='I'
  print("Row number on spreadsheet is " , i+1)
  logging.info("Row number on spreadsheet is %s " % str(i+1))
  HeadDir="F:\\"
  print("ingorpub",IngOrPub)
#Start processing I is for ingest, P is for publication bag:

  if IngOrPub=='I':
    SubDir3=f"{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}.tar"
    print("**********NOW PROCESSING ",iIngAccessionNumber[i],"**********")
    logging.info("**************************NOW PROCESSING %s ****************" % iIngAccessionNumber[i])

  #No exception/comment fetch:
  if IngOrPub=='P':
    SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}.tar"
  
#-------------------find ingest bag based on the first ingest number of the ingest bag string and version number
  if rowstart == 143 :
    files = [i2 for i2 in os.listdir(HeadDir) if os.path.isfile(os.path.join(HeadDir,i2)) and iIngAccessionNumber[i] in i2]#this is to accomodate for missing v01 in I141
  if rowstart == 160 :
    files = [i2 for i2 in os.listdir(HeadDir) if os.path.isfile(os.path.join(HeadDir,i2)) and iIngAccessionNumber[i] in i2]#this is to accomodate for missing v01 in I141  
  else:
    files = [i2 for i2 in os.listdir(HeadDir) if os.path.isfile(os.path.join(HeadDir,i2)) and iIngAccessionNumber[i] in i2 and iVersion[i] in i2]
  #For bag I00124: saved as 100124 with a number "1" instead of "I",so include this in the search instead of I00124, comment out the above line, and uncomment line below

  #files = [i2 for i2 in os.listdir(HeadDir) if os.path.isfile(os.path.join(HeadDir,i2)) and "100124" in i2 and iVersion[i] in i2]

  print("files are ",files)
  x=iIngAccessionNumber[i]
  print(x)
  y=iVersion[i]
  print(y)
  print("Head Directory is iIngAccessionNumber is ",iIngAccessionNumber[i]," iVersion is ",iVersion[i])
# if list exists true then do something; if list does not exist then do something else
  if files:
 #files returns file names which have I00xyz and v01 in the bag name as a list
    print("Ingest bag with ingest number ",iIngAccessionNumber[i]," exists and the ingest bag is ",files[0])
    print("**********NOW PROCESSING ",iIngAccessionNumber[i],"**********")
    logging.info("**************************NOW PROCESSING %s ****************" % iIngAccessionNumber[i])

 #Check if bag exists in original format, if not then check if it exists without a v in the bag name:  
    SubDir3=SubDir3.strip()
  #bagpath=os.path.join(HeadDir,SubDir3)
    bagpath=os.path.join(HeadDir,files[0])
    print("Ingest bag following the naming convention is ",SubDir3)
    if not os.path.exists(bagpath):
      print("Bag in tar format does not exist: ", SubDir3)
      logging.info("Bag in tar format does not exist: %s " % SubDir3)
    

    print("Bagname with path is : ", bagpath)
    logging.info("Bagname with path is %s " % bagpath)

  #If bag exists, find the size of the bag, extract the bag and check for validation:
    path1=bagpath#os.path.join( os.path.abspath(root1), filename1 )
    bag_size=os.path.getsize(path1)
    bag_size_gb=bag_size/(10**9)
    #size=20100
    sizeul=24*(10**9)#less than 24 GB
    #if bag_size >= size and bag_size <= sizeul:
    print("i1 is ",i1)
    count=count+1
    path1=bagpath#os.path.join( os.path.abspath(root1), filename1 )
    bag_size=os.path.getsize(path1)
      #bag_size_gb=bag_size/(10**9)
    #print("Bagname tar in S3 VTechbags is ",SubDir3,"\n") 
    print("Bagname tar in S3 VTechbags is ",files[0],"\n") 
    #sheet1.write(i1,0,SubDir3)
    sheet1.write(i1,0,files[0])
    print("Bagsize tar on S3 is: ",bag_size_gb)
    #logging.info("Bagname in S3 VTechbags is  %s " % SubDir3)
    logging.info("Bagname in S3 VTechbags is  %s " % files[0])
    
    logging.info("BagSize on S3 is %s " % bag_size_gb)
    sheet1.write(i1,3,bag_size_gb)
    aptrustBagName=f"VTDR_{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}"#f"VTDR_{extractedbag}"#this does not end with .tar
    aptrustBagName_tar=f"{aptrustBagName}.tar"
    print("APTrust bag name is ",aptrustBagName)
    print("APTrust bagname in tar format is ",aptrustBagName_tar)
    logging.info("APTrust bag name is %s " % aptrustBagName)   
    logging.info("APTrust bagname in tar format is %s " % aptrustBagName_tar)    
    sheet1.write(i1,1,aptrustBagName_tar)


    #1st set of transfer was for bags less than 24GB
    #if bag_size >= size and bag_size <= sizeul:
    #2nd set of transfer done on 20221116 for bags greater than 24GB
    if bag_size > sizeul:
      directory_path="F:\\"  
       
      destpath='F:\\'
    #if i != 96 :   
    #Extract/Untar bag on sandisk:
      mytar=tarfile.open(bagpath,"r")
    #destpath='F:\\'
      mytar.extractall(destpath)
      mytar.close()
    
    #extractedbag=SubDir3.replace('.tar','')
      extractedbag=files[0].replace('.tar','')
      print("Extracted bag ",extractedbag)
      logging.info(" Extracted bag on SanDisk is %s " % extractedbag)
      extractedbagpath=os.path.join(destpath,extractedbag)
      bag=bagit.Bag(extractedbagpath)
    #Check if bag is valid:    
      if bag.is_valid():
          print("Bag is valid")
          logging.info("Bag is valid %s " % extractedbag)
          sheet1.write(i1,2,"Bag is valid")
        #for ingest there is not additional 3rd path for below bags in 'if' 
        #source_folder=os.path.join(extractedbagpath,"data",extractedbag)s
          print("rowstrt is ",rowstrt)
          
          if rowstrt == 139 or rowstrt ==144 or rowstart == 178 or rowstart ==181:
            source_folder=os.path.join(destpath, extractedbag,"data")
          else:
            source_folder=os.path.join(destpath, extractedbag,"data",extractedbag) 
          if rowstart >= 183 and rowstart <= 206:
            source_folder=os.path.join(destpath, extractedbag,"data") 

            
          #else:            
          
          print("payload is at : ",source_folder)
          payload=os.listdir(source_folder)
        ##Bagging with DART:        
      #-----------------------------------------------------------------------  
     
         # job=Job("Workflow for depositing bag to APTrust-Demo",aptrustBagName)
          job=Job("Workflow for depositing bag to APTrust-Repo",aptrustBagName)
          for f in payload:
            job.add_file(source_folder+"\\"+f)
            print("Added following file to bag in DART: ",f)
            logging.info("Added following file to bag in DART: %s " % f)
        
        #Bag Group Identifier for ingest:        
          if IngOrPub=='I':
            bag_group_identifier=f"VTDR_{iIngAccessionNumber[i]}"
            job.add_tag("bag-info.txt", "Bag-Group-Identifier", bag_group_identifier)
        #Bag Group Identifier for Published:   
          if IngOrPub=='P':
            bag_group_identifier=f"VTDR_{pPubAccessionNumber[i]}"
            job.add_tag("bag-info.txt", "Bag-Group-Identifier", bag_group_identifier)
          job.add_tag("bag-info.txt","Source-Organization","Virginia Tech")
          job.add_tag("aptrust-info.txt", "Access", "Institution")
          job.add_tag("aptrust-info.txt", "Storage-Option", "Standard")
          aptrust_title=aptrustBagName
          job.add_tag("aptrust-info.txt","Title",aptrust_title)
          job.add_tag("bagit.txt","BagIt-Version","0.97")
          job.add_tag("bagit.txt","Tag-File-Character-Encoding","UTF-8")

          exit_code = job.run()
          if exit_code == 0:
            print("Job completed")
            print("**************************BAG MIGRATED SUCCESSFULLY TO APTRUST****************")
            logging.info("Job completed")
            logging.info("***************************BAG MIGRATED SUCCESSFULLY TO APTRUST****************")
            sheet1.write(i1,5,"Job completed")
          else:
            print("Job failed. Check the DART log for details.")
            logging.info("Job failed. Check the DART log for details.")
            print("**************************BAG MIGRATION TO APTRUST FAILED****************")
            logging.info("**************************BAG MIGRATION TO APTRUST FAILED****************")
            sheet1.write(i1,5,"Job Failed")
     
       #Compare manifest-md5 in bag made by DART and transferred to APTrust with bag made by UPACK

        #Get size of bag in tar format made by DART, then untar the bag made by dart stored as a local copy

          dartpath = "C:/Users/padma/.dart/bags/"
        #dartpath = os.getenv("dartpath")
          dartBagPath=os.path.join(dartpath,aptrustBagName_tar)
          dartBagSize=os.path.getsize(dartBagPath)
          dartBagSizeGB=dartBagSize/(10**9)
          sheet1.write(i1,4,dartBagSizeGB)
        #Extract/Untar bag made by DART:
          openDartTar=tarfile.open(dartBagPath,"r")
          destnpath=dartpath
          #destnpath="C:/Users/padma/.dart/bags/"
        #destnpath=os.getenv("DartDestnpath")
          openDartTar.extractall(destnpath)
          openDartTar.close()
          dartextractedbag=os.path.join(dartpath,aptrustBagName)#SubDir3.replace('.tar','')
          print("Extracted bag by DART",dartextractedbag)
          logging.info("Extracted bag by DART %s " % dartextractedbag)
        #Check md5 checksums of files in bags made by DART and UPACK:
          print("checking md5 of UPACK payload vs DART payload \n")
          logging.info("checking md5 of UPACK payload vs DART payload ")
          upack_manifestmd5 = os.path.join(extractedbagpath,"manifest-md5.txt")
          dart_manifestmd5=os.path.join(dartpath,aptrustBagName,"manifest-md5.txt")  
          x=comparemd5txt(upack_manifestmd5,dart_manifestmd5)
          Upackmd5=x['UPackmd5']
          UpackFilenames=x['UPackFilenames']
          Dartmd5=x['Dartmd5']
          DartFilenames=x['DartFilenames']
          Upackmd5Match=x['UPackmd5MatchedwithDart']
          Dartmd5Match=x['Dartmd5MatchedwithUpack']
          UpackFilesAssWithMD5Match=x['UPackmd5FilesmatchedwithDart']
          DartFilesAssWithMD5Match=x['Dartmd5FilesmatchedwithUpack']
          AddUpackFilesNotInDart=x['AdditionalUpackFilesNotFoundInDart']
          AddDartFilesNotInUpack=x["AdditionalDartFilesNotFoundInUpack"]
          AdditionalUpackmd5=x["AdditionalUpackmd5"]
          AdditionalDartmd5=x["AdditionalDartmd5"]
        #Log the matched and unmatched checksums to log file:
          print("UPackmd5 is ", Upackmd5 ,"\n\n\n")
          logging.info("UPackmd5 is %s " % Upackmd5 )
          print("Dartmd5 is ", Dartmd5 ,"\n\n\n")
          logging.info("Dartmd5 is %s " % Dartmd5)
          print("UPackFilenames are ", UpackFilenames ,"\n\n\n")
          logging.info("UPackFilenames are %s " % UpackFilenames)
          print("DartFilenames are ", DartFilenames ,"\n\n\n")
          logging.info("DartFilenames are %s " % DartFilenames)
          print("Upack md5s matched with Dart are ",Upackmd5Match,"\n\n\n")
          logging.info("Upack md5s matched with Dart are %s" % Upackmd5Match)
          print("UPack files associated with matched md5 with DART are ", UpackFilenames,"\n\n\n")
          logging.info("UPack files associated with matched md5 with DART are %s " % UpackFilenames)
          print("Additional Files in Upack are ",AddUpackFilesNotInDart, "\n\n\n")
          logging.info("Additional Files in Upack are %s " % AddUpackFilesNotInDart)
          print("Additional md5 associated with additional files in Upack ",AdditionalUpackmd5,"\n\n\n")
          logging.info("Additional md5 associated with additional files in Upack %s" % AdditionalUpackmd5)    
          print("Additional Dart Files not in Upack for matched md5s are ",AddDartFilesNotInUpack,"\n\n\n")
          logging.info("Additional Dart Files not in Upack for matched md5s are %s " % AddDartFilesNotInUpack)
          print("Additional md5 associated with additional files in DART ",AdditionalDartmd5,"\n\n\n")
          logging.info("Additional md5 associated with additional files in DART %s " % AdditionalDartmd5)
       
       #Log the matched and unmatched checksums to spreadsheet:

          for i4 in range(len(Upackmd5Match)):
            sheet1.write(i1,6,UpackFilesAssWithMD5Match[i4])
            sheet1.write(i1,7,DartFilesAssWithMD5Match[i4])      
            sheet1.write(i1,8,Upackmd5Match[i4])
            sheet1.write(i1,9,Dartmd5Match[i4])
            i1=i1+1
          if len(AddUpackFilesNotInDart)>=1:
            sheet1.write(i1,10,AddUpackFilesNotInDart)
            sheet1.write(i1,11,AdditionalUpackmd5)
            i1=i1+1

          if len(AddDartFilesNotInUpack)>=1:
            sheet1.write(i1,12,AddDartFilesNotInUpack)
            sheet1.write(i1,13,AdditionalDartmd5)
            i1=i1+1
         
      else:
        print("Bag is not valid")
        logging.info("Bag is not valid")
        sheet1.write(i1,2,"Bag is not valid")
        print("****************BAG VALIDATION FAILED FOR BAG ",extractedbagpath," SO BAG NOT MIGRATED to APTRUST****************")
        logging.info("****************BAG VALIDATION FAILED FOR BAG %s SO BAG NOT MIGRATED to APTRUST****************" % extractedbagpath)
        
    else:
        print("size of bag is less than lower limit of ",size," = ",' or bag size is greater than upper limit of ', sizeul )
        print("size of bag in GB is ",bag_size_gb)
        #print("**************************BAG ", bagpath," NOT FOUND SO NOT MIGRATED TO APTRUST****************************")
        logging.info("size of bag is less than lower limit of %s = " % size )
        logging.info("OR size of bag is greater than upper limit of %s = " % sizeul )
        logging.info("size of the bag calculated is %s" % bag_size)
        logging.info("size of bag in GB is %s =",bag_size_gb)
        # NOT FOUND SO NOT MIGRATED TO APTRUST****************************" % SubDir3 )
          ##Exception for corresponding author labelled with no LFI for pub bag P00005
        print("************************THE FOLLOWING PUBLICATION BAG HAS A COMMENT***************************")
        print("Comment: Bag size is ~10GB, bag transferred seperately")
        sheet1.write(i1,15,bag_size_gb)
        logging.info("************************THIS PUBLICATION BAG HAS A COMMENT***************************")
        logging.info("Comment: Bag size is below lower transfer limit and above higher transfer limit so bag transferred seperately \n")

  else:
    print("Bag does not exist, bag name is ",SubDir3)
    logging.info("Bag does not exist, bag name is %s " % SubDir3)
    sheet1.write(i1,0,SubDir3)
    aptrustBagName=f"VTDR_{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}"#f"VTDR_{extractedbag}
    sheet1.write(i1,1,aptrustBagName)
    sheet1.write(i1,2,"BAG DOES NOT EXIST IN THE EXPECTED FORMAT ON FIRST TRY OF TRANSFER, SO BAG WILL BE TRANSFERRED SEPERATELY IF IT EXISTS IN A DIFFERENT FORMAT OR BAG WAS ABANDONED AND SO DOES NOT EXIST")
 
  i1=i1+1
  print("MY i1 is ",i1)
  print("i1 at the end of last compute is ",i1)
  logging.info("i1 at the end of last compute is %s " % i1)  

#Adjust column size of the log spreadsheet
sheet1.col(0).width = 15000
sheet1.col(1).width = 15000
sheet1.col(2).width = 10000
sheet1.col(3).width = 10000
sheet1.col(4).width = 10000
sheet1.col(5).width = 7000
sheet1.col(6).width = 30000
sheet1.col(7).width = 30000
sheet1.col(8).width = 12000
sheet1.col(9).width = 12000
sheet1.col(10).width = 10000
sheet1.col(11).width = 12000
sheet1.col(12).width = 15000
sheet1.col(13).width = 10000
sheet1.col(14).width = 10000
sheet1.col(15).width = 40000
sheet1.col(16).width = 4000

wb.save(sheetname)

