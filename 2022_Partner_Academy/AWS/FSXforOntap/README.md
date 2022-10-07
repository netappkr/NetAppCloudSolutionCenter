# Amazon FSx for NetApp ONTAP
Amazon FSx for NetApp ONTAP은 ONTAP의 데이터 액세스 및 관리 기능을 제공하는 AWS 클라우드 기반의 인기 있는 완전관리형 공유 스토리지를 제공합니다.

## 특징
- AWS에서 ONTAP의 데이터 엑세스 및 데이터 관리 기능을 통해 애플리케이션을 더욱 빠르게 마이그레이션하고 구축할 수 있습니다.
- 업계 표준 NFS,SMB 및 iSCSI 프로토콜을 통해 다양한 워크로드 및 사용자에 데이터를 사용할 수 있습니다.
- 자동으로 확장 및 축소되는 스토리지 용량으로, 증가하는 데이터 집합을 지원합니다.
- 내장된 스토리지 효율성(storage efficiency) 및 계층화(Tiearing) 기술과 함께, 적은 비용으로 SSD 성능을 활용 할 수 있습니다.
# 작동방식
![fsxontap](https://d1.awsstatic.com/FSXN%402x.72d7f1b119ec9438a370775830648c5f1f362db7.png)

# Demo
<!-- 
<video width="800" height="600" controls>
    <source src="https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/FSxontap+demo.mp4" type="video/mp4">
</video>
-->
[![Demo](https://media.amazonwebservices.com/blog/2021/fsx_ontap_choice_1.png)](https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/FSxontap+demo.mp4)
## Workshop
- [Deploy Cloudmanager](./DeployCloudmanager.md)
- [Create FSX ontap](./CreateFSXontap.md)
- [Create Volume](./CreateVolume.md)
- [Storage Efficiency](./StorageEfficiency.md)
- [Volume Backup & restore](./VolumeBackupAndRestore.md)
- [Import Volume to EKS](./ImportVolumeToEKS.md)