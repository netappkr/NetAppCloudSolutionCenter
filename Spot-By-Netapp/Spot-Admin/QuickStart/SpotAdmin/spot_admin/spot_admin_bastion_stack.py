from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnTag
)
from constructs import Construct

class BastionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hands-on bastion 생성
        self.bastionrole = iam.Role(
            self, "SpotAdminbastionRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp SpotAdmin Hands on bastion Role"
        )
        self.bastionrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        ## AMI
        AMI = ec2.MachineImage.generic_linux(
            {
            "ap-northeast-2": "ami-039b82a0114f56141",
            "us-east-1" : "ami-03c2b54163839706d",
            "us-east-2" : "ami-077d8e2bb58ef66c5",
            "us-west-1" : "ami-04f35dd27b02595bf",
            "us-west-2" : "ami-09d4fc91a6e403e67",
            "ap-northeast-3" : "ami-0fbd03e6702d4e2ec",
            "ap-southeast-2" : "ami-0c4d10308b868a23a",
            "ap-northeast-1" : "ami-0199fd9c976b7312f",
            "eu-central-1" : "ami-0e3769d80ddceb352",
            "ap-southeast-1" : "ami-0aa4854fdaaee7289",
            "eu-west-1" : "ami-0bb4e6b6f2ec61013",
            "eu-west-2" : "ami-0078d7052fb56c251",
            "eu-west-3" : "ami-06f91bf996d50d2ca"
            }
        )


        ## 보안그룹
        SecurityGroup = ec2.SecurityGroup(self,"SpotAdminbastionSG",vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        
        ## Keypair
        self.keyPair=ec2.CfnKeyPair(self, "SpotAdminkey",
            key_name="SpotAdminkey",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvu2v6lkF59XSY3ch+Df2w/AN10EPXZ3JL2Xbqtsv13xVq9ZuzmUcdCpfa9NyjnyBoaXxymUvQSaeQCFxnjroAySOKVXaR6n6ahWFGQOYlfZHkKYg/N8pTpQht3QXNLoA8lUlrb3lyehQHxtCAhtgmx4BIaBpGM/FLaJqhu1OQ7gz0GBbG1qZOmEyrzcklkvriyPYzEESg3N9w+eM09rWvu3dK+EezAsgeFBlcsfHY5eNRmgp2iPfvz8tNZ3wgsrU/UiZHueqsMmGYS+Njjr461cx2q3EhjjPbYz8+tj3t/taZ/Jf419r9ZhT1JHm8/vUh22B5Xm31LdbMBPGvuUKPQ=="
        )
        user_data = ec2.UserData.for_linux()
        user_data.add_commands("aws s3 cp s3://netappkr-wyahn-s3/public/Spot_Admin/DeployTestapp/ /opt/DeployTestapp --recursive")
        # 서버생성
        ec2.Instance(self, "SpotAdminbastion",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            machine_image=AMI,
            role=self.bastionrole,
            security_group=SecurityGroup,
            key_name="SpotAdminkey",
            user_data=user_data
        )
