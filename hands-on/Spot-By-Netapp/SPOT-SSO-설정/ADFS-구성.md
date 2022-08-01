#구성
---
## ADFS 구성
- 디렉토리 wyahn.com
- ADDS 서버에 ADFS 서버를 기능추가 합니다.
- IIS 와 ADFS를 server role에 활성화 한 후 진행
##[ 구성도 ]
### 전체 구성도
![image.png](/.attachments/image-d70f6af7-6bab-4301-9734-66c2b9d2ee2a.png)
### DNS 레코드 조회
![image.png](/.attachments/image-54b739e4-4e1e-4354-9d07-78fa41871e05.png)
---
# 구성 절차
1. 서버역활 추가
![image.png](/.attachments/image-808fb75d-df90-4b3b-a3bf-94ad11c939d4.png)
2. ADFS 설정
![image.png](/.attachments/image-a951871b-b40b-447e-a85b-7c22581a6201.png)
![image.png](/.attachments/image-22a16948-95ef-4a62-acd4-79e0839e9ae0.png)
3. 서버 인증서 추가 ( 도메인발급 )
![image.png](/.attachments/image-0c9c437c-b53a-49b2-aff3-469c1e6f33b5.png)
4. 관리자 계정 지정
![image.png](/.attachments/image-0c8849c1-ea08-4ceb-9d9a-2b0d5c2705cd.png)
5. 구성완료
![image.png](/.attachments/image-9a118bc4-22b4-41f6-aab8-4e06af0abbb5.png)
![image.png](/.attachments/image-3b9852fa-6758-4249-9e4c-7f6420d79df4.png)
6. ADDS 내부 DNS 서버 설정
![image.png](/.attachments/image-9a6cea1b-39f3-4d6c-bdeb-ae0cdf3731bf.png)
7. FS 테스트페이지 접속 활성화
![image.png](/.attachments/image-6bff1a8e-bb13-4324-8972-2983b003ef1f.png)
8. ADFS 로그인 test 페이지
- https://<adfsname.domain.com>/adfs/ls/IdpInitiatedSignon.aspx
![image.png](/.attachments/image-248af552-9f94-451f-ad0e-2ca277f180ec.png)
9. 로그인 응답값 확인
 - AD 계정을 이용
#참고
---
[ ADFS 구성절차 참조 ](https://blog.limcm.kr/73)
[ ADFS 테스트 페이지 활성화](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-initiatedsignon)
[ AD FS 2016 요구 사항](https://docs.microsoft.com/en-us/windows-server/identity/ad-fs/overview/ad-fs-requirements)
[ 윈도우 10 인증서 발급 절차 - Let's Encrypt! ](https://blog.itcode.dev/posts/2021/08/19/lets-encrypt)