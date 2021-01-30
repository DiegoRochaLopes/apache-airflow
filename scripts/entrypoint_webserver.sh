#!/usr/bin/env bash

echo "=== Clear logs ==="
rm -rfv ./logs/

airflow db init

echo "=== Installing python dependencies ==="
if [ -e "./scripts/requirements.txt" ]; then
    $(command -v pip) install --user -r ./scripts/requirements.txt
fi

airflow connections add --conn-uri 'postgresql://airflow:airflow@postgres:5432/db_origem' 'db_origem'
airflow connections add --conn-uri 'postgresql://airflow:airflow@postgres:5432/db_destino' 'db_destino'

#create user admin pass
airflow users create -r Admin -u dev -f dev -l dev -p dev -e dev@xerpa.com.br

airflow webserver