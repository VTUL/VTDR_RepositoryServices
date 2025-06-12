#Following code was developed by Figshare, this code is implemented for data curation/archiving/deposition at Virginia Tech with some minor changes 
import json
from tokenize import group
import requests
from requests.exceptions import HTTPError
import os
from urllib.request import urlretrieve


def issue_request(method, url, headers, data=None, binary=False,
                  params=None):
    """Wrapper for HTTP request

    Parameters
    ----------
    method : str
        HTTP method. One of GET, PUT, POST or DELETE

    url : str
        URL for the request

    headers: dict
        HTTP header information

    data: dict
        Figshare article data

    binary: bool
        Whether data is binary or not

    params: dict
        Additional information for URL GET request

    Returns
    -------
    response_data: dict
        JSON response for the request returned as python dict
    """
    if data is not None and not binary:
        data = json.dumps(data)

    response = requests.request(method, url, headers=headers,
                                data=data, params=params)
   
    
    try:
        print(url)
        response.raise_for_status()
        try:
            response_data = json.loads(response.text)
        except ValueError:
            response_data = response.content
    except HTTPError as error:
        print('Caught an HTTPError: {}'.format(error))
        print('Body:\n', response.text)
        raise

    return response_data


class Figshare:
    """ A Python interface to Figshare

    Attributes
    ----------
    baseurl : str
        Base URL of the Figshare v2 API

    token : str
        The Figshare OAuth2 authentication token

    private : bool
        Boolean to check whether connection is to a private or public article

    stage : bool
        Boolean to use a different baseurl for Figshare stage vs production

    Methods
    -------
    endpoint(link)
        Concatenate the endpoint to the baseurl

    get_headers()
        Return the HTTP header string

    create_article()
        Create a new figshare article

    update_article(article_id)
        Update existing article

    get_article_details(article_id, version)
        Get some information about a article

    list_article_versions(article_id)
        List versions of the given article

    list_files(article_id, version)
        List files within a given article

    get_file_details(article_id, file_id)
        Print file details

    retrieve_files_from_article(article_id)
        Retrieve files and save them locally.

    """
    def __init__(self, token=None, private=False, stage=False,version=None):
        if not stage:
            self.baseurl = "https://api.figshare.com/v2"
        else:
            self.baseurl = "https://api.figsh.com/v2"

        self.token = token
        self.private = private
        self.version = version

    def endpoint(self, link):
        """Concatenate the endpoint to the baseurl"""
        return self.baseurl + link


    def get_headers(self, token=None):
        """ HTTP header information"""
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = 'token {0}'.format(token)

        return headers

    def create_article(self, title, description,
                       defined_type, tags, categories):
        """ Create a new Figshare article.

        Parameters
        ----------
        title : str
            Article title

        description : str
            Article description

        defined_type : str
            One of 'figure', 'media', 'dataset', 'fileset', 'poster',
            'paper', 'presentation', 'thesis', 'code' or 'metadata'

        tags : list of str
            List of tags associated with the article

        categories : list of int
            List of category ids associated with the article

        Returns
        -------
        article_id : str
            id of article created

        """
        if isinstance(categories, int):
            categories = [categories]

        data = {'title': title,
                'description': description,
                'defined_type': defined_type,
                'categories': categories,
                'tags': tags}

        url = self.endpoint("/account/articles")
        headers = self.get_headers(self.token)
        response = self.issue_request('POST', url, headers=headers, data=data)

        if "error" not in response:
            article_id = int(response["location"].split("/")[-1])
        else:
            article_id = None
        return article_id

    def update_article(self, article_id, **kwargs):
        """Updates an article with a given article_id.

        Parameters
        ----------
        article_id : str or int
            Article id

        Returns
        -------
        response : dict
            HTTP response json as a python dict
        """
        allowed = {'title', 'description', 'defined_type',
                   'tags', 'categories'}
        valid_keys = set(kwargs).intersection(allowed)
        body = {}

        for key in valid_keys:
            body[key] = kwargs[key]

        url = self.endpoint('/account/articles/{0}'.format(article_id))
        headers = self.get_headers(token=self.token)
        response = issue_request('PUT', url, headers=headers,
                                 data=json.dumps(body))
        return response

  #  def get_article_details(self, article_id, version=None):

    def get_article_details(self, article_id, version):        
        """ Return the details of an article with a given article ID.

        Parameters
        ----------
        article_id : str or id
            Figshare article ID

        version : str or id, default is None
            Figshare article version. If None, selects the most recent version.

        Returns
        -------
        response : dict
            HTTP request response as a python dict
        """
        if version is None:
            if self.private:
                url = self.endpoint('/account/articles/{}'.format(article_id))
            else:
                url = self.endpoint('/articles/{}'.format(article_id))
        else:
            if self.private:
                # Not supported by the Figshare V2 API
                url = self.endpoint('/account/articles/{}/versions/{}'.format(
                    article_id,
                    version))
            else:
                url = self.endpoint('/articles/{}/versions/{}'.format(
                    article_id,
                    version))
        headers = self.get_headers(self.token)
        response = issue_request('GET', url, headers=headers)
        return response

    #def get_groupid_names(self, version=None):
    def get_groupid_names(self, version):    
        """ Return the group id details of an article 

        Parameters
        ----------
        version : str or id, default is None
        Figshare article version. If None, selects the most recent version.

        Returns
        -------
        response : dict
            HTTP request response as a python dict
        """
        if version is None:
            url = self.endpoint('/account/institution/groups?access_token=token')
        headers = self.get_headers(self.token)
        group = issue_request('GET', url, headers=headers)
        return group


    def list_article_versions(self, article_id):
        """ Return the details of an article with a given article ID.

        Parameters
        ----------
        article_id : str or int
            Figshare article ID

        Returns
        -------
        response : dict
            HTTP request response as a python dict
        """
        if self.private:
            pass
        else:
            url = self.endpoint('/articles/{}/versions'.format(article_id))
        headers = self.get_headers(self.token)
        response = issue_request('GET', url, headers=headers)
        return response

    #def list_files(self, article_id, version=None):
    def list_files(self, article_id, version):
        """ List all the files associated with a given article.

        Parameters
        ----------
        article_id : str or int
            Figshare article ID

        version : str or id, default is None
            Figshare article version. If None, selects the most recent version.

        Returns
        -------
        response : dict
            HTTP request response as a python dict
        """
    #    https://api.figshare.com/v2/account/institution/review
    #    https://data.lib.vt.edu/ndownloader/files/29109711
    #    https://figshare.com/articles/dataset/AREAdata_GID2_output_files/16587311
    #    https://data.lib.vt.edu/articles/dataset/field-dependent_XFMR_fitting/15143949
    #    https://data.lib.vt.edu/articles/dataset/Social_Networks_in_Georgian_Britain/14849748
        
        if version is None:
            files = []
            page = 1
            per_page = 100  # Adjust as needed or as allowed by the API
            while True:
                if self.private:
                    url = self.endpoint('/account/articles/{}/files'.format(article_id))
                #url = self.endpoint('/account/institution/review/ '.
                #     format(article_id))
                else:
                    url = self.endpoint('/articles/{}/files'.format(article_id))
                #  url = self.endpoint('url = self.endpoint('/articles/{}/files'.format(article_id)))
                headers = self.get_headers(self.token)
                params = {'page': page, 'page_size': per_page}
                response = issue_request('GET', url, headers=headers, params=params)
                if not response:
                    break
                files.extend(response)
                if len(response) < per_page:
                    break
                page += 1
            return files
        else:
            request = self.get_article_details(article_id, version)
            return request['files']

    def get_file_details(self, article_id, file_id):
        """ Get the details about a file associated with a given article.

        Parameters
        ----------
        article_id : str or int
            Figshare article ID

        file_id : str or int
            File id

        Returns
        -------
        response : dict
            HTTP request response as a python dict

        """
        if self.private:
            url = self.endpoint('/account/articles/{0}/files/{1}'.
                                format(article_id, file_id))
        else:
            url = self.endpoint('/articles/{0}/files/{1}'.
                                format(article_id, file_id))
        response = issue_request('GET', url,
                                 headers=self.get_headers(token=self.token))
        return response

    def retrieve_files_from_article(self, article_id, directory=None):
        """ Retrieve files and save them locally.

        By default, files will be stored in the current working directory
        under a folder called figshare_<article_id> by default.
        Specify <outpath> for: <outpath>/figshare_<article_id>

        Parameters
        ----------
        article_id : str or int
            Figshare article ID

        """

        if directory is None:
            directory = os.getcwd()

        # Get list of files
        file_list = self.list_files(article_id)

        dir0 = os.path.join(directory, "figshare_{0}/".format(article_id))
        os.makedirs(dir0, exist_ok=True) # This might require Python >=3.2

        for file_dict in file_list:
            urlretrieve(file_dict['download_url'], os.path.join(dir0, file_dict['name']))

