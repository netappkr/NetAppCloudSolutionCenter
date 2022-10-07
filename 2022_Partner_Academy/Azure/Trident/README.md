# Astra Trident
![Connecting containers to storage](https://netapp-trident.readthedocs.io/en/latest/_images/DynamicStorageProvisioningProcess.png)</br>
Astra Trident는 Astra 제품군 의 일부로 NetApp에서 유지 관리하는 완전히 지원되는 오픈 소스입니다. 
CSI(Container Storage Interface)와 같은 업계 표준 인터페이스를 사용하여 컨테이너화된 애플리케이션의 지속성 요구 사항을 충족할 수 있도록 설계되었습니다.

Astra Trident는 Kubernetes 클러스터에 포드로 배포하고 Kubernetes 워크로드에 대한 동적 스토리지 오케스트레이션 서비스를 제공합니다. 
이를 통해 컨테이너화된 애플리케이션은 ONTAP(NetApp ONTAP용 AFF/FAS/Select/Cloud/Amazon FSx), Element 소프트웨어(NetApp HCI/SolidFire), Astra Data Store를 비롯한 NetApp의 광범위한 포트폴리오에서 영구 스토리지를 빠르고 쉽게 사용할 수 있습니다. 
Azure NetApp Files 서비스 및 Google Cloud의 Cloud Volumes Service로 제공됩니다.

Astra Trident는 또한 NetApp의 Astra를 위한 기본 기술로, 스냅샷, 백업, 복제 및 복제를 위한 NetApp의 업계 최고의 데이터 관리 기술을 활용하여 Kubernetes 워크로드에 대한 데이터 보호, 재해 복구, 이식성 및 마이그레이션 사용 사례를 해결합니다.

# 참조
- [Astra Trident](https://docs.netapp.com/us-en/trident/trident-concepts/intro.html#supported-kubernetes-cluster-architectures)
- [Trident on Kubernetes](https://netapp-trident.readthedocs.io/en/latest/dag/kubernetes/concepts_and_definitions.html)