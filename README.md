The codes here show the workflow set up by [Virginia Tech Data Repository](https://data.lib.vt.edu/) to download and deposit bags to aptrust via [DART](https://aptrust.github.io/dart-docs/users/workflows/). Virginia Tech Data Services uses a simple client for the figshare API in python from [Cognoma](https://github.com/cognoma/figshare), parts of [LD-Cool-P from University of Arizona workflow]( https://github.com/padmacarstens/LD-Cool-P), and [Scripting with DART](https://aptrust.github.io/dart-docs/users/scripting/). VTDR runs on the figshare for institutions platform.
The workflow creates folders for [VTDR](https://data.lib.vt.edu) articles in-review(ingest content: before curator-client interactions) and after review(published content: after curator-client interactions). The content is then bagged in tarred format. Part of the bagging for published content involves creation of ArchivalReadme.rtf file, README.rtf file, and addition of emails, ProvenanceLog.rtf by the curator. The bagged content is then transferred to APTrust via their [DART](https://aptrust.github.io/dart-docs/users/workflows/) and/or Virginia Tech Libraries storage. [APTrust registry](https://aptrust.org/documentation-page/registry/) checks are made to avoid overwriting existing bags.

Detailed documentation on how to set up a Windows/Mac environment to use these codes is available at:
ScriptsSetupAndExecution_CurationWorkflow_Windows.docx
ScriptsSetupAndExecution_CurationWorkflow_Mac.docs

Workflow diagram with description of each block is available at:
CuratorWorkflowDiagramWithScriptExecution_v1_20231108.docx

# RUNNING CODES FOR BAGGING IN REVIEW/PUBLISHED ARTICLES AND TRANSFERRING TO APTRUST:
```
git clone https://github.com/VTUL/VTDR_RepositoryServices.git
```
Open generate_config_example.py and save it as generate_config.py and fill in the credentials (see the running scripts document for more information)
Open generate_config.py, enter the figshare article id to be bagged. -Run the 'IngFolder_Download_TransferBagAPTrust.py' for bagging before-review/ingest content. 
Or
-Run PubFolder_Download.py for downloading published figshare article. Open VTCurationServicesActions folder, add non disseminated content(emails, provenance logs etc.) and then run PubBagDART_TransferAPTrust.py to bag and transfer content to aptrust.


# RUNNING BATCH CODES
  Open a new folder in your curation directory, name it 'batchcodes'. In VScode, File->OpenFolder->batchcodes, click 'Select Folder'
Open a python terminal:
```
conda activate curation
cd curation/batchcodes
git clone https://github.com/VTUL/VTDR_RepositoryServices.git
cd ..
```

From the Explorer on the left side in VSCode, open generate_config_batch_example.py and save it as generate_config_batch.py. Copy paste the credentials from generate_config.py. The only new addition will be the path to the curation services actions folder where emails are to be saved:

    VTCurSerFoldPath="/Users/padma/opt/anaconda3/envs/curation/test"

Make a new folder in 'curation' folder called 'test'(or whatever you want to name it, make sure to change it above as well if other than 'test') and move the contents of curation services actions(emails etc.) to this folder.

Open AutomateProvenanceLog_Batch.py and fill in the curator/description. Save the file. 
 
Open downloadFigshareContent_batch.py

Provide the article ids on the first line in this code:
```
FigshareArticleID=["212121","5453543","32232"]
```
Add more ids or replace with the article ids for the ingest/publication content. 
Run downloadFigshareContent_batch.py
Pick 1 for Ingest, 2 for Pub
Pick 1 for demo, 4 for repo

Run downloadFigshareContent_batch.py
(For the error bs4 not found, please do "pip3 install BeautifulSoup4")
Pick 1 for Ingest 2 for Pub
Pick 1 for demo 4 for repo

Make sure "curation" environment is activated. Ctrl+Shift+P, Select Python Interpreter, pick 'curation'.