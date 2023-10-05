from blue_xp_cdk.NW_stack import NetworkStack
from blue_xp_cdk.simple_ad_stack import ADStack
from blue_xp_cdk.bastion_stack import BastionStack
#from blue_xp_cdk.EKS_stack import EKSStack
from blue_xp_cdk.fsxn_stack import FSxNStack
from blue_xp_cdk.BlueXP_req import BlueXPReqStack
from aws_cdk import (
    Stack,
    CfnParameter,
    Tags,
    Fn
)
from constructs import Construct

class BlueXpCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        creator = CfnParameter(self, "creator", type="String", default="SeanP",
                              description="please insert you are name initial")
        
        # stack
        NW = NetworkStack(self, "NetworkStack", prefix=prefix)
        Tags.of(NW).add("creator", creator.value_as_string)

        BlueXP = BlueXPReqStack(self, "BlueXPReqStack", prefix=prefix)
        Tags.of(BlueXP).add("creator", creator.value_as_string)

        AD = ADStack(self, "ADStack", vpc=NW.vpc, prefix=prefix)
        Tags.of(AD).add("creator", creator.value_as_string)
        AD.add_dependency(NW)

        bastionhost = BastionStack(self, "BastionStack", vpc=NW.vpc, prefix=prefix)
        Tags.of(bastionhost).add("creator", creator.value_as_string)
        bastionhost.add_dependency(NW)

        FSxN = FSxNStack(self, "FSxNStack", vpc=NW.vpc, AD=AD.cfn_simple_AD , prefix=prefix)
        Tags.of(FSxN).add("creator", creator.value_as_string)
        FSxN.add_dependency(AD)
        





        