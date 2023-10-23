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
        #prefix = CfnParameter(self, "prefix", type="String", default=prefix.value_as_string, description="this parm use prefix or id in cfn. please input only english and all in lower case")
        template = cfn_inc.CfnInclude(self, "cvo-single", template_file="aws-cvo-single.json",
                                      parameters={
                                          "AMI": "",
                                          "AllocatePublicIP": True,
                                          "BootMediaType": "io1",
                                          "CoreMediaType": defaultsg,
                                          "DeploymentType" : "singlenode",
                                          "InstanceType" : "m5.xlarge",
                                          "KeyPair" : "",
                                          "PlatformSerialNumber" : "",
                                          "RootMediaType" : "",
                                          "SubnetId" : vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0],
                                          "Tenancy": "default",
                                          "VpcId" : vpc.id
                                      }
                                      )
        #cfnoutput
        #CfnOutput(self, "cfn_microsoft_AD.attr_dns_ip_addresses", value=Fn.join(delimiter=",",list_of_values=self.cfn_microsoft_AD.attr_dns_ip_addresses))
        #CfnOutput(self, "cfn_microsoft_AD.name", value=self.cfn_microsoft_AD.name)
        #CfnOutput(self, "ServiceAccountIamRole", value=self.cfn_microsoft_AD.role.role_arn)