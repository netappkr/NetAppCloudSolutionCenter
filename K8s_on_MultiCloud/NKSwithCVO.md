---


---

이번 Task 는, 앞 Task에서 생성된 NKS cluster와 CVO 구성 환경에서, Trident 이용하여 backend 스토리지를 구성하고 Persistent Volume 을 생성하는 실습을 진행 하겠습니다.

>CVO에서 배포하는 Trident 는 Kubernetes 버전 1.14까지 지원하므로, NKS 배포시 버전 선택에 주의

## Step1. Cloud Manager와 NKS 연동
Cloud Manager 화면에서,
Kubernetes Clusters 클릭 > Discover Cluster > Upload File > NKS 화면에서 원하는 Cluster 의 kubeconfig 파일을 로컬 PC에 다운로드 받고 이를 선택 > 추가된 Kubernetes cluster를 확인
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/08_K8sCluster.png)

## Step2. Trident 배포를 통해 CVO와 NKS 연동
Cloud Manager 창에서 연동하고자 하는(사전에 생성되어 있는) CVO를  선택 합니다.

Cloud Manager 우측창에 Persistent Volumes for Kubernetes 클릭 한 후, 아래 값으로 설정 합니다.
- Select Kubernetes Cluster : Winter Sun
- Custom Export Policy : 172.23.0.0/16
- NFS 선택, 다음 Connect 클릭
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/09_K8sCVOPV.png)
>Timeline 메뉴에 들어가서 정상적으로 진행되는지 모니터링 가능

## Step3. Trident 셋업 및 활용

이제, 나의 NKS에 deploy 된 K8s Cluster와의 연동이 완료 되었습니다.
NKS 페이지로 돌아가서, Kubernetes cluster의 master node의 public IP를 통해 ssh 접속을 합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">$ kubectl get sc   ## CVO용 Storage Class 가 생성 되었음을 확인 
$ kubectl get pods -n trident      ## Trident POD 가 정상 동작중임을 확인합니다.</code></pre>

> 이 후, PVC 생성하여 CVO에 Volume 생성 됨을 확인. On-premise 에서 PVC 생성 과정과 동일하여 생략함
> (참조 : [On-premise PVC 생성 과정](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md#step4-%EA%B8%B0%ED%83%80-object-%EC%83%9D%EC%84%B1-%EB%B0%8F-%EC%9A%B4%EC%98%81-%EC%98%88%EC%A0%9C))

PVC가 생성되면, Cloud Manager로 돌아가서 Azure에 생성된 CVO 구름 모양을 클릭하게 되면, Volume으로 trident_trident, trident_default_basic_pvc_xxxx 두개의 FlexVolume이 생성된 걸 확인 할 수 있습니다.
- trident_trident 볼륨은 etcd를 위한 볼륨
-  trident_default_basic_pvc_xxxx는 생성한 PVC와 binding 되어 있는 PV 볼륨
>그 이후 생성된 PVC 를 POD에 mount하여 확인하는 과정은 On-premise 에서 PVC, POD 마운트 과정과 동일하여 생략함
>(참조 : [On-premise에서 PVC, POD 마운트하는 과정](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md#step4-%EA%B8%B0%ED%83%80-object-%EC%83%9D%EC%84%B1-%EB%B0%8F-%EC%9A%B4%EC%98%81-%EC%98%88%EC%A0%9C))

끝.

[메인 메뉴로 이동](https://github.com/netappkr/NDX_Handsonworkshop-/) 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAzMTQ3ODkxMiwxMDc5Mjg0MTE3LC0xMT
E4NDM4ODYzLDE0MzU1NzkwMzFdfQ==
-->