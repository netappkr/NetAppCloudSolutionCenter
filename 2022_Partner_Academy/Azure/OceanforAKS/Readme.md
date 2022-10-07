# Ocean for Azure Kubernetes Service
일반적인 K8S와 달리 AKS는 몇가지 제약조건이 있습니다.

# AWS
달리 명시되지 않는 한 이 섹션에 설명된 모든 기능은 Ocean for AWS에서 지원됩니다.

# AKS
AKS와 함께 사용할 몇 가지 Ocean 기능을 추가하는 중입니다. 현재 지원되는 주요 기능은 다음과 같습니다.

- Scaling for Kubernetes
- Headroom
- Right Sizing
- Labels and Taints
- Virtual Node Groups

> ### AKS 참고:
> - Ocean은 Azure 계정에서 작업을 시작합니다. 이러한 작업은 계정에 제공된 Azure 구독 제한 및 할당량 에 의해 제한됩니다.
> - AKS용 Ocean은 현재 Linux 기반 노드 풀 가져오기만 지원합니다.

# 목록
 - [Connect An AKS Cluster](./ConnectAnAKSCluster.md)
 - [Workload Migration](./WorkloadMigration.md)
 - [Scaling Event](./ScalingEvent.md)
 - [Headroom](./Headroom.md)
 - [Right Sizing](./RightSizing.md)
 
# 참조
- [Spot doc](https://docs.spot.io/ocean/features/)