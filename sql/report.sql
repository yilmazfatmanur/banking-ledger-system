--id'1 işlem geçmişi--
SELECT 
    t.transactions_id,
    t.type AS işlem_tipi,
    t.amount AS tutar,
    a.balance AS güncel_bakiye
FROM transactions t 
JOIN accounts a ON t.account_id = a.account_id
WHERE t.account_id = 1
ORDER BY t.transactions_id DESC;

--tüm işlem rapor--
SELECT
    c.name AS müşteri,
    t.transactions_id,
    t.type AS işlem_tipi,
    t.amount AS tutar,
    a.balance AS bakiye
FROM transactions t 
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
ORDER BY t.transactions_id DESC;

--transfer detay rapor--
SELECT
    l.ledger_id,
    c1.name AS gönderen,
    c2.name AS alıcı,
    l.amount AS tutar
FROM ledger l 
JOIN accounts a1 ON l.debit_account = a1.account_id
JOIN customers c1 ON a1.customer_id = c1.customer_id
JOIN accounts a2 ON l.credit_account = a2.account_id
JOIN customers c2 ON a2.customer_id = c2.customer_id
WHERE l.debit_account !=0 AND l.credit_account !=0
ORDER BY l.ledger_id DESC;

--bankagenel rapor--
--toplam müşteri sayısı--
SELECT COUNT(*) AS toplam_müşteri FROM customers;

-- toplam hesap sayısı--
SELECT COUNT(*) AS toplam_hesap FROM accounts;

--toplam bankadaki para--
SELECT SUM(balance) AS toplam_bakiye FROM accounts;

--toplam işlem sayısı--
SELECT COUNT(*) AS toplam_işlem FROM transactions;


--işlem tipleri--
SELECT 
    type AS işlem_tipi,
    COUNT(*) AS adet,
    SUM(amount) AS toplam_tutar
FROM transactions
GROUP BY type;



