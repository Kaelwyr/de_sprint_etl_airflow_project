INSERT INTO raw.customer_research(
date_id,
category_id,
geo_id,
sales_qty,
sales_amt)
VALUES (
%(date_id)s,
%(category_id)s,
%(geo_id)s,
%(sales_qty)s,
%(sales_amt)s)