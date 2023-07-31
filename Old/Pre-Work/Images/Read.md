## Task 1: Cloud Central에 Azure Permission 부여

1.  NetApp Cloud Central에 로그인합니다. (https://cloud.netapp.com) 
 
 2.   Policy_for_Setup_As_Service_Azure.json 파일을 다운 받아  수정합니다. ([Policy_for_Setup_As_Service_Azure.json](https://s3.amazonaws.com/occm-sample-policies/Policy_for_Setup_As_Service_Azure.json))       Policy_for_setup_As_Service_Azure.json 파일의 끝부분에 /subscription/ 다음에 각자 본인의 Azure subscription ID값으로 변경하여 수정하고 저장합니다.
       
```"NotActions": [],
    "AssignableScopes": [
	"/subscriptions/subscription id 기입	"
    ],
    "Description": "Azure SetupAsService",
    "IsCustom": "true"
```
3. 수정한 JSON을 이용해 custom role을 생성하기 위해 azure portal에 접속합니다.

4. Azure portal에서 제공되는 cloud shell에서 해당 JSON 파일을 업로드합니다. 

5. 업로드된 JSON 파일을 통해 custom role을 생성합니다.
  
       az role definition create --role-definition Policy_for_Setup_As_Service_Azure.json

6. Azure에 생성된 Custom Role 확인합니다. 
    - Azure Subscription 을 열고 pay-as-you-go subscription선택
    - pay-as-you-go subscription선택
    - Roles 클릭 
    - Azure SetupAsService Role 확인
    
![enter image description here](https://github.com/sangwonseo/NDX-Lab-Test/blob/master/Cloud%20Central/Azure_setup_service_rol.png?raw=true)
    
7.  NetApp Cloud Central에서 Cloud Manager를 설치할 user에게 role을 할당합니다.
      - Azure내 Subscription 을 열고 pay-as-you-go subscription선택
      - Access control (IAM) 클릭
      - Add를 클릭 후 ‘add role assignment’ 선택 
      - Role : Azure SetupAsService 선택
      - Assign access to : Azure AD user, group, or application 에 Access 할당 
      - Select : 본인의 account 선택

![enter image description here](https://github.com/sangwonseo/NDX-Lab-Test/blob/master/Cloud%20Central/azure_IAM.png?raw=true)
      

## Task 2: Cloud Central에 AWS Permission 부여
       
  1.  AWS Market Place에서 Cloud Volumes ONTAP을 구독합니다. 
       ![enter image description here](https://github.com/sangwonseo/NDX-Lab-Test/blob/master/Cloud%20Central/Marketpalce_AWS.png?raw=true)  

 2.  NetApp Cloud Central policy for AWS 파일을 다운 받아 AWS IAM 콘솔에서 해당 파일을 카피하여 Policy를 생성합니다. ([NetApp Cloud Central policy for AWS](https://s3.amazonaws.com/occm-sample-policies/Policy_for_Setup_As_Service.json))
![enter image description here](https://github.com/sangwonseo/NDX-Lab-Test/blob/master/Cloud%20Central/AWS_IAM_Policy.PNG?raw=true)
  
3. 해당 Policy를 IAM 사용자에게 할당합니다. 
![enter image description here](https://github.com/sangwonseo/NDX-Lab-Test/blob/master/Cloud%20Central/AWS_IAM_User.PNG?raw=true)
