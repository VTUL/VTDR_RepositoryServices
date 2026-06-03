uname -m check what version of arc terminal linux
x86_64 -> linux intel (amd64)
aarch64 -> linux ARM

download locally and move it to the folder 

chmod -x dart-runner

./dart-runner --help

whoami -> jiren -> RunnerOutputDir

ls /scratch
ls /scratch/jiren -> null -> mkdir -p /scratch/jiren/bags 
replace with your $(whoami)

globus doesn't have the /scratch

move the configurations under the Figshare-API trust

AutomatedReadmertf.py?
(1) ingest_bagit_arc.py
(2) PubFolder_Download.py : download the metadata.JSON from figshare article id and copy from source file into the destination 
dissenminated / file / DisseminatedContent as the data source  
(2) PubBagDART_TransferAPTrust.py 

slurm globus node doesn't have the slurm 

nohup
###start the nohup
nohup bash run_vtdr_workflow.sh > workflow.log 2>&1 &

###check the log
tail -f workflow.log

###exit the log
Ctrl + C

change the "destination = choose_destination_terminal()" to "destination = "JUST BAGIT" "
(1) and (3)

Questions: 
the pubdownload source file location? is it from arc platform or from the digshare article id? -> PubFolder_Download.py "arc_resource_path" and "arc_template"
couldn't test the "31448899". test failed 
        "[jiren@globus Figshare-APTrust]$ python ./test.py
        Testing metadata download for article: 31448899
        https://api.figshare.com/v2/articles/31448899
        Caught an HTTPError: 404 Client Error: Not Found for url: https://api.figshare.com/v2/articles/31448899
        Body:
        {"message": "Entity not found: ArticleVersion", "code": "EntityNotFound"}
        Traceback (most recent call last):
        File "/projects/lib-data-share/curation_scripts/VTDR_RepositoryServices/Figshare-APTrust/./test.py", line 18, in <module>
            metadata = fs.get_article_details(article_id, version=fversion)
        File "/projects/lib-data-share/curation_scripts/VTDR_RepositoryServices/Figshare-APTrust/figshare.py", line 239, in get_article_details
            response = issue_request('GET', url, headers=headers)
        File "/projects/lib-data-share/curation_scripts/VTDR_RepositoryServices/Figshare-APTrust/figshare.py", line 48, in issue_request
            response.raise_for_status()
        File "/home/jiren/.local/lib/python3.9/site-packages/requests/models.py", line 943, in raise_for_status
            raise HTTPError(http_error_msg, response=self)
        requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://api.figshare.com/v2/articles/31448899"