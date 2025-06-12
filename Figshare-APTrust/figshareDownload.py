import requests
import hashlib
from requests import HTTPError
import os
from os.path import exists
from redata.commons.logger import log_stdout
import figshareRetrieve
#import calculateChecksum
N_TRIES_MD5 = 3 # Number of attempts for checksum
def download_files(article_id, fversion, fs, root_directory=None, data_directory=None,   metadata_directory=None, log=None, metadata_only=False):
    """
    Purpose:
      Retrieve data for a Figshare deposit following data curation workflow

    :param article_id: Figshare article ID (int)
    :param fs: Figshare object
    :param root_directory: Root path for curation workflow (str)
    :param data_directory: Relative folder path for primary location of data (str)
    :param metadata_directory: Relative folder path for primary location of metadata (str)
    :param log: logger.LogClass object. Default is stdout via python logging
    :param metadata_only: bool indicates whether to retrieve metadata. Default: True
           If set, no files are downloaded
    """
    if isinstance(log, type(None)):
        log = log_stdout()

#log = log_stdout()
    log.info("")
    if metadata_only:
        log.info(f"** NO FILE RETRIEVAL: metadata_only={metadata_only} **")
    else:
        log.info("** DOWNLOADING DATA **")

    if root_directory is None:
        root_directory = os.getcwd()

    # Retrieve article information
    file_list = fs.list_files(article_id,fversion)
    n_files = len(file_list)
    print(f"Number of files in article {article_id}: {n_files}")
    if not data_directory:
        dir_path = os.path.join(root_directory, f"figshare_{article_id}/")#, f"figsharemd_{article_id}/")
    else:
        dir_path = os.path.join(root_directory, data_directory)#, metadata_directory)
    #    dir_path = data_directory
    os.makedirs(dir_path, exist_ok=True)  # This might require Python >=3.2
    
    if not metadata_directory:
       dir1_path = os.path.join(root_directory, f"figshare_file_metadata_{article_id}/")
    else:
       dir1_path = os.path.join(root_directory, metadata_directory)

    os.makedirs(dir1_path, exist_ok=True)  # This might require Python >=3.2

    log.info(f"Total number of files: {n_files}")

    out_file_prefix = f"file_list_original_{article_id}"


    if not metadata_only:
        for n, file_dict in zip(range(n_files), file_list):
            log.info(f"Retrieving {n+1} of {n_files} : "
                     f"{file_dict['name']} ({file_dict['size']})")
            log.info(f"URL: {file_dict['download_url']}")
            filename = os.path.join(dir_path, file_dict['name'])
            retrieve_cnt = 0
            checksum_flag = False
            if not exists(filename):
                while retrieve_cnt < N_TRIES_MD5:
                    log.info(f"Retrieval attempt #{retrieve_cnt + 1}")
                    try:
                        figshareRetrieve.private_file_retrieve(file_dict['download_url'],
                                              filename=filename, token=fs.token,
                                              log=log)
                        log.info("Download successful!")
                        retrieve_cnt += 1
                    except (HTTPError, IOError):
                        retrieve_cnt += 1
                 # Perform checksum
                    if exists(filename):
                        if not file_dict['is_link_only']:
#                            checksum_flag = calculateChecksum.check_md5(filename,
#                                                      file_dict['supplied_md5'])
                            #------------------------------
                            log.info("Performing MD5 checksum ...")
                            checksum_flag=False
                            hash_md5=hashlib.md5()
                            with open(filename,"rb") as f:
                                for chunk in iter(lambda: f.read(4096),b""):
                                    hash_md5.update(chunk)
                            checksum_compute=hash_md5.hexdigest()
                            if checksum_compute == file_dict['supplied_md5']:
                                checksum_flag=True
                                print('checksum flag stage 1 ',checksum_flag)
                                log.info("MD5 Checksum passed!!!")
                            else:
                                print('checksum flag stage 2 ',checksum_flag)
                                log.warning("Checksum failed!!!")
                            log.info(f"MD5 Result: {checksum_compute}")  
                            log.info(f"Expectation: {file_dict['supplied_md5']}")
                            #-------------------------------
                            if checksum_flag:
                                print('checksum flag stage 3 ',checksum_flag)
                                break
                        else:
                            print('checksum flag stage 4 ',checksum_flag)
                            log.info("Not performing checksum on linked-only record")
                            break
                else:
                    if not checksum_flag:
                        print('checksum flag stage 5 ',checksum_flag)
                        log.warning("File retrieval unsuccessful! "
                                    f"Aborted after {N_TRIES_MD5} tries")
            else:
                log.info("File exists! Not overwriting!")


