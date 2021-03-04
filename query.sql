SELECT id, name, author_id, uuid FROM budget_family INNER JOIN budget_family_users ON budget_family.id = budget_family_users.family_id) WHERE budget_family_users.user_id = 1

SELECT budget_operation.id, budget_operation.value, budget_operation.date, budget_operation.description, budget_operation.category_id, budget_operation.user_id FROM budget_operation WHERE budget_operation.user_id = 1 AND budget_operation.date >= '2021-02-01' AND budget_operation.date < '2021-03-01' AND budget_operation.date <= '2021-03-05' ORDER BY budget_operation.date DESC, budget_operation.id DESC;
SELECT budget_category.id, budget_category.name, budget_category.user_id, budget_category.type_pay FROM budget_category WHERE budget_category.id = 1
SELECT budget_category.id, budget_category.name, budget_category.user_id, budget_category.type_pay FROM budget_category WHERE budget_category.user_id = 1 ORDER BY budget_category.type_pay ASC, budget_category.name ASC;
DELETE FROM budget_category WHERE budget_category.id IN (91);

SELECT budget_category.name, CAST(SUM(budget_operation.value) AS NUMERIC) AS total FROM budget_operation INNER JOIN budget_category ON (budget_operation.category_id=budget_category.id) WHERE (budget_category.type_pay = 0 AND budget_operation.user_id = 1 AND strftime('%m', budget_operation.date)*1 = 2 AND budget_operation.date BETWEEN '2021-01-01' AND '2021-12-31') GROUP BY budget_category.name;

