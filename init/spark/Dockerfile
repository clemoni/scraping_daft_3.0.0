FROM bitnami/spark:3.2.0

USER root 

RUN mkdir -p /opt/spark/jars

COPY postgresql-42.3.1.jar /opt/spark/jars

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

USER ${AIRFLOW_UID}