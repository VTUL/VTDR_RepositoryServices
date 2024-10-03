The codes here show the workflow set up by Virginia Tech Data Repository (https://data.lib.vt.edu/) to download and deposit bags to aptrust via DART (https://aptrust.github.io/dart-docs/users/workflows/). Virginia Tech Data Services uses  a simple client for the figshare API in python from Cognoma: https://github.com/cognoma/figshare, parts of LD-Cool-P from University of Arizona workflow: https://github.com/padmacarstens/LD-Cool-P to download files and retrieve files from the Virginia Tech Data Repository: VTDR (https://data.lib.vt.edu). VTDR runs on the figshare for institutions platform.
The codes are run to create folders to save the downloaded private files (to ingest bags)/ published files (to publication bags) to the local computer/remote storage, create an Archival Package readme file for archival purposes in addition to an automated README file in rtf format created from the filled in figshare metadata fields.
Lastly, the codes deposit these bags to APTrust via their DART platform (https://aptrust.github.io/dart-docs/users/workflows/) and/or Virginia Tech Libraries storage 

Documentation on how to set up a Windows environment to use these codes is available at CuratorWorkflowDiagramWithScriptExecution_v1_20231108.docx

# RUNNING BATCH CODES
  Open a new folder in your curation directory, name it 'batchcodes'. Go to the curation directory on vscode bash:

conda activate curation
cd curation/batchcodes
git clone https://github.com/VTUL/VTDR_RepositoryServices.git

Open generate_config_batch_example.py and save it as generate_config_batch.py. Copy paste the credentials from generate_config.py. The only new addition will be the path to the curation services actions folder where emails are to be saved:
    VTCurSerFoldPath="/Users/padma/opt/anaconda3/envs/curation/test"

Move the contents(emails, provenance log) to this folder (VTCurSerFoldPath). Open AutomateProvenanceLog_Batch.py and fill in the curator/description. Save the file. 
 
Open downloadFigshareContent_batch.py

Provide the article ids on the first line in this code:
```
FigshareArticleID=["212121","5453543","32232"]
```
Add more with a comma, or replace with the article ids for the ingest/publication content. 

Run downloadFigshareContent_batch.py
(For the error bs4 not found, please do "pip3 install BeautifulSoup4")
Pick 1 for Ingest 2 for Pub
Pick 1 for demo 4 for repo

Make sure "curation" environment is activated. Ctrl+Shift+P, Select Python Interpreter, pick 'curation'.