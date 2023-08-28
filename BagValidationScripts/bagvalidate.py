"""
Created on Tue Sep 28 09:41:18 2021

@author: padma carstens
"""
"""
Purpose: 

-Validates bag/bags provided as a list, creates a log file with the validation details, note that this code was copied originally from https://github.com/LibraryOfCongress/bagit-python before modifications were made

Parameters:

LOG_FILENAME: provide the path for the log file
bagstocheck: bags that need validation

path1: path of the bag that needs verification
"""
from cmath import log
from datetime import datetime
import logging
import os
import shutil #Used for copying files
import logging
from datetime import datetime
import sys
sys.path.append('Figshare-APTrust')
import bagit
import xlwt
from xlwt import Workbook

i1=1

LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/validationlogfile_%H_%M_%d_%m_%Y.log')
import bagit
#sheetname=datetime.now().strftime('G:/Shared drives/CurationServicesGoogleDriveArchive/Administration/DownloadingBagsFromAPTrust/finalAptrustBagValidationForAllBags_'+'%Y%m%d_%H%M.xls')

sheetname=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/bagvalidation_'+'%Y%m%d_%H%M.xls')

wb=Workbook(sheetname)
#bagstocheck=["I00180_BrownR_BrownR_v01_20211018","P00133_GutierrezC_AylwardF_v01_20210901","P00137_BalantrapuN_BalantrapuN_v01_20210923","P00155_NoahW_NoahW_v01_20211027","P00158_DeardenT_DeardenT_v01_20211130","P00159_BrooksM_BrooksM_v01_20211201","P00160_JantzenB_JantzenB_v01_20211210"]
sheet1=wb.add_sheet("aptrustDownldedBagValidn")#this name has a character limit
sheet1.write(0,0,'aptrustRestoreBagName')
sheet1.write(0,1,'bagSize in GB')
sheet1.write(0,2, 'ExtractedBagName')
sheet1.write(0,3,'BagValidationTest')

#bagstocheck=["P00169_PetersonM_PetersonM_v01_20220228"]
#bagstocheck=["VTDR_P00154_I00180_DOI_14113193_BrownR_v01_20211022"]
#bagstocheck=["VTDR_I00227_SonamS_SonamS_v01_8of8_20220701"]
#bagstocheck=["VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_3of8_20210409"]
#bagstocheck=['VTDR_P00074_I00089_DOI_yhsb-t439_JosephL_v01_20191002']
#bagstocheck=["VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_20210409"]
#bagstocheck=["VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_20210409"]
#bagstocheck=["I00221_JaberR_JaberR_v01_20220603"]
bagstocheck=["VTDR_P00179_I00209_DOI_19709143_EmoriS_v01_20220509"]
#rootfolder="E://"
#rootfolder="D://"
rootfolder="C:/Users/padma/anaconda3/envs/curation/"
bagNameWithTar=rootfolder+bagstocheck[0]+".tar"

sheet1.write(1,0,bagNameWithTar)
sheet1.write(1,2,bagNameWithTar)
bagsize=os.path.getsize(bagNameWithTar)
bagsizeGB=bagsize/(10**9)
sheet1.write(1,1,bagsizeGB)

#bagstocheck=["P00170_HaakD_HaakD_v01_20220302"]
bagstocheck=["VTDR_P00179_I00209_DOI_19709143_EmoriS_v01_20220509"]
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
#print("Validation for 3 random bags in S3: ")
print("Validation for ", bagstocheck)
#logging.info("Validation for 3 random bags in S3: ")
logging.info("Validation for ")
for x in bagstocheck:
  print("x is ",x)
  #path1="F://"+x
  #path1="F:/ErrorBagsFromAPTrust//"+x
  path1=rootfolder+x
  #path1="D:/P98New//"+x
  #path1="C:/Users/padma/anaconda3/envs/curation//"+x
  #print("path1 is ", path1)
  print("Bag name: ",x) 

  #path1="C:/Users/padma/anaconda3/envs/curation/s3_failedchecksumbags/"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/s3validate_bags/"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/gdrive_failedchecksumbags/"+x
  logging.info("Bag name: %s " % x)
  bag = bagit.Bag(path1)
  if bag.is_valid():
    print("Bag is valid")
    logging.info("Bag is valid")
    sheet1.write(1,3,"Bag is valid")
  else:
    print("Bag is not valid")
    logging.info("Bag is not valid")
    sheet1.write(1,3,"Bag is not valid")
wb.save(sheetname)

