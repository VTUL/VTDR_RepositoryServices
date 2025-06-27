#This was created from Scripting with DART page on aptrust.github.io/dart-docs/users/workflows/, this code takes values from runjob.py to run a job by passing values to DART app through command line. dart_command is where dart is stored. Only thing modified from the original script is adding: encoding='utf8'

import json
import sys
from subprocess import Popen, PIPE
#Get the parameters from configurations.ini to retrieve folder path settings
import configparser
config=configparser.ConfigParser()
config.read('configurations.ini')

class Job:

    # Be sure to set this appropriately for your system.
    # The command 'npm start' is for DART development use only.
    #dart_command = "/Users/padma/AppData/Local/Programs/DART/DART.exe"
    dart_command=config['dart_PathSettings']['dart_exe_path']
    def __init__(self, workflow_name, package_name):
        self.workflow_name = workflow_name
        self.package_name = package_name
        self.files = []
        self.tags = []

    def add_file(self, path):
        self.files.append(path)

    def add_tag(self, tag_file, tag_name, value):
        self.tags.append({
            "tagFile": tag_file,
            "tagName": tag_name,
            "userValue": value
        })

    def to_json(self):
        _dict = {
            "workflowName": self.workflow_name,
            "packageName": self.package_name,
            "files": self.files,
            "tags": self.tags
        }
        return json.dumps(_dict)

    def run(self):
        json_string = self.to_json()
        print(json_string)
        print("Starting job")
        
        cmd = "%s -- --stdin" % Job.dart_command
        child = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True,encoding='utf8')
        stdout_data, stderr_data = child.communicate(json_string +"\n")#,timeout=120
        if stdout_data is not None:
            print(stdout_data)
        if stderr_data is not None:
            sys.stderr.write(stderr_data)
        return child.returncode

      