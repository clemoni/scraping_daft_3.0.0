FROM postgres:13-alpine

RUN mkdir -p /tmp/insert_data/

ENV POSTGRES_USER airflow
ENV POSTGRES_PASSWORD airflow
ENV POSTGRES_DB airflow

COPY insert_data.sql /tmp/insert_data/
COPY init_db.sql /docker-entrypoint-initdb.d/

# VOLUME ./postgres-data:/var/lib/postgresql/data
EXPOSE 5433