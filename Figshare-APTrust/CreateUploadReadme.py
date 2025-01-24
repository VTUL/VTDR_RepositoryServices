"""
Purpose:
- Create readme file is created and and upload it to the users account
- Article ID, token and README path are taken from configurations.ini
-Code is taken from https://docs.figshare.com/old_docs/api/upload_example/
- Code only uses AutomatedREADMErtf_batch.py to create the README file and uploads it to the user's account using figshareUploadFile
"""
##########Create the README file for the article in review and upload it to the user/client's account
#Get the parameters from configurations.ini to retrieve information from an article on Figshare
from AutomatedREADMErtf_batch import create_readme_batch
from Read_VTDR_Spreadsheet import vtingsheet
from figshareUploadFile import initiate_new_upload,complete_upload,upload_parts
import configparser 
config=configparser.ConfigParser()
config.read('configurations.ini')
#Get the ArticleID
FigshareArticleID=config['FigshareSettings']['FigshareArticleID']    
#Get your figshare token 
token=config['FigshareSettings']['token']
#Get the README path
READMEPath=config['AutomatedREADMEPathSettings']['README_Dir']
#Create the README file
readmefile=create_readme_batch(FigshareArticleID,token,READMEPath)
##########Upload README file to figshare article in review:
FILE_PATH=readmefile
file_info=initiate_new_upload(FigshareArticleID,FILE_PATH)
print('*****************FigshareArticleID is ************************',FigshareArticleID)
# use the figshare upload service API to upload file:
upload_parts(file_info,FILE_PATH)
# use figshare api to complete process:
complete_upload(FigshareArticleID, file_info['id'])
######################