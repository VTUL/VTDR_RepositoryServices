#!/usr/bin/env python
'''
AutomatedProvenanceLog_batch.py
Created on   2024/10/01 12:10:20
@author  :   padma carstens 
@contact :   padma@vt.edu
@license :   MIT License
'''
"""
Purpose: 
Creates a provenance log in rtf format at the path provided, inserting a varying date string for batch upload of publication folders to aptrust. Called to automate provenance log creation for batch publication folder download/transfer by PubBagDART_TransferAPTrust_batch.py 
Input: 
PubFolderVTCSApath: Path where provenance log needs to be created
InsString: String that needs to be inserted, changes with the date/time of ingestion
Output: ProvenanceLog.rtf created at the path provided
"""
from datetime import datetime
def create_provlog(PubFolderVTCSApath,CuratorName):
    filename=PubFolderVTCSApath+"/ProvenanceLog.rtf"
  # Get today's date
    today = datetime.today()
  # Format the date as YYYY MM DD
    formatted_date = today.strftime("%Y%m%d")
    InsertString=str(formatted_date)+"\\tab "+str(CuratorName)+"\\tab Curator ingested the item, created a README using our scripts, attached the README to the dataset, and published the dataset."
    print("Inserting String: ",InsertString,' in the Provenance Log.')
    f = open(filename,'w',encoding="utf-8")
    f.write("{\\rtf1\\ansi {\\b Date\\tab Curator\\tab Action} "+"\\line\n"+
            "20240613\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240627\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240628-20240809\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240820\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240822\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240823\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            "20240909\\tab [Insert Curator]\\tab [Insert Action]"+"\\line\n"+
            InsertString+"\\line\n"+
            "}")
    f.close()

#test:
#create_provlog("C:/Users/padma/anaconda3/envs/curation","padma")