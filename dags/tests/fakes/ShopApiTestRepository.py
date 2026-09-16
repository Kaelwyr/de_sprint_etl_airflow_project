import uuid

import psycopg

from dags.repository.shop_api_postgres_repository import ShopAPIPostgresRepository


class ShopAPITestPostgresRepository(ShopAPIPostgresRepository):
    def __init__(self):
        self.conn_info = {
            'user': 'airflow',
            'password': 'airflow',
            'dbname': 'airflow',
            'host': 'localhost',
            'port': 5432,
            'autocommit': True
        }

    def create_test_db(self):
        with psycopg.connect(
                **self.conn_info
        ) as conn:
            dbid = uuid.uuid1()
            self.dbid = 'aftest_' + str(dbid).replace('-', '_')
            conn.execute ("CREATE DATABASE "+ str(self.dbid) )
            print ('dbid is', dbid)
            self.conn_info['dbname'] = self.dbid

    def print_test_db(self):
        print(self.dbid)