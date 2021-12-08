#!/bin/bash
docker build -t daft-postgres:1.0.0 ./init/postgres && \
docker build -t daft-spark:1.0.0 ./init/spark && \
docker build -t daft-airflow:1.0.0 ./init/airflow && \
docker-compose up airflow-init && \
docker-compose up -d && \
python ./include/generate_config_file.py && \
python ./include/generate_dag_file.py 