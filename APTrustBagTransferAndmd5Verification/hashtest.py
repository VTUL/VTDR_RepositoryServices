# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:39:04 2022

@author: padma carstens
"""
"""
Purpose: 

- Compares md5 checksums listed in the 'manifest-md5' text files created by DART and UPACK for small bags (size>=5GB). For similar comparison of many bags (size <=5GB) over a loop please see md5Comparison_BagsOnS3SanDiskVsGoogleDrive.py
- The bag comparison here runs well for smaller sized bags, for large bags (size >= ~5GB), see hashtest_largefiles.py
- Returns "md5 verification passed" or "md5 verification failed" for the bags provided and creates a log file at the path provided in "LOG_FILENAME"

Parameters: 
LOG_FILENAME: path to where the log file is created
path1: path of the first bag in tar format
path2: path of the second bag in tar format
upack_manifestmd5: manifest-md5 text file providing the list of md5 checksums and their corresponding file names obtained from the bag created by running UPACK software. 
dart_manifestmd5: manifest-md5 text file providing the list of md5 checksums and their corresponding file names obtained from the bag created by running DART software.

"""

import hashlib
import os
import logging
from datetime import datetime
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')


path1="F:\P00092_MilesR_MilesR_v02_20220513.tar"
path2="G:\Shared drives\CurationServicesGoogleDriveArchive\BAGS\Completed_BAGS\P00092_v02-tarred\P00092_MilesR_MilesR_v02_20220513.tar"

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
# Open,close, read file and calculate MD5 on its contents 
with open(path1, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename is  %s " % path1)
    print("Filename is ",path1)
    data1 = file_to_check.read()    
    # pipe contents of the file through
    md5_returned1 = hashlib.md5(data1).hexdigest()
    logging.info("Its md5 is %s " % md5_returned1)
    print("Its md5 is ",md5_returned1,"\n")

with open(path2, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename is  %s " % path2)
    print("Filename is ",path2)
    data = file_to_check.read()    
    
    # pipe contents of the file through
    md5_returned = hashlib.md5(data).hexdigest()
    logging.info("Its md5 is %s " % md5_returned)
    print("Its md5 is ",md5_returned,"\n")

if md5_returned == md5_returned1:
    logging.info("md5 verification passed")
    print("md5 verification passed \n")
else:
    logging.info("md5 verification failed")
    print("md5 verification failed \n")
