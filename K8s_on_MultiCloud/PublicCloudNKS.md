---


---

다음 Task는 Public Cloud (AWS, Azure) 상의 NKS 배포를 실습 합니다. [https://nks.netapp.io](https://nks.netapp.io)  로 직접 접속하여서 로그인하고 '+ADD A CLUSTER NOW' 메뉴 클릭하여 다음 단계를 진행합니다.
Azure는 VM기반으로 배포를 진행하고, AWS는 Managed Service(EKS)를 활용하여 배포 하도록 하겠습니다.
## Step1. Azure에 NKS 배포
1. 배포 플랫폼 선택
배포 진행의 첫번째 메뉴인 'Choose a provider' 단계에서 Microsoft Azure를 선택합니다.
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/05_Azure.png)

'Configure your provider' 단계 에서는 Service provider의 환경을 구성 할 수 있습니다. 

2. Credential 정보 입력
Azure와의 접속을 위한 credential 정보를 입력합니다.
```
ADD CREDENTIALS
```
이때, 'obtaining credentials for Azure'를 클릭하면 credential 생성 방법을 자세히 확인 할 수 있습니다.
> Azure credential 생성 방법 : 아래 가이드를 참조 할 것 
> ([Azure Credential 생성 참조 링크](https://docs.netapp.com/us-en/kubernetes-service/create-auth-credentials-on-azure.html#create-new-azure-credentials))

Azure Portal ([https://portal.azure.com/](https://portal.azure.com/)) 에 로그인하여 아래 진행
(Recommend) Azure Active Directory 어플리케이션을 생성하고, 요구되는 permission을 할당하는 방법으로 진행합니다.

- Step 1: Check App Registration Settings
- Step 2: Check Account Permissions
- Step 3: Check the Subscription
- Step 4: Check Your Account’s Role for the Subscription
- Step 5: Create an Azure Active Directory application
- Step 6: Get the Application ID (Client ID)
- Step 7: Generate an Authentication Key
- Step 8: Get the Tenant ID
- Step 9: Choose a Role and Scope for the App

>위 9단계의 Step 동안 SUBSCRIPTION ID, APPLICATION (CLIENT) ID, Secret key (Client Password), Directory ID (Tenant ID) 정보를 별도로 메모해 둡니다.

NetApp Cloud portal로 돌아가서, 'ADD CREDENTIALS' 클릭하여 Azure 인증정보를 기입합니다.

3. Cloud 환경 구성 셋업
기본 설정으로 1 Master (Standard D2, Disk 50GB) 와 2 Workers (Standard D2, Disk 50GB) 노드가 셋업이 되고 설치 하고자 하는 Azure region, Resource Group, Network의 값들을 기본값으로 가져 옵니다. 
이 클라우드 설정값은 Edit 메뉴를 통해 변경이 가능합니다. 여기서는 아래 설정 값만 변경 후 SUBMIT을 클릭 합니다.
* Location: Korea Central
* Resource Group: 
4. K8s Cluster 구성 셋업
Cluster Name을 Azure-cluster로 변경 후 진행 합니다. 나머지는 기본값으로 변경 없이 유지하고 SUBMIT을 클릭 합니다.

약15분 후 Azure에 Cluster 설치가 완료 됩니다.

## Step2. AWS에 NKS배포
다음은 AmazonEKS 를 이용하여 배포 실습을 진행 하겠습니다.
1. 배포 플랫폼 선택
NKS 홈페이지 우측상단의 '+ADD CLUSTER' 메뉴를 클릭합니다.
```
ADD CLUSTER
```
배포할 Provider로 AmazonEKS 를 선택합니다.
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/06_EKS.png)

다음 단계인 Configure your provider에서는 Service provider의 환경을 구성 할 수 있습니다.

2. Credential 정보 입력
AWS와의 접속을 위한 credential 정보를 입력합니다.
```
ADD CREDENTIALS
```
>AWS credential 생성 방법 : 가이드를 참조할 것 ([AWS Credential 생성 참조 링크](https://docs.netapp.com/us-en/kubernetes-service/create-auth-credentials-on-aws.html))

이때, 'obtaining credentials for AWS'를 클릭하면 credential 생성 방법을 자세히 확인 할 수 있습니다. AWS credential 이 있으면, AWS Console ([https://console.aws.amazon.com/](https://console.aws.amazon.com/)) 에 로그인하여 아래 단계를 진행 합니다.
- Step1. Create an AWS user.
- Step2. Create a policy which grants full access to:
 -- Autoscaling
 -- CloudWatch
 -- EC2
 -- Elastic Load Balancing
 -- IAM
 -- Route 53
- Step3. Attach this policy to the user.

>위 3단계의 Step 동안 Access key ID, Secret access key 정보를 별도로 메모해 둡니다.

NetApp Cloud portal로 돌아가서, 'ADD CREDENTIALS' 클릭하여 EKS 인증정보를 기입 합니다.

3. Cloud 환경 구성 셋업
기본 설정으로, Master node는 AWS managed service로 제공되며, 사용자는 Min / Max Worker 노드수를 정의 할 수 있습니다. 이번 Task에서는 Node size 및 Region을 아래와 같이 변경하여 설치 진행합니다.
* Node Size: t2.medium
* Region: Seoul
다음으로 'SUBMIT' 메뉴를 클릭 합니다.

4. K8s Cluster 구성 셋업
다음 절차는 K8s Cluster 구성입니다. 
Cluster Name을 EKS-cluster로 변경 후 진행하며, 다른 설정값은 기본값으로 변경 하지 말고 'SUBMIT' 클릭 합니다.

약15분후 AWS에 Cluster 설치가 완료 됩니다.

## Step3. NKS 관리 및 운영
1. Cluster에 containerized application 추가
- NKS home > CONTROL PLANE > CLUSTERS > Azure-cluster 선택

'+ADD SOLUTION' 메뉴 선택하여 HAPROXY를 추가해 보도록 합니다.
- NetApp Kubernetes Service Solutions 리스트에서 HAPROXY 선택 > INSTALL

약45-60초 경과 후 배포가 완료 됩니다.

CONTROL PLANE 창에서 Azure-cluster 클릭 > Solutions 에서 HAPROXY 가 설치 되었는지 확인 합니다.

>Kubernetes Dashboard 클릭하면 기본으로 설치된 dashboard를 볼수 있습니다. Dashboard를 통해 자원 사용 모니터링, Deploy 된 Object 정보들을 조회할 수 있습니다. Azure-cluster 창으로 돌아가서, Event Log 를 클릭하면 요청한 Job에 대한 처리 이력을 확인 할 수 있습니다.

또 다른 설치 예제로, K8s Cluster의 자세한 시스템 자원 모니터링을 위해 Promethus를 설치해 보도록 하겠습니다.
Azure-cluster 창에서 + ADD SOLUTION 메뉴 클릭 > Application Marketplace에서 Promethus 선택 > 1분이내 설치가 완료 됩니다.

설치 완료 후, Prometheus Endpoint URL을 클릭 합니다.

Grafana login 창이 나오면,
- 기본 ID / Password : prometheus / grafana 로 접속

Grafana home 창의 좌측 메뉴 중 Dashboard 메뉴 > manage 클릭하여 Node 자원 모니터링, Object 상태 확인등 원하는 형태로 Dashboard 구현 가능합니다.
>자세한 Promethus 및 Grafana 사용법은 이번 과정에서는 다루지 않습니다.

2. Client의 CLI 를 이용하여 Kubernetes 접속 및 관리 실습을 진행
NKS 홈페이지 > Cluster (Azure-cluster) 선택 하여 kubeconfig를 자신의 Local PC 에 다운로드 합니다. 
- 저장경로 : C:\Users\JINHAK\.kube\kubeconfig

>자신의 Local PC에는 사전에 kubectl을 설치 함 (참고 링크 : [Windows 에 kubectl 설치하기](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-windows) )

설치 완료 후, window CMD 창을 띄운 후 아래와 같이 접속 확인합니다.

<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">C:\Users\JINHAK\.kube>set KUBECONFIG=./kubeconfig
C:\Users\JINHAK\.kube>kubectl get nodes
NAME  STATUS  ROLES  AGE  VERSION
net65b5yqh-master-1  Ready  master  25h  v1.15.0
net65b5yqh-worker-1  Ready  <none>  25h  v1.15.0
net65b5yqh-worker-2  Ready  <none>  25h  v1.15.0
C:\Users\JINHAK\.kube></code></pre>

이외에, 다양한 Kubectl client를 이용해 다양한 K8s Cluster의 operation이 가능합니다.
>자세한 Kubectl client에 대한 사용법은 이번 과정에서는 다루지 않음

3. Helm Chart를 이용한 Application 배포

NKS home > Solutions > CHARTS REPOS > IMPORT CHARTS 클릭 합니다.
- Chart Repository Name : my-charts
- Source : Github
- Github Repository URL : [https://github.com/netappkr/ghost-import](https://github.com/netappkr/ghost-import)

REVIEW REPOSITORY 클릭 > Access Verified 체크 표시 확인 > SAVE REPOSITORY 클릭 합니다.

MY CHARTS에 등록이 완료 되면, NKS Home > CONTROL PLANE > CLUSTERS > Azure-cluster 클릭 합니다.
+ ADD SOLUTION 메뉴 클릭 > My Charts > ghost 선택

설치가 완료 되면, Kubernetes Dashboard > Discovery and load balancing > Services에서 ghost의 External endpoints (예: 13.92.xxx.xxx:80) 클릭하여 ghost home 화면이 구동 되는 것을  확인합니다.

끝.

[메인 메뉴로 이동](https://github.com/netappkr/NDX_Handsonworkshop-/) 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTY3OTk5ODM2LDczMjMwMTY5MywtNTU5Mz
YxNjE5LDE1OTU1NDkzNzAsLTE3MTk5ODg2NSw2ODcyMjA3MzUs
LTIwNDYyMTE5MTEsLTQyODc2NDk3NiwtMjA1MDU2NDY0MSwtND
k0MTY3OTY0LC0xNjU1MjU4OTE3LDczMDk5ODExNl19
-->