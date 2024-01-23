import pandas as pandas
import glob
import os
import json

for filename in glob.glob('*.json'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        jsondata=json.load(f)
    jsondata=json.dumps(jsondata['response']['items'])
    df = pandas.read_json(jsondata)
    df.to_csv(filename+'.csv',index=False)