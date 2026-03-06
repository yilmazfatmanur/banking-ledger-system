--ledger'dan bakiyeyi yeniden oluşturma testi--
--her hesap için ledger'dan bakiye hesaplama/test1--
SELECT 
    a.account_id,
    a.balance AS mevcut_bakiye,
    COALESCE((SELECT SUM(amount) FROM ledger WHERE debit_account = a.account_id), 0) -
    COALESCE((SELECT SUM(amount) FROM ledger WHERE credit_account = a.account_id), 0) AS ledger_bakiye,
    a.balance - (
        COALESCE((SELECT SUM(amount) FROM ledger WHERE debit_account = a.account_id), 0) -
        COALESCE((SELECT SUM(amount) FROM ledger WHERE credit_account = a.account_id), 0)
    ) AS fark
FROM accounts a;

--transaction'dan bakiye hesaplama/test2--
SELECT
    a.account_id,
    a.balance AS mevcut_bakiye,
    COALESCE((SELECT SUM(amount) FROM transactions WHERE account_id = a.account_id AND type = 'deposit'), 0) -
    COALESCE((SELECT SUM(amount) FROM transactions WHERE account_id = a.account_id AND type = 'withdraw'), 0) AS transaction_bakiye,
    a.balance - (
        COALESCE((SELECT SUM(amount) FROM transactions WHERE account_id = a.account_id AND type = 'deposit'), 0) - 
        COALESCE((SELECT SUM(amount) FROM transactions WHERE account_id = a.account_id AND type = 'withdraw'), 0)
    ) AS fark
FROM accounts a;
-- sonuç 0 olmalı--
--COALESCE sorgusu eğer bir NULL değeri varsa yerini başka değerle değiştirmek için kullanılır--