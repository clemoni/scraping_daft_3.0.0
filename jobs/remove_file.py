from pyspark.sql import SparkSession
import sys
from my_packages.main import remove_json_file


# spark-submit --master spark://517f01f8fc92:7077 ~/opt/airflow/jobs/get_ads_per_county.py louth


if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Remove file") \
        .getOrCreate()

    county = sys.argv[1]
    remove_json_file(county)
