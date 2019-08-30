---


---

<p>이번 Task는 AWS내에 신규 Cloud Volumes ONTAP을 설치 후 Azure내에 기 설치된 Cloud Volumes ONTAP의 데이터를 AWS내의 신규 Cloud Volumes ONTAP으로 SnapMirror을 통해 복제 수행합니다.</p>
<p><strong>사전 준비사항</strong></p>
<ul>
<li><a href="https://github.com/netappkr/NDX_Handsonworkshop-/tree/master/Pre-Work">AWS, Azure 네트워크 사전 구성 및 Permission 부여</a></li>
</ul>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/azuretoaws.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-aws-account-계정-추가">Step 1. AWS Account 계정 추가</h2>
<ol>
<li>Cloud Manager의 오른쪽 상단의 Settings 을 클릭합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/aws_account.PNG?raw=true" alt="enter image description here"><br>
2.  'Cloud Provider &amp; Support Accounts’를 클릭합니다.<br>
3.  '+ Add New Account’를 클릭합니다.<br>
4.  Select Account Type을 AWS로 선택합니다.<br>
5.  아래와 같이 본인의 Access Key, Secrete Key 값을 입력합니다.</p>
<pre><code> * Cloud Provider Profile Name:  AWS key 
 * AWS Access Key: xxxxxxxxxxxxxxxxxx
 * AWS Secret Key: xxxxxxxxxxxxxxx
</code></pre>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/aws_key.PNG?raw=true" alt="enter image description here"></p>
<h2 id="step-2.-aws에-cloud-volumes-ontap-설치">Step 2. AWS에 Cloud Volumes ONTAP 설치</h2>
<ol>
<li>
<p>Cloud Manager 내의 Working Environments에서 ‘create Cloud Volumes ONTAP’을 클릭합니다.</p>
</li>
<li>
<p>Cloud Provider와 Type을 선택합니다.</p>
<ul>
<li>Select Provider : Amazon Web Services</li>
<li>Select Type : Cloud Volume ONTAP</li>
</ul>
</li>
<li>
<p>details &amp; credentials에서 아래와 같이 입력하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Working Environment Name : SLNAcovm2-number(예&gt;SLNAcovm1111) <strong>특수문자 기입불가</strong></li>
<li>Resource Group Name : Use Default 선택</li>
<li>Password : Netapp123</li>
</ul>
</li>
<li>
<p>Location &amp; Connectivity는 아래와 같이 입력 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Azure Region : Asia Pacific | Seoul</li>
<li>VPC : NetApp_Lab</li>
<li>Subnet : student-number-subnet-aws</li>
<li>Security group : Use a generated security group 선택</li>
</ul>
</li>
<li>
<p>Cloud Volumes ONTAP License에 ‘BYOL’를 선택하고 ‘Continue’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>오른쪽 상단의 ‘create my own configuration’을 클릭합니다.</p>
</li>
<li>
<p>아래와 같이 선택 후 ‘continue’ 버튼을 클릭합니다.</p>
<ul>
<li>License : Cloud Volumes ONTAP Explore</li>
<li>VM type: m5.xlarge</li>
</ul>
</li>
<li>
<p>Underlying Storage Resources는 아래와 같이 선택하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Throughput Optimized HDD (ST1)</li>
<li>AWs Disk Size : 500GB</li>
</ul>
</li>
<li>
<p>Write Speed &amp; WORM은 아래와 같이 선택 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Write Speed : Normal</li>
<li>WORM : Disable WORM</li>
</ul>
</li>
<li>
<p>create volume 화면에서는 ‘skip’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>최종 구성 정보를 확인 후 체크 박스를 모두 선택하고 ‘Go’ 버튼을 클릭합니다.</p>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/AWS_CVO.PNG?raw=true" alt="enter image description here"></p>
<h2 id="step-3.-azure-cvo에서-aws-cvo로-복제-수행">Step 3. Azure CVO에서 AWS CVO로 복제 수행</h2>
<ol>
<li>
<p>Cloud Manager의  working environment에서  AzureCVO ONTAP에서 AWS CVO로 Drag &amp; Drop합니다.</p>
</li>
<li>
<p>replication setup 창이 나타나면 복제할 소스 볼륨인 content_copy 볼륨을 클릭합니다.</p>
</li>
<li>
<p>아래와 같이 설정 후 ‘continue’ 버튼을 클릭한합니다.</p>
<ul>
<li>Destination Volume Name : content_copy_aws</li>
<li>Destination disk type : Throughput Optimized HDD (ST1)</li>
</ul>
</li>
<li>
<p>Max Transfer Rate는 100MB/s으로 설정 후 ‘continue’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>Replication Policy에 Mirror를 선택합니다.</p>
</li>
<li>
<p>Schedule은 one-time copy를 선택합니다.</p>
</li>
<li>
<p>최종 구성 리뷰 후 체크 박스 활성화하고 ‘GO’버튼을 클릭합니다.</p>
</li>
<li>
<p>Working Environment에서 replication 구성이 되었음을 확인합니다.</p>
</li>
<li>
<p>Replication status에서 Replication 완료 상태를 확인합니다.</p>
<ul>
<li>Status : idle 확인(transferring 상태라면 조금 더 기다린 후 확인)</li>
<li>Mirror State : snapmirrored 확인</li>
</ul>
</li>
<li>
<p>replication status에서 content_copy 볼륨의 왼쪽에 마우스를 가져가면 나타나는 메뉴에서 ‘break’ 버튼을 클릭합니다.</p>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/break_replication.png?raw=true" alt="enter image description here"></p>
<ol start="12">
<li>
<p>target 볼륨인 content_copy_aws 볼륨은 마운트가 불가능한 상태입니다. 마운트가 가능하도록 설정하기 위해 ‘Edit’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>아래와 같이 설정 후 ‘update’ 버튼을 클릭합니다.</p>
<ul>
<li>Custom export policy : 해당 VPC subnet의 IP range</li>
</ul>
</li>
<li>
<p>content_copy_aws 볼륨의 ‘mount command’를 클릭합니다.</p>
</li>
<li>
<p>Mount command를 copy합니다.</p>
</li>
<li>
<p>해당 VPC내에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</p>
<pre><code> mkdir /mnt/content_copy_aws
 mount 10.1.3.7:/_copy_aws /mnt/content_copy_aws
</code></pre>
</li>
<li>
<p>볼륨에 대한 Write된 파일들을  확인합니다.</p>
<pre><code>  cd /mnt/content_copy_aws
  ls -al
</code></pre>
</li>
</ol>

