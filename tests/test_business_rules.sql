--iş mantığı kurallarının testi--
--negatif bakiye kontrolü/test1--
SELECT account_id, balance
FROM accounts
WHERE balance < 0;

--günlük işlem limit kontrolü/test2--
SELECT
    account_id,
    DATE(transactions_date) AS islem_gunu,
    SUM(amount) AS gunluk_toplam
FROM transactions
GROUP BY account_id, DATE(transactions_date)
HAVING SUM(amount) > 10000;

--minimum işlem tutarı  kontrolü/test3--
SELECT *
FROM transactions
WHERE amount < 1;

--maksimum işlem tutarı kontrolü/test4--
SELECT *
FROM transactions
WHERE amount > 5000;

--aynı anda çift işlem kontrolü/test5--
SELECT
    t1.transactions_id AS islem1_id,
    t1.account_id AS hesap_id,
    t1.type AS tip,
    t1.amount AS tutar,
    t2.transactions_id AS islem2_id,
    strftime('%s', t2.rowid) - strftime('%s', t1.rowid) AS saniye_farki
FROM transactions t1
JOIN transactions t2 
    ON t1.account_id = t2.account_id
    AND t1.type = t2.type
    AND t1.amount = t2.amount
    AND t1.transactions_id < t2.transactions_id
WHERE ABS(strftime('%s', t2.rowid) - strftime('%s', t1.rowid)) < 5;
--hafta sonu işlem kontrolü/test6--
SELECT *
FROM transactions
WHERE strftime('%w', transactions_date) IN ('0','6');

--bakiyeden fazla çekim kontrolü/test7--
SELECT 
    t.transactions_id,
    t.account_id,
    t.amount AS cekilen_tutar,
    a.balance AS mevcut_bakiye
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
WHERE t.type = 'withdraw'
  AND t.amount > a.balance;


--sıfır işlem kontrolü/test8--
SELECT *
FROM transactions
WHERE amount = 0 OR amount IS NULL;


