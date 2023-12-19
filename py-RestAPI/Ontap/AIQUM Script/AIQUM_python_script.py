# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import requests
import argparse
import datetime as dt
import json
import base64
import math
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description="Please refenace Netapp AIQUM doc : https://docs.netapp.com/us-en/active-iq-unified-manager/events/concept_how_scripts_work_with_alerts.html")
parser.add_argument("-eventID", type=str, help="eventID get the AIQUM",required=False)
parser.add_argument("-eventName", type=str, help="eventName get the AIQUM",required=False)
parser.add_argument("-eventSeverity", type=str, help="eventSeverity get the AIQUM",required=False)
parser.add_argument("-eventSourceID", type=str, help="eventSourceID get the AIQUM",required=False)
parser.add_argument("-eventSourceName", type=str, help="eventSourceName get the AIQUM",required=False)
parser.add_argument("-eventSourceType", type=str, help="eventSourceType get the AIQUM",required=False)
parser.add_argument("-eventState", type=str, help="eventState get the AIQUM",required=False)
parser.add_argument("-eventArgs", type=str, help="eventArgs get the AIQUM", required=False)
parser.add_argument("-test", help="eventArgs get the AIQUM",action='store_const',required=False ,const="Netapp Korea PS team")
args= parser.parse_args()
print("### your input data ###")
print(args)
## test comanned case : Inodes Nearly Full
# python .\AIQUM_python_script.py -eventID=20189 -eventName='Inodes Nearly Full' -eventSourceType='VOLUME' -eventSourceName='svm_CVO:/vol' -eventArgs='inodesNearlyFull=11,inodesFull=90,dfMountedOn=vol,dfKBytesTotal=99614720,dfKBytesUsed=1164112,dfKBytesPercent=1.168614437705592,dfInodesTotal=3112959,dfInodesUsed=3049559,dfInodesPercent=97.96335255298897'

## test comand Error EMS recived message
# python .\AIQUM_python_script.py -eventID='30797' -eventName='Error EMS received' -eventSeverity='warning' -eventSourceID='1' -eventSourceName='CVO' -eventSourceType='CLUSTER' -eventState='NEW' -eventArgs='ems-parameters=[percent_full_blocks=80, percent_full_inodes=90, app=ErrorEMSAlert7, vserver_uuid=924a8797-999a-11ee-a416-15bdde6a2aef, object_type=volume, name=vol2],ems-severity=error'


# 환경변수
UMAuth = {
    "url": "https://127.0.0.1",
    "username": "umadmin",
    "password": "Netapp123!@#"
}
auth_token = None
## test input clusterlist
cluserlist = {
    "CVO" : {
        "name" : "CVO",
        "ip": "172.30.0.186",
        "ID": "admin",
        "PW": "Netapp1!"
    },
    "FAS8040" :{
        "name":"FAS8040",
        "ip": "192.168.0.10",
        "ID": "admin",
        "PW": "Netapp1!"
    }
}


# clusterlist를 외부에서 파일로 입력할 경우 사용하는 함수
def PutClustersInfoList(filename) :
    cluserlist=json.load(filename)
    return cluserlist


## AIQ에서 수집한 Inode usd percent 값을 기준으로 계산하는 스크립트
def IncreaseVolumeInodeValues(eventName,eventArgs,ClusterAuth,resource):
    if eventName == "Inodes Full":
        if int(float(eventArgs["dfInodesPercent"])) > int(float(eventArgs["inodesFull"])) :
            inodeTotal= int(math.ceil(float(eventArgs["dfInodesUsed"])*1.66))
            url = "https://"+ClusterAuth["ip"]+'/api/private/cli/volume'
            if resource.content:
                result=json.loads(resource.content)
                
            #headers = {"Authorization": "Basic"+cred}
            params = {
                "vserver": result["records"][0]["svm"]["name"],
                "volume": result["records"][0]["name"]
            }
            data = {
                "files" : inodeTotal
            }
            response=requests.patch(url,auth=HTTPBasicAuth(ClusterAuth["ID"], ClusterAuth["PW"]),params=params,data=json.dumps(data),verify=False)
            if response.status_code == 200:
                print("### Increase Volume Inode Values ###")
                print(json.loads(response.content))
                return response
            else:
                print("### Increase Volume Inode Values ###")
                print(response.request)
                print(response.status_code)
                print(response.url)
                print(response.content)
                exit()

                

    elif eventName == "Inodes Nearly Full":
        if int(float(eventArgs["dfInodesPercent"])) > int(float(eventArgs["inodesFull"])) :
            inodeTotal= int(math.ceil(float(eventArgs["dfInodesUsed"])*1.66))
            url = "https://"+ClusterAuth["ip"]+'/api/private/cli/volume'
            if resource.content:
                result=json.loads(resource.content)
                
            #headers = {"Authorization": "Basic"+cred}
            params = {
                "vserver": result["records"][0]["svm"]["name"],
                "volume": result["records"][0]["name"]
            }
            data = {
                "files" : inodeTotal
            }
            response=requests.patch(url,auth=HTTPBasicAuth(ClusterAuth["ID"], ClusterAuth["PW"]),params=params,data=json.dumps(data),verify=False)
            if response.status_code == 200:
                print("### Increase Volume Inode Values ###")
                print(json.loads(response.content))
                return response
            else:
                print("### Increase Volume Inode Values ###")
                print(response.request)
                print(response.status_code)
                print(response.url)
                print(response.content)
                exit()

    elif eventName == "Alert EMS received":
        if int(float(eventArgs["percent_full_inodes"])) > 60 :
            if resource.content:
                result=json.loads(resource.content)
                files=GetVolumefiles(ClusterAuth,result["records"][0]["name"],result["records"][0]["svm"]["name"])
                
            if files.content:
                files=json.loads(files.content)
            else:
                print("### Increase Volume Inode Values")
                print(json.loads(files.content))

            inodeTotal= int(math.ceil(files["records"][0]["files_used"]*1.66))
            url = "https://"+ClusterAuth["ip"]+'/api/private/cli/volume'
            #headers = {"Authorization": "Basic"+cred}
            params = {
                "vserver": result["records"][0]["svm"]["name"],
                "volume": result["records"][0]["name"]
            }
            data = {
                "files" : inodeTotal
            }
            response=requests.patch(url,auth=HTTPBasicAuth(ClusterAuth["ID"], ClusterAuth["PW"]),params=params,data=json.dumps(data),verify=False)
            if response.status_code == 200:
                print("### Increase Volume Inode Values ###")
                print(json.loads(response.content))
                return response
            else:
                print("### Increase Volume Inode Values ###")
                print(response.status_code)
                print(json.loads(response.content))
                exit()
            


    elif eventName == "Error EMS received":
        if int(float(eventArgs["percent_full_inodes"])) > 60 :
            if resource.content:
                result=json.loads(resource.content)
                files=GetVolumefiles(ClusterAuth,result["records"][0]["name"],result["records"][0]["svm"]["name"])
                
            if files.content:
                files=json.loads(files.content)
                print(files)
            else:
                print("### Increase Volume Inode Values")
                print(json.loads(files.content))
                exit()

            inodeTotal= int(math.ceil(files["records"][0]["files_used"]*1.66))
            url = "https://"+ClusterAuth["ip"]+'/api/private/cli/volume'
            # headers = {"Content-Type": "application/json"}
            params = {
                "vserver": result["records"][0]["svm"]["name"],
                "volume": result["records"][0]["name"]
            }
            data = {
                "files" : inodeTotal
            }
            response=requests.patch(url,auth=HTTPBasicAuth(ClusterAuth["ID"], ClusterAuth["PW"]),params=params,data=json.dumps(data),verify=False)
            if response.status_code == 200:
                print("### Increase Volume Inode Values ###")
                print(json.loads(response.content))
            else:
                print("### Increase Volume Inode Values ###")
                print(response.status_code)
                print(json.loads(response.content))
            return response

    else:
        print("you need devolop "+eventName)
        exit()


def GetClusterAuth(clustername):
    if cluserlist.get(clustername):
        return cluserlist.get(clustername)
    else:
        print("unknown cluster please check the Clusterlist file or var")
        return 0
    


def GetVolumeResourceInfo(umurl="https://localhost",umid="umadmin",umpasswd="Netapp1!",volname="*",svmname="*",clustername="*"):
    url = umurl+'/api/datacenter/storage/volumes'
    #headers = {"Authorization": "Basic"+cred}
    params = {
        "name": volname,
        "svm.name": svmname,
        "cluster.name": clustername
    }
    response=requests.get(url,auth=HTTPBasicAuth(umid, umpasswd),params=params,verify=False)
    if response.status_code == 200:
        return response
    else:
        print("### Get Volume Resource Info ###")
        print(response.request)
        print(response.status_code)
        print(response.url)
        print(response.content)
        exit()
        
def GetVolumefiles(ClusterAuth,volname="*",svmname="*"):
    url = "https://"+ClusterAuth["ip"]+"/api/private/cli/volume"
    params = {
        "volume": volname,
        "vserver": svmname,
        "fields": "files,files-used,files-maximum-possible"
    }
    
    response=requests.get(url,auth=HTTPBasicAuth(ClusterAuth["ID"],ClusterAuth["PW"]),params=params,verify=False)
    if response.status_code == 200:
        return response
    else:
        print("### Get Volume Files ###")
        print(response.status_code)
        print(response.url)
        return response
    
def GetClusterResourceInfo(umurl,umid,umpasswd,clustername):
        url = umurl+'/api/datacenter/cluster/clusters'
        #headers = {"Authorization": "Basic"+cred}
        params = {
            "name": clustername,
        }
        response=requests.get(url,auth=HTTPBasicAuth(umid, umpasswd),params=params,verify=False)
        if response.status_code == 200:
            return response
        else:
            print(response.status_code)
            print(json.loads(resource.content))
            return response
    
def GetClusterName(querytype,resource):
    if querytype == "VOLUME":
        result=json.loads(resource.content)
        if result["records"][0]["cluster"]["name"]:
            return result["records"][0]["cluster"]["name"]
        else :
            print("### Get Cluster Name ###")
            print("[Error] plsea check the response data")
            print(result)
            exit()
            
    elif querytype == "CLUSTER":
        result=json.loads(resource.content)
        if result["records"][0]["name"]:
            return result["records"][0]["name"]
        else:
            print("### Get Cluster Name ###")
            print("[Error] plsea check the response data")
            print(result)
            exit()
    else:
        print("### Get Cluster Name ###")
        print(" you need devolp the "+querytype+" case")
        exit()
    
def ParsingEmsparameters(eventArgs):
    start_index = eventArgs.find("ems-parameters")
    end_index = eventArgs.find("],ems-severity=")
    ems_parameters_str = args.eventArgs[start_index + len("ems-parameters=["):end_index]
    eventArgs=StringToDict(ems_parameters_str)
    return eventArgs

def StringToDict(eventArgs):
    ### 문자열을 쉼표로 분할하고 등호로 다시 분할하여 키와 값의 쌍으로 구성된 튜플 생성
    pairs = [item.split('=') for item in eventArgs.split(',')]
    ### 튜플들을 딕셔너리로 변환
    eventArgs = {key.strip(): value for key, value in pairs}
    return eventArgs


########## main #########

# evntArgs가 이벤트별로 다른 argument를 가집니다.
if args.eventName == "Inodes Full":
    print("### "+args.eventName+" eventArgs ###")
    eventArgs=StringToDict(args.eventArgs)
    print(json.dumps(eventArgs,indent=3))
    print("")
    eventSourceName=args.eventSourceName.split(":") # svm_CVO:/vol3
    resource=GetVolumeResourceInfo(UMAuth["url"],UMAuth["username"],UMAuth["password"],eventArgs["dfMountedOn"],eventSourceName[0])

elif args.eventName == "Inodes Nearly Full":
    print("### "+args.eventName+" eventArgs ###")
    eventArgs=StringToDict(args.eventArgs)
    print(json.dumps(eventArgs,indent=3))
    print("")
    eventSourceName=args.eventSourceName.split(":") # svm_CVO:/vol3
    resource=GetVolumeResourceInfo(UMAuth["url"],UMAuth["username"],UMAuth["password"],eventArgs["dfMountedOn"],eventSourceName[0])

elif args.eventName == "Alert EMS received":
    print("### "+args.eventName+" eventArgs ###")
    eventArgs=ParsingEmsparameters(args.eventArgs)
    # 결과 출력
    print(json.dumps(eventArgs,indent=3))
    resource=GetVolumeResourceInfo(UMAuth["url"],UMAuth["username"],UMAuth["password"],eventArgs["name"],"*",args.eventSourceName)

elif args.eventName == "Error EMS received":
    print("### "+args.eventName+" eventArgs ###")
    eventArgs=ParsingEmsparameters(args.eventArgs)
    # 결과 출력
    print(json.dumps(eventArgs,indent=3))
    resource=GetVolumeResourceInfo(UMAuth["url"],UMAuth["username"],UMAuth["password"],eventArgs["name"],"*",args.eventSourceName)
else:
    print("### "+args.eventName+" eventArgs ###")
    eventArgs=ParsingEmsparameters(args.eventArgs)
    # 결과 출력
    print(json.dumps(eventArgs,indent=3))
    print(args.eventName + "is not defind")
    exit()

## 파일에서 clusterlist 가져오기
# clusterlist = PutClustersInfoList(clusterlist.json)
target_cluster = GetClusterName("VOLUME",resource)
ClusterAuth = GetClusterAuth(target_cluster)
result =IncreaseVolumeInodeValues(args.eventName,eventArgs,ClusterAuth,resource)
print("###")
print(result)

