#!/bin/bash 
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
wget https://github.com/NetApp/trident/releases/download/v22.07.0/trident-installer-22.07.0.tar.gz
tar -zxvf trident-installer-22.07.0.tar.gz -C /opt
sudo cp /opt/trident-installer/tridentctl /usr/local/bin
sudo apt-get -y install nfs-common
sudo apt-get -y install unzip
wget https://netappkr-wyahn-s3.s3.ap-northeast-2.amazonaws.com/public/DeployTestapp.zip
sudo unzip DeployTestapp.zip -d /opt/DeployTestapp
apt-get install -y jq
sudo wget -P /opt/ https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64
sudo mv /opt/hey_linux_amd64 /usr/local/bin/hey
sudo chmod 755 /usr/local/bin/hey