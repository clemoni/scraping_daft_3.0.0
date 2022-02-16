from pyspark.sql import SparkSession
import sys
import my_packages.dbtools.db_main as db
import random
from my_packages.main import COUNTIES, \
    get_adverts_county_from_json, \
    get_still_open_ads, \
    get_to_close_ads, \
    get_to_insert_ads, \
    remove_json_file \


PSQL_HOST = "postgres"
PSQL_PORT = "5432"
PSQL_DB = "scraping_daft"
PSQL_USERNAME = "airflow"
PSQL_PASSWORD = "airflow"


select_advert_id_by_county_and_closed_state = """SELECT advert_id
FROM rent
WHERE is_closed = :is_closed_state
AND county=(SELECT id from county WHERE name = :county)"""

update_ads_is_closed = """UPDATE rent
SET is_closed='true', closed_at=Now()
WHERE advert_id=:advert_id"""

insert_new_ads = """INSERT INTO
RENT (advert_id, rent_amount, rent_frequency,
address, rent_type, facilities, ber, ber_n, author,
description, url, created_at, closed_at, is_closed,
county, single_bedroom, double_bedroom, bathroom,
furnished, lease, address_geo)
VALUES (:advert_id,:rent_amount,:rent_frequency,
:address,:rent_type,:facilities,:ber,:ber_n,:author,
:description,:url,Now(),:closed_at,:is_closed,
(SELECT id FROM county WHERE name=:county),
:single_bedroom,:double_bedroom,:bathroom,
:furnished,:lease,point(:latitude,:longitude))"""


def change_id(ad):
    return {k: (random.randrange(3000) if k == 'advert_id' else v) for k, v in ad.items()}


if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Persist DB") \
        .config("spark.driver.bindAddress", "localhost") \
        .getOrCreate()

    county = sys.argv[1]

    path = 'postgresql+psycopg2://airflow:airflow@postgres/scraping_daft'
    db_select = db.init_select(path)

    # get newly scraped ads from county
    new_ads = get_adverts_county_from_json(county)
    # new_ads = get_adverts_county_from_json('dublin')

    # filter to get list of advert_ids from newly scraped ads
    new_ads_ids = set([ad['advert_id']for ad in new_ads])

    # ###### for testing puroses #########
    #  TO BE IGNORED
    # to_add_ads = [change_id(ad) for i, ad in enumerate(new_ads) if i <= 5]
    # new_fake_ads = [*to_add_ads, *new_ads]
    # new_ads_ids = set([ad['advert_id'] for ad in new_fake_ads])
    # db.init_insert(path)(insert_new_ads)(new_ads)
    # # print(len(new_ads_ids))
    # to_delete = [ad_id for i, ad_id in enumerate(new_ads_ids) if i > 41]
    # for i in to_delete:
    #     new_ads_ids.remove(i)

    # Select ads from db where status still open and county
    opened_ads = set([ads[0] for ads in db_select(select_advert_id_by_county_and_closed_state)(
        is_closed_state=False, county=county.capitalize())])

    # verification get ads still running
    # still_open_ads_ids = get_still_open_ads(opened_ads, new_ads_ids)

    # get the ads that were open in db but not part of the newly scraped ads
    # they need to be closed (update)
    to_close_ads_ids = get_to_close_ads(opened_ads, new_ads_ids)
    db.init_insert(path)(update_ads_is_closed)(
        [{'advert_id': ad_id}for ad_id in to_close_ads_ids])

    # get the ads that are not in the db,
    # therefore need to be iserted
    to_insert_ads_ids = get_to_insert_ads(opened_ads, new_ads_ids)
    to_insert_ads = [
        ad for ad in new_ads if ad['advert_id'] in to_insert_ads_ids]
    db.init_insert(path)(insert_new_ads)(to_insert_ads)
