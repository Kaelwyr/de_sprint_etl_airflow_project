from pathlib import Path
from typing import Optional

import psycopg
from airflow.hooks.base import BaseHook
from data_models.api_pipeline_config import pipeline_config
from data_models.user_activity_log_model import UserActivityModel
from data_models.user_order_log_model import UserOrderModel
from data_models.customer_research_model import CustomerResearchModel
from repository.shop_api_psycopg_repository import ShopAPIRepository

BASE_DIR = Path(__file__).resolve().parent

def get_sql_query_from_file(sql_file):
    path = Path(sql_file)
    if not path.is_absolute():
        path = BASE_DIR / path
    with path.open('r',encoding='utf-8') as f:
        query = f.read()
    return query


class ShopAPIPostgresRepository(ShopAPIRepository):
    def __init__(self, af_conn: Optional[str] = pipeline_config['db_connection']):
        self.postgres_hook = BaseHook.get_connection(af_conn)
        self.conn_info = {
            'user': self.postgres_hook.login,
            'password': self.postgres_hook.password,
            'dbname': self.postgres_hook.schema,
            'host': self.postgres_hook.host,
            'port': self.postgres_hook.port,
        }

    def save_order_logs(self, order_logs: list[UserOrderModel]):
        query = get_sql_query_from_file('sql/insert_raw_user_order_log.sql')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for model in order_logs:
                    cur.execute(query, model.model_dump())

    def save_activity_logs(self, activity_logs: list[UserActivityModel]):
        query = get_sql_query_from_file(sql_file='sql/insert_raw_user_activity_log.sql')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for model in activity_logs:
                    cur.execute(query, model.model_dump())

    def save_customer_research(self, research: list[CustomerResearchModel]):
        query = get_sql_query_from_file('sql/insert_raw_customer_research.sql')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for model in research:
                    cur.execute(query, model.model_dump())

    def execute_postgres_query(self, **kwargs):
        query = kwargs['query']
        params = kwargs['params']
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)

    def execute_postgres_query_with_result(self, **kwargs):
        query = kwargs['query']
        params = kwargs.get('params')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                data = cur.fetchall()
        return data

    def execute_postgres_query_batch(self, **kwargs):
        queries_list = kwargs['queries_list']
        params_list = kwargs.get('params_list')
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            with conn.cursor() as cur:
                for query, params in zip(queries_list, params_list):
                    cur.execute(query, params)

    def get_db_version(self):
        data = self.execute_postgres_query_with_result(query='SELECT max(version) FROM meta.table_info')
        print(data[0][0])
        return data[0][0]