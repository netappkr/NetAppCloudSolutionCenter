
# Terraform cheat sheet
적용 전 확인
```
terraform plan -var-file="wyahn.tfvars"
```
적용
```
terraform apply -var-file="wyahn.tfvars"
```

FSxN만 삭제하기
```
terraform destroy -target aws_fsx_ontap_storage_virtual_machine.SeanPFsxNSVM -target aws_fsx_ontap_file_system.SeanPFsxN -var-file="wyahn.tfvars"
```
Terraform 자원 목록 보기
```
terraform state list
```
```
data.aws_vpc_peering_connection.pc
aws_eip.SeanPVPC-NAT-EIP
aws_fsx_ontap_file_system.SeanPFsxN
aws_fsx_ontap_storage_virtual_machine.SeanPFsxNSVM
aws_internet_gateway.SeanPVPC-igw
aws_nat_gateway.SeanPVPC-Nat
aws_route_table.SeanPVPC-private-rt
aws_route_table.SeanPVPC-public-rt
aws_route_table_association.private-associations-a
aws_route_table_association.private-associations-b
aws_route_table_association.private-associations-c
aws_route_table_association.private-associations-d
aws_route_table_association.public-associations-a
aws_route_table_association.public-associations-b
aws_route_table_association.public-associations-c
aws_route_table_association.public-associations-d
aws_subnet.SeanPVPC-Private-sub-a
aws_subnet.SeanPVPC-Private-sub-b
aws_subnet.SeanPVPC-Private-sub-c
aws_subnet.SeanPVPC-Private-sub-d
aws_subnet.SeanPVPC-Public-sub-a
aws_subnet.SeanPVPC-Public-sub-b
aws_subnet.SeanPVPC-Public-sub-c
aws_subnet.SeanPVPC-Public-sub-d
aws_vpc.SeanP-VPC
```