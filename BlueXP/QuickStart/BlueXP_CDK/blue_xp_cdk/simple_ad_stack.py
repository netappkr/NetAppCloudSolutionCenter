from aws_cdk import aws_directoryservice as directoryservice
from aws_cdk import NestedStack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Fn
from aws_cdk import CfnParameter
from constructs import Construct


class ADStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc, prefix, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        #prefix = CfnParameter(self, "prefix", type="String", default=prefix.value_as_string, description="this parm use prefix or id in cfn. please input only english and all in lower case")
        self.cfn_simple_AD = directoryservice.CfnSimpleAD(self, "simpleAD",
            name=Fn.join(delimiter=".", list_of_values=[prefix.value_as_string, "com"]),
            size="Small",
            vpc_settings=directoryservice.CfnSimpleAD.VpcSettingsProperty(
                subnet_ids=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids,
                vpc_id=vpc.vpc_id
            ),
            create_alias=False,
            description="description",
            enable_sso=False,
            password="Netapp1!",
            short_name=prefix.value_as_string
            
        )