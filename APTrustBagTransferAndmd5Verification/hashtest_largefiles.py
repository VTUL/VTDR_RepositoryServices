"""
Created on Wed Oct  6 12:39:04 2022

@author: padma carstens
"""
"""
Purpose: 

- Compares the md5 checksums of the bags made by UPACK and DART software in tar format for one bag with path provided for large files(size>=5GB). For similar comparison of many bags (size <=5GB) over a loop please see md5Comparison_BagsOnS3SanDiskVsGoogleDrive.py

- Creates a sheet in the path provided under 'sheetname' with filenames and md5 checksum list of the associated files and the comparison results

Parameters: 
sheetname: creates the provided sheetname at the specified path containing md5 checksum verification results of the 2 bags that are compared
sheet: add the sheet with the provided name
LOG_FILENAME: path to where the log file is created in text format, containing md5 checksum verification results of the 2 bags that are compared
filename_s3: filename of the bag in s3 in tar format
path1: path of the bag on s3
filename_gd: filename of the bag in google drive in tar format
path: path of the bag on google drive

"""
import hashlib
import os
import logging
from datetime import datetime
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')

import xlwt
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/MD5Comparison_P92V2_%Y%m%d_%H%M_.xls')
wb=Workbook(sheetname)
#wb = copy(rb)
sheet=wb.add_sheet("MD5ComparisonP92V2")

sheet.write(0, 0, 'Filename on S3')
sheet.write(0, 1, 'Filename on GoogleDrive')
sheet.write(0, 2, 'MD5 on S3')
sheet.write(0, 3, 'MD5 on GoogleDrive')
sheet.write(0, 4, 'MD5 Verification')
x=1#row number that will be written

filename_s3="P00092_MilesR_MilesR_v02_20220513.tar"
path1="F:\\"+filename_s3

filename_gd="P00092_MilesR_MilesR_v02_20220513.tar"
path="C:\\Users\\padma\\anaconda3\\envs\\curation\\P92v2checkmd5\\"+filename_gd
#filename=os.path.join(filedir,'\P00003-tarred')
#filepath=os.getcwd()+filename

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
# Open,close, read file and calculate MD5 on its contents 
hashgd = hashlib.md5()
with open(path, 'rb') as file_to_check:
    for chunk in iter(lambda: file_to_check.read(4096), ''):    
            hashgd.update(chunk)

    # read contents of the file
logging.info("Filename in google drive is  %s " % path)
print("Filename in google drive is ",path)
sheet.write(x,1,filename_gd)
#    data = file_to_check.read()    
    
    # pipe contents of the file through
#md5_returned = hashlib.md5(data).hexdigest()
md5_returned = hashgd.hexdigest()
logging.info("Its md5 is %s " % md5_returned)
print("Its md5 is ",md5_returned,"\n")
sheet.write(x,3,md5_returned)

with open(path1, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename in VTechbags on S3 is  %s " % path1)
    print("Filename in  VTechbags on S3 is ",path1)
    sheet.write(x,0,filename_s3)
    data1 = file_to_check.read()    
    # pipe contents of the file through
    md5_returned1 = hashlib.md5(data1).hexdigest()
    logging.info("Its md5 is %s " % md5_returned1)
    print("Its md5 is ",md5_returned1,"\n")
    sheet.write(x,2,md5_returned)
if md5_returned == md5_returned1:
    logging.info("MD5 Verification Passed")
    print("MD5 Verification Passed \n")
    sheet.write(x,2,"MD5 Verification Passed")
else:
    logging.info("MD5 Verification Failed")
    print("MD5 Verification Failed \n")
    sheet.write(x,2,"MD5 Verification Failed")
    
wb.save(sheetname)