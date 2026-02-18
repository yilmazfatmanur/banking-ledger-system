--ps: debit(borç)=müşterini hesabı/ credit(alacak)=bankanın kasa hesabı--
--transaction ekleeme--
INSERT INTO transactions(account_id, type, amount)
VALUES (1 , 'deposit', 500);

--bakiyesel işlemler--
UPDATE accounts
SET balance = balance + 500
WHERE account_id = 1;

--ledger'a kayıt atma--
INSERT INTO ledger (transactions_id, debit_account, credit_account, amount)
VALUES (1, 1, 0 ,500);

SELECT * FROM accounts WHERE account_id = 1;