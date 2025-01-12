from redata.commons.logger import log_stdout
import requests
from requests import HTTPError
import shutil


def private_file_retrieve(url, filename=None, token=None, log=None):
    """
    Purpose:
      Custom Request to privately retrieve a file with a token.
      This was built off of the figshare Python code, but a urlretrieve
      did not handle providing a token in the header.

    :param url: Full URL (str)
    :param filename: Full filename for file to be written (str)
    :param token: API token (str)
    :param log: logger.LogClass object. Default is stdout via python logging
    """

    if isinstance(log, type(None)):
        log = log_stdout()

    headers = dict()
    if token:
        headers['Authorization'] = f'token {token}'

    try:
        h = requests.head(url, headers=headers)
        h.raise_for_status()

        # Chunk read and write with stream option and copyfileobj
        with requests.get(url, stream=True, headers=headers) as r:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except (HTTPError, IOError) as error:
        log.warning(error)
        raise HTTPError(error)