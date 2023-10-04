#!/usr/bin/env python3
import os

import aws_cdk as cdk

from blue_xp_cdk.blue_xp_cdk_stack import BlueXpCdkStack

env_netapp_apac = cdk.Environment(account="169544784679", region="ap-northeast-2")
app = cdk.App()

BlueXpCdkStack = BlueXpCdkStack(app, "BlueXpCdkStack", env=env_netapp_apac)
app.synth()
