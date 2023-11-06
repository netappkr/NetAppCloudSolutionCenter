# BlueXP 데이터 보호
BlueXP에서 Netapp SnapX 솔루션들과 연계하여 데이터를 보호합니다.

## NetApp SnapX 솔루션
Snapshot™, SnapMirror®, SnapLock®, SnapCenter® 및 SnapVault®와 같은 NetApp 독점 기술은 ONTAP 시스템 데이터를 보호하는 데 도움이 됩니다. 이러한 기능 중 일부를 자세히 살펴보겠습니다.

### NetApp Snapshot Tech
NetApp Snapshot 복사본은 ONTAP 볼륨에 저장된 데이터의 특정 시점, 불변, 증분 및 읽기 전용 복사본입니다. 스냅샷 복사본은 오버헤드가 낮으며 ONTAP 시스템에서 사용할 수 있는 고유한 WAFL(Write Anywhere File Layout) 기술을 사용하여 생성됩니다. BlueXP 스토리지 기능이 내장되어 있으므로 사용하기 전에 외부 통합이 필요하지 않습니다.

### SnapMirror
SnapMirror 데이터 복제를 사용하면 한 ONTAP 시스템에서 다른 ONTAP 시스템으로 스냅샷 복사본을 복제할 수 있습니다. 또한 백엔드에서 NetApp SnapDiff 기술을 사용하여 변경된 데이터만 식별하고 복제합니다. 이는 재해 복구, 데이터 마이그레이션 또는 동기화의 경우에 유용합니다. SnapMirror 복제 관계는 온프레미스, 하이브리드 또는 멀티클라우드 솔루션, BlueXP Cloud Volumes ONTAP 또는 FSx for ONTAP에서 호스팅되는지 여부에 관계없이 두 ONTAP 기반 시스템 간에 이루어질 수 있습니다.

### SnapVault
SnapVault는 규정 준수를 위해 ONTAP 시스템 간에 디스크 간 스냅샷 복사 복제를 수행하는 NetApp의 데이터 보관 솔루션입니다. SnapVault가 작동하려면 보조 ONTAP 시스템이 필요합니다. 기본 시스템에서 데이터가 손실된 경우 보조 ONTAP 시스템에서 데이터를 사용할 수 있으므로 빠른 복구가 가능합니다. 데이터는 디스크 간 보관 솔루션이고 데이터가 객체 스토리지로 이동되는 추가 보호 계층의 이점을 얻지 못하므로 소스와 동일한 형식으로 저장됩니다.

### SnapLock
NetApp SnapLock은 ONTAP 시스템에서 사용할 수 있는 업계 인증 WORM(Write Once, Read Many) 데이터 스토리지 기술입니다. WORM 스토리지는 데이터가 스토리지 볼륨에 지속되면 읽기 전용으로 설정하여 수정되거나 삭제되지 않도록 보장합니다. 이는 맬웨어 공격으로부터 보호하며 금융 거래, 의료 기록 및 기타 민감한 정보와 같이 법적 또는 규정 준수 요구 사항에 따라 보관해야 하는 데이터에 특히 유용합니다.

### SnapCenter
NetApp SnapCenter 소프트웨어는 NetApp ONTAP 스토리지 시스템에 저장된 데이터에 대한 중앙 집중식 백업 및 복구 서비스를 제공하는 데이터 보호 솔루션입니다. SnapCenter는 Oracle, SQL Server, SAP HANA와 같은 주요 엔터프라이즈 애플리케이션 및 데이터베이스에 대해 애플리케이션 일관성이 있는 데이터 보호 기능을 제공합니다. 스냅샷 복사본 관리, 보조 사이트에 데이터 복제, 재해 발생 시 데이터 복구를 위한 사용자 친화적인 인터페이스를 제공합니다.

## 실습 : BlueXP Data Protection 기능 살펴보기
- Step 1 : [Set_SnapMirror](./Set_SnapMirror.md)
- Step 2 ( hands on comming soon ) : [Application_bakcup](./Application_bakcup.md)
- Step 3 : [Backup_reporting](./Backup_reporting.md)

# Next
[![Next.png](./Images/Next.png)](../Data_Protection/Set_SnapMirror.md)

## 참고
- [bluexp-data-protection-using-snapx-solutions](https://bluexp.netapp.com/blog/cvo-blg-bluexp-data-protection-using-snapx-solutions)