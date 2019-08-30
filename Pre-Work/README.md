---


---

<h2 id="task-1-cloud-central에-azure-permission-부여">Task 1: Cloud Central에 Azure Permission 부여</h2>
<ol>
<li>
<p>NetApp Cloud Central에 로그인합니다. (<a href="https://cloud.netapp.com">https://cloud.netapp.com</a>)</p>
</li>
<li>
<p>Policy_for_Setup_As_Service_Azure.json 파일을 다운 받아  수정합니다. (<a href="https://s3.amazonaws.com/occm-sample-policies/Policy_for_Setup_As_Service_Azure.json">Policy_for_Setup_As_Service_Azure.json</a>)       Policy_for_setup_As_Service_Azure.json 파일의 끝부분에 /subscription/ 다음에 각자 본인의 Azure subscription ID값으로 변경하여 수정하고 저장합니다.</p>
</li>
</ol>
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">    "AssignableScopes": [
	"/subscriptions/subscription id 기입	"
    ],
    "Description": "Azure SetupAsService",
    "IsCustom": "true"
</code></pre>
<ol start="3">
<li>
<p>수정한 JSON을 이용해 custom role을 생성하기 위해 azure portal에 접속합니다.</p>
</li>
<li>
<p>Azure portal에서 제공되는 cloud shell에서 해당 JSON 파일을 업로드합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work/Images/cloudshell.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>업로드된 JSON 파일을 통해 custom role을 생성합니다.</p>
<pre><code>az role definition create --role-definition Policy_for_Setup_As_Service_Azure.json
</code></pre>
</li>
<li>
<p>Azure에 생성된 Custom Role 확인합니다.</p>
<ul>
<li>Azure Subscription 을 열고 pay-as-you-go subscription선택</li>
<li>pay-as-you-go subscription선택</li>
<li>Roles 클릭</li>
<li>Azure SetupAsService Role 확인</li>
</ul>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/raw/master/Pre-Work/Images/Azure_setup_service_rol.png?raw=true" alt="enter image description here"></p>
<ol start="8">
<li>NetApp Cloud Central에서 Cloud Manager를 설치할 user에게 role을 할당합니다.
<ul>
<li>Azure내 Subscription 을 열고 pay-as-you-go subscription선택</li>
<li>Access control (IAM) 클릭</li>
<li>Add를 클릭 후 ‘add role assignment’ 선택</li>
<li>Role : Azure SetupAsService 선택</li>
<li>Assign access to : Azure AD user, group, or application 에 Access 할당</li>
<li>Select : 본인의 account 선택</li>
</ul>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work/Images/azure_IAM.png?raw=true" alt="enter image description here"></p>
<h2 id="task-2-azure-networking-설정">Task 2: Azure Networking 설정</h2>
<ol>
<li>
<p>Outbound 인터넷 연결이 가능한 VNet을 사전에 구성합니다.</p>
<ul>
<li><a href="https://docs.microsoft.com/ko-kr/azure/virtual-network/">Azure VNet 설명서</a></li>
</ul>
</li>
<li>
<p>Cloud Manager와 Cloud Volumes ONTAP이 요구하는 Networking 구성 여부를 확인합니다.</p>
<ul>
<li><a href="https://docs.netapp.com/us-en/occm/reference_networking_cloud_manager.html#connection-to-target-networks">Cloud Manager 요구 네트워크 구성</a></li>
<li><a href="https://docs.netapp.com/us-en/occm/reference_networking_azure.html">Cloud Volumes ONTAP 요구 네트워크 구성</a></li>
</ul>
</li>
</ol>
<h2 id="task-3-cloud-central에-aws-permission-부여">Task 3: Cloud Central에 AWS Permission 부여</h2>
<ol>
<li>
<p>AWS Market Place에서 Cloud Volumes ONTAP을 구독합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work/Images/Marketpalce_AWS.png?raw=true" alt="enter image description here"></p>
</li>
<li>
<p>NetApp Cloud Central policy for AWS 파일을 다운 받아 AWS IAM 콘솔에서 해당 파일을 copy하여 Policy를 생성합니다. (<a href="https://s3.amazonaws.com/occm-sample-policies/Policy_for_Setup_As_Service.json">NetApp Cloud Central policy for AWS</a>)</p>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work/Images/AWS_IAM_Policy.PNG?raw=true" alt="enter image description here"></p>
<ol start="3">
<li>해당 Policy를 IAM 사용자에게 할당합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work/Images/AWS_IAM_User.PNG?raw=true" alt="enter image description here"></p>
<h2 id="task-4-aws-networking-설정">Task 4: AWS Networking 설정</h2>
<ol>
<li>
<p>Outbound 인터넷 연결이 가능한 VPC를 사전에 구성합니다.</p>
<ul>
<li><a href="https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/what-is-amazon-vpc.html">AWS VPC 설명서</a></li>
</ul>
</li>
<li>
<p>Cloud Manager와 Cloud Volumes ONTAP이 요구하는 Networking 구성 여부를 확인합니다.</p>
<ul>
<li><a href="https://docs.netapp.com/us-en/occm/reference_networking_cloud_manager.html#connection-to-target-networks">Cloud Manager 요구 네트워크 구성</a></li>
<li><a href="https://docs.netapp.com/us-en/occm/reference_networking_aws.html#general-aws-networking-requirements-for-cloud-volumes-ontap">Cloud Volumes ONTAP 요구 네트워크 구성</a></li>
</ul>
</li>
<li>
<p>VPC와 S3 서비스에 대한 Endpoint를 구성합니다. ( Cloud Tiering 필요 )</p>
<ul>
<li><a href="https://aws.amazon.com/ko/blogs/korea/anew-vpc-endpoint-for-amazon-s3/">AWS S3 Endpoint 설명서</a></li>
</ul>
</li>
</ol>

