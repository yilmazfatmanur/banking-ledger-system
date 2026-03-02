--transaction ve ledger karşılaştırma--
--tüm kayıtlar /test1--
SELECT 
    t.transactions_id,
    t.type,
    t.amount,
    l.ledger_id,
    l.amount AS ledger_amount
FROM transactions t
LEFT JOIN ledger l ON t.transactions_id = l.transactions_id
WHERE t.account_id = 1;

--tutarların eşleşmediği kayıtlar(HATA durumu) /test2--
SELECT
    t.transactions_id,
    t.amount AS transaction_tutar,
    l.amount AS ledger_tutar
FROM transactions t
JOIN ledger l ON t.transactions_id = l.transactions_id
WHERE t.account_id = 1 AND t.amount != l.amount OR l.amount IS NULL;
 


