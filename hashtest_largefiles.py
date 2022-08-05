#This code was copy pasted from hashtest.py to run for the 15 large GB files as "hashtest_largefiles.py" to open a new sheet on xl and keep adding the md5 checksums for the large files if md5....largefiles.py doesnt work, to do the same but one large tar file at a time 

import hashlib
import os
import logging
from datetime import datetime
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')

import xlwt
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
#rb = open_workbook("C:/Users/padma/anaconda3/envs/curation/Comparison_md5checksum_tarfiles_gdrive_vs_s3.xls")
sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/MD5Comparison_P92V2_%Y%m%d_%H%M_.xls')
wb=Workbook(sheetname)
#wb = copy(rb)
sheet3=wb.add_sheet("MD5ComparisonP92V2")
#sheet3 = wb.get_sheet("MD5comparison one at a tim>10GB")

#sheet1 = book.get_sheet_by_name(name='Sheet2')# 1st number is the row number, 2nd number "0" is the column number
#sheet1 = book.get_sheet(1)# 1st number is the row number, 2nd number "0" is the column number
sheet3.write(0, 0, 'Filename on S3')
sheet3.write(0, 1, 'Filename on GoogleDrive')
sheet3.write(0, 2, 'MD5 on S3')
sheet3.write(0, 3, 'MD5 on GoogleDrive')
sheet3.write(0, 4, 'MD5 Verification')
x=1#row number that will be written
#filename='C:/Users/padma/anaconda3/envs/curation/I00XYZ-tarred/I00XYZ_TestE_TestE_v01_20220103.tar'

#filename='\I00XYZ-tarred\I00XYZ_TestE_TestE_v01_20220103.tar'
#path="D:\\VTechbags\\P00003-tarred\\I00001_HallR_v01_20160405.tar"
#path1="G:\\Shared drives\\CurationServicesGoogleDriveArchive\\BAGS\\Completed_BAGS\\P00003_bagged\\P00003-tarred\\I00001_HallR_v01_20160405.tar"
#path1="D:\VTechbags\P00068-tarred\\I00083_WinlingL_WinlingL_v01_20190822.tar"
#filename_s3="P00104_ForuhandehM_ForuhandehM_v01_20200921.tar"
#path1="F:\VTechbags\\"+filename_s3
filename_s3="P00092_MilesR_MilesR_v02_20220513.tar"
path1="F:\\"+filename_s3


#path1="D:\VTechbags\P00068-tarred\\I00083_WinlingL_WinlingL_v01_20190822.tar"
#path="G:\Shared drives\CurationServicesGoogleDriveArchive\BAGS\Completed_BAGS\P00068_bagged\P00068-tarred\I00083_WinlingL_WinlingL_v01_20190822.tar"
#filename_gd="P00104_ForuhandehM_ForuhandehM_v01_20200921.tar"
#path="E:\googledrivebags\\"+filename_gd
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
sheet3.write(x,1,filename_gd)
#    data = file_to_check.read()    
    
    # pipe contents of the file through
#md5_returned = hashlib.md5(data).hexdigest()
md5_returned = hashgd.hexdigest()
logging.info("Its md5 is %s " % md5_returned)
print("Its md5 is ",md5_returned,"\n")
sheet3.write(x,3,md5_returned)

with open(path1, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename in VTechbags on S3 is  %s " % path1)
    print("Filename in  VTechbags on S3 is ",path1)
    sheet3.write(x,0,filename_s3)
    data1 = file_to_check.read()    
    # pipe contents of the file through
    md5_returned1 = hashlib.md5(data1).hexdigest()
    logging.info("Its md5 is %s " % md5_returned1)
    print("Its md5 is ",md5_returned1,"\n")
    sheet3.write(x,2,md5_returned)
if md5_returned == md5_returned1:
    #print("Filename in VTechBag is ",path," with md5 ",md5_returned,"\n")
    #print("Filename in google drive is ",path1," with md5 ",md5_returned1,"\n")
    logging.info("MD5 Verification Passed")
    print("MD5 Verification Passed \n")
    sheet3.write(x,2,"MD5 Verification Passed")
else:
    logging.info("MD5 Verification Failed")
    print("MD5 Verification Failed \n")
    sheet3.write(x,2,"MD5 Verification Failed")
    #print("Filename in VTechBag is ",path," with md5 ",md5_returned,"\n")
    #print("Filename in google drive is ",path1," with md5 ",md5_returned1,"\n")
    
wb.save(sheetname)