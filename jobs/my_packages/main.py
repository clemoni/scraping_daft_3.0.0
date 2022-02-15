"""
This the main scraper
"""
import pandas as pd
import my_packages.scraptools.scrap_main as sm
import my_packages.fptools.fptools as fp
import json
import os


COUNTIES = ['carlow', 'cavan', 'clare', 'cork', 'donegal',
            'dublin', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 'leitrim',
            'limerick', 'longford', 'louth', 'mayo', 'meath', 'monaghan', 'offaly',
            'roscommon', 'sligo', 'tipperary', 'waterford', 'westmeath', 'wexford', 'wicklow']


get_daft_page = sm.try_action(fn=sm.init_get_app(parser='lxml'))


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
    path_to_json = f"data/{ie_county}_rent.json"
    df_result = pd.DataFrame(res)
    df_result.to_json(path_to_json, orient="records")


get_rent_parse_county_json = fp.compose_recyle(
    parse_ads_county_json,
    run_get_ads_by_county
)


def get_ads_county_json(county):
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

    get_rent_parse_county_json('wicklow')
