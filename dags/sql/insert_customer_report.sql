BEGIN;

DELETE FROM rep.customer_report;

INSERT INTO rep.customer_report(customer_id ,first_name, last_name, uniq_actions, different_actions,
                            days_with_actions,
                            total_actions, uniq_orders, days_with_orders,
                            cities_visited, different_items_bought, money_spent)
    WITH
         agg_actions AS (
               SELECT customer_id,
               COUNT(DISTINCT ual.activity_id)      AS uniq_actions,
               COUNT(DISTINCT action_id)        AS different_actions,
               COUNT(DISTINCT ual.create_date)    AS days_with_actions,
               SUM(ual.quantity)                AS total_actions
               FROM cdm.f_activity ual
               GROUP BY customer_id ),
         agg_orders AS (
               SELECT customer_id,
               COUNT(DISTINCT uol.order_id)      AS uniq_orders,
               COUNT(DISTINCT uol.create_date)    AS days_with_orders,
               COUNT(DISTINCT city_id)          AS cities_visited,
               COUNT(DISTINCT item_id)          AS different_items_bought,
               SUM(payment_amount)              AS money_spent
               FROM cdm.f_order uol
               GROUP BY customer_id )
    SELECT dc.customer_id ,
            dc.first_name ,
            dc.last_name ,
           uniq_actions,
           different_actions,
           days_with_actions,
           total_actions,
           uniq_orders,
           days_with_orders,
           cities_visited,
           different_items_bought,
           money_spent
    FROM agg_actions ual
    FULL JOIN agg_orders uol USING (customer_id)
    JOIN cdm.d_customer dc
         ON dc.id = COALESCE(ual.customer_id, uol.customer_id)
            AND dc.end_date = '9999-12-31'::date;

COMMIT;