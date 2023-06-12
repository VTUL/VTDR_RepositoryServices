"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""
"""
Purpose: 
- test and print folder/file structure
"""
import os
import shutil #Used for copying files
import logging
from datetime import datetime
import sys
sys.path.append('Figshare-APTrust')
import bagit
from xlwt import Workbook
sourcedir = "E:\\"
ext=".tar"
iBagNo=1
LOG_FILENAME=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/folderfilestructurelog_'+'%Y%m%d_%H%M.log')
for root, dirs, files in os.walk(sourcedir):
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')

#,style='{',filename='%slog' % __file__[:2],
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
    iBagNo+=1