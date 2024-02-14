variable "fsx_admin_password" {
  description = "fsx for ontap admin password"
  type        = string
  sensitive   = true
}

variable "prefix" {
  description = "prefix"
  type        = string
  sensitive   = true
}

variable "Creator" {
  description = "Creator tag value"
  type        = string
  sensitive   = true
}

variable "vpc-cdir" {
  description = "VPC-cidr 10.92.0.0/16"
  type        = string
  sensitive   = true
  default     = "10.92.0.0/16"
}
variable "VPC-sub-cdir" {
  description = "subnet-cidr 10.92.0.0/24"
  type        = map
  sensitive   = true
  default     = {
    "VPC-Public-sub-a-cdir" = "10.92.0.0/24",
    "VPC-Private-sub-a-cdir" = "10.92.1.0/24",
    "VPC-Public-sub-b-cdir" = "10.92.2.0/24",
    "VPC-Private-sub-b-cdir" = "10.92.3.0/24",
    "VPC-Public-sub-c-cdir" = "10.92.4.0/24",
    "VPC-Private-sub-c-cdir" = "10.92.5.0/24"
    "VPC-Public-sub-d-cdir" = "10.92.6.0/24",
    "VPC-Private-sub-d-cdir" = "10.92.7.0/24"
  }
}

variable "eks-clustername" {
  description = "eks-cluster name"
  type        = string
  sensitive   = true
}

