from my_packages.scraping_tools.county_adverts import ca_main as cam
import my_packages.fp_tools.fp_lib as fp
import pandas as pd
import json
import os


COUNTIES = ['carlow', 'cavan', 'clare', 'cork', 'donegal',
            'dublin', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 'leitrim',
            'limerick', 'longford', 'louth', 'mayo', 'meath', 'monaghan', 'offaly',
            'roscommon', 'sligo', 'tipperary', 'waterford', 'westmeath', 'wexford', 'wicklow']


def get_adverts_per_county(county):
    new_adverts_per_county = cam.CountyAdverts(investigated_county=county)
    return new_adverts_per_county.get_all_adverts_for_county


def create_json_from_adverts_county(ie_county, res):
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
