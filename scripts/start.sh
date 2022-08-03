#!/bin/bash
echo "[App Start]================================"
cd /home/ec2-user/lgcns_data_manager

sudo docker-compose down --volumes --rmi all

sudo docker-compose up airflow-init
sudo docker-compose up -d
