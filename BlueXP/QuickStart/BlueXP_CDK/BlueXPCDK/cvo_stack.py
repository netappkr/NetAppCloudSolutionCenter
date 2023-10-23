from aws_cdk import aws_directoryservice as directoryservice
from aws_cdk import NestedStack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Fn
from aws_cdk import CfnParameter
from aws_cdk import CfnOutput
from aws_cdk import cloudformation_include as cfn_inc
from constructs import Construct


class CVOStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc, defaultsg, prefix, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # 보안그룹
        SecurityGroup = ec2.SecurityGroup(self, "cvosg", security_group_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "cvo_sg"]),vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.AclIcmp, "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(22), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(80), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(749), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(635), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.udp(635), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(445), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(443), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp_range(start_port=4045,end_port=4046), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.udp_range(start_port=4045,end_port=4046), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(3260), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(2049), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.udp(2049), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp_range(start_port=161,end_port=162), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.udp_range(start_port=161,end_port=162), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(139), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp_range(start_port=11104,end_port=11105), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(111), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.udp(111), "")
        SecurityGroup.add_ingress_rule(ec2.Peer.ipv4(vpc.ip_addresses), ec2.Port.tcp(10000), "")
        
        #prefix = CfnParameter(self, "prefix", type="String", default=prefix.value_as_string, description="this parm use prefix or id in cfn. please input only english and all in lower case")
        template = cfn_inc.CfnInclude(self, "cvo-single", template_file="./cvo/aws-cvo-single.json",
                                      parameters={
                                          "AMI": "ami-0f45974498ee16ac4",
                                          "AllocatePublicIP": "false",
                                          "BootMediaType": "io1",
                                          "CoreMediaType": "st1",
                                          "CustomSecurityGroup": SecurityGroup.security_group_id,
                                          "DeploymentType" : "singlenode",
                                          "InstanceName": Fn.join(delimiter="", list_of_values=[prefix.value_as_string, "cvo"]),
                                          "InstanceType" : "m5.xlarge",
                                          "KeyPair" : "wyahn_key",
                                          "NVLogMediaType" : "persistent-disk",
                                          "PlatformSerialNumber" : "90920130000001073489",
                                          "RootMediaType" : "gp3",
                                          "SubnetId" : vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0],
                                          "Tenancy": "default",
                                          "VpcId" : vpc.id
                                      }
                                      )
        #cfnoutput
        #CfnOutput(self, "cfn_microsoft_AD.attr_dns_ip_addresses", value=Fn.join(delimiter=",",list_of_values=self.cfn_microsoft_AD.attr_dns_ip_addresses))
        #CfnOutput(self, "cfn_microsoft_AD.name", value=self.cfn_microsoft_AD.name)
        #CfnOutput(self, "ServiceAccountIamRole", value=self.cfn_microsoft_AD.role.role_arn)