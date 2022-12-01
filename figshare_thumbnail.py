#from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from Read_VTDR_Spreadsheet import vtingsheet
#Get the parameters from configurations.ini to retrieve information from an article on Figshare
import configparser
#config=configload.read_config()
config=configparser.ConfigParser()
config.read('configurations.ini')

#Get the ArticleID
ArticleID=config['FigshareSettings']['FigshareArticleID']
#Get the Published Version number 
PublishedVersionNumber=config['FigshareSettings']['PublishedVersionNumber']
#Remove "0" from the published version number 
intPublishedVersionNumber=int(PublishedVersionNumber[1])

#Get the Ingest Version number 
IngestVersionNumber=config['FigshareSettings']['IngestVersionNumber']
#Remove "0" from Ingest version number
intIngestVersionNumber=int(IngestVersionNumber[1])
#Get your figshare token 
token=config['FigshareSettings']['token']
#Get information from Ingest Sheet, access google spreadsheet 20211214_VTDR_PublishedDatasets_Log_V7 and get information about the article using article ID and version number.
ingsheet=vtingsheet(ArticleID,IngestVersionNumber)
# Configure OAuth2 access token for authorization: OAuth2
swagger_client.configuration.access_token = token

# create an instance of the API class
api_instance = swagger_client.ArticlesApi()
articleId = ArticleID # Long | Article unique identifier
versionId = 1 # Long | Article version identifier
fileId = 1742889 # FileId | File ID

try: 
    # Update article version thumbnail
    api_instance.article_version_update_thumb(articleId, versionId, fileId)
except ApiException as e:
    print("Exception when calling ArticlesApi->articleVersionUpdateThumb: %s\n" % e)