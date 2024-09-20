import sys
import configparser
from generate_config_bulk import configurations
x=configurations("24328498","01")
config=configparser.ConfigParser()
config.read('configurations-bulk.ini')
curPath=config['IngestBag_PathSettings']['IngFolderPath']
print(curPath)#stop
sys.path.append(curPath)
sys.path.append(curPath+'/VTDR_RepositoryServices/Figshare-APTrust')
import aptCmd
from aptCmd import registryCheck
import Read_VTDR_Spreadsheet
from Read_VTDR_Spreadsheet import vtingsheet
#import packages and modules
import configparser
import os
import platform 

#import aptCmd
import shutil
import requests
import job
import figshareRetrieve
import figshareDownload
import json
import filecmp
import shutil
import os
#import aptCmdRegCheck
#-------------------------------
#------------import functions

from figshare import Figshare
from requests import HTTPError

from datetime import date
from datetime import datetime
from job import Job
from redata.commons.logger import log_stdout
#from aptCmdRegCheck import registryCheck
#import generate_config
from IngFolder_Download_TransferBagAPTrust_bulk import DownloadIngest
from PubFolder_Download_bulk import DownloadPub
from PubBagDART_TransferAPTrust_bulk import DownloadPubTrnsfr
#from generate_config import configurations
#----------------------

#Enter ingest articles:
#FigshareArticleID=["26860051","26781466","26086258","25267117","24749499","24328498"]

#------------------------------------

#Enter Publication articles:
#FigshareArticleID=["25196813","26364370","26227082","26397688","26401090","26487280"]
FigshareArticleID=["23646627","21818604","21538380"]#,"26397688","26401090","26487280"]
#--------------------------------

#Uncomment below: 
# If transferring ingest bags to aptrust, then uncomment 'Ing'
# If downloading publication data from figshare, then uncomment 'Pub'
# If transferring publication bags to aptrust, after VTCurationServicesActions folder is filled in(folder path already provided), then uncomment 'PubTransfer' 
#--------------------------------INPUT----------------------------------------------------------------------
while True:
  #try:
    IngOrPub=input("Please enter '1' for Ing transfer to APTrust or '2' for Pub transfer to APTrust: ")
    try:
        IngOrPub=int(IngOrPub)
      #break
    except ValueError:
        print("Oops! That was not a valid number. Try again")
        continue
    if 1 <= IngOrPub <= 2:
        break
    else:
        print("Please pick number 1 or 2")
IngOrPub=str(IngOrPub)
#-----------------------------------------------------------------------------------------------------------------

#IngOrPub=input("Enter Ing or Pub")
if IngOrPub=="1":
  DwnldContnt="Ing"
if IngOrPub=="2":
  DwnldContnt="Pub"
#DwnldContnt='Ing' #Pub Input 
#DwnldContnt='Pub' #Pub Input 
#DwnldContnt='PubTransfer' #Pub Input 
#----------------------------------------------
#print(DwnlodContnt)
#quit()
n=len(FigshareArticleID)
PubVerNum=["01" for x in range(n)] 
def workflowValue():
    while True:
  #try:
      workflow=input("Please enter '1' for deposit to APTrust Demo only, '2' for deposit to APTrust-Repo and VT libraries S3 bucket, '3' for deposit to VT libraries S3 bucket only, '4' for deposit to APTrust-Repo only:  ")
      try:
          workflow=int(workflow)
      #break
      except ValueError:
          print("Oops! That was not a valid number. Try again")
          continue
      if 1 <= workflow <= 4:
          break
      else:
          print("Please pick a workflow number between 1 and 4")
    workflowStr=str(workflow)
    return workflowStr
workflowVal=workflowValue()


for i in range(n) :
  print("STARTING CONFIGURATIONS")
  print(os.getcwd())
  x=configurations(FigshareArticleID[i],PubVerNum[i])

  if DwnldContnt=='Ing': 
    DwnldIngOrPubx=DownloadIngest(workflowVal)
  if DwnldContnt=='Pub': 
    DwnldIngOrPubx=DownloadPub()
    DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)
  #if DwnldContnt=='PubTransfer': 
  #  DwnldIngOrPubxTransfer=DownloadPubTrnsfr(workflowVal)

