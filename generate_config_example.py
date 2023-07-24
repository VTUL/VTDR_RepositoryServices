import configparser
"""
Created on Wed Oct  6 12:39:04 2021

@author: padma carstens
"""

"""
Curator fills in the following parameters/paths: 

FigshareArticleID: This is the number found towards the end of the DOI link, click the red "Cite" button on the item under review/to be published 
PubVerNum: Publication Version Number to be downloaded, found at the end of "Cite"
VTDRToken: VTDR token created under applications
CurName: Name of the curator, this shows up in ArchivalReadme Package created in the publication folder
CurationDir: Curation directory where Ingest/Publication folder/README file will be created
NonDissContentDir: Directory where Non disseminated content will be stored, non disseminated content includes provenance log, email correspondence and archival readme package created in the publication folder
FileID: This is used only in the ChangeThumbnail.py script. File ID is the number at the end of the file link, this is the ID of the file that the curator wants to change the thumbnail of the published article to
"""
FigshareArticleID="21651401"
PubVerNum="01"
VTDRToken="1234"
CurName="XYZ"
CurationDir="C:/Users/username/anaconda3/envs/curation"
NonDissContentDir="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/NonDisseminatedContent/"
DartExePath="C:/Users/username/AppData/Local/Programs/DART/DART.exe"
ReadmeDir="C:/Users/username/anaconda3/envs/curation/README_FILES"
FileID="38878398"
#spreadsheetName="20211214_VTDR_PublishedDatasets_Log_V7"
spreadsheetName="20230721_VTDR_PublishedDatasets_Log_V8"

#------------------------------------------------------

# ADD SECTION for figshare settings
# CREATE OBJECTS
config_file = configparser.ConfigParser()
config_file.add_section("FigshareSettings")
config_file.set("FigshareSettings", "FigshareArticleID", FigshareArticleID)
config_file.set("FigshareSettings", "PublishedVersionNumber", PubVerNum)
config_file.set("FigshareSettings", "IngestVersionNumber", "01")
config_file.set("FigshareSettings", "token",VTDRToken)
config_file.set("FigshareSettings", "CuratorName",CurName)

#---------------------------------------------------------
# ADD SECTION for spreadsheet settings
config_file.add_section("SpreadsheetSettings")
config_file.set("SpreadsheetSettings","SpreadsheetName",spreadsheetName)

#---------------------------------------------------------

# ADD SECTION for AutomatedREADME settings:
config_file.add_section("AutomatedREADMEPathSettings")
config_file.set("AutomatedREADMEPathSettings","README_Dir", ReadmeDir)

#-------------------------------------------------------------

# ADD SECTION for AutomatedArchivalPackageREADME settings:
config_file.add_section("ArchivalREADMEPathSettings")
config_file.set("ArchivalREADMEPathSettings","ArchivalREADME_RootDir", CurationDir)

#-------------------------------------------------------------

#ADD SECTION for IngestBag_Download_TransferAPTrust script
config_file.add_section("IngestBag_PathSettings")
config_file.set("IngestBag_PathSettings","SanDiskDirPath","F:\\")
config_file.set("IngestBag_PathSettings","IngFolderPath",CurationDir)
config_file.set("IngestBag_PathSettings","metadatajsonpath",CurationDir)

#----------------------------------------------------------------

#ADD SECTION for PubFolder_Download script
config_file.add_section("PubFolder_PathSettings")
config_file.set("PubFolder_PathSettings","PubFolderPath",CurationDir)

#----------------------------------------------------------------

#ADD SECTION for PubBagDART_TransferAPTrust script
config_file.add_section("PubBagDartAptrust_PathSettings")
config_file.set("PubBagDartAptrust_PathSettings","LargeBagsPath","F:/VTechbags")
config_file.set("PubBagDartAptrust_PathSettings","NonDisseminatedContentPath",NonDissContentDir)

#-----------------------------------------------------------------

#ADD SECTION for job.py script
config_file.add_section("dart_PathSettings")
config_file.set("dart_PathSettings","dart_exe_path",DartExePath)

#---------------------------------------------------------------

with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()