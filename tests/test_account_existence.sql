--account existence testi--
--var olmayan hesap kontrolü/test1--
SELECT 
    t.transactions_id,
    t.account_id,
    t.type,
    t.amount
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

--ledger'da olmayan hesap kontrolü/test2--
SELECT 
    l.ledger_id,
    l.debit_account,
    l.credit_account
FROM ledger l
WHERE l.debit_account NOT IN (0)
AND l.debit_account NOT IN (SELECT account_id FROM accounts)
 OR l.credit_account NOT IN (0)
AND l.credit_account NOT IN (SELECT account_id FROM accounts);
--beklenen sonuç 0--
--0=banka kasası--
