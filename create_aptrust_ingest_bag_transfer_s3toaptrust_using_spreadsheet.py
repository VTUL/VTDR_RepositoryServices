#This code is used for transferring content from S3(stored locally on sandisk) to APTrust using DART. 

#******************************TOTAL 5 CHANGES
"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""

import os
from os.path import exists
import json
from turtle import begin_fill
#from typing import _KT_co
from ldcoolp.curation import retrieve
import spreadsheet_aptrust_transfer
#from auto_fill_archive import create_archivalreadme
from spreadsheet_aptrust_transfer import aptrust_vtingsheet
from spreadsheet_aptrust_transfer import aptrust_vtpubsheet
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
from xlutils.copy import copy
import filecomparetestmod
from filecomparetestmod import comparemd5txt
import bagit

#Create a log sheet
#************CHANGE(1) FOR EVERY 10 BAG RUN***************************
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P31_to_P40.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P32.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P51_to_P60.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P50.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P61_to_P70.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P62.xls')
#sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P64.xls')
sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/APTrustTransferInformationSheet_%Y%m%d_%H%M_P71_to_P80.xls')
wb=Workbook(sheetname)

#************CHANGE(2) FOR EVERY 10 BAG RUN***************************
#sheet1=wb.add_sheet("APTrustTransferSheet_P31_P40")
#sheet1=wb.add_sheet("APTrustTransferSheet_P32")
#sheet1=wb.add_sheet("APTrustTransferSheet_P41_P50")
#sheet1=wb.add_sheet("APTrustTransferSheet_P50")
#sheet1=wb.add_sheet("APTrustTransferSheet_P51_P60")
#sheet1=wb.add_sheet("APTrustTransferSheet_P61_P70")
#sheet1=wb.add_sheet("APTrustTransferSheet_P62")
#sheet1=wb.add_sheet("APTrustTransferSheet_P64")
sheet1=wb.add_sheet("APTrustTransferSheet_P71_P80")
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
sheet1.write(0,15,'Exceptions with the bag made by UPACK')
sheet1.write(0,16,'Comments')
#Create a log file
#************CHANGE(3) FOR EVERY !) BAG RUN ***************************
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P31_to_P40.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P32.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P61_to_P70.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P50.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P62.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P64.log')
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/APTrustTransferLogfile_%Y%m%d_%H%M_P71_to_P80.log')
ext=".tar"
i1=1

#Get information from spreadsheet "20211214_VTDR_PublishedDatasets_Log_V7": Ingest and Published sheet columns as lists/arrays:

#Fetch information from Ingest sheet

ivtsheet=aptrust_vtingsheet()
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

#Fetch information from published sheet
Pvtsheet=aptrust_vtpubsheet()
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


#************CHANGE (4) FOR 10 LOOP RUN***************************
#indexing for i for P1-P10: 1,11
#indexing for i below for P11-P20: 11, 22 i=21 gets the bag P00020 which is row 22
#indexing for i for P23-P30: i=22 gets the row 23 which is the bag P00021, i=22,32 runs until i=31 and terminates when i=32, so last bag corresponds to i=31,row 32 which is P00030
#indexing for i for P41-P50: i=42 gets the row 43 which is the bag P00041, i=42,53 runs until i=52 and terminates when i=53, so last bag corresponds to i=52,row 53 which is P00050
#for i in range(21,30):
#for i in range(22,32):  
#for i in range(32,42):  
#Doing P33 again since it didnt get uploaded to repo
#for i in range(33,34):  
#for i in range(42,53): 
#for i in range(52,53):
#for i in range(53,63): 
#for i in range(57,58):  
#for i in range(30,32):   
#for i in range(63,74):
#for i in range(64,65):  #i=64 gets row 65 P62
#for i in range(67,68): 
for i in range(74,85):   
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
  IngOrPub='P' #0 for ingest 1 for pub
  print("Row number on spreadsheet is " , i+1)
  logging.info("Row number on spreadsheet is %s " % str(i+1))
  HeadDir="F:\\"
  print("ingorpub",IngOrPub)

###EXCEPTIONS-------------------------------------------------------------------------------------
  if i==125:
    pDate[i]="20210201"

  ##Exception for corresponding author labelled with no LFI for pub bag P00005
  if i==5 and IngOrPub=='P':
    pCorrespondingAuthorLFI[i]="Beauchene"
    print("************************THE FOLLOWING PUBLICATION BAG HAS AN EXCEPTION***************************")
    print("Exception: The corresponding author appears as Beauchene instead of BeaucheneC in the bag name \n")
    print("To accomodate for this exception the corresponding author name is changed to Beauchene to fetch the bag but while making the bag on APTrust the corresponding author name: BeaucheneC is used")
    sheet1.write(i1,15,"Exception: The corresponding author appears as Beauchene instead of BeaucheneC in the bag name.To accomodate for this exception the corresponding author name is changed to Beauchene to fetch the bag but while making the bag on APTrust the corresponding author name: BeaucheneC is used")
    logging.info("************************THIS PUBLICATION BAG HAS AN EXCEPTION***************************")
    logging.info("Exception: The corresponding author appears as Beauchene instead of BeaucheneC in the bag name \n")
    logging.info("To accomodate this exception the corresponding author name is changed to Beauchene to fetch the bag made by UPACK \nWhen re-making the bag using DART the corresponding author is defaulted to BeaucheneC")    

  if i==32 and IngOrPub=='P':
    pCorrespondingAuthorLFI[i]="Bilici"
    print("************************THE FOLLOWING PUBLICATION BAG HAS AN EXCEPTION***************************")
    print("Exception: The corresponding author appears as Bilici instead of BiliciC in the bag name \n")
    print("To accomodate for this exception the corresponding author name is changed to Bilici to fetch the bag but while making the bag on APTrust the corresponding author name: BiliciC is used")
    sheet1.write(i1,15,"Exception: The corresponding author appears as Bilici instead of BiliciC in the bag name.To accomodate for this exception the corresponding author name is changed to Bilici to fetch the bag but while making the bag on APTrust the corresponding author name: BiliciC is used")
    logging.info("************************THIS PUBLICATION BAG HAS AN EXCEPTION***************************")
    logging.info("Exception: The corresponding author appears as Bilici instead of BiliciC in the bag name \n")
    logging.info("To accomodate this exception the corresponding author name is changed to Bilici to fetch the bag made by UPACK \nWhen re-making the bag using DART the corresponding author is defaulted to BiliciC")  

  if i==52 and IngOrPub=='P':
    print("************************THE FOLLOWING PUBLICATION BAG HAS AN EXCEPTION***************************")
    print("Exception: The version naming v02 does not appear in this bag \n")
    print("To accomodate for this exception the bag name without version in it is used to fetch the bag but while re-making the bag using DART version 'v02' is used in the bag name")
    sheet1.write(i1,15,"Exception: The version naming v02 does not appear in this bag.To accomodate for this exception the bag name without version in it is used to fetch the bag but while re-making the bag using DART version 'v02' is used in the bag name")
    logging.info("************************THIS PUBLICATION BAG HAS AN EXCEPTION***************************")
    logging.info("Exception: The version naming v02 does not appear in this bag")
    logging.info("To accomodate for this exception the bag name without version in it is used to fetch the bag but while re-making the bag using DART version 'v02' is used in the bag name")  
    
    print("**********NOW PROCESSING ",pPubAccessionNumber[i],"**********")
    logging.info("**************************NOW PROCESSING %s ****************" % pPubAccessionNumber[i])

  if i==57 and IngOrPub=='P':
    print("************************THE FOLLOWING PUBLICATION BAG HAS AN EXCEPTION***************************")
    print("Exception: P00055 is bagged but only the extracted bag exists on Google Drive. The tar version of the bag does not exist on either drives \n")
    print("To accomodate this the extracted bag was tarred using command line tar -czvf and bag was transferred to SanDisk and S3, bag is valid")
    sheet1.write(i1,15,"Exception: P00055 is bagged but only the extracted bag exists on Google Drive. The tar version of the bag does not exist on either drives")
    logging.info("************************THIS PUBLICATION BAG HAS AN EXCEPTION***************************")
    logging.info("Exception: P00055 is bagged but only the extracted bag exists on Google Drive. The tar version of the bag does not exist on either drives \n")
    logging.info("To accomodate for this the extracted bag was tarred using command line tar -czvf and bag was transferred to SanDisk and S3, bag is valid")
  

  if i==64 and IngOrPub=='P':
    print("************************THE FOLLOWING PUBLICATION BAG HAS A COMMENT***************************")
    print("Publication bag P00062 is bagged againg using publication date on Figshare: 20190530 \n")
    sheet1.write(i1,16,"Publication bag P00062 is bagged againg using publication date on Figshare 20190530")
    logging.info("************************THE FOLLOWING PUBLICATION BAG HAS A COMMENT***************************")
    logging.info("Publication bag P00062 is bagged againg using publication date on Figshare: 20190530")


  if i==67 and IngOrPub=='P':
    print("************************THE FOLLOWING PUBLICATION BAG HAS A COMMENT***************************")
    print("Publication bag P00064 is bagged againg using publication date on Figshare: 20190611  \n")
    sheet1.write(i1,16,"Publication bag P00064 is bagged againg using publication date on Figshare: 20190611 ")
    logging.info("************************THE FOLLOWING PUBLICATION BAG HAS A COMMENT***************************")
    logging.info("Publication bag P00064 is bagged againg using publication date on Figshare: 20190611")    

  if i==70 and IngOrPub=='P':
    print("************************THE FOLLOWING PUBLICATION BAG HAS AN EXCEPTION***************************")
    print("Exception: Bag has different versions on spreadsheet and bag name. P00067 is bagged with the version 02 but the version on spreadsheet is v01. To accomodate for this: Changing version on spreadsheet to v02 and using v02 on bag made by DART, since this bag was published before migration, its published article appears with an extension of V2 on figshare \n")
    sheet1.write(i1,15,"Exception: Bag has different versions on spreadsheet and bag name. P00067 is bagged with the version 02 but the version on spreadsheet is v01. To accomodate for this: Changing version on spreadsheet to v02 and using v02 on bag made by DART, since this bag was published before migration, its published article appears with an extension of V2 on figshare ")
    logging.info("************************THIS PUBLICATION BAG HAS AN EXCEPTION***************************")
    logging.info("Exception: Bag has different versions on spreadsheet and bag name. P00067 is bagged with the version 02 but the version on spreadsheet is v01. To accomodate for this: Changing version on spreadsheet to v02 and using v02 on bag made by DART, since this bag was published before migration, its published article appears with an extension of V2 on figshare ")    


#END OF EXCEPTION**********************************************************************************************

#Start processing I is for ingest, P is for publication bag:

  if IngOrPub=='I':
    SubDir3=f"{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}.tar"
    print("**********NOW PROCESSING ",iIngAccessionNumber[i],"**********")
    logging.info("**************************NOW PROCESSING %s ****************" % iIngAccessionNumber[i])

  #No exception/comment fetch:
  if IngOrPub=='P':
    SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}.tar"
  
 #Actions taken for exceptions/comments, overwrite parts of the bag naming:

  #P00050 version missing in bag name
  if IngOrPub=='P'and i == 52:
    SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_{pDate[i]}.tar"
  #Bag P00062 published date in bag name is not the same as that on figshare
  if IngOrPub=='P'and i == 64:
    SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_20190603.tar"  
  #Bag P00064 published date in bag name is not the same as that on figshare
  if IngOrPub=='P'and i == 67:
    SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_20190619.tar"
  
  print("**********NOW PROCESSING ",pPubAccessionNumber[i],"**********")
  logging.info("**************************NOW PROCESSING %s ****************" % pPubAccessionNumber[i])

#Check if bag exists in original format, if not then check if it exists without a v in the bag name:  
  SubDir3=SubDir3.strip()
  bagpath=os.path.join(HeadDir,SubDir3)
  print("SubDirm ",SubDir3)
  if not os.path.exists(bagpath):
    print("Bag in tar format does not exist: ", SubDir3)
    logging.info("Bag in tar format does not exist: %s " % SubDir3)
    if IngOrPub=='I':
      SubDir3=f"{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_{iVersion[i]}_{iDate[i]}.tar"
    if IngOrPub=='P':
      SubDir3=f"{pPubAccessionNumber[i]}_{pRequestorLFI[i]}_{pCorrespondingAuthorLFI[i]}_{pVersion[i]}_{pDate[i]}.tar"
    bagpath=os.path.join(HeadDir,SubDir3)
    print("Looking for Bag in tar format without v in version: ", SubDir3)
    logging.info("Looking for Bag in tar format without v in version: %s " % SubDir3)
    if not os.path.exists(bagpath):
      print("Bag in tar format does not exist without v in version either ",bagpath)
      logging.info("Bag in tar format does not exist without v in version either %s " % bagpath)
    else:
      print("Bag in tar format exists without v in version either ",bagpath)
      logging.info("Bag in tar format exists without v in version either %s " % bagpath)
      sheet1.write(i1,15,"Exception: Bag name is missing v in it, where v stands for version")

  print("Bagname with path is : ", bagpath)
  logging.info("Bagname with path is %s " % bagpath)

  #If bag exists, find the size of the bag, extract the bag and check for validation:
  
  if os.path.exists(bagpath):
    print("i1 is ",i1)
    count=count+1
    path1=bagpath#os.path.join( os.path.abspath(root1), filename1 )
    bag_size=os.path.getsize(path1)
    bag_size_gb=bag_size/(10**9)
    print("Bagname tar in S3 VTechbags is ",SubDir3,"\n") 
    sheet1.write(i1,0,SubDir3)
    print("Bagsize tar on S3 is: ",bag_size_gb)
    logging.info("Bagname in S3 VTechbags is  %s " % SubDir3)
    logging.info("BagSize on S3 is %s " % bag_size_gb)
    sheet1.write(i1,3,bag_size_gb)
    directory_path="F:\\"  
       
    #Extract/Untar bag on sandisk:
    mytar=tarfile.open(bagpath,"r")
    destpath='F:\\'
    mytar.extractall(destpath)
    mytar.close()
    extractedbag=SubDir3.replace('.tar','')
    print("Extracted bag ",extractedbag)
    logging.info(" Extracted bag on SanDisk is %s " % extractedbag)

    extractedbagpath=os.path.join(destpath,extractedbag)
    bag = bagit.Bag(extractedbagpath)

    #Check if bag is valid:    
    if bag.is_valid():
        print("Bag is valid")
        logging.info("Bag is valid %s " % extractedbag)
        sheet1.write(i1,2,"Bag is valid")
        #for ingest there is not additional 3rd path
        #source_folder=os.path.join(extractedbagpath,"data",extractedbag)
        source_folder=os.path.join(destpath, extractedbag,"data",extractedbag)
        print("payload is at : ",source_folder)
        payload=os.listdir(source_folder)



        ##Bagging with DART:        

        #Exception/Actions for Publication bags:  
        if extractedbag[0]=='P':
          #Bagging name conventions for Publication bags for APTrust transfer
          aptrustBagName=f"VTDR_{pPubAccessionNumber[i]}_{pIngAccessionNumber[i]}_DOI_{pDOIsuffix[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}"
          aptrustBagName_tar=f"{aptrustBagName}.tar"          
            ##Exception for corresponding author labelled with no LFI for pub bag P00005
          if i==5:
            pCorrespondingAuthorLFI[i]="BeaucheneC"
          if i==32:
            pCorrespondingAuthorLFI[i]="BiliciC"
           ## Accomodate for different dates found in Published sheet, bag name and figshare
          if i==64:
            pDate[i]='20190530'
          if i==67:
            pDate[i]="20190611"# for bag P0064
   
        #Bagging name conventions for Ingest bags for APTrust transfer:
        if extractedbag[0]=='I':
          aptrustBagName=f"VTDR_{iIngAccessionNumber[i]}_{iRequestorLFI[i]}_{iCorrespondingAuthorLFI[i]}_v{iVersion[i]}_{iDate[i]}"#f"VTDR_{extractedbag}"#this does not end with .tar
          aptrustBagName_tar=f"{aptrustBagName}.tar"
        print("APTrust bag name is ",aptrustBagName)
        print("APTrust bagname in tar format is ",aptrustBagName_tar)
        logging.info("APTrust bag name is %s " % aptrustBagName)   
        logging.info("APTrust bagname in tar format is %s " % aptrustBagName_tar)    
        sheet1.write(i1,1,aptrustBagName_tar)
      #-----------------------------------------------------------------------  
      #************CHANGE (5) Change for every 10 loop run***************************
        job = Job("APTrust Demo Workflow for Virginia Tech",aptrustBagName)
        #job = Job("APTrust Production Workflow for Virginia Tech",aptrustBagName)
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
        dartBagPath=os.path.join(dartpath,aptrustBagName_tar)
        dartBagSize=os.path.getsize(dartBagPath)
        dartBagSizeGB=dartBagSize/(10**9)
        sheet1.write(i1,4,dartBagSizeGB)
        #Extract/Untar bag made by DART:
        openDartTar=tarfile.open(dartBagPath,"r")
        destnpath="C:/Users/padma/.dart/bags/"
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


  #----------------Copy non disseminated content to a different location for Publication bag:-------------------------
  
        if extractedbag[0]=='P':
          destn_path="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/NonDisseminatedContent"
          data_directory=f"NonDisseminatedContent_VTDR_{pPubAccessionNumber[i]}_DOI_{pDOIsuffix[i]}_{pCorrespondingAuthorLFI[i]}_v{pVersion[i]}_{pDate[i]}"
          destndir=os.path.join(destn_path,data_directory)
          count=0
          sourcedir2=f"{dartextractedbag}/data/"
          for root, dirs, files in os.walk(sourcedir2):
            print("root is",root)
            logging.info("root is %s " % root)
            print("dir is", dirs)
            logging.info("dir is %s" % dirs)
            print("files are", files)
            logging.info("files are %s " % files)
            outer_dir=f"{dartextractedbag}/data/"
            #Skip copying content of Disseminated folder, accomodate for "disseminated" spelt differently
            random_names=os.listdir(outer_dir)
            inner_dirs = [
            os.path.join(outer_dir, name)
            for name in random_names
            if name[:2] == "Dis" or name[:3] =="Diss" or name[0] =="D" or name[0] == "i" or name[0] == "I"
            ]
            inner_dirs=" ".join(inner_dirs)
            print("\n\n")
            print("Inner Dissemination Directory starting with D or Diss or Dis or i or I is ", inner_dirs,"\n")
            logging.info("Inner Dissemination Directory starting with D or Diss or Dis or i or I is %s " % inner_dirs)

            if root==inner_dirs: 
              print("*********************SKIPPING COPYING CONTENTS OF THE DISSEMINATED FOLDER******************************** ")
              logging.info("*********************************SKIPPING COPYING CONTENTS OF THE DISSEMINATED FOLDER*********************************** ")
            else:
              for filename in files:
                print("***************************STARTING COPYING CONTENTS FOR FOLLOWING PATHS*************************")
                logging.info("***************************STARTING COPYING CONTENTS FOR FOLLOWING PATHS*************************")
                print("root is",root)
                logging.info("root is %s " % root)
                print("dir is", dirs)
                logging.info("dir is %s" % dirs)
                print("files are", files)
                logging.info("files are %s " % files)
                print("FILENAME is ",filename)
                logging.info("FILENAME is %s " % filename)
                print("absolute path? ",os.path.abspath(root))
                logging.info("absolute path? %s " % os.path.abspath(root))
                print("destination path? ", os.path.join(destndir,filename))
                logging.info("destination path? %s " % os.path.join(destndir,filename))
                oldpath=os.path.join(os.path.abspath(root),filename)
                newpath=os.path.join(destndir,filename)
                if not os.path.exists(destndir):
                  print("Following directory for copying contents other than disseminated does not exist so creating it and copying following file to it ",destndir, " file copying is ", filename)
                  logging.info("Following directory for copying contents other than disseminated does not exist so creating it and copying following file to it %s " % destndir)
                  logging.info(" file copying is %s " % filename)
                  os.mkdir(destndir)
                  shutil.copy(oldpath,newpath)
                elif not os.path.exists(newpath):
                  print("Directory is already created: ", destndir, " But following file does not exist in the directory so copying it to destn dir ",filename)
                  logging.info("Directory is already created: %s " % destndir)
                  logging.info( " But following file does not exist in the directory so copying it to destn dir %s " %filename)
                  shutil.copy(oldpath,newpath)
                else:
                  print("Directory is already created: ", destndir," file already exists so not copying ",filename)
                  logging.info("Directory is already created: %s " % destndir)
                  logging.info(" file already exists so not copying %s " % filename)
          
    else:
      print("Bag is not valid")
      logging.info("Bag is not valid")
      print("****************BAG VALIDATION FAILED FOR BAG ",extractedbagpath," SO BAG NOT MIGRATED to APTRUST****************")
      logging.info("****************BAG VALIDATION FAILED FOR BAG %s SO BAG NOT MIGRATED to APTRUST****************" % extractedbagpath)
  else:
      print("path not found ",bagpath)
      print("**************************BAG ", bagpath," NOT FOUND SO NOT MIGRATED TO APTRUST****************************")
      logging.info("path not found %s " % bagpath)
      logging.info("**************************BAG %s NOT FOUND SO NOT MIGRATED TO APTRUST****************************" % bagpath )
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

