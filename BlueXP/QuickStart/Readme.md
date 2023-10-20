# BlueXP Handson 환경 배포

## Pre requirement
- [Lab prerequirement](./LabPreRequirement.md)

### 지원되는 리전

- "ap-northeast-2"
- "us-east-1"
- "us-east-2"
- "us-west-1"
- "us-west-2"
- "ap-northeast-3"
- "ap-southeast-2"
- "ap-northeast-1"
- "eu-central-1"
- "ap-southeast-1"
- "eu-west-1"
- "eu-west-2"
- "eu-west-3"

## CDK Asset 배포

1. AWS console > Cloudformation 콘솔을 엽니다.
2. stack 생성 버튼을 선택합니다.

- StackName: CDKToolkit
- Template URL: <https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/CDKToolkit.yml>

### CDKToolkit Stack Parameters

- Name : CDKToolkit
- FileAssetsBucketKmsKeyId : AWS_MANAGED_KEY
- PublicAccessBlockConfiguration : true
- Qualifier : hnb659fds </br>
<img width="80%" height="80%" src="./Images/DeployStackImage/cdktoolkit.png">

3. 전부 기본값으로 진행 후 다음을 눌러 스택생성 페이지까지 이동합니다.
4. 체크박스를 모두 활성화 후 스택을 생성합니다.

- [X] AWS CloudFormation이 사용자 지정 이름으로 IAM 리소스를 생성할 수 있음을 인정합니다.

5. 스택이 완전히 배포되기까지 기다립니다.

6. Stack 세부정보 화면에서 리소스 탭을 클릭하고 s3를 검색하여 버킷을 확인하고 링크를 클릭하여 s3버킷으로 이동합니다. </br>
![find-s3](./Images/DeployStackImage/find-s3.png)

7. CDKToolkit 스택에서 생성된 s3에 파일을 업로드합니다.

- 그림과 같이 cdkasset.zip 파일의 압축을 풀고 하위 파일들을 모두 업로드합니다.</br>
  압축파일 : [cdkasset](./cdk_asset.zip)

- 압축파일 해제 후 s3에 파일을 업로드합니다. </br>
  s3 burketname : cdk-hnb659fds-assets-<"your aws account id">-ap-northeast-2 </br>
  <img width="80%" height="80%" src="./Images/DeployStackImage/s3view.png">

## Main Stack 배포

> ### 경고!
> 반드시 CDKToolkit Stack에서 생성된 S3 버킷에 첨부된 파일이 모두 업로드된 상태에서 진행되어야 합니다.

1. Main Stack을 생성합니다.

- StackName: MainStack </br>
- Template URL: <https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/Spot_Admin/cdk/MergeStack.template.json>

2. Main Stack Parameters
모든 항목을 이미 입력된 기본값으로 설정합니다.

3. 모든 체크박스를 체크 후 스택을 생성합니다.

- [X] AWS CloudFormation이 사용자 지정 이름으로 IAM 리소스를 생성할 수 있음을 인정합니다.
- [X] AWS CloudFormation에 다음 기능이 필요할 수 있음을 인정합니다. CAPABILITY_AUTO_EXPAND

> 생성완료까지 걸리는 예상 시간 </br>
> ✨  Total time: 2492.66s

# 결과

그림과 같이 2개의 메인스택과 2개의 서브스택이 배포되고 Hands-on 환경이 생성됩니다.</br>
![image](./Images/DeployStackImage/stackview.png)

# 다음과정

- 다음과정: [exe-1_Spot by netapp 과 AWS Account를 연결합니다.](../exercise/exercise-1/1-1_ConnectAccount.md)

# 참고문서

- [CDKv2 doc](https://docs.aws.amazon.com/cdk/v2/guide/parameters.html)
- [CDkv2 python](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_eks/CfnAddon.html)