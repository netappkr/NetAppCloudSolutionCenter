import os

import aws_cdk as cdk
from cshandson.NW_stack import NetworkStack
from cshandson.AU_stack import AUStack
from cshandson.AD_stack import ADStack
from cshandson.fsxn_stack import FSxNStack
from cshandson.BlueXP_req import BlueXPReqStack
# from cshandson.merge_stack import MergeStack
# 리전 선택 최종 빌드 땐 주석처리
# env_netappkr = cdk.Environment(account="037660834288", region="ap-northeast-2")
env_netapp_apac = cdk.Environment(account="169544784679", region="ap-northeast-2")
# env_netapp_bespin = cdk.Environment(account="716551662146", region="ap-northeast-2")
app = cdk.App()
# # test 를 위한 분할 스택
NWStack = NetworkStack(app, "NetworkStack", env=env_netapp_apac)
BlueXP = BlueXPReqStack(app, "BlueXPReqStack", env=env_netapp_apac)
AU = AUStack(app, "AUStack", vpc=NWStack.vpc, env=env_netapp_apac)
AU.add_dependency(NWStack)
AD = ADStack(app, "ADStack", vpc=NWStack.vpc, keypair=AU.keyPair, env=env_netapp_apac)
AD.add_dependency(AU)

fsxN = FSxNStack(app,"FSxNStack",vpc=NWStack.vpc, sg=NWStack.SecurityGroup, env=env_netapp_apac)
# ElasticKubernetesService.add_dependency(Bastion)
# 최종
# CSHandson = MergeStack(app, "MergeStack", env=env_netapp_bespin)
# CSHandson = MergeStack(app, "MergeStack")
app.synth()
