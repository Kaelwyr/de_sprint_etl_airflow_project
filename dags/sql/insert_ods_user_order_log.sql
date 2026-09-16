INSERT INTO ods.user_order_log( uniq_id, date_time, city_id, city_name, customer_id, first_name, last_name, item_id,
                                item_name, quantity, payment_amount)
select
       uniq_id,
       max(date_time),
       max(city_id),
       max(city_name),
       max(customer_id),
       max(first_name),
       max(last_name),
       max(item_id),
       max(item_name),
       max(quantity),
       max(payment_amount)
from raw.user_order_log uol
group by uniq_id