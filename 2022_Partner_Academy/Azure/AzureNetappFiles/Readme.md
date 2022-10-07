# Azure NetApp Files
Azure NetApp Files를 사용하면 기업이 클라우드를 리팩터링할 필요 없이 성능 집약적이고 대기 시간에 민감한 핵심 비즈니스 크리티컬 애플리케이션을 Azure에서 마이그레이션하고 실행할 수 있습니다.

![ANFusecase](https://learn.microsoft.com/en-us/azure/media/azure-netapp-files/solution-architecture-categories.png)
## 특징
- 여러 프로토콜에 대한 지원을 통해 Linux 및 Windows 애플리케이션의 "lift & shift"가 Azure에서 원활하게 실행될 수 있습니다.
- 여러 성능 계층을 통해 워크로드 성능 요구 사항과 긴밀하게 조정할 수 있습니다.
- SAP HANA, GDPR 및 HIPAA를 비롯한 주요 인증을 통해 가장 까다로운 워크로드를 Azure로 마이그레이션할 수 있습니다.

# 목록
- [Cloudmanager 배포](./Deploy_Cloudmanager.md)
- Azure Netapp Files 생성
    - [cloudmanager에서 ANF 생성](./CreateAzureNetappFiles.md)
    - [Azure potal에서 ANF 생성](./CreateAzureNetappFilesonAzure.md)
- [볼륨 생성](./CreateVolmeinAzure.md)
- [AzuerNetappFiles 설정](./VolumeOperation.md)
- [백업 및 복구](./VolumeBackupAndRestore.md)
