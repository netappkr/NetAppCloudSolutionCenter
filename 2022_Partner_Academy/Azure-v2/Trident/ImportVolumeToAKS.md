# 볼륨 가져오기
tridentctl import를 사용하여 기존 스토리지 볼륨을 Kubernetes PV로 가져올 수 있습니다.

## 볼륨 가져오기를 지원하는 드라이버

|Driver	|Release|
|-----|---|
|ontap-nas | 22.07|
|ontap-nas-flexgroup|22.07|
|solidfire-san| 22.07|
|aws-cvs | 22.07|
|azure-netapp-files | 22.07|
|gcp-cvs | 22.07|
|ontap-san| 22.07|

## 볼륨 가져오기

PVC 파일은 볼륨 가져오기 프로세스에서 기존 볼륨을 PV로 정의하는 데 사용됩니다. 다음 예와 같이 PVC 파일에는 name, namespace, accessModes 및 storageClassName 필드가 포함되어야 합니다.

1. bastionhost에서 pvc.yaml파일을 작성합니다.
    - vim import-volume-pvc.yaml
    ```yaml
    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: nginx-filebrowser-vol
      namespace: default
      annotations:
        trident.netapp.io/unixPermissions: "0775"
    spec:
      accessModes:
        - ReadWriteMany
      storageClassName: handson-anf-premium
    ```

2. tridentctl import 명령으로 볼륨을 EKS로 가져옵니다.
- $ tridentctl import volume <'backendName'> <'volumeName'> -f <'path-to-pvc-file'>
    ```bash
    root@HandsonBastion-vm:/opt/DeployTestapp/ImportVolume# tridentctl import volume Handson-ANF NginxFilebrowser-restore -f import-volume-pvc.yaml -n trident
    +------------------------------------------+---------+---------------------+----------+--------------------------------------+--------+---------+
    |                   NAME                   |  SIZE   |    STORAGE CLASS    | PROTOCOL |             BACKEND UUID             | STATE  | MANAGED |
    +------------------------------------------+---------+---------------------+----------+--------------------------------------+--------+---------+
    | pvc-4c8b1d0c-626a-4bfc-a74b-477a7737dad5 | 100 GiB | handson-anf-premium | file     | 1c27fcb4-7b1e-4bc7-af38-c873d6f9e8bc | online | true    |
    +------------------------------------------+---------+---------------------+----------+--------------------------------------+--------+---------+
    ```
    [root@ip-172-31-0-48 trident-installer]# tridentctl import volume Hands-on-fsx-svm NginxBrowserVol -f import-volume-pvc.yaml -n trident

- 가져오기에 성공하면 Volume 이름이 'PVC-난수' 로 변경됩니다.
![ImportBeforeAfter](./images/ImportBeforeAfter.png)
-  kubectl get pvc
    ```bash
    root@HandsonBastion-vm:/opt/DeployTestapp/ImportVolume# k get pvc
    NAME                    STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS           AGE
    handson-anf-premium     Bound    pvc-9b1d2b50-70c5-49ff-bf0c-a0ca0f6eaefd   100Gi      RWX            handson-anf-premium    7m13s
    handson-anf-standard    Bound    pvc-8a592a36-ecee-4169-a6c7-0c74940ec6a8   100Gi      RWX            handson-anf-standard   7m13s
    nginx-filebrowser-vol   Bound    pvc-4c8b1d0c-626a-4bfc-a74b-477a7737dad5   100Gi      RWX            handson-anf-premium    97s
    ```

3. NginxBrowser app에 가져온 볼륨 연결
- nginx-file-browser 정의 파일을 열고 claimName을 NginxBrowserVol으로 변경합니다.
/opt/testapp/nginx-file-browser-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx-file-bro
  name: nginx-file-bro
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-file-bro
  template:
    metadata:
      labels:
        app: nginx-file-bro
    spec:
      containers:
      - image: docker.io/mohamnag/nginx-file-browser:latest
        name: nginx-file-browser
        volumeMounts:
        - mountPath: /opt/www/files
          name: anf-volume

      volumes:
      - name: anf-volume
        persistentVolumeClaim:
          claimName: nginx-filebrowser-vol #변경
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - operator: In
                key: purpose
                values:
                - test
```
- k apply -f /opt/DeployTestapp/nginx-file-browser/nginx-file-browser-deployment.yaml
4. 적용여부를 브라우저에서 확인합니다.
- k get svc 명령을 통해 확인한 주소를 복사하고 브라우저에 붙여넣습니다.
```
root@HandsonBastion-vm:/opt/DeployTestapp/nginx-file-browser/AKS# k get svc
NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)        AGE
kubernetes           ClusterIP      10.0.0.1      <none>         443/TCP        3d9h
nginx-file-bro-svc   LoadBalancer   10.0.18.136   20.249.49.32   80:30394/TCP   49s
```
- 브라우저에 현재 볼륨에 있는 파일들을 확인 할 수 있습니다.

- Bastionhost에서 NFS 볼륨에 파일을 다운로드 합니다. 
```bash
[root@ ~ ]# cd /ANF/NginxFileBrowserRestore/
[root@ ~ ]# wget https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/DeployTestapp/Thankyouforyou.png
```
- 브라우저를 새로고침하고 Thankyouforyou.png를 클릭합니다.
![finish](./Images/finish1.png)


## 결과
기존 볼륨을 AKS의 PV로 등록하여사용할 수 있었습니다.


# 다음과정
AKS와 fsxontap을 활용한 statfulpod 구성에 대해 알아봅니다.</br>
- 이전주제: [Volume Backup & restore](../AzureNetappFiles/VolumeBackupAndRestore.md)

# 참조
- [Netapp Doc Import volumes](https://docs.netapp.com/us-en/trident-2110/trident-use/vol-import.html#how-does-the-import-work)