import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()
#------------------------------------------------------
# ADD SECTION for figshare settings
config_file.add_section("FigshareSettings")
# ADD SETTINGS TO SECTION
#config_file.set("FigshareSettings", "FigshareArticleID", "20376462")
#Published
config_file.set("FigshareSettings", "FigshareArticleID", "20371875")
config_file.set("FigshareSettings", "PublishedVersionNumber", "01")
config_file.set("FigshareSettings", "IngestVersionNumber", "01")
config_file.set("FigshareSettings", "token","1234")

#---------------------------------------------------------

#-------------------------------------------------------------
# ADD SECTION for AutomatedREADME settings:
config_file.add_section("AutomatedREADMEPathSettings")
config_file.set("AutomatedREADMEPathSettings","README_Dir", "C:/Users/padma/anaconda3/envs/curation/README_FILES")
#---------------------------------------------
#-------------------------------------------------------------
# ADD SECTION for AutomatedArchivalPackageREADME settings:
config_file.add_section("ArchivalREADMEPathSettings")
config_file.set("ArchivalREADMEPathSettings","ArchivalREADME_RootDir", "C:/Users/padma/anaconda3/envs/curation")

#-----------------------------------------------------------------
#-------------------------------------------------------------
#ADD SECTION for IngestBag_Download_TransferAPTrust script
config_file.add_section("IngestBag_PathSettings")
config_file.set("IngestBag_PathSettings","SanDiskDirPath","F:\\")
config_file.set("IngestBag_PathSettings","IngFolderPath","C:/Users/padma/anaconda3/envs/curation")
config_file.set("IngestBag_PathSettings","metadatajsonpath","C:/Users/padma/anaconda3/envs/curation")
#-------------------------------------------------------------
#----------------------------------------------------------------
#ADD SECTION for PubFolder_Download script
config_file.add_section("PubFolder_PathSettings")
config_file.set("PubFolder_PathSettings","PubFolderPath","C:/Users/padma/anaconda3/envs/curation")

#-----------------------------------------------------------------
#----------------------------------------------------------------
#ADD SECTION for PubBagDART_TransferAPTrust script
config_file.add_section("PubBagDartAptrust_PathSettings")
config_file.set("PubBagDartAptrust_PathSettings","LargeBagsPath","F:/VTechbags")
config_file.set("PubBagDartAptrust_PathSettings","NonDisseminatedContentPath","G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/NonDisseminatedContent/")
#-------------------------------------------------------------
#-----------------------------------------------------------------

with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

