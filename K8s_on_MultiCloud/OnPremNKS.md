이번 Task는 NetApp Kubernetes Services를 이용하여 On-premise에 있는 NetApp HCI 장비에 K8s Cluster를 배포하는 실습을 진행합니다.

<strong>사전 준비사항</strong>

- NKS login 계정

## Step 1. NKS에서 HCI 기반의 Cluster 생성

1. NetApp Cloud Portal ([https://cloud.netapp.com](https://cloud.netapp.com))에 자신의 계정으로 login 하여, 'NKS(NetApp Kubernetes Service)' 를 선택 합니다.
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/01_NKS%20memu1.png)
>30일 trial license를 제공하기 때문에, credit card 등록없이 체험 가능

또는, NKS 홈페이지([https://nks.netapp.io](https://nks.netapp.io))  로 직접 접속하여서 로그인하면, 아래 웹페이지로 접속이 되고, '+ADD A CLUSTER NOW' 메뉴 선택하여 다음 단계를 진행 할 수 있습니다.
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/02_NKS%20home.png)

2. 다음 단계는 Provider를 선택하는 단계입니다.

3개의 Cloud Service Provider(AWS, Azure, GCP) 환경에서 Instance(VM)기반의 배포 또는 Managed Service 형태의 배포가 가능합니다. 또한, 최근에는 On-premise의 NetApp HCI 기반 배포를 지원하므로써, Cloud DC 및 On-premise DC 에서 동시에 다수의 K8s Cluster를 배포 할 수 있게 되었습니다.

이번 Task에서는 On-premise에 위치한 NetApp HCI상에 NKS를 배포하는 실습을 진행 하겠습니다. 

전체 절차는 아래와 같습니다.

NKS home 클릭 > 우측 상단 Organizations 아이콘 클릭 > NetAppKR_LAB 클릭 

![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/02_NKSorg1.png) >'+ ADD CLUSTER' 클릭 > NetApp | HCI 클릭 > 디폴트 설정 유지하면서 SUBMIT 클릭 > 디폴트 설정 유지(K8s version : 1.14.3)하고 SUBMIT 클릭

약 5~10분후, On-premise 상에 K8s Cluster 설치가 완료 됩니다.

## Step2. K8s Cluster 접속 환경 셋업
이번 Step 에서는 기존에 On-premise HCI 상에 설치 되어 있는 ONTAP Select와 Trident를 이용하여 연동하는 실습을 진행합니다.
> ONTAP Select : NetApp이 제공하는 Software Defined Storage 라인업으로, FAS/AFF 동일한 OS를 사용하기 때문에, 대부분의 기능이 호환됨
> Trident : Kubernetes 클러스터에서 Dynamic Storage Provisioning 을 지원하는 External Provisioner

기 배포된 On-prem NKS에 Trident 설치를 위해서는 CLI로 진행해야 합니다. NKS의 Master 노드 접속을 위해서는 SSH Key를 이용하여 접속을 진행합니다.
1. SSH Key를 다운로드 받습니다.
>SSH Key download 방법은 아래 Link 참조
>[https://docs.netapp.com/us-en/kubernetes-service/ssh-to-a-node-in-an-nks-cluster.html#get-the-ssh-keys](https://docs.netapp.com/us-en/kubernetes-service/ssh-to-a-node-in-an-nks-cluster.html#get-the-ssh-keys)

2. 다운받은 Key를 ppk 타입으로 변환합니다.
다운로드 받은 private key를 이용하여 master node에 ssh 접속이 가능한데, 만약 Putty를 이용하여 접속을 한다면, Putty Private Key로 변환하여야 하며, 변환은 Putty Key Generator를 설치하여 생성 가능 합니다.
PuTTYgen ([https://www.puttygen.com/](https://www.puttygen.com/))을 자신의 PC에 설치 후, 실행하여 Conversions > Import key > 다운로드 받은 SSH Key (id_rsa) 선택 > Save Private key 메뉴 클릭하여 자신의 로컬 PC에 저장 합니다.
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/03_Puttygen.png)

3. Putty를 이용하여 SSH 접속합니다.
Putty를 실행하고,
* Host Name (or IP address) : master node의 IP address
* Connection > SSH > Auth > Browse 클릭하여 Putty Private Key (.ppk 파일) 선택 > Open
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/images/04_Putty.png)

On-premise에 구성되는 K8s는 디폴트로 Debian OS를 기반으로 하고 있으며, SSH 접속 가능한 계정은 debian user를 이용하여 login 하면 됩니다.
debian user로 접속 후, 해당 계정으로 kubectl 사용을 위해 kubeconfig 파일을 $HOME 에 copy합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">ssh debian@115.144.xxx.xxx
debian@netyo6pai7-master-1:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
debian@netyo6pai7-master-1:~/.kube$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
debian@netyo6pai7-master-1:~$ kubectl get nodes
NAME  STATUS  ROLES  AGE  VERSION
netyo6pai7-master-1  Ready  master  17h  v1.13.7
netyo6pai7-pool-1-wz8p8  Ready  <none>  17h  v1.13.7
netyo6pai7-pool-1-z6x66  Ready  <none>  17h  v1.13.7
debian@netyo6pai7-master-1:~$</code></pre>

다음 단계로 넘어가기 전에, NKS on HCI는 기본적으로 ONTAP Select와 통신을 위한 10.255.xxx.xxx IP를 위한 Network interface가 disable 되어 있기 때문에, 수동으로 10.255.xxx.xxx 대 IP를 심어 주어야 합니다. (이 네트웍은 추후에 Public Cloud와 연동하기 위한 네트웍으로 사용될 예정) 
각 사용자 별로 Master node에 설정된 115.114.xxx.zzz의 마지막 IP(zzz)를 동일하게 10.255.yyy.zzz에 설정하도록 합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">ssh debian@115.144.xxx.xxx[kubernetes  master node IP]
login as: debian 
debian@net5c0rjuz-master-1:~$ sudo -i
root@net5c0rjuz-master-1:~# ifconfig ens160 | grep inet
        inet 115.144.xxx.xxx  netmask 255.255.255.0  broadcast 115.144.xxx.xxx
        inet6 fe80::250:56ff:fea8:a4b  prefixlen 64  scopeid 0x20<link>
root@net5c0rjuz-master-1:~# ifconfig ens192 up
root@net5c0rjuz-master-1:~# vi /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug ens160
iface ens160 inet dhcp
auto ens192
iface ens192 inet static
address 10.255.xxx.xxx
netmask 255.255.255.0
root@net5c0rjuz-master-1:~# route add -net 10.255.xxx.0 netmask 255.255.255.0 dev ens192
root@net5c0rjuz-master-1:~# /etc/init.d/networking restart
[ ok ] Restarting networking (via systemctl): networking.service.</code></pre>

나머지 두개의 worker node 도 동일하게 ens192 네트웍 설정을 진행 합니다. 

## Step3. K8s cluster에 Trident 설치
다음으로 Trident 구성을 진행합니다. NKS HCI에는 기본으로 Trident 19.04.1 버전의 패키지가 다운로드 되어 있습니다. 만약 최신 버전(19.07)의 Trident를 사용하고자 할 때는, 다시 다운로드하여 설치 하여도 됩니다. 이번 Task에서는 최신 버전을 설치하도록 하겠습니다.

1. Installer download (기존 download 되어 있는 패키지 사용시는 skip)
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">$ wget https://github.com/NetApp/trident/releases/download/v19.07.0/trident-installer-19.07.0.tar.gz
$ tar -xf trident-installer-19.07.0.tar.gz
$ cd trident-installer/</code></pre>
기본적으로 K8s의 base OS인 debian 에는 NFS client 프로그램이 설치되어 있기 때문에 Trident NFS plug-in을 사용 하더라도 설치 할 필요가 없습니다.
>19.04 이전 버전에서는 metadata 저장용으로 etcd를 사용하였기 때문에, Trident 설치 이전에 backend.json 파일을 setup 디렉토리에 copy한 후 Install을 시작해야 했지만, 19.07버전 이후 부터는 metadata 관리를 CRD를 이용해서 하기 때문에 사전에 backend.json이 설치시에는 필요 없음.
2. Trident 설치
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"> ~/trident-installer$ ./tridentctl install -n trident   ### 여기서 -d 옵션을 붙이면 debug 모드로 좀 더 자세한 install 과정을 볼 수 있습니다.
debian@net5c0rjuz-master-1:~/trident-installer$ kubectl get pod -n trident
NAME  READY  STATUS  RESTARTS  AGE
trident-csi-867d54588b-6m59b  4/4  Running  0  2m53s
trident-csi-ggd7z  2/2  Running  0  2m53s
trident-csi-rfv2q  2/2  Running  0  2m53s
### Pod의 갯수는 running 중인 node의 갯수에 따라 달라집니다.

debian@net5c0rjuz-master-1:~/trident-installer$ ./tridentctl -n trident version
+----------------+----------------+
| SERVER VERSION | CLIENT VERSION |
+----------------+----------------+
| 19.07.0  | 19.07.0  |
+----------------+----------------+
debian@net5c0rjuz-master-1:~/trident-installer$</code></pre>
>이 때, 설치가 제대로 되지 않아 Trident를 삭제할 때는 아래 command를 수행
>$ ./tridentctl uninstall -n trident  여기서 -a 옵션을 붙이면, namespace를 제외한 모든 object가 삭제 됨

## Step4. 기타 Object 생성 및 운영 예제
1. Trident Backend 생성
Trident 백엔드는 Trident와 스토리지 간의 관계를 정의합니다. Trident는 해당 스토리지와 통신하는 방법과 Trident가 해당 스토리지 시스템에서 볼륨을 프로비저닝하는 방법을 알려줍니다.
Trident는 다양한 sample yaml 파일을 제공합니다. 이 sample 파일을 활용해서 backend를 생성해 보도록 하겠습니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer$ cp sample-input/backend-ontap-nas.json setup
debian@net5c0rjuz-master-1:~/trident-installer$ vi setup/backend-ontap-nas.json
{
"version": 1,
"storageDriverName": "ontap-nas",
"backendName": "nfsBackend",
"managementLIF": "115.144.xxx.xxx",
"dataLIF": "10.255.xxx.xxx",
"svm": "svm-user1",
"username": "admin",
"password": "xxxxxxx"
}
debian@net5c0rjuz-master-1:~/trident-installer$ ./tridentctl -n trident create backend -f setup/backend-ontap-nas.json</code></pre>
> 만약, Backend 생성시 'aggr assign Error'가 발생하면, SVM에 aggregate가 assign 되지 않아 발생하는 error 임. 스토리지에 CLI로 접속하여 SVM에 aggr을 assign 하여 해결
><pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">ssh admin@  115.144.xxx.xxx
>password : xxxxxxxx
>OTC_Netapp_korea_lab::> vserver modify -vserver svm-test -aggr-list aggr1</code></pre>
다시 Master node로 돌아가서,
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer$ ./tridentctl -n trident create backend -f setup/backend-ontap-nas.json
+------------+----------------+--------------------------------------+--------+---------+
|  NAME  | STORAGE DRIVER |  UUID  | STATE  | VOLUMES |
+------------+----------------+--------------------------------------+--------+---------+
| nfsBackend | ontap-nas  | 11c0fa46-1f52-4cec-87ce-fe6e410b0118 | online |  0 |
+------------+----------------+--------------------------------------+--------+---------+
debian@net5c0rjuz-master-1:~/trident-installer$</code></pre>
Trident의 첫번째 ONTAP NFS backend를 연동 시켰습니다. 다음은 Storage Class를 생성 하도록 합니다. 이제부터는 tridentctl command 사용은 끝이 나고 kubectl을 통해서 operation을 하겠습니다.

2. Storage Class 생성
StorageClass는 관리자가 제공하는 스토리지의 "클래스"를 설명 할 수있는 방법을 제공합니다. 다른 클래스는 서비스 품질 수준, 백업 정책 또는 클러스터 관리자가 결정한 임의의 정책에 매핑 될 수 있습니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer$ cp sample-input/storage-class-basic.yaml.templ setup/storage-class-basic.yaml
debian@net5c0rjuz-master-1:~/trident-installer$ vi setup/storage-class-basic.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: basic
provisioner: netapp.io/trident
parameters:
  backendType: ontap-nas
debian@net5c0rjuz-master-1:~/trident-installer$
debian@net5c0rjuz-master-1:~/trident-installer$ kubectl create -f setup/storage-class-basic.yaml
storageclass.storage.k8s.io/basic created
debian@net5c0rjuz-master-1:~/trident-installer$ kubectl get storageclass
NAME  PROVISIONER  AGE
basic  csi.trident.netapp.io  18s
vsphere (default)  kubernetes.io/vsphere-volume  4d2h
debian@net5c0rjuz-master-1:~/trident-installer$</code></pre>
아래 명령어로 좀 더 자세한 storage class 정보를 조회 할 수 있습니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer$ ./tridentctl -n trident get storageclass basic -o json
{
  "items": [
    {
      "Config": {
        "version": "1",
        "name": "basic",
        "attributes": {
          "backendType": "ontap-nas"
        },
        "storagePools": null,
        "additionalStoragePools": null
      },
      "storage": {
        "nfsBackend": [
          "aggr1"
        ]
      }
    }
  ]
}
debian@net5c0rjuz-master-1:~/trident-installer$</code></pre>
3. 첫번째 PVC, PV, Volume 프로비저닝
PV (PersistentVolume)는 시스템 관리자가, Storage Class를 사용하여 프로비저닝 한 클러스터의 스토리지입니다. 
PVC (PersistentVolumeClaim)는 사용자의 클러스터 Storage 요청입니다. PVC는 PV와 맵핑이 되고, POD는 맵핑된 스토리지를 Mount 하여 사용하게 됩니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer$ cp sample-input/pvc-basic.yaml setup
debian@net5c0rjuz-master-1:~/trident-installer$ vi setup/pvc-basic.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: basic
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: basic
debian@net5c0rjuz-master-1:~/trident-installer$ kubectl create -f setup/pvc-basic.yaml
persistentvolumeclaim/basic created
debian@net5c0rjuz-master-1:~/trident-installer$ kubectl get pvc
NAME  STATUS  VOLUME  CAPACITY  ACCESS MODES  STORAGECLASS  AGE
basic  Bound  pvc-db6adca2-bd17-11e9-b1a8-005056a80a4b  1Gi  RWO  basic  5s
debian@net5c0rjuz-master-1:~/trident-installer$</code></pre>
PVC, PV 및 스토리지에 Volume까지 dynamic하게 생성 되었으며 서로 mapping 된 구조를 확인 할 수 있습니다. ONTAP System Manager GUI 또는 Storage CLI로 들어가서,
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"> ssh admin@115.144.xxx.xxx[ONTAP Select mgmt IP]
Password: ******
OTC_Netapp_korea_lab::> vol show -vserver svm-user1
Vserver  Volume  Aggregate  State  Type  Size  Available Used%
--------- ------------ ------------ ---------- ---- ---------- ---------- -----
svm-user1  svm_user1_root
aggr1  online  RW  1GB  969.2MB  0%
svm-user1  trident_pvc_db6adca2_bd17_11e9_b1a8_005056a80a4b
aggr1  online  RW  1GB  1023MB  0%

2 entries were displayed.</code></pre>
svm-user1 SVM에 trident_로 시작하는 1GB 사이즈의 볼륨이 생성 된 것을 확인 할 수 있습니다.

4. POD에 마운트
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer/setup$ vi task-pv-pod.yaml
kind: Pod
apiVersion: v1
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: basic
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage

debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl create -f task-pv-pod.yaml
debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl get pod --watch     ### POD가 구동되었는지 확인
debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl exec -it task-pv-pod -- df -h /usr/share/nginx/html    ### POD에 Volume이 mount 되었는지 확인

Filesystem  Size  Used Avail Use% Mounted on
115.144.xxx.xxx:/trident_pvc_db6adca2_bd17_11e9_b1a8_005056a80a4b  1.0G  256K  1.0G  1% /usr/share/nginx/html</code></pre>

끝.

[메인 메뉴로 이동](https://github.com/netappkr/NDX_Handsonworkshop-/) 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTI5ODk4NzY0LDE2NzU3NDYyNzgsMTQxNj
IwNjIxLDY4OTYxNTgzMCw1MzQ1MDQwODIsMTIzOTA3MjkyNywt
MTU1NzY4ODg0MiwtMTEyNTYyNjIxMCwxMTM5NjQ4MTk0LDExOT
kwMjIxMTEsLTE2Mzc0ODA2OTMsOTU1MDE4OTk5LDE5MzA0NjYx
MTgsOTU1MDE4OTk5LDE5MzA0NjYxMTgsLTY5NjQ4MTU3NiwtOD
k1ODIxMTYwLDMwNzY0MTkyOCwxMTEwNzQ5NzgsNDU4Mzc2MTgy
XX0=
-->