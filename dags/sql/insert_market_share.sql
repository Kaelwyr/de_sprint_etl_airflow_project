INSERT INTO rep.market_share_report( date_id, city_id, qty_share, amt_share)
WITH competition AS (
    SELECT date_id,
           city_id,
           sum(sales_qty) total_qty,
           sum(sales_amt) total_amt
        FROM cdm.f_customer_research cr
    GROUP BY date_id, city_id),
ours AS (
    SELECT create_date,
           city_id,
           sum(quantity) total_qty,
           sum(payment_amount) total_amt
        FROM cdm.f_order uol
    GROUP BY create_date , city_id )
SELECT
        create_date,
        o.city_id,
        o.total_qty/(o.total_qty + c.total_qty) as qty_share,
        o.total_amt/(o.total_amt + c.total_amt) as amt_share
    FROM ours o
        JOIN competition c
ON o.create_date = c.date_id AND o.city_id  = c.city_id
ON CONFLICT (date_id, city_id) DO UPDATE
SET qty_share = EXCLUDED.qty_share,
amt_share = EXCLUDED.amt_share
;