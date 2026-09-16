INSERT INTO ods.user_activity_log( uniq_id, date_time, action_id, customer_id, quantity)
select
       uniq_id,
       max(date_time),
       max(action_id),
       max(customer_id),
       max(quantity)
from raw.user_activity_log ual
group by uniq_id;