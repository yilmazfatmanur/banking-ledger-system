SELECT 
    customers.customer_id,
    customers.name AS müşteri_adı,
    accounts.account_id AS hesap_no,
    accounts.balance AS bakiye
FROM accounts
JOIN customers ON accounts.customer_id = customers.customer_id
ORDER BY customers.name;