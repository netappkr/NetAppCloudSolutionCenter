from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnParameter,
    Fn
)
from constructs import Construct


class AUStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")

        # Hands-on AU 생성
        self.bastionrole = iam.Role(
            self, "bastionRole",
            role_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "bastionRole"]),
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp SpotAdmin Hands on bastion Role"
        )
        self.bastionrole.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        # 보안그룹
        SecurityGroup = ec2.SecurityGroup(self, "bastionSG", security_group_name=Fn.join(delimiter="_", list_of_values=[
            prefix.value_as_string, "bastion_sg"]), vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            22), "allow ssh access from the world")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.all_traffic(),"allow ssh access from the world")

        # Keypair
        self.keyPair = ec2.CfnKeyPair(self, "Adminkey",
                                      key_name=Fn.join(delimiter="_", list_of_values=[
                                          prefix.value_as_string, "key"]),
                                      public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvu2v6lkF59XSY3ch+Df2w/AN10EPXZ3JL2Xbqtsv13xVq9ZuzmUcdCpfa9NyjnyBoaXxymUvQSaeQCFxnjroAySOKVXaR6n6ahWFGQOYlfZHkKYg/N8pTpQht3QXNLoA8lUlrb3lyehQHxtCAhtgmx4BIaBpGM/FLaJqhu1OQ7gz0GBbG1qZOmEyrzcklkvriyPYzEESg3N9w+eM09rWvu3dK+EezAsgeFBlcsfHY5eNRmgp2iPfvz8tNZ3wgsrU/UiZHueqsMmGYS+Njjr461cx2q3EhjjPbYz8+tj3t/taZ/Jf419r9ZhT1JHm8/vUh22B5Xm31LdbMBPGvuUKPQ=="

                                      )
        # init sh
        userdata_file = open("./bastion.sh", "rb").read()
        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))

        # 서버생성
        ec2.Instance(self, "AU",
                     vpc=vpc,
                     instance_type=ec2.InstanceType.of(
                         ec2.InstanceClass.T3, ec2.InstanceSize.XLARGE),
                     vpc_subnets=ec2.SubnetSelection(
                         subnet_type=ec2.SubnetType.PUBLIC),
                     # machine_image=AMI,
                     machine_image=ec2.MachineImage.latest_amazon_linux(
                         generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                         edition=ec2.AmazonLinuxEdition.STANDARD,
                         virtualization=ec2.AmazonLinuxVirt.HVM,
                         storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                     ),
                     block_devices=[ec2.BlockDevice(
                         device_name="/dev/sda1",
                         volume=ec2.BlockDeviceVolume.ebs(50)
                     )],
                     role=self.bastionrole,
                     security_group=SecurityGroup,
                     key_name=Fn.join(delimiter="_", list_of_values=[
                         prefix.value_as_string, "key"]),
                     user_data=userdata
                     )
