--olmayan hesap--
SELECT * FROM accounts WHERE account_id = 9999;

--orphan transaction var mı?--
SELECT t.*
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;
--sonuç boş dönmeli(0 kayıt)!!!--

--kaç tane orphan transaction var?--
SELECT COUNT(*) AS orphan_transaction_count
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

--hangi account_id'ler orphan??--
SELECT DISTINCT t.account_id
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

--tüm orphan transaction'ları listele(sonuç 0)--
SELECT t.*
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

--EXISTS ile kontrol--
SELECT COUNT(*) AS orphan_transaction_count
FROM transactions t
WHERE NOT EXISTS( SELECT 1 FROM accounts a WHERE a.account_id = t.account_id);
