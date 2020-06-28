import csv
import datetime
from nbiHeaderMapper import *
from neo4j_helper import *
from nbi_prop_converter import *
from set_place_name import *
import sys

root='./output/'

def exec_script_file(file_path):
    with open(file_path,'r') as file:
        for script in file:
            script=script.strip()
            if len(script)>0:
                print('executing-->'+script)
                res=execute_query(script)
        print('executed: '+file_path)

print('INFO: please ensure that all generated csv files are copied to import folder in the installation path of neo4j')

exec_script_file(root+'load_state_county.script')
exec_script_file(root+'load_nbi_data.script')
exec_script_file(root+'post_nbi_data.script')

exec_script_file(root+'load_climate_data.script')
exec_script_file(root+'post_climate_data.script')

print('all scripts are executed')