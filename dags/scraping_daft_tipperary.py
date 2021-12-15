from datetime import datetime, timedelta
from airflow.sensors.filesystem import FileSensor
from airflow.decorators import task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow import DAG

DEFAULT_ARGS = {
    "owner": "clemoni",
    "depends_on_past": False,
    "email": ["clement.liscoet@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    'start_date': datetime(2021, 1, 1),
}

spark_master = 'spark://spark:7077'


@task()
def run_init_county(county, ti=None):
    ti.xcom_push(key='county', value=county)


get_reporting_sql = "SELECT * FROM reporting_by_day_county(%(name)s)"


@task()
def get_reporting(ti=None):
    county_name = ti.xcom_pull(task_ids='run_init_county', key='county')
    print(county_name)
    pg_hook = PostgresHook(postgres_conn_id='postgres_db')
    record = pg_hook.get_first(
        sql=get_reporting_sql, parameters={"name": county_name.capitalize()}),

    county, created, closed = record[0]
    message = f'''
    Scraping-Daft Reporting:\n{county}: {created} new advertisement(s) inserted and {closed} closed
    '''
    ti.xcom_push(key='message', value=message)


with DAG('scraping_daft_tipperary',
         schedule_interval='50 10 * * *',
         catchup=False, tags=['scraping daft'],
         default_args=DEFAULT_ARGS) as dag:

    init_county = run_init_county('tipperary')

    scrap_data = SparkSubmitOperator(
        task_id="scrap_data",
        conn_id="spark_default",
        application="/opt/airflow/jobs/get_ads_per_county.py",
        application_args=[
            "{{ti.xcom_pull(task_ids='run_init_county', key='county')}}"],
        name="scrap data",
        conf={"spark.master": spark_master},
        verbose=True
    )

    waiting_for_file = FileSensor(
        task_id="waiting_for_file",
        filepath="{{ ti.xcom_pull(task_ids='run_init_county', key='county')}}_rent.json",
        fs_conn_id="file_path",
        poke_interval=180,
        timeout=180*3,
        mode="reschedule"
    )

    persist_data = SparkSubmitOperator(
        task_id="persist_data",
        conn_id="spark_default",
        application="/opt/airflow/jobs/persist_db.py",
        application_args=[
            "{{ti.xcom_pull(task_ids='run_init_county', key='county')}}"],
        name="persist data",
        conf={"spark.master": spark_master},
        verbose=True
    )

    get_report_task = get_reporting()

    notify_slack = SlackWebhookOperator(
        task_id="notify_slack",
        http_conn_id="slack_connect",
        message="{{ti.xcom_pull(task_ids='get_reporting', key='message')}}",
        channel="#scraping-daft-website"
    )

    remove_file = SparkSubmitOperator(
        task_id="remove_file",
        conn_id="spark_default",
        application="/opt/airflow/jobs/remove_file.py",
        application_args=[
            "{{ti.xcom_pull(task_ids='run_init_county', key='county')}}"],
        name="remove file",
        conf={"spark.master": spark_master},
        verbose=True
    )

    init_county >> scrap_data >> waiting_for_file >> persist_data >> get_report_task >> notify_slack >> remove_file
