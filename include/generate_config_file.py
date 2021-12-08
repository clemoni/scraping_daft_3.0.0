import json


config_filepath = 'include/dag_config'


def init_cron_interval():
    minutes = 0
    hours = 0

    def get_cron():
        return f"{minutes} {hours} * * *"

    def increment():
        nonlocal minutes, hours
        if minutes == 45:
            minutes = 0
            hours += 1
        else:
            minutes += 15

    return get_cron, increment


def init_config(county, cron_job):
    return {"DagId": f"scraping_daft_{county}",
            "Schedule": cron_job,
            "County": county,
            "SparkMaster": "spark://spark:7077"}


COUNTIES = ['carlow', 'cavan', 'clare', 'cork', 'donegal',
            'dublin', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 'leitrim',
            'limerick', 'longford', 'louth', 'mayo', 'meath', 'monaghan', 'offaly',
            'roscommon', 'sligo', 'tipperary', 'waterford', 'westmeath', 'wexford', 'wicklow']

get_cron, increment = init_cron_interval()

for county in COUNTIES:
    increment()
    json_config = init_config(county, get_cron())
    filename = f'{config_filepath}/dag_{county}_config.json'

    with open(filename, 'w') as f:
        json.dump(json_config, f)
