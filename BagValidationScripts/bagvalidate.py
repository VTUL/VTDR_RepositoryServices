#this code was written by copy pasting how to make log files from md5drivecomp_xl_sheet2_largefiles_catcherror.py to check to see if the bag is valid which means comparing the md5 checksums of the payload and seeing if they match with manifest-md5.txt. this code was first tested using testvalid.py which was copy pasted from https://github.com/LibraryOfCongress/bagit-python

from cmath import log
from datetime import datetime
import logging


i1=1
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/validationlogfile_for_3randombags_in_s3_%H_%M_%d_%m_%Y.log')
#LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/validationlogfile_for_failedchecksums_in_googledrive_%H_%M_%d_%m_%Y.log')
LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/Log/validationlogfile_for_3randombags_in_googledrive_%H_%M_%d_%m_%Y.log')
import bagit

#bagstocheck=["I00180_BrownR_BrownR_v01_20211018","P00133_GutierrezC_AylwardF_v01_20210901","P00137_BalantrapuN_BalantrapuN_v01_20210923","P00155_NoahW_NoahW_v01_20211027","P00158_DeardenT_DeardenT_v01_20211130","P00159_BrooksM_BrooksM_v01_20211201","P00160_JantzenB_JantzenB_v01_20211210"]

#bagstocheck=["P00050_PorterN_PorterN_20181026","P00099_McCulloughC_McCulloughC_01_20200824","P00170_HaakD_HaakD_v01_20220302"]
bagstocheck=["P00169_PetersonM_PetersonM_v01_20220228"]

#bagstocheck=["P00170_HaakD_HaakD_v01_20220302"]
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
#print("Validation for 3 random bags in S3: ")
print("Validation for ", bagstocheck)
#logging.info("Validation for 3 random bags in S3: ")
logging.info("Validation for ")
for x in bagstocheck:
  print("x is ",x)
  path1="F://"+x
  print("path1 is ", path1)
  print("Bag name: ",x) 
  #path1="C:/Users/padma/anaconda3/envs/curation/s3_failedchecksumbags/"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/s3validate_bags/"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/gdrive_failedchecksumbags/"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/gdrivevalidate_bags/"+x
  #path1="F://"+x
  #print("Bag name: ",x)  
  logging.info("Bag name: %s " % x)
  bag = bagit.Bag(path1)
  if bag.is_valid():
    print("Bag is valid")
    logging.info("Bag is valid")
  else:
    print("Bag is not valid")
    logging.info("Bag is not valid")

