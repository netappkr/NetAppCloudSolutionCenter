---


---

<p>이번 Task에서는 NetApp Cloud Central을 통해 Data Broker를 AWS에서 설치 후 온프레미스내의 NFS 데이터를 AWS S3로 마이그레이션을 수행합니다.</p>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cloudsync.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-data-broker-설치">Step 1. Data Broker 설치</h2>
<ol>
<li>
<p>Log in 후 Products 클릭하여 Cloud Sync 메뉴를 클릭합니다.</p>
</li>
<li>
<p>Cloud Sync 는 다양한 Source와 Target 구성이 가능합니다. 이번 실습은 On-premise에 있는 NAS 스토리지에서 AWS S3 스토리지로 데이터 동기화를 수행하는 것이므로 Source 영역에 NFS Server 아이콘을  Drag &amp; Drop 합니다.</p>
</li>
<li>
<p>AWS S3를 Target으로 Drag &amp; Drop 합니다.</p>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cloudsync_aws_s3.PNG?raw=true" alt="enter image description here"></p>
<ol start="4">
<li>
<p>하단의 Continue 버튼을 클릭합니다.</p>
</li>
<li>
<p>How It Works 를 통해 구성 Summary를 확인한 후 ‘Continue’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>NFS Source의 Data Network IP를 지정후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>NFS Source Data IP : xx.xx.xx.xx</li>
</ul>
</li>
<li>
<p>Data copy를 중계하는 Data Broker를 AWS로 선택후 클릭합니다.</p>
</li>
<li>
<p>AWS Cloud Formation을 위해  AWS Account ID와 username을 통해 접속합니다.</p>
<ul>
<li>AWS Account ID : 286603580557</li>
<li>IAM user name : student-number</li>
<li>Password: *******</li>
</ul>
</li>
<li>
<p>Create stack 단계에서 'Next’를 클릭합니다.</p>
</li>
<li>
<p>Specify stack details 단계에서 아래와 같이 설정 후 'Next’를 클릭합니다.</p>
<ul>
<li>Which VPC should this be deployed to? :  Seoul-Vpc-</li>
<li>Which subnet should this be deployed to? : Seoul-Vpc-Subnet-</li>
<li>EC2 KeyPair : NDX</li>
<li>Assign a public IP address? : True</li>
</ul>
</li>
<li>
<p>Configure stack options 단계에서 'Next’를 클릭합니다.</p>
</li>
<li>
<p>Review databroker-aws 단계에서 최종 리뷰 후 'Create Stack’을 클릭합니다.</p>
</li>
<li>
<p>설치 완료 후 열려 있는 Cloud Sync GUI에서 등록된 Data Broker가 활성화된 것을 확인한 후 ‘Continue’ 메뉴를 클릭합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/aws_databroker.PNG?raw=true" alt="enter image description here"></p>
</li>
</ol>
<h2 id="step-2.-sync-relationship-생성">Step 2. Sync Relationship 생성</h2>
<ol>
<li>
<p>실습을 위해 생성해 놓은 On-premise의 source NFS Volume 내부에 클라우드로 동기화하고자 하는 디렉토리를 선택 후 ‘Continue’ 메뉴를 클릭합니다. 이 때, 자동으로 volume 정보를 discovery하지 못하는 경우 Add Export Manually 메뉴 클릭하여 수동으로 입력해 주면 됩니다.</p>
</li>
<li>
<p>Target으로 사용할 S3 Bucket을 선택합니다. 만약 사용할 Bucket이 없다면 Add to the list를 클릭해서 새로운 Bucket을 생성합니다.</p>
</li>
<li>
<p>S3 Bucket 구성은 아래와 같이 설정 후 ‘Continue’ 메뉴를 클릭합니다.</p>
<ul>
<li>S3 Bucket Encryption : True</li>
<li>S3 Storage Class: Standard</li>
</ul>
</li>
<li>
<p>Sync Relationship Settings은 아래와 같이 설정 후 ‘Continue’ 메뉴를 클릭합니다.</p>
<ul>
<li>Recently Modified Files :  Recently Modified Files</li>
<li>Delete Files On Target: Never delete files from the target location</li>
<li>Retries: Retry 3 times before skipping file</li>
<li>File Types:  Include All</li>
<li>Exclude File Extensions: None</li>
<li>File Size: All</li>
</ul>
</li>
<li>
<p>Relationship Tag가 필요 시 기입 후 ‘Continue’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>Relationship 100% 완료되면 'View In Dashboard’를 클릭합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/ghost_relationship.PNG?raw=true" alt="enter image description here"></p>
</li>
</ol>
<h2 id="step-3.-data-복제-수행">Step 3. Data 복제 수행</h2>
<ol>
<li>
<p>Sync Relationship GUI에서 1개의 Relationship가 생성 되었음을 확인합니다.</p>
</li>
<li>
<p>해당 Relationship 박스 상단을 클릭하여 Sync Now 를 실행합니다.</p>
</li>
<li>
<p>Sync가 성공적으로 완료 후 Sync Relationship GUI에서 복제 성공 여부 및 복제된 디렉토리 및 파일 수를 확인합니다.</p>
</li>
<li>
<p>AWS S3 웹 GUI에서 Target Bucket에 파일들이 복제 되었는지를 확인합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/s3bucket.PNG?raw=true" alt="enter image description here"></p>
</li>
</ol>

