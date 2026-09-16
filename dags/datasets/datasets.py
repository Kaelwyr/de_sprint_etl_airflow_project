from airflow.datasets import Dataset

order_log_dataset = Dataset(
                "postgres://playground_etl_20260813_1a53b7145b.cdm.f_order")

activity_log_dataset = Dataset(
                "postgres://playground_etl_20260813_1a53b7145b.cdm.f_activity")

customer_dataset = Dataset(
                "postgres://playground_etl_20260813_1a53b7145b.cdm.customer_report")

customer_research_dataset = Dataset(
                "postgres://playground_etl_20260813_1a53b7145b.cdm.f_customer_research")