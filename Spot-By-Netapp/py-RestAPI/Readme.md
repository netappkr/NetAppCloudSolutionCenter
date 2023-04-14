# python으로 api 질의
로그 받아오거나 특정 데이터를 반복적으로 받아로려고 할 때 너무 피로도가 큽니다.

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
python get-spot-eg-log.py --hlep
usage: get-spot-eg-log.py [-h] [-gid GROUP_ID] [-aid ACCOUNT_ID] [-token TOKEN] [-fromDay FROMDAY] [-toDay TODAY] [-level LEVEL]
get-spot-eg-log.py: error: unrecognized arguments: --hlep
```
## 예시
```
PS Netapp\NetappKR Github\NetappkrGit\py-RestAPI> python get-spot-eg-log.py -gid sig-623baeb2 -aid act-c2b5eb8b -token 000000000000000000000000000000000000000 -fromDay 2023-03-14 -toDay 2023-03-15 -level ALL
response code:200
```

## 결과
<egid>_<fromDay>_<toDay>.json 파일이 생성됨


