#from __future__ import print_statement
import time
import swagger_client
#from swagger_client.rest import ApiException
#from pprint import pprint
from Read_VTDR_Spreadsheet import vtingsheet
#Get the parameters from configurations.ini to retrieve information from an article on Figshare
import configparser
from Read_VTDR_Spreadsheet import vtpubsheet

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

vtsheet=vtpubsheet(ArticleID,PublishedVersionNumber)

import json
import requests
# create an instance of the API class

article_id = ArticleID#ArticleID # Long | Article unique identifier
version = 1.1 # Long | Article version identifier

headers = {"Authorization": token}
url = 'https://api.figshare.com/v2'

endpoint = 'account/articles/{}/versions/{}/update_thumb'.format(article_id, version)
payload = {"file_id": 38868420}
#file_id=38843163
request = requests.put(url+endpoint.format(article_id, version), data=json.dumps(payload), headers=headers)


