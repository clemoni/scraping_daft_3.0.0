from pyspark.sql import SparkSession
import sys
import my_packages.dbtools.db_main as db
import random


PSQL_HOST = "postgres"
PSQL_PORT = "5432"
PSQL_DB = "scraping_daft"
PSQL_USERNAME = "airflow"
PSQL_PASSWORD = "airflow"


select_id_by_null_advert_id = """SELECT id
FROM rent
WHERE advert_id IS NULL"""

update_ads_is_closed = """UPDATE rent
SET is_closed='true', closed_at=Now()
WHERE id=:id"""

if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Persist DB") \
        .config("spark.driver.bindAddress", "localhost") \
        .getOrCreate()

    path = 'postgresql+psycopg2://airflow:airflow@postgres/scraping_daft'
    db_select = db.init_select(path)

    fake_ads_ids = [res[0] for res in db_select(select_id_by_null_advert_id)()]

    db.init_insert(path)(update_ads_is_closed)(
        [{'id': id} for id in fake_ads_ids])
