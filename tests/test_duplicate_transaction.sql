--duplicate transaction testi--
--aynı transaction_id'ye sahip işlemler kontrolü/test1--
SELECT
    account_id,
    type,
    amount,
    COUNT(*)AS adet
FROM transactions
GROUP BY account_id, type, amount
HAVING COUNT(*) > 1;
--beklenen sonuç 0--

--ledger'da duplicate kontrolü/test2--
SELECT
    transactions_id,
    debit_account,
    credit_account,
    amount,
    COUNT(*)AS adet
FROM ledger
GROUP BY transactions_id, debit_account, credit_account, amount
HAVING COUNT(*) > 1;
--beklenen sonuç 0--

