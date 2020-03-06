#!/usr/bin/env bash

yum -y install make gcc gcc-c++ 
yum -y install kernel-devel
yum -y install libmpc-devel zlib-devel 

mkdir /root/soft

####elasticsearch
wget  https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.5.2.zip  -P /root/soft
unzip -d /usr/local/elasticsearch /root/soft/elasticsearch-6.5.2.zip
echo 'export PATH=$PATH:/usr/local/elasticsearch/elasticsearch-6.5.2/bin' >> /etc/profile
source /etc/profile

####java
mkdir /usr/local/jdk
wget https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz -P /root/soft
tar -zxvf /root/soft/openjdk-11.0.1_linux-x64_bin.tar.gz -C /usr/local/jdk
echo 'export JAVA_HOME=/usr/local/jdk/jdk-11.0.1' >> /etc/profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile
source /etc/profile

####增加系统用户es
adduser es
passwd es << EOF
{p9Pq8.H9b22!)A[
{p9Pq8.H9b22!)A[
EOF
chown es /root -R
chown es /usr/local/ -R

#为es增加文件描述符
echo 'es soft nofile 65536 ' >>  /etc/security/limits.conf
echo 'es hard nofile  65536 ' >>  /etc/security/limits.conf
echo 'es soft nproc 4096 ' >>  /etc/security/limits.conf
echo 'es hard nproc 4096' >>  /etc/security/limits.conf
#增加虚拟内存区域
echo 'vm.max_map_count=655360' >>  /etc/sysctl.conf
sysctl -p

####python anaconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -P /root/soft
bash /root/soft/Miniconda3-latest-Linux-x86_64.sh << EOF
q
q
yes

yes
EOF
echo 'export PATH=$PATH:/root/miniconda3/bin' >> /etc/profile
source /etc/profile
conda create -n python3 python=3.6 << EOF
yes
EOF

####下载数据
wget http://www.trec-cds.org/clinical_trials.0.tar.gz -P ./data/ClinicalTrials
tar -xvf ./data/ClinicalTrials/clinical_trials.0.tar.gz -C ./data/ClinicalTrials
wget http://www.trec-cds.org/clinical_trials.1.tar.gz -P ./data/ClinicalTrials
tar -xvf ./data/ClinicalTrials/clinical_trials.1.tar.gz -C ./data/ClinicalTrials
wget http://www.trec-cds.org/clinical_trials.2.tar.gz -P ./data/ClinicalTrials
tar -xvf ./data/ClinicalTrials/clinical_trials.2.tar.gz -C ./data/ClinicalTrials
wget http://www.trec-cds.org/clinical_trials.3.tar.gz -P ./data/ClinicalTrials
tar -xvf ./data/ClinicalTrials/clinical_trials.3.tar.gz -C ./data/ClinicalTrials
