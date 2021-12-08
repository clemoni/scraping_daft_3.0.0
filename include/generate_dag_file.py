import json
import os
import shutil
import fileinput
from time import sleep

config_filepath = 'include/dag_config/'
dag_template_filename = 'include/dag_template.py'


for filename in os.listdir(config_filepath):

    f = open(config_filepath + filename)
    config = json.load(f)

    new_filename = 'dags/'+config['DagId']+'.py'
    shutil.copyfile(dag_template_filename, new_filename)

    for line in fileinput.input(files=new_filename, inplace=True):
        if line.find('dagschedule') != -1:
            line = line.replace("dagschedule", f"'{config['Schedule']}'")
        elif line.find('dagid') != -1:
            line = line.replace("dagid", f"'{config['DagId']}'")
        elif line.find('dagsparkmaster') != -1:
            line = line.replace("dagsparkmaster", f"'{config['SparkMaster']}'")
        elif line.find('dagcounty') != -1:
            line = line.replace("dagcounty", f"'{config['County']}'")

        print(line, end="")

    print(f'{new_filename} created with success')
