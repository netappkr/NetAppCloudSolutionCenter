# python으로 Spot api 질의
로그 받아오거나 특정 데이터를 반복적으로 받아오려고 할 때 너무 피로도가 큽니다.</br>
로그 분석 관련 python 스크립트를 만들어 배포합니다.</br>
개인적으로 생성한 스크립트이기 때문에 필요하신 부분은 수정하여 사용하시기 바랍니다.</br>

# 이용방법
1. 필요한 파이선 패키지 설치

```bash
$ pip install -r requirements.txt
```

2. 아래와 같이 명령
```bash
python get-spot-eg-log.py -gid <group id> -aid <account id> -token <Bear token> -fromDay <%Y-%m-%d> -toDay %Y-%m-%d -level ALL
```

```bash
python get-spot-eg-log.py --help
usage: get-spot-eg-log.py [-h] [-gid GROUP_ID] [-aid ACCOUNT_ID] [-token TOKEN] [-fromDay FROMDAY] [-toDay TODAY] [-level LEVEL]

eg group-id,token,fromData,toData,severity 입력 자세한 내용은 spot api 문서에 eg 로그 조회 참조

options:
  -h, --help            show this help message and exit
  -gid GROUP_ID, --group-id GROUP_ID
                        Elastigroup id
  -aid ACCOUNT_ID, --account-id ACCOUNT_ID
                        Account id
  -token TOKEN, --token TOKEN
                        bear token
  -fromDay FROMDAY, --fromDay FROMDAY
                        startDay 'yyyy-mm-dd' example 2023-03-14
  -toDay TODAY, --toDay TODAY
                        endDay 'yyyy-mm-dd' example 2023-03-14
  -level LEVEL, --level LEVEL
                        severity default is ALL / you can only insert ALl,INFO,DEBUG,ERROR
```
### 명령어 예시
```
PS Netapp\NetappKR Github\NetappkrGit\py-RestAPI> python get-spot-eg-log.py -gid sig-623baeb2 -aid act-c2b5eb8b -token 000000000000000000000000000000000000000 -fromDay 2023-03-14 -toDay 2023-03-15 -level INFO
response code:200
```

## 결과
<egid>_<fromDay>_<toDay>.json 파일이 생성됩니다. </br>
![example](./Images/example.png)

## 추가 스크립트 
## Json 파일 CSV로 변환

1. 단순 변환
Pandas 로 단순변환
디렉토리내에 떨어진 EG log를 CSV형식으로 변환합니다.

### 사용방법
```
python json_to_csv.py
```

2. 인스턴스 LifeTime 추출
디렉토리내에 모든 json파일들을 읽어서 결과를 xlsx 파일로 변환합니다.

### 사용방법
```
python spot_inst_lifetime.py
```

# 참고
- [elastigroup Aws Get Logs](https://docs.spot.io/api/#tag/Elastigroup-AWS/operation/elastigroupAwsGetLogs )
