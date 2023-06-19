from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnTag,
    CfnParameter,
    Fn
)
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                           vpc_name=Fn.join(delimiter="_", list_of_values=[
                                            prefix.value_as_string, "vpc"]),
                           ip_addresses=ec2.IpAddresses.cidr("172.30.0.0/16"),
                           nat_gateways=1,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   cidr_mask=24, name="public-subnet", subnet_type=ec2.SubnetType.PUBLIC),
                               ec2.SubnetConfiguration(
                                   cidr_mask=24, name="private-subnet", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                           ])
        # CfnOutput(self,"private-subnet-id-0",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0])
        # CfnOutput(self,"private-subnet-id-1",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[1])
        # CfnOutput(self,"routetable-id",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets[0].route_table.route_table_id)
        # 보안 그룹
        self.SecurityGroup = ec2.SecurityGroup(self,"default_sg",vpc=self.vpc,security_group_name=Fn.join(delimiter="_", list_of_values=[prefix.value_as_string, "default_sg"]),)
        self.SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(self.vpc.vpc_cidr_block), ec2.Port.all_traffic(), "allow all access from the vpc")