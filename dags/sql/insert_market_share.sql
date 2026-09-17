BEGIN;

INSERT INTO rep.market_share_report(date_time, city_id, qty_share, amt_share)

WITH competition AS (
    SELECT date_time,
           city_id,
           sum(sales_qty) total_qty,
           sum(sales_amt) total_amt
    FROM cdm.f_customer_research cr
    GROUP BY date_time, city_id
),
ours AS (
    SELECT create_date,
           city_id,
           sum(quantity) total_qty,
           sum(payment_amount) total_amt
    FROM cdm.f_order uol
    GROUP BY create_date , city_id
)
SELECT
    o.create_date AS date_time,
    o.city_id,
    COALESCE(o.total_qty::numeric / NULLIF(o.total_qty + c.total_qty, 0), 0) AS qty_share,
    COALESCE(o.total_amt::numeric / NULLIF(o.total_amt + c.total_amt, 0), 0) AS amt_share
FROM ours o
INNER JOIN competition c ON o.create_date = c.date_time AND o.city_id  = c.city_id
    ON CONFLICT (date_time, city_id) DO UPDATE
        SET qty_share = EXCLUDED.qty_share, amt_share = EXCLUDED.amt_share;

COMMIT;