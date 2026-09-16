from datetime import datetime

from dags.tests.fakes.ShopApiRepositoryFake import ShopAPIRepositoryFake
from dags.utils.api_config import get_insert_customer_research


class TestCustomerResearch:
    def test_insert_order_log(self, mocker):
        mock_get_customer_research = mocker.patch('dags.utils.api_config.get_customer_research')
        mock_get_customer_research.return_value = """
                        [
                        {
                        "date_time":"2024-09-19T00:00:00",
                        "category_id":1001,
                        "geo_id":1,
                        "sales_qty":8,
                        "sales_amt":1944
                        },
                        {
                        "date_time":"2024-07-20T00:00:00",
                        "category_id":10,
                        "geo_id":2,
                        "sales_qty":6,
                        "sales_amt":1458
                        }
                        ]"""
        repo = ShopAPIRepositoryFake()
        get_insert_customer_research(repo)

        assert len(repo.customer_research) == 2

        first_research = repo.customer_research[0]
        assert first_research.date_time == datetime(year=2024, month=9, day=19)
        assert first_research.category_id == 1001
        assert first_research.geo_id == 1

        second_research = repo.customer_research[1]
        assert second_research.sales_qty == 6
        assert second_research.sales_amt == 1458