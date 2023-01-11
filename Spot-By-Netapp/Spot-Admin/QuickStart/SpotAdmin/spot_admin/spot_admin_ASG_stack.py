from aws_cdk.aws_ec2 import SubnetType
from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    Duration
    )
from constructs import Construct

class ASGStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, keypair, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        userdata_file = open("./userdata.sh", "rb").read()

        # Creates a userdata object for Linux hosts
        userdata = ec2.UserData.for_linux()
        # Adds one or more commands to the userdata object.
        userdata.add_commands(str(userdata_file, 'utf-8'))

        ## AMI
        AMI = ec2.MachineImage.generic_linux(
            {
            "ap-northeast-2": "ami-097de6c1fdd6b0ddd",
            "us-east-1" : "ami-06ae61f84151ed8cd",
            "us-east-2" : "ami-08b017cdaea47e2c1",
            "us-west-1" : "ami-05a54dcc0c98c8bc6",
            "us-west-2" : "ami-0f650af0664024939",
            "ap-northeast-3" : "ami-05a19c473ced2b2b9",
            "ap-southeast-2" : "ami-01a9e2e12c28937d5",
            "ap-northeast-1" : "ami-02eae9af12de01aae",
            "eu-central-1" : "ami-07afa59ac5b958b39",
            "ap-southeast-1" : "ami-0dafd5bd4bd2655ee",
            "eu-west-1" : "ami-018f740244757a6e3",
            "eu-west-2" : "ami-0103f11e0252ea397",
            "eu-west-3" : "ami-0374f232079b7698c"
            }
        )
        asg = autoscaling.AutoScalingGroup(
            self,
            "wordpress-asg",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM
            ),
            machine_image=AMI,
            key_name=keypair.key_name,
            vpc_subnets=ec2.SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_EGRESS),
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
        listener.add_targets("Target", 
        port=80, targets=[asg],
        target_group_name= "spotadmin-wordpress-TG")
        # This creates a "0.0.0.0/0" rule to allow every one to access the
        # application
        listener.connections.allow_default_port_from_any_ipv4("Open to the world")