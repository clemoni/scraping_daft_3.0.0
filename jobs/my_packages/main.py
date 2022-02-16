# modules

import my_packages.fp_tools.fp_lib as fp
import my_packages.scraping_tools.county_adverts.ca_main as cam
import pandas as pd
import json
import os


COUNTIES = ['carlow', 'cavan', 'clare', 'cork', 'donegal',
            'dublin', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 'leitrim',
            'limerick', 'longford', 'louth', 'mayo', 'meath', 'monaghan', 'offaly',
            'roscommon', 'sligo', 'tipperary', 'waterford', 'westmeath', 'wexford', 'wicklow']


<<<<<<< HEAD
get_daft_page = sm.try_action(fn=sm.init_get_app(parser='lxml'))
||||||| 0454624
get_daft = sm.try_action(sm.init_get_app('lxml'))
=======
def get_adverts_per_county(county):
    new_adverts_per_county = cam.CountyAdverts(investigated_county=county)
    return new_adverts_per_county.get_all_adverts_for_county
>>>>>>> refactoring


<<<<<<< HEAD
def run_get_ads_by_county(county):
    url = sm.init_url(county)

    daft = get_daft_page(url['base'],
                         url['general_search'],
                         url['county'],
                         url['pages'])

    limit = sm.get_calculated_limit(daft)

    flatten_data_ads_county = sm.init_get_adds_by_page(
        get_daft_page)(limit, county=county)

    return sm.flatten_data_ads(flatten_data_ads_county)


def parse_ads_county_json(ie_county, res):
||||||| 0454624
def run_get_ads_by_county(county):
    url = sm.init_url(county)

    daft = get_daft(url['base'],
                    url['general_search'],
                    url['county'],
                    url['pages'])

    limit = sm.get_calculated_limit(daft)

    flatten_data_ads_county = sm.init_get_adds_by_page(
        get_daft)(limit, county=county)

    return sm.flatten_data_ads(flatten_data_ads_county)


def parse_ads_county_json(ie_county, res):
=======
def create_json_from_adverts_county(ie_county, res):
>>>>>>> refactoring
    path_to_json = f"data/{ie_county}_rent.json"
    df_result = pd.DataFrame(res)
    df_result.to_json(path_to_json, orient="records")


create_adverts_json_from_county = fp.compose_recyle(
    create_json_from_adverts_county,
    get_adverts_per_county
)


def get_adverts_county_from_json(county):
    path = f"/opt/airflow/data/{county}_rent.json"
    try:
        with open(path) as file:
            return json.load(file)
    except Exception as e:
        return f"There was an error: {e}"


def get_still_open_ads(saved_ads, new_collect_ads):
    return saved_ads.intersection(new_collect_ads)


def get_to_close_ads(saved_ads, new_collect_ads):
    return saved_ads.difference(new_collect_ads)


def get_to_insert_ads(saved_ads, new_collect_ads):
    return new_collect_ads.difference(saved_ads)


def remove_json_file(county):
    os.remove(f"/opt/airflow/data/{county}_rent.json")
    print(f"file: {county}_rent.json deleted")


if __name__ == "__main__":

    get_adverts_per_county('wicklow')
