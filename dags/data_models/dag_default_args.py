from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'concurrency': 1,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
    'pool': 'postgres_pool'}