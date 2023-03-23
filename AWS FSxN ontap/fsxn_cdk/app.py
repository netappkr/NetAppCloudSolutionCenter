import os

import aws_cdk as cdk
# from fsxn_cdk.NW_stack import NetworkStack
# from fsxn_cdk.bastion_stack import BastionStack
# from fsxn_cdk.ASG_stack import ASGStack
# from fsxn_cdk.EKS_stack import EKSStack
# from fsxn_cdk.fsxn_stack import FSxNStack
# from fsxn_cdk.BlueXP_req import BlueXPReqStack
from fsxn_cdk.merge_stack import MergeStack
# 리전 선택 최종 빌드 땐 주석처리
env_netappkr = cdk.Environment(account="037660834288", region="ap-northeast-2")
# env_netapp_apac = cdk.Environment(account="169544784679", region="ap-northeast-2")
# env_netapp_bespin = cdk.Environment(account="716551662146", region="ap-northeast-2")
app = cdk.App()
# # test 를 위한 분할 스택
# NWStack = NetworkStack(app, "NetworkStack", env=env_netapp_bespin)
# BlueXP = BlueXPReqStack(app, "BlueXPReqStack", env=env_netapp_bespin)
# Bastion = BastionStack(app, "BastionStack", vpc=NWStack.vpc, env=env_netapp_bespin)
# Bastion.add_dependency(NWStack)

# # AutoScalingGroup = ASGStack(app, "ASGStack", vpc=NWStack.vpc, keypair=Bastion.keyPair, env=env_netappkr)
# # AutoScalingGroup.add_dependency(Bastion)

# ElasticKubernetesService = EKSStack(app, "EKSStack", vpc=NWStack.vpc, keypair=Bastion.keyPair, env=env_netapp_bespin)
# ElasticKubernetesService.add_dependency(Bastion)

# fsxN = FSxNStack(app,"FSxNStack",vpc=NWStack.vpc, env=env_netapp_bespin)
# ElasticKubernetesService.add_dependency(Bastion)
# 최종
# FSxNAdmin = MergeStack(app, "MergeStack", env=env_netapp_bespin)
FSxNAdmin = MergeStack(app, "MergeStack")
app.synth()