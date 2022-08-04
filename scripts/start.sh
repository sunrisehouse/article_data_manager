#!/bin/bash
echo "[App Start]================================"

ENV=$1

if [ $ENV = "local" ]
then
    echo "Local Start !!"
    docker-compose up airflow-init
    docker-compose up -d
else
    echo "Prod Start !!"
    cd /home/ec2-user/lgcns_data_manager
    sudo docker-compose up airflow-init
    sudo docker-compose up -d
fi
