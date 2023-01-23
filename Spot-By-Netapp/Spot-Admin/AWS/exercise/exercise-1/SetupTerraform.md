# 실습환경 구성
테라폼을 이용해 Lab 환경을 구성합니다.

## Terraform 설치
각 OS환경에 맞게 테라폼을 설치합니다.
[Terraform install Guide](https://developer.hashicorp.com/terraform/downloads)
![install_terraform](./Images/install_terraform.png)


## Terraform 구성
1. Github에서 다운로드 받은 테라폼 파일의 디렉토리까지 이동합니다.
```
cd C:\Users\wooyeoun\OneDrive\Terraform
```
2. aws-provider.tf 파일을 생성 또는 편집합니다.
> ### Tips
> 아직 엑세스 키를 생성하지 않았다면 하기 문서를 참고하여 엑세스키를 발급합니다.
> [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
```t
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.40.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "ap-northeast-2"
  access_key = "AKIASO6NIDMTQCFMOIPU"
  secret_key = "ㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁㅁ"
}
```
3. 테라폼 환경을 구성합니다.
```t
terraform init
```
4. 적용 전 구성 될 항목을 확인합니다.
```t
terraform plan -var-file="auth.tfvars"
```
5. 구성 명령을 수행됩니다.
```t
terraform apply -var-file="auth.tfvars"
```
# 클라우드에 배포한 환경 삭제
클라우드에 배포한 환경 삭제가 필요한 경우 하기 명령을 사용합니다.
```t
terraform destory -var-file="auth.tfvars"
```

```
Usage: terraform [global options] <subcommand> [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands.

Main commands:
  init          Prepare your working directory for other commands
  validate      Check whether the configuration is valid
  plan          Show changes required by the current configuration
  apply         Create or update infrastructure
  destroy       Destroy previously-created infrastructure

All other commands:
  console       Try Terraform expressions at an interactive command prompt
  fmt           Reformat your configuration in the standard style
  force-unlock  Release a stuck lock on the current workspace
  get           Install or upgrade remote Terraform modules
  graph         Generate a Graphviz graph of the steps in an operation
  import        Associate existing infrastructure with a Terraform resource
  login         Obtain and save credentials for a remote host
  logout        Remove locally-stored credentials for a remote host
  output        Show output values from your root module
  providers     Show the providers required for this configuration
  refresh       Update the state to match remote systems
  show          Show the current state or a saved plan
  state         Advanced state management
  taint         Mark a resource instance as not fully functional
  untaint       Remove the 'tainted' state from a resource instance
  version       Show the current Terraform version
  workspace     Workspace management

Global options (use these before the subcommand, if any):
  -chdir=DIR    Switch to a different working directory before executing the
                given subcommand.
  -help         Show this help output, or the help for a specified subcommand.
  -version      An alias for the "version" subcommand.
```


> ### 번외
> ### AWS CLI 설치
> AWS CLI을 설치하여 credential 구성을 쉽게 할 수 있습니다.</br>
> [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/>latest/userguide/getting-started-install.html)

> ### AWS CLI 구성 and credential file 설정
> aws configure 명령으로 설정파일을 구성합니다.
>> ### Tips
>> 아직 엑세스 키를 생성하지 않았다면 하기 문서를 참고하여 엑세스키를 발급합니다.</br>
>> [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

> ```
> $ aws configure
> AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
> AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
> Default region name [None]: ap-norteast-2
> Default output format [None]: json
> ```
> ~/.aws/credentials
> ```
> [default]
> aws_access_key_id=AKIAIOSFODNN7EXAMPLE
> aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
> ```
> ~/.aws/config
> ```
> [default]
> region=us-west-2
> output=json
> ```


# 참조
- [Terraform install Guide](https://developer.hashicorp.com/terraform/downloads)
- [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Managing access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
- [Terraform Basic CLI Features](https://developer.hashicorp.com/terraform/cli/commands)