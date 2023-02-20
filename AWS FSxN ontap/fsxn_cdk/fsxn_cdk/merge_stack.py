from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    # aws_autoscaling as autoscaling,
    # aws_elasticloadbalancingv2 as elbv2,
    # Duration,
    CfnParameter,
    Fn,
    aws_fsx as fsx,
    CfnTag
)
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer

class MergeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        
#################################################
        # VPC
        vpc = ec2.Vpc(self, "VPC",
                           vpc_name=Fn.join(delimiter="_", list_of_values=[
                                            prefix.value_as_string, "vpc"]),
                           cidr="172.30.0.0/16",
                           nat_gateways=1,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   cidr_mask=24, name="public-subnet", subnet_type=ec2.SubnetType.PUBLIC),
                               ec2.SubnetConfiguration(
                                   cidr_mask=24, name="private-subnet", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
                           ]
                           )
        # CfnOutput(self,"private-subnet-id-0",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0])
        # CfnOutput(self,"private-subnet-id-1",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[1])
        # CfnOutput(self,"routetable-id",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets[0].route_table.route_table_id)

#################################################################
        # Hands-on bastion 생성
        bastionrole = iam.Role(
            self, "bastionRole",
            role_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "bastionRole"]),
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp SpotAdmin Hands on bastion Role"
        )
        bastionrole.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        # AMI
        AMI = ec2.MachineImage.generic_linux(
            {
                "ap-northeast-2": "ami-039b82a0114f56141",
                "us-east-1": "ami-03c2b54163839706d",
                "us-east-2": "ami-077d8e2bb58ef66c5",
                "us-west-1": "ami-04f35dd27b02595bf",
                "us-west-2": "ami-09d4fc91a6e403e67",
                "ap-northeast-3": "ami-0fbd03e6702d4e2ec",
                "ap-southeast-2": "ami-0c4d10308b868a23a",
                "ap-northeast-1": "ami-0199fd9c976b7312f",
                "eu-central-1": "ami-0e3769d80ddceb352",
                "ap-southeast-1": "ami-0aa4854fdaaee7289",
                "eu-west-1": "ami-0bb4e6b6f2ec61013",
                "eu-west-2": "ami-0078d7052fb56c251",
                "eu-west-3": "ami-06f91bf996d50d2ca"
            }
        )

        # 보안그룹
        SecurityGroup = ec2.SecurityGroup(self, "bastionSG", security_group_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "bastion_sg"]),vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            22), "allow ssh access from the world")

        # Keypair
        keyPair = ec2.CfnKeyPair(self, "Adminkey",
                                      key_name=Fn.join(delimiter="_", list_of_values=[
                                          prefix.value_as_string, "key"]),
                                      public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvu2v6lkF59XSY3ch+Df2w/AN10EPXZ3JL2Xbqtsv13xVq9ZuzmUcdCpfa9NyjnyBoaXxymUvQSaeQCFxnjroAySOKVXaR6n6ahWFGQOYlfZHkKYg/N8pTpQht3QXNLoA8lUlrb3lyehQHxtCAhtgmx4BIaBpGM/FLaJqhu1OQ7gz0GBbG1qZOmEyrzcklkvriyPYzEESg3N9w+eM09rWvu3dK+EezAsgeFBlcsfHY5eNRmgp2iPfvz8tNZ3wgsrU/UiZHueqsMmGYS+Njjr461cx2q3EhjjPbYz8+tj3t/taZ/Jf419r9ZhT1JHm8/vUh22B5Xm31LdbMBPGvuUKPQ=="
        
                                     )
        # init sh 
        userdata_file = open("./bastion.sh", "rb").read()
        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))

        # 서버생성
        ec2.Instance(self, "bastion",
                     vpc=vpc,
                     instance_type=ec2.InstanceType.of(
                         ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
                     vpc_subnets=ec2.SubnetSelection(
                         subnet_type=ec2.SubnetType.PUBLIC),
                     # machine_image=AMI,
                     machine_image=ec2.MachineImage.latest_amazon_linux(
                         generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                         edition=ec2.AmazonLinuxEdition.STANDARD,
                         virtualization=ec2.AmazonLinuxVirt.HVM,
                         storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                     ),
                     role=bastionrole,
                     security_group=SecurityGroup,
                     key_name=Fn.join(delimiter="_", list_of_values=[
                         prefix.value_as_string, "key"]),
                     user_data=userdata
                     )
        

##########################################################################
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
                remote_access=eks.NodegroupRemoteAccess(ssh_key_name=keyPair.key_name),
                min_size = 0
        )
        #iam
        # BastionStack/SpotAdminbastionRole should be defined in the scope of the EKSStack stack to prevent circular dependencies
        # 순환참조 방지를 위해 EKS 스택에다가 롤을 직접정의가 필요합니다.
        # merge 할때는 bastion host role로 입력해야 합니다.
        # role = iam.Role(
        #     self, "eksadmin_ec2_Role",
        #     assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        #     # custom description if desired
        #     description="Netapp SpotAdmin Hands on bastion Role"
        # )
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
        cluster.aws_auth.add_role_mapping(bastionrole, groups=["system:masters"])

        #core.CfnOutput(core,construct_id,value="출력")
##############################
        # FSxN

        # ad_dns_ips =CfnParameter(self, "dns_ips", type="String", default=None,description="it is required for AD join.")
        # ad_domain_name = CfnParameter(self, "domain_name", type="String", default=None,description="it is required for AD join.")
        # ad_file_system_administrators_group = CfnParameter(self, "ad_file_system_administrators_group", type="String", default=None, description="option")
        # ad_organizational_unit_distinguished_name = CfnParameter(self, "ad_organizational_unit_distinguished_name", type="String", default=None, description="option")
        # ad_user_name = CfnParameter(self, "ad_user_name", type="String", default=None,description="it is required for AD join.")
        # ad_password = CfnParameter(self, "ad_password", type="String", default=None,description="it is required for AD join.")
        # FSXontap
        cfn_file_system = fsx.CfnFileSystem(self, "fsx",
                                            file_system_type="ONTAP",
                                            subnet_ids=[vpc.select_subnets(
                                                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0]],
                                            storage_capacity=1024,
                                            tags=[CfnTag(
                                                key="Name",
                                                value=Fn.join(delimiter="_", list_of_values=[
                                                    prefix.value_as_string, "FSx_N"])
                                            )],
                                            ontap_configuration=fsx.CfnFileSystem.OntapConfigurationProperty(
                                                deployment_type="SINGLE_AZ_1",

                                                # the properties below are optional
                                                automatic_backup_retention_days=0,
                                                # daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                                                disk_iops_configuration=fsx.CfnFileSystem.DiskIopsConfigurationProperty(
                                                    mode="AUTOMATIC"
                                                ),
                                                # endpoint_ip_address_range="endpointIpAddressRange",
                                                fsx_admin_password="Netapp1!",
                                                # preferred_subnet_id="preferredSubnetId",
                                                # route_table_ids=[[]],
                                                throughput_capacity=128,
                                            ),
                                            # self_managed_active_directory_configuration_property=fsx.CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty(
                                            #     dns_ips=[ad_dns_ips],
                                            #     domain_name=ad_domain_name,
                                            #     file_system_administrators_group=ad_file_system_administrators_group,
                                            #     organizational_unit_distinguished_name=ad_organizational_unit_distinguished_name,
                                            #     password=ad_password,
                                            #     user_name=ad_user_name
                                            # )
                                            )
############################################################
        #CloudmanagerRole 생성
        role = iam.Role(self, "BlueXP_Role",
                        role_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "BlueXP_Role"]),
            assumed_by=iam.AccountPrincipal("952013314444"),
            # custom description if desired
            description="Netapp Pertner Summit Hands on Cloudmanager Role"
        )
        # Pollicy 문서
        policy_document = iam.PolicyDocument.from_json(
        {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "cvoServicePolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:RunInstances",
                "ec2:ModifyInstanceAttribute",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeRouteTables",
                "ec2:DescribeImages",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:DescribeVolumes",
                "ec2:ModifyVolumeAttribute",
                "ec2:CreateSecurityGroup",
                "ec2:DescribeSecurityGroups",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:CreateSnapshot",
                "ec2:DescribeSnapshots",
                "ec2:GetConsoleOutput",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeRegions",
                "ec2:DescribeTags",
                "cloudformation:CreateStack",
                "cloudformation:DescribeStacks",
                "cloudformation:DescribeStackEvents",
                "cloudformation:ValidateTemplate",
                "iam:PassRole",
                "iam:CreateRole",
                "iam:PutRolePolicy",
                "iam:CreateInstanceProfile",
                "iam:AddRoleToInstanceProfile",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:ListInstanceProfiles",
                "sts:DecodeAuthorizationMessage",
                "ec2:AssociateIamInstanceProfile",
                "ec2:DescribeIamInstanceProfileAssociations",
                "ec2:DisassociateIamInstanceProfile",
                "s3:GetBucketTagging",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:CreateBucket",
                "s3:GetLifecycleConfiguration",
                "s3:ListBucketVersions",
                "s3:GetBucketPolicyStatus",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicy",
                "s3:GetBucketAcl",
                "kms:List*",
                "kms:ReEncrypt*",
                "kms:Describe*",
                "kms:CreateGrant",
                "ce:GetReservationUtilization",
                "ce:GetDimensionValues",
                "ce:GetCostAndUsage",
                "ce:GetTags",
                "ec2:CreatePlacementGroup",
                "ec2:DescribeReservedInstancesOfferings",
                "sts:AssumeRole",
                "ec2:AssignPrivateIpAddresses",
                "ec2:CreateRoute",
                "ec2:DescribeVpcs",
                "ec2:ReplaceRoute",
                "ec2:UnassignPrivateIpAddresses",
                "s3:PutObjectTagging",
                "s3:GetObjectTagging",
                "fsx:Describe*",
                "fsx:List*",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteSnapshot",
                "ec2:DeleteTags",
                "ec2:DeleteRoute",
                "ec2:DeletePlacementGroup",
                "iam:DeleteRole",
                "iam:DeleteRolePolicy",
                "iam:DeleteInstanceProfile",
                "cloudformation:DeleteStack",
                "ec2:DescribePlacementGroups",
                "iam:GetRolePolicy",
                "s3:ListAllMyBuckets",
                "s3:GetObject",
                "iam:GetRole",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:PutObject",
                "ec2:ModifyVolume",
                "ec2:DescribeVolumesModifications"
            ],
            "Resource": "*"
            },
            {
            "Sid": "backupPolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeImages",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSecurityGroup",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeRegions",
                "cloudformation:CreateStack",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeStacks",
                "kms:List*",
                "kms:Describe*",
                "ec2:describeVpcEndpoints",
                "kms:ListAliases",
                "athena:StartQueryExecution",
                "athena:GetQueryResults",
                "athena:GetQueryExecution",
                "athena:StopQueryExecution",
                "glue:CreateDatabase",
                "glue:CreateTable",
                "glue:BatchDeletePartition"
            ],
            "Resource": "*"
            },
            {
            "Sid": "backupS3Policy",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:CreateBucket",
                "s3:GetLifecycleConfiguration",
                "s3:PutLifecycleConfiguration",
                "s3:PutBucketTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketAcl",
                "s3:PutBucketPublicAccessBlock",
                "s3:GetObject",
                "s3:PutEncryptionConfiguration",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:ListBucketMultipartUploads",
                "s3:PutObject",
                "s3:PutBucketAcl",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts",
                "s3:DeleteBucket"
            ],
            "Resource": [
                "arn:aws:s3:::netapp-backup-*"
            ]
            },
            {
            "Sid": "tagServicePolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags",
                "ec2:DescribeTags",
                "tag:getResources",
                "tag:getTagKeys",
                "tag:getTagValues",
                "tag:TagResources",
                "tag:UntagResources"
            ],
            "Resource": "*"
            },
            {
            "Sid": "fabricPoolS3Policy",
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:GetLifecycleConfiguration",
                "s3:PutLifecycleConfiguration",
                "s3:PutBucketTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketPolicyStatus",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketAcl",
                "s3:GetBucketPolicy",
                "s3:PutBucketPublicAccessBlock",
                "s3:DeleteBucket"
            ],
            "Resource": [
                "arn:aws:s3:::fabric-pool*"
            ]
            },
            {
            "Sid": "fabricPoolPolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
            },
            {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances"
            ],
            "Condition": {
                "StringLike": {
                "ec2:ResourceTag/netapp-adc-manager": "*"
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:instance/*"
            ]
            },
            {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:TerminateInstances",
                "ec2:AttachVolume",
                "ec2:DetachVolume"
            ],
            "Condition": {
                "StringLike": {
                "ec2:ResourceTag/GFCInstance": "*"
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:instance/*"
            ]
            },
            {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:TerminateInstances",
                "ec2:AttachVolume",
                "ec2:DetachVolume",
                "ec2:StopInstances",
                "ec2:DeleteVolume"
            ],
            "Condition": {
                "StringLike": {
                "ec2:ResourceTag/WorkingEnvironment": "*"
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:instance/*"
            ]
            },
            {
            "Effect": "Allow",
            "Action": [
                "ec2:AttachVolume",
                "ec2:DetachVolume"
            ],
            "Resource": [
                "arn:aws:ec2:*:*:volume/*"
            ]
            },
            {
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteVolume"
            ],
            "Condition": {
                "StringLike": {
                "ec2:ResourceTag/WorkingEnvironment": "*"
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:volume/*"
            ]
            },
            {
            "Sid": "K8sServicePolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions",
                "iam:ListInstanceProfiles",
                "eks:ListClusters",
                "eks:DescribeCluster"
            ],
            "Resource": "*"
            },
            {
            "Sid": "GFCservicePolicy",
            "Effect": "Allow",
            "Action": [
                "cloudformation:DescribeStacks",
                "cloudwatch:GetMetricStatistics",
                "cloudformation:ListStacks"
            ],
            "Resource": "*"
            }
        ]
        }
        )
        policy_document2 = iam.PolicyDocument.from_json(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "createfsx",
                    "Effect": "Allow",
                    "Action": [
                        "fsx:*",
                        "ec2:Describe*",
                        "ec2:CreateTags",
                        "kms:Describe*",
                        "kms:List*",
                        "kms:CreateGrant",
                        "iam:CreateServiceLinkedRole"
                    ],
                    "Resource": "*"
                }
            ]
        }
        )
        # Policy 생성
        BlueXP_Policy = iam.Policy(
            self,"HandsonCloudmangerPolicy",
            policy_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "BlueXP_Policy"]),
            document=policy_document
        )
        OCCMFSx = iam.Policy(
            self,"OCCMFSx",
            policy_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "OCCMFSxN_Policy"]),
            document=policy_document2
        )
        # Role 에 Policy 부여
        role.attach_inline_policy(BlueXP_Policy)
        role.attach_inline_policy(OCCMFSx)