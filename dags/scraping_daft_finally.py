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


get_reporting_sql = """
with t1 as (
SELECT 
COUNT(*) nbr_created,
created_at
FROM RENT 
WHERE created_at=CURRENT_DATE
GROUP BY 2
), 
t2 AS (
SELECT 
COUNT(*) nbr_closed,
closed_at
FROM RENT 
WHERE closed_at=CURRENT_DATE
AND advert_id IS NOT NULL
GROUP BY closed_at
),
t3 AS (
SELECT 
COUNT(*) nbr_fake,
created_at
FROM RENT 
WHERE created_at=CURRENT_DATE
AND advert_id IS NULL
GROUP BY created_at
)
SELECT 
t1.created_at,
t1.nbr_created, 
t2.nbr_closed,
t3.nbr_fake
FROM t1
JOIN t2 
ON t1.created_at = t2.closed_at
JOIN t3
ON t1.created_at = t3.created_at
"""


@task()
def get_reporting_all(ti=None):
    pg_hook = PostgresHook(postgres_conn_id='postgres_db')
    record = pg_hook.get_first(sql=get_reporting_sql),
    print(record)
    exec_date, nbr_created, nbr_closed, nbr_fake = record[0]

    message = f'''Scraping Daft 
    Reporting of the day ({str(exec_date)}):
    - {nbr_created} ads inserted to DB with {nbr_fake} fakes.
    - {nbr_closed} closed.'''
    ti.xcom_push(key='message', value=message)


with DAG('finally_scraping_daft',
         schedule_interval='30 11 * * *',
         catchup=False, tags=['scraping daft', 'finally'],
         default_args=DEFAULT_ARGS) as dag:

    clear_fake_ads = SparkSubmitOperator(
        task_id="clear_fake_ads",
        conn_id="spark_default",
        application="/opt/airflow/jobs/clear_fake_ads.py",
        name="clear data",
        conf={"spark.master": spark_master},
        verbose=True
    )

    get_report_all_task = get_reporting_all()

    notify_slack_report = SlackWebhookOperator(
        task_id="notify_slack_report",
        http_conn_id="slack_connect",
        message="{{ti.xcom_pull(task_ids='get_reporting_all', key='message')}}",
        channel="#scraping-daft-website"
    )

    clear_fake_ads >> get_report_all_task >> notify_slack_report
