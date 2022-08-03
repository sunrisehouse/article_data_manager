#!/bin/bash
echo "[App Start]================================"
sudo docker-compose down --volumes --rmi all

sudo docker-compose up airflow-init
sudo docker-compose up
