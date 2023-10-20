# 사전 요구사항
이 섹션에서는 BlueXP 및 Cloud Volumes ONTAP 배포 전에 이해하고 해결해야 하는 주요 설계 고려 사항을 강조합니다.

## NetApp BlueXP 계정 생성
NetApp BlueXP 계정이 필요합니다.</br>
계정이 없는 경우 BlueXP 계정을 생성합니다.

1. [BluxXP](https://bluexp.netapp.com/)에 접속 합니다.
2. 오른쪽 상단의 ```Get Started``` 를 눌러 로그인 화면으로 넘어갑니다.
로그인되어 있는 상태라면 ID/PW를 물어보는 화면이 나오지 않습니다.
3. 로그인 화면 하단 ```Sign up``` 을 클릭합니다.
<img src=./Images/image.png alt="Girl in a jacket" width="500">
4. 필요항목을 넣고 회원가입하여 계정을 생성합니다.
<img src=./Images/image-1.png alt="Girl in a jacket" width="500">


## AWS 구독 
AWS에서 Cloud Volumes ONTAP 배포를 시작하기 전에 활성 AWS 구독이 있어야 합니다.AWS를 구독하고 있지 않다면 여기에서 계정을 등록하세요. 
이 계정은 무료 등급에 있어서는 안 되므로 PAYGO 계정을 권장합니다.

### AWS Marketplace Subscription
BlueXP Console에서 Cloud Volumes ONTAP을 배포하려면 사용자가 AWS Marketplace 내에서 Cloud Volumes ONTAP을 구독해야 합니다. 이 단계는 AWS EULA 약관을 수락하고 확인하기 위해 한 번만 필요합니다.

1. 인터넷 브라우저를 통해 AWS 관리 콘솔에 로그인합니다.
2. [AWS Marketplace](https://aws.amazon.com/marketplace/search/results?page=1&searchTerms=netapp+cloud+volumes+ontap) (동일한 세션 자격 증명을 공유하는 동일한 브라우저) 에서 NetApp Cloud Volumes ONTAP 솔루션을 방문하십시오 . "AWS용 Cloud Volumes ONTAP"(정확한 이름)을 선택합니다.
![AWS Marketplace 1](./Images/Screenshot%2030.bmp)

3. 상단의 '구독 계속'을 클릭하세요.
![AWS Marketplace 2](./Images/Screenshot%2031.bmp)

4. "약관 동의"를 클릭하세요.
![AWS Marketplace 3](./Images/Screenshot%2032.bmp)

5. 구독 확인을 확인하고 브라우저 탭/창을 닫습니다. 
![AWS Marketplace 4](./Images/Screenshot%2033.bmp)

# 참조
- [step by step guide to setting up cloud volumes ontap on aws](https://bluexp.netapp.com/blog/a-step-by-step-guide-to-setting-up-cloud-volumes-ontap-on-aws)



