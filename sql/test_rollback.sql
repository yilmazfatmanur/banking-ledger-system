--rollback testi--
BEGIN TRANSACTION;

UPDATE accounts SET balance = 999 WHERE account_id = 2;
SELECT balance FROM accounts WHERE account_id = 2;

ROLLBACK;

SELECT balance FROM accounts WHERE account_id = 2;

--commit testi--
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance + 1 WHERE account_id = 2;
COMMIT;
SELECT balance FROM accounts WHERE account_id = 2;

--bakiye yetersizlik testi--
--id2 (ayse) 1000tl çeksin (bakiye yetersiz)
SELECT balance FROM accounts WHERE account_id = 2;

