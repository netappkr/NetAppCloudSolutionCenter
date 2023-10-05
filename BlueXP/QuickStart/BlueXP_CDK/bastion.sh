yum -y update

# install aws cli v2
ARCH=$(uname -m)
curl "https://awscli.amazonaws.com/awscli-exe-linux-$ARCH.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update

# install python 3
yum install -y python3

# install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /opt
sudo mv /tmp/eksctl /usr/local/bin

# install tridentctl
wget https://github.com/NetApp/trident/releases/download/v23.07.1/trident-installer-23.07.1.tar.gz
sudo tar -zxvf trident-installer-23.01.0.tar.gz -C /opt
sudo install -o root -g root -m 0755 /opt/trident-installer/tridentctl /usr/local/bin/tridentctl

# bash-completton
sudo yum install bash-completion
sudo kubectl completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
sudo echo 'alias k=kubectl' >> /etc/bashrc
sudo echo 'complete -o default -F __start_kubectl k' >> /etc/bashrc