"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""
"""
Purpose:
-Compares md5 checksums for the 2 copies of bags in tar format that were stored in S3 and google drive
-Prints out bag names, bag sizes, their md5 checksums and verification details in a log sheet stored in 'VTDR_CompletedBagChecking' on curation services google drive

Note: For file sizes greater than 10GB, if md5 checksum gives errors due to large size of the bag, error catching/exception handling is done, and the calculation repeats again catching the errors until the md5 checksum passes, this could take many hours for bags greater than 40GB

Parameters:
bagstartID: start of publication bag accession number for which the md5 verification is to be performed 

bagendID: end of publication bag accession number for which the md5 verification is to be performed 
LOG_FILENAME: provide the path where the log file is to be created
sourcedir1: path to the s3 bags copied to the sandisk F folder
sourcedir2: path to the google drive
"""
from cmath import log
import os
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

bagstartID="I203"
bagendID="I224"

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/md5VerificationBags_'+bagstartID+"_"+bagendID+'_%Y%m%d_%H%M_.xls')

wb=Workbook(sheetname)
#sheet = wb.add_sheet("MD5VerificationPubBags_"+bagstartID+"_"+bagendID)
sheet = wb.add_sheet("MD5VerBags_"+bagstartID+"_"+bagendID)
sheet.write(0, 0, 'Filename on S3')

sheet.write(0, 1, 'Filename on GoogleDrive')
sheet.write(0, 2, 'MD5 on S3')
sheet.write(0, 3, 'MD5 on GoogleDrive')
sheet.write(0, 4, 'MD5 Verification')
sheet.write(0,5,'File Size in GB')
i1=1
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_md5Verification_'+bagstartID+"_"+bagendID+'_%H_%M_%d_%m_%Y.log')
#sourcedir1="F:"
sourcedir1="D:"
#sourcedir2 ="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/Completed_BAGS"
sourcedir2="C:/Users/padma/anaconda3/envs/curation/MissedGoogleDriveBags"
ext=".tar"

def retry_on_ioerror(exc):
    return isinstance(exc, IOError)

@retry(retry_on_exception=retry_on_ioerror)
def calc_md5(fnamepath):
  with open(fnamepath, 'rb') as file_to_check:
    data=file_to_check.read()
    md5_fname=hashlib.md5(data).hexdigest()    
    return md5_fname

@retry(retry_on_exception=retry_on_ioerror)
def calc_md5_largefiles(fnamepath, blocksize=2**20):
    m = hashlib.md5()
    with open( fnamepath , "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()


count=0
for root1, dirs1, files1 in os.walk(sourcedir1):
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')

  for filename1 in files1:
    logging.info("Filename1 on sandisk is  %s " % filename1)
    print("Filename1 on sandisk is ",filename1,"\n")
    print("i1 is ",i1)
    #if filename1[0:3]=="P00":
    if filename1[0:3]=="I00":
      pubnostr=filename1[3:6]
      pubno=int(pubnostr)
    else:
      pubno=1  
      pubnostr="no"
    print("pubno is", pubno)
    logging.info("pubno is  %s " % pubno)
   # if filename1.endswith(ext) and pubno > 203 and pubno < 224 :
    if filename1.endswith(ext) :
    #if filename1.endswith(ext) and pubno == "175" :      
      count=count+1
      for root2, dirs2, files2 in os.walk(sourcedir2):
        for filename2 in files2:
          if re.match(filename1,filename2):
            path1=os.path.join( os.path.abspath(root1), filename1 )
            file_size=os.path.getsize(path1)
            file_size_gb=file_size/(10**9)
            #if file_size > (40*(10**9)):
            if file_size > 0:
            #if file_size > (1*(10**9)) and file_size <= (3*(10**9)):
              logging.info("Filename2 in Google Drive is  %s " % filename2)
              logging.info("File names match in both drives ")
              print("Filename2 in Google Drive is ",filename2,"\n")
              print("File names match in both drives ",filename1,"\n",filename2,"\n")
              print("i1 is ",i1)
              i1=i1+1
              sheet.write(i1,0,filename1)
              sheet.write(i1,1,filename2)
              print("File size is ",file_size_gb)
              sheet.write(i1,5,file_size_gb)
              path2=os.path.join( os.path.abspath(root2), filename2 )
            #  file_size=os.path.getsize(path1)
              print("File size is ",file_size_gb)
              logging.info("files less than 2GB, filename is: %s " % filename1)
              logging.info("file size is %s " % file_size_gb)
              #try:
              #with open(path1, 'rb') as file_to_check1:
              #  data1=file_to_check1.read()
              #  md5_returned1=hashlib.md5(data1).hexdigest()
              if file_size < (10*(10**9)):
               md5_returned1=calc_md5(path1)
               md5_returned2=calc_md5(path2)
              else:
                md5_returned1=calc_md5_largefiles(path1)
                md5_returned2=calc_md5_largefiles(path2)
              sheet.write(i1,2,md5_returned1)
              #hashs3=hashlib.md5()
              #md5_returned2=calc_md5(path2)
                #return md5_returned2
              #with open(path2, 'rb') as file_to_check2:
              #  data2=file_to_check2.read()
              #  md5_returned2=hashlib.md5(data2).hexdigest()
              sheet.write(i1,3,md5_returned2)
              #except Exception as e:
              #except OSError as err:
              #    print("OS error: ")
              #    continue#print(sys.exc_type)
              if md5_returned1 == md5_returned2:
                logging.info("Filename in VTechBag is  %s " % path1)
                logging.info("Its md5 is  %s " % md5_returned1)
                logging.info("Filename in google drive is  %s " % path2)
                logging.info("Its md5 is  %s " % md5_returned2)
                logging.info("MD5 verification passed  " )
                print("Filename in VTechBag is ",path1," with md5 ",md5_returned1,"\n")
                print("Filename in google drive is ",path2," with md5 ",md5_returned2,"\n")
                print("MD5 verification passed \n")
                sheet.write(i1,4,"Passed")
              else:
                logging.info("MD5 VERIFICATION FAILED FOR THE FOLLOWING FILES")
                logging.info("Filename in VTechBag is  %s " % path1)
                logging.info("Its md5 is  %s " % md5_returned1)
                logging.info("Filename in google drive is  %s " % path2)
                logging.info("Its md5 is  %s " % md5_returned2)
                print("MD5 VERIFICATION FAILED FOR FOLLOWING FILES \n")
                print("Filename in VTechBag is ",path1," with md5 ",md5_returned1,"\n")
                print("Filename in google drive is ",path2," with md5 ",md5_returned2,"\n")
                sheet.write(i1,4,"Failed")
         # else:
         #   logging.info("NO MATCHING FILE FOUND FOR THE FOLLOWING FILES:")
         #   logging.info("Filename in VTechBag is  %s " % path1)
           

      print("Counted files ",count,"\n")
      logging.info("Counted files %s " % count)
    i1=i1+1 
sheet.col(0).width = 15000
sheet.col(1).width = 15000
sheet.col(2).width = 15000
sheet.col(3).width = 15000
sheet.col(4).width = 15000
sheet.col(5).width = 15000
wb.save(sheetname)



