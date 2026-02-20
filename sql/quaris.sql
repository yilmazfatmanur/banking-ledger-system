--checking--
SELECT balance FROM accounts
WHERE account_id = 2;

--kayıt--
INSERT INTO transactions (account_id, type, amount)
VALUES (2,'withdraw', 200 );

--bakiye azaltma--
UPDATE accounts
SET  balance = balance - 200
WHERE account_id = 2;

--ledger kaydı--
INSERT INTO ledger (transactions_id, debit_account, credit_account, amount)
VALUES(2, 0, 2, 500);

SELECT * From accounts WHERE account_id = 2; 

