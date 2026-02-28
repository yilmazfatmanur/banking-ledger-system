--veri bütünlük testleri--
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

--geçersiz transaction tipi kontrolü /test1--
INSERT INTO transactions (account_id, type, amount)
VALUES (1, 'gecersiz_tip', 100.00);
SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE type = 'gecersiz_tip') = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--NULL account_id kontrolü / test2--
INSERT OR IGNORE INTO transactions (account_id, type, amount)
VALUES (NULL, 'deposit', 100.00);

SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE account_id IS NULL) = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--NULL amount kontrolü / test3--
INSERT OR IGNORE INTO transactions (account_id, type, amount)
VALUES (1, 'deposit', -50.00);

SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE amount < 0) = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--negatif amount kontrolü / test4--
INSERT OR IGNORE INTO transactions (account_id, type, amount)
VALUES (1, 'deposit', -50.00);
SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE amount < 0) = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--geçersiz account_id(foreign key)kontrolü / test5--
INSERT OR IGNORE INTO transactions (account_id, type, amount)
VALUES (999, 'deposit', 100.00);

SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE account_id = 999) = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--transaction sonrası bakiye update kontrolü / test6--
UPDATE accounts SET balance = 100.00 WHERE account_id = 1;
INSERT INTO transactions (account_id, type, amount)
VALUES (1, 'deposit', 250.00);

SELECT 
    a.balance AS guncel_bakiye,
    1250.00 AS beklenen_bakiye,
    CASE 
        WHEN a.balance = 1250.00 THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM accounts a
WHERE a.account_id = 1;

--çoklu transaction testi / test7--
INSERT INTO transactions (account_id, type, amount) VALUES 
    (2, 'deposit', 50.00),
    (2, 'deposit', 75.00),
    (2, 'deposit', 35.00);

SELECT
    COUNT(*) AS islem_sayisi,
    3 AS beklenen_islem_sayisi,
    CASE 
        WHEN COUNT(*) = 3 THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM transactions
WHERE account_id = 2 AND julianday('now') - julianday(date) < 1;  -- son 24 saat içinde yapılan işlemler--

--account işlem özeti kontrolü / test8--
SELECT 
   account_id,
   COUNT(*) AS toplam_islem,
    SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) AS toplam_yatirma,
    SUM(CASE WHEN type = 'withdraw' THEN amount ELSE 0 END) AS toplam_cekme,
FROM transactions
WHERE account_id IN (1,2)
GROUP BY account_id;

--transaction atomcity kontrolü / test9--
BEGIN TRANSACTION;
    INSERT INTO transactions (account_id, type, amount) VALUES (1, 'withdraw', 100.00);
    INSERT INTO transactions (account_id, type, amount) VALUES (999, 'deposit', 100.00);
COMMIT;

SELECT 
   CASE 
         WHEN (SELECT COUNT(*) FROM transactions WHERE account_id = 1 AND amount = 100.00 AND type = 'withdraw' AND  julianday('now') - julianday(date) < 1) = 0 
         THEN 'Test Passed'
         ELSE 'Test Failed'
    END AS sonuc;

--test sonuçları--
SELECT '==Test Sonuçları==' AS '';
SELECT 'Toplam transaction : '|| COUNT(*) FROM transactions WHERE type = 'deposit';
SELECT 'Deposit' || COUNT(*) FROM transactions WHERE type = 'deposit';
SELECT 'Withdraw' || COUNT(*) FROM transactions WHERE type = 'withdraw';

--testleri geri al--
ROLLBACK;
   