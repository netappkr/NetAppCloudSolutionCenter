# BlueXP API 사용을 위한 인증절차
BlueXP는 API를 통한 제어가 가능합니다. 인증에 JWT Token을 사용합니다.
특히 ```Terraform```이나 ```Ansible```을 통한 IaC 활용 시에도 필요합니다.

## Service Account 생성
1. NetApp Cloud Central에 로그인 후 [BlueXP web console](https://cloudmanager.netapp.com/)에 접속합니다.
2. ```Account``` > ```Manage Account```</br>
![Alt text](./Images/Readme-0.png.png)
3. ```Members``` Tab</br>
![Alt text](./Images/Readme-1.png.png)
4. ```Create Service Account```</br>
![Alt text](./Images/Readme-2.png.png)
5. ```sa_client_id```, ```sa_secret_key```를 복사한 후 ```Notepad```을 열고 ```BlueXP_Auth.tfvars``` 파일을 생성합니다.
cloudmanager_sa_secret_key = "복사한 sa_secret_key"
cloudmanager_sa_client_id = "복사한 sa_client_id"

외부에 id와 key 값이 유출되지 않도록 관리해야 합니다.

## Refresh Token 생성
NetApp Cloud Central에 로그인 후 여기서 [refresh_token](https://services.cloud.netapp.com/refresh-token)을 생성합니다.


# 참조
- [JWT 토큰 인증 이란? (쿠키 vs 세션 vs 토큰)](https://inpa.tistory.com/entry/WEB-%F0%9F%93%9A-JWTjson-web-token-%EB%9E%80-%F0%9F%92%AF-%EC%A0%95%EB%A6%AC)