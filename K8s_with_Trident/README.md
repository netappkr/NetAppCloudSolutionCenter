
---


---
이번 실습에서는 기 설치되어 있는 Kubernetes cluster와 Trident를 이용하여, 다양한 데이터 관리 기능을 실습하도록 하겠습니다.

**사전 준비 사항** 
- Kubernetes cluster 설치
- Trident 설치
>Trident를 설치하지 않은 분은 이전 실습과제를 참조하여 Trident 설치 및 구성을 진행합니다.
>[Trident 설치 및 구성 가이드](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md#step3-k8s-cluster%EC%97%90-trident-%EC%84%A4%EC%B9%98)
>Step3 - 4까지 진행

## RWX Access mode PVC 구성

RWX(Read Write Many) 모드는 다수의 Worker에서 동시에 Volume을 mount 하여 Read/Write 가 가능 하도록 합니다. Kubernetes 환경에서 다수의 node에 다수의 container를 통해 파일 공유가 필요 할 경우에 사용합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"># vi access-mode-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-pvc
spec:
  accessModes:
    - ReadWriteMany       ## Access Mode: RWM은 다수의 Node에서 동시 read/write 가 가능하도록 설정하는 옵션
  resources:
    requests:
      storage: 1Gi
  storageClassName: basic      ## Storage Class는 기존에 Trident를 통해 생성한 이름을 기입
# kubectl create -f access-mode-pvc.yaml</code></pre>
PVC 및 PV 생성이 완료 되었으면, 다음은 2개의 nginx POD를 생성 후 위에서 생성한 PVC를 이용하여 Volume을 mount 하도록 합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"># vi access-mode-nginx1.yaml
kind: Pod
apiVersion: v1
metadata:
  name: nginx1
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: nginx-pvc
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
# vi access-mode-nginx2.yaml
kind: Pod
apiVersion: v1
metadata:
  name: nginx2
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: nginx-pvc
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
# kubectl create -f access-mode-nginx1.yaml
# kubectl create -f access-mode-nginx2.yaml
# kubectl exec -it nginx1 -- sh
sh> df -k    ## NAS mount 여부 확인
# kubectl exec -it nginx2 -- sh
sh> df -k    ## nginx1과 동일한 NAS mount 되었는지 확인
</code></pre>

## PVC/PV Resize 기능 구현

PVC Resize 기능은, 이미 배포되어 있는  PV의 사용량 증가로 인해, 온라인 중에 Volume 용량을 늘리고 싶을 때 사용 할 수 있는 기능입니다. 현재 Kubernetes의 PVC resize는 용량 증설만 가능하며, 용량 Shrink 는 지원하지 않습니다.

<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"># vi storage-class-basic-nfs-resize.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: basic-nfs-resize
provisioner: netapp.io/trident
parameters:
  backendType: "ontap-nas"
allowVolumeExpansion: true     ##Volume resize 기능을 켜기 위해서 설정 해 주어야 하는 Storage Class 파라미터
# kubectl create -f storage-class-basic-nfs-resize.yaml
# vi pvc-basic-nfs-resize.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: basic-nfs-resize
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: basic-nfs-resize
# kubectl create -f pvc-basic-nfs-resize.yaml
# kubectl edit pvc basic-nfs-resize
…
spec:
  accessModes:
  - ReadWriteOnce
  dataSource: null
  resources:
    requests:
      storage: 3Gi   ### size 조정 후 저장하면 바로 resize 됨
  storageClassName: basic-nfs-resize
  volumeName: default-basic-nfs-resize-1e512
...
</code></pre>

## PVC/PV Clone 기능 구현

Clone 기능은 기존에 생성되어 운영중인 Volume을, Trident는 NetApp의 FlexClone 기능을 이용하기 때문에 Volume에 저장되어 있는 데이터량과 상관없이 수초내에 다수개의 PVC/PV를 복제 할 수 있습니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"># cat pvc-basic-clone-nfs.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: basicclone-nfs
  annotations:
    trident.netapp.io/cloneFromPVC: basic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: basic
# kubectl create -f pvc-basic-clone-nfs.yaml
# kubectl get pvc
</core></pre>

# Legacy Volume Import 기능 구현

On-premise의 Linux서버에 Mount 되어 있는 Legacy NAS 스토리지 Volume 에 테스트 데이터를 생성 한 후, 이 Volume을 Linux 서버에서 Umount 한 후, 기 생성되어 있는 K8s Cluster의 PV로 Import 한 후 Legacy 에서 생성한 data 가 그대로 인식되는지 확인합니다.

**Test 볼륨 생성**

기 설치되어 있는 ONTAP Select의 System Manager에 접속하여 실습을 위한 볼륨을 각자 생성하도록 합니다.
웹 브라우저에서 https://[ONTAP Select cluster management IP] 로 접속합니다.
- login : admin
- password : **********

우측 Storage 메뉴 > SVMs > svm-user1 > Volumes > + Create > Create FlexVol
- Name: vol01
- Aggregate: aggr1
- Storage Type: NAS
- Total Size: 1GB
- Snapshot Reserve (%): 0

![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_with_Trident/images/10_VolCreate.PNG)

**Legacy에 Test 데이터 생성**
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">ssh root@115.144.xxx.xxx [user1 VM IP]
password: *******
[root@user1 ~]# df -k
Filesystem              1K-blocks    Used Available Use% Mounted on
/dev/mapper/cl-root      27245572 3339096  23906476  13% /
devtmpfs                  1928336       0   1928336   0% /dev
tmpfs                     1940444       0   1940444   0% /dev/shm
tmpfs                     1940444  131880   1808564   7% /run
tmpfs                     1940444       0   1940444   0% /sys/fs/cgroup
/dev/sda1                 1038336  182564    855772  18% /boot
10.255.xxx.xxx:/content   4980736   14016   4966720   1% /var/lib/ghost/content
tmpfs                      388092       0    388092   0% /run/user/0
[root@user1 ~]# mount 10.255.xxx.xxx:/vol01 /mnt      ###기존에 content 볼륨이 mount 되어 있는 IP를 사용하여 새로운 볼륨을 mount 함
[root@user1 ~]# df -k
Filesystem              1K-blocks    Used Available Use% Mounted on
/dev/mapper/cl-root      27245572 3339096  23906476  13% /
devtmpfs                  1928336       0   1928336   0% /dev
tmpfs                     1940444       0   1940444   0% /dev/shm
tmpfs                     1940444  131880   1808564   7% /run
tmpfs                     1940444       0   1940444   0% /sys/fs/cgroup
/dev/sda1                 1038336  182564    855772  18% /boot
10.255.xxx.xxx:/content   4980736   14080   4966656   1% /var/lib/ghost/content
tmpfs                      388092       0    388092   0% /run/user/0
10.255.xxx.xxx:/vol01     1048576     256   1048320   1% /mnt
[root@user1 /]# vi mnt/testdata.txt
...
This is test data!!!
...
[root@user1 /]# umount /mnt</code></pre>

**Trident Import 수행**

이제는 K8s cluster로 접속하여 trident import 기능을 통해, Legacy의 vol01 볼륨을 K8s의 Persistent Volume으로 가져오도록 하겠습니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~$ tridentctl get backend -n trident
+------------+----------------+--------------------------------------+--------+---------+
|    NAME    | STORAGE DRIVER |                 UUID                 | STATE  | VOLUMES |
+------------+----------------+--------------------------------------+--------+---------+
| nfsBackend | ontap-nas      | 11c0fa46-1f52-4cec-87ce-fe6e410b0118 | online |       1 |
+------------+----------------+--------------------------------------+--------+---------+
debian@net5c0rjuz-master-1:~$ kubectl get storageclass
NAME                PROVISIONER                    AGE
basic               csi.trident.netapp.io          8d
vsphere (default)   kubernetes.io/vsphere-volume   12d
debian@net5c0rjuz-master-1:~$ kubectl get pvc
NAME    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
basic   Bound    pvc-db6adca2-bd17-11e9-b1a8-005056a80a4b   1Gi        RWO            basic          8d
debian@net5c0rjuz-master-1:~$ cd trident-installer/setup
debian@net5c0rjuz-master-1:~/trident-installer/setup$ ls
backend-ontap-nas.json  pvc-basic.yaml  storage-class-basic.yaml
debian@net5c0rjuz-master-1:~/trident-installer/setup$ cp pvc-basic.yaml pvc-import.yaml
debian@net5c0rjuz-master-1:~/trident-installer/setup$ vi pvc-import.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc-import
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: basic
debian@net5c0rjuz-master-1:~/trident-installer/setup$ tridentctl import volume nfsBackend vol01 -f pvc-import.yaml -n trident
debian@net5c0rjuz-master-1:~/trident-installer/setup$ tridentctl import volume nfsBackend1 vol01 -f pvc-import.yaml -n trident
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
|                   NAME                   |  SIZE   | STORAGE CLASS | PROTOCOL |             BACKEND UUID             | STATE  | MANAGED |
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
| pvc-5ed37b32-c388-11e9-b1a8-005056a80a4b | 1.0 GiB | basic         | file     | b1f87f94-6966-4ffe-9bf0-cff7e2c1a2cd | online | true    |
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl get pvc
NAME         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
basic        Bound    pvc-db6adca2-bd17-11e9-b1a8-005056a80a4b   1Gi        RWO            basic          8d
pvc-import   Bound    pvc-5ed37b32-c388-11e9-b1a8-005056a80a4b   1Gi        RWO            basic          2m5s
</code></pre>

**POD에 mount하여 데이터 확인**
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl get pod
NAME                     READY   STATUS              RESTARTS   AGE
nginx-58df4bbfdd-l2tkt   1/1     Running             0          7d19h
task-pod                 1/1     Running   0          18s
debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl exec -it task-pod -- df -h /usr/share/nginx/html
Filesystem  Size  Used Avail Use% Mounted on
10.200.xxx.xxx:/trident_pvc_6c2c5022_f48f_453a_a10c_a0f23d180478  1.0G  320K  1.0G  1% /usr/share/nginx/html
debian@net5c0rjuz-master-1:~/trident-installer/setup$ kubectl exec -it task-pod -- cat /usr/share/nginx/html
...
This is test data!!!
...
</code></pre>


<!--stackedit_data:
eyJoaXN0b3J5IjpbOTMzNjM3NTY2LDI1ODA3NDkyOCwxMjMyOT
Y5OTQwLC02MTA0NTg0NDksLTExMjQ3NjI1NjAsODg2MzcyMjEw
LDE5ODk4ODkyNDEsLTYwOTk5ODE2LC05NDI1ODExMjgsMjAzNz
E5MTM2NiwtMzc1MDk1OTMsLTk5NjA2NzQxOSwtNDExMTI5NTc1
LDE4MDU2NDgwNjIsLTczNjIzMDMzNSwtMTExMDg1MzE3MiwtMj
Y5MzM0NDYxLC0yMzA5MjU2NTksNDc4Nzc3NDEyLC0xNjY4NTE1
ODM1XX0=
-->