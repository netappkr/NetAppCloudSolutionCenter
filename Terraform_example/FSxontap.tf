#file_system
#This deploy require vpc and subnet


resource "aws_fsx_ontap_file_system" "SeanPFsxN" {
  storage_capacity    = 1024
  subnet_ids          = [aws_subnet.SeanPVPC-Private-sub-a.id]
  deployment_type     = "SINGLE_AZ_1"
  throughput_capacity = 128
  preferred_subnet_id = aws_subnet.SeanPVPC-Private-sub-a.id
  automatic_backup_retention_days = 0
  # route_table_ids = [aws_route_table.SeanPVPC-public-rt.id, aws_route_table.SeanPVPC-private-rt.id]
  fsx_admin_password = var.fsx_admin_password
  tags = {
    Name = "SeanPFsxN"
    creator = "SeanP"
    managed = "terraform"
  }
}

# terraform import aws_fsx_ontap_storage_virtual_machine.wyahnFsxSVM svm-12345678abcdef123
#SVM AD enable
# resource "aws_fsx_ontap_storage_virtual_machine" "SeanPFsxNSVM" {
#   file_system_id = aws_fsx_ontap_file_system.SeanPFsxN.id
#   name           = "SeanPFsxN"
#   active_directory_configuration {
#     netbios_name = "SeanPFsxN"
#     self_managed_active_directory_configuration {
#       dns_ips     = ["172.31.0.152"]
#       domain_name = "wyahn.com"
#       password    = "NetApp123!@#"
#       username    = "wyahn"
#     }
#   }
#   depends_on = [aws_route_table.SeanPVPC-private-rt]
# }

#SVM
resource "aws_fsx_ontap_storage_virtual_machine" "SeanPFsxNSVM" {
  file_system_id = aws_fsx_ontap_file_system.SeanPFsxN.id
  name           = "SeanPFsxN"
  depends_on = [aws_route_table.SeanPVPC-private-rt]
}
# #volume_cifs
# resource "aws_fsx_ontap_volume" "cifs_Vol" {
#   name                       = "cifs_Vol"
#   junction_path              = "/cifs_Vol"
#   size_in_megabytes          = 5120
#   storage_efficiency_enabled = true
#   storage_virtual_machine_id = aws_fsx_ontap_storage_virtual_machine.SeanPFsxNSVM.id

#   tiering_policy {
#     name           = "AUTO"
#     cooling_period = 2
#   }
#   tags = {
#     creator = "SeanP"
#     managed = "terraform"
#   }
# }

#volume_cifs
resource "aws_fsx_ontap_volume" "nfs_Vol" {
  name                       = "nfs_Vol"
  junction_path              = "/nfs_Vol"
  size_in_megabytes          = 5120
  storage_efficiency_enabled = true
  storage_virtual_machine_id = aws_fsx_ontap_storage_virtual_machine.SeanPFsxNSVM.id

  tiering_policy {
    name           = "AUTO"
    cooling_period = 2
  }
  tags = {
    creator = "SeanP"
    managed = "terraform"
  }
}

