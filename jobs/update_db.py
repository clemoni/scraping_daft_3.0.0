from my_packages.main import COUNTIES
import argparse

from pyspark.sql import SparkSession
from pathlib import Path

# spark-submit \
# --master spark://29465e8f5373:7077 \
# --driver-class-path /opt/spark/jars/postgresql-42.3.1.jar \
# --jars /opt/spark/jars/postgresql-42.3.1.jar \
# /opt/airflow/jobs/update_db.py louth


if __name__ == "__main__":
    get_ads_parser = argparse.ArgumentParser(
        prog="get_ads_per_county",
        description="Arguments for the get ads per county spark job")

    get_ads_parser.add_argument("county",
                                action="store",
                                choices=COUNTIES,
                                help="One of Irlande county,see https://en.wikipedia.org/wiki/List_of_Irish_counties_by_area")

    # conf = pyspark.SparkConf()
    # sc = pyspark.SparkContext(conf=conf)
    spark = SparkSession \
        .builder \
        .appName("Update DB") \
        .getOrCreate()
    args = get_ads_parser.parse_args()

    # base = Path(__file__).resolve().parents[1]
    file = f"/opt/airflow/data/{args.county}_rent.json"
    new_ads = spark.read.format("json").option("multiLine", "true").load(file)

    new_ads.createOrReplaceTempView("new_ads")
    new_ads_ids = spark.sql("SELECT advert_id FROM new_ads")
    test = spark.sql("SELECT * FROM new_ads LIMIT 1")

    PSQL_SERVERNAME = "postgres"
    PSQL_PORT = 5432
    PSQL_DB = "scraping_daft"
    PSQL_USERNAME = "airflow"
    PSQL_PASSWORD = "airflow"

    url = f"jdbc:postgresql://{PSQL_SERVERNAME}:{PSQL_PORT}/{PSQL_DB}"

    # jdbcDF1 = spark.read.format("jdbc").option("query", "SELECT * FROM county").option("url", url).option(
    #     "user", PSQL_USERNAME).option("password", PSQL_PASSWORD).load()

    old_ads_ids = spark.read \
        .format("jdbc") \
        .option("query", "SELECT advert_id FROM rent WHERE is_closed=False") \
        .option("url", url) \
        .option("user", PSQL_USERNAME) \
        .option("password", PSQL_PASSWORD) \
        .load()

    # test.write \
    #     .mode("append") \
    #     .format("jdbc") \
    #     .option("dbtable", "rent") \
    #     .option("url", url) \
    #     .option("user", PSQL_USERNAME) \
    #     .option("password", PSQL_PASSWORD) \
    #     .save()
    test.show(vertical=True)

    # jdbcDF1.show()
    # Return a new DataFrame containing rows only in both this DataFrame and another DataFrame.
    still_opens_ads = old_ads_ids.intersect(new_ads_ids)
    # still_opens_ads.show()

    # the one to be removed
    # old_ads_ids.exceptAll(new_ads_ids).show()

    # newly cresated
    # new_ads_ids.exceptAll(old_ads_ids).show()
