INSERT INTO raw.user_activity_log(
ID,
uniq_id,
date_time,
action_id ,
customer_id,
quantity)
VALUES (%(id)s,
%(uniq_id)s,
%(date_time)s,
%(action_id)s,
%(customer_id)s,
%(quantity)s)