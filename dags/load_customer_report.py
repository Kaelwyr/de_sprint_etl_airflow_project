from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from data_models.api_pipeline_config import pipeline_config
from data_models.dag_default_args import default_args
from datasets.datasets import (activity_log_dataset, customer_dataset, order_log_dataset)


with DAG('load_customer_report_dag',
        default_args=default_args,
        start_date=datetime(2024, 6, 1),
        schedule=[order_log_dataset, activity_log_dataset, customer_dataset],
        tags=['Postgres'],
        catchup=False,
        max_active_runs=1) as dag:
    start_task = EmptyOperator(task_id='start_task')
    end_task = EmptyOperator(task_id='end_task')

    customer_report = SQLExecuteQueryOperator(
        task_id='load_customer_report',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_customer_report.sql',
        outlets=[customer_dataset]
    )

    start_task >> customer_report >> end_task