---


---

<p>이번 Task는 NetApp Cloud Central에서 Cloud Manager 및 Cloud Volume ONTAP을 Azure 내에 설치 후 온프레미스 내의 ONTAP의 데이터를 NetApp 복제 솔루션인 SnapMirror을 통해 Azure내의 Cloud Volumes ONTAP으로 복제합니다.</p>
<p><strong>사전 준비사항</strong></p>
<ul>
<li><a href="https://github.com/netappkr/NDX_Handsonworkshop-/tree/master/Pre-Work">AWS, Azure 네트워크 사전 구성 및 Permission 부여</a></li>
</ul>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/diagram_onpremtoazure.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-azure에-cloud-manager-설치">Step 1. Azure에 Cloud Manager 설치</h2>
<ol>
<li>
<p>NetApp Cloud Central의 Cloud Volumes ONTAP  아래 'create cloud manager’을 클릭합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cloudmanagergui.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>Cloud Manager가 설치될 Cloud로 ‘Azure’를 선택합니다.</p>
</li>
<li>
<p>Virtual Machine Authentication을 다음과 같이 입력하고 ‘Continue’ 버튼을 누릅니다.</p>
<ul>
<li>Cloud Manager VM Name : OCCM-student</li>
<li>User Name : netapp</li>
<li>Authentication Method : Password</li>
<li>Password : Netapp123!@#</li>
</ul>
</li>
<li>
<p>Basic Settings을 다음과 같이 입력하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Subscription : Azure Pass - Sponsorship</li>
<li>Region : Korea Central</li>
<li>Resource Group : Use an existing group 선택</li>
<li>student</li>
</ul>
</li>
<li>
<p>Network을 다음과 같이 입력하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Vnet : NetApp_LAB</li>
<li>Subnet : student-number-subnet</li>
<li>Public IP : Enable</li>
</ul>
</li>
<li>
<p>Security Group을 다음과 같이 입력하고 ‘Go’ 버튼을 클릭합니다.</p>
<ul>
<li>Assign a Security group : Create a new security group 선택</li>
<li>HTTP / HTTPS / SSH : Anywhere 선택</li>
</ul>
</li>
<li>
<p>Cloud Manager의 설치가 진행됩니다. (약 7분 소요) 진행중에 창을 닫지 않도록 주의합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cm_install.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>정상적으로 설치되면 아래와 같은 Cloud Manager 창이 나타납니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cm_done.png?raw=true" alt="cm_done.png"></p>
</li>
</ol>
<h2 id="step-2.-azure에-cloud-volumes-ontap-설치">Step 2. Azure에 Cloud Volumes ONTAP 설치</h2>
<ol>
<li>
<p>Cloud Manager 내의 Working Environments에서 ‘create Cloud Volumes ONTAP’을 클릭합니다.</p>
</li>
<li>
<p>Cloud Provider와 Type을 선택합니다.</p>
<ul>
<li>Select Provider : Microsoft Azure</li>
<li>Select Type : Cloud Volume ONTAP</li>
</ul>
</li>
<li>
<p>details &amp; credentials에서 아래와 같이 입력하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Working Environment Name : AzureCVO</li>
<li>Resource Group Name : Use Default 선택</li>
<li>Password : Netapp123!@#</li>
</ul>
</li>
<li>
<p>Location &amp; Connectivity는 아래와 같이 입력 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Azure Region : Korea Central</li>
<li>VNet : NetApp_LAB</li>
<li>Subnet : student0-number-subnet</li>
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
<p>아래와 같이 선택 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>License : Cloud Volumes ONTAP Standard</li>
<li>VM type: Standard_DS4_v2</li>
</ul>
</li>
<li>
<p>Underlying Storage Resources는 아래와 같이 선택하고 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Standard HDD</li>
<li>Azure Disk Size : 500GB</li>
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
<p>최종 구성 정보를 확인 후 체크 박스를 모두 선택하고 ‘Go’ 버튼을 클릭합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/cvo_azure_check.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>Cloud Volumes ONTAP 설치가  진행됩니다. (<strong>약 25분 소요</strong>)</p>
</li>
</ol>
<h2 id="step-3.-on-prem내의-ontap에서-azure-cvo로-복제-수행">Step 3. On-Prem내의 ONTAP에서 Azure CVO로 복제 수행</h2>
<ol>
<li>
<p>Cloud Manager 내의 Working Environments에서 ‘Discover’를 클릭합니다.</p>
</li>
<li>
<p>ONTAP을 선택합니다.</p>
</li>
<li>
<p>아래 ONTAP 정보를 아래와 같이 입력하고  ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Cluster management IP : xx.xx.xx.xx</li>
<li>User name: admin</li>
<li>Password : Netapp123!</li>
</ul>
</li>
<li>
<p>등록된 On-Prem ONTAP의 Volumes Tab에서 사전에 생성된 볼륨들을 확인합니다.</p>
</li>
<li>
<p>Cloud Manager의  working environment에서 On-Prem ONTAP을 AzureCVO로 Drag &amp; Drop합니다.</p>
</li>
<li>
<p>replication setup 창이 나타나면 복제할 소스 볼륨인  Content 볼륨을 클릭합니다.</p>
</li>
<li>
<p>아래와 같이 설정 후 ‘Continue’ 버튼을 클릭한합니다.</p>
<ul>
<li>Destination Volume Name : Content_copy</li>
<li>Destination disk type : standard storage</li>
</ul>
</li>
<li>
<p>Max Transfer Rate는 100MB/s으로 설정 후 ‘Continue’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>Replication Policy에 Mirror를 선택합니다.</p>
</li>
<li>
<p>Schedule은 one-time copy를 선택합니다.</p>
</li>
<li>
<p>최종 구성 리뷰 후 체크 박스 활성화하고 ‘Go’버튼을 클릭합니다.</p>
</li>
<li>
<p>Working Environment에서 replication 구성이 되었음을 확인합니다.</p>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/azure_replication.PNG?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>Replication status에서 Replication 완료 상태를 확인합니다.</p>
<ul>
<li>Status : idle 확인(transferring 상태라면 조금 더 기다린 후 확인)</li>
<li>Mirror State : snapmirrored 확인</li>
</ul>
</li>
<li>
<p>replication status에서 Content 볼륨의 왼쪽에 마우스를 가져가면 나타나는 메뉴에서 ‘break’ 버튼을 클릭합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/images/break_replication.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>target 볼륨인 content_copy 볼륨은 마운트가 불가능한 상태입니다. 마운트가 가능하도록 설정하기 위해 ‘Edit’ 버튼을 클릭합니다.</p>
</li>
<li>
<p>아래와 같이 설정 후 ‘update’ 버튼을 클릭합니다.</p>
<ul>
<li>Custom export policy : 해당 VNet subnet의 IP range</li>
</ul>
</li>
<li>
<p>Production_copy 볼륨의 ‘mount command’를 클릭합니다.</p>
</li>
<li>
<p>Mount command를 copy합니다.</p>
</li>
<li>
<p>해당 VNet에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</p>
<pre><code> mkdir /mnt/content_copy
 mount 10.1.2.7:/content_copy /mnt/content_copy
</code></pre>
</li>
<li>
<p>볼륨에 대한 Read와 Write 가 가능함을 확인합니다.</p>
<pre><code>  cd /mnt/content_copy
  ls -al
  vi netappfabric.txt
</code></pre>
</li>
</ol>

