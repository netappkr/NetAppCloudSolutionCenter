from aws_cdk import aws_directoryservice as directoryservice
from aws_cdk import NestedStack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Fn
from aws_cdk import CfnParameter
from aws_cdk import CfnOutput
from constructs import Construct


class ADStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc, prefix, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        #prefix = CfnParameter(self, "prefix", type="String", default=prefix.value_as_string, description="this parm use prefix or id in cfn. please input only english and all in lower case")
        self.cfn_microsoft_AD  = directoryservice.CfnMicrosoftAD(self, "MSAD",
            name=Fn.join(delimiter=".", list_of_values=[prefix.value_as_string, "com"]),
            vpc_settings=directoryservice.CfnMicrosoftAD.VpcSettingsProperty(
                subnet_ids=[
                    vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0],
                    vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[1]
                ],
                vpc_id=vpc.vpc_id
            ),
            create_alias=False,
            edition ="Standard",
            enable_sso=False,
            password="Netapp1!",
            short_name=prefix.value_as_string
        )
        #cfnoutput
        CfnOutput(self, "cfn_microsoft_AD.AttrDnsIpAddresses", export_name="dnsipaddress", value=Fn.join(delimiter=",",list_of_values=self.cfn_microsoft_AD.attr_dns_ip_addresses))
        CfnOutput(self, "cfn_microsoft_AD.name", value=self.cfn_microsoft_AD.name)
        CfnOutput(self, "cfn_microsoft_AD.OrgINFO", value=Fn.join(delimiter="", list_of_values=["OU=Computers,OU=",prefix.value_as_string,",DC=",prefix.value_as_string,",DC=com"]))
        #CfnOutput(self, "ServiceAccountIamRole", value=self.cfn_microsoft_AD.role.role_arn)