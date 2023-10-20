from optparse import Values
from aws_cdk import (
    NestedStack,
    aws_iam as iam,
    CfnParameter,
    CfnOutput,
    Fn
)
from constructs import Construct

class BlueXPReqStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, prefix, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameter
        #prefix = CfnParameter(self, "prefix", type="String", default=prefix.value_as_string, description="this parm use prefix or id in cfn. please input only english and all in lower case")
        #CloudmanagerRole 생성
        role = iam.Role(self, "BlueXP_Role",
                        role_name=Fn.join(delimiter="_", list_of_values=[
                              prefix.value_as_string, "BlueXP_Role"]),
            assumed_by=iam.AccountPrincipal("952013314444"),
            # custom description if desired
            description="Netapp Hands on BlueXP Role"
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

        CfnOutput(self, "BlueXPRoleArn", value=role.role_arn)
        CfnOutput(self, "BluxXP.CredentinalName", value=Fn.join(delimiter="_", list_of_values=[self.account,role.role_name]))