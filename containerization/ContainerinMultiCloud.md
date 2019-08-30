
이번 Task는 온프레미스내의 Ghost 블로그  Container을 AWS와 Azure로 이동합니다. 

**사전 준비사항** 
 - [ ] [오프레미스의 Legacy Application을 Container로 전환](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/OnPremcontainer.md)
 - [ ]  [CVO를 활용한 NKS + Trident 구성](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/NKSwithCVO.md)
  - [ ]  [Cloud Sync 구성](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Data_Mobility_MultiCloud/OnPremtoCloudStorage.md)
 
  ## Step 1. 온프레미스 Ghost POD 및 데이터를 AWS로 이동 
1. NKS에서 설치한 AWS K8SCluster 콘솔에 접속합니다. 

2. Service 생성될 ghost라는 namespace를 생성합니다.
     
      `# kubectl create namespace ghost`
     
3. AWS내에 설치된 K8SCluster에서 신규 PVC를 생성합니다. ([ghost_PVC.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/ghost_PVC.yaml))
     
     `# kubectl apply -f ghost_pvc.yaml -n ghost` 

      > [Trident 구성  후 신규 PVC 생성 과정](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md) 

4. PVC 생성된 것을 CVO GUI에서 확인합니다. 
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/cvo_pvc.PNG)

6. CloudSync GUI로 이동합니다.

7. Create New Sync Relationship을 클릭합니다.

8. 아래 정보를 기반으로 Relationship을 생성합니다.
     * Source: NFS Server 
     * Target: NFS Server 
     *  Enable data-in-flight encryption when syncing data? : No
     * Source NFS Server IP: 10.255.100.xx (SVM Data LIF)
     * Target NFS Server IP: 10.200.x.x ( CVO nfs Data LIF)
     * Source Volume Name :  On-Prem Cluster PVC 이름 확인
     *  Target Volume Name :  AWS Cluster 신규 PVC 이름 확인 
     
     > CVO의 Data LIF 정보는 Cloud Manager GUI에서 확인 가능 
     ![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/cvo_nfs_datalif.PNG)

9. 데이터 복제 완료 후 Sync Relationship을 삭제합니다. 
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/trident_cloudsync.PNG)
10. AWS K8SCluster 설치된 NKS GUI로 이동 후 My Charts를 통해 Ghost 블로그 Pod를 설치합니다. 
     * Solutions -> ADD SOLUTION -> My Charts -> Ghost 클릭
     * storageClassName: netapp-file
     * name: ghost-content 
     * Install 클릭 
 9. 설치 완료 후 해당 K8S Cluster Dashboard GUI 접속 후 Service IP을 확인합니다. 
     * Kubernetes Dashboard 클릭
     * Name Space: Ghost 선택
     * Services 클릭 
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/ghost_external_ip.PNG)
11. Ghost Service 내의 External end Points를 클릭하여 Ghost 블로그 POD 정상 동작을 확인합니다.     
![enter image description here](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/images/aws_ghost.PNG)

 ## Step 2. 온프레미스 Ghost POD 및 데이터를 Azure로 이동 
1. NKS에서 설치한 Azure K8SCluster 콘솔에 접속합니다. 

2. Service 생성될 ghost라는 namespace를 생성합니다.
     
      `# kubectl create namespace ghost`
     
3. Azure내에 설치된 K8SCluster에서 신규 PVC를 생성합니다. ([ghost_PVC.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/ghost_PVC.yaml))
     
     `# kubectl apply -f ghost_pvc.yaml -n ghost` 

4. PVC 생성된 것을 CVO GUI에서 확인합니다. 

6. CloudSync GUI로 이동합니다.

7. Create New Sync Relationship을 클릭합니다.

8. 아래 정보를 기반으로 Relationship을 생성합니다.
     * Source: NFS Server 
     * Target: NFS Server 
     *  Enable data-in-flight encryption when syncing data? : No
     * Source NFS Server IP: 10.255.100.xx (SVM Data LIF)
     * Target NFS Server IP: 10.100.x.x ( CVO nfs Data LIF)
     * Source Volume Name :  On-Prem Cluster PVC 이름 확인
     *  Target Volume Name :  Azure Cluster 신규 PVC 이름 확인 
     
9. 데이터 복제 완료 후 Sync Relationship을 삭제합니다. 

10. Azure K8SCluster 설치된 NKS GUI로 이동 후 My Charts를 통해 Ghost 블로그 Pod를 설치합니다. 
     * Solutions -> ADD SOLUTION -> My Charts -> Ghost 클릭
     * storageClassName: netapp-file
     * name: ghost-content 
     * Install 클릭 
 9. 설치 완료 후 해당 K8S Cluster Dashboard GUI 접속 후 Service IP을 확인합니다. 
     * Kubernetes Dashboard 클릭
     * Name Space: Ghost 선택
     * Services 클릭 
11. Ghost Service 내의 External end Points를 클릭하여 Ghost 블로그 POD 정상 동작을 확인합니다.     

<!--stackedit_data:
eyJoaXN0b3J5IjpbODMxOTY2Nzg4LC05MzQ3ODMwMzIsNDU4Mz
Q0NDAwLDIxNDExNjIyNzcsLTMxNTA4ODI1OSwtMTYxMDAyODc2
NywxMjEzNjg0MjgwLC0xNzAyMzQ1MTAzXX0=
-->