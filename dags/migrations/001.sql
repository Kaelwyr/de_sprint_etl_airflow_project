-- Добавление данных customer_research
-- =========================================================

-- Таблица для сырых данных
CREATE TABLE raw.customer_research(
        date_id     TIMESTAMP NOT NULL,
        category_id BIGINT,
        geo_id      BIGINT,
        sales_qty   BIGINT,
        sales_amt   BIGINT
);

-- Очищенные данные
CREATE TABLE ods.customer_research(
        id           BIGINT GENERATED ALWAYS AS IDENTITY,
        date_id      TIMESTAMP NOT NULL,
        category_id  BIGINT,
        geo_id       BIGINT,
        sales_qty    BIGINT,
        sales_amt    BIGINT,
        CONSTRAINT customer_research_unique_key UNIQUE (date_id, category_id, geo_id)
);

-- Таблица фактов
CREATE TABLE cdm.f_customer_research(
        id           BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
        date_id      TIMESTAMP NOT NULL,
        category_id  BIGINT,
        city_id      BIGINT,
        sales_qty    BIGINT,
        sales_amt    BIGINT,
        CONSTRAINT f_research_pkey PRIMARY KEY (id),
        CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES cdm.d_city (id)
);

-- Витрина
CREATE TABLE rep.market_share_report (
            date_time   TIMESTAMP NOT NULL,
            city_id     BIGINT NOT NULL,
            qty_share   FLOAT ,
            amt_share   FLOAT,
            CONSTRAINT market_share_report_uniq UNIQUE(date_time, city_id)
);