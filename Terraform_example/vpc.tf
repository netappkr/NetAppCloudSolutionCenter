# terraform import aws_default_vpc.default vpc-7e17af15
resource "aws_vpc" "VPC" {
  cidr_block = var.vpc-cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = ${var.prefix}+"VPC"
    creator = var.Creator
    managed = "terraform"
  }
}

# public sub
resource "aws_subnet" "VPC-Public-sub-a" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Public-sub-a-cdir")
  availability_zone = "ap-northeast-2a"
  map_public_ip_on_launch = true
  tags = {
    Name = ${var.prefix}+"VPC-Public-sub-a"
    creator = var.Creator
    managed = "terraform"
  }
}
resource "aws_subnet" "VPC-Public-sub-b" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Public-sub-b-cdir")
  availability_zone = "ap-northeast-2b"
  map_public_ip_on_launch = true
  tags = {
    Name = ${var.prefix}+"VPC-Public-sub-b"
    creator = var.Creator
    managed = "terraform"
  }
}
resource "aws_subnet" "VPC-Public-sub-c" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Public-sub-c-cdir")
  availability_zone = "ap-northeast-2c"
  map_public_ip_on_launch = true
  tags = {
    Name = ${var.prefix}+"VPC-Public-sub-c"
    creator = var.Creator
    managed = "terraform"
  }
}
resource "aws_subnet" "VPC-Public-sub-d" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Public-sub-d-cdir")
  availability_zone = "ap-northeast-2d"
  map_public_ip_on_launch = true
  tags = {
    Name = ${var.prefix}+"VPC-Public-sub-d"
    creator = var.Creator
    managed = "terraform"
  }
}
#private sub
resource "aws_subnet" "VPC-Private-sub-a" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Private-sub-a-cdir")
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = ${var.prefix}+"VPC-Private-sub-a"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_subnet" "VPC-Private-sub-b" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Private-sub-b-cdir")
  availability_zone = "ap-northeast-2b"

  tags = {
    Name = ${var.prefix}+"VPC-Private-sub-b"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_subnet" "VPC-Private-sub-c" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Private-sub-c-cdir")
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = ${var.prefix}+"VPC-Private-sub-c"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_subnet" "VPC-Private-sub-d" {
  vpc_id     = aws_vpc.VPC.id
  cidr_block = lookup(var.VPC-sub-cdir, "VPC-Private-sub-d-cdir")
  availability_zone = "ap-northeast-2d"

  tags = {
    Name = ${var.prefix}+"VPC-Private-sub-d"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_internet_gateway" "VPC-igw" {
  vpc_id = aws_vpc.VPC.id

  tags = {
    Name = ${var.prefix}+"VPC-igw"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_eip" "VPC-NAT-EIP" {
  vpc      = true
    tags = {
    Name = ${var.prefix}+"VPC-NAT-EIP"
    creator = var.Creator
    managed = "terraform"
  }
  depends_on = [aws_internet_gateway.VPC-igw]
}
resource "aws_nat_gateway" "VPC-Nat" {
  connectivity_type = "public"
  subnet_id     = aws_subnet.VPC-Private-sub-a.id
  allocation_id = aws_eip.VPC-NAT-EIP.id
  tags = {
    Name = ${var.prefix}+"VPC-Nat"
    creator = var.Creator
    managed = "terraform"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.VPC-igw]
}

# data "aws_vpc_peering_connection" "pc" {
#  vpc_id = aws_vpc.VPC.id
#  peer_cidr_block = "172.31.0.0/16"
# }

resource "aws_route_table" "VPC-public-rt" {
  vpc_id = aws_vpc.VPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.VPC-igw.id
  }

#  route {
#    cidr_block = "172.31.0.0/16"
#    vpc_peering_connection_id = data.aws_vpc_peering_connection.pc.id
#  }

  tags = {
    Name = ${var.prefix}+"VPC-public-rt"
    creator = var.Creator
    managed = "terraform"
  }
}

resource "aws_route_table" "VPC-private-rt" {
  vpc_id = aws_vpc.VPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.VPC-Nat.id
  }

#  route {
#    cidr_block = "172.31.0.0/16"
#    vpc_peering_connection_id = data.aws_vpc_peering_connection.pc.id
#  }

  tags = {
    Name = ${var.prefix}+"VPC-private-rt"
    creator = var.Creator
    managed = "terraform"
  }
}

# Public RT associations
resource "aws_route_table_association" "public-associations-a" {
  subnet_id      = aws_subnet.VPC-Public-sub-a.id
  route_table_id = aws_route_table.VPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-b" {
  subnet_id      = aws_subnet.VPC-Public-sub-b.id
  route_table_id = aws_route_table.VPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-c" {
  subnet_id      = aws_subnet.VPC-Public-sub-c.id
  route_table_id = aws_route_table.VPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-d" {
  subnet_id      = aws_subnet.VPC-Public-sub-d.id
  route_table_id = aws_route_table.VPC-public-rt.id
}

# Private RT associations
resource "aws_route_table_association" "private-associations-a" {
  subnet_id      = aws_subnet.VPC-Private-sub-a.id
  route_table_id = aws_route_table.VPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-b" {
  subnet_id      = aws_subnet.VPC-Private-sub-b.id
  route_table_id = aws_route_table.VPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-c" {
  subnet_id      = aws_subnet.VPC-Private-sub-c.id
  route_table_id = aws_route_table.VPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-d" {
  subnet_id      = aws_subnet.VPC-Private-sub-d.id
  route_table_id = aws_route_table.VPC-private-rt.id
}

