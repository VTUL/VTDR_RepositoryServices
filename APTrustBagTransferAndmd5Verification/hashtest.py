#This code was written before "md5drivecomp_xl.py", this code compares tar files in two different directories and does md5 checksum comparison. This code was copy pasted and modified to "md5drivecomp_xl.py". This code is now being copy pasted to run for the 15 large GB files as "hashtest_largefiles.py" to open a new sheet on xl and keep adding the md5 checksums for the large files if md5....largefiles.py doesnt work

import hashlib
import os
import logging
from datetime import datetime
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/logfile_%H_%M_%d_%m_%Y.log')

#filename='C:/Users/padma/anaconda3/envs/curation/I00XYZ-tarred/I00XYZ_TestE_TestE_v01_20220103.tar'

#filename='\I00XYZ-tarred\I00XYZ_TestE_TestE_v01_20220103.tar'
#path="D:\\VTechbags\\P00003-tarred\\I00001_HallR_v01_20160405.tar"
#path1="G:\\Shared drives\\CurationServicesGoogleDriveArchive\\BAGS\\Completed_BAGS\\P00003_bagged\\P00003-tarred\\I00001_HallR_v01_20160405.tar"
path1="F:\P00092_MilesR_MilesR_v02_20220513.tar"
path="G:\Shared drives\CurationServicesGoogleDriveArchive\BAGS\Completed_BAGS\P00092_v02-tarred\P00092_MilesR_MilesR_v02_20220513.tar"
#filename=os.path.join(filedir,'\P00003-tarred')
#filepath=os.getcwd()+filename
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
# Open,close, read file and calculate MD5 on its contents 
with open(path, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename in google drive is  %s " % path)
    print("Filename in google drive is ",path)
    data = file_to_check.read()    
    
    # pipe contents of the file through
    md5_returned = hashlib.md5(data).hexdigest()
    logging.info("Its md5 is %s " % md5_returned)
    print("Its md5 is ",md5_returned,"\n")


with open(path1, 'rb') as file_to_check:
    # read contents of the file
    logging.info("Filename in VTechbags on S3 is  %s " % path1)
    print("Filename in  VTechbags on S3 is ",path1)
    data1 = file_to_check.read()    
    # pipe contents of the file through
    md5_returned1 = hashlib.md5(data1).hexdigest()
    logging.info("Its md5 is %s " % md5_returned1)
    print("Its md5 is ",md5_returned1,"\n")

if md5_returned == md5_returned1:
    #print("Filename in VTechBag is ",path," with md5 ",md5_returned,"\n")
    #print("Filename in google drive is ",path1," with md5 ",md5_returned1,"\n")
    logging.info("md5 Verification Passed")
    print("MD5 verification passed \n")
else:
    logging.info("md5 VERIFICATION FAILED")
    print("MD5 vVERIFICATION FAILED \n")
    #print("Filename in VTechBag is ",path," with md5 ",md5_returned,"\n")
    #print("Filename in google drive is ",path1," with md5 ",md5_returned1,"\n")
    