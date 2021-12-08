#!/bin/bash
docker-compose down && \
docker-compose down --volumes --rmi all && \
rm -rf dags data logs plugins conf && \
rm ./include/dag_config/*