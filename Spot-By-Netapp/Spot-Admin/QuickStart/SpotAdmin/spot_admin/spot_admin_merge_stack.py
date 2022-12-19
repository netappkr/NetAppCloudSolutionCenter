from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    Duration,
    SecretValue,
    CfnOutput,
    aws_fsx as fsx,
    CfnTag
)
from constructs import Construct

class MergeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "SpotAdmin-VPC",
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
            self, "SpotAdminbastionRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            # custom description if desired
            description="Netapp SpotAdmin Hands on bastion Role"
        )
        bastionrole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        ## AMI
        AMI = ec2.MachineImage.generic_linux(
            {
            "ap-northeast-2": "ami-0632d76430fad92e4"
            }
        )


        ## 보안그룹
        SecurityGroup = ec2.SecurityGroup(self,"SpotAdminbastionSG",vpc=vpc)
        SecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        
        ## Keypair
        keyPair=ec2.CfnKeyPair(self, "SpotAdminkey",
            key_name="SpotAdminkey",
            public_key_material="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvu2v6lkF59XSY3ch+Df2w/AN10EPXZ3JL2Xbqtsv13xVq9ZuzmUcdCpfa9NyjnyBoaXxymUvQSaeQCFxnjroAySOKVXaR6n6ahWFGQOYlfZHkKYg/N8pTpQht3QXNLoA8lUlrb3lyehQHxtCAhtgmx4BIaBpGM/FLaJqhu1OQ7gz0GBbG1qZOmEyrzcklkvriyPYzEESg3N9w+eM09rWvu3dK+EezAsgeFBlcsfHY5eNRmgp2iPfvz8tNZ3wgsrU/UiZHueqsMmGYS+Njjr461cx2q3EhjjPbYz8+tj3t/taZ/Jf419r9ZhT1JHm8/vUh22B5Xm31LdbMBPGvuUKPQ=="
        )
        user_data = ec2.UserData.for_linux()
        user_data.add_commands("aws s3 cp s3://netappkr-wyahn-s3/public/DeployTestapp/ /opt/DeployTestapp --recursive")
        # 서버생성
        ec2.Instance(self, "SpotAdminbastion",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            machine_image=AMI,
            role=bastionrole,
            security_group=SecurityGroup,
            key_name="SpotAdminkey",
            user_data=user_data
        )

        userdata_file = open("./userdata.sh", "rb").read()

        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))

        ## AMI
        AMI = ec2.MachineImage.generic_linux(
            {
            "ap-northeast-2": "ami-097de6c1fdd6b0ddd"
            }
        )
        asg = autoscaling.AutoScalingGroup(
            self,
            "wordpress-asg",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY5, ec2.InstanceSize.XLARGE
            ),
            machine_image=AMI,
            key_name=keyPair.key_name,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            user_data=userdata,
        )

        # Creates a security group for our application
        WordpressSG = ec2.SecurityGroup(
                self,
                id="WordpressSG",
                vpc=vpc,
                security_group_name="Wordpress-SG"
        )

        # Allows only the IP of "any"
        # to access this security group for SSH
        WordpressSG.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description = "allow ssh access from the world"
        )
        WordpressSG.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description = "allow http access from the world"
        )
        WordpressSG.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description = "allow https access from the world"
        )
        WordpressSG.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(443),
            description = "allow https access from the world"
        )

        # Creates a security group for the application load balancer
        AppLBSG = ec2.SecurityGroup(
                self,
                id="AppLBSG",
                vpc=vpc,
                security_group_name="AppLB-SG"
        )

        # Allows connections from security group "AppLBSG"
        # inside the "WordpressSG" security group to access port 8080
        # where our app listens
        WordpressSG.connections.allow_from(
                AppLBSG, ec2.Port.tcp(80), "Ingress")

        # Adds the security group 'WordpressSG' to the autoscaling group
        asg.add_security_group(WordpressSG)

        # Creates an application load balance
        AppLB = elbv2.ApplicationLoadBalancer(
                self,
                "ALB",
                vpc=vpc,
                security_group=AppLBSG,
                load_balancer_name="SpotAdminALB",
                internet_facing=True)

        listener = AppLB.add_listener("Listener", port=80)
        # Adds the autoscaling group's (asg) instance to be registered
        # as targets on port 80
        listener.add_targets("Target", port=80, targets=[asg], stickiness_cookie_duration=Duration.minutes(5), target_group_name= "spotadmin-wordpress-TG")
        # This creates a "0.0.0.0/0" rule to allow every one to access the
        # application
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")

        #EKS
        cluster = eks.Cluster(self, "SpotAdmin-eks",
            version=eks.KubernetesVersion.V1_21,
            vpc = vpc,
            default_capacity=1,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
            cluster_name = "SpotAdmin-eks",
            alb_controller = eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_4_1
            )
        )
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow http access from the world")
        cluster.cluster_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow https access from the world")
        
        cluster.add_nodegroup_capacity("custom-node-group",
            instance_types=[
                ec2.InstanceType("m5.large")],
                nodegroup_name = "custom-ng",
                desired_size = 1,
                labels={
                    "purpose": "test"
                },
                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                remote_access=eks.NodegroupRemoteAccess(ssh_key_name=keyPair.key_name),
                min_size = 0
        )
        #iam
        admin_user = iam.User(
            self, "SpotAdminAdmin",
            user_name="SpotAdminAdmin", 
            password=SecretValue.unsafe_plain_text("SpotAdmin123!@#")
        )
        admin_user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        #admin_user.addToGroup(IGroup.fromGroupArn("arn:aws:iam::<your aws account id>:group/admin"))
        
        # EKS에 iam user등록
        cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
        cluster.aws_auth.add_role_mapping(bastionrole, groups=["system:masters"])

        #core.CfnOutput(core,construct_id,value="출력")