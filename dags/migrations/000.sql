-- Создание схемы
CREATE SCHEMA IF NOT EXISTS raw;

CREATE SCHEMA IF NOT EXISTS stg;

CREATE SCHEMA IF NOT EXISTS ods;

CREATE SCHEMA IF NOT EXISTS cdm;

CREATE SCHEMA IF NOT EXISTS rep;

-- Создание таблиц
CREATE TABLE IF NOT EXISTS raw.user_order_log (
    id bigint,
    uniq_id varchar(32),
    date_time timestamp,
    city_id bigint,
    city_name varchar(100),
    customer_id bigint,
    first_name varchar(100),
    last_name varchar(100),
    item_id bigint,
    item_name varchar(255),
    quantity bigint,
    payment_amount numeric(14, 2) ,
    CONSTRAINT user_order_log_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS raw.user_activity_log (
    id bigint,
    uniq_id varchar(32),
    date_time timestamp,
    action_id bigint,
    customer_id bigint,
    quantity bigint,
    CONSTRAINT user_activity_log_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ods.user_order_log (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    uniq_id varchar(32),
    date_time timestamp,
    city_id bigint ,
    city_name varchar(100),
    customer_id bigint,
    first_name varchar(100),
    last_name varchar(100),
    item_id bigint,
    item_name varchar(255),
    quantity bigint,
    payment_amount numeric(14, 2) ,
    CONSTRAINT user_order_log_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ods.user_activity_log (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    uniq_id varchar(32),
    date_time timestamp,
    action_id bigint,
    customer_id bigint,
    quantity bigint,
    CONSTRAINT user_activity_log_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS stg.d_city (
    id bigint,
    city_id bigint NOT NULL,
    city_name varchar(100)
);

CREATE TABLE IF NOT EXISTS stg.d_customer (
    id bigint ,
    customer_id bigint NOT NULL,
    first_name varchar(100),
    last_name varchar(100)
);

CREATE TABLE IF NOT EXISTS stg.d_item (
    id bigint ,
    item_id bigint NOT NULL,
    item_name varchar(255)
);

CREATE TABLE IF NOT EXISTS cdm.d_city (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    city_id bigint NOT NULL,
    city_name varchar(100),
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_city_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cdm.d_customer (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    customer_id bigint NOT NULL,
    first_name varchar(100),
    last_name varchar(100),
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_customer_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cdm.d_item (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    item_id bigint NOT NULL,
    item_name varchar(255),
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_item_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS cdm.f_activity
(
    id             bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    activity_id    varchar(32) NOT null unique,
    create_date    date,
    customer_id    bigint,
    action_id      bigint,
    quantity       bigint,
    CONSTRAINT f_activity_pkey PRIMARY KEY (id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES cdm.d_customer (id)
);


CREATE TABLE IF NOT EXISTS cdm.f_order
(
    id             bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    order_id       varchar(32) NOT null unique,
    create_date    date,
    customer_id    bigint,
    city_id        bigint,
    item_id        bigint,
    quantity       bigint,
    payment_amount numeric(14, 2),
    CONSTRAINT f_order_pkey PRIMARY KEY (id),
    CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES cdm.d_city (id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES cdm.d_customer (id),
    CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES cdm.d_item (id)
);

CREATE TABLE IF NOT EXISTS rep.customer_report (
    customer_id             BIGINT NOT NULL,
    first_name              VARCHAR(100),
    last_name               VARCHAR(100),
    uniq_actions            BIGINT,
    different_actions       BIGINT,
    days_with_actions       INTEGER,
    total_actions           BIGINT,
    uniq_orders             BIGINT,
    days_with_orders        INTEGER,
    cities_visited          BIGINT,
    different_items_bought  BIGINT,
    money_spent             BIGINT
);
CREATE INDEX IF NOT EXISTS main_customer ON rep.customer_report USING btree (customer_id);