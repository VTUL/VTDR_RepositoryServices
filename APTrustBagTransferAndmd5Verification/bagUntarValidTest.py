"""
Created on Tue April 28 09:41:18 2023

@author: padma carstens
"""
"""
Purpose: 
-Untar ingest and publication bags in tar format in the sandisk copied from aptrust
-Performs bag validation on the bag 
-Creates a sheet/log file for extracted bags and prints out bag validation result. Log files saved n 'MovingContentToAPTrust' folder in curation services google drive archive.
"""
import os
import shutil #Used for copying files
import logging
from datetime import datetime
import sys
sys.path.append('Figshare-APTrust')
import bagit
from xlwt import Workbook
#-----------------------------------------------------------------
import tarfile

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/finalAptrustBagValidationForAllBags_'+'%Y%m%d_%H%M.xls')
LOG_FILENAME=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/finalAptrustBagValidationForAllBags_'+'%Y%m%d_%H%M.log')
wb=Workbook(sheetname)
sheet1=wb.add_sheet("aptrustDownldedBagValidn")#this name has a character limit
sheet1.write(0,0,'aptrustRestoreBagName')
sheet1.write(0,1,'bagSize in GB')
sheet1.write(0,2, 'ExtractedBagName')
sheet1.write(0,3,'BagValidationTest')
#sourcedir = "C:/Users/padma/anaconda3/envs/curation/invalidBagTestAptrustDownlds"
sourcedir="E:"
ext=".tar"
iBagNo=1
for root, dirs, files in os.walk(sourcedir):
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
  logging.info("root is %s " % root)
  logging.info("dir is %s " %  dirs)
  logging.info("files are %s " %  files)
  #logging.info ("\n")
  print("root is",root,"\n")
  print("dir is", dirs,"\n")
  print("files are", files,"\n")
  print ("\n")
  iBagNo=1
  for bagName in files:
    logging.info("bagName is  %s " % bagName)
    print("bagName is ",bagName,"\n")
    sheet1.write(iBagNo,0,bagName)
    if (bagName.endswith(ext)) and iBagNo > 271: 
      logging.info("BagName that ends with .tar is  %s " % bagName)
      print("BagName that ends with .tar is ",bagName,"\n")
      bagNameNoTar=os.path.splitext(bagName)[0]
      print("bagname with no tar extension is ",bagNameNoTar)
      bagWithPathTarext=os.path.join(sourcedir,bagName)
      bagWithPathNoTarext=os.path.join(sourcedir,bagNameNoTar)
      print("bag path with tar ext ",bagWithPathTarext)
      print("Bag path with no tar ext ",bagWithPathNoTarext)
      bag_size=os.path.getsize(bagWithPathTarext)
      bag_size_gb=bag_size/(10**9)
      print("bag size in gb is ",bag_size_gb)
      logging.info("BagSize in GB is  %s " % bag_size_gb)
      sheet1.write(iBagNo,1,bag_size_gb)
      extractedBag= tarfile.open(bagWithPathTarext,"r")
      print("extracted bag is ",extractedBag)
      print("sourcedir ",sourcedir)
      extractedBag.extractall(sourcedir)
      extractedBag.close()
      print("extracted bag is ",extractedBag)
      extractedBagNoTar=bagNameNoTar
      print("Extracted bag ",extractedBagNoTar)
      logging.info(" Extracted bag on SanDisk is %s " % extractedBagNoTar)
      sheet1.write(iBagNo,2,extractedBagNoTar)
          #Check if bag is valid:    
      bag=bagit.Bag(bagWithPathNoTarext)    
      if bag.is_valid():
        print("Bag is valid")
        logging.info("Bag is valid %s " % extractedBagNoTar )
        sheet1.write(iBagNo,3,"Bag is valid")
      else:
        print("Bag is not valid")
        logging.info("Bag is not valid")
        sheet1.write(iBagNo,3,"Bag is not valid")
        print("****************BAG VALIDATION FAILED FOR BAG ",extractedBagNoTar)
        logging.info("****************BAG VALIDATION FAILED FOR BAG %s " % extractedBagNoTar)
    print('iBagNo is ',iBagNo)
    logging.info("BagNo is %s " % iBagNo)
    iBagNo += 1
    wb.save(sheetname)


          


