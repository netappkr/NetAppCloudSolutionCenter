#from blue_xp_cdk.NW_stack import NetworkStack
#from blue_xp_cdk.AD_stack import AD_stack
#from blue_xp_cdk.ASG_stack import ASGStack
#from blue_xp_cdk.EKS_stack import EKSStack
#from blue_xp_cdk.fsxn_stack import FSxNStack
from blue_xp_cdk.BlueXP_req import BlueXPReqStack
from aws_cdk import (
    Stack,
    CfnParameter
)
from constructs import Construct

class BlueXpCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        BlueXP = BlueXPReqStack(self, "BlueXPReqStack",prefix=prefix)