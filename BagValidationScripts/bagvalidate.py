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


i1=1

LOG_FILENAME=datetime.now().strftime('C:/Users/padma/anaconda3/envs/curation/validationlogfile_%H_%M_%d_%m_%Y.log')
import bagit

#bagstocheck=["I00180_BrownR_BrownR_v01_20211018","P00133_GutierrezC_AylwardF_v01_20210901","P00137_BalantrapuN_BalantrapuN_v01_20210923","P00155_NoahW_NoahW_v01_20211027","P00158_DeardenT_DeardenT_v01_20211130","P00159_BrooksM_BrooksM_v01_20211201","P00160_JantzenB_JantzenB_v01_20211210"]

#bagstocheck=["P00169_PetersonM_PetersonM_v01_20220228"]
#bagstocheck=["VTDR_P00154_I00180_DOI_14113193_BrownR_v01_20211022"]
#bagstocheck=["VTDR_I00227_SonamS_SonamS_v01_8of8_20220701"]
#bagstocheck=["VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_3of8_20210409"]
bagstocheck=['VTDR_P00074_I00089_DOI_yhsb-t439_JosephL_v01_20191002']
#bagstocheck=["VTDR_P00098_I00115_DOI_2v3w-sb92_AsbeckA_v02_20210409"]



#bagstocheck=["P00170_HaakD_HaakD_v01_20220302"]
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO, filemode='w')
#print("Validation for 3 random bags in S3: ")
print("Validation for ", bagstocheck)
#logging.info("Validation for 3 random bags in S3: ")
logging.info("Validation for ")
for x in bagstocheck:
  print("x is ",x)
  #path1="F://"+x
  #path1="F:/ErrorBagsFromAPTrust//"+x
  path1="E://"+x
  #path1="C:/Users/padma/anaconda3/envs/curation/invalidBagTestAptrustDownlds//"+x
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
  else:
    print("Bag is not valid")
    logging.info("Bag is not valid")

