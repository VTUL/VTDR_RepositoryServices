import requests
import hashlib
from requests import HTTPError
import os
from os.path import exists
from redata.commons.logger import log_stdout
import figshareRetrieve
#import calculateChecksum
from collections import defaultdict


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
    print(f"****************Retrieving file list for article {article_id} version {fversion}")
    file_list = fs.list_files(article_id,fversion)
    n_files = len(file_list)
    print(f"Number of files in article {article_id}: {n_files}")

# --------------------------------------------------
# Check for duplicated file names
# --------------------------------------------------

    filename_groups = defaultdict(list)

    for file_dict in file_list:
        filename_groups[file_dict["name"]].append(file_dict)

    duplicate_filename_groups = {
        filename: files
        for filename, files in filename_groups.items()
        if len(files) > 1
    }

    if duplicate_filename_groups:
        print("\n")
        print("=" * 80)
        print("DUPLICATE FILE NAME CHECK")
        print("=" * 80)
        print(
            "Files with duplicated file names were found. "
            "Please review whether their contents are duplicated."
        )

        for group_number, (filename, files) in enumerate(
            duplicate_filename_groups.items(),
            start=1
        ):
            print(f"\nDuplicate Filename Group {group_number}")
            print(f"Filename: {filename}")

            for file_dict in files:
                print(f"    Figshare file ID: {file_dict.get('id')}")
                print(f"    Size: {file_dict.get('size')}")
                print(f"    URL: {file_dict.get('download_url')}")

    else:
        print("\n")
        print("=" * 80)
        print("DUPLICATE FILE NAME CHECK")
        print("=" * 80)
        print("No duplicated file names were detected.")

# --------------------------------------------------
# Check for duplicated MD5 checksums
# --------------------------------------------------

    md5_groups = defaultdict(list)

    for file_dict in file_list:
        supplied_md5 = file_dict.get("supplied_md5")

        if supplied_md5:
            md5_groups[supplied_md5.lower()].append(file_dict)

    duplicate_md5_groups = {
        md5: files
        for md5, files in md5_groups.items()
        if len(files) > 1
    }

    if duplicate_md5_groups:
        print("\n")
        print("=" * 80)
        print("DUPLICATE MD5 CHECK")
        print("=" * 80)
        print(
            "Files with duplicated MD5 checksums were found. "
            "These files may contain identical content."
        )

        for group_number, (md5, files) in enumerate(
            duplicate_md5_groups.items(),
            start=1
        ):
            print(f"\nDuplicate MD5 Group {group_number}")
            print(f"MD5: {md5}")

            for file_dict in files:
                print(f"    Filename: {file_dict.get('name')}")
                print(f"    Figshare file ID: {file_dict.get('id')}")
                print(f"    Size: {file_dict.get('size')}")
                print(f"    URL: {file_dict.get('download_url')}")

    else:
        print("\n")
        print("=" * 80)
        print("DUPLICATE MD5 CHECK")
        print("=" * 80)
        print("No duplicated MD5 checksums were detected.")


# --------------------------------------------------
# Ask curator whether to proceed if duplicates exist
# --------------------------------------------------
    if duplicate_filename_groups or duplicate_md5_groups:

        while True:

            response = input(
                "\nDuplicated file names and/or duplicated MD5 checksums were detected.\n"
                "Please review the file information above.\n"
                "Would you like to proceed with the download? (yes/no): "
            ).strip().lower()

            print(f"Curator response: {response}")

            if response == "yes":
                print("Proceeding with the workflow.")
                break

            elif response == "no":
                print(
                    "Workflow stopped so the curator can review or revise "
                    "the possible duplicated files."
                )

                return {
                    "file_list": file_list,
                    "expected_file_count": n_files,
                    "duplicate_filename_groups": duplicate_filename_groups,
                    "duplicate_md5_groups": duplicate_md5_groups
                }

            else:
                print("Please enter 'yes' or 'no'.")




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
    return {
    "file_list": file_list,
    "expected_file_count": n_files,
    "duplicate_filename_groups": duplicate_filename_groups
    }


