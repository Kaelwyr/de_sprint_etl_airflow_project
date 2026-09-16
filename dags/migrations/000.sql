CREATE SCHEMA raw;

CREATE SCHEMA stg;

CREATE SCHEMA ods;

CREATE SCHEMA cdm;

CREATE SCHEMA rep;

CREATE TABLE raw.user_order_log (
    id bigint,
    uniq_id varchar ,
    date_time timestamp ,
    city_id bigint ,
    city_name varchar ,
    customer_id bigint ,
    first_name varchar ,
    last_name varchar,
    item_id bigint ,
    item_name varchar,
    quantity bigint ,
    payment_amount numeric(14, 2) ,
    CONSTRAINT user_order_log_pkey PRIMARY KEY (id)
);

CREATE TABLE raw.user_activity_log (
    id bigint,
    uniq_id varchar ,
    date_time timestamp ,
    action_id bigint,
    customer_id bigint ,
    quantity bigint ,
    CONSTRAINT user_activity_log_pkey PRIMARY KEY (id)
);

CREATE TABLE ods.user_order_log (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    uniq_id varchar ,
    date_time timestamp ,
    city_id bigint ,
    city_name varchar ,
    customer_id bigint ,
    first_name varchar ,
    last_name varchar,
    item_id bigint ,
    item_name varchar,
    quantity bigint ,
    payment_amount numeric(14, 2) ,
    CONSTRAINT user_order_log_pkey PRIMARY KEY (id)
);

CREATE TABLE ods.user_activity_log (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    uniq_id varchar ,
    date_time timestamp ,
    action_id bigint,
    customer_id bigint ,
    quantity bigint ,
    CONSTRAINT user_activity_log_pkey PRIMARY KEY (id)
);

CREATE TABLE stg.d_city (
    id bigint ,
    city_id bigint NOT NULL,
    city_name varchar
);

CREATE TABLE stg.d_customer (
    id bigint ,
    customer_id bigint NOT NULL,
    first_name varchar ,
    last_name varchar
);

CREATE TABLE stg.d_item (
    id bigint ,
    item_id bigint NOT NULL,
    item_name varchar
);

CREATE TABLE cdm.d_city (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    city_id bigint NOT NULL,
    city_name varchar ,
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_city_pkey PRIMARY KEY (id)
);

CREATE TABLE cdm.d_customer (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    customer_id bigint NOT NULL,
    first_name varchar ,
    last_name varchar ,
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_customer_pkey PRIMARY KEY (id)
);

CREATE TABLE cdm.d_item (
    id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    item_id bigint NOT NULL,
    item_name varchar ,
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT d_item_pkey PRIMARY KEY (id)
);

CREATE TABLE cdm.f_activity
(
    id             bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    activity_id    varchar NOT null unique,
    create_date    date,
    customer_id    bigint,
    action_id      bigint,
    quantity       bigint,
    CONSTRAINT f_activity_pkey PRIMARY KEY (id),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES cdm.d_customer (id)
);


CREATE TABLE cdm.f_order
(
    id             bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
    order_id       varchar NOT null unique,
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

CREATE TABLE rep.customer_report (
    customer_id             BIGINT NOT NULL,
    first_name              VARCHAR,
    last_name               VARCHAR,
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
CREATE INDEX main_customer ON rep.customer_report USING btree (customer_id);