# Ontap Data Tiering
비활성 데이터를 저렴한 개체 스토리지로 자동 계층화하여 스토리지 비용을 절감합니다. 활성 데이터는 고성능 SSD 또는 HDD에 남아 있고, 비활성 데이터는 저렴한 개체 스토리지에 계층화되어 있습니다. 이를 통해 기본 스토리지의 공간을 회수하고 보조 스토리지를 축소할 수 있습니다.

![diagram_data_tiering](https://docs.netapp.com/us-en/bluexp-cloud-volumes-ontap/media/diagram_data_tiering.png)

# Data tiering in AWS
AWS에서 데이터 계층화를 활성화하면 Cloud Volumes ONTAP은 EBS를 핫 데이터의 성능 계층으로 사용하고 AWS S3를 비활성 데이터의 용량 계층으로 사용합니다.

## Performance tier
성능 계층은 범용 SSD(gp3 또는 gp2) 또는 프로비저닝된 IOPS SSD(io1)일 수 있습니다.
처리량 최적화 HDD(st1)를 사용하는 경우 데이터를 개체 스토리지로 계층화하는 것은 권장되지 않습니다.

## Capacity tier
Cloud Volumes ONTAP 시스템은 비활성 데이터를 단일 S3 버킷으로 계층화합니다.
BlueXP는 각 작업 환경에 대해 단일 S3 버킷을 생성하고 이름을 fabric-pool- cluster 고유 식별자로 지정합니다 . 각 볼륨마다 다른 S3 버킷이 생성되지 않습니다.
BlueXP는 S3 버킷을 생성할 때 다음 기본 설정을 사용합니다.

- 보관 등급: 표준
- 기본 암호화: 비활성화됨
- 공개 접근 차단: 모든 공개 접근을 차단합니다.
- 객체 소유권: ACL 활성화됨
- 버킷 버전 관리: 비활성화됨
- 객체 잠금: 비활성화됨

## Volume tiering policies
일부 계층화 정책에는 데이터가 "콜드"로 간주되어 용량 계층으로 이동하기 위해 볼륨의 사용자 데이터가 비활성 상태로 유지되어야 하는 시간을 설정하는 연관된 최소 냉각 기간이 있습니다. 
냉각 기간은 데이터가 집계에 기록될 때 시작됩니다.

> ### Tips
> 최소 냉각 기간과 기본 집계 임계값인 50%를 변경할 수 있습니다(자세한 내용은 아래 참조). 
> - [냉각 기간을 변경하는 방법](http://docs.netapp.com/ontap-9/topic/com.netapp.doc.dot-mgng-stor-tier-fp/GUID-AD522711-01F9-4413-A254-929EAE871EBF.html)
> - [임계값을 변경하는 방법](http://docs.netapp.com/ontap-9/topic/com.netapp.doc.dot-mgng-stor-tier-fp/GUID-8FC4BFD5-F258-4AA6-9FCB-663D42D92CAA.html)

### Snapshot Only
집계 용량이 50%에 도달하면 Cloud Volumes ONTAP은 활성 파일 시스템과 연결되지 않은 스냅샷 복사본의 콜드 사용자 데이터를 용량 계층으로 계층화합니다. 냉각 기간은 약 2일입니다.

읽으면 용량 계층의 콜드 데이터 블록이 핫 데이터 블록이 되어 성능 계층으로 이동됩니다.

### All
모든 데이터(메타데이터 제외)는 즉시 콜드 상태로 표시되고 가능한 한 빨리 객체 스토리지에 계층화됩니다. 볼륨의 새 블록이 차가워질 때까지 48시간을 기다릴 필요가 없습니다. All 정책이 설정되기 전에 볼륨에 있는 블록이 콜드 상태가 되기까지 48시간이 소요됩니다.

읽으면 클라우드 계층의 콜드 데이터 블록은 콜드 상태로 유지되며 성능 계층에 다시 기록되지 않습니다. 이 정책은 ONTAP 9.6부터 사용할 수 있습니다.

### Auto
집계 용량이 50%에 도달하면 Cloud Volumes ONTAP은 볼륨의 콜드 데이터 블록을 용량 계층으로 계층화합니다. 콜드 데이터에는 스냅샷 복사본뿐만 아니라 활성 파일 시스템의 콜드 사용자 데이터도 포함됩니다. 냉각 기간은 약 31일입니다.

이 정책은 Cloud Volumes ONTAP 9.4부터 지원됩니다.

무작위 읽기로 읽는 경우 용량 계층의 콜드 데이터 블록은 핫 상태가 되어 성능 계층으로 이동합니다. 인덱스 및 바이러스 백신 검사와 관련된 순차 읽기로 읽는 경우 콜드 데이터 블록은 콜드 상태로 유지되며 성능 계층으로 이동하지 않습니다.

### None
볼륨의 데이터를 성능 계층에 유지하여 용량 계층으로 이동하는 것을 방지합니다.

볼륨을 복제할 때 데이터를 객체 스토리지로 계층화할지 여부를 선택할 수 있습니다. 그렇게 하면 BlueXP는 데이터 보호 볼륨에 백업 정책을 적용합니다. Cloud Volumes ONTAP 9.6부터 모든 계층화 정책이 백업 정책을 대체합니다.

## Turning off Cloud Volumes ONTAP impacts the cooling period
냉각 스캔을 통해 데이터 블록이 냉각됩니다. 이 과정에서 사용되지 않은 블록의 블록 온도는 다음으로 낮은 값으로 이동(냉각)됩니다. 기본 냉각 시간은 볼륨 계층화 정책에 따라 다릅니다.
- Auto: 31일
- Snapshot Only: 2일


## 참조
- [BlueXP tiering technical FAQ](https://docs.netapp.com/us-en/bluexp-tiering/faq-cloud-tiering.html#bluexp-tiering-service)