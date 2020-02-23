#!/bin/bash

yum update -y
yum upgrade -y

cd ~
cd /root/aws-ec2

git pull
chmod +x reboot.sh
python3 server.py
