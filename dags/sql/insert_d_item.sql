BEGIN TRANSACTION;

UPDATE cdm.d_item
set end_date = '{{ ds }}'::date - interval '1 day'
WHERE id IN (SELECT id
             FROM stg.d_item
             WHERE id IS NOT NULL); --обновляем end_date

INSERT INTO cdm.d_item(item_id, item_name, start_date, end_date)
SELECT stg.item_id,
       stg.item_name,
       '{{ ds }}',
       '9999-12-31'
FROM stg.d_item stg; -- вставляем актуальное инфо

COMMIT TRANSACTION;