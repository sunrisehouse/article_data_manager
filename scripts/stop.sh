#!/bin/bash
echo "[App Stop]================================"
cd /home/ec2-user/lgcns_data_manager

sudo docker-compose down --volumes --rmi all
