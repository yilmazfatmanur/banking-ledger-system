--bakiye hesaplama test--
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

-- başlangıç bakiye 1000tl--
UPDATE accounts SET balance = 1000.00 WHERE account_id IN (1,2);

--para yatırma işlemi kontrolu / test1--
INSERT INTO transactions (account_id, type, amount)
VALUES (2, 'deposit', 500.00);

--bakiye kontrolü--
SELECT 
    a.balance AS guncel_bakiye,
    1500.00 AS beklenen_bakiye,
    CASE 
        WHEN a.balance = 1500.00 THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM accounts a
WHERE a.account_id = 2;

--para çekme işlemi kontrolu / test2--
INSERT INTO transactions (account_id, type, amount)
VALUES (1, 'withdraw', 300.00);  -- 'withdrawal' değil 'withdraw'

SELECT
    a.balance AS guncel_bakiye,
    700.00 AS beklenen_bakiye,
    CASE 
        WHEN a.balance = 700.00 THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM accounts a
WHERE a.account_id = 1;

--transfer işlemi kontrolu / test3--
INSERT INTO transactions (account_id, type, amount)
VALUES 
    (1, 'withdraw', 200.00),
    (2, 'deposit', 200.00);

SELECT
    a.account_id,   
    a.balance AS guncel_bakiye,
    CASE
        WHEN a.account_id = 1 THEN 500.00
        WHEN a.account_id = 2 THEN 1700.00
    END AS beklenen_bakiye,
    CASE 
        WHEN (a.account_id = 1 AND a.balance = 500.00) OR
             (a.account_id = 2 AND a.balance = 1700.00) THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM accounts a
WHERE a.account_id IN (1, 2)  -- virgül kaldırıldı
ORDER BY a.account_id;

--toplam bakiye kontrolu / test4--
SELECT
    SUM(balance) AS toplam_bakiye,
    2200.00 AS beklenen_toplam_bakiye,
    CASE 
        WHEN SUM(balance) = 2200.00 THEN 'Test Passed'
        ELSE 'Test Failed'
    END AS sonuc
FROM accounts a  -- 'a' eklendi, virgül kaldırıldı
WHERE a.account_id IN (1, 2);

--testleri geri al--
ROLLBACK;