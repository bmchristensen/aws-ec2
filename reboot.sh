#!/bin/bash

sudo su root

yum update -y
yum upgrade -y

cd ~
cd aws-ec2

git pull
python3 server.py
