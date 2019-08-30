이번 Task는 기존 VM 기반의 Ghost 블로그 Application과 기존 데이터를 K8S Cluster로 이관합니다. 

**사전 준비사항** 
 - [ ] [K8s Cluster 접속 환경 셋업](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.) 
 - [ ] [Trident 설치 및 Backend 구성](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md) 
 - [ ] [VM 기반의 Ghost 블로그 App 설치](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Pre-Work2/README.md)
 
 ## Step 1. 기존 Ghost 블로그 데이터 Clone 복제  
1. 기 설치되어 있는 ONTAP Select의 System Manager에 접속합니다. 웹 브라우저에서 https://[ONTAP Select cluster management IP] 로 접속합니다.
2. 부여 받은 SVM에 접속하여 생성된 볼륨들을 확인합니다.
     * Storage 메뉴 > SVMs > svm-user-number 

3. Content 볼륨에 대해 Clone을 수행합니다.
     * More Actions > Clone > Create > Volume 
     * Thin Provisioning 활성화
     * Create new Snapshot copy now 선택 
     * Clone 클릭  
   
   ![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/content_clone_2.png)

 ## Step 2. Clone 볼륨을 K8S Cluster내의 PVC로 Import 수행      
1. 기 설치된 K8S Cluster에 접속합니다.

2.  Trident 설치 시 사용한 trident-installer 폴더로 이동합니다.

3.  Trident에서 제공하는 Import 기능을 통해  Step1에서 생성한 content clone 볼륨을 해당 Cluster내의 PVC 볼륨으로 Import 합니다. ([import-pvc.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/import-pvc.yaml))

      ` # ./tridentctl import volume nfsBackend content_clone -f import-pvc.yaml -n trident
`

8. Import된 PVC 볼륨을 확인합니다. 
 <pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net8uz4wdg-master-1:/home/admindebian/trident-installer$ ./tridentctl import volume ontapnfs-user17 content_clone -f import-pvc.yaml -n trident
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
|                   NAME                   |  SIZE   | STORAGE CLASS | PROTOCOL |             BACKEND UUID             | STATE  | MANAGED |
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
| pvc-d1e07765-c416-11e9-8a78-005056a8832a | 5.0 GiB | netapp-csi    | file     | b9fefdec-5645-4ef4-95a6-e3d9f208bc63 | online | true    |
+------------------------------------------+---------+---------------+----------+--------------------------------------+--------+---------+
debian@net8uz4wdg-master-1:/home/admindebian/trident-installer$ kubectl get pvc -n ghost
NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
ghost-content     Bound    pvc-d1e07765-c416-11e9-8a78-005056a8832a   5Gi        RWO            netapp-csi     14s</code></pre>

> [Trident의 Legacy Volume Import Task](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_with_Trident/README.md)

 ## Step 3. Ghost 블로그 Container 실행   
1. Ghost deployment yaml 파일로 신규 Ghost 블로그 POD를 생성합니다. ([ghost_deployment.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/ghost_deployment.yaml))

    ` # kubectl create -f ghost_deployment.yaml -n ghost
`

3. Ghost Pod 정상 동작을 확인합니다. 
 <pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">debian@net8uz4wdg-master-1:/home/admindebian/trident-installer$ kubectl get pod -n ghost
NAME                    READY   STATUS    RESTARTS   AGE
ghost-75869fbd6-68ccd   1/1     Running   0          10m</code></pre>
3. Ghost 블로그에 할당된  Service IP 및 Port 확인을 확인합니다.  
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">
debian@net8uz4wdg-master-1:/home/admindebian/trident-installer$ kubectl get svc -n ghost
NAME    TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
ghost   LoadBalancer   10.255.100.23   115.144.174.247   80:31435/TCP   21h</code></pre>
4. 웹브라우저을 열어 http://EXTERNAL-IP 을 입력 후 Ghost 블로그 정상 동작 및 기존 데이터 Import 여부를 확인합니다.

![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/ghost_import.PNG)

[메인 메뉴로 이동](https://github.com/netappkr/NDX_Handsonworkshop-/)






<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5NDk0NTQ2OCwxOTA4NDg2ODE3LDM3OD
k2MjM2Miw5MjkxOTA1NTcsMTQ0NjU0MjM2MCwzOTQ0OTY0OTAs
LTc2NjEzODkwOSwtODkyMjk1MTg5LDIwNTg4MzMzOSwtOTY4Mz
g4OTUzLDc2MDc5ODk5OSwtMzg3NTI4NDg4LC0xMTAzNjQ4MjE5
LDE2OTk5NzQ1MzksLTE0Mjk4ODQzMCwtOTM1MzcyMzA0LDg3Nz
YzNTUyNl19
-->