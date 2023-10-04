from optparse import Values
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_fsx as fsx,
    CfnTag,
    CfnParameter,
    Fn
)
from constructs import Construct


class FSxNStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # parameter
        prefix = CfnParameter(self, "prefix", type="String", default="netapp",
                              description="this parm use prefix or id in cfn. please input only english and all in lower case")
        # joinAD = CfnParameter(self, "prefix", type="Boolean", default=False,description="do you required join AD?")
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
                                            # 조건 부 옵션 추가 설정 방법 모르겠음... 
                                        
                                            # Fn.condition_if(value_if_true="joinAD",condition_id=)
                                            # self_managed_active_directory_configuration_property=fsx.CfnFileSystem.SelfManagedActiveDirectoryConfigurationProperty(
                                            #     dns_ips=[ad_dns_ips],
                                            #     domain_name=ad_domain_name,
                                            #     file_system_administrators_group=ad_file_system_administrators_group,
                                            #     organizational_unit_distinguished_name=ad_organizational_unit_distinguished_name,
                                            #     password=ad_password,
                                            #     user_name=ad_user_name
                                            # )
                                            )
