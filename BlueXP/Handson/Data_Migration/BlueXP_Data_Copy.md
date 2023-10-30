# BlueXP Data Copy
BlueXP 에서 Cloud sync 서비스를 이용하여 Data를 migration 합니다.

## Data Blocker
## Data Broker 배포
1. BlueXP console을 엽니다.
2. managed Data Broker </br>
![Alt text](image.png)
3. Add New Data Broker </br>
![Alt text](image-1.png)
3. 
![Alt text](image-2.png)
4. use a CloudFormation
![Alt text](image-3.png)
5. CloudFormation </br>
![Alt text](image-4.png)</br>
6. Specify stack details
- VPC : 생성한 VPC
- subnet : public-subnet1
![Alt text](image-5.png)
7. Review DataBroker
![Alt text](image-6.png)