BEGIN;

TRUNCATE TABLE rep.customer_report;

-- Агрегация по активностям
CREATE TEMP TABLE tmp_agg_actions ON COMMIT DROP AS
SELECT
    customer_id,
    COUNT(DISTINCT activity_id) AS uniq_actions,
    COUNT(DISTINCT action_id) AS different_actions,
    COUNT(DISTINCT create_date) AS days_with_actions,
    SUM(quantity) AS total_actions
FROM cdm.f_activity
GROUP BY customer_id;

-- Агрегация по заказам
CREATE TEMP TABLE tmp_agg_orders ON COMMIT DROP AS
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS uniq_orders,
    COUNT(DISTINCT create_date) AS days_with_orders,
    COUNT(DISTINCT city_id) AS cities_visited,
    COUNT(DISTINCT item_id) AS different_items_bought,
    SUM(payment_amount) AS money_spent
FROM cdm.f_order
GROUP BY customer_id;

-- Сбор отчёта
INSERT INTO rep.customer_report (
    customer_id, first_name, last_name,
    uniq_actions, different_actions, days_with_actions,
    total_actions, uniq_orders, days_with_orders,
    cities_visited, different_items_bought, money_spent
)
SELECT
    dc.id AS customer_id,
    dc.first_name,
    dc.last_name,
    COALESCE(a.uniq_actions, 0) AS uniq_actions,
    COALESCE(a.different_actions, 0) AS different_actions,
    COALESCE(a.days_with_actions, 0) AS days_with_actions,
    COALESCE(a.total_actions, 0) AS total_actions,
    COALESCE(o.uniq_orders, 0) AS uniq_orders,
    COALESCE(o.days_with_orders, 0) AS days_with_orders,
    COALESCE(o.cities_visited, 0) AS cities_visited,
    COALESCE(o.different_items_bought, 0) AS different_items_bought,
    COALESCE(o.money_spent, 0) AS money_spent
FROM cdm.d_customer dc
LEFT JOIN tmp_agg_actions a ON a.customer_id = dc.id
LEFT JOIN tmp_agg_orders o ON o.customer_id = dc.id
WHERE dc.end_date = '9999-12-31'::date;

COMMIT;