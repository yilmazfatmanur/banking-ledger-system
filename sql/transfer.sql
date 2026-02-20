--id2 ide1'a 300tl gönderiyor--

--ilk bakiye check--
BEGIN TRANSACTION;
SELECT balance FROM accounts
WHERE account_id = 2;

--transaction(gönderen)--
INSERT INTO transactions (account_id, type, amount)
VALUES (2, 'transfer_out', 300);

--transaction(alıcı)--
INSERT INTO transactions (account_id, type, amount)
VALUES(1, 'transfer_in', 300);

--update bakiye(gönderen)--
UPDATE accounts SET balance = balance - 300 WHERE account_id = 2;

--update bakiye(alıcı)--
UPDATE accounts SET balance = balance + 300 WHERE account_id = 1;

INSERT INTO ledger ( transactions_id, debit_account, credit_account, amount)
VALUES(3, 2, 1, 300);

COMMIT;
--checking--
SELECT * FROM accounts WHERE account_id IN (1,2); 