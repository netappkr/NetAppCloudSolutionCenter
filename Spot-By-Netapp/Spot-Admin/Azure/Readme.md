# Spot by Netapp Admin Cloud Hands-on
Spot by Netapp 관리자 Azure Hands on 가이드 입니다.
본 과정에서는 Spot by Netapp 계정 연동, Elastigroup, Ocean의 기능들을 실습할 수 있습니다.

## 실습 전 필요사항

- Azure 구독 </br>
Azure Resource Manager Templeate을 이용하여 실습환경을 배포합니다.</br>
안타깝게도 본 과정에서는 실습에 필요한 클라우드 인프라 사용 비용을 지불해드리지 않습니다.

- Administartor 권한 </br>
본과정에서는 EC2, IAM, EKS, Billing, S3 자원에 대한 CRUD 권한이 필요합니다.

## 실습환경 배포

실습 전 Hands on 환경을 미리 배포해주세요. </br>
[빠른시작 Spot by Netapp Amdin Hands on](./QuickStart/CreateLabQuickstartGuide.md)

## 구성도
![SpotAzureAdmin](./Images/SpotAzureAdmin.png)

# 절차
1. [Hands on Lab 배포](./Quickstart/Quickstart.md)
2. [클라우드매니저 배포](./AzureNetappFiles/Deploy_Cloudmanager.md) 
3. [Azure Netapp Files](./AzureNetappFiles/Readme.md) </br>
  3-1. [Azure 콘솔에서 Azure Netapp Files 생성](./AzureNetappFiles/CreateAzureNetappFilesonAzure.md) </br>
4. [Azure NetApp Files에 NFS 볼륨 생성](./AzureNetappFiles/CreateVolmeinAzure.md)
5. [엘라스틱그룹으로 가져오기](./Elasticgroup/CreateElasticgroup.md)
6. [AZure Netapp Files](./AzureNetappFiles/Readme.md)</br>
  6-1. [Volume Operation](./AzureNetappFiles/VolumeOperation.md)</br>
  6-2. [Volume Backup & restore](./AzureNetappFiles/VolumeBackupAndRestore.md)</br>


