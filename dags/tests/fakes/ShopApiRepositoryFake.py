from dags.data_models.user_activity_log_model import  UserActivityModel
from dags.data_models.user_order_log_model import UserOrderModel
from dags.data_models.customer_research_model import CustomerResearchModel
from dags.repository.shop_api_psycopg_repository import ShopAPIRepository


class ShopAPIRepositoryFake(ShopAPIRepository):
    def __init__(self):
        self.order_logs = []
        self.activity_logs = []
        self.customer_research = []

    def save_order_logs(self, order_logs: list[UserOrderModel]):
        self.order_logs.extend(order_logs)

    def save_activity_logs(self, activity_logs: list[UserActivityModel]):
        self.activity_logs.extend(activity_logs)

    def save_customer_research(self, research: list[CustomerResearchModel]):
        self.customer_research.extend(research)