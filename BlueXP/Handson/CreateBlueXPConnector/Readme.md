# BlueXP Connector
BlueXP Connector는 클라우드 네트워크 또는 온프레미스 네트워크에서 실행되는 NetApp 소프트웨어입니다. 데이터 인프라를 관리하기 위해 BlueXP가 수행해야 하는 작업을 실행합니다. 커넥터는 수행해야 하는 모든 작업에 대해 BlueXP SaaS 계층을 지속적으로 폴링합니다. BlueXP를 시작하는 데에는 커넥터가 필요하지 않지만 모든 BlueXP 기능과 서비스를 잠금 해제하려면 커넥터를 만들어야 합니다.

# When a Connector is required
Standard 모드에서 BlueXP를 사용하는 경우 BlueXP의 다음 기능과 서비스에 커넥터가 필요합니다.

- Amazon FSx for ONTAP management features
- Amazon S3 storage
- Azure Blob storage
- Backup and recovery
- Classification
- Cloud Volumes ONTAP
- Disaster recovery
- E-Series systems
- Economic efficiency 1
- Edge caching
- Google Cloud Storage buckets
- Kubernetes clusters
- Migration reports
- On-premises ONTAP cluster integration with BlueXP data services
- Operational resiliency 1
- StorageGRID systems
- Tiering
- Volume caching

# Standard mode
다음 이미지는 Standard mode 배포의 예입니다.

![diagram-standard-mode.png](https://docs.netapp.com/us-en/bluexp-setup-admin/media/diagram-standard-mode.png)

## 실습 : BlueXP 배포
- Step 1 : [Add_AWS_Credentinal](./Add_AWS_Credentinal.md)
- Step 2 : [Deploy_BlueXP_connector](./Deploy_BlueXP_connector.md)

# 참조
- [concept BlueXP connectors](https://docs.netapp.com/us-en/bluexp-setup-admin/concept-connectors.html)
- [concept BlueXP deploy modes](https://docs.netapp.com/us-en/bluexp-setup-admin/concept-modes.html)