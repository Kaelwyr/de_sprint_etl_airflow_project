# Проект: добавление нового источника в DWH

## Описание проекта

Проект посвящен интеграции нового источника данных в существующую систему хранения данных (DWH). В рамках этого проекта добавляются данные о продажах на конкурирующем сайте (`customer_research`) в систему.

## Структура и директории

### Структура директорий

```
de_sprint_etl_airflow_project/
├── .venv/                       # виртуальное окружение (Python 3.11)
│   ├── Lib/site-packages/       # зависимости (airflow, sqlalchemy, pydantic, psycopg, pytest и др.)
│   └── Scripts/                 # исполняемые файлы (airflow.exe, pytest.exe, python.exe, ...)
│
├── config/                      # конфигурация
│
├── dags/                        # DAG'и Airflow и вспомогательный код
│   ├── .airflowignore
│   ├── api_data_load.py         # DAG загрузки данных из API
│   ├── datamarts_load.py        # DAG загрузки витрин
│   ├── db_migrator.py           # DAG миграций БД
│   ├── load_customer_report.py  # DAG отчёта по клиентам
│   ├── load_market_share.py     # DAG market share
│   ├── __init__.py
│   │
│   ├── datasets/                # описание датасетов
│   │   └── datasets.py
│   │
│   ├── data_models/             # модели данных (pydantic)
│   │   ├── api_pipeline_config.py
│   │   ├── customer_research_model.py
│   │   ├── dag_default_args.py
│   │   ├── user_activity_log_model.py
│   │   ├── user_order_log_model.py
│   │   └── __init__.py
│   │
│   ├── migrations/              # SQL-миграции
│   │   ├── 000.sql
│   │   └── 001.sql
│   │
│   ├── repository/              # доступ к БД
│   │   ├── shop_api_postgres_repository.py
│   │   ├── shop_api_psycopg_repository.py
│   │   └── sql/                 # SQL-запросы вставки raw-данных
│   │       ├── insert_raw_customer_research.sql
│   │       ├── insert_raw_user_activity_log.sql
│   │       └── insert_raw_user_order_log.sql
│   │
│   ├── sql/                     # SQL-запросы витрин (ODS / DDS / DM)
│   │   ├── insert_d_city.sql, insert_d_customer.sql, insert_d_item.sql
│   │   ├── insert_f_activity.sql, insert_f_order.sql, insert_f_customer_research.sql
│   │   ├── insert_ods_*.sql
│   │   ├── insert_customer_report.sql
│   │   └── insert_market_share.sql
│   │
│   ├── tests/                   # тесты
│   │   ├── test_customer_research.py
│   │   ├── test_postgres_scripts.py
│   │   ├── fakes/               # фейковые репозитории
│   │   ├── test_data/           # эталонные SQL-данные
│   │   └── .pytest_cache/
│   │
│   └── utils/                   # утилиты
│       └── api_config.py
│
├── logs/                        # логи Airflow
│   └── scheduler/latest/
│
├── plugins/                     # плагины Airflow
│
└── scripts/                     # вспомогательные скрипты
```

#### Кратко о ключевых блоках
| Блок           | Назначение                                                                 |
|----------------|----------------------------------------------------------------------------|
| `dags/*.py`    | Пять DAG'ов: загрузка API, витрины, миграции, отчёт клиентов, market share |
| `data_models/` | Pydantic/ORM-модели конфигов и таблиц                                      |
| `repository/`  | Слой доступа к Postgres (psycopg) + SQL для raw-слоя                       |
| `sql/`         | SQL для ODS → DDS → DM (city, customer, item, activity, order, research)   |
| `migrations/`  | DDL-миграции                                                               |
| `tests/`       | pytest-тесты + фейки + тестовые данные                                     |


### Установка и запуск

#### 1. Клонирование репозитория

```bash
git clone https://github.com/Kaelwyr/de_sprint_etl_airflow_project.git
cd de_sprint_etl_airflow_project
```

#### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 3. Настройка Docker Compose

Перед запуском Docker Compose, убедитесь, что у вас установлены Docker и Docker Compose.

```bash
docker-compose up --build -d
```

#### 4. Создание Airflow UI

После запуска Docker Compose, откройте браузер и перейдите по адресу:

```
http://localhost:7001
```

#### 5. Добавление соединений в Airflow

1. Перейдите в Airflow UI. Данные для входа (login | pass): Airflow | Airflow
2. Перейдите в "Admin" -> "Connections".
3. Добавьте следующие соединения:
   - `conn_pg` для подключения к базе данных PostgreSQL.
   - `api__conn` для подключения к API.

#### 6. Создание пулов

1. Перейдите в Airflow UI.
2. Перейдите в "Admin" -> "Pools".
3. Создайте два пула:
   - `API_pool` для задач, связанных с API.
   - `postgres_pool` для задач, связанных с PostgreSQL.

#### 7. Миграция базы данных

1. Перейдите в Airflow UI.
2. Перейдите в "Admin" -> "Connections".
3. Выберите соединение `conn_pg`.
4. Перейдите в "Admin" -> "DAGs".
5. Запустите DAG `db_migration`.
