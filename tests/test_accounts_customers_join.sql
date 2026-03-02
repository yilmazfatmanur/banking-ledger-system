--tüm hesaplar--
SELECT 
    a.account_id,
    a.customer_id,
    c.name,
    a.balance
FROM  accounts a
JOIN customers c ON a.customer_id = c.customer_id;

--orphan (müşteri olmayan hesaplar) var mı check--
SELECT 
    a.account_id,
    a.customer_id,
    a.balance
FROM  accounts a
LEFT JOIN customers c ON a.customer_id = c.customer_id
WHERE c.customer_id IS NULL;