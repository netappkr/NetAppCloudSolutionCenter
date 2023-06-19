from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnParameter,
    Fn
)
from constructs import Construct


class ADStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, keypair, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")

        # 보안그룹
        SecurityGroup = ec2.SecurityGroup(self, "ADDCSG", security_group_name=Fn.join(delimiter="_", list_of_values=[
            prefix.value_as_string, "ADDC_sg"]), vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            3389), "allow RDP access from the world")

        # init sh
        # userdata_file = open("./bastion.sh", "rb").read()
        # Creates a userdata object for Linux hosts
        # userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        # userdata.add_commands(str(userdata_file, 'utf-8'))

        # AMI
        AMI = ec2.MachineImage.generic_linux(
            {
                "ap-northeast-2": "ami-02b5c49b2e10dc79e"
            }
        )
        # 서버생성
        ec2.Instance(self, "ADDC",
                     vpc=vpc,
                     instance_type=ec2.InstanceType.of(
                         ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
                     vpc_subnets=ec2.SubnetSelection(
                         subnet_type=ec2.SubnetType.PUBLIC),
                     machine_image=AMI,
                     security_group=SecurityGroup,
                     key_name=keypair.key_name
                     # ,user_data=userdata
                     )
