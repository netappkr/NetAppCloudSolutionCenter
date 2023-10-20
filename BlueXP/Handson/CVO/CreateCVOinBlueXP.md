# BlueXP를 통해 Cloud Volume Ontap 생성
BlueXP를 통해 Demo에 사용할 CVO를 손쉽게 배포할 수 있습니다.

## Quick Start
1. __Add Working Enviroment__ </br>
![Alt text](./Images/CreateCVOinBlueXP-0.png)
2. Choose a Location </br>
![Alt text](./Images/CreateCVOinBlueXP-1.png)
3. Details and Credentials </br>
![Alt text](./Images/CreateCVOinBlueXP-2.png)
4. Services </br>
![Alt text](./Images/CreateCVOinBlueXP-3.png)
5. Location & Connectivity </br>
![Alt text](./Images/CreateCVOinBlueXP-4.png)
6. Data Encryption </br>
![Alt text](./Images/CreateCVOinBlueXP-5.png)
7. Cloud Volumes ONTAP Charging Methods & NSS Account </br>
![Alt text](./Images/CreateCVOinBlueXP-6.png)
8. Preconfigured Packages </br>
![Alt text](./Images/CreateCVOinBlueXP-7.png)

__Tips__
<details>
    <summary>HDD로 배포</summary>

<!-- summary 아래 한칸 공백 두고 내용 삽입 -->
## HDD 볼륨을 배포하여 유지비 절약
aws ```gp2```나 ```gp3``` type의 볼륨이 아닌 ```st1``` type을 사용하도록 설정합니다.
이 경우 Tiring 기능을 선택할 수 없습니다.
8. Preconfigured Packages </br>
![Alt text](./Images/CreateCVOinBlueXP-7-1.png)
9. IAM Role </br>
![Alt text](./Images/CreateCVOinBlueXP-8.png)
10. Licensing </br>
![Alt text](./Images/CreateCVOinBlueXP-9.png)
11. Underlying Storage Resources </br>
![Alt text](./Images/CreateCVOinBlueXP-10.png)
12. Underlying Storage Configuration </br>
![Alt text](./Images/CreateCVOinBlueXP-11.png)
13. WORM (write once, read many) </br>
![Alt text](./Images/CreateCVOinBlueXP-12.png)
</details>

14. volume </br>
![Alt text](./Images/CreateCVOinBlueXP-13.png)
15. CIFS Setup </br>
Cloudformation > ADStack
![Alt text](./Images/CreateCVOinBlueXP-14.png)
![Alt text](./Images/CreateCVOinBlueXP-15.png)

<details>
    <summary>POC용 표준 배포</summary>

16. Create Volume - Usage Profile Disk Type & Tiering Policy </br>
![Alt text](./Images/CreateCVOinBlueXP-16.png)
</details>
<details>
    <summary>HDD로 배포</summary>

16. Create Volume - Usage Profile Disk Type & Tiering Policy </br>
![Alt text](./Images/CreateCVOinBlueXP-18.png)
</details>


17. Review & Apporve </br>
![Alt text](./Images/CreateCVOinBlueXP-17.png)