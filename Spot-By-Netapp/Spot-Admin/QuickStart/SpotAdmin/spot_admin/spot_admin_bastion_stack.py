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
            "ap-northeast-2": "ami-0632d76430fad92e4"
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
        user_data.add_commands("aws s3 cp s3://netappkr-wyahn-s3/public/DeployTestapp/ /opt/DeployTestapp --recursive")
        # 서버생성
        ec2.Instance(self, "SpotAdminbastion",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            machine_image=AMI,
            role=self.bastionrole,
            security_group=SecurityGroup,
            key_name="SpotAdminkey",
            user_data=user_data
        )
