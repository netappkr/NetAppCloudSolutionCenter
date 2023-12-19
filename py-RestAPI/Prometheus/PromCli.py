#!/usr/bin/env python3
import requests
import json
import argparse
import datetime as dt
import time
import textwrap
parser = argparse.ArgumentParser(description="PromAPI 문서 참조")
parser.add_argument("-url", "--server-url", type=str, help="prometheus server url default http://127.0.0.1:9090", default="http://127.0.0.1:9090")
# promcli -help
subparsers = parser.add_subparsers(dest='kind', help='sub-command help')
subparsers.required = True
# promcli admin -help
parser_admin = subparsers.add_parser('admin', help='used admin api "promcli admin --help"')
parser_admin.add_argument("command",type=str, help=textwrap.dedent('''
                                                                   value list[delete_series, status, snapshot
                                                                   '''))
parser_admin.add_argument("--series",type=str, help=textwrap.dedent('''
                                                                    required = false,
                                                                    example value : cluster_new_status,
                                                                    default : "",
                                                                    please recomand this https://prometheus.io/docs/prometheus/latest/querying/basics/#time-series-selectors
                                                                    '''),default="")
parser_admin.add_argument("--query",type=str, help=textwrap.dedent('''
                                                                    required = false,
                                                                    example value : job=~'harvest',
                                                                    default="job='harvest'",
                                                                    please recomand this https://prometheus.io/docs/prometheus/latest/querying/basics/#time-series-selectors
                                                                    ''')
                                                                    ,default="job='harvest'")
parser_admin.add_argument("-st","--starttime", type=str, help=textwrap.dedent('''
                                                                               example value : 2023-12-08,
                                                                               "please insert to start time about tsdb data"
                                                                               '''))
parser_admin.add_argument("-et","--endtime", type=str, help=textwrap.dedent('''
                                                                             example value : 2023-12-08,
                                                                             "please insert to start time about tsdb data"
                                                                             '''))
# promcli series -help
parser_series = subparsers.add_parser('series', help='used series api "promcli series --help"')
parser_series.add_argument("--series",type=str,help=textwrap.dedent('''
                                                                    required = false,
                                                                    example value : cluster_new_status,
                                                                    default : "",
                                                                    please recomand this https://prometheus.io/docs/prometheus/latest/querying/basics/#time-series-selectors
                                                                    '''),default="")
parser_series.add_argument("--query",type=str, help=textwrap.dedent('''
                                                                    required = false,
                                                                    example value : job=~'harvest',
                                                                    default="job='harvest'",
                                                                    please recomand this https://prometheus.io/docs/prometheus/latest/querying/basics/#time-series-selectors
                                                                    ''')
                                                                    ,default="job='harvest'")
parser_series.add_argument("-st","--starttime", type=str, help=textwrap.dedent('''
                                                                               example value : 2023-12-08,
                                                                               "please insert to start time about tsdb data"
                                                                               '''))
parser_series.add_argument("-et","--endtime", type=str, help=textwrap.dedent('''
                                                                             example value : 2023-12-08,
                                                                             "please insert to start time about tsdb data"
                                                                             '''))

# promcli target -help
parser_series = subparsers.add_parser('target', help='used series api "promcli targets --help"')
parser_series.add_argument("--state",type=str, help=textwrap.dedent('''
                                                                    required = false,
                                                                    value list[active, dropped, any],
                                                                    defalt=any,
                                                                    please recomand this https://prometheus.io/docs/prometheus/latest/querying/api/#targets
                                                                    ''')
                                                                    ,default="any")
parser_series.add_argument("--scrapePool",type=str, help=textwrap.dedent('''
                                                                         required = false,
                                                                         example value : harvest ,
                                                                         please recomand this https://prometheus.io/docs/prometheus/latest/querying/api/#targets
                                                                         ''')
                                                                         ,default="harvest")
args= parser.parse_args()
print(args)
def promcli_tsdb_delete(promurl,st,et):
    # starttime=dt.datetime.strptime(st,'%Y-%m-%d')
    # endtime=dt.datetime.strptime(et,'%Y-%m-%d')
    
    start_timestamp = time.mktime(dt.datetime.strptime(st,'%Y-%m-%d').timetuple())
    end_timestamp = time.mktime(dt.datetime.strptime(et,'%Y-%m-%d').timetuple())

    print("url: "+promurl+" starttime: "+st)
    # API req
    url = promurl+'/api/v1/admin/tsdb/delete_series'
    # 'http://localhost:9090/api/v1/admin/tsdb/delete_series?match[]=up&match[]=process_start_time_seconds{job="prometheus"}'
    # http://localhost:9090/api/v1/series?match[]={job="harvest"}&start=1701356400&end=1701442799
    headers = {}
    params = {
        'match[]':'{job=~"harvest"}',
        'start' : start_timestamp,
        'end': end_timestamp
    }
    response=requests.post(url,headers=headers,params=params)
    if response.status_code == 204:
        url = promurl+'/api/v1/admin/tsdb/clean_tombstones'
        response=requests.post(url)
        if response.status_code == 204:
            return response
    # post예시 response = requests.post(url1, headers=headers1, params=params,data=json.dumps(data1))
    return response

def promcli_tsdb_status(promurl):
    url = promurl+'/status/tsdb'
    response = requests.post(url)
    return response

def promcli_backup(promurl):
    url = promurl+'/api/v1/admin/tsdb/snapshot'
    response = requests.post(url)
    return response

def promcli_get_series(promurl,series,query,st,et):
    start_timestamp = time.mktime(dt.datetime.strptime(st,'%Y-%m-%d').timetuple())
    end_timestamp = time.mktime(dt.datetime.strptime(et,'%Y-%m-%d').timetuple())
    url = promurl+'/api/v1/series'
    headers = {}
    params = {
        'match[]':series+'{'+query+'}',
        'start' : start_timestamp,
        'end': end_timestamp
    }
    # http://localhost:9090/api/v1/series??match[]={job="harvest"}&start=1701356400&end=1701442799
    response = requests.post(url,headers=headers,params=params)
    return response           

def promcli_get_target(promurl,state,scrapePool):
    url = promurl+'/api/v1/targets'
    headers = {}
    params = {
        'state':state,
        'scrapePool' : scrapePool
    }
    # http://localhost:9090/api/v1/series??match[]={job="harvest"}&start=1701356400&end=1701442799
    response = requests.post(url,headers=headers,params=params)
    return response 

# main
result=None
if args.kind == "admin":
    if args.command == "delete_series":
        result=promcli_tsdb_delete(args.server_url,args.starttime,args.endtime)
    if args.command == "status":
        result=promcli_tsdb_status(args.server_url)
    if args.command == "snapshot":
        if args.command == "create":
            result=promcli_backup(args.server_url)
elif args.kind == "series":
    result=promcli_get_series(args.server_url,args.series,args.query,args.starttime,args.endtime)
elif args.kind == "target":
    result=promcli_get_target(args.server_url,args.state,args.scrapePool)
else:
    print("you need instart target args please check the --help command")

# return
if result:
    if result.content:
        jsondata = json.loads(result.content)
        print(result.status_code)
        print(json.dumps(jsondata,indent=3))
    else:
        print(result.status_code)

else:
    print(result)
    print("someting wrong")