import json
import os

#the config.json is ignored, refer to config_sample.json and provide the secrets in that file and rename it to config.json before starting the server
with open('config.json', "r") as f:
    config = json.load(f)

if(config.get('db',{}).get('schema_name', '')):
    os.environ['SCHEMA_NAME'] = config['db']['schema_name']

if(config.get('db',{}).get('db_name', '')):
    os.environ['DB_NAME'] = config['db']['db_name']

if(config.get('db',{}).get('table_name', '')):
    os.environ['TABLE_NAME'] = config['db']['table_name']