from pyspark.sql import SparkSession
import sys
from my_packages.main import create_adverts_json_from_county


# spark-submit --master spark://517f01f8fc92:7077 ~/opt/airflow/jobs/get_ads_per_county.py louth


if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Get Ads per county") \
        .getOrCreate()

    county = sys.argv[1]
    create_adverts_json_from_county(county)
