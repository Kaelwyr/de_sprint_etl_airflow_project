INSERT INTO cdm.f_customer_research(date_id, category_id, city_id, sales_qty, sales_amt )
SELECT
    date_id,
    category_id,
    c.city_id ,
    sales_qty,
    sales_amt
FROM ods.customer_research r
 JOIN cdm.d_city c on r.geo_id = c.city_id
  WHERE date_id = '{{ ds }}'::date