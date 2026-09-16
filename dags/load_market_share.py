from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datasets.datasets import order_log_dataset, customer_research_dataset

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

with DAG('load_market_share_report_dag',
         default_args=default_args,
         start_date=datetime(2024, 6, 1),
         schedule_interval=[order_log_dataset, customer_research_dataset],
         catchup=True,
         max_active_runs=1) as dag:
    start_task = EmptyOperator(task_id='start_task')
    end_task = EmptyOperator(task_id='end_task')

    market_share_report = SQLExecuteQueryOperator(
        task_id='load_market_share_report',
        conn_id='conn_pg',
        sql="sql/insert_market_share.sql",
    )

    start_task >> market_share_report >> end_task