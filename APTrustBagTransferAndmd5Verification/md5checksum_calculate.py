"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""
"""
Purpose:
Calculates and returns md5 chcksum of the bag in tar format with the path provided in 'path'
"""

from test_md5 import md5sum
import os
import logging
from datetime import datetime
from xlwt import Workbook
LOG_FILENAME=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/md5log_'+'%Y%m%d_%H%M.log')
sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/md5checksumSheet_'+'%Y%m%d_%H%M.xls')
wb=Workbook(sheetname)
sheet1=wb.add_sheet("checksums")#this name has a character limit
sheet1.write(0,0,'filename')
sheet1.write(0,1,'checksum')

#path='E:/VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_1of8_20210409/data'
#path='G:/Shared drives/Data Services TEAM DRIVE/DataManagementCurationServices/ALT_COMPLETED_BAGS/P00098_not_tarred/P00098_AsbeckA_AsbeckA_02(1of8)_20210521/P00098_AsbeckA_AsbeckA_02(1of8)_20210521/data'
#path='E:/VTDR_P00074_I00089_DOI_yhsb-t439_JosephL_v01_20191002/data'
#path='C:/Users/padma/anaconda3/envs/curation/VTDR_P00074_I00089_DOI_yhsb-t439_JosephL_v01_20191002/data'
path='C:/Users/padma/anaconda3/envs/curation/MissedGoogleDriveBags/I00221_JaberR_JaberR_v01_20220603/data'
#path='D://I00221_JaberR_JaberR_v01_20220603/data'
payload=os.listdir(path)
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
iCount=1
for root, dirs, files in os.walk(path):
    for filename in files:
        print("FILENAME is ",filename)
        abspath=os.path.join(os.path.abspath(root),filename)
        filewithpath=os.path.join(os.path.abspath(root),filename)
        md5_returned=md5sum(filewithpath).hexdigest()
        print("File's md5 checksum is ",md5_returned)
        sheet1.write(iCount,1,filename)
        sheet1.write(iCount,2,md5_returned)
        logging.info("filename is %s " % filename)
        logging.info("md5checksum is %s " % md5_returned)
        iCount += 1
        wb.save(sheetname)
