from typing_extensions import Self
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    SecretValue,
    CfnOutput,
    aws_fsx as fsx
)
from constructs import Construct
import app
class fsxontapStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        # FSXontap
        cfn_file_system = fsx.CfnFileSystem(self, "Hands-on-fsx",
            file_system_type="ONTAP",
            subnet_ids=[app.PrivateSubnetId0,app.PrivateSubnetId1]
        )
        ontap_configuration=fsx.CfnFileSystem.OntapConfigurationProperty(
            deployment_type="deploymentType",

            # the properties below are optional
            automatic_backup_retention_days=0,
            #daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
            disk_iops_configuration=fsx.CfnFileSystem.DiskIopsConfigurationProperty(
                mode="AUTOMATIC"
            ),
            #endpoint_ip_address_range="endpointIpAddressRange",
            fsx_admin_password="Netapp1!",
            # preferred_subnet_id="preferredSubnetId",
            # route_table_ids=[[]],
            throughput_capacity=123,
            weekly_maintenance_start_time="weeklyMaintenanceStartTime"
        )