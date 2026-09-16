import logging

import pytest
from db_migrator import get_sql_query_from_file, run_migration
from jinja2 import Template
from dags.tests.fakes.ShopApiTestRepository import ShopAPITestPostgresRepository


def prepare_data(repo, scripts=[]):
    for script in scripts:
        script = 'tests/test_data/' + script
        query = get_sql_query_from_file(script)
        repo.execute_postgres_query(query=query, params=[])


@pytest.fixture(scope='class')
def test_repo():
    repo = ShopAPITestPostgresRepository()
    repo.create_test_db()
    run_migration(repo=repo)
    yield repo
    repo.conn_info['dbname'] = 'airflow'
    repo.execute_postgres_query(query=f'DROP DATABASE {repo.dbid};', params=[])


@pytest.fixture(scope='class')
def test_date():
    test_date = '2024-09-01'
    return test_date


@pytest.fixture(scope='class')
def prepare_data_for_d_customer(test_repo, test_date):
    prepare_data(test_repo, scripts=['d_customer_1.sql', 'order_log.sql', 'activity_log.sql'])
    query = get_sql_query_from_file('sql/insert_ods_user_order_log.sql')
    test_repo.execute_postgres_query(query=query, params=[])

    query = get_sql_query_from_file('sql/insert_ods_user_activity_log.sql')
    test_repo.execute_postgres_query(query=query, params=[])

    query_templ = get_sql_query_from_file('sql/insert_d_customer_stg.sql')
    query = Template(query_templ).render(ds=test_date)
    test_repo.execute_postgres_query(query=query, params=[])

    query_templ = get_sql_query_from_file('sql/insert_d_customer.sql')
    query = Template(query_templ).render(ds=test_date)
    test_repo.execute_postgres_query(query=query, params=[])


@pytest.fixture(scope='class')
def prepare_market_share(test_repo,test_date):
    prepare_data(test_repo, scripts=['d_customer_3.sql', 'd_item.sql', 'd_city.sql',
                                     'f_customer_research.sql', 'f_order.sql', 'market_share_report.sql'])
    query_templ = get_sql_query_from_file('sql/insert_market_share.sql')
    query = Template(query_templ).render(ds=test_date)
    test_repo.execute_postgres_query(query=query, params=[])


@pytest.mark.usefixtures('prepare_data_for_d_customer')
class TestPostgresScript:

    def test_dedup_orders(self, test_repo):
        test_query_1 = """
        SELECT count(1) FROM ods.user_order_log
        WHERE uniq_id = '4ed55d5f4d8d0a65fcbb5a6209b0f3c5'
        """
        res = test_repo.execute_postgres_query_with_result(query=test_query_1)

        assert res[0][0] == 1

    def test_dedup_activity(self, test_repo):
        test_query_2 = """
        SELECT count(1) FROM ods.user_activity_log
        WHERE uniq_id = '3fad646208167a268255b5b16e30b9ba'
        """
        res = test_repo.execute_postgres_query_with_result(query=test_query_2)

        assert res[0][0] == 1

    def test_customer_stg(self, test_repo):
        test_query_3 = """
               SELECT count(1) FROM stg.d_customer
               WHERE customer_id = 7300
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_3)

        assert res[0][0] == 0

        test_query_4 = """
               SELECT count(1) FROM stg.d_customer
               WHERE customer_id = 4203
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_4)

        assert res[0][0] == 1

    def test_customer(self, test_repo, test_date):
        test_query_5 = """
               SELECT count(1) FROM cdm.d_customer
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_5)

        assert res[0][0] == 4

        test_query_5 = """
               SELECT start_date::text, end_date::text FROM cdm.d_customer
               WHERE customer_id = 7300
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_5)

        assert res[0][0] == '2024-07-01'
        assert res[0][1] == '9999-12-31'

        test_query_6 = """
               SELECT start_date::text, end_date::text FROM cdm.d_customer
               WHERE customer_id = 4203
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_6)

        assert res[0][0] == test_date
        assert res[0][1] == '9999-12-31'

        test_query_7 = """
               SELECT start_date::text, end_date::text, first_name, last_name FROM cdm.d_customer
               WHERE customer_id = 591
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_7)

        assert res[0][0] == test_date
        assert res[0][1] == '9999-12-31'
        assert res[0][2] == 'неизвестно'
        assert res[0][3] == 'неизвестно'


@pytest.fixture(scope='class')
def prepare_data_for_d_customer_second(test_repo, test_date):
    prepare_data(test_repo, scripts=['d_customer_2.sql', 'order_log.sql', 'activity_log.sql'])
    query = get_sql_query_from_file('sql/insert_ods_user_order_log.sql')
    test_repo.execute_postgres_query(query=query, params=[])

    query = get_sql_query_from_file('sql/insert_ods_user_activity_log.sql')
    test_repo.execute_postgres_query(query=query, params=[])

    query_templ = get_sql_query_from_file('sql/insert_d_customer_stg.sql')
    query = Template(query_templ).render(ds=test_date)
    test_repo.execute_postgres_query(query=query, params=[])

    query_templ = get_sql_query_from_file('sql/insert_d_customer.sql')
    query = Template(query_templ).render(ds=test_date)
    test_repo.execute_postgres_query(query=query, params=[])


@pytest.mark.usefixtures('prepare_data_for_d_customer_second')
class TestPostgresDimCustomer:

    def test_customer_stg(self, test_repo, test_date):
        test_query_1 = """
               SELECT count(1) FROM stg.d_customer
               WHERE customer_id = 7300
               """
        res = test_repo.execute_postgres_query_with_result(**{'query': test_query_1})

        assert res[0][0] == 1

    def test_customer(self, test_repo, test_date):
        test_query_3 = """
               SELECT count(1) FROM cdm.d_customer
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_3)

        assert res[0][0] == 5

        test_query_4 = """
               SELECT start_date::text, end_date::text FROM cdm.d_customer
               WHERE customer_id = 7300
               ORDER by start_date
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_4)

        assert res[0][0] == '2024-07-01'
        assert res[0][1] == '2024-08-31'
        assert res[1][0] == test_date
        assert res[1][1] == '9999-12-31'


@pytest.mark.usefixtures('prepare_market_share')
class TestPostgresScriptMarketShareReport:

    def test_market_share_report_count(self, test_repo):
        test_query_1 = """
               SELECT count(1)
               FROM rep.market_share_report
               """
        res = test_repo.execute_postgres_query_with_result(**{'query': test_query_1})

        assert res[0][0] == 1

    def test_market_share_report(self, test_repo):
        test_query_1 = """
               SELECT date_id::date::text, city_id, qty_share, amt_share
               FROM rep.market_share_report
               """
        res = test_repo.execute_postgres_query_with_result(query=test_query_1)

        assert res[0][0] == '2024-09-01'
        assert res[0][1] == 1
        assert res[0][2] == 0.45
        assert res[0][3] == 0.375