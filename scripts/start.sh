#!/bin/bash
echo "[App Start]================================"
cd /home/ec2-user/lgcns_data_manager

sudo docker-compose up airflow-init
sudo docker-compose up -d
