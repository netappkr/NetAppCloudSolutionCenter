# BlueXP에서 FSxN Volume 생성
```AWS console```에서 설정 할 수 없거나 ```Ontap CLI```를 통해서 설정했던 항목을 BlueXP console을 통해 손쉽게 설정 및 관리합니다.

## FlexGroup Volume 생성
AWS web Console에서는 FlexVolume 생성만 지원합니다.</br>
BlueXP를 통해 100Tib 이상 크기의 볼륨을 생성 할 수 있습니다.

1. [BlueXP console](https://cloudmamager.netapp.com)에 접속합니다.
2. ```Canvas```에서 FSxN 을 클릭합니다.
![Alt text](./Images/Create_Volume-0.png)
2. View Volumes
![Alt text](./Images/Create_Volume-1.png)
3. Add Volume
![Alt text](./Images/Create_Volume-2.png)

4. Volume details, protection & tags
- Optimization option : [X] Distribute volume data across the cluster (FlexGroup)
![Alt text](./Images/Create_Volume-3.png)

5. Volume Protocal</br>
```AWS web Console```에서는 Volume 생성 시 ```CIFS share point``` 생성 설정을 지원하지 않습니다.
![Alt text](./Images/Create_Volume-4.png)

6. Usage Profile & Tiering Policy
![Alt text](./Images/Create_Volume-5.png)
    a. Volume distribution
    ![Alt text](./Images/Create_Volume-6.png)

7. review</br>
![Alt text](./Images/Create_Volume-7.png)

8. 잠시 후 FlexGroup 볼륨이 생성됩니다.</br>
![Alt text](./Images/Create_Volume-8.png)

9. Manage Volume</br>
![Alt text](./Images/Create_Volume-9.png)

10. mount command</br>
![Alt text](./Images/Create_Volume-10.png)

11. Bastion host에 접속합니다.
12. 생성 한 볼륨을 마운트 합니다.

```bash
sudo mkdir -p /storage/fsxn/cifs/fsx_cifs_share
sudo mount -t cifs -o user='admin',password='Netapp1!' //172.30.3.30/fsx_cifs_share /storage/fsxn/cifs/fsx_cifs_share
```

13. 마운트한 볼륨을 확인합니다.
```bash
[root@ip-172-30-0-12 /]# df -h
Filesystem                    Size  Used Avail Use% Mounted on
//172.30.3.30/fsx_cifs_share  190T  190T  852G 100% /storage/fsxn/cifs/fsx_cifs_share
```