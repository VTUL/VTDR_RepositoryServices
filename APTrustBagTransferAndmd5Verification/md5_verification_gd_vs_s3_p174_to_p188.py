
from cmath import log
import os
import shutil #Used for copying files
import logging
from datetime import datetime
import re
import hashlib
import xlwt
from xlrd import open_workbook
from xlwt import Workbook
from xlutils.copy import copy
from test_md5 import md5sum

sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/MovingContentToAPTrust/MD5checksumComparisonBagsP174-P_%Y%m%d_%H%M_P174_P188.xls')
wb=Workbook(sheetname)

#______________________________
sheet2 = wb.add_sheet("MD5comparison_tarfiles_P174_to_P188")

sheet2.write(0, 0, 'Filename on S3')

sheet2.write(0, 1, 'Filename on GoogleDrive')
sheet2.write(0, 2, 'MD5 on S3')
sheet2.write(0, 3, 'MD5 on GoogleDrive')
sheet2.write(0, 4, 'MD5 Verification')
sheet2.write(0,5,'File Size in GB')
i1=1
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')

sourcedir1="F:/VTechbags"

sourcedir2 ="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/Completed_BAGS"

ext=".tar"

count=0
for root1, dirs1, files1 in os.walk(sourcedir1):
  logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')

  for filename1 in files1:
    logging.info("Filename1 in S3 VTechbags is  %s " % filename1)
    print("Filename1 is  in S3 VTechbags is ",filename1,"\n")
    print("i1 is ",i1)
    print("Getting the publication number from the bag name in tar format: ")
    pubnostr=filename1[3:6]
    pubno=int(pubnostr)

    if filename1.endswith(ext) and pubno > 173:
      count=count+1
      for root2, dirs2, files2 in os.walk(sourcedir2):
        for filename2 in files2:
          if re.match(filename1,filename2):
            path1=os.path.join( os.path.abspath(root1), filename1 )
            file_size=os.path.getsize(path1)
            file_size_gb=file_size/(10**9)
            print("File size is ",file_size_gb)
            sheet2.write(i1,5,file_size_gb)
            if file_size <= (1*(10**9)):
              logging.info("Filename2 in Google Drive is  %s " % filename2)
              logging.info("File names match in both drives ")
              print("Filename2 in Google Drive is ",filename2,"\n")
              print("File names match in both drives ",filename1,"\n",filename2,"\n")
              print("i1 is ",i1)
              i1=i1+1
              sheet2.write(i1,0,filename1)
              sheet2.write(i1,1,filename2)
              path2=os.path.join( os.path.abspath(root2), filename2 )
            #  file_size=os.path.getsize(path1)
              print("File size is ",file_size_gb)
              logging.info("files less than 2GB, filename is: %s " % filename1)
              logging.info("file size is %s " % file_size_gb)

              md5_returned1=md5sum(path1).hexdigest()
              #with open(path1, 'rb') as file_to_check1:
              #  data1=file_to_check1.read()
              #  md5_returned1=hashlib.md5(data1).hexdigest()
              sheet2.write(i1,2,md5_returned1)
              #hashs3=hashlib.md5()
              md5_returned2=md5sum(path2).hexdigest()
              #with open(path2, 'rb') as file_to_check2:
              #  data2=file_to_check2.read()
              #  md5_returned2=hashlib.md5(data2).hexdigest()
              sheet2.write(i1,3,md5_returned2)
              if md5_returned1 == md5_returned2:
                logging.info("Filename in VTechBag is  %s " % path1)
                logging.info("Its md5 is  %s " % md5_returned1)
                logging.info("Filename in google drive is  %s " % path2)
                logging.info("Its md5 is  %s " % md5_returned2)
                logging.info("MD5 verification passed  " )
                print("Filename in VTechBag is ",path1," with md5 ",md5_returned1,"\n")
                print("Filename in google drive is ",path2," with md5 ",md5_returned2,"\n")
                print("MD5 verification passed \n")
                sheet2.write(i1,4,"Passed")
              else:
                logging.info("MD5 VERIFICATION FAILED FOR THE FOLLOWING FILES")
                logging.info("Filename in VTechBag is  %s " % path1)
                logging.info("Its md5 is  %s " % md5_returned1)
                logging.info("Filename in google drive is  %s " % path2)
                logging.info("Its md5 is  %s " % md5_returned2)
                print("MD5 VERIFICATION FAILED FOR FOLLOWING FILES \n")
                print("Filename in VTechBag is ",path1," with md5 ",md5_returned1,"\n")
                print("Filename in google drive is ",path2," with md5 ",md5_returned2,"\n")
                sheet2.write(i1,4,"Failed")
         # else:
         #   logging.info("NO MATCHING FILE FOUND FOR THE FOLLOWING FILES:")
         #   logging.info("Filename in VTechBag is  %s " % path1)
           

      print("Counted files ",count,"\n")
      logging.info("Counted files %s " % count)
    i1=i1+1 
sheet2.col(0).width = 15000
sheet2.col(1).width = 15000
sheet2.col(2).width = 15000
sheet2.col(3).width = 15000
sheet2.col(4).width = 15000
sheet2.col(5).width = 15000
wb.save("Comparison_md5checksum_tarfiles_gdrive_vs_s3.xls")



