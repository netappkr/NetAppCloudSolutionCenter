# ADFS SAML 인증 설정
_A사용자 로그인 시 SSO 동작 과정 설명_
먼저 ADFS의 주요 항목 및 용어에 대해 이해합니다.
[Understanding Key AD FS Concepts](https://docs.microsoft.com/ko-kr/windows-server/identity/ad-fs/technical-reference/understanding-key-ad-fs-concepts)

![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-c71c96e1-db88-4662-9186-d92d113008fe.png)
#전제 조건
- Spot 계정 및 계정의 관리자 권한
- ADFS 역할이 설치된 도메인 구성원 Windows Server 2012R2/2016
#1단계: 신뢰 당사자 트러스트 마법사 추가
1. ADFS(Active Directory Federation Services) 관리 콘솔을 엽니다.
2. 신뢰 당사자 트러스트를 마우스 오른쪽 단추로 클릭하고 신뢰 당사자 트러스트 추가를 클릭합니다.
<IMG  src="https://docs.spot.io/administration/_media/adfs-saml-01.png"/>
3. 클레임 인식을 선택하고 시작을 클릭합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-693b9849-b8ff-4a29-b5a1-f294fcfb99a2.png)
'Enter data about the relying party manually' 선택하고 다음을 클릭합니다.

4. RP의 이름을 선택하고 다음을 클릭합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-3ec16258-cd2b-4a81-9a77-d836afdb6912.png)
5. 인증서를 요청하면 다음을 클릭합니다.
( 클레임값 암호화 할 키(인증서)를 넣을것인지 묻습니다만 test에서는 구성하지 않습니다.)
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-6c638d0e-ecb5-439c-8b4b-4e12f33e53d2.png)

6. "Enable support for the SAML 2.0 WebSSO protocol"을 선택하고 URL을 입력합니다. 
https://console.spotinst.com/auth/saml
(이 url은 인증처리 완료 시 브로커(ADFS)가 처리결과를 보고 할 주소 입력란 입니다.)
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-ed7b200b-a9ce-4bb2-9109-87582d7bfb30.png)


7. RPID(신뢰 당사자 ID)와 동일한 URL을 추가합니다.
_대부분 주소를 동일하게 구성합니다._
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-30ec2941-9bae-42a5-b02a-f05fe8c1a8ad.png)
8. 다음을 클릭한 후 마침을 클릭하여 마법사를 완료합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-84aafc0a-0731-48d9-af46-1a70216ceaaa.png)
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-b7128909-bf22-460a-909b-031d1a37f821.png)

# 클레임 규칙 구성
1. 클레임 규칙을 구성할 수 있는 새 마법사를 엽니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-3ab1d55b-450f-40d9-a83c-87712bf967e2.png)
2. 규칙 유형을 묻는 메시지가 나타나면 다음을 클릭합니다.
3. 클레임 규칙의 이름을 입력하고 Active Directory를 속성 저장소로 선택합니다.
다음 속성 매핑을 입력합니다.

| LDAP 속성 | 나가는 CLAIM |
|--|--|
| E-Mail-Address | Email |
| Given-Name | FirstName |
| Surname | LastName |
		
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-ee29aea9-dd44-4c06-9636-9e889625a2fc.png)
```
[TIP]
 클레임값 mapping을 통해 AD 계정이 사용할 spot 계정을 구분합니다.
 일반적으로 로그인시 문제가 있다면 클레임값이 불일치 하는 경우가 많습니다.
 이러한 문제에 대해 트러블슈팅이 필요한 경우 Saml tracer라는 tool 사용을 추천합니다.
```
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-22868aec-f316-4996-8f38-73c24d01fe99.png)

4. 마침을 클릭하여 마법사를 완료합니다.

# 2단계: 메타데이터 가져오기 및 삽입
1. ADFS 메타데이터 xml 파일을 다운로드합니다.
[메타데이터에 대한 내용](https://docs.microsoft.com/ko-kr/windows-server/identity/ad-fs/troubleshooting/ad-fs-tshoot-endpoints)
```
https:://<adfs_domain>/federationmetadata/2007-06/federationmetadata.xml
```
https://fs.wyahn.com/FederationMetadata/2007-06/FederationMetadata.xml

2. 편집을 위해 XML 파일을 엽니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-3c24424a-c44a-476d-9782-d31064aecb70.png)

3. 시작태그와 마침태그 모두 `ds:X509Certificate` 로 변경합니다.
x509Certificat >> ds:X509Certificate
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-89a94d47-870c-421f-9a40-27c201ef2681.png)

```
아직 XML 항목에 어떤것들이 있는지 정확히 이해하지 못했습니다. ( 공부를 다하는데로 추후 업데이트 하겠습니다.)
```
4. 스팟 계정에 관리자로 로그인합니다.
- 반드시 관리자 계정으로 등록된 이메일이 AD 사용자에 등록된 메일이여야 합니다.
```
<예시> 
- spot 사용자로 등록한 이메일 : Wooyeoung.Ahn@netapp.com
- AD 사용자 상세정보 이메일 항목 : Wooyeoung.Ahn@netapp.com
```
5. 화면 오른쪽 상단의 사용자 아이콘을 클릭하고 설정을 클릭합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-e826f6ef-e5e0-4f38-9735-02747bb31241.png)

6. 보안 탭을 클릭한 다음 ID 제공자를 선택하십시오.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-d36ee542-634d-4d13-9a86-476b081ab88d.png)

7. 찾아보기를 클릭하고 메타데이터 파일을 선택한 다음 저장을 클릭합니다.

# 로그인 test
1. AD에 user를 추가합니다.
   - 약속한 클레임 값을 반드시 채워주세요.
     E-Mail-Address	Email
     Given-Name	FirstName
     Surname	LastName
     ![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-8c08e80e-38be-47bf-871a-cd6c8c19f8ac.png)
2. OU 레벨 계정생성
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-6194c407-1fcc-4715-8c46-ccf11aa27511.png)
3. 하단 SSO 로그인 선택 > 이메일 입력
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-3a915083-e95f-49c5-bbad-2946a89ed028.png)

---
# 추가구성( 옵션 )
# 3단계: IDP 시작 SSP 구성
IDP에서 SSO를 구성하려면 다음과 같이 추가 설정을 구성해야 합니다.

1. 스팟 계정에 관리자로 로그인합니다.
2. 화면 오른쪽 상단의 사용자 아이콘을 클릭하고 설정을 클릭합니다.
3. 보안 탭을 클릭한 다음 ID 제공자를 선택하십시오.
4. 릴레이 값을 복사합니다. ( 릴레이값은 유출되면 피곤합니다.)
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-abcae635-8989-44c3-9c4f-a6f7ec80216e.png)
5. ADFS 서버에 연결합니다.
6. 관리 권한으로 Powershell을 엽니다.
7. 다음 명령을 실행하여 IDP 시작 SSO를 활성화합니다. 
   ```PowerShell
   Set-ADFSProperties -EnableIdPInitiatedSignonPage $true
   ```
   - Windows Server 2016에서 실행 중인 경우 다음 명령을 실행하여 릴레이 상태를 활성화합니다.
      ```
      Set-ADFSProperties -EnableRelayStateForIDPInitiatedSignon $true
      ```
      > [옵션설명- MS Doc](https://docs.microsoft.com/en-us/powershell/module/adfs/set-adfsproperties?view=windowsserver2022-ps)
      > -EnableRelayStateForIdpInitiatedSignOn
      >
      >IDP(배포 지점) 시작 로그온을 위한 릴레이 상태가 활성화되어 있음을 나타냅니다.
      >유형:	부울
      >위치:	명명 된
      >기본값:	없음
      >파이프라인 입력 수락:	거짓
      >와일드카드 문자 허용:	거짓

   - Windows Server 2012R2에서 실행 중인 경우: 
     - 편집을 위해 다음 파일을 엽니다. 
      ```
      %systemroot%\ADFS\Microsoft.IdentityServer.Servicehost.exe.config
      ```
     - `<microsoft.identityserver.web>` 행을 찾습니다.
     - `<microsoft.identityserver.web>` 항목 바로 뒤에 다음 행을 추가합니다. `<useRelayStateForIdpInitiatedSignOn enabled="true" />`

8. Active Directory Federation Services 서비스를 재시작 합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-d3ecdee9-0204-4814-b4fd-cb6dae139243.png)

# IDP SSO URL 생성
[ADFS relay state 생성기](http://jackstromberg.com/adfs-relay-state-generator/)
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-a7640499-7ae7-451f-b994-834656479b93.png)

[ 필요 항목 설명 ]
- RPM
  - 이 값은 신뢰 당사자 식별자입니다.( ex> https://fs.wyahn.com/auth/saml)
  - 이 값은 인코딩되어야 합니다.
- 중첩된 릴레이 상태
  - 이 값은 RelayState로 신뢰 당사자에게 전달됩니다.
  - 이 값은 인코딩되어야 합니다.
- URL 쿼리는 두 부분으로 구성됩니다. 
주어진 매개변수를 기반으로 URL을 인코딩하고 생성하는 RelayState Generator입니다. 
다음을 삽입하기만 하면 됩니다.
  - IDP URL: https:///adfs/ls/idpinitiatedsignon.aspx
  - RP URL: https://console.spotinst.com/auth/saml
  - 4단계에서 복사한 릴레이 상태

##임시 토큰 생성

임시 토큰을 생성할 때 사용자 자격 증명은 IDP에서 확인됩니다.

임시 토큰을 생성하려면 IDP에서 생성된 SAML 어설션을 제공합니다. 
ADFS에서 SAML 어설션을 가져오려면 다음 지침 을 따르세요 .
다음 요청을 실행합니다. 
'<>'를 일반 XML 본문(json 래퍼 없음)으로 SAML 어설션 응답으로 바꿉니다.
```
curl -X POST -H "Content-Type: application/xml" -d
'<SAML_assertion_response_XML>' https://oauth.spotinst.io/samlToken?organizationId=<organization_id>
```