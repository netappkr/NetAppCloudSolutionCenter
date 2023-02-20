from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    SecretValue,
    CfnParameter,
    Fn
)
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer
class EKSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, keypair, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        #EKS
        cluster = eks.Cluster(self, "eks",
            kubectl_layer=KubectlV24Layer(self, "kubectl"),
            version=eks.KubernetesVersion.V1_24,
            vpc = vpc,
            # cluster_name=Fn.join(delimiter="_", list_of_values=[prefix.value_as_string, "eks"]),
            cluster_name="eks",
            default_capacity=1,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            alb_controller = eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_4_1
            )
        )
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow http access from the world")
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow https access from the world")
        
        cluster.add_nodegroup_capacity("custom-node-group",
            instance_types=[
                ec2.InstanceType("m5.large")],
                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                nodegroup_name = "custom-ng",
                desired_size = 1,
                labels={
                    "purpose": "test"
                },
                remote_access=eks.NodegroupRemoteAccess(ssh_key_name=keypair.key_name),
                min_size = 0
        )
        #iam
        # BastionStack/SpotAdminbastionRole should be defined in the scope of the EKSStack stack to prevent circular dependencies
        # 순환참조 방지를 위해 EKS 스택에다가 롤을 직접정의가 필요합니다.
        # merge 할때는 bastion host role로 입력해야 합니다.
        role = iam.Role(
            self, "eksadmin_ec2_Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp SpotAdmin Hands on bastion Role"
        )
        # role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        # admin_user = iam.User(
        #    self, "NetappAdmin",
        #    user_name="NetappAdmin", 
        #    password=SecretValue.unsafe_plain_text("Netapp1!")
        # )
        # admin_user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        #admin_user.addToGroup(IGroup.fromGroupArn("arn:aws:iam::<your aws account id>:group/admin"))
        
        # EKS에 iam user등록
        # cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
        cluster.aws_auth.add_role_mapping(role, groups=["system:masters"])

        #core.CfnOutput(core,construct_id,value="출력")
