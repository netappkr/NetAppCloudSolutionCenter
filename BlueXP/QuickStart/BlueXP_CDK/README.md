## 명령어

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


## CDK Python 코드 작성
[CDK Python example](https://github.com/aws-samples/aws-cdk-examples)

## CDK asset download
```
aws s3 cp s3://cdk-hnb659fds-assets-037660834288-ap-northeast-2/* ./
```

## CDK Cheat Sheet
```powershell 
aws configure list-profiles
```
```powershell
PS BlueXP_CDK> aws configure list-profiles
default
user1
cds-user-01
```
- ```cdk deploy --require-approval never --profile cds-user-01```
- ```cdk deploy {스택이름} --require-approval never --profile cds-user-01```
- ```cdk deploy --all --profile cds-user-01 --parameters prefix=test```
- ```cdk synth --profile cds-user-01 --parameters prefix=test --parameters creator=wyahn```
#### CDK destory
- ```cdk destroy --all --force --profile cds-user-01```

#### CDK stack list
- ```cdk list```
#### CDK config review
- ```cdk diff```

### CDK 출력 디렉터리 지정
--output( ) 옵션을 추가하면 -o합성된 템플릿을 가 아닌 다른 디렉토리에 쓸 수 있습니다 cdk.out.
```cdk synth --output=~/templates```

# 참고자료
- [CDK guide](https://docs.aws.amazon.com/ko_kr/cdk/v2/guide/home.html)
- [about_Execution_Policies](https://docs.microsoft.com/ko-kr/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2)
- [CDK Python example](https://github.com/aws-samples/aws-cdk-examples)
- [AWS CLI](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-files.html)