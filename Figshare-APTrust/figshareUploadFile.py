#Following codes use figshare api and figshare upload service api taken from figshare api documentation: https://docs.figshare.com/old_docs/api/upload_example/ and modified for VTUL figshare upload purposes. 
# Note: If the same file is uploaded to figshare account twice, it appears twice in the item and is not overwritten
#Purpose: Upload a file to VTUL figshare
#Input: article id, token and file name

import sys
import configparser
#import generate_config_batch
from generate_config_batch import configurations
sys.path.append('curation')
import os
import requests
import json
import os
from requests import HTTPError
import hashlib
import json
CHUNK_SIZE = 1048576
BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
config=configparser.ConfigParser()
config.read('configurations-batch.ini')
#Get your figshare token, only using batch.ini for token, not the article id, so it doesn't matter if its reading this token from configurations.ini or configurations-batch.ini
TOKEN=config['FigshareSettings']['token']


def raw_issue_request(method, url, data=None, binary=False):
    headers = {'Authorization': 'token ' + TOKEN}
    if data is not None and not binary:
        data = json.dumps(data)
    response = requests.request(method, url, headers=headers, data=data)
    try:
        response.raise_for_status()
        try:
            data = json.loads(response.content)
        except ValueError:
            data = response.content
    except HTTPError as error:
        print('Caught an HTTPError: {}'.format(error.message))
        print('Body:\n', response.content)
        raise

    return data
def get_file_check_data(file_name):
    print("FILENAME IS ",file_name)
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(CHUNK_SIZE)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(CHUNK_SIZE)
        return md5.hexdigest(), size
def issue_request(method, endpoint, *args, **kwargs):
    return raw_issue_request(method, BASE_URL.format(endpoint=endpoint), *args, **kwargs)

def initiate_new_upload(article_id, file_name):
    endpoint = 'account/articles/{}/files'
    endpoint = endpoint.format(article_id)

    md5, size = get_file_check_data(file_name)
    data = {'name': os.path.basename(file_name),
            'md5': md5,
            'size': size}

    result = issue_request('POST', endpoint, data=data)
   # print 'Initiated file upload:', result['location'], '\n'

    result = raw_issue_request('GET', result['location'])

    return result

def complete_upload(article_id, file_id):
    issue_request('POST', 'account/articles/{}/files/{}'.format(article_id, file_id))


def upload_parts(file_info,FILE_PATH):
    url = '{upload_url}'.format(**file_info)
    result = raw_issue_request('GET', url)

    print('Uploading parts:')
    with open(FILE_PATH, 'rb') as fin:
        for part in result['parts']:
            upload_part(file_info, fin, part)
   # print
def upload_part(file_info, stream, part):
    udata = file_info.copy()
    udata.update(part)
    url = '{upload_url}/{partNo}'.format(**udata)

    stream.seek(part['startOffset'])
    data = stream.read(part['endOffset'] - part['startOffset'] + 1)

    raw_issue_request('PUT', url, data=data, binary=True)
    print ('  Uploaded part {partNo} from {startOffset} to {endOffset}'.format(**part))

#def main():
  #  # We first create the article
  # # Note that this part uploads article to figshare account, see figshareUpload.py where this was tested in the Padma's account

  #  list_articles()
  #  article_id = create_article(TITLE)
  #  list_articles()
  #  list_files_of_article(article_id)

 #   # Then we upload the file.
 #   file_info = initiate_new_upload(article_id, FILE_PATH)
 #   # Until here we used the figshare API; following lines use the figshare upload service API.
 #   upload_parts(file_info)
 #   # We return to the figshare API to complete the file upload process.
 #   complete_upload(article_id, file_info['id'])
 #   list_files_of_article(article_id)


#if __name__ == '__main__':
#    main()

##test:
#config=configparser.ConfigParser()
#config.read('configurations-batch.ini')
##Get your figshare token 
##token=config['FigshareSettings']['token']
#TOKEN=config['FigshareSettings']['token']
#PubFolderPath=config['PubFolder_PathSettings']['PubFolderPath'] 
##from AutomatedREADMErtf import create_readme
#FigshareArticleID="24328498"
#FILE_PATH=PubFolderPath+"/"+"README.rtf"
##file_info=initiate_new_upload(FigshareArticleID,PubFolderPath+"/"+"README.rtf")
#file_info=initiate_new_upload(FigshareArticleID,FILE_PATH)
## Until here we used the figshare API; following lines use the figshare upload service API.
#upload_parts(file_info)
## We return to the figshare API to complete the file upload process.
#complete_upload(FigshareArticleID, file_info['id'])
##list_files_of_article(article_id)
