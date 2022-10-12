# 2022 Partner Academy Cloud Hands-on
본 과정에서는 Spot Ocean과 Azure Netapp Files를 이용하여 다양한 서비스들을 배포하고 설정합니다.
이 과정에서 이용할 수 있는 솔루션의 기능에 대해 소개합니다.

## 구성도
![test](./Images/myplan.png)

# 절차
1. [Hands on Lab 배포](./Quickstart/Quickstart.md)
2. [클라우드매니저 배포](./AzureNetappFiles/Deploy_Cloudmanager.md) 
3. [Azure Netapp Files](./AzureNetappFiles/Readme.md) </br>
  3-1. [Azure 콘솔에서 Azure Netapp Files 생성](./AzureNetappFiles/CreateAzureNetappFilesonAzure.md) </br>
4. [Azure NetApp Files에 NFS 볼륨 생성](./AzureNetappFiles/CreateVolmeinAzure.md)
5. [엘라스틱그룹으로 가져오기](./Elasticgroup/CreateElasticgroup.md)
6. [트라이던트 생성](./Trident/README.md)</br>

6. [Deploy testapp](./Trident/deploy_testapp.md)
7. [Workload Migration](./OceanforAKS/WorkloadMigration.md)
8. [Ocean Features & Concept](https://docs.spot.io/ocean/features/)</br>
  8-1. [Scaling event](./OceanforAKS/ScalingEvent.md)</br>
  8-2. [Headroom](./OceanforAKS/Headroom.md)</br>
  **번외**</br>
  8-3. [Right Sizing](./OceanforAKS/RightSizing.md)</br>
  8-4. [Cost Analysis](./OceanforAKS/CostAnalysis.md)</br>
9. [AZure Netapp Files](./AzureNetappFiles/Readme.md)</br>
  9-1. [Create Volume](./AzureNetappFiles/CreateVolmeinAzure.md)</br>
  9-2. [Volume Operation](./AzureNetappFiles/VolumeOperation.md)</br>
  9-3. [Volume Backup & restore](./AzureNetappFiles/VolumeBackupAndRestore.md)</br>
  9-4. [Import volume to AKS](./Trident/ImportVolumeToAKS.md) </br>
  **번외**</br>
  9-5. [stateful pod](./FSXforOntap/K8SWithFSxOntap_Stateful.md)

