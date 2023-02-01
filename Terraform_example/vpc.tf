# terraform import aws_default_vpc.default vpc-7e17af15
resource "aws_vpc" "SeanP-VPC" {
  cidr_block = "172.30.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "SeanP-VPC"
    creator = "SeanP"
    managed = "terraform"
  }
}

# public sub
resource "aws_subnet" "SeanPVPC-Public-sub-a" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.0.0/24"
  availability_zone = "ap-northeast-2a"
  map_public_ip_on_launch = true
  tags = {
    Name = "SeanPVPC-Public-sub-a"
    creator = "SeanP"
    managed = "terraform"
  }
}
resource "aws_subnet" "SeanPVPC-Public-sub-b" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.1.0/24"
  availability_zone = "ap-northeast-2b"
  map_public_ip_on_launch = true
  tags = {
    Name = "SeanPVPC-Public-sub-b"
    creator = "SeanP"
    managed = "terraform"
  }
}
resource "aws_subnet" "SeanPVPC-Public-sub-c" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.2.0/24"
  availability_zone = "ap-northeast-2c"
  map_public_ip_on_launch = true
  tags = {
    Name = "SeanPVPC-Public-sub-c"
    creator = "SeanP"
    managed = "terraform"
  }
}
resource "aws_subnet" "SeanPVPC-Public-sub-d" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.3.0/24"
  availability_zone = "ap-northeast-2d"
  map_public_ip_on_launch = true
  tags = {
    Name = "SeanPVPC-Public-sub-d"
    creator = "SeanP"
    managed = "terraform"
  }
}
#private sub
resource "aws_subnet" "SeanPVPC-Private-sub-a" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.4.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "SeanPVPC-Private-sub-a"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_subnet" "SeanPVPC-Private-sub-b" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.5.0/24"
  availability_zone = "ap-northeast-2b"

  tags = {
    Name = "SeanPVPC-Private-sub-b"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_subnet" "SeanPVPC-Private-sub-c" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.6.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "SeanPVPC-Private-sub-c"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_subnet" "SeanPVPC-Private-sub-d" {
  vpc_id     = aws_vpc.SeanP-VPC.id
  cidr_block = "172.30.7.0/24"
  availability_zone = "ap-northeast-2d"

  tags = {
    Name = "SeanPVPC-Private-sub-d"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_internet_gateway" "SeanPVPC-igw" {
  vpc_id = aws_vpc.SeanP-VPC.id

  tags = {
    Name = "SeanPVPC-igw"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_eip" "SeanPVPC-NAT-EIP" {
  vpc      = true
    tags = {
    Name = "SeanPVPC-NAT-EIP"
    creator = "SeanP"
    managed = "terraform"
  }
  depends_on = [aws_internet_gateway.SeanPVPC-igw]
}
resource "aws_nat_gateway" "SeanPVPC-Nat" {
  connectivity_type = "public"
  subnet_id     = aws_subnet.SeanPVPC-Private-sub-a.id
  allocation_id = aws_eip.SeanPVPC-NAT-EIP.id
  tags = {
    Name = "SeanPVPC-Nat"
    creator = "SeanP"
    managed = "terraform"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.SeanPVPC-igw]
}

# data "aws_vpc_peering_connection" "pc" {
#  vpc_id = aws_vpc.SeanP-VPC.id
#  peer_cidr_block = "172.31.0.0/16"
# }

resource "aws_route_table" "SeanPVPC-public-rt" {
  vpc_id = aws_vpc.SeanP-VPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.SeanPVPC-igw.id
  }

#  route {
#    cidr_block = "172.31.0.0/16"
#    vpc_peering_connection_id = data.aws_vpc_peering_connection.pc.id
#  }

  tags = {
    Name = "SeanPVPC-public-rt"
    creator = "SeanP"
    managed = "terraform"
  }
}

resource "aws_route_table" "SeanPVPC-private-rt" {
  vpc_id = aws_vpc.SeanP-VPC.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.SeanPVPC-Nat.id
  }

#  route {
#    cidr_block = "172.31.0.0/16"
#    vpc_peering_connection_id = data.aws_vpc_peering_connection.pc.id
#  }

  tags = {
    Name = "SeanPVPC-private-rt"
    creator = "SeanP"
    managed = "terraform"
  }
}

# Public RT associations
resource "aws_route_table_association" "public-associations-a" {
  subnet_id      = aws_subnet.SeanPVPC-Public-sub-a.id
  route_table_id = aws_route_table.SeanPVPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-b" {
  subnet_id      = aws_subnet.SeanPVPC-Public-sub-b.id
  route_table_id = aws_route_table.SeanPVPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-c" {
  subnet_id      = aws_subnet.SeanPVPC-Public-sub-c.id
  route_table_id = aws_route_table.SeanPVPC-public-rt.id
}
resource "aws_route_table_association" "public-associations-d" {
  subnet_id      = aws_subnet.SeanPVPC-Public-sub-d.id
  route_table_id = aws_route_table.SeanPVPC-public-rt.id
}

# Private RT associations
resource "aws_route_table_association" "private-associations-a" {
  subnet_id      = aws_subnet.SeanPVPC-Private-sub-a.id
  route_table_id = aws_route_table.SeanPVPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-b" {
  subnet_id      = aws_subnet.SeanPVPC-Private-sub-b.id
  route_table_id = aws_route_table.SeanPVPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-c" {
  subnet_id      = aws_subnet.SeanPVPC-Private-sub-c.id
  route_table_id = aws_route_table.SeanPVPC-private-rt.id
}
resource "aws_route_table_association" "private-associations-d" {
  subnet_id      = aws_subnet.SeanPVPC-Private-sub-d.id
  route_table_id = aws_route_table.SeanPVPC-private-rt.id
}

