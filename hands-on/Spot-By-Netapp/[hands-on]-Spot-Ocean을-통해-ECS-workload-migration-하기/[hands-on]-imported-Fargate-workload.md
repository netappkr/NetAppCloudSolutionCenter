AWS Fargate 서비스는 task를 ec2 node에 할당하는것이 아닌 aws 관리영역에 할당합니다.
이를 통해 사용자들은 node의 자원 사용률 및 상태를 모니터링 및 관리할 필요가 없어지는 효과가 있습니다 만
이로 인해 발생하는 제약조건과 상응하는 서비스 이용료를 지불해야 합니다.

오션에서 제공하는 migration 기능을 통해 자동으로 Fargate task를 ocean for ecs 클러스터에 할당합니다.

https://docs.spot.io/api/#operation/oceanEcsFargateGetMigrationStatus

1. spot ocean 콘솔 > action > imaport Fargate Services로 이동합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-214331f8-9d15-46ba-a177-013b46c3fad9.png)

2. migration 할 fargate task를 선택합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-a4bcda1e-86dc-4bc8-8dc3-51492d5f7029.png)

3. task 정보를 수집하여 migration을 진행합니다.
![image.png](https://dev.azure.com/sangwon0200/NetApp_KR_Cloud_KB/_git/NetApp_KR_Cloud_KB.wiki?path=/.attachments/image-93c37877-0cdc-43dd-9f7e-75f285a09bbf.png)