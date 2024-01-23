import requests
import json
import argparse
from datetime import datetime, timedelta
import time
import pandas
import traceback
import textwrap
import re

parser = argparse.ArgumentParser(description="eg group-id,token,fromData,toData,severity 입력 자세한 내용은 spot api 문서에 eg 로그 조회 참조")
## 커맨더 분기
subparsers = parser.add_subparsers(dest='kind', help='sub-command help')
subparsers.required = True

## GetSpotLog eg --help
parser_eg = subparsers.add_parser('eg', help='used eg api "GetSpotLog eg --help"')
parser_eg.add_argument("-gid","--group-id", type=str, help="Elastigroup id",required=True)
parser_eg.add_argument("-aid","--account-id", type=str, help="Account id",required=True)
parser_eg.add_argument("-from","--fromtime", type=str, help="from time yyyy-mm-dd hh:mm:ss example '2023-12-09 13:31:00'",required=True)
parser_eg.add_argument("-to","--totime", type=str, help="to time yyyy-mm-dd hh:mm:ss example '2024-01-08 13:31:00'",required=True)
parser_eg.add_argument("-level","--level", type=str, help="severity default is ALL / you can only insert ALl,INFO,DEBUG,ERROR", default='ALL')
parser_eg.add_argument("-token","--token", type=str, help="bear token",required=True)
parser_eg.add_argument("-o","--output", type=str, help="you can choise format json or excel",default='json')
## GetSpotLog ocean --help
parser_ocean = subparsers.add_parser('ocean', help='used Ocean api "GetSpotLog ocean --help"')
parser_ocean.add_argument("-gid","--group-id", type=str, help="ocean id",required=True)
parser_ocean.add_argument("-aid","--account-id", type=str, help="Account id",required=True)
parser_ocean.add_argument("-from","--fromtime", type=str, help="from time yyyy-mm-dd hh:mm:ss example '2023-12-09 13:31:00'",required=True)
parser_ocean.add_argument("-to","--totime", type=str, help="to time yyyy-mm-dd hh:mm:ss example '2024-01-08 13:31:00'",required=True)
parser_ocean.add_argument("-level","--level", type=str, help="severity default is ALL / you can only insert ALl,INFO,DEBUG,ERROR", default='ALL')
parser_ocean.add_argument("-token","--token", type=str, help="bear token",required=True)
parser_ocean.add_argument("-o","--output", type=str, help="you can choise format json or excel",default='json')

args= parser.parse_args()
from_time=datetime.strptime(args.fromtime,'%Y-%m-%d %H:%M:%S')
to_time=datetime.strptime(args.totime,'%Y-%m-%d %H:%M:%S')

# from_timestamp = time.mktime(from_time.timetuple())
# to_timestamp = time.mktime(to_time.timetuple())

##
### 날짜형식 (ISO 8601) 예시 YYYY-MM-DDThh:mm:ssTZD , 2016-09-18T17:34:02.666Z
# from_time = datetime.strptime("2023-12-09 13:31:00",'%Y-%m-%d %H:%M:%S')
# to_time = datetime.strptime("2024-01-08 13:31:00",'%Y-%m-%d %H:%M:%S')
# from_timestamp = time.mktime(next_time.timetuple())
# next_time = next_time+datetime.timedelta(days=1)
# next_timestamp = time.mktime(next_time.timetuple())


# API req
def GetData(kind,from_time,to_time):
	logdata = {}
	if kind == "eg" or "Ocean":
		next_time = from_time
		while to_time > next_time:
			from_timestamp = int(time.mktime(next_time.timetuple())*1000)
			next_time = next_time+timedelta(days=1)
			next_timestamp = int(time.mktime(next_time.timetuple())*1000)
			
			url = 'https://api.spotinst.io/aws/ec2/group/'+args.group_id+'/logs'
			headers = {
				'Authorization': 'Bearer '+args.token,
				'Content-Type':'json'
			}
			params = {
				'accountId':args.account_id,
				'fromDate': from_timestamp,
				'toDate': next_timestamp,
				'severity':args.level
			}
			#data1 = {'example':'example'}

			response = requests.get(url,headers=headers,params=params)
			#post예시 response = requests.post(url1, headers=headers1, params=params,data=json.dumps(data1))
			if response.status_code == 200:
				logdata[next_timestamp]=json.loads(response.content)
			else:
				print("status_code:",response.status_code)
				print("content:",response.content)
				continue
			# print(response.url)
			# print(response.headers)
			# print(response.content)
			
	else:
		print("unknown",kind)
	return logdata

def output(output,logdata):
	if output == "json":
		for timestamp, values in logdata.items():
			filename = f"{args.group_id + datetime.utcfromtimestamp(int(timestamp) / 1000.0).strftime('%Y-%m-%d')}.json"
			# JSON 파일로 저장
			with open(filename, 'w') as file:
				json.dump(values, file, indent=2)
			# f = open(args.group_id +'_'+next_time.strftime('%Y-%m-%d') +'log.json',mode='w')
			# f.write(json.dumps(response.json()))
			# f.close
	elif output == "excel":
		datatable = pandas.DataFrame()
		launch_ec2_dt = pandas.DataFrame()
		detach_ec2_dt = pandas.DataFrame()
		for timestamp, values in logdata.items():
			datatable = datatable._append(pandas.DataFrame.from_dict(values["response"]["items"]),ignore_index=True)
			
			for data in values["response"]["items"]:
				ec2_launched_date = None
				ec2_detached_date = None
				Reason = None
				is_launched=re.findall('have been launched',data['message'])
				if is_launched:
					ec2_launched_date = data['createdAt']
				is_detached=re.findall('have been detached',data['message'])
				if is_detached: 
					ec2_detached_date = data['createdAt']
				Reason = str(data['message'])
				if Reason.find("Reason") != -1:
					Reason = Reason[Reason.find("Reason"):]
				else:
					Reason = None

				# instaance ID 추출 정규식 i-[a-z0-9]{17}
				ec2_ids=re.findall('i-[a-z0-9]{17}',data['message'])
				if ec2_ids:
					if  ec2_launched_date:
						for ec2_id in ec2_ids:
							add=pandas.DataFrame.from_records([{
								'InstanceId': ec2_id,
								'lanch_at': ec2_launched_date
							}])
							launch_ec2_dt=launch_ec2_dt._append(add,ignore_index = True)
					elif ec2_detached_date:
						for ec2_id in ec2_ids:
							add=pandas.DataFrame.from_records([{
								'InstanceId': ec2_id,
								'detach_at': ec2_detached_date,
								'message' : Reason
							}])
							detach_ec2_dt=detach_ec2_dt._append(add,ignore_index = True)
				
		df_OUTER_JOIN = pandas.merge(launch_ec2_dt,detach_ec2_dt,left_on='InstanceId',right_on='InstanceId',how='outer')
		with pandas.ExcelWriter(args.group_id + from_time.strftime('%Y-%m-%d')+"-"+to_time.strftime('%Y-%m-%d')+"log.xlsx") as writer:
			datatable.to_excel(writer,sheet_name=args.group_id, index=False)
			df_OUTER_JOIN.to_excel(writer,sheet_name='instance_lifetime_history', index=False)
	else:
		print("unknown",output)

data = GetData(args.kind,from_time,to_time)
output(args.output,data)