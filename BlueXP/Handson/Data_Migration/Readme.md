# BlueXP copy and sync
NetApp BlueXP 복사 및 동기화 서비스는 클라우드 또는 온프레미스의 모든 대상으로 데이터를 마이그레이션하는 간단하고 안전하며 자동화된 방법을 제공합니다. </br>
파일 기반 NAS 데이터세트(NFS 또는 SMB), Amazon Simple Storage Service(S3) 개체 형식, NetApp StorageGRID® 어플라이언스 또는 기타 클라우드 공급자 개체 저장소 등 무엇이든 ```BlueXP copy and sync```를 통해 변환하고 이동할 수 있습니다.

![diagram_cloud_sync_overview](https://docs.netapp.com/us-en/bluexp-copy-sync/media/diagram_cloud_sync_overview.png)

## BlueXP copy and sync 비용
BlueXP 복사 및 동기화 사용과 관련된 비용에는 리소스 요금과 서비스 요금이라는 두 가지 유형이 있습니다.

### 컴퓨팅 비용
리소스 요금은 클라우드에서 하나 이상의 데이터 브로커를 실행하기 위한 컴퓨팅 및 스토리지 비용과 관련됩니다.

### 서비스 금액
14일 무료 평가판이 종료된 후 동기화 관계 비용을 지불하는 방법에는 두 가지가 있습니다. 첫 번째 옵션은 AWS 또는 Azure에서 구독하는 것으로, 이를 통해 시간별 또는 연간 요금을 지불할 수 있습니다. 두 번째 옵션은 NetApp에서 직접 라이센스를 구입하는 것입니다.

> ### Tips
> 지속적인 동기화가 아닌 one time 작업을 고려하신다면 무료 라이선스를 적극 활용하세요

## 실습 : BlueXP에서 AWS s3 데이터를 CVO로 가져오기
- Info : [Read me](./Readme.md)
- Step 1 : [Create_Data_Broker](./Create_Data_Broker.md)
- Step 2 : [Deploy_BlueXP_connector](./Create_Sync_relationship.md)
- Step 3 : [Sync_report](./Sync_report.md)

# Next
[![Next.png](./Images/Next.png)](./Create_Data_Broker.md)


# 참고
- [copy and sync FAQ](https://docs.netapp.com/us-en/bluexp-copy-sync/faq.html#getting-started)