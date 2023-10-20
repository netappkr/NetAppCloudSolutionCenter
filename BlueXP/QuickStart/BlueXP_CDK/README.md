# my Cheat Sheet

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

## aws profile 구성 확인
```powershell 
aws configure list-profiles
```
```powershell
PS BlueXP_CDK> aws configure list-profiles
default
user1
cds-user-01
```

#### CDK Deploy command
```
cdk deploy --require-approval never --profile cds-user-01
```
```
cdk deploy {스택이름} --require-approval never --profile cds-user-01
```
```
cdk deploy --all --profile cds-user-01 --parameters prefix=wyahn
```
```
cdk synth --profile cds-user-01 --parameters prefix=wyahn --parameters creator=wooyoung
```

#### CDK destory
- ```cdk destroy --all --force --profile cds-user-01```

#### CDK stack list
- ```cdk list```
#### CDK config review
- ```cdk diff```

### CDK 출력 디렉터리 지정
- output( ) 옵션을 추가하면 -o합성된 템플릿을 가 아닌 다른 디렉토리에 쓸 수 있습니다 cdk.out.
```
cdk synth --output=~/templates
```
### CDK version update
```
npm install -g aws-cdk@latest
```
### no synth test
```cdk --app cdk.out deploy --profile cds-user-01 --parameters prefix=wyahn --parameters creator=wooyoung``` 

### CDK issue
원인은 모르나 CDK를 통해서 deploy하면 ```validation errors detected: Value '' at 'stackName'``` 에러가 발생함
스택 이름이 비어있으면 빌드단계에서 실패해야될텐데 이상하네요...

```
Error occurred while monitoring stack: Error [ValidationError]: 2 validation errors detected: Value '' at 'stackName' failed to satisfy constraint: Member must satisfy regular expression pattern: [a-zA-Z][-a-zA-Z0-9]*|arn:[-a-zA-Z0-9:/._+]*; Value '' at 'stackName' failed to satisfy constraint: Member must have length greater than or equal to 1
    at Request.extractError (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:46430)
    at Request.callListeners (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:90083)
    at Request.emit (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:89531)
    at Request.emit (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:196289)
    at Request.transition (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:189841)
    at AcceptorStateMachine.runTo (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:154713)
    at C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:155043
    at Request.<anonymous> (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:190133)
    at Request.<anonymous> (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:196364)
    at Request.callListeners (C:\Users\wyahn\AppData\Roaming\npm\node_modules\aws-cdk\lib\index.js:362:90251) {
  code: 'ValidationError',
  time: 2023-10-19T04:25:07.138Z,
  requestId: '7733ec5d-495a-46a0-bbbe-2cc8181d1ccc',
  statusCode: 400,
  retryable: false,
  retryDelay: 566.9198441623209
}
```
## 주의
사내PC는 s3에서 Download는 되지만 Upload가 정책으로 막혀있어 CDK를 사용한 Deploy가 불가능합니다.


# 참고자료
- [CDK guide](https://docs.aws.amazon.com/ko_kr/cdk/v2/guide/home.html)
- [about_Execution_Policies](https://docs.microsoft.com/ko-kr/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2)
- [CDK Python example](https://github.com/aws-samples/aws-cdk-examples)
- [AWS CLI](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-files.html)