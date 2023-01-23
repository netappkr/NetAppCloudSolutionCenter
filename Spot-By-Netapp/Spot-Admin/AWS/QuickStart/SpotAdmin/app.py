#!/usr/bin/env python3
import os

import aws_cdk as cdk

from spot_admin.spot_admin_NW_stack import NetworkStack
from spot_admin.spot_admin_bastion_stack import BastionStack
from spot_admin.spot_admin_ASG_stack import ASGStack
from spot_admin.spot_admin_EKS_stack import EKSStack
from spot_admin.spot_admin_merge_stack import MergeStack
# 리전 선택 최종빌드땐 주석처리
# env_netappkr = cdk.Environment(account="037660834288", region="ap-northeast-2")
env_netappkr = cdk.Environment(account="037660834288", region="ap-northeast-1")
app = cdk.App()

# test 를 위한 분할 스택
NWStack = NetworkStack(app, "NetworkStack", env=env_netappkr)

Bastion = BastionStack(app, "BastionStack", vpc=NWStack.vpc, env=env_netappkr)
Bastion.add_dependency(NWStack)

# AutoScalingGroup = ASGStack(app, "ASGStack", vpc=NWStack.vpc, keypair=Bastion.keyPair, env=env_netappkr)
# AutoScalingGroup.add_dependency(Bastion)

ElasticKubernetesService = EKSStack(app, "EKSStack", vpc=NWStack.vpc, keypair=Bastion.keyPair, env=env_netappkr)
ElasticKubernetesService.add_dependency(Bastion)

# 최종
# SpotAdmin = MergeStack(app, "MergeStack", env=env_netappkr)
# SpotAdmin = MergeStack(app, "MergeStack")
app.synth()
