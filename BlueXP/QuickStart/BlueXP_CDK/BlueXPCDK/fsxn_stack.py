from optparse import Values
from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
    aws_fsx as fsx,
    CfnTag,
    CfnParameter,
    CfnOutput,
    Fn
)
from constructs import Construct


class FSxNStack(NestedStack):
    def __init__(self, scope: Construct, id: str, vpc, AD, defaultsg, prefix, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # parameter
        # prefix = CfnParameter(self, "prefix", type="String", default="netapp",description="this parm use prefix or id in cfn. please input only english and all in lower case")
        #ad_dns_ips=AD.attr_dns_ip_addresses
        ad_dns_ips=Fn.split(",", Fn.import_value("dnsipaddress"))
        ad_domain_name = AD.name
        ad_file_system_administrators_group = prefix.value_as_string
        ad_organizational_unit_distinguished_name = Fn.join(delimiter="", list_of_values=["OU=Computers,OU=",prefix.value_as_string,",DC=",prefix.value_as_string,",DC=com"])
        ## example : OU=Computers,OU=wyahn,DC=wyahn,DC=com
        ad_user_name = "Admin"
        ad_password = "Netapp1!"

        CfnOutput(self, "adorginfo", value=ad_organizational_unit_distinguished_name)
        # FSXontap
        self.cfn_file_system = fsx.CfnFileSystem(self, "fsx",
                                            file_system_type="ONTAP",
                                            subnet_ids=[vpc.select_subnets(
                                                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0]],
                                            storage_capacity=1024,
                                            security_group_ids=[defaultsg.security_group_id],
                                            tags=[CfnTag(
                                                key="Name",
                                                value=Fn.join(delimiter="-", list_of_values=[
                                                    prefix.value_as_string, "FSxN"])
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
                                                throughput_capacity=128
                                            )
        )
        # SVM
        self.cfn_storage_virtual_machine = fsx.CfnStorageVirtualMachine(self, "CfnStorageVirtualMachine",
            file_system_id=Fn.select(1,Fn.split('/',self.cfn_file_system.attr_resource_arn)),
            name=Fn.join(delimiter="-", list_of_values=[prefix.value_as_string, "svm"]),
            active_directory_configuration=fsx.CfnStorageVirtualMachine.ActiveDirectoryConfigurationProperty(
                net_bios_name="FSxN",
                self_managed_active_directory_configuration=fsx.CfnStorageVirtualMachine.SelfManagedActiveDirectoryConfigurationProperty(
                    dns_ips=ad_dns_ips,
                    domain_name=ad_domain_name,
                    #file_system_administrators_group=ad_file_system_administrators_group,
                    organizational_unit_distinguished_name=ad_organizational_unit_distinguished_name,
                    password=ad_password,
                    user_name=ad_user_name
                )
            ),
            root_volume_security_style="NTFS",
            svm_admin_password="Netapp1!"
        )
        CfnOutput(self, "svmid", value=self.cfn_storage_virtual_machine.attr_storage_virtual_machine_id)
        
        #volume
        self.cfn_volume = fsx.CfnVolume(self, "CifsVolume",
            name=Fn.join(delimiter="_", list_of_values=[prefix.value_as_string, "volume"]),
            volume_type="ONTAP",
            # the properties below are optional
            #backup_id="backupId",
            ontap_configuration=fsx.CfnVolume.OntapConfigurationProperty(
                size_in_megabytes="10240",
                storage_virtual_machine_id=self.cfn_storage_virtual_machine.attr_storage_virtual_machine_id,

                # the properties below are optional
                # copy_tags_to_backups=prefix.value_as_string,
                junction_path=Fn.join(delimiter="", list_of_values=["/",prefix.value_as_string]),
                ontap_volume_type="RW",
                security_style="NTFS",
                # snaplock_configuration=fsx.CfnVolume.SnaplockConfigurationProperty(
                #     snaplock_type="snaplockType",

                #     # the properties below are optional
                #     audit_log_volume="auditLogVolume",
                #     autocommit_period=fsx.CfnVolume.AutocommitPeriodProperty(
                #         type="type",

                #         # the properties below are optional
                #         value=123
                #     ),
                #     privileged_delete="privilegedDelete",
                #     retention_period=fsx.CfnVolume.SnaplockRetentionPeriodProperty(
                #         default_retention=fsx.CfnVolume.RetentionPeriodProperty(
                #             type="type",

                #             # the properties below are optional
                #             value=123
                #         ),
                #         maximum_retention=fsx.CfnVolume.RetentionPeriodProperty(
                #             type="type",

                #             # the properties below are optional
                #             value=123
                #         ),
                #         minimum_retention=fsx.CfnVolume.RetentionPeriodProperty(
                #             type="type",

                #             # the properties below are optional
                #             value=123
                #         )
                #     ),
                #     volume_append_mode_enabled="volumeAppendModeEnabled"
                # ),
                snapshot_policy=None,
                storage_efficiency_enabled="True",
                tiering_policy=fsx.CfnVolume.TieringPolicyProperty(
                    cooling_period=2,
                    name="SNAPSHOT_ONLY"
                )
            )
        )
