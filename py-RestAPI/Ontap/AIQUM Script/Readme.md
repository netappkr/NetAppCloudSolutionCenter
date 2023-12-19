# AIQUM Python Script
이 스크립트는 inode full 방지를 위해서 80% 이상 inode 사용 시 60% 로 inode 를 수정하는 스크립트 입니다.
이 스크립트는 예시 입니다. 스크립트는 항상 운영자분이 직접 수정,관리하여야 합니다.
자세한 설명은 [여기](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_wiki/wikis/NetApp_KR_Cloud_KB.wiki/360/AIQUM-Alert-%EB%B0%9C%EC%83%9D-%EC%8B%9C-Script%EA%B0%80-%EC%8B%A4%ED%96%89%EB%90%98%EB%8F%84%EB%A1%9D-%EC%84%A4%EC%A0%95%ED%95%98%EB%A0%A4%EB%A9%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%ED%95%B4%EC%95%BC%ED%95%A9%EB%8B%88%EA%B9%8C)를 참조하세요

## Pre requirement
이 스크립트를 사용하려면 AIQUM 서버에 ```python3``` 와 필수 ```Python package```들이 설치되어 있어야 합니다.
또한 환경변수 항목을 적절한 항목으로 수정하세요.

- python3
### AIQUM이 외부 인터넷이 가능한 경우
아래 명령으로 필수 패키지를 설치 합니다.

```bash
pip install -r requirements.txt
```
### AIQUM에 아래 패키지들을 수동 설치합니다.

```
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import requests
import argparse
import datetime as dt
import json
import base64
import math
from requests.auth import HTTPBasicAuth
```
### Tips 
[인터넷이 안되는곳에서 파이썬 패키지 설치하기! (pip download)](https://stricky.tistory.com/92)


## 스크립트 사용법
1. 스크립트 파일을 열고 환경 변수 항목을 수정합니다.


### 환경변수
UMAuth 와 Clusterlist 항목을 알맞게 수정합니다.
- UMAuth = AIQUM의 접속정보입니다.
- ClusterList = AIQUM에 등록된 클러스터의 접속정보 입니다.

```python
UMAuth = {
    "url": "https://localhost",
    "username": "umadmin",
    "password": "Netapp123!@#"
}
## clusterlist
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
```

2. AIQUM에 스크립트를 등록합니다.
AIQUM에서 스크립트를 등록하는 방법은 [여기](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_wiki/wikis/NetApp_KR_Cloud_KB.wiki/360/AIQUM-Alert-%EB%B0%9C%EC%83%9D-%EC%8B%9C-Script%EA%B0%80-%EC%8B%A4%ED%96%89%EB%90%98%EB%8F%84%EB%A1%9D-%EC%84%A4%EC%A0%95%ED%95%98%EB%A0%A4%EB%A9%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%ED%95%B4%EC%95%BC%ED%95%A9%EB%8B%88%EA%B9%8C)를 참조하세요

3. script를 test 해본 후 적용합니다.

## 스크립트 Test 방법
아래와 같은 옵션을 가지고 있습니다.
AIQUM 서버에 스크립트를 등록하기 전에 아래와 같이 Test 값을 넣어 동작 Test를 해볼 수 있습니다.

```powershell
python .\AIQUM_python_script.py --help
```

```powershell
usage: AIQUM_python_script.py [-h] [-eventID EVENTID] [-eventName EVENTNAME] [-eventSeverity EVENTSEVERITY] [-eventSourceID EVENTSOURCEID] [-eventSourceName EVENTSOURCENAME] [-eventSourceType EVENTSOURCETYPE] [-eventState EVENTSTATE] [-eventArgs EVENTARGS] [-test]

Please refenace Netapp AIQUM doc : https://docs.netapp.com/us-en/active-iq-unified-manager/events/concept_how_scripts_work_with_alerts.html

optional arguments:
  -h, --help            show this help message and exit
  -eventID EVENTID      eventID get the AIQUM
  -eventName EVENTNAME  eventName get the AIQUM
  -eventSeverity EVENTSEVERITY
                        eventSeverity get the AIQUM
  -eventSourceID EVENTSOURCEID
                        eventSourceID get the AIQUM
  -eventSourceName EVENTSOURCENAME
                        eventSourceName get the AIQUM
  -eventSourceType EVENTSOURCETYPE
                        eventSourceType get the AIQUM
  -eventState EVENTSTATE
                        eventState get the AIQUM
  -eventArgs EVENTARGS  eventArgs get the AIQUM
  -test                 eventArgs get the AIQUM
```

위 항목들은 AIQUM에서 전달하는 기본 항목입니다. 각 이벤트 별로 AIQUM에서 eventArgs에 전달하는 항목이 조금씩 다릅니다. 여러 이벤트를 추가하시는 경우 이 전달자에 어떠한 값이 담기는지 확인하세요.

## test input case : Inodes Nearly Full
```
python .\AIQUM_python_script.py -eventID=20189 -eventName='Inodes Nearly Full' -eventSourceType='VOLUME' -eventSourceName='svm_CVO:/vol' -eventArgs='inodesNearlyFull=11,inodesFull=90,dfMountedOn=vol,dfKBytesTotal=99614720,dfKBytesUsed=1164112,dfKBytesPercent=1.168614437705592,dfInodesTotal=3112959,dfInodesUsed=3049559,dfInodesPercent=97.96335255298897'
```
## test input Error EMS recived message
```
python .\AIQUM_python_script.py -eventID='30797' -eventName='Error EMS received' -eventSeverity='warning' -eventSourceID='1' -eventSourceName='CVO' -eventSourceType='CLUSTER' -eventState='NEW' -eventArgs='ems-parameters=[percent_full_blocks=80, percent_full_inodes=90, app=ErrorEMSAlert7, vserver_uuid=924a8797-999a-11ee-a416-15bdde6a2aef, object_type=volume, name=vol2],ems-severity=error'
```

