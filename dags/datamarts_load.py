from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sensors.external_task import ExternalTaskSensor
from data_models.api_pipeline_config import pipeline_config
from data_models.dag_default_args import default_args
from datasets.datasets import (activity_log_dataset, customer_dataset, order_log_dataset, customer_research_dataset)

with DAG('datamarts_load',
         default_args=default_args,
         start_date=datetime(2024, 6, 1),
         schedule_interval='@daily',
         tags=['Postgres'],
         catchup=True,
         max_active_runs=1) as dag:

    start_task = EmptyOperator(task_id='start_task')
    end_task = EmptyOperator(task_id='end_task')

    end_source_load = EmptyOperator(task_id='end_source_load')
    end_dim_load = EmptyOperator(task_id='end_dim_load')

    check_raw_order_log = ExternalTaskSensor(
        task_id='ext_check_raw_order_log',
        external_dag_id='api_data_load', # DAG, на который мы хотим посмотреть
        external_task_id='order_log',  # Task, на которую хотим смотреть в этом DAG
        timeout=60 * 60 * 10,
        poke_interval=60 * 5,
        mode='reschedule'
    )

    check_raw_activity_log = ExternalTaskSensor(
        task_id='ext_check_raw_activity_log',
        external_dag_id='api_data_load',
        external_task_id='activity_log',
        timeout=60 * 60 * 10,
        poke_interval=60 * 5,
        mode='reschedule',
    )

    check_raw_customer_research = ExternalTaskSensor(
        task_id='ext_check_raw_customer_research',
        external_dag_id='api_data_load',
        external_task_id='customer_research',
        timeout=60 * 60 * 10,
        poke_interval=60 * 5,
        mode='reschedule',
    )

    delete_from_order_log_ods = SQLExecuteQueryOperator(
        task_id='delete_from_order_log_ods',
        conn_id=pipeline_config['db_connection'],
        sql="""DELETE FROM ods.user_order_log
               WHERE date_time::date='{{ ds }}'"""
    )

    load_order_log_ods = SQLExecuteQueryOperator(
        task_id='load_order_log_ods',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_ods_user_order_log.sql'
    )

    delete_from_activity_log_ods = SQLExecuteQueryOperator(
        task_id='delete_from_activity_log_ods',
        conn_id=pipeline_config['db_connection'],
        sql="""DELETE FROM ods.user_activity_log
               WHERE date_time::date='{{ ds }}'"""
    )
    load_activity_log_ods = SQLExecuteQueryOperator(
        task_id='load_activity_log_ods',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_ods_user_activity_log.sql"
    )

    delete_from_customer_research_ods = SQLExecuteQueryOperator(
        task_id='delete_from_customer_research_ods',
        conn_id=pipeline_config['db_connection'],
        sql="""DELETE FROM ods.customer_research
                   WHERE date_time::date='{{ ds }}'"""
    )

    load_customer_research_ods = SQLExecuteQueryOperator(
        task_id='load_customer_research_ods',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_ods_customer_research.sql'
    )

    clean_d_customer_stg = SQLExecuteQueryOperator(
        task_id='clean_d_customer_stg',
        conn_id=pipeline_config['db_connection'],
        sql="TRUNCATE stg.d_customer"  # очистка stg таблицы
    )

    d_customer_stg = SQLExecuteQueryOperator(
        task_id='d_customer_stg',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_customer_stg.sql"
    )

    d_customer = SQLExecuteQueryOperator(
        task_id='load_d_customer',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_customer.sql",
        outlets= [customer_dataset]
    )

    clean_d_city_stg = SQLExecuteQueryOperator(
        task_id='clean_d_city_stg',
        conn_id=pipeline_config['db_connection'],
        sql="TRUNCATE stg.d_city"
    )

    d_city_stg = SQLExecuteQueryOperator(
        task_id='d_city_stg',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_city_stg.sql"
    )

    d_city = SQLExecuteQueryOperator(
        task_id='load_d_city',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_city.sql"
    )

    clean_d_item_stg = SQLExecuteQueryOperator(
        task_id='clean_d_item_stg',
        conn_id=pipeline_config['db_connection'],
        sql="TRUNCATE stg.d_item"
    )

    d_item_stg = SQLExecuteQueryOperator(
        task_id='d_item_stg',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_item_stg.sql"
    )

    d_item = SQLExecuteQueryOperator(
        task_id='load_d_item',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_d_item.sql"
    )
    clean_f_order = SQLExecuteQueryOperator(
        task_id='clean_f_order',
        conn_id=pipeline_config['db_connection'],
        sql="""DELETE FROM cdm.f_order
            WHERE create_date::date='{{ ds }}'"""
    )
    # на датасет order_log_dataset (с табличкой заказов) влияет этот Task
    f_order = SQLExecuteQueryOperator(
        task_id='load_f_order',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_f_order.sql',
        outlets=[order_log_dataset]
    )

    clean_f_activity = SQLExecuteQueryOperator(
        task_id='clean_f_activity',
        conn_id=pipeline_config['db_connection'],
        sql="""DELETE FROM cdm.f_activity
                WHERE create_date::date='{{ ds }}'"""
    )
    # на датасет activity_log_dataset (с табличкой активностей) влияет этот Task
    f_activity = SQLExecuteQueryOperator(
        task_id='load_f_activity',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_f_activity.sql',
        outlets=[activity_log_dataset]
    )

    clean_f_customer_research = SQLExecuteQueryOperator(
        task_id='clean_f_customer_research',
        conn_id=pipeline_config['db_connection'],
        sql="""
               DELETE FROM cdm.f_customer_research
               WHERE date_time::date='{{ ds }}'""")

    f_customer_research = SQLExecuteQueryOperator(
        task_id='f_customer_research',
        conn_id=pipeline_config['db_connection'],
        sql="sql/insert_f_customer_research.sql",
        outlets=[customer_research_dataset])

    customer_report = SQLExecuteQueryOperator(
        task_id='load_customer_report',
        conn_id=pipeline_config['db_connection'],
        sql='sql/insert_customer_report.sql'
    )

    start_task >> check_raw_order_log  >> delete_from_order_log_ods >> load_order_log_ods >> end_source_load
    start_task >> check_raw_activity_log >> delete_from_activity_log_ods >> load_activity_log_ods >> end_source_load
    start_task >> check_raw_customer_research >> delete_from_customer_research_ods >> load_customer_research_ods >> end_source_load
    end_source_load >> clean_d_customer_stg >> d_customer_stg >> d_customer >> end_dim_load
    end_source_load >> clean_d_city_stg >> d_city_stg >> d_city >> end_dim_load
    end_source_load >> clean_d_item_stg >> d_item_stg >> d_item >> end_dim_load
    end_dim_load >> clean_f_order >> f_order >> end_task
    end_dim_load >> clean_f_activity >> f_activity >> end_task
    end_dim_load >> clean_f_customer_research >> f_customer_research >> end_task