INSERT INTO ods.customer_research(date_id, category_id, geo_id, sales_qty, sales_amt )
SELECT
    date_id,
    category_id,
    geo_id ,
    max(sales_qty) as sales_qty,
    max(sales_amt) as sales_amt
FROM raw.customer_research
  WHERE date_id = '{{ ds }}'::date
 GROUP BY date_id, category_id, geo_id