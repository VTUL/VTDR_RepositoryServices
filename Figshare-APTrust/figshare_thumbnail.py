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
#swagger_client.configuration.access_token = token
import json
import requests
# create an instance of the API class
#api_instance = swagger_client.ArticlesApi()
article_id = 19738957#ArticleID # Long | Article unique identifier
version = 2 # Long | Article version identifier
#fileId = 35068654  
#{'properties': {'file_id': {'description': 'File ID','example': 35086231, 'format': 'int64','type': 'integer'}},'type': 'object','x-model': 'FileId','x-tag': 'articles'}


headers = {"Authorization": token}
url = 'https://api.figshare.com/v2'
#endpoint = '/account/articles/{}/versions/{}/update_thumb'.format(article_id, version)
endpoint = '/articles/{}/versions/{}/update_thumb'.format(article_id, version)
payload = {"file_id": 35086231}
request = requests.put(url+endpoint.format(article_id, version), data=json.dumps(payload), headers=headers)

#class file_ID:
#    fileid=35068654
#fid=file_ID()
#fileID=fid.fileid

#fileID=35068654
#fileID={'File': 35086231}
#38132628#https://data.lib.vt.edu/ndownloader/files/35068654#'#'https://data.lib.vt.edu/articles/dataset/Data_for_Hotspot_for_Building_Collapse_due_to_Land_Subsidence_in_the_Coastal_City_of_Lagos_West_Africa/19738957?file=35068654'#35068654#1742889 # FileId | File ID
#api_instance.article_version_update_thumb(articleId, versionId, fileID['File'])
#api_instance.article_version_update_thumb(articleId, versionId, fileID)
#try: 
#    # Update article version thumbnail
#    api_instance.article_version_update_thumb(articleId, versionId, #fileId)
#except ApiException as e:
#    print("Exception when calling #ArticlesApi->articleVersionUpdateThumb: %s\n" % e)



#token = 'token <article owner token>'

