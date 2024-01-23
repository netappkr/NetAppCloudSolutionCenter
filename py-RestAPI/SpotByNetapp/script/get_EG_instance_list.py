import requests
import json
import argparse
from datetime import datetime, timedelta
import time
import pandas as pandas
import json

parser = argparse.ArgumentParser(description="eg group-id,token,fromData,toData,severity 입력 자세한 내용은 spot api 문서에 eg 로그 조회 참조")
parser.add_argument("-gid","--group-id", type=str, help="Elastigroup id")
parser.add_argument("-aid","--account-id", type=str, help="Account id")
parser.add_argument("-token","--token", type=str, help="bear token")

args= parser.parse_args()

# API req
url1 = 'https://api.spotinst.io/aws/ec2/group/'+args.group_id+'/status'
headers = {'Authorization': 'Bearer '+args.token,'Content-Type':'json'}
params = {'accountId':args.account_id}
#data1 = {'example':'example'}

response1 = requests.get(url1,headers=headers,params=params)
    #post예시 response = requests.post(url1, headers=headers1, params=params,data=json.dumps(data1))

print('url1 response code:'+ str(response1.status_code) +'\n')
    # print(response.url)
    # print(response.headers)
    # print(response.content)
eg_ec2_status_dt = pandas.DataFrame()
eg_ec2_health_dt = pandas.DataFrame()
url2 = 'https://api.spotinst.io/aws/ec2/group/'+args.group_id+'/instanceHealthiness'
headers = {'Authorization': 'Bearer '+args.token,'Content-Type':'json'}
params = {'accountId':args.account_id}
response2 = requests.get(url2,headers=headers,params=params)

print('url2 response code:'+ str(response1.status_code) +'\n')

jsondata = json.loads(response1.content)
if response1.status_code == 200:
    #jsondata=json.dumps(jsondata['response']['items'])
    for value in jsondata['response']['items']:
        add=pandas.DataFrame.from_records([{
        'instanceId': value['instanceId'],
        "instanceType": value['instanceType'],
        "product": value['product'],
        "groupId": value['groupId'],
        "availabilityZone": value['availabilityZone'],
        "privateIp": value['privateIp'],
        "createdAt": value['createdAt'],
        "publicIp": value['publicIp'],
        "ipv6Address": value['ipv6Address'],
        "status": value['status'],
        "lockStatus": value['lockStatus']
        }])
        eg_ec2_status_dt=eg_ec2_status_dt.append(add,ignore_index = True)
    #eg_status_df.to_csv(args.group_id + '-'+ datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '-instance-list.csv',index=False)

jsondata = json.loads(response2.content)
#print(json.dumps(jsondata['response']['items']))
if response2.status_code == 200:
    #jsondata=json.dumps(jsondata['response']['items'])
    for value in jsondata['response']['items']:
        add=pandas.DataFrame.from_records([{
        'instanceId': value['instanceId'],
        "lifeCycle": value['lifeCycle']
        }])
        eg_ec2_health_dt=eg_ec2_health_dt.append(add,ignore_index = True)
# print(eg_ec2_status_dt)
# print(eg_ec2_health_dt)
df_OUTER_JOIN = pandas.merge(eg_ec2_status_dt,eg_ec2_health_dt,left_on='instanceId',right_on='instanceId',how='outer')

with pandas.ExcelWriter(args.group_id + '-'+ datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '-instance-list.xlsx') as writer:
    df_OUTER_JOIN.to_excel(writer,sheet_name='instance_lifetime_history', index=False)