import requests
import json
import argparse
from datetime import datetime
import time

parser = argparse.ArgumentParser(description="eg group-id,token,fromData,toData,severity 입력 자세한 내용은 spot api 문서에 eg 로그 조회 참조")
parser.add_argument("-gid","--group-id", type=str, help="Elastigroup id")
parser.add_argument("-aid","--account-id", type=str, help="Account id")
parser.add_argument("-token","--token", type=str, help="bear token")
parser.add_argument("-fromDay","--fromDay", type=str, help="startDay '%Y-%m-%d' example 2023-03-14")
parser.add_argument("-toDay","--toDay", type=str, help="endDay '%Y-%m-%d' example 2023-03-14")
parser.add_argument("-level","--level", type=str, help="severity default is ALL / you can only insert ALl,INFO,DEBUG,ERROR", default='ALL')

args= parser.parse_args()
fromDay=datetime.strptime(args.fromDay,'%Y-%m-%d')
toDay=datetime.strptime(args.toDay,'%Y-%m-%d')

from_timestamp = time.mktime(datetime.strptime(args.fromDay,'%Y-%m-%d').timetuple())
to_timestamp = time.mktime(datetime.strptime(args.toDay,'%Y-%m-%d').timetuple())
date_diff = toDay - fromDay

# API req
for i in range(date_diff.days):
    url1 = 'https://api.spotinst.io/aws/ec2/group/'+args.group_id+'/logs'
    headers = {'Authorization': 'Bearer '+args.token,'Content-Type':'json'}
    params = {'accountId':args.account_id,
            'fromDate': int(from_timestamp*1000),
            'toDate': int(to_timestamp*1000),
            'severity':args.level
            }
    #data1 = {'example':'example'}

    response = requests.get(url1,headers=headers,params=params)
    #post예시 response = requests.post(url1, headers=headers1, params=params,data=json.dumps(data1))

    print('response code:'+ str(response.status_code) +'\n')
    # print(response.url)
    # print(response.headers)
    # print(response.content)
    
    f = open(args.group_id +'_'+args.fromDay+'_'+args.toDay+'log.json',mode='w')
    f.write(json.dumps(response.json()))
    f.close