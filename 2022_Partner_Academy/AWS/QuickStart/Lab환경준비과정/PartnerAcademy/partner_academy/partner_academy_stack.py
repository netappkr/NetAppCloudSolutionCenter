from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    SecretValue,
    CfnOutput,
    aws_fsx as fsx,
    CfnTag
)
from constructs import Construct

class PartnerAcademyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "Hands-on-VPC",
            cidr="172.30.0.0/16",
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(cidr_mask=24,name="public-subnet",subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(cidr_mask=24,name="private-subnet",subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
                ]
        )
        # CfnOutput(self,"private-subnet-id-0",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[0])
        # CfnOutput(self,"private-subnet-id-1",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[1])
        # CfnOutput(self,"routetable-id",value=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnets[0].route_table.route_table_id)
        
        # Hands-on bastion 생성
        bastionrole = iam.Role(
            self, "HandsonbastionRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp Pertner Summit Hands on bastion Role"
        )
        bastionrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        ## AMI
        AMI = ec2.MachineImage.generic_linux(
            {
            "ap-northeast-2": "ami-0f66e1efa1404fdaf"
            }
        )


        ## 보안그룹
        SecurityGroup = ec2.SecurityGroup(self,"handsonbastionSG",vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        
        ## Keypair
        ec2.CfnKeyPair(self, "Handsonkey",
            key_name="Handsonkey",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvu2v6lkF59XSY3ch+Df2w/AN10EPXZ3JL2Xbqtsv13xVq9ZuzmUcdCpfa9NyjnyBoaXxymUvQSaeQCFxnjroAySOKVXaR6n6ahWFGQOYlfZHkKYg/N8pTpQht3QXNLoA8lUlrb3lyehQHxtCAhtgmx4BIaBpGM/FLaJqhu1OQ7gz0GBbG1qZOmEyrzcklkvriyPYzEESg3N9w+eM09rWvu3dK+EezAsgeFBlcsfHY5eNRmgp2iPfvz8tNZ3wgsrU/UiZHueqsMmGYS+Njjr461cx2q3EhjjPbYz8+tj3t/taZ/Jf419r9ZhT1JHm8/vUh22B5Xm31LdbMBPGvuUKPQ=="
        )
        user_data = ec2.UserData.for_linux()
        user_data.add_commands("aws s3 cp s3://netappkr-wyahn-s3/public/DeployTestapp/ /opt/DeployTestapp --recursive")
        # 서버생성
        ec2.Instance(self, "Handsonbastion",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            machine_image=AMI,
            role=bastionrole,
            security_group=SecurityGroup,
            key_name="Handsonkey",
            user_data=user_data
        )


        #EKS
        cluster = eks.Cluster(self, "Hands-on-eks",
            version=eks.KubernetesVersion.V1_21,
            vpc = vpc,
            default_capacity=1,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            cluster_name = "Hands-on-eks",
            alb_controller = eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_4_1
            )
        )
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow http access from the world")
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow https access from the world")
        #iam
        admin_user = iam.User(
            self, "HandsOnAdmin",
            user_name="HandsOnAdmin", 
            password=SecretValue.unsafe_plain_text("HandsOnAdmin123!@#")
        )
        admin_user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        #admin_user.addToGroup(IGroup.fromGroupArn("arn:aws:iam::<your aws account id>:group/admin"))
        
        # EKS에 iam user등록
        cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
        cluster.aws_auth.add_role_mapping(bastionrole, groups=["system:masters"])

        #core.CfnOutput(core,construct_id,value="출력")

        #CloudmanagerRole 생성
        role = iam.Role(
            self, "HandsonCloudmangerRole",
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
        HandsonCloudmangerPolicy = iam.Policy(
            self,"HandsonCloudmangerPolicy",
            document=policy_document
        )
        HandsonOCCMFSx = iam.Policy(
            self,"HandsonOCCMFSx",
            document=policy_document2
        )
        # Role 에 Policy 부여
        role.attach_inline_policy(HandsonCloudmangerPolicy)
        role.attach_inline_policy(HandsonOCCMFSx)

        # FSXontap
        ontap_configuration=fsx.CfnFileSystem.OntapConfigurationProperty(
            deployment_type="MULTI_AZ_1",
            # the properties below are optional
            automatic_backup_retention_days=0,
            #daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
            disk_iops_configuration=fsx.CfnFileSystem.DiskIopsConfigurationProperty(
                mode="AUTOMATIC"
            ),
            #endpoint_ip_address_range="endpointIpAddressRange",
            fsx_admin_password="Netapp1!",
            preferred_subnet_id=vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[0],
            route_table_ids=[
                vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnets[0].route_table.route_table_id,
                vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets[0].route_table.route_table_id
                ],
            throughput_capacity=128
            # weekly_maintenance_start_time="weeklyMaintenanceStartTime"
        )
        cfn_file_system = fsx.CfnFileSystem(self, "Hands-on-fsx",
            file_system_type="ONTAP",
            subnet_ids=[vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[0],vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[1]],
            storage_capacity=1024,
            ontap_configuration=ontap_configuration,
            tags=[
                CfnTag(
                key="Name",
                value="Hands-on-fsx"
            )]
        )

        cfn_storage_virtual_machine = fsx.CfnStorageVirtualMachine(self, "Hands-on-fsx-svm",
        file_system_id=cfn_file_system,
        name="Hands-on-fsx-svm",

        # the properties below are optional
        # active_directory_configuration=fsx.CfnStorageVirtualMachine.ActiveDirectoryConfigurationProperty(
        #    net_bios_name="netBiosName",
        #    self_managed_active_directory_configuration=fsx.CfnStorageVirtualMachine.SelfManagedActiveDirectoryConfigurationProperty(
        #        dns_ips=["dnsIps"],
        #        domain_name="domainName",
        #        file_system_administrators_group="fileSystemAdministratorsGroup",
        #        organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
        #        password="password",
        #        user_name="userName"
        #    )
        #),
        # root_volume_security_style="rootVolumeSecurityStyle",
        svm_admin_password="Netapp1!"
        )