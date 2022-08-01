[[_TOC_]]

# ECS 란?
- > Amazon Elastic Container Service(Amazon ECS)는 클러스터에서 컨테이너를 손쉽게 실행, 중지 및 관리할 수 있게 하는 컨테이너 관리 서비스입니다.` 
- `K8S와 같은 컨테이너 관리 서비스로서 AWS가 개발 관리합니다.`
ecs 동작방식에 대한 자세한 내용은 [여기](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/Welcome.html)서 확인 하실 수 있습니다.
#구성도
![image.png](/.attachments/image-972a7457-7ad3-4fc3-a3fe-d84755282e89.png)

##ECS cli 설치 및 구성
ecs-cli configure profile --profile-name netapp_wyahn --access-key AKIAQRRGCXHYLLBVGIRS --secret-key 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
ecs-cli configure --cluster wyahn-ecs-spot --region ap-northeast-2 --default-launch-type FARGATE --config-name wyahn-ecs-spot
ecs-cli configure default --config-name netapp_wyahn

#Test 환경 구성
https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/ecs-cli-tutorial-fargate.html
task-execution-assume-role.json
```yaml
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
``` bash
$ aws iam --region ap-northeast-2 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://task-execution-assume-role.json
$ aws iam --region ap-northeast-2 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```
##서비스 생성
```
vim docker-compose.yml
```
```yaml
version: '3'
services:
  web:
    image: amazon/amazon-ecs-sample
    ports:
      - "80:80"
    logging:
      driver: awslogs
      options: 
        awslogs-group: wyahn-ecs
        awslogs-region: ap-northeast-2
        awslogs-stream-prefix: web
```

##상세옵션 지정
```bash
$ vi ecs-params.yml
```
```yaml
version: 1
task_definition:
  task_execution_role: ecsTaskExecutionRole
  ecs_network_mode: awsvpc
  task_size:
    mem_limit: 0.5GB
    cpu_limit: 256
run_params:
  network_configuration:
    awsvpc_configuration:
      subnets:
        - "subnet-04eb9f7e9d69dfaf7"
        - "subnet-0d8b67c078792059a"
      security_groups:
        - "sg-004770f948989c33b"
```

##클러스터에 Compose 파일 배포
compose 파일을 생성한 후 ecs-cli compose service up을 사용하여 클러스터에 배포할 수 있습니다. 
기본적으로 이 명령은 현재 디렉터리에서 docker-compose.yml 및 ecs-params.yml이라는 파일을 찾습니다. 
하지만 --file 옵션을 사용하여 다른 Docker compose 파일을 지정하고 --ecs-params 옵션을 사용하여 다른 ECS Params 파일을 지정할 수 있습니다. 
이 명령을 통해 생성된 리소스에는 기본적으로 제목에 현재 디렉터리가 포함되어 있지만 --project-name 옵션을 사용하여 이를 재정의할 수 있습니다. 
--create-log-groups 옵션은 컨테이너 로그를 위한 CloudWatch 로그 그룹을 만듭니다.

```bash
$ ecs-cli compose --project-name wyahn-tutorial service up --create-log-groups --file docker-compose.yml --ecs-params ecs-params.yml
```
![ecs compose.png](/.attachments/ecs%20compose-bf0514bd-e9ad-46c3-9064-b661a2910bb4.png)


##로드 밸런서에 서비스 연결
로드벨런서 연결 시 미리 만든 tg 와 연결하는 방식을 사용합니다.
[로드벨런서에 서비스 연결 ](https://stackoverflow.com/questions/60584656/how-to-register-multiple-target-groups-via-aws-ecs-cli-service-command)

```bash
$ ecs-cli compose --project-name wyahn-tutorial service up \
--target-groups "targetGroupArn=arn:aws:elasticloadbalancing:ap-northeast-2:037660834288:targetgroup/ECS-WEB/8e857f02e29045a2,containerPort=80,containerName=web" \
--create-log-groups 
```
![targetgroup.png](/.attachments/targetgroup-c46f300c-95e4-404d-9823-885c2e79fb0d.png)
![console-targetgroup.png](/.attachments/console-targetgroup-e369bb62-d098-4965-9314-fa296b330362.png)
> ecs-cli compose --project-name wyahn-tutorial service ps

>###[ 로그보기 ]
>ecs-cli logs --task-id 9511444acc684d0d9f608b9d0709d971 --follow
>### [ 태스크 규모 조정 ]
> ecs-cli compose --project-name wyahn-tutorial service scale 2 


# 참조
---
[자습서: Amazon ECS CLI를 사용하여 Fargate 태스크가 있는 클러스터 생성 ](https://docs.aws.amazon.com/ko_kr/AmazonECS/latest/developerguide/ecs-cli-tutorial-fargate.html)






