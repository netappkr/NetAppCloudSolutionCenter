#!/usr/bin/env python3
import os
import aws_cdk as cdk
from BlueXPCDK.main_stack import mainStack

env_netapp_apac = cdk.Environment(account="169544784679", region="ap-northeast-2")
app = cdk.App()

BlueXpCdkStack = mainStack(app, "mainstack", env=env_netapp_apac)
app.synth()
