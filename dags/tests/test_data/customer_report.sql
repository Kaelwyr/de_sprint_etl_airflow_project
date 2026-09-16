INSERT INTO rep.customer_report(customer_id ,first_name, last_name, uniq_actions,
                            different_actions,
                            days_with_actions,
                            total_actions, uniq_orders, days_with_orders,
                            cities_visited, different_items_bought, money_spent)
OVERRIDING SYSTEM VALUE
VALUES
(2,'Константин','Смирнов',1,1,1,1,0,0,0,0,0);