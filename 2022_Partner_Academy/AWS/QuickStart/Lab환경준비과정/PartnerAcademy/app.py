#!/usr/bin/env python3
import os
#import aws_cdk as cdk
from aws_cdk import (
    App,
    Tags,
    CfnOutput,
    Fn
)
from partner_academy.partner_academy_stack import PartnerAcademyStack
# from partner_academy.fsxontap_stack import fsxontapStack
app = App()
PartnerAcademyStack(app, "PartnerAcademyStack")
# fsxontapStack(app,"FsxOntapStack")
# Tags.of(PartnerAcademyStack).add("Name", "PartnerAcademy",
#    include_resource_types=["AWS::EC2::Subnet"]
# )
# PrivateSubnetId0=Fn.import_value("private-subnet-id-0")
# PrivateSubnetId1=Fn.import_value("private-subnet-id-1")
app.synth()
